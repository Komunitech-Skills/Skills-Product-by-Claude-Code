# 03 — "bikinin promo gajian dong" kopi literan (S3, singkat/malas)

## Skenario
Penjual kopi susu literan menulis permintaan pendek tanpa kanal jualan, penjualan normal, atau anggaran. Hari ini Rabu, 23 September 2026.

## Input pengguna
> bikinin promo gajian dong buat kopi literan aku 85rb modal 50rb

## Langkah agent
Info wajib (momen, harga, HPP) sudah ada. Kanal jualan tidak disebut, jadi **default 0% biaya platform (jualan langsung/WA)**, dengan asumsi yang disebut di akhir. Tanggal gajian default 25. Karena 25 September tinggal 2 hari, agent memakai 25 Oktober: `cek_promo.py jadwal --momen gajian --tanggal-gajian 25 --dari 2026-09-26`. Dua opsi dicek: diskon 15% dan bundling 2 = Rp 155.000.

## Output

# Rencana Promo Gajian — Kopi Susu Literan
**Periode:** Sabtu, 24 Oktober 2026 pukul 17.00 s.d. Selasa, 27 Oktober 2026 pukul 21.00 WIB  |  **Tujuan:** menambah pembeli ulang saat gajian  |  **Anggaran:** Rp 0 (konten sendiri)

Gajian 25 September tinggal 2 hari, terlalu mepet untuk persiapan, jadi rencana ini untuk **gajian 25 Oktober 2026 (Minggu)**. Kalau kamu tetap mau promo minggu ini, bisa pakai versi kilat: pengumuman hari ini, promo 25–27 September.

## 1. Pilihan promo (hasil cek margin)
| Opsi | Harga efektif/liter | Laba/liter (normal Rp 35.000 →) | Margin | Status |
|---|---|---|---|---|
| Diskon 15% | Rp 72.300 | Rp 22.300 | 30,8% | ✅ AMAN |
| **Bundling 2 liter = Rp 155.000** | Rp 77.500 | **Rp 27.500** | 35,5% | ✅ AMAN, **disarankan** |

**Rekomendasi: "Paket Gajian 2 liter Rp 155.000"** (klaim aman "hemat 8%", dari Rp 170.000). Laba per liter lebih tinggi daripada diskon 15%, dan pembeli membawa pulang 2 liter.
Diskon maksimal agar tidak rugi: **41,1%**. Ini batas bawah, bukan saran.

## 2. Linimasa (dari script)
| Hari | Tanggal | Fase | Kegiatan |
|---|---|---|---|
| H-14 | Minggu, 11 Oktober 2026 | Persiapan | Pastikan stok botol literan & bahan untuk ±2x penjualan biasa |
| H-7 | Minggu, 18 Oktober 2026 | Teaser | Status WA/IG: "Paket Gajian datang minggu depan" |
| H-3 | Kamis, 22 Oktober 2026 | Pengingat | Buka pre-order paket, broadcast ke pelanggan yang setuju |
| H-1 | Sabtu, 24 Oktober 2026 | Mulai | Promo dibuka pukul 17.00 |
| H | Minggu, 25 Oktober 2026 | Hari H gajian | Pantau stok & chat |
| H+1 | Senin, 26 Oktober 2026 | Lanjutan (sudah diumumkan) | Promo sampai Selasa pukul 21.00 |
| H+3 | Rabu, 28 Oktober 2026 | Kirim & layani | Selesaikan pesanan |
| H+7 | Minggu, 1 November 2026 | Evaluasi | Liter terjual vs minggu biasa |

## 3. S&K (siap tempel)
Paket Gajian 2 liter Kopi Susu Rp 155.000 (harga normal Rp 85.000/liter), berlaku Sabtu, 24 Oktober 2026 pukul 17.00 s.d. Selasa, 27 Oktober 2026 pukul 21.00 WIB atau selama stok promo (… paket) tersedia. Varian boleh dicampur. Tidak dapat digabung dengan promo lain. Ongkir ditanggung pembeli.

**Asumsi:** jualan langsung via WA/IG, sehingga potongan platform 0%. Kalau jualan di GoFood/GrabFood/Shopee, kirimkan persen potongannya (lihat di aplikasi merchant/Seller Center) dan aku hitung ulang, karena komisi bisa membuat hasilnya jauh berbeda. Penjualan normal belum diketahui, jadi target unit belum bisa dibandingkan. Diskon 15% perlu penjualan 1,57x lipat agar laba sama.

## Catatan penguji
- Angka dicek manual: 85.000 × 0,85 = 72.250 → dibulatkan ke atas Rp 72.300 → laba 22.300 ✓; bundling 155.000 − 100.000 = 55.000 → 27.500/liter ✓; impas 50.000 → 1 − 50/85 = 41,18% → 41,1% ✓.
- Default + asumsi disebut sesuai SKILL.md. Permintaan malas tetap menghasilkan rencana utuh.
- Kekurangan script: saat gajian terdekat tinggal 2 hari, script tetap memilihnya dan menandai H-14/H-7/H-3 "(sudah lewat)". Catatan "fase yang sudah lewat **dipadatkan**" tidak benar-benar dilakukan script (lihat HASIL-UJI). Agent perlu memakai `--dari`.
