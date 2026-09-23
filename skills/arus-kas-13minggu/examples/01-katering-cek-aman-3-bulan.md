# 01 — Katering rumahan: "Kas saya aman nggak 3 bulan ke depan?"

## Skenario
S1 — permintaan normal. Pemilik katering rumahan memberi data lengkap dalam kalimat biasa: saldo, penjualan mingguan, satu piutang, lima pengeluaran rutin bertanggal, satu belanja alat, dan bonus akhir tahun. Tanggal hari ini: Rabu, 23 September 2026. Semua nama fiktif.

## Input pengguna
> Halo, saya punya usaha katering rumahan. Saldo kas + rekening sekarang kira-kira 35 juta. Pemasukan rata-rata 15 juta per minggu dari pesanan harian. PT Arunika Fiktif masih punya tagihan ke saya 24 juta, biasanya baru dibayar pertengahan November. Pengeluaran: belanja bahan 9,5 juta per minggu, gaji 5 karyawan total 15 juta tiap tanggal 28, sewa dapur 7 juta tiap tanggal 5, cicilan mobil box 3,2 juta tiap tanggal 15, listrik-gas-air sekitar 2,5 juta tiap tanggal 20. Awal November saya mau beli freezer baru 12 juta, terus tanggal 20 Desember bayar bonus akhir tahun karyawan 15 juta. Kas saya aman nggak 3 bulan ke depan?

## Langkah yang dijalankan agent (mengikuti SKILL.md)
1. CSV rencana `rencana-kas.csv` (pemisah `;`):
   ```
   minggu;jenis;kategori;nominal;keterangan;kritis
   semua;masuk;Penjualan tunai (pesanan harian);15.000.000;perkiraan rata-rata;
   8;masuk;Pelunasan piutang;24.000.000;PT Arunika Fiktif (pertengahan November);
   semua;keluar;Belanja bahan (supplier);9.500.000;pasar & supplier ayam;ya
   tgl:28;keluar;Gaji karyawan;15.000.000;5 orang;ya
   tgl:5;keluar;Sewa dapur;7.000.000;;ya
   tgl:15;keluar;Cicilan mobil box;3.200.000;;ya
   tgl:20;keluar;Listrik, gas, air;2.500.000;;ya
   6;keluar;Freezer baru;12.000.000;rencana awal November;tidak
   12;keluar;Bonus akhir tahun karyawan;15.000.000;20 Desember;
   ```
2. `python3 scripts/proyeksi_kas.py rencana-kas.csv --saldo-awal "35 juta" --mulai 2026-09-28 --output-csv proyeksi-kas-13-minggu.csv`
3. Opsi di luar simulasi bawaan dihitung dengan mengubah CSV lalu menjalankan ulang script (langkah 6 SKILL.md).

## Output

## Proyeksi Kas 13 Minggu (28 Sep – 27 Des 2026)
Saldo awal Rp 35.000.000 · Batas aman Rp 17.969.231 (asumsi: rata-rata pengeluaran 1 minggu. Kalau Anda punya angka sendiri, misalnya "minimal 20 juta", kabari saya.)

| Mg | Periode | Masuk | Keluar | Saldo akhir | Status |
|---|---|---:|---:|---:|---|
| 1 | 28 Sep – 4 Okt | Rp 15.000.000 | Rp 24.500.000 | Rp 25.500.000 | 🟢 Aman |
| 2 | 5 – 11 Okt | Rp 15.000.000 | Rp 16.500.000 | Rp 24.000.000 | 🟢 Aman |
| 3 | 12 – 18 Okt | Rp 15.000.000 | Rp 12.700.000 | Rp 26.300.000 | 🟢 Aman |
| 4 | 19 – 25 Okt | Rp 15.000.000 | Rp 12.000.000 | Rp 29.300.000 | 🟢 Aman |
| 5 | 26 Okt – 1 Nov | Rp 15.000.000 | Rp 24.500.000 | Rp 19.800.000 | 🟢 Aman |
| 6 | 2 – 8 Nov | Rp 15.000.000 | Rp 28.500.000 | Rp 6.300.000 | 🟡 Di bawah batas |
| 7 | 9 – 15 Nov | Rp 15.000.000 | Rp 12.700.000 | Rp 8.600.000 | 🟡 Di bawah batas |
| 8 | 16 – 22 Nov | Rp 39.000.000 | Rp 12.000.000 | Rp 35.600.000 | 🟢 Aman |
| 9 | 23 – 29 Nov | Rp 15.000.000 | Rp 24.500.000 | Rp 26.100.000 | 🟢 Aman |
| 10 | 30 Nov – 6 Des | Rp 15.000.000 | Rp 16.500.000 | Rp 24.600.000 | 🟢 Aman |
| 11 | 7 – 13 Des | Rp 15.000.000 | Rp 9.500.000 | Rp 30.100.000 | 🟢 Aman |
| 12 | 14 – 20 Des | Rp 15.000.000 | Rp 30.200.000 | Rp 14.900.000 | 🟡 Di bawah batas |
| 13 | 21 – 27 Des | Rp 15.000.000 | Rp 9.500.000 | Rp 20.400.000 | 🟢 Aman |

