"""EMA trend + RSI filter strategy as pure functions.

Input: DataFrame of CLOSED candles (columns open/high/low/close, ascending ``ts``).
Output: signals. No I/O, no state, no clock — the same code is used by backtest,
paper and live; only the executor differs.

Every value at row ``t`` depends only on rows ``<= t`` (EMA/RSI are recursive
filters, swing low is a trailing window), so there is no lookahead.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

from core.config import StrategyParams

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Signal:
    """Entry signal on a closed candle. Entry itself happens at the NEXT candle's open."""

    ts: int             # open time (UTC ms) of the signal candle
    index: int          # positional index of the signal candle
    stop_loss: float    # min(low of last N candles incl. signal) × (1 − buffer)
    close: float        # signal candle close (reference only; never used as fill)


@dataclass(frozen=True)
class TradePlan:
    entry: float
    stop_loss: float
    take_profit: float
    risk_distance_pct: float   # (entry − SL) / entry


@dataclass(frozen=True)
class Skip:
    reason: str
    detail: str


# --------------------------------------------------------------------------- indicators

def ema(series: pd.Series, period: int) -> pd.Series:
    """Exponential moving average, alpha = 2/(period+1), seeded with the first value."""
    return series.ewm(span=period, adjust=False).mean()


def rsi(close: pd.Series, period: int) -> pd.Series:
    """Wilder's RSI (smoothing alpha = 1/period). NaN until ``period`` changes exist."""
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss
    out = 100.0 - 100.0 / (1.0 + rs)
    out = out.where(avg_loss != 0.0, 100.0)            # no losses -> RSI 100
    return out.where(avg_gain.notna())


def compute_signals(df: pd.DataFrame, p: StrategyParams) -> pd.DataFrame:
    """Add indicator, entry/exit signal and stop-loss columns. Pure: returns a new frame."""
    if not df["ts"].is_monotonic_increasing or df["ts"].duplicated().any():
        raise ValueError("candles must be unique and sorted by ts")
    out = df.copy()
    close = out["close"]
    fast, slow = ema(close, p.ema_fast), ema(close, p.ema_slow)
    out["ema_fast"], out["ema_slow"] = fast, slow
    out["ema_trend"] = ema(close, p.ema_trend)
    out["rsi"] = rsi(close, p.rsi_period)

    prev_fast, prev_slow = fast.shift(1), slow.shift(1)
    cross_up = (prev_fast <= prev_slow) & (fast > slow)
    cross_down = (prev_fast >= prev_slow) & (fast < slow)
    rsi_ok = (out["rsi"] >= p.rsi_min) & (out["rsi"] <= p.rsi_max)
    trend_ok = close > out["ema_trend"]
    warmed_up = pd.Series(np.arange(len(out)) >= p.warmup_candles, index=out.index)

    out["swing_low"] = out["low"].rolling(p.swing_lookback, min_periods=p.swing_lookback).min()
    out["stop_loss"] = out["swing_low"] * (1.0 - p.sl_buffer_pct)
    out["cross_up"] = cross_up.fillna(False)
    out["entry_signal"] = (cross_up & rsi_ok & trend_ok & warmed_up & out["stop_loss"].notna()).fillna(False)
    out["exit_signal"] = cross_down.fillna(False)
    return out


def latest_signal(df: pd.DataFrame, p: StrategyParams) -> Signal | None:
    """Entry signal on the most recent CLOSED candle, if any (used by paper/live)."""
    if df.empty:
        return None
    sig = compute_signals(df, p)
    last = sig.iloc[-1]
    if not bool(last["entry_signal"]):
        return None
    return Signal(ts=int(last["ts"]), index=len(sig) - 1, stop_loss=float(last["stop_loss"]), close=float(last["close"]))


def latest_exit(df: pd.DataFrame, p: StrategyParams) -> bool:
    """True if EMA fast crossed below EMA slow on the most recent closed candle."""
    return bool(compute_signals(df, p)["exit_signal"].iloc[-1]) if not df.empty else False


# --------------------------------------------------------------------------- trade plan

def plan_trade(stop_loss: float, entry: float, p: StrategyParams) -> TradePlan | Skip:
    """Turn a signal's SL and the actual entry fill price into SL/TP, or a skip reason.

    ``entry`` is the fill price (next open incl. adverse slippage); risk distance and
    TP are measured from it.
    """
    if not (np.isfinite(stop_loss) and np.isfinite(entry)) or entry <= 0:
        return Skip("invalid_price", f"entry={entry} sl={stop_loss}")
    if stop_loss >= entry:
        log.error("sl_not_below_entry", extra={"entry": entry, "sl": stop_loss})
        return Skip("sl_not_below_entry", f"SL {stop_loss:.2f} >= entry {entry:.2f}")
    distance = (entry - stop_loss) / entry
    if distance > p.max_sl_distance_pct:
        return Skip("sl_too_far", f"SL distance {distance:.4%} > {p.max_sl_distance_pct:.2%}")
    take_profit = entry + p.reward_risk * (entry - stop_loss)
    return TradePlan(entry=entry, stop_loss=stop_loss, take_profit=take_profit, risk_distance_pct=distance)
