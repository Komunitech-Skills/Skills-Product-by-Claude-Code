# Uji 02 — Gaji September + BPJS + PPh 21 (2 karyawan warung)

Tanggal uji: 2026-10-01 · OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill usaha-offline. Teks balasan disalin utuh, tanpa suntingan.

## Pesan member
> Tolong hitungin gaji september 2 karyawan warung makan saya di Solo. Andi: gapok 2,8jt + uang makan tetap 300rb, status nikah anak 1, lembur 3 hari masing2 2 jam (hari kerja biasa). Sari: gapok 2,65jt, belum nikah, ga lembur. Dua2nya ikut BPJS Kesehatan & BPJS TK (JHT, JKK, JKM, JP). Yg ditransfer ke masing2 berapa, saya nyetor BPJS berapa total, PPh 21 nya ada ga?

## Giliran 1

Alat — SEBELUM: tidak ada. SESUDAH: baca `gaji-umkm/SKILL.md`, `references/perintah.md`, `references/dasar-aturan.md`, jalankan `scripts/gaji.py info` (cek database), lalu bertanya balik.

### SEBELUM (tanpa skill)
> Halo! Ini perhitungan gaji September 2026 untuk Andi & Sari, pakai aturan lembur PP 35/2021, iuran BPJS standar, dan PPh 21 metode TER (PMK 168/2023). Asumsi: JKK pakai tarif risiko sangat rendah (0,24%) — umum untuk usaha kuliner kecil, tapi cek lagi kalau kamu tahu kelas risiko resmi warungmu di BPJS TK.
>
> ## 1. Andi (K/1 – nikah, anak 1)
>
> **Komponen gaji**
> - Gaji pokok: Rp 2.800.000
> - Uang makan tetap: Rp 300.000
> - Upah sebulan (dasar lembur & BPJS) = Rp 3.100.000
> - Upah per jam = 3.100.000 ÷ 173 = Rp 17.919
> - Lembur (hari kerja biasa, 2 jam × 3 hari): jam ke-1 = 1,5×, jam ke-2 = 2× → 3,5 × 17.919 × 3 hari ≈ **Rp 188.150**
> - **Gaji bruto total: Rp 3.288.150**
>
> **BPJS Kesehatan** (dasar Rp 3.100.000)
> - Perusahaan 4%: Rp 124.000
> - Andi 1%: Rp 31.000
>
> **BPJS Ketenagakerjaan** (dasar Rp 3.100.000)
> | Program | Perusahaan | Karyawan |
> |---|---|---|
> | JHT (3,7% / 2%) | 114.700 | 62.000 |
> | JKK (0,24%) | 7.440 | - |
> | JKM (0,3%) | 9.300 | - |
> | JP (2% / 1%) | 62.000 | 31.000 |
> | **Total** | **193.440** | **93.000** |
>
> **Potongan Andi:** BPJS Kesehatan 31.000 + BPJS TK 93.000 = **Rp 124.000**
>
> **PPh 21 (TER kategori B, status K/1):** penghasilan bruto 3.288.150 masih di bawah batas 0% TER B (~6,2 juta/bulan) → **PPh 21 = Rp 0**
>
> ➡️ **Transfer ke Andi: Rp 3.288.150 − 124.000 = Rp 3.164.150**
>
> ---
>
> ## 2. Sari (TK/0 – belum nikah, tanpa lembur)
>
> **Gaji bruto = Rp 2.650.000**
>
> **BPJS Kesehatan** (dasar 2.650.000)
> - Perusahaan 4%: Rp 106.000
> - Sari 1%: Rp 26.500
>
> **BPJS Ketenagakerjaan**
> | Program | Perusahaan | Karyawan |
> |---|---|---|
> | JHT | 98.050 | 53.000 |
> | JKK | 6.360 | - |
> | JKM | 7.950 | - |
> | JP | 53.000 | 26.500 |
> | **Total** | **165.360** | **79.500** |
>
> **Potongan Sari:** 26.500 + 79.500 = **Rp 106.000**
>
> **PPh 21 (TER kategori A, status TK/0):** bruto 2.650.000 jauh di bawah batas 0% TER A (~5,4 juta/bulan) → **PPh 21 = Rp 0**
>
> ➡️ **Transfer ke Sari: Rp 2.650.000 − 106.000 = Rp 2.544.000**
>
> ---
>
> ## 3. Rekap
>
> | | Andi | Sari | Total |
> |---|---|---|---|
> | Gaji bruto | 3.288.150 | 2.650.000 | 5.938.150 |
> | Potongan karyawan | 124.000 | 106.000 | 230.000 |
> | **Transfer ke rekening** | **3.164.150** | **2.544.000** | **5.708.150** |
> | Iuran BPJS perusahaan | 317.440 | 271.360 | 588.800 |
> | Iuran BPJS karyawan (dipotong) | 124.000 | 106.000 | 230.000 |
> | **Total setor BPJS (ke BPJS, semua program)** | **441.440** | **377.360** | **Rp 818.800** |
>
> **Ringkasan:**
> - Transfer ke Andi: **Rp 3.164.150**
> - Transfer ke Sari: **Rp 2.544.000**
> - Total disetor ke BPJS (Kesehatan + TK, gabungan perusahaan & karyawan): **Rp 818.800**
> - PPh 21: **tidak ada (Rp 0)** untuk keduanya — gaji mereka masih di bawah ambang 0% tabel TER.
>
> Catatan: kedua gaji pokok (2,8jt & 2,65jt) sudah di atas kisaran UMK Solo, jadi aman dari sisi batas upah minimum. Kalau JKK warungmu ternyata terdaftar di kelas risiko lain (bukan 0,24%), total iuran BPJS TK bisa sedikit berubah — tinggal kabari aku kelas risikonya kalau mau dikoreksi.

