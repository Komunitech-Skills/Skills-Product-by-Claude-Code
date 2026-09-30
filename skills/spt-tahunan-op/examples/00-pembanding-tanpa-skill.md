# 00 — Uji A/B: tanpa skill vs dengan skill (skenario normal 06)

Penguji independen, 2026-09-30. Kedua jawaban dari agent headless Claude Sonnet (`claude -p`) dengan prompt pengguna yang sama. Tanpa skill: tanpa akses file/tool. Dengan skill: membaca `SKILL.md` dan menjalankan `scripts/spt_op.py`.

**Prompt:** "Saya karyawan di satu perusahaan, status menikah anak 2 (K/2). Di bukti potong A1 tahun 2025: penghasilan neto Rp180.000.000, PPh 21 yang dipotong Rp10.500.000. Hitung SPT tahunan saya: kurang bayar atau lebih bayar berapa, dan apa yang harus saya siapkan?"

## A. Tanpa skill (apa adanya)

> # Hitungan SPT Tahunan 2025 (K/2)
> 
> **Hasilnya kurang bayar Rp375.000.**
> 
> | Komponen | Jumlah (Rp) |
> |---|---|
> | Penghasilan neto setahun | 180.000.000 |
> | PTKP: WP 54.000.000 + kawin 4.500.000 + 2 anak 9.000.000 | (67.500.000) |
> | **PKP** | **112.500.000** |
> | PPh terutang: 5% × 60.000.000 = 3.000.000; 15% × 52.500.000 = 7.875.000 | 10.875.000 |
> | Kredit pajak (PPh 21 dipotong di A1) | (10.500.000) |
> | **PPh kurang bayar (Pasal 29)** | **375.000** |
> 
> ## Yang perlu disiapkan
> 1. **Bukti potong A1** dari perusahaan.
> 2. **Akses Coretax DJP**, yaitu NPWP/NIK dan kata sandi. Pastikan akun sudah aktif.
> 3. **Daftar harta dan utang per 31 Desember 2025**: kas/tabungan, kendaraan, tanah/rumah, investasi, dan cicilan (KPR, kendaraan).
> 4. **Data keluarga**: NIK istri/suami dan kedua anak, sesuai Kartu Keluarga.
> 5. **Penghasilan lain**, jika ada: usaha sampingan, sewa, bunga, dividen. Jika pasangan bekerja dan tidak pisah harta, penghasilannya digabung ke SPT Anda.
> 6. **Kode billing dan bukti bayar (NTPN)** untuk kekurangan Rp375.000. Buat kode billing di Coretax dengan jenis pajak PPh Pasal 29 Orang Pribadi (MAP 411125, KJS 300). Bayar dulu, lalu isi NTPN di SPT.
> 7. **Formulir SPT 1770 S**, karena Anda karyawan dengan penghasilan neto di atas Rp60 juta.
> 
> ## Catatan
> - **Selisih Rp375.000 sebaiknya dicek.** Jika pemotongan Januari–Desember benar, PPh 21 di A1 biasanya sudah sama dengan yang terutang, yaitu Rp10.875.000. Kemungkinan penyebabnya:
>   - Perusahaan memakai status PTKP yang berbeda.
>   - Ada penghasilan yang belum masuk hitungan.
>   - Angka neto atau PTKP di A1 berbeda dari hitungan ini.
> 
>   Kalau A1 memang keliru, minta HRD memperbaikinya. Kalau tidak, bayar selisihnya sendiri.
> - **Batas lapor SPT 2025 adalah 31 Maret 2026, dan hari ini sudah 30 September 2026.** Jika belum lapor, ada denda keterlambatan Rp100.000 untuk orang pribadi. Kekurangan bayar juga bisa kena sanksi bunga bulanan, jadi bayar dan lapor secepatnya. Jika sudah lapor tetapi angkanya keliru, buat pembetulan.
> - Hitungan ini memakai angka neto dari A1 apa adanya, yaitu setelah biaya jabatan dan iuran pensiun/JHT. Jika ada zakat/sumbangan wajib atau penghasilan lain, hasilnya bisa berubah.

## B. Dengan skill (apa adanya)

