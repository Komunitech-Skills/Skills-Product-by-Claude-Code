# 01 — Rencana promo 11.11 skincare di Shopee (S1, normal)

## Skenario
Pemilik brand skincare kecil ingin ikut 11.11 dan berencana "diskon gede 40%". Ia memberi harga, modal, potongan Shopee (angka dari rincian penghasilan Seller Center miliknya) dan penjualan biasa. Tanggal hari ini: Rabu, 23 September 2026.

## Input pengguna
> Mau ikut 11.11 di Shopee. Serum 20ml harga 120rb modal 45rb, toner 100ml harga 75rb modal 28rb. Potongan Shopee total kira2 12% + 1.250 per pesanan (aku liat di rincian penghasilan). Serum biasanya laku 80/bulan, toner 50/bulan. Rencana mau diskon 40% biar rame, promonya 3 hari 10–12 Nov. Budget iklan 1 juta. Aman ga? Atau mending bundling?

## Langkah agent (mengikuti SKILL.md)
1. Momen 11.11 adalah tanggal tetap, jadi tanggalnya dihitung script.
2. Opsi disimulasikan dengan script: serum diskon 40% / diskon 25% / bundling 2 = Rp 199.000 / beli 2 gratis 1; toner diskon 20% + gratis ongkir Rp 10.000 / voucher 10% maks Rp 15.000 min. belanja Rp 60.000. Perintah: `cek_promo.py margin --config opsi.json`.
3. Penjualan normal dikonversi ke periode promo 3 hari: serum 80/bulan ≈ **8 unit per 3 hari**, toner 50/bulan ≈ **5 unit per 3 hari** (asumsi, disebut di akhir).
4. Rencana final dicek ulang dengan `cek_promo.py margin --config final.json` (anggaran kampanye Rp 1.000.000).
5. Linimasa: `cek_promo.py jadwal --momen 11.11 --dari 2026-09-23`.

## Output

# Rencana Promo 11.11 — Toko Skincare Kamu
**Periode:** Selasa, 10 November 2026 pukul 00.00 s.d. Kamis, 12 November 2026 pukul 23.59 WIB  |  **Tujuan:** menambah pembeli baru & menjual paket, tanpa merusak laba  |  **Target:** 40 serum satuan + 30 paket (60 serum) + 60 toner, laba bersih ±Rp 4,6 juta  |  **Anggaran:** Rp 1.000.000 (iklan)

## 1. Produk & mekanisme (hasil cek margin)
| Produk | Mekanisme | Harga efektif/unit | Laba/unit (normal → promo) | Margin promo | Status |
|---|---|---|---|---|---|
| Serum 20 ml | Diskon 40% (rencana awal) | Rp 72.000 | Rp 59.350 → Rp 17.110 | 23,8% | ✅ AMAN, tapi laba/unit anjlok 71% |
| Serum 20 ml | Diskon 25% | Rp 90.000 | Rp 59.350 → Rp 32.950 | 36,6% | ✅ AMAN |
| Serum 20 ml | **Bundling 2 = Rp 199.000** | Rp 99.500 | Rp 59.350 → **Rp 41.935** | 42,1% | ✅ AMAN, **terbaik** |
| Serum 20 ml | Beli 2 gratis 1 | Rp 80.000 | Rp 59.350 → Rp 24.983 | 31,2% | ✅ AMAN |
| Toner 100 ml | Diskon 20% + gratis ongkir Rp 10.000 | Rp 60.000 | Rp 36.750 → Rp 13.550 | 22,6% | ✅ AMAN, boros |
| Toner 100 ml | **Voucher 10% (maks Rp 15.000, min. Rp 60.000)** | Rp 67.500 | Rp 36.750 → **Rp 30.150** | 44,7% | ✅ AMAN, **terbaik** |

**Jawaban singkat: diskon 40% tidak rugi, tapi boros.** Laba per serum turun dari Rp 59.350 ke Rp 17.110. Agar laba total sama dengan 3 hari biasa, penjualan harus **3,47x lipat** (dari 8 menjadi minimal 28 serum). Dengan bundling 2 serum Rp 199.000, laba per serum tetap Rp 41.935 dan cukup naik 1,42x (minimal 12 serum).
**Diskon maksimal agar tidak rugi:** serum 56,2% (harga impas Rp 52.557); toner 40,5% bila ditambah gratis ongkir Rp 10.000, atau 55,6% tanpa subsidi ongkir.