### SESUDAH (paket skill)
> Sebelum saya hitung, saya perlu 2 info wajib yang belum ada (field wajib di aplikasi gaji):
>
> 1. **Tanggal masuk kerja** Andi dan Sari (boleh perkiraan, misalnya "sudah kerja dari 2022" cukup tanggal 1 di bulan itu). Ini memengaruhi perhitungan PPh 21 kalau mereka baru masuk tahun ini.
> 2. Apakah warung sudah punya **database gaji** sebelumnya di aplikasi ini? (Sepertinya belum — saya cek, belum ada file database, jadi ini pemakaian pertama kali, akan saya buatkan.)
>
> Boleh dijawab singkat, misalnya: "Andi masuk dari 2020, Sari dari 2023" — saya lanjutkan hitungannya begitu dapat tanggal itu.

## Giliran 2 (hanya SESUDAH yang bertanya balik; jawaban member: "Andi masuk 1 Maret 2022, Sari 1 Januari 2024. Belum pernah pakai, bikinin aja.")

SEBELUM sudah menjawab tuntas di giliran 1 (diulang di bawah agar berdampingan). SESUDAH menjalankan `gaji.py init` (pratinjau lalu `--ya`), `karyawan tambah` ×2 (pratinjau lalu `--ya`), `isi --lembur-hari-kerja 2+2+2`, `hitung --bulan 2026-09`. **Skill benar-benar terpakai.**

