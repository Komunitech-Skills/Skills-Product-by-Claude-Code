# 05 - Script: data skenario 1 & 2, data rusak, kasus batas, verifikasi angka independen

- **Tanggal:** 2026-10-14 · **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Regresi:** `python3 tests/uji_regresi.py` → **47 uji OK** (2,3 detik).
- **Cara verifikasi:** semua angka dihitung ulang dengan `data/verifikasi-penguji.py` (tulisan penguji, `decimal.Decimal`, tidak memakai kode skill): biaya sampai di tempat, per unit, PPN 11% (= 12% × 11/12) dibulatkan ke bawah sekali, pemecahan harga termasuk PPN, selisih %, skor tertimbang, sensitivitas 2×, bagi 70/30.

## A. Data skenario 1 (tepung 600 kg, tenggat 5 hari) - `data/s1-tepung-penguji.json`
Pemetaan penguji: Sentosa `harga 118rb, isi_kemasan 10, tingkat "51: 5%"` ("di atas 50 dus" = mulai 51 dus), ongkir 100rb, 2-3 hari, COD; Mitra PKP belum PPN, MOQ 300, ongkir 150rb ditagih di invoice, 3-4 hari, tempo 30; Berkah non-PKP franco, 5-7 hari, transfer penuh di muka.

| Angka | Script | Hitung ulang penguji | Cocok |
|---|---|---|---|
| Sentosa: 60 dus × 118.000 = 7.080.000; diskon 5% 354.000; + ongkir 100.000 | Rp6.826.000 (Rp11.377/kg) | 6.826.000 (11.376,67) | ✔ |
| Mitra: DPP 6.720.000 + 150.000 = 6.870.000; PPN ⌊11%⌋ | PPN Rp755.700 → Rp7.625.700 (Rp12.710/kg) | 755.700 (12%×11/12 juga 755.700) → 7.625.700 | ✔ |
| Berkah: 600 × 11.900 | Rp7.140.000 | 7.140.000 | ✔ |
| Selisih vs termurah | +Rp799.700 (+11,7%); +Rp314.000 (+4,6%) | 799.700 (11,7%); 314.000 (4,6%) | ✔ |
| Skor (40/20/15/15/10) | 86,5 / 85,8 / 63,0 (Berkah telat → lead 0) | 86,50 / 85,81 / 62,99 | ✔ |
| Potensi PPN Sentosa (status PKP tidak disebut) | Rp750.860 | 750.860 | ✔ |
| Jumlah 2× (1.200 kg) | 13.552.000 / 15.084.900 / 14.280.000 | sama | ✔ |
| Bagi 70/30 (Sentosa 420 kg tanpa diskon + Mitra 180 kg → beli 300 MOQ) | Rp8.952.100, tambahan Rp2.126.100 (+31,1%) | 5.056.000 + 3.896.100 = 8.952.100; +31,1% | ✔ |
| Sentosa telat 7 hari → 10 hari > 5 | rekomendasi BERUBAH ke Mitra | benar (Berkah juga telat) | ✔ |

Bila ongkir Mitra **tidak** ikut DPP (ditagih sebagai penggantian biaya ekspedisi), PPN = 739.200 dan total 7.609.200 (beda Rp16.500). Ini yang dipakai model dasar di sisi SEBELUM; lihat PERLU REVIEW di HASIL-UJI.

## B. Data skenario 2 (box kue 1.000 pcs, tenggat 7 hari) - `data/penawaran-box-kue.csv`

| Pemasok | Script | Penguji | Catatan |
|---|---|---|---|
| Percetakan Box Mandiri (PKP, sudah termasuk PPN, tingkat 1.000 tepat di batas) | 1.000 × 2.100 + 120.000 = Rp2.220.000; DPP 2.000.000, PPN 220.000, sisa 0; **telat** (10 > 7) | sama | ✔ tingkat tepat di batas berlaku |
| Toko Kemasan Kilat (Rp135.000/pak isi 50, MOQ 5 pak, ongkir 15rb/pak) | 1.000 × 2.700 + 20 pak × 15.000 = Rp3.000.000 | 3.000.000 | ✔ per pak → per pcs benar |
| UD Karton Jaya (loco, "3-5 hari kerja") | Rp2.400.000 + `[isian: biaya ambil]`; 5 hari kerja → 7 hari kalender (masuk tenggat) | sama | ✔ |
| CV Pack Nusantara (PKP belum PPN, franco) | 2.300.000 + PPN 253.000 = Rp2.553.000 | sama | ✔ |
| Skor bobot default | Pack 76,8 · Kilat 76,1 · Karton 72,0 · Mandiri 68,3 → rekomendasi Pack ("hampir seri" 0,7) | 76,78 / 76,10 / 72,00 / 68,25 | ✔ |
| Skor bobot "cepat" (lead 40, biaya 30, termin 10, kualitas 15, MOQ 5) | Kilat 81,2 · Pack 63,1 · Karton 59,1 · Mandiri 51,2 → rekomendasi Kilat | 81,20 / 63,09 / 59,08 / 51,17 | ✔ |

