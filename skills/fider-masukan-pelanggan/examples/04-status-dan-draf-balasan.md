# 04 - Ubah status & draf "sudah kami perbaiki" (Fider v0.38.0 asli)

```
$ status 5 selesai --catatan "Rumus ongkir sudah diperbaiki" --ya
SELESAI: pos #5 sekarang "Selesai".
Untuk balasan ke pelanggan: draf-balasan 5

$ status 5 bogus
GALAT: Status 'bogus' tidak dikenal. Pilihan: terbuka, rencana, dikerjakan, selesai, ditolak. ... (kode keluar 2; Fider asli diam-diam menjadikannya "terbuka")

$ draf-balasan 5 --catatan "Rumus ongkir luar Jawa sudah kami perbaiki."
DRAF BALASAN untuk pos #5 (belum dikirim ke siapa pun; pemilik yang mengirim/menempel):
------------------------------
Selamat siang,
Kami informasikan bahwa usulan "Ongkir ke luar Jawa sering salah hitung. Kontak: [email disembunyikan]" telah selesai kami perbaiki/tambahkan.
Rumus ongkir luar Jawa sudah kami perbaiki.
Terima kasih atas masukan Anda. Jika masih ada kendala, silakan sampaikan kembali kepada kami.
------------------------------
Untuk menempelkannya sebagai komentar publik di Fider: komentar 5 --teks "..." --ya
```

Draf tidak dikirim ke siapa pun; pemilik yang menempelkannya ke WA/email pelanggan. Judul pos di contoh ini memuat sisa teks uji ("Kontak: [email disembunyikan]"); pada pemakaian nyata judul sebaiknya dirapikan dulu di pratinjau impor.
