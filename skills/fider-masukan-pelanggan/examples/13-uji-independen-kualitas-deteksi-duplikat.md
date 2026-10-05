# 13 - Kualitas deteksi duplikat

Penguji independen, Fider v0.38.0 ASLI (Docker+PostgreSQL 17), 2026-09-29. Data fiktif. Kunci tidak dicetak.

```
BUAT | Notifikasi WA saat pesanan dikirim | None
LEWATI | Notifikasi email saat pesanan dikirim | {'nomor': None, 'judul': 'Notifikasi WA saat pesanan dikirim', 'skor': 0.84}
LEWATI | Tambah pembayaran GoPay | {'nomor': 1, 'judul': 'Tambah pembayaran QRIS', 'skor': 0.72}
LEWATI | Tambah pembayaran ShopeePay | {'nomor': None, 'judul': 'Tambah pembayaran GoPay', 'skor': 0.79}
LEWATI | Tambah metode pembayaran QRIS | {'nomor': 1, 'judul': 'Tambah pembayaran QRIS', 'skor': 0.78}
BUAT | Bisa bayar QRIS | None
LEWATI | Kirim notifikasi WhatsApp kalau paket sudah dikirim | {'nomor': 2, 'judul': 'Notifikasi WA otomatis kalau paket sudah dikirim, minta 4 orang', 'skor': 0.69}
LEWATI | Tambah pembayaran QRIS | {'nomor': 1, 'judul': 'Tambah pembayaran QRIS', 'skor': 1.0}
```
