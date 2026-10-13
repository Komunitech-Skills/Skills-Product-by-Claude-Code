# 03 — Normal + PKP/PPN: nugget beku, naik harga termasuk PPN + paket

> Uji independen Tahap 6 (2026-09-29). Penguji: agent terpisah dari pembuat. Output agent dihasilkan oleh sesi `claude -p` baru (Claude Code, simulasi agent) dengan skill terpasang di folder sementara `.claude/skills/` (tanpa folder `examples/`). Nama usaha fiktif.

## Input pengguna

> Usaha frozen food kami (CV Dapur Nugget, sudah PKP) jual nugget ayam 500 gram. HPP naik dari 28 ribu jadi 31 ribu per pack. Harga tayang sekarang Rp54.900 sudah termasuk PPN, laku sekitar 800 pack sebulan. Biaya tetap 12 juta sebulan. Kami mau naikkan harga tayang ke Rp59.900 termasuk PPN. Tolong hitung DPP dan PPN-nya, margin kami sebelum dan sesudah naik, dan apakah masih aman kalau penjualan turun. Kami juga mau bikin paket 3 pack buat reseller kafe seharga Rp150.000 termasuk PPN, dus tambahan 2.500 per paket.

## Output agent (dengan skill, apa adanya)

# Harga Nugget 500 g: naik ke Rp59.900 dan paket reseller 3 pack

**Ringkasan**
- Naik ke **Rp59.900 (termasuk PPN)** aman dan perlu. Margin pulih ke 42,55% setelah HPP naik.
- **Paket 3 pack Rp150.000 tidak disarankan.** Marginnya hanya 29,33%, dan paket ini menurunkan rata-rata margin usaha.
- Paket lebih aman di kisaran **Rp164.900**, dengan margin sekitar 35,7%.

**Asumsi**
- Semua margin dihitung dari DPP, bukan dari harga yang sudah termasuk PPN.
- HPP Rp28.000 dan Rp31.000 saya anggap tanpa PPN. PPN masukan dari bahan atau kemasan dikreditkan terpisah.
- Tambahan Rp2.500 per paket saya anggap biaya kemasan atau tambahan tanpa PPN.
- Volume tetap 800 pack per bulan pada semua skenario, kecuali di bagian simulasi.

## 1. DPP dan PPN
Tarif efektif 11% (12% × DPP nilai lain 11/12).

| Harga tayang | DPP | PPN |
|---|---|---|
| Rp54.900 (sekarang) | Rp49.460 | Rp5.440 |
| **Rp59.900 (baru)** | **Rp53.964** | **Rp5.936** |
| Paket 3 pack Rp150.000 | Rp135.136 | Rp14.864 |

## 2. Margin sebelum dan sesudah naik

| Kondisi | DPP | HPP | Laba/pack | Margin | Markup |
|---|---|---|---|---|---|
| Sebelum HPP naik (Rp54.900) | Rp49.460 | Rp28.000 | Rp21.460 | 43,39% | 76,64% |
| HPP naik, harga belum naik | Rp49.460 | Rp31.000 | Rp18.460 | 37,32% | 59,55% |
| **HPP naik, harga Rp59.900** | Rp53.964 | Rp31.000 | **Rp22.964** | **42,55%** | 74,08% |

Kenaikan HPP Rp3.000 memangkas margin hampir 6 poin. Harga baru mengembalikannya ke level semula. Laba per pack bahkan naik Rp1.504 dibanding sebelum HPP naik.

## 3. Aman kalau penjualan turun?
Biaya tetap Rp12 juta per bulan, penjualan 800 pack.

| Skenario | BEP | Laba/bulan | Penjualan boleh turun |
|---|---|---|---|
| Sebelum HPP naik | 560 pack | Rp5.168.000 | 30% |
| HPP naik, harga lama | 651 pack | Rp2.768.000 | 18,63% |
| **Harga Rp59.900** | **523 pack** | **Rp6.371.200** | **34,63%** |

- Dengan harga baru, penjualan boleh turun sampai 523 pack (sekitar 35%) sebelum rugi. Ini lebih aman daripada bertahan di harga lama.
- **Volume impas kenaikan** (angka pasti): kalau penjualan tetap di atas **644 pack** (turun kurang dari 19,5%), laba tetap lebih besar dari laba sekarang Rp2,77 juta.

**ESTIMASI** laba per bulan setelah naik 9,11%. Ini perkiraan, bukan kepastian:

| Kepekaan pembeli | Perkiraan volume | Perkiraan laba |
|---|---|---|
| Tidak peka (-0,5) | 764 pack | Rp5,54 juta |
| Sedang (-1) | 727 pack | Rp4,69 juta |
| Sangat peka (-2) | 654 pack | Rp3,02 juta |

Bahkan kalau pembeli sangat peka, laba masih di atas kondisi sekarang. Kenaikan di bawah 10% ini tergolong ringan.

