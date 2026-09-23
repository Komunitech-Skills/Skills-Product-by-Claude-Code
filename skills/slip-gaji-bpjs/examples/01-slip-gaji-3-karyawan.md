# 01 — Slip gaji September untuk 3 karyawan

**Skenario:** S1 — permintaan normal: pemilik CV minta slip gaji & rekap payroll bulanan, ada lembur hari kerja dan hari Minggu.

**Input pengguna (persis):**
> Tolong buatkan slip gaji September 2026 buat 3 karyawan CV Contoh Maju Jaya. UMK kami 5.396.761, JKK 0,54%, kerja 5 hari seminggu.
> 1. Budi (K/1) Staf Gudang: gapok 5 jt, tunjangan tetap 500 rb, uang makan 600 rb, lembur Senin 2 jam, Rabu 3 jam, Minggu 8 jam, kasbon 100 rb.
> 2. Siti (TK/0) Admin: gapok 4,8 jt, tunjangan tetap 300 rb, uang makan 400 rb.
> 3. Dewi (K/2) Supervisor: gapok 9 jt, tunjangan tetap 1,5 jt, uang makan & transport 750 rb, lembur 1 jam dan 2 jam hari kerja, potongan koperasi 250 rb.

**Langkah agent:** menyusun `karyawan.csv` (nama diberi awalan "Contoh" karena fiktif):
```
nama;jabatan;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;lembur_hari_kerja;lembur_hari_libur;potongan_lain
Contoh Budi Santoso;Staf Gudang;K/1;5.000.000;500.000;600.000;2+3;8;100.000
Contoh Siti Aminah;Admin;TK/0;4.800.000;300.000;400.000;;;
Contoh Dewi Lestari;Supervisor;K/2;9.000.000;1.500.000;750.000;1+2;;250.000
```
Perintah: `python3 scripts/payroll.py --data karyawan.csv --periode 2026-09 --perusahaan "CV Contoh Maju Jaya" --umk "5.396.761" --jkk 0,54 --out payroll-2026-09`

**Output (rekap dari script):**

**Rekap payroll September 2026 — CV Contoh Maju Jaya** (3 karyawan)

| Nama | Total pendapatan | Potongan | PPh 21 | Take home pay | Biaya perusahaan |
|---|---:|---:|---:|---:|---:|
| Contoh Budi Santoso | Rp 6.894.798 | Rp 373.707 | Rp 53.707 | Rp 6.521.091 | Rp 7.474.498 |
| Contoh Siti Aminah | Rp 5.500.000 | Rp 235.761 | Rp 28.793 | Rp 5.264.239 | Rp 6.049.410 |
| Contoh Dewi Lestari | Rp 11.553.468 | Rp 1.031.850 | Rp 361.850 | Rp 10.521.618 | Rp 12.660.168 |
| **Total** | **Rp 23.948.266** | | | **Rp 22.306.948** | **Rp 26.184.076** |

- Setor BPJS Kesehatan (4% + 1%): Rp 1.069.838
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 2.012.940
- Setor PPh 21 (tanpa DTP): Rp 444.350
- Batas upah JP dipakai: Rp 11.086.300 · JKK default 0,54% · UMK: Rp 5.396.761

File: payroll-2026-09/slip-gaji-2026-09.md, payroll-2026-09/slip-gaji-2026-09.html, payroll-2026-09/rekap-payroll-2026-09.csv

⚠️ Peringatan:
- Contoh Siti Aminah: gaji pokok + tunjangan tetap Rp 5.100.000 di bawah UMK yang Anda isi (Rp 5.396.761). Pastikan tidak melanggar ketentuan upah minimum (usaha mikro/kecil punya aturan tersendiri).

Pembulatan: iuran BPJS & lembur ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax/aplikasi BPJS; bila berbeda, ikuti sistem resmi).

_Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Perpres 64/2020 (BPJS Kesehatan), PP 44/2015 & PP 45/2015 & PP 46/2015 (BPJS Ketenagakerjaan), PP 35/2021 (lembur), PP 58/2023 & PMK 168/2023 (PPh 21 TER), PMK 105/2025 (DTP), berlaku per 23 September 2026. Untuk kasus khusus hubungi BPJS, Disnaker, Kring Pajak 1500200, atau konsultan._

**Contoh isi slip (file `slip-gaji-2026-09.md`, slip pertama; file HTML siap cetak berisi slip yang sama, satu per halaman):**

# SLIP GAJI — CV Contoh Maju Jaya
**Periode:** September 2026  
**Nama:** Contoh Budi Santoso · Staf Gudang  
**Status PTKP:** K/1

| Pendapatan | Jumlah |
|---|---:|
| Gaji pokok | Rp 5.000.000 |
| Tunjangan tetap | Rp 500.000 |
| Tunjangan tidak tetap | Rp 600.000 |
| Lembur | Rp 794.798 |
| **Total pendapatan** | **Rp 6.894.798** |

| Potongan | Jumlah |
|---|---:|
| BPJS Kesehatan 1% | Rp 55.000 |
| BPJS TK - JHT 2% | Rp 110.000 |
| BPJS TK - JP 1% | Rp 55.000 |
| PPh 21 | Rp 53.707 |
| Potongan lain | Rp 100.000 |
| **Total potongan** | **Rp 373.707** |

### TAKE HOME PAY: Rp 6.521.091

_Ditanggung perusahaan (tidak memotong gaji): BPJS Kesehatan 4% Rp 220.000, JHT 3,7% Rp 203.500, JKK 0,54% Rp 29.700, JKM 0,3% Rp 16.500, JP 2% Rp 110.000._
_PPh 21: TER kategori B 0,75% × penghasilan bruto pajak Rp 7.160.998 (termasuk premi JKK, JKM, BPJS Kesehatan perusahaan)._
_Lembur: upah sejam = 1/173 × Rp 5.500.000 = Rp 31.791,91; 25 jam setara × upah sejam = Rp 794.798._

Asumsi: uang makan/transport dianggap tunjangan tidak tetap (tidak ikut dasar BPJS & lembur); pola 5 hari kerja; skema PPh 21 dipotong dari gaji (bukan ditanggung perusahaan); perusahaan bukan penerima PPh 21 DTP.

**Catatan penguji:**
- Semua angka diverifikasi dengan kalkulator payroll independen penguji (BPJS Kes 4%/1% dasar upah tetap min UMK maks Rp 12 jt; JHT 3,7%/2%; JKK tarif; JKM 0,3%; JP 2%/1% maks Rp 11.086.300; lembur 1/173 dengan pengali PP 35/2021 Pasal 31–32; TER dari tabel PDF): Budi THP Rp 6.521.091 & biaya Rp 7.474.498; Siti PPh Rp 28.793, THP Rp 5.264.239 (iuran BPJS Kes naik ke dasar UMK); Dewi lembur Rp 303.468, PPh Rp 361.850, THP Rp 10.521.618 — **cocok persis**.
- Peringatan UMK untuk Siti muncul dengan bahasa yang sopan. Tiga file (MD, HTML, CSV `;`) dibuat. Bagus.
