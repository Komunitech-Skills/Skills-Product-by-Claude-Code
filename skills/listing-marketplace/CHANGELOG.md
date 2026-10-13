# Riwayat perubahan — listing-marketplace

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.4 (2026-10-01)
- Temuan uji ulang OpenClaw: panjang deskripsi yang dilaporkan (505) beda dengan teks yang ditampilkan (515).
- Kini angka panjang wajib diambil dari run script terakhir pada teks final yang persis sama dengan yang ditampilkan.

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw: AI sempat menambah klaim "ga gampang buyar" yang tidak disebut pemilik, dan cek otomatis tetap lulus.
- Aturan baru: setiap sifat/klaim produk harus berasal dari kata-kata pemilik. Script `cek_listing.py` kini menerima `--fakta`/`--fakta-file` dan menandai GAGAL frasa sifat/layanan ("awet", "anti …", "tidak mudah …", "dikirim cepat", "packing aman") yang tidak ada di fakta. Ditambah 4 uji regresi.
