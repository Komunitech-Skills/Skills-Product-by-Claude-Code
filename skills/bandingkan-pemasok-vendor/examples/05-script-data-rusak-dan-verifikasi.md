# 05 - Script 1.0.1: data skenario, data rusak, kasus batas, verifikasi angka independen

- **Tanggal:** 2026-10-14 (putaran 2) · **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Audit keamanan 1.0.1:** tidak ada impor baru (argparse, csv, io, json, re, sys, decimal); hanya membaca `--file`/`--data`/stdin; tanpa jaringan, tanpa menulis file, tanpa eval/exec/subprocess.
- **Regresi:** `python3 tests/uji_regresi.py` → **66 uji OK** (3,6 detik).
- **Cara verifikasi:** `data/verifikasi-penguji-1.0.1.py` (+ `data/verifikasi-penguji.py` putaran 1), ditulis penguji dengan `decimal.Decimal` tanpa memakai kode skill.

## A. Skenario 1 (tepung 600 kg, tenggat 5 hari) - `data/s1-tepung-penguji.json`
| Angka | Script 1.0.1 | Hitung ulang penguji | Cocok |
|---|---|---|---|
| Total Sentosa / Mitra / Berkah | 6.826.000 / 7.625.700 / 7.140.000 | sama | ✔ |
| Kolom selisih | "termurah sementara" / "lebih mahal Rp799.700 (11,7%)" / "lebih mahal Rp314.000 (4,6%)" | 799.700 (11,7%); 314.000 (4,6%) | ✔ |
| Skor | 86,5 / 85,8 / 63,0 | 86,50 / 85,81 / 62,99 | ✔ |
| "Sentosa lebih MURAH Rp314.000 daripada CV Berkah" | arah & nilai | benar | ✔ |
| "Bila Sentosa telat 7 hari → pindah ke PT Mitra, yang lebih MAHAL Rp799.700 (11,7%) daripada Sentosa" | arah & nilai | benar (Berkah juga telat) | ✔ |
| Bagi 70/30 | Rp8.952.100, "lebih MAHAL Rp2.126.100 (31,1%)" | 5.056.000 + 3.896.100; 31,1% | ✔ |
| **Bila Sentosa PKP & belum PPN** | total 7.576.860 (naik 750.860); "Sentosa lebih MURAH Rp48.840 daripada PT Mitra; rekomendasi berubah menjadi PT Mitra (unggul di termin)" | 6.826.000 + ⌊11% × 6.826.000⌋ = 7.576.860; 7.625.700 − 7.576.860 = 48.840; skor Mitra 87,45 vs Sentosa 84,19 (CV Berkah jadi termurah keseluruhan tetapi telat); Mitra unggul hanya di termin (100 vs 50) | ✔ benar dan masuk akal (tempo 30 hari atas ±Rp7,6 jt > Rp48.840) |
| Asumsi pajak PPN atas ongkir Mitra | Rp16.500 | ⌊11% × 6.870.000⌋ − ⌊11% × 6.720.000⌋ = 755.700 − 739.200 | ✔ |

## B. Skenario 2 (box kue 1.000 pcs, tenggat 7 hari, bobot cepat 20/50/10/10/10) - `data/penawaran-box-kue.csv`
| Angka | Script | Penguji | Cocok |
|---|---|---|---|
| Total Kilat / Pack / Karton / Mandiri | 3.000.000 / 2.553.000 / 2.400.000 / 2.220.000 (telat, DPP 2.000.000) | sama | ✔ |
| Skor | 85,8 / 57,9 / 54,3 / 42,2 | 85,80 / 57,89 / 54,33 / 42,17 | ✔ |
| "Kilat lebih MAHAL Rp600.000 (25,0%) daripada Karton Jaya" | | 600.000 ÷ 2.400.000 = 25,0% | ✔ |
| Batas biaya ambil Karton Jaya vs CV Pack Nusantara | Rp153.000 | 2.553.000 − 2.400.000 | ✔ |
| Bagi 70/30 | Rp2.820.000, "lebih MURAH Rp180.000" (tanda "+-" sudah hilang) | 2.100.000 + 720.000 | ✔ |
| CSV `belum` (CV Pack Nusantara) | PKP belum termasuk PPN; **tidak** masuk `DATA BELUM ADA` | | ✔ (cacat 1.0.0 diperbaiki) |

