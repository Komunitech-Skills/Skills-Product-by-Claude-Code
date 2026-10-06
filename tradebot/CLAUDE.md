# CLAUDE.md — Crypto Trading Bot (EMA Trend + RSI Filter)

## Peran
Kamu senior quant developer + risk engineer. Bangun bot trading kripto yang aman, bisa di-backtest, dan jalan 24/7. Prioritas: **correctness dan keamanan di atas kecepatan**. Kalau spec ambigu, TANYA, jangan asumsi.

## Cara Kerja (WAJIB)
- Kerjakan **satu fase**, lalu **BERHENTI** dan tunggu approval eksplisit dari user sebelum lanjut.
- Di akhir tiap fase: ringkas apa yang dibuat, asumsi yang dipakai, dan risiko yang kamu lihat.
- **Jangan tulis kode live executor sebelum Fase 4.** Jangan sentuh API key asli sebelum Fase 5.
- Jangan ubah parameter strategi setelah melihat hasil backtest. Kalau ada usulan, laporkan sebagai saran, bukan diterapkan.

## Keputusan user (2026-10-06, Fase 1)
- **Sizing fee-aware:** `qty = risk / (entry×(1+fee) − SL×(1−slippage)×(1−fee))` → rugi aktual di SL ≤ 1% equity (fee + slippage termasuk). Menggantikan rumus `risk/(entry−SL)` di bawah.
- **Backtest memakai simulator sendiri** (`backtest/simulator.py`), bukan vectorbt: aturan exit/fill harus persis dan logika fill dipakai ulang oleh paper executor.
- **Lokasi kode:** folder `tradebot/` di root repo Skills Factory (tidak tercatat di catalog.csv, tidak ikut build skill).

## Konteks
- Exchange: Binance **spot** (long-only)
- Pair: BTC/USDT, timeframe 4h, max 1 posisi terbuka
- Modal awal: 1.000 USDT (configurable), equity berjalan (compounding)
- Risk per trade: 1% dari equity berjalan
- Stack: Python 3.11, ccxt, pandas, vectorbt (backtest), SQLite, python-telegram-bot
- Hosting nanti: VPS + systemd
- Mode awal: **PAPER**. Live hanya setelah user approve eksplisit.

## Strategi: EMA Trend + RSI Filter

### Entry (dievaluasi hanya pada candle yang sudah CLOSE)
Semua harus terpenuhi:
1. **Cross up:** `EMA20[t-1] <= EMA50[t-1]` DAN `EMA20[t] > EMA50[t]`
2. **RSI(14)[t]** antara 45 dan 70 (inklusif)
3. **Close[t] > EMA200[t]**

Parameter angka bulat, **dilarang di-tuning**: 20/50/200, RSI 14, band 45–70.

### Harga entry
- Fill di **open candle berikutnya** (t+1) setelah sinyal. Jangan pakai close candle sinyal (lookahead bias).
- Slippage 0.05% merugikan (entry lebih mahal).

### Stop Loss
- `SL = min(Low dari 10 candle terakhir, TERMASUK candle sinyal) × (1 − 0.005)`
- Jarak risiko dihitung dari harga entry: `(entry − SL) / entry`
- Kalau jarak SL **> 4%** → **skip trade** (log alasan).
- Kalau SL >= entry (data aneh) → skip + log error.

### Take Profit
- `TP = entry + 2 × (entry − SL)` (RR 1:2)

### Exit (mana yang kena duluan)
1. **SL/TP intrabar** (cek High/Low candle)
2. **Exit sinyal:** EMA20 cross ke bawah EMA50 → exit di **open candle berikutnya** setelah cross terdeteksi
- Kalau SL dan TP sama-sama tersentuh di candle yang sama → **asumsikan SL kena duluan** (konservatif).
- Kalau candle entry (t+1) sendiri menyentuh SL → SL kena di candle itu juga.

### Position Sizing
```
risk_amount = equity * 0.01
qty = risk_amount / (entry - SL)      # diganti versi fee-aware, lihat "Keputusan user"
```
- Fee **0.1% per sisi** (entry dan exit), dimasukkan ke PnL.
- Slippage **0.05%** merugikan di entry, SL exit, dan exit sinyal. TP (limit) tanpa slippage.
- Batasi qty: nilai posisi tidak boleh melebihi equity yang tersedia (spot, tanpa leverage).
- Bulatkan qty ke **stepSize** Binance, cek **minNotional**; kalau di bawah minimum → skip + log.