**Rekomendasi:**
- Promo utama: **Paket 2 Serum Rp 199.000** (klaim aman "hemat 17%" dari Rp 240.000).
- Pembeli satuan: **serum diskon 25% → Rp 90.000** (klaim "hemat 25%").
- Toner: **voucher toko 10% maks Rp 15.000, min. belanja Rp 60.000** (hemat 10% per toner). Gratis ongkir subsidi Rp 10.000 memakan 27% laba toner, jadi tidak dipakai.

## 2. Hitungan kampanye (dari script)
| Produk | Target | Pesanan | Dibayar pembeli | Laba sebelum iklan |
|---|---|---|---|---|
| Serum satuan diskon 25% | 40 unit | 40 | Rp 3.600.000 | Rp 1.318.000 |
| Paket 2 Serum | 60 unit (30 paket) | 30 | Rp 5.970.000 | Rp 2.516.100 |
| Toner + voucher | 60 unit | 60 | Rp 4.050.000 | Rp 1.809.000 |
| **Total** | **160 unit** | **130** | **Rp 13.620.000** | **Rp 5.643.100** |

Anggaran iklan Rp 1.000.000 → **laba bersih kampanye Rp 4.643.100**. Sebagai pembanding, 3 hari biasa (8 serum + 5 toner) menghasilkan laba ±Rp 658.550. Iklan Rp 1.000.000 tertutup setelah ±31 serum satuan atau ±24 serum dalam paket terjual.
*Target adalah hitungan kebutuhan, bukan ramalan penjualan.*

## 3. Linimasa (dari script)
| Hari | Tanggal | Fase | Kegiatan |
|---|---|---|---|
| H-14 | Rabu, 28 Oktober 2026 | Persiapan | Pesan stok (±70 serum & 70 toner, termasuk cadangan), kardus & bubble wrap; daftar kampanye 11.11 di Seller Center bila tersedia |
| H-7 | Rabu, 4 November 2026 | Pemanasan | Umumkan "Paket 2 Serum Rp 199.000 mulai 10 Nov"; ajak follow toko & simpan produk |
| H-3 | Minggu, 8 November 2026 | Pengingat | Voucher toner bisa diklaim; broadcast hanya ke pelanggan yang setuju menerima pesan |
| H-2 | Senin, 9 November 2026 | Cek sistem | Pastikan harga, paket, dan voucher sudah terjadwal benar di Seller Center |
| H-1 → H+1 | Selasa–Kamis, 10–12 November 2026 | **PROMO BERJALAN** | Pantau stok & chat tiap 2–3 jam; live/story di jam ramai; syarat tidak diubah di tengah jalan |
| H+3 | Sabtu, 14 November 2026 | Kirim & layani | Selesaikan pengiriman; balas ulasan |
| H+7 | Rabu, 18 November 2026 | Evaluasi | Target vs realisasi |
*(Linimasa script disesuaikan: hari H diperpanjang 3 hari sesuai periode promo pengguna. H-2 ditambahkan agent.)*

## 4. Materi & kanal
- Teaser (4–9 Nov): video "Kenapa serum ini dibeli sepasang?" (skill `caption-sosmed-umkm` untuk caption, `foto-produk-brief` untuk foto paket).
- Hari H: live Shopee jam ramai malam (naskah: skill `naskah-live-jualan`).
- Broadcast WA ke pelanggan yang pernah setuju menerima info (skill `broadcast-wa`), dengan cara berhenti berlangganan.

## 5. Kesiapan operasional
- Stok: serum ≥ 110 (40 satuan + 60 paket + cadangan 10), toner ≥ 70.
- Kemasan: 30 kardus paket + bubble wrap; label "Paket 2 Serum".
- Jam potong kirim [isi: jam]; admin piket 10–12 Nov sampai pukul [isi: jam].

