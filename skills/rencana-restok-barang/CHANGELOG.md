# Riwayat perubahan — rencana-restok-barang

Catatan teknis per versi (ringkasan pembeli ada di README).

## 1.0.1 (2026-10-14)
Revisi dari uji OpenClaw penguji independen (versi 1.0.0: 6,1 → 8,3, LULUS); lima temuan diperbaiki:
- **Akan kosong sebelum barang datang:** script menghitung `akan_kosong_hari` = ⌈lead time − stok ÷ laku/hari⌉ untuk semua barang yang stoknya diketahui, termasuk barang "data belum cukup" (memakai laju sementara). Daftar `akan_kosong_sebelum_barang_datang` + jumlahnya di ringkasan, dengan saran (pesan hari ini / pesanan kecil untuk barang data pendek, pemasok lebih cepat, atau terima kosong ±X hari). Ditulis paling atas di balasan.
- **Tren:** dideteksi dari laju 4 minggu terakhir vs sampai 8 minggu sebelumnya (bukan vs rata-rata seluruh data yang ikut memuat minggu terakhir), ambang ±20 % tetap. Laju yang dipakai = laju 4 minggu terakhir, dibatasi 0,5–2,0× rata-rata seluruh data (sebelumnya 0,5–1,5×); batas yang terpakai disebut terbuka. `kalimat_tren` per barang + catatan tren per barang; SKILL.md melarang menulis "stabil/tidak tajam" untuk barang naik/turun. Contoh: minyak goreng 130 → 165 per 4 minggu kini "naik 27 %" (sebelumnya "stabil").
- **Pencocokan nama:** huruf besar/kecil, tanda kurung, tanda baca, dan spasi diabaikan ("(isi 3)" = "isi 3"); SKU tanpa tanda baca/spasi. Nama yang hanya mirip masuk kelompok baru MUNGKIN BARANG YANG SAMA dan ditanyakan, tidak lagi dicatat sebagai barang mati.
- **Lonjakan:** aturan baru (> rata-rata + 3 simpangan, ≥ 4× dan ≥ 8 di atas median hari laku); hasil tanpa lonjakan dihitung sebagai pembanding (`tanpa_lonjakan`), catatan menyebut bila tren naik terjadi karena lonjakan, pertanyaan "promo atau borongan sekali?" dengan dua hasil.
- **Hitungan manual (tanpa Python):** wajib menampilkan baris rumus dengan angka terisi untuk maksimal 5 barang, asumsi simpangan disebut, pembulatan ke atas.
- Lain-lain: `--lead-time` dari pengguna dilabeli "lead time umum dari pengguna" (tidak ditanya ulang); satuan diambil dari nama bila tertulis dalam kurung, mis. "(karung)"; tabel lebar baris = minggu/tanggal dan kolom = barang terbaca langsung; ringkasan tanpa harga menampilkan `[isian]`, bukan Rp0; catatan "7 hari terakhir lebih ramai" bila ≥ 20 % dan ≥ 5 unit di atas rata-rata.
- Uji regresi: 139 cek (26 cek baru untuk butir di atas).

## 1.0.0 (2026-10-14)
- Rilis awal. Script `rencana_restok.py` (Decimal, pustaka standar): membaca CSV/TSV/tabel markdown/XLSX/JSON, ekspor marketplace (baris judul dicari, status batal/belum bayar/retur dilewati, baris dobel per nomor pesanan), ekspor mutasi dan laporan stok buku-stok, tabel lebar per tanggal, data per minggu/bulan; tanggal campur format termasuk nomor seri Excel dan file bergaya bulan/tanggal.
- Hitungan: rata-rata dan simpangan harian, tren 4 minggu (dibatasi 0,5–1,5×), faktor musim dari pengguna, stok pengaman z × sd × √lead time, titik pesan ulang, stok target (lead time + horizon), kelompok PESAN SEKARANG / MINGGU DEPAN / AMAN, pembulatan ke minimal order dan isi per dus, nilai pesanan, pesanan per pemasok + draf WA, minimal belanja pemasok, catatan stok minus dan barang di daftar yang tidak ada di data penjualan, barang mati (≥ 60 hari), stok berlebih (> 90 hari), data belum cukup (< 14 hari), lonjakan (ditandai, bisa diabaikan atas persetujuan pengguna), pertanyaan usulan maksimal 3.
- 113 cek uji regresi dengan angka pembanding dihitung terpisah.
