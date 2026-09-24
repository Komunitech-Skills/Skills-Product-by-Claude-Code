# 02 — Pabrik kecil pola 5 hari: shift malam 22.00–06.00, lembur libur resmi, pekerja upah harian

**Skenario:** normal (kompleks). Pabrik fiktif, 3 karyawan pola 5 hari (istirahat Sabtu–Minggu). Hadi shift MALAM 22.00–06.00 (lewat tengah malam), Wati & Slamet shift PAGI 07.00–16.00. Slamet dibayar **harian** Rp 180.000. Laporan dari software mesin berformat **per hari** (Scan Masuk/Scan Pulang, pemisah `;`, tanggal `dd-mm-yyyy`). Termasuk: shift 31/08 yang pulang 01/09 08.04 (lewat pergantian bulan), lembur di 17 Agustus (Senin, libur resmi), lembur Sabtu 10 jam, lembur hari kerja 4,5 jam (> 4 jam/hari) dan 5 × 4 jam dalam satu minggu (20 jam > 18 jam/minggu), lembur pecahan `2:15`, dan satu hari lupa tap pulang.

Cuplikan `laporan-agustus.csv` (63 baris data, fiktif):
```
No. ID;Nama;Tanggal;Jam Kerja;Scan Masuk;Scan Pulang
11;Hadi;03-08-2026;22.00-06.00;21.54;06.01
12;Wati;04-08-2026;07.00-16.00;07.02;20.35
13;Slamet;08-08-2026;07.00-16.00;06.55;18.05
11;Hadi;17-08-2026;22.00-06.00;21.58;07.03
13;Slamet;17-08-2026;07.00-16.00;07.00;10.05
13;Slamet;19-08-2026;07.00-16.00;07.03;
11;Hadi;31-08-2026;22.00-06.00;21.57;08.04
```

## Input pengguna (persis)

> bikinin rekap absen pabrik agustus dong, file terlampir. Hadi shift malem jam 10 malam - 6 pagi gaji 4,5jt + tunj tetap 400rb. Wati QC jam 7-4 gaji 4,2jt. Slamet harian 180rb/hari jam 7-4. Semua libur sabtu minggu. SPL lembur terlampir juga (lembur.csv). Nanti mau dibikin slip gajinya.

`lembur.csv` (dari pengguna):
```
tanggal;kode;jam;disetujui_oleh
17/08/2026;P01;8;Bu Lina (SPL-017)
31/08/2026;P01;2;Bu Lina (SPL-031)
04/08/2026;P02;4,5;Bu Lina (SPL-004)
10/08/2026;P02;4;Bu Lina (SPL-010)
11/08/2026;P02;4;Bu Lina (SPL-011)
12/08/2026;P02;4;Bu Lina (SPL-012)
13/08/2026;P02;4;Bu Lina (SPL-013)
14/08/2026;P02;4;Bu Lina (SPL-014)
26/08/2026;P02;2:15;Bu Lina (SPL-026)
08/08/2026;P03;10;Bu Lina (SPL-008)
17/08/2026;P03;3;Bu Lina (SPL-017b)
```

## Output (mengikuti SKILL.md)

Satu pertanyaan dulu (data wajib kurang): "Toleransi terlambat berapa menit (default 0)? Apakah 17 Agustus satu-satunya tanggal merah di bulan Agustus untuk pabrik Anda?" → pengguna: "0 aja, iya cuma 17an."

Perintah (masing-masing dipratinjau, disimpan setelah "ya"): `init`, `shift tambah --kode MALAM --masuk 22.00 --pulang 06.00 --istirahat 60` (pratinjau: "MALAM 22.00-06.00 (lewat tengah malam) ... Jam kerja efektif per hari: 7 jam"), `shift tambah --kode PAGI --masuk 07.00 --pulang 16.00`, 3 × `karyawan tambah` (Slamet `--upah-harian 180rb`), `libur tambah --tanggal 17/08/2026 --nama "Hari Kemerdekaan RI"`, `impor-absen laporan-agustus.csv`, `lembur --file lembur.csv`.

Pratinjau impor:
```
Impor absen dari laporan-agustus.csv (format per hari: masuk/pulang)
Pemetaan kolom: id <- 'No. ID', nama <- 'Nama', tanggal <- 'Tanggal', masuk <- 'Scan Masuk', pulang <- 'Scan Pulang'
Contoh cara baca: Hadi: Senin 3 Agustus 2026 jam 21.54 (masuk) | Hadi: Selasa 4 Agustus 2026 jam 06.01 (pulang) | Wati: Senin 3 Agustus 2026 jam 06.55 (masuk)
Tap baru: 125 | sudah ada sebelumnya (dilewati): 0 | di luar rentang: 0
Rentang tanggal: 03/08/2026 s.d. 31/08/2026
Per karyawan: Hadi 42, Slamet 43, Wati 40
```

Pratinjau lembur (dipotong): Hadi 17/08 8 jam "hari istirahat/libur, pola 5 hari kerja (Pasal 31 ayat (3))" = 16 jam setara ≈ Rp 453.179; Wati 04/08 4,5 jam = 8,5 jam setara, "Catatan: Melebihi batas 4 jam/hari di hari kerja (Pasal 26 ayat (1))"; Wati 26/08 `2:15` = 2,25 jam = 4 jam setara; Slamet 08/08 10 jam = 8×2 + 1×3 + 1×4 = 23 jam setara ≈ Rp 502.543 (upah sejam Rp 21.850 = 180.000 × 21 ÷ 173).

