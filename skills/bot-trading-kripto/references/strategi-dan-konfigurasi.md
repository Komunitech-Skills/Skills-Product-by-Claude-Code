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
| Rugi harian | nilai pada putaran terakhir sebelum 00.00 WIB − nilai sekarang > `rugi_harian_maks`. Patokan per tanggal disimpan di `state.json` (`buku_rugi_harian`) dan tidak pernah ditimpa; tanggal diambil dari waktu putaran **terbaru yang pernah dilihat** (`waktu_terakhir`), jadi jam komputer mundur tidak me-reset batas. **Juga 24 jam bergulir:** nilai pada sampel tertua dalam 24 jam terakhir (jam komputer, sampel tiap 15 menit di `jejak_ekuitas`) − nilai sekarang > `rugi_harian_maks` → berhenti (lebih ketat dari per tanggal). Selama jam tidak monoton (jam < putaran terbaru), patokan = yang tertinggi dari tanggal jam komputer s.d. tanggal efektif | **berhenti** |
| Modal per order | nilai beli > `modal_maks_per_order` | **berhenti** |
| Modal total | modal terpakai (biaya perolehan posisi) + order > `modal_maks_total`. **Live:** modal terpakai = max(buku live folder, buku live global akun di `~/.komunitech/bot-trading-kripto/akun/`, (saldo koin bursa − saldo milik member sebelum live pertama) × harga + order beli terbuka), dicek sebelum SETIAP beli di bawah kunci akun (satu proses per kunci API); buku live tidak di-reset oleh ganti mode atau hapus folder bot | **berhenti** |
| Order terbuka | jumlah order terbuka di bursa ≥ `order_terbuka_maks` | **berhenti** |
| Tombol berhenti | salah satu ada: `<folder bot>/STOP`, `<folder konfigurasi>/STOP`, `~/.komunitech/bot-trading-kripto/STOP-<id konfigurasi>`, `~/.komunitech/bot-trading-kripto/STOP-SEMUA` | **berhenti** |
Lain-lain yang menghentikan bot: status order tidak pasti, order ditolak bursa, kunci
bermasalah/berizin withdraw (Binance live), konfigurasi berubah saat memegang koin, gerbang live gagal.
Berhenti = tidak ada order baru; posisi tidak dijual (kecuali stop-loss).

## Akuntansi bot
- Kas bot awal = `modal_maks_total` (anggaran virtual; bot tidak memakai saldo lain di akun).
- Beli: jumlah = bulat_bawah((nominal / (1+fee+t)) / harga, lot); bayar = harga×jumlah + fee + PPh beli ≤ nominal.
  t = PPh sisi beli: 0 untuk kutipan rupiah; = tarif PPh untuk kutipan aset kripto (USDT dll., swap,
  PMK 50/2025 Pasal 12 ayat (5) huruf b).
- Jual: bruto = harga × jumlah; fee = bruto × fee%; PPh = ⌊bruto × tarif⌋; bersih = bruto − fee − PPh.
- Untung/rugi terealisasi memakai **harga rata-rata tertimbang** (berbeda dari FIFO di skill
  `pantau-pasar-kripto`; keduanya sah, sebut metodenya bila dibandingkan).
- Rupiah dibulatkan ke rupiah terdekat; USDT 8 desimal; PPh dibulatkan ke bawah.
- **Grid:** rata-rata dihitung dari SEMUA koin bot. Akibatnya stop-loss global bisa terpicu saat harga
  masih di dalam rentang grid, dan jual satu slot di atas harga belinya bisa tercatat rugi (pesan
  bot memberi catatan). Pilih `stop_loss_persen` dengan mempertimbangkan lebar grid.
- Angka ditulis tanpa pemisah ribuan ("500000"); "500.000" ditolak supaya tidak terbaca Rp500.

## File di folder bot
`konfigurasi.json` (member) · `state.json` (status bot) · `audit.jsonl` (log semua kejadian,
append-only, kunci disamarkan) · `transaksi.csv` · `STOP` (tombol berhenti; juga ada salinan global di
`~/.komunitech/bot-trading-kripto/`) ·
`KONFIRMASI-LIVE.json` (bukti konfirmasi live; **sekali pakai**, berisi `id`, `hash_konfigurasi`, `waktu`,
`segel`, dan `dipakai` setelah dipakai). Di `state.json`, buku tiap mode yang sedang tidak aktif disimpan
di `buku_per_mode` (buku live tidak pernah dibuang), konfirmasi yang sudah dipakai di
`konfirmasi_live_dipakai`, dan sesi live aktif di `sesi_live`.