Penempatan tanggal: gaji 28 September masuk minggu 1 (minggu 28 Sep – 4 Okt), sewa tanggal 5 masuk minggu 2, 6, dan 10, cicilan tanggal 15 masuk minggu 3, 7, dan 12, listrik tanggal 20 masuk minggu 4, 8, dan 12.

### Kesimpulan
- **Kas tidak sampai minus**, tapi ada 3 minggu yang tipis.
- **Titik paling kritis: minggu 6 (2–8 Nov), saldo tinggal Rp 6.300.000.** Penyebabnya, pada minggu yang sama ada freezer Rp 12.000.000, sewa dapur Rp 7.000.000, dan belanja bahan Rp 9.500.000. Minggu sebelumnya baru saja keluar gaji Rp 15.000.000. Uang dari PT Arunika Fiktif (Rp 24.000.000) baru masuk 2 minggu kemudian (minggu 8).
- Minggu negatif: tidak ada · Di bawah batas aman: minggu 6, 7, 12 (minggu 12 karena bonus Rp 15.000.000 jatuh bersamaan dengan cicilan dan listrik).
- Tambahan dana agar tidak minus: Rp 0 · agar selalu di atas batas aman: Rp 11.669.231.
- ⚠️ **Perlu diperhatikan:** dalam 13 minggu ini uang keluar (Rp 233.600.000) lebih besar dari uang masuk (Rp 219.000.000), jadi kas turun Rp 14.600.000. Selain itu, gaji 28 Desember (Rp 15.000.000) jatuh sehari setelah minggu 13, sehingga awal Januari saldo bisa tinggal sekitar Rp 5.400.000. Pola ini perlu dibenahi, misalnya lewat harga jual atau porsi belanja bahan, bukan hanya dengan menggeser jadwal bayar.

### Opsi tindakan (urut dari dampak terbesar dan paling mudah)
1. **Tunda beli freezer Rp 12.000.000 dari minggu 6 ke minggu 10 (awal Desember)**, sesudah PT Arunika membayar. Hasil hitung ulang: saldo minggu 6 naik dari Rp 6.300.000 menjadi Rp 18.300.000. Saldo terendah menjadi Rp 14.900.000 (minggu 12), dan minggu di bawah batas tinggal minggu 12. Caranya: kalau freezer lama masih bisa dipakai sebulan lagi, tanyakan ke toko apakah harganya bisa dikunci dengan DP kecil.
   *Alternatif lebih ringan:* cicil freezer 2 × Rp 6.000.000 (minggu 6 dan 10). Hasilnya saldo terendah Rp 12.300.000 di minggu 6, jadi masih di bawah batas.
