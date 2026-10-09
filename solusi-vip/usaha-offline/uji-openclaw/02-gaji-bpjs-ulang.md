# Uji ulang 02 — Gaji September + BPJS + PPh 21 (gaji-umkm 1.0.6)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech` (jawaban dilayani `claude-sonnet-5`). Home baru `sol2-usaha-offline` (paket skill solusi, dibuat ulang lewat script reset sebelum skenario). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama ([02-gaji-bpjs.md](02-gaji-bpjs.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran).

## Pesan member (giliran 1)
> Tolong hitungin gaji september 2 karyawan warung makan saya di Solo. Andi: gapok 2,8jt + uang makan tetap 300rb, status nikah anak 1, lembur 3 hari masing2 2 jam (hari kerja biasa). Sari: gapok 2,65jt, belum nikah, ga lembur. Dua2nya ikut BPJS Kesehatan & BPJS TK (JHT, JKK, JKM, JP). Yg ditransfer ke masing2 berapa, saya nyetor BPJS berapa total, PPh 21 nya ada ga?

## Giliran 1 — alat `read, ls, exec` (89 dtk)
> Sudah saya hitung pakai mesin payroll resmi skill gaji-umkm (hitungan sementara, belum disimpan ke database). Ini rekap gaji September 2026 untuk 2 karyawan:
>
> **REKAP GAJI SEPTEMBER 2026**
>
> | Nama | Gapok+Tunj. Tetap | Lembur | Total Pendapatan | Potongan BPJS (karyawan) | PPh 21 | **Transfer (take home)** |
> |---|---:|---:|---:|---:|---:|---:|
> | Andi (K/1) | Rp 3.100.000 | Rp 188.150 | Rp 3.288.150 | Rp 124.000 | Rp 0 | **Rp 3.164.150** |
> | Sari (TK/0) | Rp 2.650.000 | — | Rp 2.650.000 | Rp 106.000 | Rp 0 | **Rp 2.544.000** |
> | **Total** | | | **Rp 5.938.150** | | | **Rp 5.708.150** |
>
> Detail lembur Andi (hari kerja biasa, PP 35/2021, dasar upah 3.100.000/173): 3 hari × 2 jam → jam ke-1 = 1,5× upah sejam, jam ke-2 = 2× upah sejam ≈ Rp 62.717/hari × 3 = Rp 188.150.
>
> **Yang Bapak/Ibu transfer ke karyawan:**
> - Andi: **Rp 3.164.150**
> - Sari: **Rp 2.544.000**
> - Total transfer gaji: **Rp 5.708.150**
>
> **Setoran BPJS (total 2 karyawan):**
> - BPJS Kesehatan (4% perusahaan + 1% karyawan dari gapok+tunjangan tetap): **Rp 287.500**
> - BPJS Ketenagakerjaan (JHT, JKK, JKM, JP — perusahaan+karyawan): **Rp 531.300**
> - **Total setor BPJS: Rp 818.800**
>
> **PPh 21:** Rp 0 untuk Andi maupun Sari — penghasilan bruto bulanan keduanya masih di bawah ambang kena pajak skema TER bulanan untuk kategori PTKP masing-masing. Tidak ada yang perlu disetor bulan ini.
>
> **Biaya total perusahaan (gaji + iuran perusahaan):** Rp 6.526.950
>
> Catatan tambahan (pakai angka dari mesin hitung, bukan nasihat hukum/pajak):
> - Dasar: Perpres 64/2020 (BPJS Kesehatan), PP 44/45/46/2015 (BPJS TK), PP 35/2021 (lembur), PP 58/2023 & PMK 168/2023 (PPh 21 TER). Pembulatan belum dicocokkan dengan Coretax/aplikasi BPJS resmi.
>
> ⚠️ Dua hal perlu Bapak cek supaya hitungan ini pas:
> 1. **UMK Kota Surakarta (Solo) 2026** belum saya masukkan — tanpa ini saya tidak bisa cek apakah gaji Sari (TK/0, 2,65jt) di bawah UMK. Boleh kirim angka UMK Solo dari SK Gubernur?
> 2. **Tarif JKK perusahaan** saya pakai default 0,24% (risiko sangat rendah). Kalau sertifikat BPJS Ketenagakerjaan warung Bapak beda, tolong kasih tahu angkanya.
> 3. Saya asumsikan Andi & Sari sudah bekerja sejak sebelum September (bukan karyawan baru bulan ini) — kalau salah satu baru masuk/keluar bulan ini, beri tahu tanggalnya karena itu memengaruhi PPh 21.
>
> Ini masih hitungan sekali pakai. Kalau mau saya jadikan **aplikasi gaji bulanan** (data Andi & Sari tersimpan, tinggal update lembur/kasbon tiap bulan, bisa bikin slip & file transfer CSV, dikunci per periode), bilang saja "ya, simpan" — nanti saya buatkan databasenya.