Rekap (teks script):
```
REKAP ABSENSI AGUSTUS 2026
Periode 01/08/2026-31/08/2026 | toleransi terlambat 0 menit
Libur resmi: 17/08/2026 Hari Kemerdekaan RI

1. Hadi (P01) - Operator
   Hadir 20 dari 20 hari kerja | masuk di hari libur 1
   Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 152 jam 46 menit
   Lembur disetujui: hari kerja 2 jam, hari libur 8 jam (setara 19,5 jam) -> Rp 552.312

2. Wati (P02) - QC
   Hadir 20 dari 20 hari kerja
   Terlambat 8x (16 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 188 jam 27 menit
   Lembur disetujui: hari kerja 26,75 jam, hari libur 0 jam (setara 50 jam) -> Rp 1.213.873

3. Slamet (P03) - Buruh harian
   Hadir 20 dari 20 hari kerja | masuk di hari libur 2
   Terlambat 8x (24 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 165 jam 59 menit (+1 hari data tidak lengkap, belum dihitung)
   Lembur disetujui: hari kerja 0 jam, hari libur 13 jam (setara 29 jam) -> Rp 633.642

Total upah lembur: Rp 2.399.827

PERLU DICEK (3):
- Wati 04/08/2026: lembur hari kerja 4,5 jam melebihi batas 4 jam/hari (PP 35/2021 Pasal 26 ayat (1)); tetap dihitung sesuai jam yang disetujui
- Wati: lembur hari kerja minggu ke-33/2026 = 20 jam, melebihi 18 jam/minggu (PP 35/2021 Pasal 26 ayat (1))
- Slamet 19/08/2026: hanya ada jam masuk (07.03); jam pulang tidak tercatat

Upah lembur: PP 35/2021 Pasal 31-32 (upah sejam = 1/173 x upah sebulan), hanya dari lembur yang disetujui, dibulatkan ke rupiah terdekat. Alat bantu hitung, bukan nasihat hukum; kasus khusus tanyakan ke Disnaker/konsultan.

File untuk slip-gaji-bpjs: gaji-agustus.csv
Catatan: Jalankan slip-gaji-bpjs dengan --hari-kerja 5.
Catatan: slip-gaji-bpjs menghitung ulang rupiah lembur dari gaji pokok + tunjangan tetap di file gajinya; bandingkan dengan angka rekap ini.
Catatan: Kolom ptkp dan gaji wajib diisi dulu sebelum dipakai slip-gaji-bpjs (...)
```

Tambahan agent: dasar upah Slamet = Rp 180.000 × 21 = Rp 3.780.000 (Pasal 33 ayat (1) huruf b); Wati melewati batas Pasal 26 — upah tetap dibayar sesuai jam yang disetujui, tetapi jadwal lembur minggu itu melanggar batas dan perlu dibenahi; Slamet 19/08 pulang jam berapa? Lembur ≥ 4 jam (Hadi 17/08, Wati, Slamet 08/08) → wajib makan-minum ≥ 1.400 kkal (Pasal 29).

`gaji-agustus.csv` untuk slip-gaji-bpjs:
```
nama;jabatan;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;lembur_hari_kerja;lembur_hari_libur;kode_absensi;hari_hadir;hari_alpa;terlambat_menit
Hadi;Operator;;;;;2;8;P01;20;0;0
Wati;QC;;;;;4,5+4+4+4+4+4+2,25;;P02;20;0;16
Slamet;Buruh harian;;;;;;10+3;P03;20;0;24
```

**Uji kompatibilitas:** penguji mengisi ptkp & gaji (Slamet gaji_pokok = 3.780.000) lalu menjalankan `skills/slip-gaji-bpjs/scripts/payroll.py --hari-kerja 5`: file diterima (kolom tambahan diabaikan), lembur di slip **sama persis**: Hadi 552.312, Wati 1.213.873, Slamet 633.642.

**Cek pergantian bulan:** `rekap --bulan 2026-09 --karyawan Hadi` tidak menghitung ulang tap 01/09 06.xx/08.04 (milik shift 31/08) — tidak dobel.

## Catatan penguji
- **Angka diverifikasi independen** (`/tmp/uji-absensi-lokal/b/verif_b.py`): hadir, masuk di hari libur, terlambat kali/menit, jam kerja shift malam lintas tengah malam, hari tidak lengkap, jam setara dan rupiah. Hitung manual: Hadi (16 + 3,5) × 4.900.000 ÷ 173 = 552.312,14 → 552.312; Wati (8,5 + 5×7,5 + 4) = 50 × 4.200.000 ÷ 173 = 1.213.872,83 → 1.213.873; Slamet (23 + 6) = 29 × 3.780.000 ÷ 173 = 633.641,62 → 633.642. Semua cocok.
- Bagus: shift malam & pergantian bulan benar; upah harian × 21 (Pasal 33); peringatan Pasal 26 harian & mingguan; format per-hari terbaca otomatis; jam pecahan `2:15` diterima.
- Kurang: (1) `--csv-gaji` mengosongkan gaji_pokok padahal gaji sudah ada di database — pengguna harus mengetik ulang, dan untuk pekerja **harian** tidak ada catatan khusus bahwa gaji_pokok di slip harus diisi 180.000 × 21 = 3.780.000 agar rupiah lembur sama (kalau diisi upah riil 20 hari = 3.600.000, slip-gaji menghitung lembur lebih kecil); (2) peringatan 18 jam/minggu hanya dihitung di dalam periode rekap — minggu yang terbelah akhir bulan tidak terdeteksi (lihat HASIL-UJI); (3) pratinjau `lembur --file` tidak memperingatkan total mingguan (baru muncul saat rekap).
