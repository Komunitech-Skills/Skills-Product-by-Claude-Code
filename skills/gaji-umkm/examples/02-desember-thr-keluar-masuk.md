# 02 — Normal: Oktober–Desember 2026 (karyawan keluar November, THR Natal, masuk Desember, hitung ulang setahun)

> Penguji independen Akun B, 26-09-2026, lanjutan database skenario 01. Nama FIKTIF. `claude-code (simulasi agent)`.

## Permintaan pemilik (diringkas)
1. "Saya baru pakai aplikasi ini September. Ini total Januari–Agustus tiap karyawan dari catatan lama." → `saldo-awal` ×10 (angka dihitung penguji dari aturan, JP Jan–Feb batas 10.547.400, Mar–Agu 11.086.300).
2. "Gaji Oktober seperti biasa, kunci." → `hitung` + `final --ya`.
3. "Dedi resign 20 November, gaji penuh." → `karyawan keluar --karyawan K04 --tanggal 2026-11-20` → pratinjau → `--ya` → `hitung --bulan 2026-11` → `final`.
4. "Mira masuk 10 Desember, dibayar Rp 4.258.065. Andi bonus akhir tahun 2 juta. THR Natal (25/12) untuk Citra, Gita, Kiki, Mira."
   → `thr --bulan 2026-12 --hari-raya 2026-12-25 --nama-hari-raya "Natal 2026" --karyawan K03 --karyawan K07 --karyawan K11 --karyawan K13`

## THR (pratinjau script, apa adanya)
```
THR Natal 2026 - hari raya 25/12/2026, batas bayar 18/12/2026, rencana bayar 18/12/2026 (masuk gaji Desember 2026):
- Citra Fiktif: Rp 13.000.000 (masa kerja ≥ 12 bulan → 1 × upah; masa kerja 107 bulan; dasar gaji pokok + tunjangan tetap)
- Gita Fiktif: Rp 7.300.000 (masa kerja ≥ 12 bulan → 1 × upah; masa kerja 52 bulan; dasar gaji pokok + tunjangan tetap)
- Kiki Fiktif: Rp 2.000.000 (3/12 × upah; masa kerja 3 bulan; dasar upah bersih/gaji pokok)
- Mira Fiktif: tidak berhak (Masa kerja kurang dari 1 bulan — belum wajib THR (Permenaker 6/2016 Pasal 2).)
Total THR: Rp 22.300.000
```
Cek penguji: Citra 02/01/2018→25/12/2026 = 107 bulan penuh ✓; Kiki 15/09→25/12 = 3 bln 10 hari → 3/12 × 8.000.000 = 2.000.000 ✓ (bulan tidak penuh diabaikan — cara yang umum, tetap sebutkan ke pemilik); Mira 15 hari → tidak wajib ✓; batas bayar H-7 = 18/12 ✓ (Permenaker 6/2016 Pasal 5 ayat 4).
Catatan kecil: frasa "dasar upah bersih/gaji pokok" pada Kiki kurang jelas bagi orang awam.

## Rekap Desember (keluaran script, dipotong)
```
REKAP GAJI DESEMBER 2026 - CV Uji Fiktif Makmur
Status: DRAF (belum final) | 11 karyawan

| Kode | Nama | Pendapatan | Potongan | PPh 21 | Gaji bersih | Biaya perusahaan |
|---|---|---:|---:|---:|---:|---:|
| K01 | Andi Fiktif | Rp 9.150.000 | Rp 559.568 | Rp 289.568 * | Rp 8.590.432 | Rp 9.861.450 |
| K02 | Budi Fiktif | Rp 4.000.000 | Rp 173.968 | Rp 0 * | Rp 3.826.032 | Rp 4.477.470 |
| K03 | Citra Fiktif | Rp 26.000.000 | Rp 2.556.115 | Rp 2.065.252 * | Rp 23.443.885 | Rp 27.291.926 |
| K05 | Eka Fiktif | Rp 15.338.820 | Rp 530.863 | -Rp 338.820 * | Rp 14.807.957 | Rp 16.382.726 |
| K06 | Fajar Fiktif | Rp 5.500.000 | Rp 165.000 | Rp 0 * | Rp 5.335.000 | Rp 5.988.950 |
| K07 | Gita Fiktif | Rp 14.600.000 | Rp 569.470 | Rp 496.470 * | Rp 14.030.530 | Rp 14.892.000 |
| K08 | Hadi Fiktif | Rp 22.000.000 | Rp 1.014.411 | Rp 343.548 * | Rp 20.985.589 | Rp 23.700.526 |
| K09 | Indah Fiktif | Rp 5.400.000 | Rp 216.000 | Rp 0 * | Rp 5.184.000 | Rp 5.969.160 |
| K10 | Joko Fiktif | Rp 3.800.000 | Rp 0 | Rp 0 * | Rp 3.800.000 | Rp 3.800.000 |
| K11 | Kiki Fiktif | Rp 10.251.616 | Rp 320.000 | -Rp 251.616 * | Rp 9.931.616 | Rp 10.843.200 |
| K13 | Mira Fiktif (baru) | Rp 4.258.065 | Rp 181.710 | Rp 0 * | Rp 4.076.355 | Rp 4.752.412 |
| | **Total** | **Rp 120.298.501** | **Rp 6.287.105** | **Rp 2.604.402** | **Rp 114.011.396** | **Rp 127.959.820** |
* PPh 21 dihitung ulang setahun (Masa Pajak Terakhir: Desember/bulan keluar).

Yang harus dibayar/disetor:
- Transfer gaji bersih ke karyawan: Rp 114.011.396
- Setor BPJS Kesehatan (4% perusahaan + 1% karyawan): Rp 3.987.176
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 7.356.846
- Setor PPh 21: Rp 3.194.838
- Kelebihan PPh 21 dikembalikan ke karyawan (sudah di gaji bersih): Rp 590.436
- Total biaya gaji perusahaan: Rp 127.959.820

Perlu diperhatikan:
```

