"""Execution semantics of the backtest loop on hand-built signal frames."""
from __future__ import annotations

import numpy as np
import pytest

from backtest.metrics import max_drawdown, profit_factor
from backtest.simulator import buy_and_hold, simulate, simulate_signals
from tests.conftest import flat_frame, make_frame, random_walk, signal_frame

EQ = 1_000.0


def run(sig, params, costs, filters):
    return simulate_signals(sig, params, costs, filters, initial_equity=EQ, risk_pct=0.01)


def frame_with(n=20, overrides=None):
    """Flat 100 candles; overrides {i: (o, h, l, c)}."""
    df = flat_frame(n)
    for i, (o, h, l, c) in (overrides or {}).items():
        df.iloc[i, df.columns.get_indexer(["open", "high", "low", "close"])] = [o, h, l, c]
    return df


def test_entry_at_next_open_not_signal_close(params_nowarm, costs, filters):
    df = frame_with(overrides={5: (100, 101, 99, 100.0), 6: (102.0, 103, 101.5, 102.5)})
    res = run(signal_frame(df, {5: 98.0}), params_nowarm, costs, filters)
    t = res.trades[0]
    assert t.entry_ts == df["ts"].iloc[6] and t.signal_ts == df["ts"].iloc[5]
    assert t.entry_price == pytest.approx(102.0 * (1 + costs.slippage_pct))
    assert t.take_profit == pytest.approx(t.entry_price + 2 * (t.entry_price - 98.0))


def test_sl_wins_when_sl_and_tp_hit_same_candle(params_nowarm, costs, filters):
    df = frame_with(overrides={7: (100, 200, 50, 100)})          # touches both
    res = run(signal_frame(df, {5: 98.0}), params_nowarm, costs, filters)
    t = res.trades[0]
    assert t.exit_reason == "stop_loss" and t.exit_ts == df["ts"].iloc[7]
    assert t.exit_price == pytest.approx(98.0 * (1 - costs.slippage_pct))


def test_sl_hit_on_entry_candle(params_nowarm, costs, filters):
    df = frame_with(overrides={6: (100, 100.5, 97.0, 99.0)})
    res = run(signal_frame(df, {5: 98.0}), params_nowarm, costs, filters)
    t = res.trades[0]
    assert t.entry_ts == t.exit_ts == df["ts"].iloc[6] and t.exit_reason == "stop_loss"


def test_gap_below_sl_fills_at_open(params_nowarm, costs, filters):
    df = frame_with(overrides={8: (95.0, 96, 94, 95)})
    t = run(signal_frame(df, {5: 98.0}), params_nowarm, costs, filters).trades[0]
    assert t.exit_price == pytest.approx(95.0 * (1 - costs.slippage_pct))


def test_tp_exit_fees_both_sides_no_tp_slippage(params_nowarm, costs, filters):
    df = frame_with(overrides={9: (100, 110, 99.5, 109)})
    t = run(signal_frame(df, {5: 98.0}), params_nowarm, costs, filters).trades[0]
    entry = 100.0 * (1 + costs.slippage_pct)
    tp = entry + 2 * (entry - 98.0)
    assert t.exit_reason == "take_profit" and t.exit_price == pytest.approx(tp)
    expected = t.qty * (tp - entry) - t.qty * entry * costs.fee_pct - t.qty * tp * costs.fee_pct
    assert t.pnl == pytest.approx(expected)
    assert t.entry_fee == pytest.approx(t.qty * entry * costs.fee_pct)
    assert t.exit_fee == pytest.approx(t.qty * tp * costs.fee_pct)


def test_signal_exit_at_next_open_with_slippage(params_nowarm, costs, filters):
    df = frame_with(overrides={10: (100, 101, 99, 100.0), 11: (100.7, 101, 99.5, 100.2)})
    t = run(signal_frame(df, {5: 98.0}, exits=(10,)), params_nowarm, costs, filters).trades[0]
    assert t.exit_reason == "signal_exit" and t.exit_ts == df["ts"].iloc[11]
    assert t.exit_price == pytest.approx(100.7 * (1 - costs.slippage_pct))


def test_equity_reconciles_with_trade_pnls(params_nowarm, costs, filters):
    df = frame_with(30, overrides={9: (100, 110, 99.5, 109), 17: (100, 100, 90, 95)})
    res = run(signal_frame(df, {5: 98.0, 14: 98.0}), params_nowarm, costs, filters)
    assert [t.exit_reason for t in res.trades] == ["take_profit", "stop_loss"]
    assert res.equity.iloc[-1] == pytest.approx(EQ + sum(t.pnl for t in res.trades))


def test_loss_at_sl_is_about_one_percent_of_equity(params_nowarm, costs, filters):
    df = frame_with(overrides={8: (100, 100, 97.5, 99)})
    res = run(signal_frame(df, {5: 98.0}), params_nowarm, costs, filters)
    loss = -res.trades[0].pnl
    assert 0.0099 * EQ < loss <= 0.01 * EQ + 1e-9


def test_skip_wide_sl_is_logged_not_traded(params_nowarm, costs, filters):
    res = run(signal_frame(frame_with(), {5: 90.0}), params_nowarm, costs, filters)
    assert res.trades == [] and [s.reason for s in res.skipped] == ["sl_too_far"]


def test_skip_below_min_notional(params_nowarm, costs, filters):
    res = simulate_signals(signal_frame(frame_with(), {5: 98.0}), params_nowarm, costs, filters,
                           initial_equity=3.0, risk_pct=0.01)
    assert res.trades == [] and res.skipped[0].reason in ("below_min_notional", "below_min_qty")


def test_single_position_only(params_nowarm, costs, filters):
    res = run(signal_frame(frame_with(), {5: 98.0, 7: 98.0}), params_nowarm, costs, filters)
    assert len(res.trades) == 1 and res.trades[0].exit_reason == "end_of_data"


def test_signal_on_last_candle_ignored(params_nowarm, costs, filters):
    df = frame_with(10)
    assert run(signal_frame(df, {9: 98.0}), params_nowarm, costs, filters).trades == []


def test_backtest_has_no_lookahead_on_trades(params, costs, filters):
    df = random_walk(6000, seed=4)
    full = simulate(df, params, costs, filters, EQ, 0.01)
    assert len(full.trades) >= 3
    cut = full.trades[len(full.trades) // 2].exit_ts
    cut_idx = int(np.flatnonzero(df["ts"].to_numpy() == cut)[0])
    part = simulate(df.iloc[: cut_idx + 2], params, costs, filters, EQ, 0.01)
    done_full = [t for t in full.trades if t.exit_ts <= cut]
    done_part = [t for t in part.trades if t.exit_ts <= cut]
    assert [(t.entry_ts, t.exit_ts, t.pnl) for t in done_full] == [(t.entry_ts, t.exit_ts, t.pnl) for t in done_part]


def test_buy_and_hold_includes_costs(costs):
    df = make_frame([100, 100, 100], [101] * 3, [99] * 3, [100, 100, 100])
    bh = buy_and_hold(df, costs, EQ, 0, 3)
    assert bh.iloc[-1] < EQ                                     # flat market: costs only
    expected = EQ / (100 * 1.0005 * 1.001) * 100 * 0.9995 * 0.999
    assert bh.iloc[-1] == pytest.approx(expected)


def test_metric_helpers():
    import pandas as pd
    assert max_drawdown(pd.Series([110.0, 88.0, 120.0]), 100.0) == pytest.approx(0.2)
    assert profit_factor([10, -5, 5]) == pytest.approx(3.0)
