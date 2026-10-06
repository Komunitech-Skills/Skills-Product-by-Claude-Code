# tradebot — BTC/USDT 4h, EMA Trend + RSI Filter

Status: **Fase 1 (data + strategy + backtest)**. Belum ada eksekusi order, belum ada API key.
Spec lengkap & keputusan: [`CLAUDE.md`](CLAUDE.md). Bukan nasihat investasi.

## Jalankan (Python 3.11)

```bash
cd tradebot
python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q          # wajib hijau sebelum mempercayai angka backtest
.venv/bin/python -m backtest.run       # tarik/cache data 3 thn + warm-up, tulis laporan ke reports/
.venv/bin/python -m backtest.run --offline   # pakai cache SQLite saja
```

Data publik diambil dari `data-api.binance.vision` (mirror market data resmi Binance;
`api.binance.com` menolak sebagian lokasi dengan HTTP 451). Ubah `exchange.public_api_url`
di `config.yaml` bila perlu. Di balik proxy perusahaan, `exchange.trust_env: true` membuat ccxt
memakai `HTTPS_PROXY` / `REQUESTS_CA_BUNDLE`.

## Isi

| File | Fungsi |
|---|---|
| `core/data.py` | fetch OHLCV via ccxt, cache SQLite (hanya candle tertutup), cek gap/OHLC |
| `core/strategy.py` | indikator + sinyal entry/exit + SL/TP plan — fungsi murni |
| `core/sizing.py` | harga fill (fee, slippage) + sizing fee-aware, stepSize/minNotional |
| `backtest/simulator.py` | loop candle-per-candle (urutan event di docstring) |
| `backtest/metrics.py` | metrik + flag overfit |
| `backtest/run.py` | CLI: split IS/OOS, laporan `reports/backtest-YYYY-MM-DD.{md,json}` + daftar trade CSV |
