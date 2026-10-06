"""OHLCV data: fetch from Binance via ccxt, cache in SQLite, drop unclosed candles.

All timestamps are UTC epoch milliseconds (candle OPEN time, as Binance returns).
A candle with open time ``ts`` is closed once ``ts + timeframe_ms <= now_ms``.
"""
from __future__ import annotations

import logging
import sqlite3
import time
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

import ccxt
import pandas as pd

from core.config import ROOT, Config, MarketFilters

log = logging.getLogger(__name__)

OHLCV_COLUMNS = ["ts", "open", "high", "low", "close", "volume"]
MS_PER_YEAR = 365 * 24 * 60 * 60 * 1000


def timeframe_ms(timeframe: str) -> int:
    """'4h' -> 14_400_000. Uses ccxt's parser so it matches the exchange."""
    return ccxt.Exchange.parse_timeframe(timeframe) * 1000


def now_utc_ms() -> int:
    return int(time.time() * 1000)


# --------------------------------------------------------------------------- exchange

def make_exchange(cfg: Config) -> ccxt.Exchange:
    """Public (unauthenticated) ccxt client. No API key is ever used in this module."""
    ex_cfg = cfg.exchange
    exchange_cls = getattr(ccxt, ex_cfg["id"])
    exchange = exchange_cls(
        {
            "enableRateLimit": True,
            "requests_trust_env": bool(ex_cfg.get("trust_env", False)),
            "options": {
                "defaultType": ex_cfg["market_type"],
                "fetchMarkets": {"types": [ex_cfg["market_type"]]},
            },
        }
    )
    public_url = ex_cfg.get("public_api_url")
    if public_url:
        exchange.urls["api"]["public"] = public_url
    return exchange


def fetch_market_filters(exchange: ccxt.Exchange, symbol: str, fallback: MarketFilters) -> MarketFilters:
    """Read LOT_SIZE / NOTIONAL filters from exchangeInfo; fall back to config on failure."""
    try:
        market = exchange.load_markets()[symbol]
        filters = {f["filterType"]: f for f in market["info"]["filters"]}
        lot = filters["LOT_SIZE"]
        notional = filters.get("NOTIONAL") or filters["MIN_NOTIONAL"]
        result = MarketFilters(
            step_size=Decimal(lot["stepSize"]).normalize(),
            min_qty=Decimal(lot["minQty"]).normalize(),
            min_notional=Decimal(notional["minNotional"]).normalize(),
        )
        log.info("market_filters", extra={"symbol": symbol, "filters": str(result)})
        return result
    except (ccxt.BaseError, KeyError) as exc:
        log.warning("market_filters_fallback", extra={"symbol": symbol, "error": repr(exc)})
        return fallback


def fetch_ohlcv_range(
    exchange: ccxt.Exchange,
    symbol: str,
    timeframe: str,
    since_ms: int,
    until_ms: int,
    limit: int = 1000,
) -> list[list[float]]:
    """Paginate fetch_ohlcv from since_ms (inclusive) to until_ms (exclusive)."""
    tf_ms = timeframe_ms(timeframe)
    rows: list[list[float]] = []
    cursor = since_ms
    while cursor < until_ms:
        batch = exchange.fetch_ohlcv(symbol, timeframe, since=cursor, limit=limit)
        if not batch:
            break
        rows.extend(r for r in batch if since_ms <= r[0] < until_ms)
        next_cursor = batch[-1][0] + tf_ms
        if next_cursor <= cursor:  # defensive: no progress
            break
        cursor = next_cursor
        log.debug("ohlcv_page", extra={"symbol": symbol, "last_ts": batch[-1][0], "n": len(batch)})
    return rows


# --------------------------------------------------------------------------- cleaning

def to_frame(rows: Iterable[Iterable[Any]]) -> pd.DataFrame:
    """Rows [ts, o, h, l, c, v] -> DataFrame sorted by ts, duplicates removed, UTC index."""
    df = pd.DataFrame(list(rows), columns=OHLCV_COLUMNS)
    if df.empty:
        return df.set_index(pd.DatetimeIndex([], tz="UTC", name="time"))
    df["ts"] = df["ts"].astype("int64")
    df = df.drop_duplicates("ts", keep="last").sort_values("ts").reset_index(drop=True)
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    df.index = pd.to_datetime(df["ts"], unit="ms", utc=True).rename("time")
    return df


def drop_unclosed(df: pd.DataFrame, timeframe: str, now_ms: int) -> pd.DataFrame:
    """Remove candles whose close time (open + timeframe) is still in the future."""
    tf_ms = timeframe_ms(timeframe)
    closed = df["ts"] + tf_ms <= now_ms
    dropped = int((~closed).sum())
    if dropped:
        log.info("drop_unclosed", extra={"dropped": dropped, "last_ts": int(df["ts"].iloc[-1])})
    return df[closed]