## Verifikasi independen (Decimal) — Masa Pajak Terakhir
Rumus penguji: bruto setahun (saldo awal + Sep + Okt + Nov + Des, termasuk THR/bonus & premi JKK/JKM/Kes perusahaan) − biaya jabatan (5%, maks 500.000 × bulan kerja) − iuran JHT+JP karyawan − PTKP → PKP dibulatkan ke bawah ribuan → Pasal 17 → dikurangi PPh Jan–Nov. Karyawan baru **tidak disetahunkan** (sesuai contoh Tuan B PMK 168/2023).

| Kode | Bulan | Bruto setahun | Biaya jabatan | Iuran | PKP | PPh setahun | PPh Des penguji | app | Hasil |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| K01 | 12 | 92.434.995 | 4.621.749 | 2.430.000 | 22.383.000 | 1.119.150 | 289.568 | 289.568 | cocok |
| K02 | 12 | 50.993.640 | 2.549.682 | 1.440.000 | 0 | 0 | 0 | 0 | cocok |
| K03 (THR) | 12 | 176.070.400 | 6.000.000 | 4.439.578 | 93.630.000 | 8.044.500 | 2.065.252 | 2.065.252 | cocok |
| K04 (keluar Nov) | 11 | 109.557.800 | 5.477.890 | 3.135.000 | 37.944.000 | 1.897.200 | Nov: 403.230 | 403.230 | cocok |
| K05 | 12 | 187.272.000 | 6.000.000 | 4.919.578 | 117.852.000 | 11.677.800 | −338.820 | −338.820 | cocok |
| K06 | 12 | 69.425.400 | 3.471.270 | 1.320.000 | 0 | 0 | 0 | 0 | cocok |
| K07 (THR) | 12 | 98.404.000 | 4.920.200 | 0 | 34.983.000 | 1.749.150 | 496.470 | 496.470 | cocok |
| K08 | 12 | 271.977.600 | 6.000.000 | 6.599.578 | 191.878.000 | 22.781.700 | 343.548 | 343.548 | cocok |
| K09 | 12 | 68.217.245 | 3.410.862 | 1.944.000 | 0 | 0 | 0 | 0 | cocok |
| K10 | 12 | 45.600.000 | 2.280.000 | 0 | 0 | 0 | 0 | 0 | cocok |
| K11 (masuk Sep, THR) | 4 | 31.679.977 | 1.583.998 | 848.000 | 0 | 0 | −251.616 | −251.616 | cocok |
| K13 (masuk Des) | 1 | 4.509.703 | 225.485 | 127.742 | 0 | 0 | 0 | 0 | cocok |

Gaji bersih & biaya perusahaan per karyawan, serta rekap Desember (BPJS Kes 3.987.176; BPJS TK 7.356.846; gaji bersih 114.011.396; PPh positif 3.194.838; neto 2.604.402) — **semua cocok**.
Batas biaya jabatan K04 = 500.000 × 11 dan K11 = 500.000 × 4 diterapkan benar; K04 tidak ikut Desember ✓.

## Fitur pendukung
- `pph21-tahunan --tahun 2026`: 13/13 "cocok" dengan mesin pph21-ter (termasuk Lina keluar Sep, Dedi keluar Nov, Kiki, Mira).
- `rekap --tahun 2026`: hanya periode final, total per bulan konsisten dengan rekap bulanan.
- Revisi Oktober setelah Desember final (bonus Hadi terlewat): script memperingatkan "Periode 2026-11, 2026-12 sudah final dan bisa terpengaruh", dan `pph21-tahunan` langsung menandai **SELISIH −Rp 23.352** untuk Hadi → alur deteksi berantai bekerja.

## Catatan penguji
- ⚠️ Setoran PPh 21 Desember Rp 3.194.838 vs neto Rp 2.604.402 (kelebihan Eka & Kiki Rp 590.436 tidak dikompensasi) — sama dengan temuan P1-b.
- Skor skenario: 9/10.
