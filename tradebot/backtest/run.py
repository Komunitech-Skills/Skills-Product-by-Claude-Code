"""Backtest CLI: fetch/cache data, run in-sample and out-of-sample, write a report.

Usage (from tradebot/):  python -m backtest.run [--config config.yaml] [--offline]
"""
from __future__ import annotations

import argparse
import json
import logging
import math
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from backtest.metrics import Metrics, compute_metrics, oos_flags, segment_flags
from backtest.simulator import SimResult, buy_and_hold, simulate
from core.config import ROOT, Config, load_config
from core.data import (
    MS_PER_YEAR,
    OhlcvCache,
    check_quality,
    fetch_market_filters,
    load_history,
    make_exchange,
)
from core.logging_setup import setup_logging

log = logging.getLogger("backtest")


def split_index(df: pd.DataFrame, warmup: int, in_sample_years: float) -> int:
    """First positional index of the out-of-sample segment."""
    split_ts = int(df["ts"].iloc[warmup]) + int(in_sample_years * MS_PER_YEAR)
    return int((df["ts"].to_numpy() < split_ts).sum())


def run_segment(cfg: Config, df: pd.DataFrame, filters, start: int, end: int) -> tuple[SimResult, Metrics]:
    res = simulate(
        df, cfg.strategy, cfg.costs, filters,
        initial_equity=cfg.risk.initial_equity, risk_pct=cfg.risk.risk_per_trade_pct,
        start=start, end=end,
    )
    bh = buy_and_hold(df, cfg.costs, cfg.risk.initial_equity, res.first_index, res.last_index + 1)
    m = compute_metrics(res, bh, cfg.backtest["periods_per_year"], cfg.report_flags.top_trades_for_dependency)
    return res, m


def _fmt(x: float, pct: bool = False) -> str:
    if isinstance(x, float) and math.isinf(x):
        return "∞"
    return f"{x:.2%}" if pct else f"{x:.2f}"


def metrics_table(rows: dict[str, Metrics]) -> str:
    spec = [
        ("Periode", lambda m: f"{m.start[:10]} → {m.end[:10]}"),
        ("Candle", lambda m: str(m.n_candles)),
        ("Jumlah trade", lambda m: str(m.n_trades)),
        ("Win rate", lambda m: _fmt(m.win_rate, True)),
        ("Profit factor", lambda m: _fmt(m.profit_factor)),
        ("PF tanpa 2 trade terbesar", lambda m: _fmt(m.profit_factor_ex_top)),
        ("Expectancy / trade (USDT)", lambda m: f"{m.expectancy_usdt:+.2f}"),
        ("Expectancy / trade (R)", lambda m: f"{m.expectancy_r:+.3f}"),
        ("Rata-rata menang / kalah (R)", lambda m: f"{m.avg_win_r:+.2f} / {m.avg_loss_r:+.2f}"),
        ("Max drawdown", lambda m: _fmt(m.max_drawdown, True)),
        ("Sharpe (√2190)", lambda m: _fmt(m.sharpe)),
        ("Total return", lambda m: _fmt(m.total_return, True)),
        ("Equity akhir (USDT)", lambda m: f"{m.final_equity:,.2f}"),
        ("Exposure (waktu di pasar)", lambda m: _fmt(m.exposure, True)),
        ("Buy & hold return", lambda m: _fmt(m.bh_return, True)),
        ("Buy & hold max DD", lambda m: _fmt(m.bh_max_drawdown, True)),
        ("Buy & hold Sharpe", lambda m: _fmt(m.bh_sharpe)),
        ("Exit (alasan)", lambda m: ", ".join(f"{k} {v}" for k, v in sorted(m.exit_reasons.items())) or "-"),
        ("Sinyal di-skip", lambda m: ", ".join(f"{k} {v}" for k, v in sorted(m.skip_reasons.items())) or "-"),
    ]
    head = "| Metrik | " + " | ".join(rows) + " |\n|---|" + "---|" * len(rows) + "\n"
    return head + "".join(f"| {name} | " + " | ".join(fn(m) for m in rows.values()) + " |\n" for name, fn in spec)