## C. Data rusak & kasus batas

| Uji | Hasil script | Penilaian |
|---|---|---|
| Kolom kosong (hanya nama + harga) | dihitung; ongkir, status PKP (potensi PPN Rp396.000), lead time, termin masuk `DATA BELUM ADA` | ✔ |
| Harga kosong pada 1 baris | baris itu `DILEWATI` + alasan; lainnya tetap dihitung | ✔ |
| MOQ 500 untuk kebutuhan 300 | beli 500, kelebihan 200 kg, modal tertahan Rp2.120.000, per kg kebutuhan Rp17.667 | ✔ (10.600 × 200) |
| Tingkat tepat di batas (300 → Rp10.000) | 300 kg pakai harga tingkat | ✔ |
| 1 di bawah batas (299) | "beli 300 (+1) LEBIH MURAH total (-Rp289.000)" | ✔ 3.289.000 − 3.000.000 |
| Diskon % per dus di batas (Sentosa 500 / 505 / 510 kg) | 500 kg = 50 dus tanpa diskon Rp6.000.000 + saran 510 kg lebih murah (Rp5.817.100); 505 → naik ke 510 (kelipatan dus) | ✔ |
| Minimal belanja Rp1 jt + diskon 5% + MOQ "2 lusin" | beli 43 pcs (1.075.000 − 53.750 ≥ 1 jt), total Rp1.041.250 | ✔ |
| PKP "sudah termasuk PPN" 77 × 12.345 = 950.565 | DPP 856.365, PPN 94.200, sisa 0 (DPP terbesar) | ✔ (856.366 akan melebihi) |
| PKP vs non-PKP, pembeli PKP | PPN dikreditkan; biaya bersih 856.365 / 872.000 / 885.500; +1,8% / +3,4% | ✔ |
| JSON rusak, qty 0, data kosong, bobot "murah=50" | kode keluar 2 + `error` + `saran` bahasa awam | ✔ |
| Semua baris rusak (harga negatif, DP 150%, MOQ "5 dus" tanpa isi) | kode 2, ketiga alasan disebut | ✔ |

## D. Cacat script yang ditemukan (angka tetap benar)
1. **"belum" dibaca "tidak diketahui".** Kolom `harga termasuk ppn` = `belum` (persis seperti di `templates/contoh-penawaran.csv` dan contoh JSON di `templates/format-penawaran.md`) masuk daftar KOSONG, sehingga muncul `DATA BELUM ADA: harga sudah/belum termasuk PPN` padahal pemasok sudah menulis "belum termasuk PPN". Angka tidak berubah (default = belum termasuk), tetapi agent bisa mengajukan pertanyaan yang tidak perlu ke pengguna/pemasok. Terjadi juga pada CSV skenario 2 (CV Pack Nusantara). Teks `belum termasuk` terbaca benar.
2. **Bagi pesanan lebih murah ditulis "tambahan -Rp45.900 (+-1,8%)"** (skenario 2, bobot default; bobot cepat: "-Rp180.000 (+-6,0%)"). Angkanya benar, tetapi tanda "+-" membingungkan; seharusnya "lebih hemat Rp45.900 (1,8%)". Pada kasus ini cadangan (UD Karton Jaya) loco dan biaya ambilnya belum dihitung, jadi "lebih hemat" pun belum pasti.
3. Pemasok yang status PKP-nya tidak disebut tetap diberi "potensi PPN". Untuk barang kebutuhan pokok yang dibebaskan PPN (mis. gula konsumsi, beras, telur) baris ini bisa menyesatkan; lihat PERLU REVIEW.
