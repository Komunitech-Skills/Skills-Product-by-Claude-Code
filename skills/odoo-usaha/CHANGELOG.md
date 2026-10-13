# Riwayat perubahan — odoo-usaha

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
- **1.0.2 (30 Sep 2026)** — panduan §5: sisa saran hak akses versi lama (Billing/Own Documents) dihapus; hanya satu tabel hak akses.
- **1.0.1 (30 Sep 2026)** — perbaikan dari uji ke Odoo Community 18 & 19 asli: (1) hak *Own Documents* tidak lagi menghasilkan angka penjualan/faktur kecil (bisa Rp 0) diam-diam — `cek` menampilkan cakupan data, laporan memberi **PERINGATAN DATA SEBAGIAN** + kode 9 (`--terima-sebagian` bila memang disengaja); (2) `piutang --per-tanggal` di masa lalu tidak lagi memasukkan faktur yang belum terbit dan memperhitungkan pelunasan setelah tanggal itu; (3) panduan hak pengguna diperbaiki secara jujur (Odoo tidak punya peran Penjualan baca-saja; pengaman tulis ada di script); (4) keterangan "barang masuk terjadwal" di stok menipis; (5) ENV `ODOO_HOST_DIIZINKAN` dihapus (host hanya lewat `atur --izinkan-host`).
- **1.0.0 (30 Sep 2026)** — rilis awal.
