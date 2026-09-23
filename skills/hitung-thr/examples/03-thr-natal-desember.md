# 03 — THR Natal dibayar Desember

**Skenario:** S3 — permintaan normal; THR jatuh di Masa Pajak Terakhir (Desember).

**Input pengguna (persis):**
> THR Natal untuk Yohanes, K/2, gaji pokok 9 juta + tunjangan tetap 1 juta, kerja dari April 2022. Rencana dibayar 18 Desember 2026. Berapa THR-nya dan pajaknya? Usaha kami bengkel, bukan tekstil/pariwisata. Iuran JHT+JP dia 300 ribu sebulan, gaji 10 juta flat sepanjang tahun.

**Perintah 1:** `python3 scripts/thr.py --hari-raya 2026-12-25 --nama-hari-raya "Natal 2026" --nama "Contoh Yohanes" --ptkp K/2 --gaji-pokok 9jt --tunjangan-tetap 1jt --mulai 2022-04-01 --tanggal-bayar 2026-12-18`

**Rincian THR Natal 2026 — -**
Hari raya: Jumat, 25 Desember 2026 · **Batas bayar (H-7): Jumat, 18 Desember 2026** · Rencana bayar: Jumat, 18 Desember 2026

| Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR | Tambahan PPh 21 | THR diterima |
|---|---|---:|---:|---|---:|---:|---:|
| Contoh Yohanes | Tetap (PKWTT) | 56 bln | Rp 10.000.000 | masa kerja ≥ 12 bulan → 1 × upah | **Rp 10.000.000** | – | Rp 10.000.000 |
| **Total** | | | | | **Rp 10.000.000** | **Rp 0** | **Rp 10.000.000** |


⚠️ Peringatan:
- Contoh Yohanes: THR dibayar di Masa Pajak Terakhir (Desember/bulan berhenti): PPh 21 dihitung ulang setahun — gunakan hitungan setahun (skill pph21-ter/slip-gaji-bpjs).

Catatan:
- THR wajib dibayar penuh (tidak dicicil) paling lambat 7 hari sebelum hari raya. Terlambat: denda 5% dari total THR, dan THR tetap wajib dibayar (Permenaker 6/2016 Pasal 10).
- THR bukan dasar iuran BPJS (iuran dihitung dari upah pokok + tunjangan tetap).
- 'Tambahan PPh 21' = selisih PPh 21 bulan itu dengan dan tanpa THR (THR digabung ke bruto bulan dibayar, tarif TER bisa naik). Di Desember semua dihitung ulang setahun.
- Pembulatan: THR ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax).
- Masa kerja dihitung dalam bulan penuh sampai tanggal hari raya (asumsi skill; aturan tidak mengatur pecahan bulan). Ubah dengan kolom masa_kerja_bulan bila perusahaan memakai cara lain.

**Draf pengumuman untuk karyawan (siap kirim WA/email):**

```
Yth. Rekan-rekan karyawan kami,

Menyambut Natal 2026, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan pada Jumat, 18 Desember 2026 (paling lambat Jumat, 18 Desember 2026, yaitu 7 hari sebelum hari raya).

Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026):
• Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
• Masa kerja 1 bulan s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
• THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.

Rincian THR masing-masing akan disampaikan secara pribadi. Jika ada pertanyaan, silakan hubungi bagian HR/keuangan.

Selamat menyambut hari raya. Terima kasih atas kerja keras Bapak/Ibu.

Salam,
Manajemen
```

_Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Permenaker 6/2016, SE Menaker M/3/HK.04.00/III/2026, PP 58/2023 & PMK 168/2023 (PPh 21 TER), berlaku per 23 September 2026. Untuk sengketa/kasus khusus hubungi Disnaker setempat, Posko THR (poskothr.kemnaker.go.id), Kring Pajak 1500200, atau konsultan._

**Perintah 2 (sesuai langkah 4 SKILL.md, hitung ulang setahun dengan skill `pph21-ter`):**
`python3 ../pph21-ter/scripts/pph21.py setahun --ptkp K/2 --gaji 10jt --tambahan Des=10jt --iuran 300rb`

**PPh 21 2026 — status K/2 (TER kategori B)**

