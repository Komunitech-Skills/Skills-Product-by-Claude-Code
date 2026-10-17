# Riwayat perubahan — rekap-penjualan-csv

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.2.6 (2026-10-17)
- Temuan uji bot Telegram asli 17 Okt 2026 (gelombang A5, ekspor gaya Shopee September 72 baris): tanpa skill 8,0 → dengan skill 6,5, BELUM. Angka utama benar, tetapi (1) satu kalimat insight dikarang dan bertentangan dengan daftar produk ("Topi Baseball paling banyak terjual … paling murah"; yang benar Tote Bag Natural 23 pcs, Rp 35.000/pcs); (2) memakai istilah "margin per unit" padahal data tidak memuat modal; (3) produk terlaris menurut jumlah tidak disebut; (4) balasan chat terlalu berat (judul `##`, dua jenis rata-rata).
- Script kini menghitung semua perbandingan produk: `sorotan_produk` (terlaris menurut omzet, terlaris menurut jumlah, harga jual per pcs termurah/termahal, termasuk seri), `produk_terlaris_qty`, `harga_per_pcs` + `peringkat_omzet`/`peringkat_qty` per produk, dan `fakta_produk` (kalimat fakta siap pakai sebagai dasar saran).
- Keluaran baru `rekap_chat`: rekap siap kirim di chat, teks biasa tanpa judul Markdown/tabel, satu rata-rata (per hari kalender, dasarnya disebut), terlaris menurut omzet **dan** jumlah. `ringkasan_siap_tempel` ikut menyebut produk yang paling banyak terjual. Konstanta `VERSI` dan opsi `--versi` ditambahkan.
- SKILL.md: bagian "Aturan saran (insight)": setiap saran wajib bersandar pada `fakta_produk`/angka script dan menyebut angkanya; kata pembanding hanya bila tertulis di `sorotan_produk`; tanpa angka pendukung → saran tidak ditulis; kata margin/laba/untung dilarang tanpa data modal/HPP (pakai "harga jual"). Format chat diganti (tanpa judul, tanpa tabel, satu rata-rata), plus contoh saran salah/benar dari kasus uji.
- Temuan verifikator independen putaran 1 (diperbaiki di versi yang sama, sebelum commit):
  - File **tanpa kolom jumlah** (mis. `Tanggal,Produk,Total`) masih ditulis "2 pcs", "× Rp X", harga per pcs termurah/termahal, dan "terlaris menurut jumlah", padahal tiap baris hanya dianggap 1 pcs. Kini script masuk mode "baris transaksi" (`satuan_jumlah_produk`): per produk ada `jumlah_baris`; `harga_per_pcs` dan `peringkat_qty` = null; `produk_terlaris_qty` dan `sorotan_produk.terlaris_qty` kosong; sisi kedua "paling laku" = `terlaris_baris` ("paling sering tercatat", satuan baris transaksi); `rekap_chat`, `ringkasan_siap_tempel`, dan `fakta_produk` tidak menyebut pcs/harga per pcs dan memuat catatan bahwa jumlah pcs tidak diketahui. Opsi baru `--satu-baris-satu-pcs` untuk dipakai **hanya** setelah pengguna memastikan 1 baris = 1 pcs (catatan "tiap baris dihitung 1 pcs" ikut tampil). Kolom `qty` per produk tetap berisi angka (jumlah baris) agar resep `laporan-otomatis-terjadwal` tidak rusak.
  - `rekap_chat` dengan satu status dihitung yang belum final (mis. semua "Sedang Dikirim") kini menulis "(belum final, bisa berubah bila batal/retur)".
  - Kalimat fakta terlaris seri tidak lagi memakai garis miring ("peringkat 1/3", "Rp 72.000/Rp 30.000"); tiap produk ditulis lengkap: "Kopi Susu Rp 72.000, peringkat 1 menurut omzet; Roti Bakar Rp 30.000, peringkat 3 menurut omzet; dari 3 produk".
  - Bila terlaris menurut jumlah sama dengan menurut omzet, `rekap_chat` menulis "Terlaris menurut jumlah juga X (N pcs)".
  - README: cuplikan "Contoh sebelum & sesudah" diganti dengan keluaran `rekap_chat` 1.2.6 (teks biasa, tanpa judul/tabel, satu rata-rata) pada data fiktif uji 17 Okt; bagian Syarat menyebut akibat file tanpa kolom jumlah.
  - SKILL.md: aturan "File tanpa kolom jumlah" (tidak menyebut pcs/harga per pcs; bila pengguna menanyakannya, tanya sekali apakah 1 baris = 1 pcs, lalu `--satu-baris-satu-pcs`).