> ## Hitungan SPT Tahunan PPh OP — Tahun Pajak 2025 (status K/2)
> 
> Hasilnya **KURANG BAYAR Rp375.000**. Angka di bawah dihitung dengan script `spt_op.py`.
> 
> | Langkah | Jumlah |
> |---|---|
> | Penghasilan neto (A1) | Rp180.000.000 |
> | PTKP K/2 (54 jt + 4,5 jt kawin + 2 × 4,5 jt anak) | Rp67.500.000 |
> | PKP (neto − PTKP) | Rp112.500.000 |
> | PPh terutang: 5% × 60 jt | Rp3.000.000 |
> | PPh terutang: 15% × 52,5 jt | Rp7.875.000 |
> | **Total PPh terutang** | **Rp10.875.000** |
> | Kredit pajak (PPh 21 di A1) | Rp10.500.000 |
> | **Kurang bayar (PPh Pasal 29)** | **Rp375.000** |
> 
> **Penjelasan singkat:** Pajak setahun yang seharusnya Anda bayar adalah Rp10.875.000. Kantor baru memotong Rp10.500.000, jadi masih kurang Rp375.000. Selisih seperti ini sering terjadi karena pemotongan bulanan hanya perkiraan. Anda wajib menyetor selisihnya sebelum melapor.
> 
> **⚠️ Batas lapor sudah lewat.** Batas lapor tahun pajak 2025 adalah 31 Maret 2026, diperpanjang sampai 30 April 2026. Hari ini 30 September 2026, jadi Anda terlambat. Kalau belum lapor:
> - Lapor secepatnya.
> - Denda telat lapor Rp100.000, ditagih lewat STP.
> - Kekurangan bayar yang disetor setelah batas juga kena bunga bulanan. Tarifnya berubah tiap bulan, jadi tidak saya hitung.
> 
> **Peta ke Coretax**
> - **Lampiran 1:** neto pekerjaan dan bukti potong A1, biasanya terisi otomatis. Harta, utang, dan tanggungan juga diisi di sini.
> - **Induk Bagian B dan C:** neto, PTKP, PKP, dan PPh terutang.
> - **Induk Bagian D dan E:** kredit pajak dan kurang bayar.
> 
> **Langkah berikutnya**
> 1. Login Coretax dan cek A1 sudah muncul otomatis.
> 2. Isi harta, utang, dan tanggungan (istri dan 2 anak, lengkap dengan NIK).
> 3. SPT kurang bayar masuk ke "SPT menunggu pembayaran", dan kode billing dibuat otomatis. Bayar Rp375.000 (ditambah bunga bila ada), lalu kirim SPT.
> 
> **Yang perlu disiapkan**
> - [ ] Akun Coretax aktif (NIK/NPWP 16 digit) dan kode otorisasi untuk tanda tangan SPT
> - [ ] Bukti potong A1 (satu lembar dari pemberi kerja)
> - [ ] Daftar harta per 31 Desember 2025 (tanah, kendaraan, tabungan, deposito, emas, investasi), dengan tahun perolehan dan nilai
> - [ ] Daftar utang per 31 Desember 2025 (KPR, kredit kendaraan, pinjaman)
> - [ ] Data keluarga dan NIK tanggungan sesuai keadaan 1 Januari 2025
> - [ ] Dana Rp375.000 untuk melunasi PPh Pasal 29
> 
> **Asumsi:**
> - Status K/2 berlaku per 1 Januari 2025.
> - Hanya satu pemberi kerja.
> - Tidak ada zakat mandiri, penghasilan lain, atau angsuran PPh 25 (semuanya dianggap 0).
> - Istri tidak digabung (bukan K/I).
> 
> Kalau salah satu asumsi itu tidak sesuai, kabari saya dan hitungannya saya ulang.
> 
> _Ini alat bantu hitung, bukan nasihat pajak. Pembulatan belum dicocokkan dengan Coretax. Saya tidak mengisi atau mengirim SPT atas nama Anda. Cek ulang ke Coretax DJP, Kring Pajak 1500200, atau konsultan pajak terdaftar sebelum melapor._

## Penilaian berdampingan

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Angka (PTKP, PKP, PPh, KB Rp375.000) | Benar | Benar (dihitung script, bisa diaudit) |
| Formulir | **Salah**: "Formulir SPT 1770 S" — sudah dihapus sejak TP 2025 (PER-11/PJ/2025) | Benar: satu SPT OP Coretax + peta Lampiran/Bagian |
| Cara bayar KB | Kurang tepat: suruh buat billing sendiri & isi NTPN (alur DJP Online lama) | Benar: Coretax membuat kode billing otomatis ("SPT menunggu pembayaran") |
| Batas lapor | 31 Maret 2026, tidak tahu KEP-55 | Tahu KEP-55, tetapi menyebut "diperpanjang" (DJP: jatuh tempo formal tetap 31 Maret; yang diberikan penghapusan sanksi s.d. 30 April) |
| Wawasan | **Lebih baik**: menyarankan cek HRD karena 1 pemberi kerja setahun penuh seharusnya NIHIL | Tidak ada; malah salah menyebut "kantor baru" |
| Checklist, asumsi, disclaimer | Checklist cukup; tanpa disclaimer | Lengkap, asumsi eksplisit, disclaimer |

**Kesimpulan:** dengan skill lebih baik secara jelas pada ketepatan prosedur era Coretax (formulir, billing, peta lampiran) dan konsistensi, tetapi selisihnya **tidak telak** untuk kasus sederhana — model dasar sudah menghitung angka yang sama dan memberi satu wawasan yang tidak dimiliki skill. Nilai tambah skill lebih besar pada kasus NPPN/pemberitahuan, zakat, pembulatan PKP, dan beberapa bukti potong (lihat 07–08).
