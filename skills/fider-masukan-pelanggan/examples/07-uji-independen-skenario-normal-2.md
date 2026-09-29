# 07 - Skenario normal 2: tag dan gabung duplikat

Penguji independen, Fider v0.38.0 ASLI (Docker+PostgreSQL 17), 2026-09-29. Data fiktif. Kunci tidak dicetak.

```
$ tag 1 pembayaran
Akan MEMASANG tag pembayaran pada pos #1 "Tambah pembayaran QRIS" (tag saat ini: -).

PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya.
$ tag 1 pembayaran --ya
SELESAI: tag pembayaran dipasang pada pos #1.
$ tag 4 pembayaran --ya
SELESAI: tag pembayaran dipasang pada pos #4.
$ tag 5 pengiriman,tidakada
GALAT: Tag belum ada: tidakada. Buat dulu: tag-buat "tidakada" --ya (butuh Administrator). Daftar tag: tag-daftar.
kode=2
$ tag 5 Pengiriman --ya
SELESAI: tag pengiriman dipasang pada pos #5.
$ cari qris
#1        0 suara    0 komentar  [Terbuka]  Tambah pembayaran QRIS  (tag: pembayaran)
#4        1 suara    0 komentar  [Terbuka]  Bayar pakai QRIS dong  (tag: pembayaran)
$ gabung 4 1
Akan menandai pos #4 "Bayar pakai QRIS dong" (1 suara) sebagai DUPLIKAT dari #1 "Tambah pembayaran QRIS" (0 suara).
Pos duplikat hilang dari daftar utama dan suaranya dipindahkan ke pos induk oleh Fider.

PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya.
$ gabung 4 1 --ya
SELESAI: #4 digabung ke #1. Suara #1 sekarang 1.
$ gabung 4 1 --ya (ulang)
Pos #4 sudah berstatus duplikat; tidak ada yang diubah.
$ gabung 1 4 (induk duplikat)
GALAT: Pos #4 sendiri sudah berstatus duplikat. Pilih pos induk yang lain.
kode=2
$ gabung 1 1
GALAT: Pos tidak bisa digabung ke dirinya sendiri.
kode=2
$ lihat 1
POS #1: Tambah pembayaran QRIS
Status : Terbuka    Suara: 1    Komentar: 0    Dibuat: 29 Sep 2026
Tag    : pembayaran
Uraian : Sumber: WhatsApp pelanggan.
$ daftar
#1        1 suara    0 komentar  [Terbuka]  Tambah pembayaran QRIS  (tag: pembayaran)
#2        1 suara    0 komentar  [Terbuka]  Notifikasi WA otomatis kalau paket sudah dikirim, minta 4 orang  (tag: -)
#3        0 suara    0 komentar  [Terbuka]  Cetak resi langsung dari halaman pesanan  (tag: -)
#5        0 suara    0 komentar  [Terbuka]  Ongkir ke Papua sering salah hitung  (tag: pengiriman)
```