## C. Skenario 1V (data baru: margarin 180 kg, tenggat 6 hari) - `data/s1v-margarin-penguji.json`
| Angka | Script | Penguji | Cocok |
|---|---|---|---|
| Lancar Jaya: 12 karton × 380.000 + 12 × 8.000, PPN termasuk | 4.656.000; DPP 4.194.595, PPN 461.405, sisa 0 | sama (DPP 4.194.596 akan melebihi) | ✔ |
| Sumber Rejeki: 180 × 24.900, ongkir belum diketahui | 4.482.000 "termurah sementara" | 4.482.000 | ✔ |
| Margarindo: MOQ 200 × 23.800 + PPN | 5.283.600; sisa 20 kg, modal tertahan 528.360; "4-5 hari kerja" = 7 hari → telat | 4.760.000 + 523.600; 26.418 × 20 | ✔ |
| Selisih & skor | +174.000 (3,9%), +801.600 (17,9%); 86,5 / 81,8 / 64,2 | 3,9% / 17,9%; 86,50 / 81,84 / 64,16 | ✔ |
| **Batas ongkir Sumber Rejeki** | maks. Rp174.000 untuk 180 kg (Rp966,67/kg) | 4.656.000 − 4.482.000 (non-PKP, ongkir tanpa PPN) | ✔ |
| 2x / bagi 70/30 | 8.964.000; 7.067.400, lebih MAHAL 2.585.400 (57,7%) | Lancar Jaya 54 kg → wajib 10 karton (150 kg, tanpa harga tingkat) | ✔ |

## D. Skenario 3 & 4
- Gula, `--qty 1 --barang "gula pasir"`: Makmur Rp15.500 "termurah sementara", Sinar lebih mahal Rp700 (4,5%), batas ongkir Rp700 per kg, tanpa potensi PPN + catatan PP 49/2022. ✔ (10 kg → Rp7.000; 50 kg → Rp35.000)
- Kertas, `--pilihan "Sinar ATK"`: peringkat 1 Toko Kertas Abadi (85,8). "CV Sinar ATK ... peringkat 2: lebih MURAH Rp50.000 daripada Toko Kertas Abadi; skor 83,3 vs 85,8; unggul di biaya, termin; kalah di lead time". Bagi 70/30 Rp2.762.500 = lebih MAHAL Rp37.500 daripada semua dari Abadi. ✔ (penguji: 85,77 / 83,33; 1.907.500 + 855.000)

## E. Data rusak & kasus batas (1.0.1)
| Uji | Hasil | Penilaian |
|---|---|---|
| `templates/contoh-penawaran.csv` (kolom `ppn` = `belum`) | `DATA BELUM ADA` hanya untuk Toko Grosir Abadi (ongkir, status PKP); CV Kemasan Prima tidak lagi ditanya | ✔ |
| Kolom `ppn` tidak dikenal ("mungkin") | baris `DILEWATI` + saran kamus (termasuk/belum/non-pkp/bebas/?) | ✔ |
| Kolom kosong, MOQ 500 untuk 300, tingkat tepat di batas, harga kosong | sama dengan putaran 1 (3.000.000 / 3.600.000 / 5.300.000; D dilewati); "walau tanpa ongkir, A Kosong lebih MAHAL Rp600.000" | ✔ |
| PKP termasuk vs belum vs non-PKP, pembeli PKP | 856.365 / 872.000 / 885.500; asumsi PPN atas ongkir Rp2.750 + syarat pengkreditan ditulis | ✔ |
| `--bebas-ppn ya` | PPN tidak ditambahkan untuk pemasok `belum` | ✔ |
| JSON rusak, qty 0, semua baris rusak, bobot "murah=50" | kode 2 + `error` + `saran` | ✔ |

## F. Cacat script yang tersisa (1.0.1)
1. **Termin "DP 30% sisa 30 hari" / "DP 30% pelunasan 30 hari" (tanpa kata "tempo"/"setelah") dibaca diam-diam sebagai pelunasan saat barang tiba.** Tempo hilang tanpa peringatan dan tanpa catatan "termin tidak terbaca". Ini terjadi nyata di skenario 1V Telegram: skor Margarindo 58,9, seharusnya 64,2. Rupiah dan peringkat tidak berubah. Varian "sisa tempo 30 hari" dan "30 hari setelah barang diterima" terbaca benar.
2. Baris rincian menampilkan harga per kg yang sudah dibulatkan, sehingga perkaliannya tidak cocok. Contoh: "Beli 180 kg x Rp25.333 = Rp4.560.000", padahal 180 × 25.333 = 4.559.940. Subtotal benar (380.000/15 tidak dibulatkan dalam hitungan); hanya tampilannya yang membingungkan bila disalin.
3. Tanpa `--barang`, catatan umum PP 49/2022 ("beberapa bahan pokok dibebaskan PPN") muncul untuk barang yang jelas bukan bahan pokok (contoh: kertas/kolom kosong). Tidak salah, tetapi menambah kebisingan.
4. Untuk input per 1 satuan tanpa lead time (skenario 3), baris "jumlah 2x" dan "telat 7 hari" tidak bermakna.

## Riwayat: putaran 1 (1.0.0)
Regresi 47 uji OK; semua angka script 1.0.0 cocok 100%. Tiga cacat script, semuanya **sudah diperbaiki di 1.0.1**:
1. Nilai `belum` dibaca "tidak diketahui".
2. Bagi pesanan yang lebih murah ditulis "tambahan -Rp… (+-…%)".
3. Potensi PPN ditambahkan untuk bahan pokok yang dibebaskan PPN.
