"""Strategy (pure function) tests: cross detection, no lookahead, swing low, trade plan."""
from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from core.strategy import Skip, TradePlan, compute_signals, latest_signal, plan_trade, rsi
from tests.conftest import make_frame, random_walk


def v_shape(flat: int = 300, down: int = 100, up: int = 150) -> pd.DataFrame:
    close = np.concatenate([np.full(flat, 100.0), np.linspace(100, 80, down), np.linspace(80, 130, up)])
    open_ = np.concatenate([[close[0]], close[:-1]])
    return make_frame(open_, np.maximum(open_, close) + 0.2, np.minimum(open_, close) - 0.2, close)


def test_cross_up_detected_exactly_once(params):
    sig = compute_signals(v_shape(), params)
    assert int(sig["cross_up"].sum()) == 1
    i = int(np.flatnonzero(sig["cross_up"])[0])
    # fast stays above slow afterwards, yet no further cross is reported
    assert (sig["ema_fast"].iloc[i:] > sig["ema_slow"].iloc[i:]).all()
    assert not sig["cross_up"].iloc[i + 1:].any()
    assert int(sig["entry_signal"].sum()) <= 1


def test_exit_cross_down_detected_once(params):
    df = v_shape()
    mirrored = make_frame(200 - df["open"], 200 - df["low"], 200 - df["high"], 200 - df["close"])
    sig = compute_signals(mirrored, params)
    assert int(sig["exit_signal"].sum()) == 1


def test_entry_requires_all_three_conditions(params):
    sig = compute_signals(random_walk(3000, seed=3), params)
    e = sig[sig["entry_signal"]]
    assert len(e) > 0
    assert (e["cross_up"]).all()
    assert ((e["rsi"] >= 45) & (e["rsi"] <= 70)).all()
    assert (e["close"] > e["ema_trend"]).all()
    # crosses rejected by a filter exist too (filters actually bite)
    assert sig["cross_up"].sum() > len(e)


def test_no_signal_during_warmup(params):
    sig = compute_signals(random_walk(3000, seed=3), params)
    assert not sig["entry_signal"].iloc[: params.warmup_candles].any()


@pytest.mark.parametrize("cut", [650, 900, 1234, 1777])
def test_no_lookahead(params, cut):
    df = random_walk(2000, seed=11)
    full = compute_signals(df, params)
    trunc = compute_signals(df.iloc[: cut + 1], params)
    cols = ["ema_fast", "ema_slow", "ema_trend", "rsi", "stop_loss", "entry_signal", "exit_signal"]
    pd.testing.assert_frame_equal(full[cols].iloc[: cut + 1], trunc[cols])


def test_latest_signal_matches_batch(params):
    df = random_walk(2000, seed=11)
    full = compute_signals(df, params)
    idx = int(np.flatnonzero(full["entry_signal"])[0])
    s = latest_signal(df.iloc[: idx + 1], params)
    assert s is not None and s.index == idx and s.stop_loss == pytest.approx(full["stop_loss"].iloc[idx])
    assert latest_signal(df.iloc[: idx], params) is None


def test_swing_low_includes_signal_candle(params):
    n = 30
    close = np.full(n, 100.0)
    lows = np.full(n, 99.0)
    lows[25] = 90.0                       # candle "t" itself is the lowest
    lows[15] = 80.0                       # inside the window of t=24, outside the window of t=25
    df = make_frame(close, close + 1, lows, close)
    sig = compute_signals(df, replace(params, warmup_candles=0))
    assert sig["stop_loss"].iloc[25] == pytest.approx(90.0 * 0.995)     # includes t
    assert sig["stop_loss"].iloc[24] == pytest.approx(80.0 * 0.995)     # window 15..24 includes 80
    assert sig["stop_loss"].iloc[26] == pytest.approx(90.0 * 0.995)     # window 17..26, 80 dropped


def test_plan_trade_tp_is_two_r(params):
    plan = plan_trade(stop_loss=97.0, entry=100.0, p=params)
    assert isinstance(plan, TradePlan)
    assert plan.take_profit == pytest.approx(106.0)
    assert plan.risk_distance_pct == pytest.approx(0.03)


def test_skip_when_sl_distance_above_4pct(params):
    assert isinstance(plan_trade(95.9, 100.0, params), Skip)
    assert plan_trade(95.9, 100.0, params).reason == "sl_too_far"
    assert isinstance(plan_trade(96.0, 100.0, params), TradePlan)        # exactly 4% allowed


def test_skip_when_sl_not_below_entry(params):
    assert plan_trade(100.0, 100.0, params).reason == "sl_not_below_entry"
    assert plan_trade(101.0, 100.0, params).reason == "sl_not_below_entry"


def test_rsi_bounds_and_known_value():
    up = pd.Series(np.arange(1, 40, dtype=float))
    assert rsi(up, 14).dropna().eq(100.0).all()
    alt = pd.Series([100.0, 101.0] * 30)
    assert rsi(alt, 14).iloc[-1] == pytest.approx(50.0, abs=5)


def test_rejects_unsorted_input(params):
    df = random_walk(300)
    with pytest.raises(ValueError):
        compute_signals(df.iloc[::-1], params)
