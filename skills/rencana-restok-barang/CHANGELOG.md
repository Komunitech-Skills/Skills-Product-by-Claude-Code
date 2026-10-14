# Riwayat perubahan — rencana-restok-barang

Catatan teknis per versi (ringkasan pembeli ada di README).

## 1.0.0 (2026-10-14)
- Rilis awal. Script `rencana_restok.py` (Decimal, pustaka standar): membaca CSV/TSV/tabel markdown/XLSX/JSON, ekspor marketplace (baris judul dicari, status batal/belum bayar/retur dilewati, baris dobel per nomor pesanan), ekspor mutasi dan laporan stok buku-stok, tabel lebar per tanggal, data per minggu/bulan; tanggal campur format termasuk nomor seri Excel dan file bergaya bulan/tanggal.
- Hitungan: rata-rata dan simpangan harian, tren 4 minggu (dibatasi 0,5–1,5×), faktor musim dari pengguna, stok pengaman z × sd × √lead time, titik pesan ulang, stok target (lead time + horizon), kelompok PESAN SEKARANG / MINGGU DEPAN / AMAN, pembulatan ke minimal order dan isi per dus, nilai pesanan, pesanan per pemasok + draf WA, minimal belanja pemasok, catatan stok minus dan barang di daftar yang tidak ada di data penjualan, barang mati (≥ 60 hari), stok berlebih (> 90 hari), data belum cukup (< 14 hari), lonjakan (ditandai, bisa diabaikan atas persetujuan pengguna), pertanyaan usulan maksimal 3.
- 113 cek uji regresi dengan angka pembanding dihitung terpisah.
