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
1. Cek kesiapan data:
   ```bash
   python3 <folder-skill-laporan-otomatis-terjadwal>/scripts/cek_sumber_data.py \
     --folder "<folder sumber>" --pola "*.csv" --label "penjualan" --maks-umur-hari 10
   ```
2. Kalau siap, jalankan (lihat `rekap-penjualan-csv/SKILL.md` untuk detail argumen):
   ```bash
   python3 <folder-skill-rekap-penjualan-csv>/scripts/rekap.py "<file terbaru>" \
     --kolom-tanggal "<isi>" --kolom-produk "<isi>" --kolom-qty "<isi>" \
     --kolom-total "<isi>" --kolom-status "<isi, opsional>" --top 3
   ```
3. Ambil dari hasil JSON: `total_omzet`, `jumlah_baris_valid`,
   `rata_rata_omzet_per_hari_kalender`, 3 `produk_terlaris`, `hari_terbaik`/`hari_terendah`
   (untuk laporan mingguan), dan **semua isi `peringatan`/`baris_dilewati`**.

## Format pesan (lewat scripts/susun_pesan.py)
- Judul: "Laporan Penjualan Harian" atau "Laporan Penjualan Mingguan"
- Baris angka: Total omzet (Rupiah), Jumlah transaksi, Rata-rata omzet/hari (Rupiah); untuk
  mingguan tambahkan Hari terbaik & Hari terendah
- Daftar: "Produk terlaris" -- 3 item, format `Nama -- qty pcs -- Rp omzet`
- Catatan: sertakan peringatan dari script (baris dilewati, tanggal ambigu, dll.)
- **Tanpa** nama pelanggan/nomor pesanan perorangan.

## Tujuan kirim
- Kanal: `<isi -- Telegram (default) atau WhatsApp nomor terpisah>`
- Penerima: `<isi ID chat Telegram atau nomor WA pemilik -- HARUS pemilik/admin sendiri>`
