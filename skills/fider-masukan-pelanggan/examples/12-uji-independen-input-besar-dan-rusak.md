# 12 - Input besar dan rusak

Penguji independen, Fider v0.38.0 ASLI (Docker+PostgreSQL 17), 2026-09-29. Data fiktif. Kunci tidak dicetak.

```

posts sebelum: 4
$ impor besar60.txt
GALAT: Terlalu banyak butir (60); maksimum 50 per impor. Pecah berkasnya.
kode=2
$ impor besar50.txt (pratinjau, waktu)
      mirip dengan butir lain di berkas ini "Fitur juliet308841 khusus39" (kemiripan 80%)
Catatan: pos yang dibuat lewat kunci API otomatis mendapat 1 suara dari pemilik kunci.
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya.
real	0m0.127s
user	0m0.111s
$ impor judul-panjang.txt
RENCANA IMPOR dari judul-panjang.txt: 1 butir
1. [BUAT  ] Tolong tambahkan fitur yang sangat panjang sekali Tolong tambahkan fitur yang sangat panjang sekali…
      uraian: Tolong tambahkan fitur yang sangat panjang sekali Tolong tambahkan fitur yang sangat panj…
Catatan: pos yang dibuat lewat kunci API otomatis mendapat 1 suara dari pemilik kunci.

$ impor raksasa.txt (5.5MB)
RENCANA IMPOR dari raksasa.txt: 1 butir
1. [BUAT  ] Judul biasa
      uraian: kalimat panjang sekali kalimat panjang sekali kalimat panjang sekali kalimat panjang seka…
Catatan: pos yang dibuat lewat kunci API otomatis mendapat 1 suara dari pemilik kunci.
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya.
real	0m0.682s
user	0m0.614s
$ impor biner.txt
GALAT: Berkas biner.txt bukan teks UTF-8. Simpan ulang sebagai UTF-8.
kode=6
$ impor rusak.json
GALAT: JSON rusak di rusak.json: Expecting property name enclosed in double quotes: line 1 column 18 (char 17)
kode=6
$ impor salahbentuk.json
GALAT: JSON harus berupa daftar objek [{"judul":..., "uraian":..., "tag":[...]}].
kode=6
$ impor tanpajudul.json
GALAT: Butir ke-1 di JSON tidak punya 'judul'.
kode=6
$ impor pelanggan-aneh.json
GALAT: 'pelanggan' harus angka (butir: 'Tes jumlah aneh').
kode=6
$ impor inflasi.json (pratinjau)
RENCANA IMPOR dari inflasi.json: 1 butir
1. [BUAT  ] Usulan uji inflasi
      uraian: Dilaporkan oleh sekitar 9.999 pelanggan.
Catatan: pos yang dibuat lewat kunci API otomatis mendapat 1 suara dari pemilik kunci.
$ komentar 5001 huruf
GALAT: Komentar terlalu panjang (maks. 5.000 karakter).
kode=2
posts sesudah: 4
```
