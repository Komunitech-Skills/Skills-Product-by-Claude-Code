# Resep laporan: Penjualan <harian/mingguan>

_Salin file ini ke `laporan/RESEP-penjualan-<harian atau mingguan>.md` di workspace pengguna,
lalu isi bagian bertanda `<isi>` sesuai jawaban wawancara._

## Sumber data
- Folder: `<isi -- mis. Dokumen/Laporan-AI/masuk/penjualan/>`
- Pola file: `*.csv` (ekspor kasir/Shopee/Tokopedia/spreadsheet disimpan sebagai CSV)
- Kolom tanggal: `<isi>` · Kolom produk: `<isi>` · Kolom qty: `<isi, opsional>` ·
  Kolom total/harga: `<isi>` · Kolom status pesanan: `<isi, opsional -- disarankan untuk
  ekspor marketplace agar pesanan batal/retur tidak ikut terhitung>`

## Jadwal
- `<isi -- mis. Setiap Senin 07:00 WIB, untuk periode Senin-Minggu lalu>`
- Zona waktu: Asia/Jakarta (default) atau `<isi bila beda>`

## Langkah hitung
1. Cek kesiapan data. `--maks-umur-hari` HARUS lebih ketat dari irama jadwal, supaya file basi
   (mis. ekspor minggu lalu yang lupa diganti) tidak lolos tanpa peringatan: **harian = 1**,
   **mingguan = 6**.
   ```bash
   python3 <folder-skill-laporan-otomatis-terjadwal>/scripts/cek_sumber_data.py \
     --folder "<folder sumber>" --pola "*.csv" --label "penjualan" --maks-umur-hari <1 atau 6>
   ```
   Kalau pengguna mengekspor **satu file per hari** tapi jadwalnya mingguan (terlihat dari
   `file_lain_cocok` > 0), jalankan ulang dengan `--daftar-semua`, lalu gabungkan (concat, satu
   header saja) file-file bertanggal dalam minggu target sebelum Langkah 2 -- memakai hanya file
   terbaru akan membuat laporan mingguan cuma menghitung 1 hari.
2. Kalau siap, jalankan (lihat `rekap-penjualan-csv/SKILL.md` untuk detail argumen):
   ```bash
   python3 <folder-skill-rekap-penjualan-csv>/scripts/rekap.py "<file terbaru atau gabungan>" \
     --kolom-tanggal "<isi>" --kolom-produk "<isi>" --kolom-qty "<isi>" \
     --kolom-total "<isi>" --kolom-status "<isi, opsional>" --top 3
   ```
3. **Cek periode.** Bandingkan `periode.awal`/`periode.akhir` hasil JSON dengan periode yang
   seharusnya dicakup (mis. laporan Senin pagi = Senin-Minggu minggu lalu). Kalau tidak mencakup
   penuh (mis. cuma 1-2 hari untuk laporan mingguan), **jangan kirim sebagai laporan periode
   itu** -- katakan "Data yang tersedia mencakup <awal>-<akhir>, bukan seluruh <periode
   diminta>" dan hentikan, seperti data kosong.
4. Ambil dari hasil JSON: `total_omzet`, `jumlah_baris_valid` (ini jumlah **baris/item terjual**,
   BUKAN jumlah pesanan/transaksi unik -- satu pesanan marketplace bisa berisi beberapa baris
   produk), `rata_rata_omzet_per_hari_kalender`, 3 `produk_terlaris`, `hari_terbaik`/
   `hari_terendah` (untuk laporan mingguan), dan **semua isi `peringatan`/`baris_dilewati`**.

## Format pesan (lewat scripts/susun_pesan.py)
- Judul: "Laporan Penjualan Harian" (periode 1 hari) atau "Laporan Penjualan Mingguan" (periode
  Senin-Minggu) -- pilih sesuai `periode.awal`/`periode.akhir` hasil hitung, bukan cuma nama
  jadwalnya.
- Baris angka: Total omzet (Rupiah), Jumlah baris/item terjual (label ini, bukan "jumlah
  transaksi", supaya tidak disalahartikan sebagai jumlah pesanan), Rata-rata omzet/hari (Rupiah);
  untuk mingguan tambahkan Hari terbaik & Hari terendah
- Daftar: "Produk terlaris" -- 3 item, format `Nama -- qty pcs -- Rp omzet`
- `catatan` (netral): cakupan periode yang dilaporkan
- `peringatan`: baris dilewati, tanggal ambigu, status batal/retur yang dibuang, dll. dari script
- **Tanpa** nama pelanggan/nomor pesanan perorangan.

## Tujuan kirim
- Kanal: `<isi -- Telegram (default) atau WhatsApp nomor terpisah>`
- Penerima: `<isi ID chat Telegram atau nomor WA pemilik -- HARUS pemilik/admin sendiri>`
