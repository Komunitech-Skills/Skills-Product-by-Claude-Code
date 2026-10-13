# Riwayat perubahan — rekap-penjualan-csv

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

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