### SEBELUM (tanpa skill)
> Halo! Ini perhitungan gaji September 2026 untuk Andi & Sari, pakai aturan lembur PP 35/2021, iuran BPJS standar, dan PPh 21 metode TER (PMK 168/2023). Asumsi: JKK pakai tarif risiko sangat rendah (0,24%) — umum untuk usaha kuliner kecil, tapi cek lagi kalau kamu tahu kelas risiko resmi warungmu di BPJS TK.
>
> ## 1. Andi (K/1 – nikah, anak 1)
>
> **Komponen gaji**
> - Gaji pokok: Rp 2.800.000
> - Uang makan tetap: Rp 300.000
> - Upah sebulan (dasar lembur & BPJS) = Rp 3.100.000
> - Upah per jam = 3.100.000 ÷ 173 = Rp 17.919
> - Lembur (hari kerja biasa, 2 jam × 3 hari): jam ke-1 = 1,5×, jam ke-2 = 2× → 3,5 × 17.919 × 3 hari ≈ **Rp 188.150**
> - **Gaji bruto total: Rp 3.288.150**
>
> **BPJS Kesehatan** (dasar Rp 3.100.000)
> - Perusahaan 4%: Rp 124.000
> - Andi 1%: Rp 31.000
>
> **BPJS Ketenagakerjaan** (dasar Rp 3.100.000)
> | Program | Perusahaan | Karyawan |
> |---|---|---|
> | JHT (3,7% / 2%) | 114.700 | 62.000 |
> | JKK (0,24%) | 7.440 | - |
> | JKM (0,3%) | 9.300 | - |
> | JP (2% / 1%) | 62.000 | 31.000 |
> | **Total** | **193.440** | **93.000** |
>
> **Potongan Andi:** BPJS Kesehatan 31.000 + BPJS TK 93.000 = **Rp 124.000**
>
> **PPh 21 (TER kategori B, status K/1):** penghasilan bruto 3.288.150 masih di bawah batas 0% TER B (~6,2 juta/bulan) → **PPh 21 = Rp 0**
>
> ➡️ **Transfer ke Andi: Rp 3.288.150 − 124.000 = Rp 3.164.150**
>
> ---
>
> ## 2. Sari (TK/0 – belum nikah, tanpa lembur)
>
> **Gaji bruto = Rp 2.650.000**
>
> **BPJS Kesehatan** (dasar 2.650.000)
> - Perusahaan 4%: Rp 106.000
> - Sari 1%: Rp 26.500
>
> **BPJS Ketenagakerjaan**
> | Program | Perusahaan | Karyawan |
> |---|---|---|
> | JHT | 98.050 | 53.000 |
> | JKK | 6.360 | - |
> | JKM | 7.950 | - |
> | JP | 53.000 | 26.500 |
> | **Total** | **165.360** | **79.500** |
>
> **Potongan Sari:** 26.500 + 79.500 = **Rp 106.000**
>
> **PPh 21 (TER kategori A, status TK/0):** bruto 2.650.000 jauh di bawah batas 0% TER A (~5,4 juta/bulan) → **PPh 21 = Rp 0**
>
> ➡️ **Transfer ke Sari: Rp 2.650.000 − 106.000 = Rp 2.544.000**
>
> ---
>
> ## 3. Rekap
>
> | | Andi | Sari | Total |
> |---|---|---|---|
> | Gaji bruto | 3.288.150 | 2.650.000 | 5.938.150 |
> | Potongan karyawan | 124.000 | 106.000 | 230.000 |
> | **Transfer ke rekening** | **3.164.150** | **2.544.000** | **5.708.150** |
> | Iuran BPJS perusahaan | 317.440 | 271.360 | 588.800 |
> | Iuran BPJS karyawan (dipotong) | 124.000 | 106.000 | 230.000 |
> | **Total setor BPJS (ke BPJS, semua program)** | **441.440** | **377.360** | **Rp 818.800** |
>
> **Ringkasan:**
> - Transfer ke Andi: **Rp 3.164.150**
> - Transfer ke Sari: **Rp 2.544.000**
> - Total disetor ke BPJS (Kesehatan + TK, gabungan perusahaan & karyawan): **Rp 818.800**
> - PPh 21: **tidak ada (Rp 0)** untuk keduanya — gaji mereka masih di bawah ambang 0% tabel TER.
>
> Catatan: kedua gaji pokok (2,8jt & 2,65jt) sudah di atas kisaran UMK Solo, jadi aman dari sisi batas upah minimum. Kalau JKK warungmu ternyata terdaftar di kelas risiko lain (bukan 0,24%), total iuran BPJS TK bisa sedikit berubah — tinggal kabari aku kelas risikonya kalau mau dikoreksi.