- Uji regresi `scripts/uji_regresi.py` kini 27 tes, termasuk data fiktif yang dibuat ulang dengan angka agregat sama dengan uji 17 Okt (Selesai 66 / Rp 5.519.000, Batal 4 / Rp 238.000, Pengembalian Dana 2 / Rp 272.000), pembanding hitung independen untuk terlaris per jumlah, terlaris per omzet, dan harga per pcs termurah/termahal, kasus tanpa kolom jumlah (dengan dan tanpa `--satu-baris-satu-pcs`), status tunggal belum final, dan pencocokan cuplikan README dengan keluaran `rekap_chat`.
- Belum: contoh `examples/01`–`08` masih keluaran versi lama (format chat sebelum 1.2.6); uji ulang di OpenClaw/bot Telegram (dengan pra-cek `uji-tg.sh`) belum dijalankan.

## Catatan revisi 1.2.5 (2026-10-02)
- Revisi putaran 2 pada aturan promo di SKILL.md: pesan massal lewat fitur broadcast di dalam marketplace (mis. Shopee Chat Broadcast) ikut dilarang karena berisiko melanggar kebijakan platform. Yang masih boleh hanya promo resmi marketplace berbasis pengikut/opt-in yang dipakai manual oleh penjual, atau ajakan "ikuti toko" di kemasan/kartu ucapan.

## Catatan revisi 1.2.4 (2026-10-02)
- Temuan uji gabungan paket Toko Online: nilai pesanan "Sedang Dikirim" dan hari pembatalan dikira-kira oleh AI, bukan dihitung.
- Script kini mengeluarkan omzet & jumlah pesanan **per status** (selesai, dikirim, batal, dll.), tanggal pesanan yang batal/retur, dan blok **"RINGKASAN SIAP TEMPEL"** berisi kalimat lengkap untuk grup tim (tanpa nama/nomor pembeli).
- Aturan privasi baru: teks grup hanya angka agregat; daftar pelanggan untuk promo hanya yang sudah setuju (opt-in) — pembeli marketplace dianggap belum setuju; tanpa broadcast.
- Uji regresi `scripts/uji_regresi.py` kini 9 tes, termasuk pembanding hitung independen.

## Catatan revisi 1.2.3 (2026-10-01)
- Temuan uji OpenClaw: pertanyaan "hari paling rame" hanya dijawab dari sisi omzet.
- Rekap kini juga menampilkan hari dengan transaksi terbanyak (per pesanan unik lewat `--kolom-pesanan`, atau per baris). Ditambah uji regresi `scripts/uji_regresi.py` (4 tes).

## Catatan revisi 1.2.2 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.2.1 (2026-09-24)
- Versi saat skill pertama masuk repo (lolos uji muat OpenClaw). Perbaikan kecil; rincian di riwayat git.

## Catatan revisi 1.2.0 (sebelum 2026-09-24)
- Perbaikan dari uji kedua (v1.1.0 mendapat 6/10): status "Pengembalian Barang/Dana", "Belum Bayar", "Menunggu Pembayaran", "Dibatalkan Sistem", dan "Unpaid" tidak lagi dihitung sebagai omzet; daftar status yang ikut dihitung ditampilkan (`status_dihitung`).
- Angka yang meragukan (mis. `15.000.00`, `1.5E+06`, `1,50,000`) dilewati dan dilaporkan, tidak dihitung diam-diam. Nama produk yang hanya beda huruf besar/kecil atau spasi ("Kopi", "kopi ", "KOPI") digabung dan dilaporkan di `nama_produk_digabung`.

## Catatan revisi 1.1.0 (sebelum 2026-09-24)
- Revisi setelah uji pertama (v1.0.0 mendapat 5/10). Pada uji berikutnya masih mendapat 6/10 karena status pengembalian dan belum bayar dihitung sebagai omzet (diperbaiki di 1.2.0). Rincian lain di riwayat git.

## Catatan revisi 1.0.0 (sebelum 2026-09-24)
- Rilis awal (uji internal).