2. **Minta PT Arunika Fiktif melunasi Rp 24.000.000 dua minggu lebih cepat (minggu 6, bukan minggu 8).** Hasil simulasi: minggu 6–7 menjadi Rp 30.300.000 dan Rp 32.600.000, saldo terendah Rp 14.900.000 (minggu 12), minggu di bawah batas tinggal minggu 12. Contoh kalimat: *"Pak/Bu, apakah tagihan Rp 24.000.000 bisa dibayar paling lambat 6 November? Kalau bisa, kami beri potongan 1% (Rp 240.000)."* Kalau perlu, saya bisa bantu menyusun pesan tagihan bertahap dengan skill `tagih-piutang`.
3. **Geser pembayaran bonus dari 20 Des (minggu 12) ke 23 Des (minggu 13), dengan persetujuan karyawan, lalu gabungkan dengan opsi 1.** Hasil hitung ulang: **semua 13 minggu aman**, saldo terendah Rp 18.300.000 (minggu 6), minggu 12 menjadi Rp 29.900.000. Bonus tetap dibayar sebelum Natal. Jangan menunda tanpa kesepakatan karyawan.
4. **Negosiasi termin bahan mundur 2 minggu dengan supplier (hanya bila supplier bersedia).** Hasil simulasi: saldo terendah naik ke Rp 25.300.000, tanpa minggu di bawah batas. **PERHATIAN:** Rp 9.500.000 tagihan bahan pindah ke setelah minggu 13, jadi kewajibannya tetap ada dan hanya pindah waktu. Termin ini juga berlaku seterusnya: setiap minggu Anda berutang 2 minggu belanja ke supplier.
5. **Tekan belanja bahan 5% (Rp 9.500.000 → Rp 9.025.000 per minggu)**, misalnya dengan beli grosir, mengurangi sisa bahan terbuang, atau menyesuaikan menu. Hasil hitung ulang: saldo akhir minggu 13 naik dari Rp 20.400.000 menjadi Rp 26.575.000 (+Rp 6.175.000). Saldo terendah Rp 9.150.000 (minggu 6). Opsi ini tidak menyelesaikan minggu 6, tetapi mengurangi masalah struktural dan membantu menutup gaji 28 Desember.

Catatan: simulasi otomatis "tunda belanja non-kritis" dari script ikut menunda **bonus karyawan** karena kata "bonus" dianggap tidak kritis. Karena itu hasil tersebut tidak saya pakai. Menunda bonus tanpa kesepakatan tidak disarankan.

### File Excel
`proyeksi-kas-13-minggu.csv` bisa dibuka di Excel/Google Sheets. Pemisahnya titik koma (`;`), cocok untuk Excel berbahasa Indonesia. Isinya: rincian per pos per minggu, total, saldo, batas aman, dan status.

Asumsi: penjualan rata Rp 15.000.000/minggu · minggu 1 mulai Senin 28 Sep 2026 · PT Arunika membayar di minggu 8 (16–22 Nov) · batas aman = rata-rata pengeluaran 1 minggu · Pembulatan: setiap nominal dibulatkan ke rupiah penuh.
Catatan: proyeksi ini berdasarkan perkiraan Anda. Perbarui setiap minggu dengan angka aktual. Ini bukan nasihat keuangan profesional.

## Catatan penguji
- **Angka diverifikasi independen**: 13/13 minggu (masuk, keluar, saldo, status) dan batas aman cocok dengan hitungan terpisah. Hitungan pembanding menempatkan pos per tanggal kalender, bukan lewat pencarian per minggu seperti script (`/tmp/uji-arus-kas-13minggu/verif/`). Lima varian opsi (freezer, piutang, pecah, gabungan, freezer+bonus) juga cocok.
- Bagus: `tgl:28` dengan minggu mulai 28 Sep benar ditempatkan di minggu 1. Peringatan "jatuh setelah minggu 13" muncul di simulasi supplier.
- Kurang (sedang): simulasi "Tunda belanja non-kritis" otomatis menunda **bonus karyawan** Rp 15.000.000 ke setelah minggu 13 (kata "bonus" masuk `KATA_NONKRITIS`). Agent harus menjelaskannya sendiri.
- Kurang (sedang): script tidak memberi tahu bahwa masalahnya struktural (arus kas bersih 13 minggu −Rp 14.600.000). Script juga tidak mendeteksi pos rutin yang jatuh tepat setelah horizon (gaji 28 Des). Kedua hal itu di sini ditemukan oleh penguji, bukan diminta SKILL.md.
- Kurang (ringan): hasil "Gabungan" dari script (saldo terendah Rp 35.000.000) terlihat sangat bagus, padahal Rp 24.500.000 kewajiban didorong ke luar horizon. Hasil itu tidak dipakai di sini.
