# 02 — Permintaan singkat, satu karyawan

**Skenario:** S2 — permintaan malas; periode, JKK, dan UMK tidak disebut.

**Input pengguna (persis):**
> bikinin dong slip gaji rina, gaji 6jt, tk0

**Langkah agent:** pengguna ingin cepat → pakai default dan sebutkan asumsi (periode = bulan berjalan September 2026, JKK 0,24%, tanpa cek UMK).
Perintah: `python3 scripts/payroll.py --periode 2026-09 --nama "Contoh Rina" --ptkp TK/0 --gaji-pokok 6jt --out payroll-2026-09`

**Output:**

**Rekap payroll September 2026 — -** (1 karyawan)

| Nama | Total pendapatan | Potongan | PPh 21 | Take home pay | Biaya perusahaan |
|---|---:|---:|---:|---:|---:|
| Contoh Rina | Rp 6.000.000 | Rp 287.043 | Rp 47.043 | Rp 5.712.957 | Rp 6.614.400 |
| **Total** | **Rp 6.000.000** | | | **Rp 5.712.957** | **Rp 6.614.400** |

- Setor BPJS Kesehatan (4% + 1%): Rp 300.000
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 554.400
- Setor PPh 21 (tanpa DTP): Rp 47.043
- Batas upah JP dipakai: Rp 11.086.300 · JKK default 0,24% · UMK: tidak diisi (cek UMK dilewati)

File: payroll-2026-09/slip-gaji-2026-09.md, payroll-2026-09/slip-gaji-2026-09.html, payroll-2026-09/rekap-payroll-2026-09.csv

⚠️ Peringatan:
- Tarif JKK belum diisi: dipakai 0,24% (risiko sangat rendah, mis. kantor). Ganti dengan tarif di sertifikat/penetapan BPJS Ketenagakerjaan perusahaan Anda.
- UMK tidak diisi, jadi cek upah minimum dan batas bawah iuran BPJS Kesehatan dilewati.

Pembulatan: iuran BPJS & lembur ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax/aplikasi BPJS; bila berbeda, ikuti sistem resmi).

_Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Perpres 64/2020 (BPJS Kesehatan), PP 44/2015 & PP 45/2015 & PP 46/2015 (BPJS Ketenagakerjaan), PP 35/2021 (lembur), PP 58/2023 & PMK 168/2023 (PPh 21 TER), PMK 105/2025 (DTP), berlaku per 23 September 2026. Untuk kasus khusus hubungi BPJS, Disnaker, Kring Pajak 1500200, atau konsultan._

Asumsi yang saya pakai: periode September 2026; gaji 6 jt = gaji pokok tanpa tunjangan; JKK 0,24% (kantor/risiko sangat rendah); UMK tidak dicek. Kalau ada tunjangan, lembur, atau tarif JKK lain, kabari — saya hitung ulang.

**Catatan penguji:**
- Verifikasi manual: bruto pajak = 6.000.000 + JKK 14.400 + JKM 18.000 + BPJS Kes 240.000 = 6.272.400 → TER A 0,75% = Rp 47.043; THP = 6.000.000 − 60.000 − 120.000 − 60.000 − 47.043 = **Rp 5.712.957**; biaya perusahaan Rp 6.614.400. Cocok.
- Default + asumsi disebut dengan jelas, sesuai prinsip "instan".
