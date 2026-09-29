#!/usr/bin/env python3
"""Unduh data harga harian PUBLIK (tanpa kunci) ke CSV untuk backtest.

  python3 ambil_candle.py --bursa indodax --pasangan btc_idr --hari 365 --keluar data/btcidr-harian.csv
  python3 ambil_candle.py --bursa binance --pasangan BTCUSDT --hari 365 --keluar data/btcusdt-harian.csv

Sumber: Indodax `/tradingview/history_v2` (tf=1D) dan Binance `data-api.binance.vision/api/v3/klines`
(interval 1d). Kolom keluaran: tanggal,open,high,low,close,volume. Waktu = tanggal candle (UTC).
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "komunitech-bot-trading-kripto/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def indodax(pasangan, hari):
    sekarang = int(time.time())
    q = urllib.parse.urlencode({"symbol": pasangan.replace("_", "").upper(), "tf": "1D",
                                "from": sekarang - hari * 86400, "to": sekarang})
    data = _get(f"https://indodax.com/tradingview/history_v2?{q}")
    return [(datetime.fromtimestamp(int(c["Time"]), tz=timezone.utc).date().isoformat(),
             c["Open"], c["High"], c["Low"], c["Close"], c["Volume"]) for c in data]


def binance(pasangan, hari):
    q = urllib.parse.urlencode({"symbol": pasangan, "interval": "1d", "limit": min(hari, 1000)})
    data = _get(f"https://data-api.binance.vision/api/v3/klines?{q}")
    return [(datetime.fromtimestamp(int(k[0]) // 1000, tz=timezone.utc).date().isoformat(),
             k[1], k[2], k[3], k[4], k[5]) for k in data]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Unduh candle harian publik ke CSV")
    ap.add_argument("--bursa", choices=("indodax", "binance"), required=True)
    ap.add_argument("--pasangan", required=True)
    ap.add_argument("--hari", type=int, default=365)
    ap.add_argument("--keluar", required=True)
    a = ap.parse_args(argv)
    if not 2 <= a.hari <= 1000:
        print("--hari harus 2-1000.")
        return 1
    try:
        baris = (indodax if a.bursa == "indodax" else binance)(a.pasangan, a.hari)
    except Exception as e:  # noqa: BLE001
        print(f"Gagal mengambil data publik {a.bursa}: {type(e).__name__}: {e}")
        return 2
    if not baris:
        print("Bursa tidak mengembalikan data (cek nama pasangan).")
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.keluar)), exist_ok=True)
    with open(a.keluar, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tanggal", "open", "high", "low", "close", "volume"])
        w.writerows(baris)
    print(f"{len(baris)} baris ({baris[0][0]} s.d. {baris[-1][0]}) disimpan ke {a.keluar}. Sumber: API publik {a.bursa}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
