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
     --kolom-total "<isi>" --kolom-status "<isi, opsional>" \
     --kolom-pesanan "<isi, bila ada kolom no. nota/pesanan>" --top 1000 > laporan/hasil-rekap.json
   ```
   `--top 1000` supaya `produk_terlaris` memuat **semua** produk (cek: jumlahnya =
   `jumlah_produk_unik`); total barang terjual (pcs) dihitung dari situ dengan script, bukan dikira:
   ```bash
   python3 -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); assert len(d['produk_terlaris'])==d['jumlah_produk_unik']; q=sum(p['qty'] for p in d['produk_terlaris']); print(int(q) if q==int(q) else q)" laporan/hasil-rekap.json
   ```
3. **Cek periode.** Bandingkan `periode.awal`/`periode.akhir` hasil JSON dengan periode yang
   seharusnya dicakup (mis. laporan Senin pagi = Senin-Minggu minggu lalu). Kalau tidak mencakup
   penuh (mis. cuma 1-2 hari untuk laporan mingguan), **jangan kirim sebagai laporan periode
   itu** -- katakan "Data yang tersedia mencakup <awal>-<akhir>, bukan seluruh <periode
   diminta>" dan hentikan, seperti data kosong.
4. Ambil dari hasil JSON: `total_omzet`, jumlah nota/baris (lihat aturan label di bawah), total
   pcs (dari perintah di atas), `rata_rata_omzet_per_hari_kalender`, 3 teratas `produk_terlaris`, `hari_terbaik`/
   `hari_terendah` (untuk laporan mingguan), dan **semua isi `peringatan`/`baris_dilewati`**.

## Format pesan (lewat scripts/susun_pesan.py)
- Judul: "Laporan Penjualan Harian" (periode 1 hari) atau "Laporan Penjualan Mingguan" (periode
  Senin-Minggu) -- pilih sesuai `periode.awal`/`periode.akhir` hasil hitung, bukan cuma nama
  jadwalnya.
- Baris angka: Total omzet (Rupiah), **Transaksi: `<N> nota / <Q> pcs`** (contoh "57 nota / 110
  pcs"), Rata-rata omzet/hari (Rupiah);
  untuk mingguan tambahkan Hari terbaik & Hari terendah
- **Aturan label hitungan (wajib):** `<N>` = jumlah `jumlah_transaksi_harian` dijumlahkan.
  Satuannya "nota" hanya bila `hari_transaksi_terbanyak.satuan` = "pesanan unik" (pakai
  `--kolom-pesanan`) **atau** pengguna memastikan 1 baris CSV = 1 nota; selain itu tulis
  "<N> baris penjualan". `<Q>` = total pcs dari script. Jangan pernah menyebut jumlah baris/nota
  sebagai "item" atau "barang terjual". Tanpa kolom qty → tulis nota/baris saja, tanpa pcs.
- Daftar: "Produk terlaris" -- 3 teratas, format `Nama -- qty pcs -- Rp omzet`
- `catatan` (netral): cakupan periode yang dilaporkan
- `peringatan`: baris dilewati, tanggal ambigu, status batal/retur yang dibuang, dll. dari script
- **Tanpa** nama pelanggan/nomor pesanan perorangan.

## Tujuan kirim
- Kanal: `<isi -- Telegram (default) atau WhatsApp nomor terpisah>`
- Penerima: `<isi ID chat Telegram atau nomor WA pemilik -- HARUS pemilik/admin sendiri>`
