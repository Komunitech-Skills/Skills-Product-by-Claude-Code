# Skema konfigurasi & rumus strategi

Semua angka ditulis sebagai **teks** (`"100000"`), kecuali `jumlah_grid`, `interval_jam` (boleh
angka bulat) dan `order_terbuka_maks` (angka bulat). Float (`100000.5` tanpa kutip) ditolak.

## Kerangka
```json
{
  "mode": "paper | testnet | live",
  "bursa": "indodax | binance",
  "pasangan": "btc_idr (Indodax) | BTCUSDT (Binance, wajib + koin & kutipan)",
  "strategi": { "jenis": "dca | grid | tp_sl | rebalancing", "...": "..." },
  "batas_risiko": {
    "modal_maks_per_order": "…", "modal_maks_total": "…",
    "stop_loss_persen": "…", "rugi_harian_maks": "…", "order_terbuka_maks": 2
  },
  "biaya": { "fee_persen": "0.2", "pajak": "domestik | luar_negeri | tidak_dihitung" },
  "kunci": { "file": "~/.komunitech/kunci-bot.json" }  // atau {"env": true}; wajib testnet/live
}
```
Opsional: `langkah_jumlah` & `min_nilai_order` (untuk paper; testnet/live diambil dari bursa).

## Strategi (semua milik member; bot tidak menilai)
| Jenis | Field | Perilaku per putaran |
|---|---|---|
| `dca` | `nominal_per_beli`, `interval_jam`, opsional `take_profit_persen` | Beli `nominal` bila sudah ≥ `interval_jam` sejak beli terakhir. Bila TP diisi & harga ≥ rata-rata × (1+TP%) → jual semua posisi bot, DCA lanjut. |
| `grid` | `harga_bawah`, `harga_atas`, `jumlah_grid` (2–100), `nominal_per_grid` | Level L_i = bawah + i×(atas−bawah)/N. Harga di pita [L_i, L_i+1) & slot i kosong → beli `nominal`. Slot i terisi & harga ≥ L_i+1 → jual jumlah slot itu. Di luar rentang: tidak beli. Syarat: N × nominal ≤ modal total. |
| `tp_sl` | `nominal_beli`, `take_profit_persen`, `stop_loss_persen`, opsional `harga_masuk_maks` | Masuk sekali (bila harga ≤ harga_masuk_maks, jika diisi). Jual semua saat ≥ rata-rata × (1+TP%) atau ≤ rata-rata × (1−SL%). Lalu selesai (tidak masuk ulang). |
| `rebalancing` | `target_persen_koin`, `ambang_deviasi_persen` | Nilai total E = kas bot + koin × harga. Bila \|porsi koin − target\| ≥ ambang → beli/jual selisih (E × target − nilai koin), dibatasi `modal_maks_per_order` dan kas. |

## Batas risiko (dicek setiap putaran, sebelum strategi)
| Batas | Rumus | Akibat |
|---|---|---|
| Stop-loss global | harga ≤ rata-rata × (1 − SL%) | jual semua posisi bot → **berhenti** |
| Rugi harian | nilai pada putaran terakhir sebelum 00.00 WIB − nilai sekarang > `rugi_harian_maks` | **berhenti** |
| Modal per order | nilai beli > `modal_maks_per_order` | **berhenti** |
| Modal total | modal terpakai (biaya perolehan posisi) + order > `modal_maks_total` | **berhenti** |
| Order terbuka | jumlah order terbuka di bursa ≥ `order_terbuka_maks` | **berhenti** |
| Tombol berhenti | file `bot/STOP` ada | **berhenti** |
Lain-lain yang menghentikan bot: status order tidak pasti, order ditolak bursa, kunci
bermasalah/berizin withdraw (Binance live), konfigurasi berubah saat memegang koin, gerbang live gagal.
Berhenti = tidak ada order baru; posisi tidak dijual (kecuali stop-loss).

## Akuntansi bot
- Kas bot awal = `modal_maks_total` (anggaran virtual; bot tidak memakai saldo lain di akun).
- Beli: jumlah = bulat_bawah((nominal / (1+fee)) / harga, lot); bayar = harga×jumlah + fee ≤ nominal.
- Jual: bruto = harga × jumlah; fee = bruto × fee%; PPh = ⌊bruto × tarif⌋; bersih = bruto − fee − PPh.
- Untung/rugi terealisasi memakai **harga rata-rata tertimbang** (berbeda dari FIFO di skill
  `pantau-pasar-kripto`; keduanya sah, sebut metodenya bila dibandingkan).
- Rupiah dibulatkan ke rupiah terdekat; USDT 8 desimal; PPh dibulatkan ke bawah.

## File di folder bot
`konfigurasi.json` (member) · `state.json` (status bot) · `audit.jsonl` (log semua kejadian,
append-only, kunci disamarkan) · `transaksi.csv` · `STOP` (tombol berhenti) ·
`KONFIRMASI-LIVE.json` (bukti konfirmasi live).
