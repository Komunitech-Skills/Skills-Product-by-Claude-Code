# Uji ulang OpenClaw — Toko Online 05 · Promo 11.11 diskon 30% (promo-kalender 1.0.3)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · Uji pertama: [05-promo-1111-cek-margin.md](05-promo-1111-cek-margin.md)

OpenClaw lokal, model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`). Home `sol-toko-online` direset dari skill terbaru, sesi baru. Sisi SEBELUM memakai hasil uji pertama.

**Cacat yang diuji ulang:** (1) target dihitung untuk promo 3 hari tetapi linimasa & S&K memakai 1 hari; (2) S&K memuat janji "Dikirim maks 2 hari kerja" yang tidak diberikan pemilik.

## Pesan member (sama persis)

> kak 11.11 nanti aku mau diskon 30% buat serum wajah aku. harga normal 89rb, modal 41rb. jualnya di shopee potongan admin dll totalnya kira2 12% + 1250 per pesanan. masih untung ga? biasanya sebulan laku 60 botol. bikinin rencana promonya skalian ya

## Balasan SESUDAH baru — utuh

_Alat: `read, exec` (6 panggilan, 0 gagal) · durasi 78 detik_

> Cek margin pakai angka yang kakak kasih — **masih untung**, diskon 30% aman dipakai. Ini rencananya:
> 
> ## 1. Cek margin (Serum Wajah, modal Rp 41.000, platform 12% + Rp 1.250/pesanan)
> 
> **Diskon 30% → harga promo Rp 62.300**
> - Laba normal/unit: Rp 36.070 (margin 40,5%)
> - Laba promo/unit: Rp 12.574 (margin 20,2%) → **✅ AMAN**, bukan tipis
> - Diskon maksimal biar nggak rugi: 46,0% — jadi 30% masih jauh dari batas
> - Supaya laba 11.11 nyamain laba hari biasa, penjualan harus naik 2,87x lipat
> 
> **Pembanding, diskon 20% → harga promo Rp 71.200** (kalau mau main aman)
> - Laba promo/unit: Rp 20.406 (margin 28,7%)
> - Perlu naik 1,77x lipat buat samain laba hari biasa
> 
> Rekomendasi: **pakai diskon 30%** sesuai rencana kakak — marginnya masih sehat (20,2%), cuma perlu jualan lebih banyak biar untung totalnya nambah, bukan sekadar nutup laba harian.
> 
> ## 2. Hitungan kampanye (asumsi promo 1 hari, 11 Nov — normal 60 botol/bulan ≈ 2 botol/hari)
> - Target minimal: **6 botol** (biar laba hari itu ≥ laba hari biasa)
> - Kalau laku 6 botol: omzet Rp 373.800, laba Rp 75.444
> - Makin banyak dari 6, makin untung — nggak ada batas atas selama stok ada
> 
> *Kalau maksud kakak promo 2–3 hari, kabarin ya, nanti aku hitung ulang target & linimasanya biar pas.*
> 
> ## 3. Linimasa 11.11
> - **H-14 (28 Okt):** fiksasi harga promo Rp 62.300, cek stok & kemasan, daftar promo di Seller Center kalau ada program Shopee
> - **H-7 (4 Nov):** mulai teaser — foto/video "diskon 30% khusus 11.11", ajak follow/wishlist toko
> - **H-3 (8 Nov):** share info promo ke pelanggan yang udah pernah chat/beli
> - **H-1 (10 Nov):** cek ulang harga & stok di sistem Shopee udah bener
> - **H (11 Nov):** promo jalan, pantau stok & chat tiap 2-3 jam
> - **H+3 (14 Nov):** kebut kirim semua pesanan promo
> - **H+7 (18 Nov):** evaluasi — unit terjual vs target 6, laba, sisa stok
> 
> ## 4. Syarat & Ketentuan (siap tempel)
> 1. Periode promo: Rabu, 11 November 2026, pukul [isi: jam mulai] s.d. [isi: jam selesai] WIB
> 2. Produk: Serum Wajah — harga normal Rp 89.000, harga promo Rp 62.300 (diskon 30%)
> 3. Berlaku untuk [isi: kuota] unit pertama atau selama stok masih ada
> 4. Maksimal pembelian [isi: jumlah] unit per akun
> 5. Pesanan dikirim paling lambat [isi: jumlah] hari kerja setelah pembayaran
> 6. Retur/penukaran mengikuti kebijakan toko: [isi: ringkasan kebijakan]
> 
> *(Bagian [isi: ...] itu yang perlu kakak lengkapi sendiri — aku nggak mau ngarang kuota/jam kirim.)*
> 
> **Catatan:** stok minimal 6 botol harus siap tanggal 11 Nov — kalau stok sekarang kurang dari itu, kabari aku biar ukuran target disesuaikan.
## Verifikasi independen (Python; laba = harga − 12%×harga − 1.250 − 41.000)

| Hal | Hitung ulang | Balasan baru |
|---|---|---|
| Laba normal Rp 89.000 | Rp 36.070 (40,5%) | ✅ |
| Diskon 30% → Rp 62.300 | Rp 12.574 (20,2%) | ✅ |
| Diskon 20% → Rp 71.200 | Rp 20.406 (28,7%) | ✅ |
| Diskon maks sebelum rugi | 46,05% | ✅ "46,0%" |
| Kelipatan agar laba = normal | 30%: 2,87x · 20%: 1,77x | ✅ |
| Promo 1 hari: normal 60/30 = 2 botol/hari, laba normal Rp 72.140 | 6 botol → Rp 75.444 (≥), 5 botol → Rp 62.870 (<) → target **6** | ✅ |
| Omzet 6 botol | Rp 373.800 | ✅ |
| Tanggal | 11 Nov 2026 Rabu; H-14 28 Okt, H-7 4 Nov, H-3 8 Nov, H-1 10 Nov, H+3 14 Nov, H+7 18 Nov | ✅ semua |

## Penilaian

- **Cacat 1 (periode tidak konsisten): HILANG — ya.** Periode ditetapkan sekali: *"asumsi promo 1 hari, 11 Nov — normal 60 botol/bulan ≈ 2 botol/hari"* → target 6 botol; linimasa H-day 11 Nov; evaluasi "unit terjual vs target 6"; S&K "Rabu, 11 November 2026". Semua memakai 1 hari. Agent juga menawarkan hitung ulang bila maksud member 2–3 hari.
- **Cacat 2 (janji kirim dikarang): HILANG — ya.** S&K: *"Pesanan dikirim paling lambat [isi: jumlah] hari kerja setelah pembayaran"*, kuota, batas per akun, jam, dan retur juga `[isi: …]`, dengan catatan *"aku nggak mau ngarang kuota/jam kirim."*
- **Regresi / kekurangan baru:**
  - Opsi **bundling 2 botol** (di uji pertama: laba/botol Rp 24.375, 2x diskon 30%) tidak muncul lagi; pembanding hanya diskon 20%. Nilai saran sedikit turun (variasi model, bukan cacat skill).
  - Peringatan **harga coret palsu** ("jangan naikin dulu baru didiskon") yang ada di uji pertama tidak muncul di S&K; S&K hanya mencantumkan harga normal Rp 89.000. Kecil.
  - Pengingat "cek potongan di Seller Center / bukan ramalan penjualan" tidak muncul lagi. Kecil.
  - Tidak ada angka yang salah.

| | Sesudah (lama) | Sesudah (baru) |
|---|---|---|
| Skor | 8 | **8,5** |

Alasan: dua cacat yang dilaporkan tertutup dengan bukti jelas dan semua angka benar; tidak naik ke 9 karena opsi bundling dan peringatan harga coret yang dulu jadi nilai tambah kini hilang (jawaban sedikit lebih tipis).
