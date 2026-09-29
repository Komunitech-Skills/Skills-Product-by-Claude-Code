# 08 - Skenario normal 3: status, ringkasan mingguan, draf balasan (admin dan Collaborator)

Penguji independen, Fider v0.38.0 ASLI (Docker+PostgreSQL 17), 2026-09-29. Data fiktif. Kunci tidak dicetak.

```
$ status 2 dikerjakan (pratinjau)
Akan mengubah status pos #2 "Notifikasi WA otomatis kalau paket sudah dikirim, minta 4 orang": Terbuka -> Sedang dikerjakan.
Teks tanggapan publik: "Mulai kami kerjakan bulan ini"

PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya.
$ status 2 dikerjakan --ya
SELESAI: pos #2 sekarang "Sedang dikerjakan".
$ status 3 selesai --ya (collab)
SELESAI: pos #3 sekarang "Selesai".
Untuk balasan ke pelanggan: draf-balasan 3
$ status 5 macet
GALAT: Status 'macet' tidak dikenal. Pilihan: terbuka, rencana, dikerjakan, selesai, ditolak. (Untuk duplikat pakai perintah gabung.) Fider diam-diam menganggap status asing sebagai 'terbuka', jadi script menolaknya di sini.
kode=2
$ status 5 duplicate
GALAT: Status 'duplicate' tidak dikenal. Pilihan: terbuka, rencana, dikerjakan, selesai, ditolak. (Untuk duplikat pakai perintah gabung.) Fider diam-diam menganggap status asing sebagai 'terbuka', jadi script menolaknya di sini.
kode=2
$ ringkasan-mingguan (admin)
RINGKASAN MASUKAN PELANGGAN - 7 hari terakhir (per 29 Sep 2026)
- Pos aktif (terbuka/direncanakan/dikerjakan): 3, total 5 suara
- Pos baru minggu ini: 4
- Ditandai selesai minggu ini: 1

TOP 3 SUARA TERBANYAK
1. #1 Tambah pembayaran QRIS - 2 suara  (+2 minggu ini) [Terbuka]
2. #2 Notifikasi WA otomatis kalau paket sudah dikirim, minta 4 orang - 2 suara  (+2 minggu ini) [Sedang dikerjakan]
3. #5 Ongkir ke Papua sering salah hitung - 1 suara  (+1 minggu ini) [Terbuka]

POS BARU
- #5 Ongkir ke Papua sering salah hitung (1 suara)
- #3 Cetak resi langsung dari halaman pesanan (1 suara)
- #2 Notifikasi WA otomatis kalau paket sudah dikirim, minta 4 orang (2 suara)
- #1 Tambah pembayaran QRIS (2 suara)

BARU SELESAI
- #3 Cetak resi langsung dari halaman pesanan

Catatan: angka dari Fider apa adanya; suara pemilik/tim ikut terhitung.
$ ringkasan-mingguan (collab)
RINGKASAN MASUKAN PELANGGAN - 7 hari terakhir (per 29 Sep 2026)
- Pos aktif (terbuka/direncanakan/dikerjakan): 3, total 5 suara
- Pos baru minggu ini: 4
- Ditandai selesai minggu ini: 1

TOP 3 SUARA TERBANYAK
1. #1 Tambah pembayaran QRIS - 2 suara  (+2 minggu ini) [Terbuka]
2. #2 Notifikasi WA otomatis kalau paket sudah dikirim, minta 4 orang - 2 suara  (+2 minggu ini) [Sedang dikerjakan]
3. #5 Ongkir ke Papua sering salah hitung - 1 suara  (+1 minggu ini) [Terbuka]

POS BARU
- #5 Ongkir ke Papua sering salah hitung (1 suara)
- #3 Cetak resi langsung dari halaman pesanan (1 suara)
- #2 Notifikasi WA otomatis kalau paket sudah dikirim, minta 4 orang (2 suara)
- #1 Tambah pembayaran QRIS (2 suara)

BARU SELESAI
- #3 Cetak resi langsung dari halaman pesanan

Catatan: angka dari Fider apa adanya; suara pemilik/tim ikut terhitung.
$ draf-balasan 3
DRAF BALASAN untuk pos #3 (belum dikirim ke siapa pun; pemilik yang mengirim/menempel):
------------------------------
Halo Kak, kabar baik!
Usulan "Cetak resi langsung dari halaman pesanan" sekarang sudah kami kerjakan dan bisa dipakai.
Sekarang ada di menu Pesanan
Terima kasih sudah ikut memberi masukan. Kalau masih ada yang kurang pas, kabari kami ya.
------------------------------
Untuk menempelkannya sebagai komentar publik di Fider: komentar 3 --teks "..." --ya
$ draf-balasan 2 (belum selesai)
PERINGATAN: pos #2 berstatus "Sedang dikerjakan", belum "Selesai". Pastikan perbaikannya benar-benar sudah jalan sebelum draf ini dikirim.

DRAF BALASAN untuk pos #2 (belum dikirim ke siapa pun; pemilik yang mengirim/menempel):
------------------------------
Selamat siang,
Kami informasikan bahwa usulan "Notifikasi WA otomatis kalau paket sudah dikirim, minta 4 orang" telah selesai kami perbaiki/tambahkan.
Usulan ini didukung 2 orang, terima kasih untuk semuanya.
Terima kasih atas masukan Anda. Jika masih ada kendala, silakan sampaikan kembali kepada kami.
------------------------------
Untuk menempelkannya sebagai komentar publik di Fider: komentar 2 --teks "..." --ya
$ komentar 3 pratinjau
Akan menulis komentar PUBLIK pada pos #3 "Cetak resi langsung dari halaman pesanan" atas nama akun pemilik kunci:
---
Sudah bisa dipakai, hubungi [nomor disembunyikan]
---
(1 nomor HP/email disembunyikan.)

PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya.
```
