# 01 — PPh 21 setahun karyawan K/1 dengan THR

**Skenario:** S1 — permintaan normal: pemilik usaha ingin tahu potongan PPh 21 sepanjang 2026 untuk karyawan tetap, termasuk bulan THR dan Desember.

**Input pengguna (persis):**
> Karyawan saya statusnya K/1, gaji 12 juta sebulan. THR 12 juta dibayar bulan Maret. Iuran JHT+JP yang dipotong dari gajinya 360 ribu per bulan. PPh 21 setahun 2026 berapa aja per bulannya?

**Perintah yang dijalankan agent:**
`python3 scripts/pph21.py setahun --ptkp K/1 --gaji 12jt --iuran 360rb --tambahan Mar=12jt`

**Output (disampaikan ke pengguna):**

**PPh 21 2026 — status K/1 (TER kategori B)**

| Bulan | Penghasilan bruto | Tarif TER | PPh 21 dipotong |
|---|---:|---:|---:|
| Januari | Rp 12.000.000 | 3% | Rp 360.000 |
| Februari | Rp 12.000.000 | 3% | Rp 360.000 |
| Maret | Rp 24.000.000 | 9% | Rp 2.160.000 |
| April | Rp 12.000.000 | 3% | Rp 360.000 |
| Mei | Rp 12.000.000 | 3% | Rp 360.000 |
| Juni | Rp 12.000.000 | 3% | Rp 360.000 |
| Juli | Rp 12.000.000 | 3% | Rp 360.000 |
| Agustus | Rp 12.000.000 | 3% | Rp 360.000 |
| September | Rp 12.000.000 | 3% | Rp 360.000 |
| Oktober | Rp 12.000.000 | 3% | Rp 360.000 |
| November | Rp 12.000.000 | 3% | Rp 360.000 |
| Desember | Rp 12.000.000 | Pasal 17 (hitung ulang) | Rp 642.000 |
| **Jumlah** | **Rp 156.000.000** | | **Rp 6.402.000** |

**Hitung ulang Masa Pajak Terakhir (Desember)**
- Penghasilan bruto 12 bulan: Rp 156.000.000
- Biaya jabatan 5% (maks Rp 6.000.000): Rp 6.000.000
- Iuran pensiun/JHT/JP dibayar pegawai: Rp 4.320.000
- Penghasilan neto: Rp 145.680.000
- PTKP K/1: Rp 63.000.000
- PKP (dibulatkan ke bawah ke ribuan): Rp 82.680.000
  - 5% × Rp 60.000.000 = Rp 3.000.000
  - 15% × Rp 22.680.000 = Rp 3.402.000
- PPh 21 terutang setahun: Rp 6.402.000
- Sudah dipotong bulan-bulan sebelumnya: Rp 5.760.000
- **PPh 21 dipotong di Desember: Rp 642.000**

**Ringkasan setahun**
- Total bruto: Rp 156.000.000
- Total PPh 21 terutang (kredit pajak pegawai di SPT Tahunan): Rp 6.402.000

Catatan:
- Masa Pajak Terakhir: PPh 21 = PPh setahun (tarif Pasal 17 × PKP) − PPh yang sudah dipotong bulan sebelumnya. Bila hasilnya negatif, kelebihan dikembalikan ke pegawai paling lambat akhir bulan berikutnya (kecuali PPh DTP).
- Biaya jabatan 5% dari bruto, maks Rp 500.000 × jumlah bulan bekerja (maks Rp 6.000.000 setahun).
- Status PTKP ditentukan keadaan awal tahun (1 Januari).
- PPh 21 dibulatkan ke bawah ke rupiah penuh; PKP dibulatkan ke bawah hingga ribuan rupiah (PMK 168/2023 Pasal 8 ayat 4). Pembulatan belum dicocokkan dengan Coretax; bila Coretax menampilkan angka berbeda, ikuti Coretax.

_Alat bantu hitung, bukan nasihat pajak. Dasar: PP 58/2023 (tarif TER), PMK 168/2023 (tata cara PPh 21), UU 7/2021 HPP (PTKP & tarif Pasal 17), PMK 105/2025 (PPh 21 DTP 2026), berlaku per 23 September 2026. Untuk kasus khusus (ekspatriat, pesangon, pensiun, natura, gross-up) hubungi Kring Pajak 1500200 atau konsultan pajak._

Asumsi:
- "Gaji 12 juta" dianggap sudah penghasilan bruto pajak per bulan. Jika perusahaan membayar premi JKK, JKM, dan BPJS Kesehatan 4%, premi itu harus ditambahkan ke bruto (angka akan sedikit naik) — kirimkan rinciannya bila ingin dihitung ulang.
- Gaji tetap > Rp 10 juta, jadi PPh 21 DTP 2026 (PMK 105/2025) tidak berlaku dan tidak ditanyakan.

**Catatan penguji:**
- Angka diverifikasi dengan kalkulator independen penguji (tabel TER diurai langsung dari PDF PP 58/2023): Jan–Feb & Apr–Nov Rp 360.000 (TER B 3%), Maret Rp 2.160.000 (TER B 9% × 24 jt), Desember Rp 642.000, setahun Rp 6.402.000 — **cocok persis**.
- Bagus: hitung ulang Desember lengkap per lapisan, kategori B untuk K/1 benar, disclaimer & pembulatan jelas.
- Kurang (ringan): output `setahun` tidak mengingatkan bahwa premi JKK/JKM/BPJS Kesehatan perusahaan masuk bruto (subperintah `bulan` punya catatan itu). Agent harus menambahkannya sendiri sebagai asumsi (dilakukan di atas).
