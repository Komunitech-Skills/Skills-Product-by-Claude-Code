# Riwayat perubahan — rekap-penjualan-csv

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.2.3 (2026-10-01)
- Temuan uji OpenClaw: pertanyaan "hari paling rame" hanya dijawab dari sisi omzet.
- Rekap kini juga menampilkan hari dengan transaksi terbanyak (per pesanan unik lewat `--kolom-pesanan`, atau per baris). Ditambah uji regresi `scripts/uji_regresi.py` (4 tes).

## Catatan revisi 1.2.4 (2026-10-02)
- Temuan uji gabungan paket Toko Online: nilai pesanan "Sedang Dikirim" dan hari pembatalan dikira-kira oleh AI, bukan dihitung.
- Script kini mengeluarkan omzet & jumlah pesanan **per status** (selesai, dikirim, batal, dll.), tanggal pesanan yang batal/retur, dan blok **"RINGKASAN SIAP TEMPEL"** berisi kalimat lengkap untuk grup tim (tanpa nama/nomor pembeli).
- Aturan privasi baru: teks grup hanya angka agregat; daftar pelanggan untuk promo hanya yang sudah setuju (opt-in) — pembeli marketplace dianggap belum setuju; tanpa broadcast.
- Uji regresi `scripts/uji_regresi.py` kini 9 tes, termasuk pembanding hitung independen.