## Giliran 2
Jawaban member sama dengan uji pertama: *"Andi masuk 1 Maret 2022, Sari 1 Januari 2024. Belum pernah pakai, bikinin aja."* (dikirim karena agent menawarkan menyimpan dan meminta konfirmasi data). Alat `exec` (101 dtk).

> Database gaji sudah jadi dan hasilnya sama persis dengan hitungan cepat tadi (angka tidak berubah karena tanggal masuk Andi & Sari sudah lama, jadi September 2026 tetap dihitung normal, bukan bulan masuk/keluar).
>
> **Aplikasi gaji "Warung Makan" sudah dibuat** di komputer Bapak sendiri (`KomunitechData/gaji/gaji.db`), isinya:
> - K001 Andi — tetap, K/1, gapok Rp 2.800.000 + tunjangan tetap Rp 300.000, masuk 1 Maret 2022, BPJS kes+tk+jp
> - K002 Sari — tetap, TK/0, gapok Rp 2.650.000, masuk 1 Januari 2024, BPJS kes+tk+jp
> - Lembur Andi September sudah diisi: 2+2+2 jam (3 hari)
> - Gaji September 2026 sudah dihitung (status: **DRAF**, belum dikunci)
>
> **REKAP GAJI SEPTEMBER 2026**
> | Kode | Nama | Pendapatan | Potongan | PPh 21 | Gaji bersih (transfer) | Biaya perusahaan |
> |---|---|---:|---:|---:|---:|---:|
> | K001 | Andi | Rp 3.288.150 | Rp 124.000 | Rp 0 | **Rp 3.164.150** | Rp 3.605.590 |
> | K002 | Sari | Rp 2.650.000 | Rp 106.000 | Rp 0 | **Rp 2.544.000** | Rp 2.921.360 |
> | | **Total** | **Rp 5.938.150** | **Rp 230.000** | **Rp 0** | **Rp 5.708.150** | **Rp 6.526.950** |
>
> **Yang harus dibayar/disetor:**
> - Transfer ke Andi: Rp 3.164.150
> - Transfer ke Sari: Rp 2.544.000
> - Setor BPJS Kesehatan: Rp 287.500
> - Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 531.300
> - Setor PPh 21: **Rp 0** (belum kena pajak bulan ini)
>
> ⚠️ Masih sama seperti tadi, dua hal ini perlu dikonfirmasi biar aplikasinya akurat ke depan:
> 1. **UMK Kota Surakarta/Solo 2026** (dari SK Gubernur) — belum diisi, jadi cek batas bawah upah & BPJS Kesehatan dilewati.
> 2. **Tarif JKK** usaha warung makan — saya pakai default 0,24% (risiko sangat rendah). Kalau sertifikat BPJS TK Bapak beda, kasih tahu angkanya, nanti saya update (`gaji.py atur`).
>
> Kalau datanya sudah dicek dan sudah pas, bilang **"final"** — nanti saya kunci periode September ini, baru bisa bikin slip gaji per orang dan file transfer CSV untuk diunggah ke bank. Database ini juga sudah siap dipakai tiap bulan ke depan, tinggal update lembur/kasbon lalu hitung ulang.

## Verifikasi independen
Upah/jam 3.100.000/173 = 17.919,08; lembur 3,5 × 17.919,08 × 3 = **188.150** ✔. BPJS Kes 5% × (3.100.000 + 2.650.000) = **287.500** ✔. BPJS TK 9,24% (JHT 5,7 + JKK 0,24 + JKM 0,3 + JP 3) × 3.100.000 = 286.440 + × 2.650.000 = 244.860 → **531.300** ✔. Total setor **818.800** ✔. Transfer **3.164.150 / 2.544.000** ✔. Biaya perusahaan 5.938.150 + 588.800 = **6.526.950** ✔. PPh 21 TER A/B = 0 ✔. Database giliran 2 menghasilkan angka identik.

## Penilaian
- **Cacat lama hilang: YA.** Angka lengkap langsung keluar di giliran 1 tanpa menanyakan tanggal masuk dulu: *"Saya asumsikan Andi & Sari sudah bekerja sejak sebelum September … kalau salah satu baru masuk/keluar bulan ini, beri tahu tanggalnya"*. UMK & JKK digabung dalam satu pesan.
- **Regresi:** tidak ada yang berarti. Kecil: *"Dua hal perlu Bapak cek"* lalu tiga butir.
- Database dibuat hanya setelah member setuju; slip & CSV ditawarkan setelah "final". Sesuai alur.
- **Skor: 9/10** (uji pertama SESUDAH: 8).
