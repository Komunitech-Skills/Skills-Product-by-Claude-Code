"""Shared fixtures: config objects and synthetic candle builders (no network)."""
from __future__ import annotations

import sys
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config import MarketFilters, load_config  # noqa: E402

TF_MS = 4 * 60 * 60 * 1000
T0 = 1_700_000_000_000 // TF_MS * TF_MS


@pytest.fixture(scope="session")
def cfg():
    return load_config()


@pytest.fixture
def params(cfg):
    return cfg.strategy


@pytest.fixture
def params_nowarm(cfg):
    """Same rules, warm-up 0, for hand-built signal frames."""
    return replace(cfg.strategy, warmup_candles=0)


@pytest.fixture
def costs(cfg):
    return cfg.costs


@pytest.fixture
def filters():
    return MarketFilters(step_size=Decimal("0.00001"), min_qty=Decimal("0.00001"), min_notional=Decimal("5"))


def make_frame(opens, highs, lows, closes, t0: int = T0) -> pd.DataFrame:
    n = len(closes)
    ts = t0 + np.arange(n, dtype="int64") * TF_MS
    df = pd.DataFrame({"ts": ts, "open": opens, "high": highs, "low": lows, "close": closes,
                       "volume": np.ones(n)}).astype({"open": float, "high": float, "low": float, "close": float})
    df.index = pd.to_datetime(df["ts"], unit="ms", utc=True).rename("time")
    return df


def flat_frame(n: int, price: float = 100.0) -> pd.DataFrame:
    """Candles with open=close=price, high=price+1, low=price-1."""
    p = np.full(n, price)
    return make_frame(p, p + 1, p - 1, p)


def signal_frame(df: pd.DataFrame, entries: dict[int, float], exits: tuple[int, ...] = ()) -> pd.DataFrame:
    """Attach hand-set entry signals {index: stop_loss} and exit signals to a candle frame."""
    sig = df.copy()
    sig["entry_signal"] = False
    sig["exit_signal"] = False
    sig["stop_loss"] = np.nan
    for i, sl in entries.items():
        sig.iloc[i, sig.columns.get_loc("entry_signal")] = True
        sig.iloc[i, sig.columns.get_loc("stop_loss")] = sl
    for i in exits:
        sig.iloc[i, sig.columns.get_loc("exit_signal")] = True
    return sig


def random_walk(n: int = 2000, seed: int = 7) -> pd.DataFrame:
    """Deterministic trending/mean-reverting synthetic market with realistic wicks."""
    rng = np.random.default_rng(seed)
    drift = np.sin(np.arange(n) / 150.0) * 0.002
    rets = drift + rng.normal(0, 0.005, n)
    close = 30_000 * np.exp(np.cumsum(rets))
    open_ = np.concatenate([[close[0]], close[:-1]])
    high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.004, n)))
    low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.004, n)))
    return make_frame(open_, high, low, close)
