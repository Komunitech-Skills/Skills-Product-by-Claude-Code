# Mencatat supaya data tidak berantakan lagi

Panduan singkat untuk pemilik usaha yang mencatat pelanggan, stok, atau penjualan di Excel/Google Sheets.

> Prinsip tabel rapi di bawah ini diadaptasi dari pelajaran *Data Organization in Spreadsheets* (Data Carpentry, The Carpentries), berlisensi CC BY 4.0, https://datacarpentry.org/spreadsheet-ecology-lesson/ . **Telah diubah:** ditulis ulang dalam Bahasa Indonesia dengan contoh usaha Indonesia; contoh ekologi dan bagian lain tidak dipakai. Lihat `ATTRIBUTION.md`.

## 5 aturan yang cukup untuk 90% masalah

1. **Satu baris = satu catatan.** Satu pesanan, satu pelanggan, atau satu produk per baris. Jangan menyisipkan baris judul atau subjumlah di tengah data.
2. **Satu kolom = satu jenis isi.** Kolom "Nama" hanya nama; kolom "No HP" hanya nomor. Jangan menulis "Budi - 0812xxxx - Bandung" dalam satu sel; pisahkan jadi tiga kolom.
3. **Satu sel = satu nilai.** Dua nomor HP? Buat dua kolom (HP 1, HP 2). Jangan memakai sel gabungan (merge cells) di dalam data.
4. **Warna dan coretan bukan data.** Baris yang "diwarnai kuning = sudah dibayar" hilang saat file diekspor. Buat kolom "Status" (Lunas / Belum) dan isi tulisannya.
5. **Format seragam dari awal.** Tanggal selalu `2026-10-05` (tahun-bulan-hari), nomor HP selalu `628...` tanpa spasi/strip, harga hanya angka tanpa "Rp" dan titik (atur format sel, bukan diketik), kota ditulis seragam (pilih "Yogyakarta" atau "Jogja", jangan campur).

## Kebiasaan tambahan yang menyelamatkan
- **Simpan salinan data mentah.** Jangan menimpa file asli; rapikan di salinan. (Itu sebabnya alat ini tidak pernah menimpa file asli.)
- **Judul kolom satu baris, tanpa spasi/tanda aneh di ujung**, dan tidak kembar. Contoh: `Nama Pelanggan`, `No HP`, `Tanggal Order`, `Total Bayar`.
- **Sel kosong dibiarkan kosong.** Jangan mengisi "-", "NA", "tidak ada", atau 0 untuk "tidak tahu"; angka 0 berarti nol sungguhan.
- **Jangan menyimpan nomor HP sebagai angka.** Excel membuang 0 depan dan menampilkan `6,28E+11`. Atur kolom bertipe *Teks* sebelum mengetik/menempel.
- **Satu tabel per lembar**, tanpa catatan atau kotak ringkasan di sampingnya. Ringkasan dibuat di lembar lain.
- **Ekspor sebagai CSV UTF-8** untuk dipindah antaraplikasi; semua alat bisa membacanya.

## Template kolom siap pakai
| Kebutuhan | Kolom yang disarankan |
|---|---|
| Daftar pelanggan | Nama Pelanggan, No HP, Kota, Tanggal Pertama Beli, Setuju Dihubungi (Ya/Tidak), Tanggal Setuju |
| Penjualan | No Pesanan, Tanggal Order, Nama Pelanggan, Produk, Jumlah, Harga Satuan, Total Bayar, Status |
| Stok | Kode Produk, Nama Produk, Satuan, Stok Awal, Masuk, Keluar, Stok Akhir |
| Buku kas | Tanggal, Keterangan, Kategori, Masuk, Keluar |
