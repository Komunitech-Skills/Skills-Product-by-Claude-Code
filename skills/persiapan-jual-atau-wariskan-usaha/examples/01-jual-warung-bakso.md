# Skenario 1 (normal): pemilik warung bakso ingin menjual usaha

- Tanggal: 2026-10-09 · Penguji independen (agent, bukan pembuat) · Platform: `claude-code (simulasi agent)`
- Cara: penguji berperan sebagai agent yang mengikuti SKILL.md apa adanya (termasuk menjalankan `scripts/nilai_usaha.py` persis seperti rumus di SKILL.md). Semua data fiktif.
- Berkas ini menggantikan berkas parsial dari uji sebelumnya yang terputus (berkas lama tidak dipakai sebagai hasil).

## Pesan pengguna

> Saya Pak Darto, jualan bakso "Bakso Mas Darto" di Klaten sudah 7 tahun. Kios sewa, sisa kontrak 2 tahun. Mau pensiun, rencana dioper tahun depan. Laba bersih 2023 84 juta, 2024 97 juta, 2025 91 juta, itu sudah dipotong ambilan saya 3 juta/bulan. Kalau pembeli pakai orang buat jaga, gajinya kira2 3,5 juta/bulan. Tahun 2024 ada renovasi kios+gerobak 12 juta, sekali itu saja, sudah masuk biaya 2024. Alat (gerobak, freezer, meja kursi, motor) kira2 65 juta, anggap turun 25%. Utang koperasi sisa 18 juta. Tetangga nawar "dua kali laba", saya mikirnya 2 sampai 3 kali. Resep bumbu cuma saya yang tahu, potong saja 20%. Biaya notaris/perantara anggap 4%. Setelah pensiun butuh 6 juta/bulan selama 18 bulan. Kira2 laku berapa, apa yang harus disiapkan?

## Perintah hitung (angka dihitung ulang skrip 2026-10-13)

```
python3 scripts/nilai_usaha.py --laba 2023=84000000 2024=97000000 2025=91000000 --kelipatan 2 3 \
  --aset 65000000 --utang 18000000 --penyesuaian-aset 25 --gaji-diambil 36000000 --gaji-pengganti 42000000 \
  --biaya-sekali 2024=12000000 --diskon-pemilik 20 --biaya-transaksi 4 --kebutuhan-bulanan 6000000 --bulan 18
```

Renovasi Rp12.000.000 dicatat hanya di tahun kejadiannya (2024). Bagian 3 di output di bawah memakai keluaran perintah ini.

## Output agent (SESUDAH, dengan skill)

# Persiapan Jual Usaha "Bakso Mas Darto"

**1. Ringkasan situasi dan asumsi**
- Warung bakso 7 tahun di Klaten, kios sewa (sisa kontrak 2 tahun). Tujuan: **dijual/dioper**, target tahun depan → kerangka **12 bulan**.
- Laba yang Bapak sebut sudah dipotong ambilan Bapak Rp3.000.000/bulan (Rp36.000.000/tahun). Pembeli perlu penjaga Rp3.500.000/bulan (Rp42.000.000/tahun), jadi laba dihitung ulang dari sudut pembeli.
- Renovasi Rp12.000.000 dianggap biaya sekali jalan dan ditambahkan kembali hanya ke laba 2024.
- Kelipatan 2-3 kali, potongan resep 20%, penyusutan alat 25%, biaya notaris/perantara 4%: **semua asumsi Bapak sendiri**, bukan angka pasar.

**2. Daftar periksa kesiapan**

| Area | Status | Langkah berikut |
|---|---|---|
| Pembukuan 2-3 tahun | Setengah (ada angka laba per tahun, belum tahu rinciannya) | Rapikan rekap uang masuk-keluar per bulan 2023-2025 |
| Pemisahan uang pribadi-usaha | Belum diketahui | Buka/rapikan rekening khusus warung |
| SOP | Belum (resep hanya di kepala Bapak) | Tulis resep bumbu & alur masak langkah demi langkah |
| Ketergantungan pada pemilik | Belum | Latih 1 orang meracik bumbu sampai rasanya sama |
| Aset | Setengah (ada perkiraan nilai) | Daftar alat + bukti milik (BPKB motor, nota freezer) |
| Utang | Siap (koperasi Rp18.000.000) | Putuskan: dilunasi dari hasil jual atau dialihkan |
| Kontrak sewa | Setengah (sisa 2 tahun) | Tanya pemilik kios: boleh dialihkan ke pembeli? |
| Izin (NIB, PIRT/halal bila ada) | Belum diketahui | Cek atas nama siapa |
| Pelanggan/pemasok kunci | Belum diketahui | Catat pemasok daging/mie dan langganan besar |
| Karyawan | Belum diketahui | Daftar karyawan dan hak yang tertunda |
| Akun online / nomor WA | Belum diketahui | Pastikan atas nama usaha, bisa diserahkan |
| Penerus/pembeli | Setengah (ada tetangga berminat) | Jangan buka data rinci sebelum serius |

**Prioritas pembenahan:** (1) tulis resep & latih peracik, (2) rapikan pembukuan 3 tahun, (3) tanya pemilik kios soal pengalihan sewa, (4) putuskan nasib utang koperasi.

**3. Perkiraan rentang nilai** *(bahan diskusi, bukan harga pasti)*

