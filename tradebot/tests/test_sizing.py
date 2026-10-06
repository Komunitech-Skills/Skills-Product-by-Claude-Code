"""Fee-aware sizing: loss at SL ≈ 1% equity incl. fees, stepSize floor, minNotional skip."""
from __future__ import annotations

from decimal import Decimal

import pytest

from core.sizing import floor_to_step, loss_per_unit_at_stop, size_position
from core.strategy import Skip


def realized_loss_at_stop(qty: float, entry: float, sl: float, costs) -> float:
    """Independent recomputation: cash out at entry minus cash in at SL fill."""
    paid = qty * entry + qty * entry * costs.fee_pct
    sl_fill = sl * (1 - costs.slippage_pct)
    received = qty * sl_fill - qty * sl_fill * costs.fee_pct
    return paid - received


@pytest.mark.parametrize("entry,sl", [(60_000.0, 58_800.0), (60_000.0, 57_700.0), (25_000.0, 24_500.0)])
def test_actual_risk_is_one_percent_including_fees(entry, sl, costs, filters):
    equity = 1_000.0
    size = size_position(equity, entry, sl, 0.01, costs, filters)
    assert not isinstance(size, Skip)
    loss = realized_loss_at_stop(float(size.qty), entry, sl, costs)
    assert loss <= equity * 0.01 + 1e-9                            # never more than 1%
    step_loss = float(filters.step_size) * loss_per_unit_at_stop(entry, sl, costs)
    assert loss >= equity * 0.01 - step_loss - 1e-9                # short only by < 1 step
    assert loss == pytest.approx(size.loss_at_stop)


def test_qty_is_floored_to_step(costs, filters):
    size = size_position(1_234.56, 61_234.5, 60_100.0, 0.01, costs, filters)
    assert not isinstance(size, Skip)
    assert size.qty % filters.step_size == 0
    raw = 12.3456 / loss_per_unit_at_stop(61_234.5, 60_100.0, costs)
    assert float(size.qty) <= raw < float(size.qty) + float(filters.step_size)


def test_floor_to_step_never_rounds_up():
    assert floor_to_step(Decimal("0.123459999"), Decimal("0.00001")) == Decimal("0.12345")
    assert floor_to_step(Decimal("0.3"), Decimal("0.1")) == Decimal("0.3")


def test_skip_below_min_notional(costs, filters):
    # 1% of 10 USDT = 0.10 risk; 3% SL distance -> ~3 USDT position < 5 USDT minNotional
    res = size_position(10.0, 60_000.0, 58_200.0, 0.01, costs, filters)
    assert isinstance(res, Skip) and res.reason in ("below_min_notional", "below_min_qty")


def test_skip_below_min_qty(costs, filters):
    res = size_position(1.0, 60_000.0, 58_200.0, 0.01, costs, filters)
    assert isinstance(res, Skip) and res.reason == "below_min_qty"


def test_position_capped_by_equity_for_tight_sl(costs, filters):
    equity = 1_000.0
    size = size_position(equity, 60_000.0, 59_880.0, 0.01, costs, filters)   # 0.2% SL -> 5x notional wanted
    assert not isinstance(size, Skip) and size.capped_by_equity
    assert float(size.qty) * 60_000.0 * (1 + costs.fee_pct) <= equity
    assert size.loss_at_stop < equity * 0.01
