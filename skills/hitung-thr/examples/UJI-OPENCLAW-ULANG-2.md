# Uji ulang 2 OpenClaw — hitung-thr 1.0.5

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal asli (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech`. Home `sol2-thr` direset lewat script reset tepat sebelum skenario (tidak ada file data yang perlu dibuat ulang; semua data ada di pesan). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama dan uji ulang 1 ([UJI-OPENCLAW-ULANG.md](UJI-OPENCLAW-ULANG.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python dan script skill dijalankan ulang oleh penguji. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran). Keluaran mentah: `hasil/ulang4-*.txt`.
Home `sol2-thr` hanya berisi skill `hitung-thr`.

## Cacat sisa dari uji ulang 1 (versi 1.0.4)
1. Giliran 1 menanyakan nama karyawan dulu (*"saya tidak boleh pakai nama contoh dari skill"*), hitungan baru keluar di giliran 2.
2. Tanggal Lebaran keliru (20 Maret 2027 = 11 Syawal 1448 H) tidak ditanggapi; rencana bayar 13 Maret jatuh setelah Idul Fitri perkiraan (±10 Maret).
3. Kecil: SE Menaker 2026 dikutip untuk Lebaran 2027; kolom PPh "–" tetapi total "Rp 0".

## Pesan member (giliran 1)
> Halo, hitungin THR karyawan saya dong. Gajinya 4,5 juta sebulan, mulai kerja 1 Maret 2026, lebarannya 20 Maret 2027.

Jawaban lanjutan member dari uji ulang 1 (*"ga usah pake nama, langsung aja"*) **tidak diperlukan**: hitungan lengkap sudah keluar di giliran 1.

## Giliran 1 — alat `read, exec` (selesai satu giliran)
> Halo! Ini hasil hitungan THR-nya.
>
> ⚠️ **Catatan tanggal Lebaran dulu:** 20 Maret 2027 itu setara 11 Syawal 1448 H (bukan 1 Syawal/Idul Fitri). Perkiraan Idul Fitri 1448 H jatuh di **10 Maret 2027** (kalender tabular — tanggal resmi masih menunggu penetapan pemerintah/SKB). Saya hitung pakai perkiraan ini; batas bayar H-7 jadi **3 Maret 2027**. Kalau nanti ternyata tanggal resminya beda, kabari saya, saya hitung ulang — risikonya kalau telat bayar ada denda 5%.
>
> **Rincian THR Idul Fitri 1448 H — Usaha Anda**
> Hari raya (perkiraan): Rabu, 10 Maret 2027 · **Batas bayar (H-7): Rabu, 3 Maret 2027**
>
> | Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR | THR diterima |
> |---|---|---:|---:|---|---:|---:|
> | Karyawan 1 | Tetap (PKWTT) | 12 bln | Rp 4.500.000 | masa kerja ≥ 12 bulan → 1× upah | **Rp 4.500.000** | **Rp 4.500.000** |
>
> Masa kerja dari 1 Maret 2026 sampai 10 Maret 2027 = pas 12 bulan penuh → THR full 1 bulan gaji = **Rp 4.500.000**.
>
> **Asumsi yang saya pakai:**
> - Nama karyawan belum disebut → saya pakai "Karyawan 1".
> - Status PTKP tidak diberikan → PPh 21 atas THR belum dihitung (kalau mau, kasih tahu status PTKP-nya, nanti saya hitungkan potongannya juga).
> - Upah 1 bulan = gaji pokok Rp 4,5 juta (asumsi tidak ada tunjangan tetap terpisah).
>
> **Draf pengumuman (tanpa nominal pribadi):**
> ```
> Yth. Rekan-rekan karyawan Usaha Anda,
>
> Menyambut Idul Fitri 1448 H, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan paling lambat Rabu, 3 Maret 2027 (7 hari sebelum hari raya).
>
> Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
> • Masa kerja 1 s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.
>
> Rincian THR masing-masing akan disampaikan secara pribadi. Ada pertanyaan, silakan hubungi HR/keuangan.
>
> Selamat menyambut hari raya.
>
> Salam,
> Manajemen Usaha Anda
> ```
>
> _Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Permenaker 6/2016, SE Menaker M/3/HK.04.00/III/2026, berlaku per 23 September 2026. Sengketa/kasus khusus → Disnaker atau Posko THR (poskothr.kemnaker.go.id)._
>
> Mau saya tambahkan karyawan lain, atau hitungkan potongan PPh 21-nya kalau status PTKP-nya ada?

## Verifikasi independen
- `tahun_hijriah.py 2027-03-20 --cek idul-fitri` (dijalankan penguji): *"PERINGATAN: 2027-03-20 = 11 Syawal 1448 H, bukan 1 Syawal … Idul Fitri 1448 H diperkirakan 2027-03-10 … batas bayar THR (H-7) = 2027-03-03."* Balasan menyalin isi ini dengan benar ✔.
- 10 Maret 2027 = Rabu, 3 Maret 2027 = Rabu ✔ (Python `datetime`).
- Masa kerja 1 Mar 2026 s.d. 10 Mar 2027 = 12 bulan 9 hari → ≥ 12 bulan → THR = 1 × 4.500.000 = **Rp4.500.000** ✔ (Permenaker 6/2016 Ps. 3). Dengan tanggal member (20 Mar) hasilnya sama.
- "1448 H" benar untuk Idul Fitri Maret 2027 ✔.

## Penilaian
- **Cacat sisa hilang: YA (keduanya).**
  1. Tidak bertanya nama: *"Nama karyawan belum disebut → saya pakai "Karyawan 1"."* Hitungan lengkap di giliran 1.
  2. Tanggal keliru ditanggapi sopan sekali: *"20 Maret 2027 itu setara 11 Syawal 1448 H (bukan 1 Syawal/Idul Fitri). Perkiraan Idul Fitri 1448 H jatuh di 10 Maret 2027 … batas bayar H-7 jadi 3 Maret 2027 … risikonya kalau telat bayar ada denda 5%."* Batas bayar kini aman.
  3. Inkonsistensi "Rp 0" hilang (kolom PPh tidak ditampilkan; PTKP disebut "belum dihitung" di asumsi).
- **Regresi:** tidak ada. Catatan kecil: (a) agent langsung memakai tanggal perkiraan, bukan tanggal member, tetapi terbuka soal itu dan menawarkan hitung ulang (lebih aman bagi member; nilai THR sama); (b) frasa *"pas 12 bulan penuh"* kurang tepat (12 bulan 9 hari), hasil tetap benar; (c) SE Menaker **2026** masih dikutip untuk Lebaran 2027 (sisa saran no. 3 dari uji ulang 1, belum direvisi).
- **Skor: 8,5/10** (uji ulang 1: 7). **LULUS.**
