"""Load config.yaml into typed, immutable parameter objects."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT / "config.yaml"


@dataclass(frozen=True)
class StrategyParams:
    """Parameter strategi EMA trend + RSI filter (dikunci, tidak di-tuning)."""

    ema_fast: int
    ema_slow: int
    ema_trend: int
    rsi_period: int
    rsi_min: float
    rsi_max: float
    swing_lookback: int
    sl_buffer_pct: float
    max_sl_distance_pct: float
    reward_risk: float
    warmup_candles: int


@dataclass(frozen=True)
class CostParams:
    """Fee per sisi dan slippage merugikan, dalam pecahan (0.001 = 0,1%)."""

    fee_pct: float
    slippage_pct: float


@dataclass(frozen=True)
class MarketFilters:
    """Filter order exchange (LOT_SIZE.stepSize/minQty, NOTIONAL.minNotional)."""

    step_size: Decimal
    min_qty: Decimal
    min_notional: Decimal


@dataclass(frozen=True)
class RiskParams:
    initial_equity: float
    risk_per_trade_pct: float
    max_open_positions: int


@dataclass(frozen=True)
class ReportFlags:
    min_trades: int
    oos_degradation_ratio: float
    top_trades_for_dependency: int
    bh_margin_pct_points: float


@dataclass(frozen=True)
class Config:
    raw: dict[str, Any]
    mode: str
    symbol: str
    timeframe: str
    strategy: StrategyParams
    costs: CostParams
    risk: RiskParams
    fallback_filters: MarketFilters
    report_flags: ReportFlags

    @property
    def exchange(self) -> dict[str, Any]:
        return self.raw["exchange"]

    @property
    def data(self) -> dict[str, Any]:
        return self.raw["data"]

    @property
    def backtest(self) -> dict[str, Any]:
        return self.raw["backtest"]


def load_config(path: Path | str = DEFAULT_CONFIG_PATH) -> Config:
    """Read YAML config; raises on missing keys or unsupported mode."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    mode = raw["mode"]
    if mode not in ("paper", "live"):
        raise ValueError(f"mode harus 'paper' atau 'live', bukan {mode!r}")
    ff = raw["market_filters_fallback"]
    return Config(
        raw=raw,
        mode=mode,
        symbol=raw["symbol"],
        timeframe=raw["timeframe"],
        strategy=StrategyParams(**raw["strategy"]),
        costs=CostParams(**raw["costs"]),
        risk=RiskParams(**raw["risk"]),
        fallback_filters=MarketFilters(
            step_size=Decimal(str(ff["step_size"])),
            min_qty=Decimal(str(ff["min_qty"])),
            min_notional=Decimal(str(ff["min_notional"])),
        ),
        report_flags=ReportFlags(**raw["report_flags"]),
    )
