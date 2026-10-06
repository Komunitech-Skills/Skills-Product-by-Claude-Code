"""Backtest metrics and overfit / unconvincing-result flags."""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd

from backtest.simulator import SimResult
from core.config import ReportFlags


@dataclass(frozen=True)
class Metrics:
    n_trades: int
    win_rate: float
    profit_factor: float
    profit_factor_ex_top: float          # PF after removing the N largest winners
    expectancy_usdt: float
    expectancy_r: float
    avg_win_r: float
    avg_loss_r: float
    max_drawdown: float                  # fraction, positive
    sharpe: float
    total_return: float
    final_equity: float
    exposure: float                      # fraction of candles holding a position
    bh_return: float
    bh_max_drawdown: float
    bh_sharpe: float
    exit_reasons: dict[str, int]
    skip_reasons: dict[str, int]
    start: str
    end: str
    n_candles: int

    def as_dict(self) -> dict:
        return asdict(self)


def max_drawdown(equity: pd.Series, initial: float) -> float:
    curve = np.concatenate([[initial], equity.to_numpy(dtype=float)])
    peak = np.maximum.accumulate(curve)
    return float(np.max(1.0 - curve / peak))


def sharpe(equity: pd.Series, initial: float, periods_per_year: int) -> float:
    curve = np.concatenate([[initial], equity.to_numpy(dtype=float)])
    rets = np.diff(curve) / curve[:-1]
    sd = rets.std(ddof=1)
    return float(rets.mean() / sd * math.sqrt(periods_per_year)) if sd > 0 else 0.0


def profit_factor(pnls: list[float]) -> float:
    gp = sum(p for p in pnls if p > 0)
    gl = -sum(p for p in pnls if p < 0)
    if gl == 0:
        return math.inf if gp > 0 else 0.0
    return gp / gl


def compute_metrics(res: SimResult, bh: pd.Series, periods_per_year: int, top_n: int) -> Metrics:
    pnls = [t.pnl for t in res.trades]
    rs = [t.r_multiple for t in res.trades]
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r <= 0]
    ex_top = sorted(pnls, reverse=True)[top_n:] if len(pnls) > top_n else []
    in_pos = sum(
        int(((res.equity.index >= pd.Timestamp(t.entry_ts, unit="ms", tz="UTC"))
             & (res.equity.index <= pd.Timestamp(t.exit_ts, unit="ms", tz="UTC"))).sum())
        for t in res.trades
    )
    final = float(res.equity.iloc[-1])
    return Metrics(
        n_trades=len(res.trades),
        win_rate=len(wins) / len(rs) if rs else 0.0,
        profit_factor=profit_factor(pnls),
        profit_factor_ex_top=profit_factor(ex_top),
        expectancy_usdt=float(np.mean(pnls)) if pnls else 0.0,
        expectancy_r=float(np.mean(rs)) if rs else 0.0,
        avg_win_r=float(np.mean(wins)) if wins else 0.0,
        avg_loss_r=float(np.mean(losses)) if losses else 0.0,
        max_drawdown=max_drawdown(res.equity, res.initial_equity),
        sharpe=sharpe(res.equity, res.initial_equity, periods_per_year),
        total_return=final / res.initial_equity - 1.0,
        final_equity=final,
        exposure=in_pos / len(res.equity),
        bh_return=float(bh.iloc[-1]) / res.initial_equity - 1.0,
        bh_max_drawdown=max_drawdown(bh, res.initial_equity),
        bh_sharpe=sharpe(bh, res.initial_equity, periods_per_year),
        exit_reasons=dict(Counter(t.exit_reason for t in res.trades)),
        skip_reasons=dict(Counter(s.reason for s in res.skipped)),
        start=str(res.equity.index[0]),
        end=str(res.equity.index[-1]),
        n_candles=len(res.equity),
    )


def segment_flags(m: Metrics, f: ReportFlags, label: str) -> list[str]:
    flags = []
    if m.n_trades < f.min_trades:
        flags.append(f"{label}: hanya {m.n_trades} trade (< {f.min_trades}) — sampel terlalu kecil")
    if m.profit_factor > 1 and m.profit_factor_ex_top < 1:
        flags.append(
            f"{label}: PF {m.profit_factor:.2f} turun ke {m.profit_factor_ex_top:.2f} tanpa "
            f"{f.top_trades_for_dependency} trade terbesar — bergantung pada 1–2 trade"
        )
    if m.total_return < m.bh_return + f.bh_margin_pct_points / 100 and m.max_drawdown > m.bh_max_drawdown:
        flags.append(
            f"{label}: return {m.total_return:.1%} tidak jauh di atas B&H {m.bh_return:.1%} "
            f"sementara DD lebih buruk ({m.max_drawdown:.1%} vs {m.bh_max_drawdown:.1%})"
        )
    if m.total_return < m.bh_return:
        flags.append(f"{label}: kalah dari buy & hold ({m.total_return:.1%} vs {m.bh_return:.1%})")
    if m.n_trades and m.expectancy_r <= 0:
        flags.append(f"{label}: expectancy ≤ 0 ({m.expectancy_r:+.2f}R per trade)")
    return flags


def oos_flags(is_m: Metrics, oos_m: Metrics, f: ReportFlags) -> list[str]:
    flags = []
    ratio = f.oos_degradation_ratio
    if is_m.expectancy_r > 0 and oos_m.expectancy_r < ratio * is_m.expectancy_r:
        flags.append(
            f"OOS jauh lebih buruk: expectancy {oos_m.expectancy_r:+.2f}R vs IS {is_m.expectancy_r:+.2f}R"
        )
    if is_m.profit_factor > 1 and oos_m.profit_factor < ratio * is_m.profit_factor:
        flags.append(f"OOS jauh lebih buruk: PF {oos_m.profit_factor:.2f} vs IS {is_m.profit_factor:.2f}")
    return flags
