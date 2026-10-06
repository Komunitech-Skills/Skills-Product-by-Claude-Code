"""Fill prices (fee + slippage) and fee-aware position sizing.

Shared by the backtest and (Fase 3) the paper executor so both model costs identically.
Quantities are rounded with ``Decimal`` to avoid float floor errors on stepSize.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_DOWN, Decimal

from core.config import CostParams, MarketFilters
from core.strategy import Skip


# --------------------------------------------------------------------------- fills

def entry_fill_price(open_price: float, costs: CostParams) -> float:
    """Market buy at next open, slippage against us (pay more)."""
    return open_price * (1.0 + costs.slippage_pct)


def stop_fill_price(stop_loss: float, candle_open: float, costs: CostParams) -> float:
    """Stop-market sell. If the candle opens below SL (gap), fill from the open, not the SL."""
    return min(stop_loss, candle_open) * (1.0 - costs.slippage_pct)


def market_exit_fill_price(open_price: float, costs: CostParams) -> float:
    """Market sell at open (signal exit / end of data), slippage against us."""
    return open_price * (1.0 - costs.slippage_pct)


def take_profit_fill_price(take_profit: float) -> float:
    """Limit sell: filled at the TP price, no slippage (and no credit for gap-ups)."""
    return take_profit


def fee(notional: float, costs: CostParams) -> float:
    return notional * costs.fee_pct


# --------------------------------------------------------------------------- sizing

@dataclass(frozen=True)
class PositionSize:
    qty: Decimal
    notional: float              # qty × entry, before fee
    risk_amount: float           # target loss at SL (equity × risk %)
    loss_at_stop: float          # modelled loss if SL fills at SL price, incl. both fees + slippage
    capped_by_equity: bool


def floor_to_step(qty: Decimal, step: Decimal) -> Decimal:
    """Round DOWN to a multiple of stepSize (never round up into more risk)."""
    if step <= 0:
        raise ValueError("step_size must be > 0")
    return (qty / step).to_integral_value(rounding=ROUND_DOWN) * step


def loss_per_unit_at_stop(entry: float, stop_loss: float, costs: CostParams) -> float:
    """Cash lost per unit bought at ``entry`` and sold by the SL order (fees + slippage incl.)."""
    exit_price = stop_loss * (1.0 - costs.slippage_pct)
    return entry * (1.0 + costs.fee_pct) - exit_price * (1.0 - costs.fee_pct)


def size_position(
    equity: float,
    entry: float,
    stop_loss: float,
    risk_pct: float,
    costs: CostParams,
    filters: MarketFilters,
) -> PositionSize | Skip:
    """Fee-aware sizing: loss at SL (fees + SL slippage) ≈ ``risk_pct`` × equity, never more.

    Spot, no leverage: cost of the position incl. entry fee is capped at equity.
    Gap-downs through the SL can still lose more; that is an execution risk, not sizing.
    """
    if equity <= 0:
        return Skip("no_equity", f"equity={equity}")
    per_unit = loss_per_unit_at_stop(entry, stop_loss, costs)
    if per_unit <= 0:
        return Skip("sl_not_below_entry", f"loss per unit {per_unit}")
    risk_amount = equity * risk_pct
    qty_risk = Decimal(str(risk_amount / per_unit))
    qty_cash = Decimal(str(equity / (entry * (1.0 + costs.fee_pct))))
    capped = qty_cash < qty_risk
    qty = floor_to_step(min(qty_risk, qty_cash), filters.step_size)
    notional = float(qty) * entry
    if qty < filters.min_qty or qty <= 0:
        return Skip("below_min_qty", f"qty {qty} < minQty {filters.min_qty}")
    if Decimal(str(notional)) < filters.min_notional:
        return Skip("below_min_notional", f"notional {notional:.4f} < minNotional {filters.min_notional}")
    return PositionSize(
        qty=qty,
        notional=notional,
        risk_amount=risk_amount,
        loss_at_stop=float(qty) * per_unit,
        capped_by_equity=capped,
    )
