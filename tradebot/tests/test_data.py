"""Data layer: unclosed candles are never used or cached; cache is incremental."""
from __future__ import annotations

import numpy as np

from core.data import OhlcvCache, check_quality, drop_unclosed, load_history, timeframe_ms, to_frame
from tests.conftest import T0, TF_MS


def rows(n: int, t0: int = T0):
    return [[t0 + i * TF_MS, 100.0, 101.0, 99.0, 100.5, 1.0] for i in range(n)]


def test_timeframe_ms():
    assert timeframe_ms("4h") == TF_MS


def test_drop_unclosed_removes_running_candle():
    df = to_frame(rows(5))
    now = T0 + 4 * TF_MS + TF_MS // 2                 # inside candle #4
    assert drop_unclosed(df, "4h", now)["ts"].tolist() == df["ts"].tolist()[:4]


def test_drop_unclosed_keeps_candle_at_exact_close():
    df = to_frame(rows(5))
    assert len(drop_unclosed(df, "4h", T0 + 5 * TF_MS)) == 5


def test_to_frame_dedupes_and_sorts():
    r = rows(3)
    df = to_frame([r[2], r[0], r[1], r[1]])
    assert df["ts"].tolist() == [r[0][0], r[1][0], r[2][0]]


def test_quality_detects_gap_and_bad_ohlc():
    r = rows(6)
    del r[3]
    r[0][3] = 200.0                                    # low above open/close
    q = check_quality(to_frame(r), "4h")
    assert q.missing_candles == 1 and len(q.gaps) == 1 and q.bad_ohlc_rows == 1


class FakeExchange:
    """Serves synthetic history up to and INCLUDING a still-running candle."""

    def __init__(self, first_ts: int, now_ms: int) -> None:
        self.first_ts, self.now_ms, self.calls = first_ts, now_ms, 0

    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=1000):
        self.calls += 1
        start = max(since, self.first_ts)
        out = []
        t = start
        while t <= self.now_ms and len(out) < limit:  # includes the unclosed candle
            out.append([t, 100.0, 101.0, 99.0, 100.0, 1.0])
            t += TF_MS
        return out


def test_load_history_never_caches_unclosed(cfg, tmp_path):
    now = T0 + 5000 * TF_MS + 123_456                  # mid-candle
    ex = FakeExchange(first_ts=0, now_ms=now)
    df = load_history(cfg, now_ms=now, exchange=ex, root=tmp_path)
    last_closed_open = (now // TF_MS) * TF_MS - TF_MS
    assert df["ts"].iloc[-1] == last_closed_open
    assert (df["ts"] + TF_MS <= now).all()
    cache = OhlcvCache(tmp_path / cfg.data["db_path"])
    assert cache.bounds(cfg.symbol, cfg.timeframe)[1] == last_closed_open
    assert np.all(np.diff(df["ts"].to_numpy()) == TF_MS)

    # second call one candle later only fetches the new tail
    calls = ex.calls
    later = now + TF_MS
    ex.now_ms = later
    df2 = load_history(cfg, now_ms=later, exchange=ex, root=tmp_path)
    assert ex.calls == calls + 1
    assert df2["ts"].iloc[-1] == last_closed_open + TF_MS
