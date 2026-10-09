# 09 - Skenario input tidak lengkap

Penguji independen, Fider v0.38.0 ASLI (Docker+PostgreSQL 17), 2026-09-29. Data fiktif. Kunci tidak dicetak.

```

$ impor (tanpa berkas)
usage: fider.py impor [-h] [--url URL] [--kunci-file KUNCI_FILE] [--json]
                      [--ya] [--sumber SUMBER] [--tetap] [--hapus-suara-saya]
                      [--jeda JEDA]
                      berkas
fider.py impor: error: the following arguments are required: berkas
kode=2
$ impor tidak-ada.txt
GALAT: Tidak bisa membaca berkas catatan tidak-ada.txt: No such file or directory
kode=6
$ impor kosong.txt
GALAT: Berkas kosong.txt kosong.
kode=6
$ impor hampa.txt (hanya butir kosong)
RENCANA IMPOR dari hampa.txt: 1 butir
1. [BUAT  ] -
      uraian: -
Catatan: pos yang dibuat lewat kunci API otomatis mendapat 1 suara dari pemilik kunci.

PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya.
kode=0
$ status 3 (tanpa nama status)
usage: fider.py status [-h] [--url URL] [--kunci-file KUNCI_FILE] [--json]
                       [--ya] [--catatan CATATAN]
                       nomor status
fider.py status: error: the following arguments are required: status
kode=2
$ gabung 3
usage: fider.py gabung [-h] [--url URL] [--kunci-file KUNCI_FILE] [--json]
                       [--ya] [--catatan CATATAN]
                       duplikat asli
fider.py gabung: error: the following arguments are required: asli
kode=2
$ tag 3
usage: fider.py tag [-h] [--url URL] [--kunci-file KUNCI_FILE] [--json] [--ya]
                    [--lepas]
                    nomor nama
fider.py tag: error: the following arguments are required: nama
kode=2
$ lihat abc
GALAT: Nomor pos tidak valid: 'abc' (contoh: 12).
kode=2
$ lihat "1; DROP"
GALAT: Nomor pos tidak valid: '../admin' (contoh: 12).
kode=2
$ status 999 selesai
GALAT: Tidak ditemukan (/api/v1/posts/999). Nomor pos/tag salah?
kode=2
$ daftar --status ngawur
GALAT: Status 'ngawur' tidak dikenal. Pilihan: terbuka, rencana, dikerjakan, selesai, ditolak.
kode=2
$ ringkasan-mingguan --hari 0
GALAT: --batas/--hari/--top minimal 1.
kode=2
$ komentar 3 --teks ""
GALAT: Teks komentar kosong.
kode=2
```