Laba setelah penyesuaian per tahun: 2023 Rp78.000.000; 2024 Rp103.000.000; 2025 Rp85.000.000 (renovasi ditambahkan kembali hanya ke 2024). Rata-rata Rp88.666.667; tahun terakhir Rp85.000.000; basis dipakai Rp85.000.000 (laba tahun terakhir lebih rendah dari rata-rata, jadi dipakai angka yang lebih hati-hati).

| Metode | Rumus | Hasil |
|---|---|---|
| Kelipatan laba (nilai usaha berjalan, sebelum utang) | basis × kelipatan [2-3] × (100 - 20)/100 | Rp136.000.000 s/d Rp204.000.000 |
| Nilai aset setelah penyesuaian (batas bawah bila hanya alat dijual, sebelum utang) | Rp65.000.000 × (100 - 25)/100 | Rp48.750.000 |
| Harga yang dibayar pembeli | | Rp136.000.000 s/d Rp204.000.000 |
| Setelah biaya 4% | | Rp130.560.000 s/d Rp195.840.000 |
| Hasil bersih ke Bapak (setelah biaya dan utang koperasi Rp18.000.000 dilunasi) | | Rp112.560.000 s/d Rp177.840.000 |
| Aset dikurangi utang (gambaran bila warung ditutup dan alat dijual) | | Rp30.750.000 |

Kebutuhan setelah pensiun Rp6.000.000 × 18 = Rp108.000.000; selisih hasil bersih ke Bapak vs kebutuhan: Rp4.560.000 s/d Rp69.840.000.

Peringatan: nilai aset adalah batas bawah bila warung hanya dijual alatnya. Kelipatan dan persentase adalah asumsi Bapak, bukan angka pasar. Pajak dan biaya notaris belum dihitung. **Ini bahan diskusi, bukan harga pasti.**

**4. Pilihan struktur** (tanyakan ke notaris/konsultan pajak): jual seluruh warung (alat + resep + nama + pengalihan sewa) atau hanya alat; bayar sekaligus atau bertahap; masa pendampingan Bapak 1-3 bulan untuk mengajari bumbu.

**5. Rencana transisi 12 bulan**

| Bulan | Tugas |
|---|---|
| 1 | Isi daftar periksa; kumpulkan catatan 2023-2025; tetapkan harga terendah yang Bapak terima |
| 2-3 | Pisahkan uang warung; rekap aset & utang; tanya pemilik kios soal pengalihan sewa |
| 3-5 | Tulis resep & SOP; latih peracik; Bapak mulai libur 1 hari/minggu untuk uji |
| 4-6 | Bawa daftar pertanyaan ke notaris & konsultan pajak |
| 6-9 | Kenalkan calon pembeli ke pemasok & langganan; buka data setelah ada perjanjian kerahasiaan |
| 9-12 | Pendampingan; ubah nama izin/rekening/akun; umumkan ke karyawan & pelanggan |

Rencana darurat: siapa memegang resep tertulis, kunci kios, kontak pemasok bila Bapak mendadak sakit.

**6. Dokumen untuk calon pembeli:** rekap keuangan 2023-2025 + mutasi rekening; daftar alat & bukti milik; daftar utang; kontrak sewa kios; NIB/izin; daftar karyawan; SOP & resep (diserahkan setelah sepakat); daftar pemasok (tanpa kontak sebelum serius); perjanjian kerahasiaan.

**7. Pertanyaan untuk notaris & konsultan pajak:** bagaimana pengalihan NIB/izin; kontrak sewa perlu persetujuan pemilik kios?; bagaimana perjanjian kerahasiaan & pendampingan dibuat; apa kewajiban pajak atas penjualan usaha/alat; apakah pajak perlu diperhitungkan dalam harga terendah.

**8. Penutup.** Ini persiapan, bukan nasihat hukum/pajak atau penilaian resmi; tanggal acuan Oktober 2026. Pertanyaan: (1) Utang koperasi akan dilunasi dari hasil jual? (2) Ada karyawan selain Bapak? (3) Tetangga yang menawar sudah menyebut angka?

## Catatan penguji

- **Angka dihitung ulang skrip 2026-10-13** (`scripts/nilai_usaha.py` versi 1.0.1, perintah di atas, renovasi hanya di 2024): laba setelah penyesuaian 2023 Rp78.000.000; 2024 Rp103.000.000; 2025 Rp85.000.000; basis = tahun terakhir Rp85.000.000 (peringatan "laba tahun terakhir lebih rendah dari rata-rata" muncul); kelipatan Rp136.000.000 s/d **Rp204.000.000**; setelah biaya 4% Rp130.560.000 s/d Rp195.840.000; hasil bersih ke pemilik setelah utang Rp112.560.000 s/d Rp177.840.000; selisih vs kebutuhan Rp4.560.000 s/d Rp69.840.000. Bagian 3 output di atas sudah memakai angka ini.
- Utang koperasi Rp18 juta dikurangkan sekali (dilunasi dari hasil jual), dan nilai jual-alat-saja ditampilkan terpisah sebagai batas bawah, tidak lagi dicampur dalam satu rentang gabungan.
- Hal positif: struktur 8 bagian lengkap, status tidak ditebak, asumsi dilabeli milik pengguna, rencana per bulan konkret, tidak menyebut "script", maks 3 pertanyaan, tidak menjanjikan harga.
- Nilai uji asli (2026-10-09): **6,5/10**, diberikan sebelum angka bagian 3 dihitung ulang; bagian lain output tidak diubah.