## Aturan Wajib (non-negotiable)
1. API key hanya via `.env`, permission **trade-only, TANPA withdrawal**, whitelist IP VPS. Jangan pernah hardcode secret. `.env` ada di `.gitignore`.
2. **Setiap order wajib punya SL.** Tidak ada order tanpa SL. Di live: pakai OCO (SL + TP) di sisi exchange.
3. **Daily max drawdown 3%** → bot auto-halt + alert Telegram.
4. Semua trade, error, dan keputusan di-log ke SQLite + Telegram.
5. **Kill switch:** `/stop` di Telegram → tutup semua posisi, set flag `halted` persisten di DB (restart tidak boleh mengaktifkan bot lagi). Hanya terima dari chat ID user. `/resume` manual untuk melanjutkan.
6. **Live butuh 2 kunci:** `mode: live` di config DAN konfirmasi lewat Telegram `/golive <kode>`. Default selalu paper.
7. **Startup reconciliation:** saat nyala, bandingkan state DB dengan posisi/order asli di exchange. Kalau beda → berhenti + alert, jangan menebak.
8. **Idempotency:** `clientOrderId` unik per sinyal. **Jangan retry order sebelum cek status order.**
9. Heartbeat Telegram tiap 6 jam.
10. Buang candle yang belum close. Semua timestamp UTC.

## Arsitektur
Prinsip: **strategy = pure function** (data masuk, sinyal keluar), dipakai **identik** oleh backtest, paper, dan live. Hanya executor yang beda.

```
tradebot/
├── .env.example
├── config.yaml           # pair, tf, risk %, mode (paper|live)
├── main.py               # scheduler + wiring
├── core/
│   ├── data.py           # fetch OHLCV ccxt, cache SQLite
│   ├── strategy.py       # EMA/RSI -> Signal(entry, sl, tp)
│   ├── sizing.py         # fill fee/slippage + sizing fee-aware (dipakai backtest & paper)
│   ├── risk.py           # sizing, veto, daily DD, halt
│   ├── executor_base.py  # interface
│   ├── executor_paper.py # fee + slippage simulasi
│   ├── executor_live.py  # ccxt + OCO (Fase 4, off default)
│   ├── store.py          # SQLite: trades, orders, events, state
│   └── notifier.py       # Telegram out + command in
├── backtest/run.py       # pakai strategy.py yang sama
├── tests/
└── deploy/bot.service
```

Alur per candle 4h close: scheduler bangun +10 detik setelah close → `data` → `strategy` → `risk` (hak veto: SL ada, jarak ≤ 4%, belum ada posisi, tidak halted, DD harian belum kena) → `executor` → `store` + `notifier`. Loop terpisah tiap 1 menit: cek posisi, PnL harian, trigger halt.

## Fase Pengerjaan

### Fase 1 — Data + Strategy + Backtest (SELESAI 2026-10-06, menunggu approval)
Buat: `data.py`, `strategy.py`, `backtest/run.py`, `tests/`. **Stop setelah ini.**
- Data: tarik **3 tahun** OHLCV BTC/USDT 4h dari Binance via ccxt, cache ke SQLite. Warm-up minimal 200 candle sebelum sinyal pertama.
- Split: **in-sample** (2 tahun pertama) dan **out-of-sample** (1 tahun terakhir). Laporkan keduanya terpisah.
- Metrik: jumlah trade, win rate, profit factor, expectancy per trade, max drawdown, Sharpe (annualisasi 4h: `sqrt(6*365)`), total return, dan **pembanding buy & hold**.
- **Flag overfit/tidak meyakinkan** kalau: trade < 30, performa OOS jauh lebih buruk dari IS, profit factor bergantung pada 1–2 trade besar, atau return hanya sedikit di atas buy & hold dengan DD lebih buruk.
- Hasil biasa saja itu normal. Tujuan fase ini validasi pipeline, bukan cari profit.

**Unit test wajib (sebelum mempercayai angka backtest):**
- Cross terdeteksi tepat 1x, bukan tiap candle
- Entry di open t+1, bukan close sinyal
- Tidak ada lookahead (hasil sinyal di t tidak berubah kalau data setelah t dihapus)
- Candle belum close dibuang
- SL dan TP di candle yang sama → SL menang
- Swing low termasuk candle sinyal
- Skip trade kalau jarak SL > 4%
- Sizing: risiko aktual ≈ 1% equity (termasuk fee), pembulatan stepSize, skip < minNotional
- Fee dan slippage dihitung di entry dan exit

### Fase 2 — Risk manager + Store
`risk.py`, `store.py` + unit test (DD harian, halt persisten, veto). Pakai test ketat, ini kode yang menjaga uang.

### Fase 3 — Paper trading engine + Notifier
`executor_paper.py`, `notifier.py`, `main.py`. Kondisi identik live (fee, slippage, stepSize). Telegram: notif trade, heartbeat, `/stop`, `/resume`, `/status`. Jalankan paper minimal 2–4 minggu sebelum Fase 4.

### Fase 4 — Live executor (OFF default)
`executor_live.py` dengan OCO, idempotency, reconciliation. Checklist go-live ditulis dan harus dicentang user. Uji pertama dengan nominal sangat kecil.

### Fase 5 — Deploy + README
systemd auto-restart, README: setup, cara monitor, checklist harian.

## Standar Kode
- Type hints, docstring singkat, logging terstruktur (jangan `print`).
- Semua angka uang pakai `Decimal` atau handling presisi yang jelas di layer executor.
- Config di `config.yaml`, secret di `.env`. Tidak ada magic number di kode.
- Tiap modul penting punya test. Jangan lanjut fase kalau test merah.
