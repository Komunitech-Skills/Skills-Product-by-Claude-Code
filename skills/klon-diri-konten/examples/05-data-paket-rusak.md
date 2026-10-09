# Contoh 5 - Tabel paket rusak

Input `paket.json` berisi `harga_bulanan: "abc"` atau `batas_bulanan: 0`.
Keluaran script: `GALAT: paket 'X': 'harga_bulanan' bukan angka: 'abc'` (kode keluar 2). Respons skill: minta pengguna memeriksa halaman harga resmi dan mengisi ulang angka; tidak menebak harga.
