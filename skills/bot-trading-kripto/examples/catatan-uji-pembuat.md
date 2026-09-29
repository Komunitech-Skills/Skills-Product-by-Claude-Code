# Catatan uji oleh PEMBUAT skill (bukan HASIL-UJI independen) — 2026-09-29

Penguji independen (Tahap 6) tetap wajib menjalankan 5 skenario, uji A/B, banding pesaing,
dan verifikasi angka sendiri. Catatan ini hanya merekam apa yang sudah dijalankan pembuat.

## 1. Uji regresi otomatis
`python3 tests/uji_regresi.py` → 47 tes:
```
----------------------------------------------------------------------
Ran 47 tests in 0.597s

OK
```
Cakupan: vektor tanda tangan dari dokumentasi resmi (Binance HMAC-SHA256 `c8db5682…6b71`,
Indodax HMAC-SHA512 `bab004e5…ae99`), validasi konfigurasi (batas risiko wajib, float
ditolak, grid × nominal ≤ modal total, live Binance butuh pernyataan, live tanpa pajak ditolak),
matematika DCA/grid/TP-SL/rebalancing, isi order + fee + PPh (dibulatkan ke bawah), rata-rata
tertimbang, stop-loss global, rugi harian (termasuk pergantian hari), batas modal & order
terbuka, tombol berhenti (+ notifikasi sekali), `--lanjutkan` wajib `--saya-sudah-cek`,
perubahan aturan saat memegang koin, `--openclaw` selalu exit 0, kunci (izin file 600, di
repo git ditolak, di folder skill ditolak, repr tersembunyi, penyamar log, URL uji hanya
localhost), gerbang live bertahap (tanpa bukti paper, frasa salah, tanpa pernyataan withdraw,
tanpa `--izinkan-live`, kunci ber-withdraw, konfigurasi berubah), order putus → berhenti,
order ditolak → berhenti, Indodax lewat server tiruan, backtest data asli dengan verifikasi
kas & PPh independen, CSV rusak.

## 2. Endpoint publik — dipanggil SUNGGUHAN dari lingkungan uji
| Endpoint | Hasil |
|---|---|
| Indodax `/api/ticker/btcidr` | OK, harga ±Rp1,50 miliar |
| Indodax `/api/pairs` | OK, `trade_min_base_currency` 10000, fee taker 0,2% |
| Indodax `/tradingview/history_v2` (1D, 365 hari) | OK, 366 baris → `tests/data/btcidr-harian-2025-2026.csv` |
| Binance `data-api.binance.vision` ticker/exchangeInfo/klines | OK, 365 baris → `tests/data/btcusdt-harian-2025-2026.csv` |
| Binance `testnet.binance.vision` & `api.binance.com` | **Ditolak HTTP 451 "restricted location"** (IP lingkungan uji) |
| `demo-indodax.com` | **302 ke login Cloudflare Access** — tidak bisa diuji |

## 3. Endpoint bertanda tangan — diuji terhadap SERVER TIRUAN
`tests/mock_bursa.py` meniru contoh respons dokumentasi resmi & memverifikasi tanda tangan,
timestamp/recvWindow, dan header kunci. Lihat transkrip `contoh-03`. **Belum** diuji terhadap
akun Binance testnet / demo Indodax / live sungguhan → pemilik/tim perlu uji platform asli
(Tahap 6.10) dengan kunci testnet milik pemilik sebelum status naik.

## 4. Yang belum dilakukan
- Uji A/B tanpa-skill vs dengan-skill, uji banding pesaing, 5 skenario independen.
- Jadwal `--command-argv` di Gateway OpenClaw khusus untuk skill ini.

## 5. Uji muat OpenClaw
`bash scripts/uji_openclaw.sh` (OpenClaw 2026.9.6 eb377ac): eligible 100/100, modelVisible 100/100,
commandVisible 100/100 — termasuk `bot-trading-kripto`.
- Uji di Windows.
