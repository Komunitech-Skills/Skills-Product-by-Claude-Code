# 14 - Gerbang tulis --ya

Penguji independen, Fider v0.38.0 ASLI (Docker+PostgreSQL 17), 2026-09-29. Data fiktif. Kunci tidak dicetak.

```

$ impor wa1-bersih.txt --tetap
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ impor mirip.txt --tetap --hapus-suara-saya
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ tag 3 pembayaran
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ tag 1 pembayaran --lepas
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ tag-buat Baru
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ gabung 5 3
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ status 5 ditolak --catatan x
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ komentar 3 --teks halo
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ --ya nilai palsu: --ya=false / --YA / --no-ya / -ya
$ status 5 ditolak --ya=false
fider.py status: error: argument --ya: ignored explicit argument 'false'
$ status 5 ditolak --YA
fider.py: error: unrecognized arguments: --YA
$ status 5 ditolak --no-ya
fider.py: error: unrecognized arguments: --no-ya
$ status 5 ditolak -ya
fider.py: error: unrecognized arguments: -ya
$ FIDER_YA=1 / YES=1 env
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
$ --json tanpa --ya
{
  "pratinjau": true,
  "nomor": 5,
$ pipa: yes | status
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang 
TIDAK BERUBAH (gerbang utuh) untuk semua perintah di atas
--- catatan: 'status 5 ditolak --y' (singkatan argparse) MENULIS (terbukti) -> bypass
```
