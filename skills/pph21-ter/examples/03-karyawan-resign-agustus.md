# 03 — Karyawan resign di tengah tahun

**Skenario:** S3 — permintaan normal: karyawan berhenti akhir Agustus, pengguna bingung PPh terakhirnya.

**Input pengguna (persis):**
> Pak, karyawan saya resign akhir Agustus 2026. Gajinya 17,5 juta, status TK/0, iuran pensiun dipotong 100rb tiap bulan. Dia cuma pindah kerja, masih di Indonesia. PPh 21 bulan terakhirnya gimana?

**Perintah:** `python3 scripts/pph21.py setahun --ptkp TK/0 --gaji 17,5jt --iuran 100rb --akhir 8 --status berhenti`
(tanpa `--disetahunkan`, karena karyawan masih subjek pajak dalam negeri)

**Output:**

**PPh 21 2026 — status TK/0 (TER kategori A)**

| Bulan | Penghasilan bruto | Tarif TER | PPh 21 dipotong |
|---|---:|---:|---:|
| Januari | Rp 17.500.000 | 8% | Rp 1.400.000 |
| Februari | Rp 17.500.000 | 8% | Rp 1.400.000 |
| Maret | Rp 17.500.000 | 8% | Rp 1.400.000 |
| April | Rp 17.500.000 | 8% | Rp 1.400.000 |
| Mei | Rp 17.500.000 | 8% | Rp 1.400.000 |
| Juni | Rp 17.500.000 | 8% | Rp 1.400.000 |
| Juli | Rp 17.500.000 | 8% | Rp 1.400.000 |
| Agustus | Rp 17.500.000 | Pasal 17 (hitung ulang) | (Rp 3.620.000) lebih potong |
| **Jumlah** | **Rp 140.000.000** | | **Rp 6.180.000** |

**Hitung ulang Masa Pajak Terakhir (Agustus)**
- Penghasilan bruto 8 bulan: Rp 140.000.000
- Biaya jabatan 5% (maks Rp 4.000.000): Rp 4.000.000
- Iuran pensiun/JHT/JP dibayar pegawai: Rp 800.000
- Penghasilan neto: Rp 135.200.000
- PTKP TK/0: Rp 54.000.000
- PKP (dibulatkan ke bawah ke ribuan): Rp 81.200.000
  - 5% × Rp 60.000.000 = Rp 3.000.000
  - 15% × Rp 21.200.000 = Rp 3.180.000
- PPh 21 terutang bagian tahun: Rp 6.180.000
- Sudah dipotong bulan-bulan sebelumnya: Rp 9.800.000
- **Lebih potong Agustus: Rp 3.620.000** → wajib dikembalikan ke pegawai paling lambat akhir bulan berikutnya

**Ringkasan setahun**
- Total bruto: Rp 140.000.000
- Total PPh 21 terutang (kredit pajak pegawai di SPT Tahunan): Rp 6.180.000
- Kelebihan potong yang harus dikembalikan: Rp 3.620.000

Catatan:
- Masa Pajak Terakhir: PPh 21 = PPh setahun (tarif Pasal 17 × PKP) − PPh yang sudah dipotong bulan sebelumnya. Bila hasilnya negatif, kelebihan dikembalikan ke pegawai paling lambat akhir bulan berikutnya (kecuali PPh DTP).
- Biaya jabatan 5% dari bruto, maks Rp 500.000 × jumlah bulan bekerja (maks Rp 6.000.000 setahun).
- Status PTKP ditentukan keadaan awal tahun (1 Januari).
- PPh 21 dibulatkan ke bawah ke rupiah penuh; PKP dibulatkan ke bawah hingga ribuan rupiah (PMK 168/2023 Pasal 8 ayat 4). Pembulatan belum dicocokkan dengan Coretax; bila Coretax menampilkan angka berbeda, ikuti Coretax.

_Alat bantu hitung, bukan nasihat pajak. Dasar: PP 58/2023 (tarif TER), PMK 168/2023 (tata cara PPh 21), UU 7/2021 HPP (PTKP & tarif Pasal 17), PMK 105/2025 (PPh 21 DTP 2026), berlaku per 23 September 2026. Untuk kasus khusus (ekspatriat, pesangon, pensiun, natura, gross-up) hubungi Kring Pajak 1500200 atau konsultan pajak._

Artinya: di slip gaji Agustus, perusahaan **tidak memotong** PPh 21 lagi dan **mengembalikan Rp 3.620.000** ke karyawan (paling lambat akhir September 2026), serta memberikan bukti potong Masa Pajak Terakhir (A1) agar bisa diserahkan ke kantor barunya.

**Catatan penguji:**
- Angka sama persis dengan contoh resmi Tuan D di Lampiran PMK 168/2023 (lebih potong Rp 3.620.000; PPh terutang Rp 6.180.000).
- Koreksi pembuat terverifikasi dari teks PMK 168/2023 Lampiran I.2 angka 6 huruf a: pegawai yang berhenti tetapi tetap subjek pajak dalam negeri dihitung atas penghasilan selama bekerja, PTKP penuh, **tidak disetahunkan**; penyetahunan (angka 6 huruf c, Pasal 15 ayat 3) hanya bila kewajiban pajak subjektif mulai/berakhir (contoh Tuan C & E). Skill menerapkannya dengan benar.
