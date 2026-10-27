# 02 - Tag dan gabung duplikat (Fider v0.38.0 asli)

> **FORMAT LAMA (sebelum v1.0.10), direkam apa adanya:** judul pos #3 masih memuat nama "Bu Rina". Sekarang nama berpola sapaan disamarkan dan agent menulis "seorang pelanggan". Jangan ditiru.

```
$ tag-buat "Pengiriman" --ya
Tag dibuat: Pengiriman (slug: pengiriman)
$ tag 3 pengiriman --ya
SELESAI: tag pengiriman dipasang pada pos #3.
$ tag 3 fitur                       # tag belum ada
GALAT: Tag belum ada: fitur. Buat dulu: tag-buat "fitur" --ya (butuh Administrator). Daftar tag: tag-daftar.
$ gabung 3 1                        # tanpa --ya
Akan menandai pos #3 "Pelanggan minta bisa bayar pakai QRIS (Bu Rina [nomor disembunyikan])" (0 suara) sebagai DUPLIKAT dari #1 "Tambah pembayaran QRIS" (1 suara).
Pos duplikat hilang dari daftar utama dan suaranya dipindahkan ke pos induk oleh Fider.

PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya.
$ gabung 3 1 --ya
SELESAI: #3 digabung ke #1. Suara #1 sekarang 1.
$ gabung 3 1 --ya                   # diulang
Pos #3 sudah berstatus duplikat; tidak ada yang diubah.
```