def trades_frame(res: SimResult, segment: str) -> pd.DataFrame:
    def iso(ms: int | None) -> str:
        return pd.Timestamp(ms, unit="ms", tz="UTC").isoformat() if ms is not None else ""

    return pd.DataFrame(
        [
            {
                "segment": segment, "signal_time": iso(t.signal_ts), "entry_time": iso(t.entry_ts),
                "entry": round(t.entry_price, 2), "stop_loss": round(t.stop_loss, 2),
                "take_profit": round(t.take_profit, 2), "qty": t.qty, "exit_time": iso(t.exit_ts),
                "exit": round(t.exit_price or 0.0, 2), "exit_reason": t.exit_reason,
                "pnl_usdt": round(t.pnl, 4), "r": round(t.r_multiple, 3),
                "equity_before": round(t.equity_before, 2),
            }
            for t in res.trades
        ]
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=str(ROOT / "config.yaml"))
    ap.add_argument("--offline", action="store_true", help="pakai cache SQLite saja, tanpa fetch")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    cfg = load_config(args.config)
    p = cfg.strategy

    if args.offline:
        df = OhlcvCache(ROOT / cfg.data["db_path"]).load(cfg.symbol, cfg.timeframe)
        filters = cfg.fallback_filters
    else:
        exchange = make_exchange(cfg)
        df = load_history(cfg, exchange=exchange)
        filters = fetch_market_filters(exchange, cfg.symbol, cfg.fallback_filters)

    quality = check_quality(df, cfg.timeframe)
    log.info("data_quality", extra={"n": quality.n_candles, "gaps": len(quality.gaps),
                                    "missing": quality.missing_candles, "bad_ohlc": quality.bad_ohlc_rows})
    if quality.bad_ohlc_rows:
        raise SystemExit("data OHLC tidak konsisten; berhenti (jangan menebak)")
    if len(df) <= p.warmup_candles + 1:
        raise SystemExit("data kurang dari warm-up")

    split = split_index(df, p.warmup_candles, cfg.backtest["in_sample_years"])
    segments = {
        "In-sample": (p.warmup_candles, split),
        "Out-of-sample": (split, len(df)),
        "Penuh (referensi)": (p.warmup_candles, len(df)),
    }
    results: dict[str, tuple[SimResult, Metrics]] = {
        name: run_segment(cfg, df, filters, s, e) for name, (s, e) in segments.items()
    }
    is_m, oos_m = results["In-sample"][1], results["Out-of-sample"][1]
    flags = (
        segment_flags(is_m, cfg.report_flags, "IS")
        + segment_flags(oos_m, cfg.report_flags, "OOS")
        + oos_flags(is_m, oos_m, cfg.report_flags)
    )

    out_dir = ROOT / cfg.backtest["report_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    trades = pd.concat(
        [trades_frame(results[k][0], k) for k in ("In-sample", "Out-of-sample")], ignore_index=True
    )
    trades.to_csv(out_dir / f"backtest-{stamp}-trades.csv", index=False)
    (out_dir / f"backtest-{stamp}.json").write_text(
        json.dumps({k: v[1].as_dict() for k, v in results.items()} | {"flags": flags,
                   "filters": {k: str(v) for k, v in vars(filters).items()},
                   "data_gaps": quality.gaps}, indent=2, default=str),
        encoding="utf-8",
    )
    first = df.index[0].isoformat()
    report = (
        f"# Backtest {cfg.symbol} {cfg.timeframe} — EMA {p.ema_fast}/{p.ema_slow} + RSI {p.rsi_period} "
        f"[{p.rsi_min}–{p.rsi_max}] + EMA{p.ema_trend}\n\n"
        f"Dibuat {datetime.now(timezone.utc).isoformat(timespec='seconds')}. Data {first[:10]} → "
        f"{df.index[-1].isoformat()[:16]} UTC, {len(df)} candle tertutup "
        f"(warm-up {p.warmup_candles} candle tidak diperdagangkan). "
        f"Gap data: {len(quality.gaps)} ({quality.missing_candles} candle hilang).\n\n"
        f"Modal {cfg.risk.initial_equity:,.0f} USDT per segmen (dimulai ulang), risiko "
        f"{cfg.risk.risk_per_trade_pct:.0%} equity/trade (fee-aware), fee {cfg.costs.fee_pct:.2%}/sisi, "
        f"slippage {cfg.costs.slippage_pct:.2%}. Filter: stepSize {filters.step_size}, "
        f"minNotional {filters.min_notional}.\n\n"
        + metrics_table({k: v[1] for k, v in results.items()})
        + "\n## Flag overfit / tidak meyakinkan\n\n"
        + ("".join(f"- ⚠️ {f}\n" for f in flags) if flags else "- Tidak ada flag.\n")
    )
    (out_dir / f"backtest-{stamp}.md").write_text(report, encoding="utf-8")
    for name, (_, m) in results.items():
        log.info("segment_result", extra={"segment": name, "trades": m.n_trades,
                                          "return": round(m.total_return, 4), "pf": m.profit_factor,
                                          "max_dd": round(m.max_drawdown, 4), "bh_return": round(m.bh_return, 4)})
    for f in flags:
        log.warning("flag", extra={"detail": f})
    log.info("report_written", extra={"path": str(out_dir / f"backtest-{stamp}.md")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