| Bulan | Penghasilan bruto | Tarif TER | PPh 21 dipotong |
|---|---:|---:|---:|
| Januari | Rp 10.000.000 | 1,5% | Rp 150.000 |
| Februari | Rp 10.000.000 | 1,5% | Rp 150.000 |
| Maret | Rp 10.000.000 | 1,5% | Rp 150.000 |
| April | Rp 10.000.000 | 1,5% | Rp 150.000 |
| Mei | Rp 10.000.000 | 1,5% | Rp 150.000 |
| Juni | Rp 10.000.000 | 1,5% | Rp 150.000 |
| Juli | Rp 10.000.000 | 1,5% | Rp 150.000 |
| Agustus | Rp 10.000.000 | 1,5% | Rp 150.000 |
| September | Rp 10.000.000 | 1,5% | Rp 150.000 |
| Oktober | Rp 10.000.000 | 1,5% | Rp 150.000 |
| November | Rp 10.000.000 | 1,5% | Rp 150.000 |
| Desember | Rp 20.000.000 | Pasal 17 (hitung ulang) | Rp 995.000 |
| **Jumlah** | **Rp 130.000.000** | | **Rp 2.645.000** |

**Hitung ulang Masa Pajak Terakhir (Desember)**
- Penghasilan bruto 12 bulan: Rp 130.000.000
- Biaya jabatan 5% (maks Rp 6.000.000): Rp 6.000.000
- Iuran pensiun/JHT/JP dibayar pegawai: Rp 3.600.000
- Penghasilan neto: Rp 120.400.000
- PTKP K/2: Rp 67.500.000
- PKP (dibulatkan ke bawah ke ribuan): Rp 52.900.000
  - 5% × Rp 52.900.000 = Rp 2.645.000
- PPh 21 terutang setahun: Rp 2.645.000
- Sudah dipotong bulan-bulan sebelumnya: Rp 1.650.000
- **PPh 21 dipotong di Desember: Rp 995.000**

**Ringkasan setahun**
- Total bruto: Rp 130.000.000
- Total PPh 21 terutang (kredit pajak pegawai di SPT Tahunan): Rp 2.645.000

Catatan:
- Masa Pajak Terakhir: PPh 21 = PPh setahun (tarif Pasal 17 × PKP) − PPh yang sudah dipotong bulan sebelumnya. Bila hasilnya negatif, kelebihan dikembalikan ke pegawai paling lambat akhir bulan berikutnya (kecuali PPh DTP).
- Biaya jabatan 5% dari bruto, maks Rp 500.000 × jumlah bulan bekerja (maks Rp 6.000.000 setahun).
- Status PTKP ditentukan keadaan awal tahun (1 Januari).
- PPh 21 dibulatkan ke bawah ke rupiah penuh; PKP dibulatkan ke bawah hingga ribuan rupiah (PMK 168/2023 Pasal 8 ayat 4). Pembulatan belum dicocokkan dengan Coretax; bila Coretax menampilkan angka berbeda, ikuti Coretax.

_Alat bantu hitung, bukan nasihat pajak. Dasar: PP 58/2023 (tarif TER), PMK 168/2023 (tata cara PPh 21), UU 7/2021 HPP (PTKP & tarif Pasal 17), PMK 105/2025 (PPh 21 DTP 2026), berlaku per 23 September 2026. Untuk kasus khusus (ekspatriat, pesangon, pensiun, natura, gross-up) hubungi Kring Pajak 1500200 atau konsultan pajak._

Ringkasnya: THR Rp 10.000.000 dibayar paling lambat Jumat, 18 Desember 2026. PPh 21 bulan Desember (gaji + THR, hitung ulang setahun) = **Rp 995.000**; tanpa THR, PPh Desember akan Rp 495.000, jadi tambahan karena THR ≈ Rp 500.000.

Asumsi: "gaji 10 juta" dianggap sudah bruto pajak (bila ada premi JKK/JKM/BPJS Kes perusahaan, bruto sedikit lebih besar).

**Catatan penguji:**
- Script THR benar tidak memakai TER di Desember dan mengarahkan ke hitung ulang setahun. Angka Desember diverifikasi independen: dengan THR, PKP Rp 52.900.000 → PPh setahun Rp 2.645.000 − Rp 1.650.000 = Rp 995.000; tanpa THR, PKP Rp 42.900.000 → Rp 2.145.000 − Rp 1.650.000 = Rp 495.000; tambahan karena THR Rp 500.000. Cocok.
- Gaji ≤ Rp 10 jt di 2026, tetapi pengguna sudah menyebut sektor bengkel → DTP tidak berlaku; agent tidak perlu bertanya lagi.
- Kurang (ringan): hand-off ke `pph21-ter` membutuhkan agent memasang kedua skill; bila hanya `hitung-thr` terpasang, agent harus hitung manual. Saran: `thr.py` bisa menerima `--bruto-sd-bulan-lalu`/`--pph21-sd-bulan-lalu` dan memanggil `ter_core.hitung_masa_terakhir` (sudah tersedia di folder yang sama).