@dataclass(frozen=True)
class DataQuality:
    n_candles: int
    gaps: list[tuple[int, int]]          # (ts_before_gap, ts_after_gap)
    missing_candles: int
    bad_ohlc_rows: int


def check_quality(df: pd.DataFrame, timeframe: str) -> DataQuality:
    """Report gaps in the series and OHLC rows violating low <= open/close <= high."""
    tf_ms = timeframe_ms(timeframe)
    diffs = df["ts"].diff().dropna()
    gap_idx = diffs[diffs != tf_ms].index
    gaps = []
    missing = 0
    for idx in gap_idx:
        pos = df.index.get_loc(idx)
        before, after = int(df["ts"].iloc[pos - 1]), int(df["ts"].iloc[pos])
        gaps.append((before, after))
        missing += (after - before) // tf_ms - 1
    bad = (
        (df["low"] > df[["open", "close"]].min(axis=1))
        | (df["high"] < df[["open", "close"]].max(axis=1))
        | (df["low"] <= 0)
    )
    return DataQuality(len(df), gaps, int(missing), int(bad.sum()))


# --------------------------------------------------------------------------- SQLite cache

class OhlcvCache:
    """SQLite cache of CLOSED candles only (unclosed candles are never stored)."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as con:
            con.execute(
                """CREATE TABLE IF NOT EXISTS ohlcv (
                    symbol TEXT NOT NULL, timeframe TEXT NOT NULL, ts INTEGER NOT NULL,
                    open REAL NOT NULL, high REAL NOT NULL, low REAL NOT NULL,
                    close REAL NOT NULL, volume REAL NOT NULL,
                    PRIMARY KEY (symbol, timeframe, ts))"""
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def upsert(self, symbol: str, timeframe: str, df: pd.DataFrame) -> int:
        records = [
            (symbol, timeframe, int(r.ts), r.open, r.high, r.low, r.close, r.volume)
            for r in df.itertuples(index=False)
        ]
        with self._connect() as con:
            con.executemany("INSERT OR REPLACE INTO ohlcv VALUES (?,?,?,?,?,?,?,?)", records)
        return len(records)

    def load(self, symbol: str, timeframe: str, since_ms: int | None = None) -> pd.DataFrame:
        query = "SELECT ts, open, high, low, close, volume FROM ohlcv WHERE symbol=? AND timeframe=?"
        params: list[Any] = [symbol, timeframe]
        if since_ms is not None:
            query += " AND ts >= ?"
            params.append(since_ms)
        with self._connect() as con:
            rows = con.execute(query + " ORDER BY ts", params).fetchall()
        return to_frame(rows)

    def bounds(self, symbol: str, timeframe: str) -> tuple[int | None, int | None]:
        with self._connect() as con:
            lo, hi = con.execute(
                "SELECT MIN(ts), MAX(ts) FROM ohlcv WHERE symbol=? AND timeframe=?", (symbol, timeframe)
            ).fetchone()
        return lo, hi


def load_history(
    cfg: Config,
    now_ms: int | None = None,
    exchange: ccxt.Exchange | None = None,
    root: Path = ROOT,
) -> pd.DataFrame:
    """Return closed candles covering warm-up + history_years, fetching only what the cache lacks."""
    now_ms = now_ms if now_ms is not None else now_utc_ms()
    tf = cfg.timeframe
    tf_ms = timeframe_ms(tf)
    last_closed_open = (now_ms // tf_ms) * tf_ms - tf_ms          # open time of last CLOSED candle
    start_ms = last_closed_open - cfg.data["history_years"] * MS_PER_YEAR - cfg.strategy.warmup_candles * tf_ms
    start_ms = (start_ms // tf_ms) * tf_ms

    cache = OhlcvCache(root / cfg.data["db_path"])
    lo, hi = cache.bounds(cfg.symbol, tf)
    ranges: list[tuple[int, int]] = []
    if lo is None:
        ranges.append((start_ms, now_ms))
    else:
        if start_ms < lo:
            ranges.append((start_ms, lo))
        if hi + tf_ms <= last_closed_open:
            ranges.append((hi + tf_ms, now_ms))

    if ranges:
        exchange = exchange or make_exchange(cfg)
        for since, until in ranges:
            rows = fetch_ohlcv_range(exchange, cfg.symbol, tf, since, until, cfg.data["fetch_limit"])
            fresh = drop_unclosed(to_frame(rows), tf, now_ms) if rows else to_frame([])
            n = cache.upsert(cfg.symbol, tf, fresh)
            log.info("ohlcv_fetched", extra={"since": since, "until": until, "stored": n})

    df = cache.load(cfg.symbol, tf, since_ms=start_ms)
    return drop_unclosed(df, tf, now_ms)