## 4. Paket 3 pack Rp150.000 (termasuk PPN)
- Harga satuan 3 × Rp59.900 = Rp179.700, jadi pembeli hemat Rp26.756 (DPP) atau sekitar 16,5%.
- HPP paket Rp95.500 (Rp93.000 isi + Rp2.500 tambahan).
- **Laba per paket Rp39.636, margin 29,33%.** Kalau dijual satuan, labanya Rp68.892 (margin 42,55%).
- Paket harus menambah transaksi sekitar 74% agar laba kotor setara jual satuan.
- Di bawah margin minimum 40% untuk makanan (default skill, bisa diubah). Harga paket terendah untuk margin 40% adalah Rp176.675 (DPP Rp159.167 + PPN Rp17.508), yang hampir sama dengan harga satuan 3 pack. Jadi diskon 16% ini terlalu dalam.

**Alternatif** (dihitung script `bundel --ppn termasuk`):

| Harga paket | Margin | Hemat vs satuan |
|---|---|---|
| Rp150.000 | 29,33% | Rp29.700 (16,53%) |
| **Rp164.900** | **35,72%** | Rp14.800 (8,24%) |
| Rp169.900 | 37,61% | Rp9.800 (5,45%) |

Karena pembeli reseller kafe membeli rutin dan dalam jumlah banyak, margin 35% sudah wajar. Rp164.900 tetap terasa lebih murah dari satuan dan tidak menggerus laba.

## Langkah minggu ini
1. Umumkan harga baru Rp59.900 satu sampai dua minggu sebelum berlaku, dengan alasan jujur: bahan baku naik.
2. Pastikan faktur dan struk menampilkan DPP dan PPN. Karena PKP, tulis harga "termasuk PPN".
3. Ganti paket kafe ke Rp164.900, atau Rp169.900 kalau ingin margin lebih tebal.
4. Kalau tetap ingin Rp150.000, batasi untuk pembeli rutin dengan minimal pesanan bulanan tertentu, dan sadari margin paketnya 29%.
5. Catat penjualan dua minggu pertama. Kalau turun di bawah 644 pack per bulan (sekitar 150 per minggu), tinjau lagi.

**Teks pengumuman (siap tempel):**
> Halo pelanggan setia Dapur Nugget! Mulai [tanggal], harga Nugget Ayam 500 g menjadi Rp59.900 (sudah termasuk PPN) karena harga bahan baku naik. Kualitas tetap sama. Beli dengan harga lama masih bisa sampai [tanggal]. Terima kasih!

Angka dihitung dengan script dari data yang Anda berikan. Keputusan harga tetap di tangan Anda. Pembulatan PPN belum dicocokkan dengan Coretax, jadi ikuti Coretax kalau berbeda. Untuk detail pajak, konsultasikan ke konsultan pajak atau pajak.go.id.

## Verifikasi penguji

Standar pedoman kurasi Komunitech: PPN dari DPP persis dibulatkan ke bawah sekali; harga termasuk PPN → DPP = rupiah bulat terbesar dengan DPP + PPN ≤ harga. Penguji mencari DPP secara brute force (Fraction), dibandingkan dengan script pada 9.045 kasus (termasuk mewah 12%): **0 selisih**.
- 54.900 → DPP **49.460**, PPN 5.440 (49.461 → total 54.901 > harga) ✔.
- 59.900 → DPP **53.964**, PPN 5.936 ✔. 150.000 → DPP **135.136**, PPN 14.864 ✔.
- Margin: 21.460/49.460 = 43,39% ✔; 18.460/49.460 = 37,32% ✔; 22.964/53.964 = 42,55% ✔; markup 76,64% / 59,55% / 74,08% ✔.
- BEP: 12 jt ÷ 21.460 → 560; ÷ 18.460 → 651; ÷ 22.964 → 523 ✔. Laba 5.168.000 / 2.768.000 / 6.371.200 ✔. Batas aman 30% / 18,63% / 34,63% ✔.
- Volume impas 800 × 18.460 ÷ 22.964 = 643,1 → **644** ✔. ESTIMASI Δ 9,11%: 764 / 727 / 654; laba Rp5.544.496 / 4.694.828 / 3.018.456 ✔.
- Paket (script `bundel` dijalankan penguji): laba 39.636, margin 29,33%, hemat 26.756 (16,53%), faktor +73,81%, lantai 40% DPP 159.167 ✔.

**Catatan penguji:** angka dihitung ulang skrip 2026-10-13 (`bundel --item "Nugget 500 g:59900:31000:3" --harga-bundel <harga> --biaya-tambahan 2500 --kategori pangan --ppn termasuk` dan `margin --hpp 95500 --margin 40 --ppn termasuk`); angka paket alternatif dan lantai paket di output di atas sudah memakai hasil skrip:
- Lantai paket margin 40%: **Rp176.675** (DPP 159.167 + PPN 17.508).
- Rp164.900 → DPP 148.559, margin **35,72%**, hemat Rp14.800 (**8,24%**).
- Rp169.900 → DPP 153.063 (sisa pembulatan Rp1), margin **37,61%**, hemat Rp9.800 (5,45%).
- Ketiga harga alternatif (Rp150.000, Rp164.900, Rp169.900) berstatus **DI BAWAH MIN** terhadap margin minimum 40% (default skill kategori pangan, bisa diubah). Agent menyarankan Rp164.900 tanpa menandainya di bawah minimum — catatan kualitas, bukan salah hitung.

**Nilai: 6,5/10** — PPN, margin inti, BEP, estimasi semua benar dan asumsi PKP jelas; minus: harga paket yang disarankan di bawah margin minimum tanpa tanda.
