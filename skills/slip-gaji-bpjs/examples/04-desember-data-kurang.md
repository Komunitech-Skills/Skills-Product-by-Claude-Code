# 04 — Input tidak lengkap: slip Desember

**Skenario:** S4 — slip bulan Desember tanpa data Januari–November (wajib untuk hitung ulang PPh 21).

**Input pengguna (persis):**
> Buat slip gaji Desember 2026 untuk Andi, K/0, gaji pokok 10 juta.

**Percobaan pertama agent:** `python3 scripts/payroll.py --periode 2026-12 --nama "Contoh Andi" --ptkp K/0 --gaji-pokok 10jt --out payroll-2026-12`
```
ERROR: data berikut harus diperbaiki dulu (tidak ada file yang dibuat):
- Contoh Andi: bulan ini Masa Pajak Terakhir (Desember). PPh 21 wajib dihitung ulang setahun, jadi isi kolom bruto_sd_bulan_lalu, pph21_sd_bulan_lalu (total bruto pajak & PPh 21 Januari s.d. bulan lalu).
```
(tidak ada file dibuat — aman)

**Output ke pengguna (bertanya sekali):**
> Bulan Desember itu "bulan hitung ulang" PPh 21 setahun, jadi saya butuh data Januari–November dulu. Mohon kirim:
> 1. Total penghasilan bruto pajak Andi Januari–November 2026 (gaji + tunjangan + lembur + THR/bonus + premi JKK/JKM/BPJS Kesehatan perusahaan). Bisa juga kirim rekap payroll tiap bulan, nanti saya jumlahkan.
> 2. Total PPh 21 yang sudah dipotong Januari–November.
> 3. Total iuran JHT 2% + JP 1% yang dipotong dari gaji Andi Januari–November.
> 4. Andi bekerja penuh sejak Januari? Kalau masuk di tengah tahun, bulan apa?
> 5. Tarif JKK perusahaan (kalau tidak tahu, saya pakai 0,24%).

**Setelah pengguna menjawab** ("bruto Jan–Nov 114.994.000, PPh sudah dipotong 2.874.850, iuran 3.300.000, kerja penuh, JKK 0,24%"):
`python3 scripts/payroll.py --periode 2026-12 --nama "Contoh Andi" --ptkp K/0 --gaji-pokok 10jt --jkk 0,24 --bruto-sd-bulan-lalu 114.994.000 --pph21-sd-bulan-lalu 2.874.850 --iuran-sd-bulan-lalu 3.300.000 --out payroll-2026-12`

**Rekap payroll Desember 2026 — -** (1 karyawan)

| Nama | Total pendapatan | Potongan | PPh 21 | Take home pay | Biaya perusahaan |
|---|---:|---:|---:|---:|---:|
| Contoh Andi | Rp 10.007.450 | Rp 400.000 | -Rp 7.450 | Rp 9.607.450 | Rp 11.024.000 |
| **Total** | **Rp 10.007.450** | | | **Rp 9.607.450** | **Rp 11.024.000** |

- Setor BPJS Kesehatan (4% + 1%): Rp 500.000
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 924.000
- Setor PPh 21 (tanpa DTP): Rp 0
- Batas upah JP dipakai: Rp 11.086.300 · JKK default 0,24% · UMK: tidak diisi (cek UMK dilewati)

File: payroll-2026-12/slip-gaji-2026-12.md, payroll-2026-12/slip-gaji-2026-12.html, payroll-2026-12/rekap-payroll-2026-12.csv

⚠️ Peringatan:
- Contoh Andi: PPh 21 lebih potong Rp 7.450 dikembalikan ke karyawan di slip ini.
- UMK tidak diisi, jadi cek upah minimum dan batas bawah iuran BPJS Kesehatan dilewati.

Pembulatan: iuran BPJS & lembur ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax/aplikasi BPJS; bila berbeda, ikuti sistem resmi).

_Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Perpres 64/2020 (BPJS Kesehatan), PP 44/2015 & PP 45/2015 & PP 46/2015 (BPJS Ketenagakerjaan), PP 35/2021 (lembur), PP 58/2023 & PMK 168/2023 (PPh 21 TER), PMK 105/2025 (DTP), berlaku per 23 September 2026. Untuk kasus khusus hubungi BPJS, Disnaker, Kring Pajak 1500200, atau konsultan._

**Isi slip:**

# SLIP GAJI — (nama perusahaan)
**Periode:** Desember 2026  
**Nama:** Contoh Andi  
**Status PTKP:** K/0

| Pendapatan | Jumlah |
|---|---:|
| Gaji pokok | Rp 10.000.000 |
| Pengembalian kelebihan PPh 21 | Rp 7.450 |
| **Total pendapatan** | **Rp 10.007.450** |

| Potongan | Jumlah |
|---|---:|
| BPJS Kesehatan 1% | Rp 100.000 |
| BPJS TK - JHT 2% | Rp 200.000 |
| BPJS TK - JP 1% | Rp 100.000 |
| **Total potongan** | **Rp 400.000** |

### TAKE HOME PAY: Rp 9.607.450

_Ditanggung perusahaan (tidak memotong gaji): BPJS Kesehatan 4% Rp 400.000, JHT 3,7% Rp 370.000, JKK 0,24% Rp 24.000, JKM 0,3% Rp 30.000, JP 2% Rp 200.000._
_PPh 21: dihitung ulang setahun (Masa Pajak Terakhir); PPh setahun Rp 2.867.400 − sudah dipotong Rp 2.874.850._

**Catatan penguji:**
- Diverifikasi independen: setahun bruto Rp 125.448.000, biaya jabatan Rp 6 jt, iuran Rp 3,6 jt, PKP Rp 57.348.000, PPh setahun Rp 2.867.400 − Rp 2.874.850 = **lebih potong Rp 7.450** dikembalikan di slip. Cocok.
- Script menolak dengan pesan jelas dan tidak membuat file setengah jadi. Bagus.
- Kurang (sedang): bila `jumlah_bulan_kerja` tidak diisi, script memakai nomor bulan (12) sebagai jumlah bulan kerja (baris `n = int(angka(r.get("jumlah_bulan_kerja"), ..., Decimal(bulan)))` di `hitung_karyawan`). Untuk karyawan yang baru masuk di tengah tahun, biaya jabatan maksimal jadi terlalu besar (mis. Rp 6 jt padahal seharusnya Rp 500 rb × bulan kerja) → PPh Desember terlalu kecil, tanpa peringatan. Pertanyaan nomor 4 di atas menutup celah ini, tetapi SKILL.md tidak mewajibkannya.