## 6. Syarat & ketentuan promo (siap tempel)
**Promo 11.11 — <nama toko>**
1. Periode promo: Selasa, 10 November 2026 pukul 00.00 s.d. Kamis, 12 November 2026 pukul 23.59 WIB.
2. Produk yang ikut: Serum 20 ml (satuan Rp 90.000 dari Rp 120.000), Paket 2 Serum 20 ml Rp 199.000, Toner 100 ml (voucher toko).
3. Harga promo berlaku selama periode di atas atau sampai stok promo habis (serum 100 unit, toner 60 unit).
4. Voucher toko 10% untuk Toner 100 ml, maksimal potongan Rp 15.000, minimum belanja Rp 60.000, kuota 60 voucher.
5. Isi Paket 2 Serum tidak dapat ditukar dengan produk lain. (asumsi, ganti dengan data Anda)
6. Promo tidak dapat digabung dengan voucher toko lain (voucher platform mengikuti ketentuan Shopee). (asumsi, ganti dengan data Anda)
7. Pesanan dikirim paling lambat [isi: jumlah] hari kerja setelah pembayaran.
8. Retur/tukar untuk barang rusak atau salah kirim maksimal [isi: jumlah] hari setelah diterima, dengan [isi: bukti yang diminta, mis. video pembukaan paket].

## 7. Ukuran evaluasi (H+7, 18 November 2026)
Unit terjual per produk vs target, laba bersih setelah iklan (bukan omzet), biaya iklan per pesanan, stok sisa, jumlah keluhan/retur (skill `analisis-ulasan`).

**Asumsi & catatan:**
- Potongan platform 12% + Rp 1.250 per pesanan berasal dari pengguna (rincian penghasilan Seller Center). Tarif bisa berubah; cek lagi sebelum 10 Nov. Program gratis ongkir/cashback dari platform yang diikuti harus ditambahkan ke persen potongan.
- Penjualan normal 3 hari = 80/bulan × 3/30 ≈ 8 serum dan 50 × 3/30 = 5 toner.
- Harga coret Rp 120.000 dan Rp 75.000 harus harga yang benar-benar berlaku sebelum promo (UU 8/1999 Pasal 11 huruf f). Kuota & jam wajib dipenuhi (Pasal 12).
- Waktu kirim, batas retur/tukar, jam potong kirim, dan jam piket admin tidak diberikan pengguna, jadi ditulis `[isi: ...]`; lengkapi dengan kebijakan toko Anda sebelum S&K ditayangkan. Syarat nomor 5 dan 6 adalah usulan (asumsi, ganti dengan data Anda).
- Pembulatan: harga promo dari diskon % dibulatkan ke atas ke Rp 100; klaim % dibulatkan ke bawah. Ini alat bantu perencanaan, bukan jaminan hasil atau nasihat hukum.

## Catatan penguji
- **Verifikasi independen:** 300 kombinasi acak (diskon, harga promo, potongan Rp, bundling, beli-gratis, voucher Rp/% dengan cap & min. belanja, subsidi ongkir, cashback, biaya lain, biaya platform) dihitung ulang dengan python terpisah memakai pecahan eksak. Laba/unit, margin, harga impas, diskon maksimal dan status **cocok 300/300**. Angka di atas dicek manual, contohnya: Paket 2 Serum 199.000 − 23.880 − 1.250 − 90.000 = 83.870 → 41.935/unit ✓; toner 75.000 − 7.500 (voucher) − 8.100 − 1.250 − 28.000 = 30.150 ✓.
- Nama hari di linimasa dicek dengan `datetime`: 28 Okt 2026 Rabu, 11 Nov 2026 Rabu, 18 Nov 2026 Rabu ✓.
- Kurang: (1) Saat banyak **opsi** dibandingkan dalam satu `--config`, "Ringkasan kampanye" menjumlahkan semua opsi (total 519 unit tanpa arti). Agent harus menjalankan ulang untuk rencana final. (2) Script hanya mendukung hari H satu tanggal; periode promo 3 hari harus disesuaikan agent. (3) "Unit normal" harus sepanjang periode promo; SKILL.md tidak menjelaskan konversi ini ke pengguna awam.
