# 03 — Take home pay dengan lembur hari libur

**Skenario:** S3 — pertanyaan normal: berapa potongan BPJS, pajak, dan gaji bersih, dengan lembur hari libur panjang.

**Input pengguna (persis):**
> Karyawan pabrik saya Agus, K/2, gaji pokok 7 juta tanpa tunjangan. Bulan ini lembur di hari Minggu 8 jam, terus pas tanggal merah 10 jam. JKK kami 0,89%. Potongan BPJS sama pajaknya berapa, terus gaji bersihnya berapa?

**Perintah:** `python3 scripts/payroll.py --periode 2026-09 --nama "Contoh Agus" --ptkp K/2 --gaji-pokok 7jt --lembur-hari-libur 8+10 --jkk 0,89 --out payroll-2026-09`

**Output:**

**Rekap payroll September 2026 — -** (1 karyawan)

| Nama | Total pendapatan | Potongan | PPh 21 | Take home pay | Biaya perusahaan |
|---|---:|---:|---:|---:|---:|
| Contoh Agus | Rp 8.578.035 | Rp 369.413 | Rp 89.413 | Rp 8.208.622 | Rp 9.340.335 |
| **Total** | **Rp 8.578.035** | | | **Rp 8.208.622** | **Rp 9.340.335** |

- Setor BPJS Kesehatan (4% + 1%): Rp 350.000
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 692.300
- Setor PPh 21 (tanpa DTP): Rp 89.413
- Batas upah JP dipakai: Rp 11.086.300 · JKK default 0,89% · UMK: tidak diisi (cek UMK dilewati)

File: payroll-2026-09/slip-gaji-2026-09.md, payroll-2026-09/slip-gaji-2026-09.html, payroll-2026-09/rekap-payroll-2026-09.csv

⚠️ Peringatan:
- UMK tidak diisi, jadi cek upah minimum dan batas bawah iuran BPJS Kesehatan dilewati.

Pembulatan: iuran BPJS & lembur ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax/aplikasi BPJS; bila berbeda, ikuti sistem resmi).

_Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Perpres 64/2020 (BPJS Kesehatan), PP 44/2015 & PP 45/2015 & PP 46/2015 (BPJS Ketenagakerjaan), PP 35/2021 (lembur), PP 58/2023 & PMK 168/2023 (PPh 21 TER), PMK 105/2025 (DTP), berlaku per 23 September 2026. Untuk kasus khusus hubungi BPJS, Disnaker, Kring Pajak 1500200, atau konsultan._

**Isi slip:**

# SLIP GAJI — (nama perusahaan)
**Periode:** September 2026  
**Nama:** Contoh Agus  
**Status PTKP:** K/2

| Pendapatan | Jumlah |
|---|---:|
| Gaji pokok | Rp 7.000.000 |
| Lembur | Rp 1.578.035 |
| **Total pendapatan** | **Rp 8.578.035** |

| Potongan | Jumlah |
|---|---:|
| BPJS Kesehatan 1% | Rp 70.000 |
| BPJS TK - JHT 2% | Rp 140.000 |
| BPJS TK - JP 1% | Rp 70.000 |
| PPh 21 | Rp 89.413 |
| **Total potongan** | **Rp 369.413** |

### TAKE HOME PAY: Rp 8.208.622

_Ditanggung perusahaan (tidak memotong gaji): BPJS Kesehatan 4% Rp 280.000, JHT 3,7% Rp 259.000, JKK 0,89% Rp 62.300, JKM 0,3% Rp 21.000, JP 2% Rp 140.000._
_PPh 21: TER kategori B 1% × penghasilan bruto pajak Rp 8.941.335 (termasuk premi JKK, JKM, BPJS Kesehatan perusahaan)._
_Lembur: upah sejam = 1/173 × Rp 7.000.000 = Rp 40.462,43._

Penjelasan lembur: upah sejam = Rp 7.000.000 ÷ 173 = Rp 40.462,43. Minggu 8 jam = 8 × 2 = 16 jam setara; tanggal merah 10 jam = 8 × 2 + 1 × 3 + 1 × 4 = 23 jam setara (pola 5 hari kerja, PP 35/2021 Pasal 31 ayat 3). Total 39 × Rp 40.462,43 = **Rp 1.578.035**.

Ingat: lembur di hari kerja dibatasi 4 jam/hari & 18 jam/minggu; lembur di hari libur tidak masuk batas itu, tapi maksimal 12 jam (pola 5 hari).

**Catatan penguji:**
- Diverifikasi independen: lembur Rp 1.578.035, bruto pajak Rp 8.941.335 → TER B 1% = Rp 89.413, THP Rp 8.208.622. Cocok.
- Tabel pengali hari libur sesuai teks PP 35/2021 Pasal 31 ayat (3) yang penguji baca sendiri (jam 1–8 2×, jam 9 3×, jam 10–12 4×).
- Kurang (ringan): ringkasan rekap tidak menampilkan rincian jam setara; agent perlu menjelaskannya sendiri (sudah dilakukan).