### SESUDAH (paket skill)
> Sudah saya buatkan database gaji Warung Makan dan hitung periode September 2026 untuk Andi & Sari (masih **draf**, belum dikunci). Ini hasilnya:
>
> | Kode | Nama | Pendapatan | Potongan | PPh 21 | Gaji bersih | Biaya perusahaan |
> |---|---|---:|---:|---:|---:|---:|
> | K001 | Andi | Rp 3.288.150 | Rp 124.000 | Rp 0 | **Rp 3.164.150** | Rp 3.605.590 |
> | K002 | Sari | Rp 2.650.000 | Rp 106.000 | Rp 0 | **Rp 2.544.000** | Rp 2.921.360 |
> | | **Total** | **Rp 5.938.150** | **Rp 230.000** | **Rp 0** | **Rp 5.708.150** | **Rp 6.526.950** |
>
> Jawaban pertanyaan Anda:
> - **Transfer ke Andi: Rp 3.164.150** (termasuk lembur 3×2 jam = Rp 188.150, dipotong BPJS Kes 1% + JHT 2% + JP 1%)
> - **Transfer ke Sari: Rp 2.544.000** (gaji pokok saja, dipotong BPJS Kes 1% + JHT 2% + JP 1%, tanpa lembur)
> - **Total setoran BPJS Anda: Rp 818.800** = BPJS Kesehatan Rp 287.500 (4% perusahaan + 1% karyawan) + BPJS Ketenagakerjaan Rp 531.300 (JHT, JKK, JKM, JP gabungan perusahaan+karyawan)
> - **PPh 21: Rp 0** untuk keduanya. Gaji mereka masih di bawah ambang TER bulanan (Andi kategori B, Sari kategori A) jadi tarifnya 0% bulan ini.
>
> Perlu diperhatikan (dari script, mohon dikonfirmasi):
> - Tarif JKK belum saya atur, jadi dipakai default 0,24% (risiko sangat rendah). Kalau sertifikat BPJS TK warung Anda beda (0,54/0,89/1,27/1,74%), kasih tahu saya biar dikoreksi.
> - UMK Solo belum saya masukkan, jadi belum dicek apakah gaji pokok di atas UMK dan batas bawah dasar BPJS Kesehatan. Kalau Anda tahu UMK Kota Solo 2026, kasih angkanya.
>
> _Alat bantu hitung, bukan nasihat hukum/pajak final. Dasar: Perpres 64/2020 (BPJS Kes), PP 44/45/46/2015 (BPJS TK), PP 35/2021 (lembur), PP 58/2023 & PMK 168/2023 (PPh 21 TER), berlaku per 23 Sep 2026. Pembulatan belum dicocokkan dengan Coretax/aplikasi BPJS._
>
> Kalau sudah oke dan tarif JKK/UMK tidak perlu diubah, bilang saja "kunci" — saya **final**-kan periode ini lalu buatkan slip gaji per orang dan file transfer CSV-nya.

## Verifikasi independen
Dihitung ulang dengan Python: upah dasar = gaji pokok + tunjangan tetap; upah/jam = upah/173; lembur hari kerja jam-1 1,5×, jam-2 2× (PP 35/2021) → 3,5 × 3 hari; BPJS Kes 4%/1% (Perpres 64/2020); JHT 3,7%/2%; JKK 0,24% (asumsi risiko sangat rendah); JKM 0,3%; JP 2%/1% (di bawah batas upah JP); PPh 21 TER PMK 168/2023 (TER A 0% s.d. Rp5,4 jt; TER B 0% s.d. Rp6,2 jt).

| | Andi | Sari |
|---|---:|---:|
| Lembur | 188.150 | 0 |
| Bruto | 3.288.150 | 2.650.000 |
| Potongan pekerja | 124.000 | 106.000 |
| **Transfer** | **3.164.150** | **2.544.000** |
| Iuran perusahaan | 317.440 | 271.360 |
| Total setor BPJS | 441.440 | 377.360 → **818.800** |
| PPh 21 | 0 | 0 |

- **Kedua sisi 100% cocok** dengan hitungan independen.
- SEBELUM menyatakan "gaji pokok sudah di atas kisaran UMK Solo" tanpa menyebut angka/sumber (klaim tak terverifikasi; UMK Surakarta 2025 = Rp2.416.560, angka 2026 tidak dicek di uji ini).
- SESUDAH jujur bahwa UMK belum dimasukkan dan meminta angkanya; menyebut dasar aturan + catatan pembulatan belum dicocokkan Coretax/aplikasi BPJS; menawarkan kunci periode → slip + CSV transfer.
- SESUDAH butuh 1 giliran tambahan (tanggal masuk) sebelum menghitung — bagi awam ini friksi; tanggal masuk hanya memengaruhi karyawan yang masuk tahun berjalan.

## Nilai
| | Ketepatan | Siap pakai | Aturan ID | Keamanan | Kejelasan | **Skor** |
|---|---|---|---|---|---|---|
| SEBELUM | 9 | 8 | 8 | 9 | 9 | **8** |
| SESUDAH | 9 | 9 | 9 | 9 | 8 | **8** |

Alasan: angka sama-sama benar. SESUDAH unggul di hal yang tidak terlihat dalam satu jawaban: data tersimpan lokal untuk bulan depan, slip & file transfer, dasar aturan, tidak mengklaim UMK tanpa data. SEBELUM unggul di kecepatan (1 giliran) dan rincian per program BPJS yang lebih mudah dibaca. Seri.
