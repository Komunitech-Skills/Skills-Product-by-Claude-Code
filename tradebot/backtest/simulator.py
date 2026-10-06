"""Candle-by-candle backtest simulator.

Event order inside candle ``i`` (only information known at that moment is used):
  1. pending signal exit (cross down at close i-1)  -> sell at open[i]
  2. pending entry (signal at close i-1), if flat   -> buy at open[i]
  3. open position: intrabar SL / TP on high/low[i] (SL wins ties; entry candle included)
  4. at close[i]: detect exit cross / new entry signal -> act at open[i+1]
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from core.config import CostParams, MarketFilters, StrategyParams
from core.sizing import (
    PositionSize,
    entry_fill_price,
    fee,
    market_exit_fill_price,
    size_position,
    stop_fill_price,
    take_profit_fill_price,
)
from core.strategy import Skip, TradePlan, compute_signals, plan_trade

log = logging.getLogger(__name__)


@dataclass
class Trade:
    signal_ts: int
    entry_ts: int
    entry_price: float
    stop_loss: float
    take_profit: float
    qty: float
    entry_fee: float
    equity_before: float
    risk_amount: float
    exit_ts: int | None = None
    exit_price: float | None = None
    exit_fee: float | None = None
    exit_reason: str | None = None

    @property
    def pnl(self) -> float:
        """Net PnL in quote currency, both fees included."""
        assert self.exit_price is not None and self.exit_fee is not None
        return self.qty * (self.exit_price - self.entry_price) - self.entry_fee - self.exit_fee

    @property
    def r_multiple(self) -> float:
        return self.pnl / self.risk_amount


@dataclass
class SkippedSignal:
    signal_ts: int
    reason: str
    detail: str


@dataclass
class SimResult:
    trades: list[Trade]
    skipped: list[SkippedSignal]
    equity: pd.Series                 # mark-to-market equity at each candle close
    initial_equity: float
    first_index: int
    last_index: int
    frame: pd.DataFrame = field(repr=False)


def simulate(
    df: pd.DataFrame,
    params: StrategyParams,
    costs: CostParams,
    filters: MarketFilters,
    initial_equity: float,
    risk_pct: float,
    start: int | None = None,
    end: int | None = None,
) -> SimResult:
    """Run the strategy on positional rows [start, end) of ``df`` (indicators use all prior rows).

    Signals are only taken on candles inside the window; a position still open at the
    last candle is closed at its close (``end_of_data``).
    """
    return simulate_signals(
        compute_signals(df, params), params, costs, filters, initial_equity, risk_pct, start, end
    )


def simulate_signals(
    sig: pd.DataFrame,
    params: StrategyParams,
    costs: CostParams,
    filters: MarketFilters,
    initial_equity: float,
    risk_pct: float,
    start: int | None = None,
    end: int | None = None,
) -> SimResult:
    """Execution loop over a frame that already has entry_signal / exit_signal / stop_loss."""
    n = len(sig)
    start = params.warmup_candles if start is None else max(start, params.warmup_candles)
    end = n if end is None else min(end, n)
    if start >= end:
        raise ValueError(f"empty simulation window [{start}, {end})")

    ts = sig["ts"].to_numpy()
    o, h, l, c = (sig[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
    entry_sig = sig["entry_signal"].to_numpy(dtype=bool)
    exit_sig = sig["exit_signal"].to_numpy(dtype=bool)
    sl_arr = sig["stop_loss"].to_numpy(dtype=float)

    cash = initial_equity
    pos: Trade | None = None
    pending_entry: int | None = None     # index of signal candle
    pending_exit = False
    trades: list[Trade] = []
    skipped: list[SkippedSignal] = []
    equity_curve = np.empty(end - start)

    def close_position(i: int, price: float, reason: str) -> None:
        nonlocal cash, pos
        assert pos is not None
        exit_fee = fee(pos.qty * price, costs)
        cash += pos.qty * price - exit_fee
        pos.exit_ts, pos.exit_price, pos.exit_fee, pos.exit_reason = int(ts[i]), price, exit_fee, reason
        trades.append(pos)
        log.debug("exit", extra={"ts": int(ts[i]), "reason": reason, "pnl": pos.pnl})
        pos = None

    for i in range(start, end):
        # 1. signal exit at this open
        if pos is not None and pending_exit:
            close_position(i, market_exit_fill_price(o[i], costs), "signal_exit")
        pending_exit = False

        # 2. entry at this open
        if pos is None and pending_entry is not None:
            s = pending_entry
            entry = entry_fill_price(o[i], costs)
            plan = plan_trade(sl_arr[s], entry, params)
            size: PositionSize | Skip
            size = plan if isinstance(plan, Skip) else size_position(
                cash, entry, plan.stop_loss, risk_pct, costs, filters
            )
            if isinstance(size, Skip):
                skipped.append(SkippedSignal(int(ts[s]), size.reason, size.detail))
                log.info("skip_trade", extra={"signal_ts": int(ts[s]), "reason": size.reason, "detail": size.detail})
            else:
                assert isinstance(plan, TradePlan)
                qty = float(size.qty)
                entry_fee = fee(qty * entry, costs)
                pos = Trade(
                    signal_ts=int(ts[s]), entry_ts=int(ts[i]), entry_price=entry,
                    stop_loss=plan.stop_loss, take_profit=plan.take_profit, qty=qty,
                    entry_fee=entry_fee, equity_before=cash, risk_amount=size.risk_amount,
                )
                cash -= qty * entry + entry_fee
        pending_entry = None

        # 3. intrabar SL / TP (SL first: conservative when both are touched)
        if pos is not None:
            if l[i] <= pos.stop_loss:
                close_position(i, stop_fill_price(pos.stop_loss, o[i], costs), "stop_loss")
            elif h[i] >= pos.take_profit:
                close_position(i, take_profit_fill_price(pos.take_profit), "take_profit")

        # 4. decisions at close
        is_last = i == end - 1
        if pos is not None and is_last:
            close_position(i, market_exit_fill_price(c[i], costs), "end_of_data")
        elif pos is not None and exit_sig[i]:
            pending_exit = True
        elif pos is None and entry_sig[i] and not is_last:
            pending_entry = i

        equity_curve[i - start] = cash + (pos.qty * c[i] if pos is not None else 0.0)

    equity = pd.Series(equity_curve, index=sig.index[start:end], name="equity")
    return SimResult(trades, skipped, equity, initial_equity, start, end - 1, sig)


def buy_and_hold(df: pd.DataFrame, costs: CostParams, initial_equity: float, start: int, end: int) -> pd.Series:
    """Equity of buying at open[start] (fee + slippage) and holding; last value is after selling."""
    o = df["open"].to_numpy(dtype=float)
    c = df["close"].to_numpy(dtype=float)
    entry = entry_fill_price(o[start], costs)
    qty = initial_equity / (entry * (1.0 + costs.fee_pct))
    equity = qty * c[start:end]
    exit_px = market_exit_fill_price(c[end - 1], costs)
    equity[-1] = qty * exit_px * (1.0 - costs.fee_pct)
    return pd.Series(equity, index=df.index[start:end], name="buy_hold")
