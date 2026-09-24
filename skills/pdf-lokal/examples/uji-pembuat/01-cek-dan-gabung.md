# Contoh 1 (normal): cek server lalu gabung PDF

Diuji ke Stirling-PDF v2.14.3 sungguhan (Docker, `ghcr.io/stirling-tools/stirling-pdf:latest`).

```
$ python3 scripts/pdf.py cek
Stirling-PDF HIDUP di http://localhost:8080
  Versi  : 2.14.3
  Status : UP
Siap dipakai. Coba: python3 pdf.py gabung file1.pdf file2.pdf

$ python3 scripts/pdf.py gabung resi1.pdf resi2.pdf
Berhasil digabung (2 file) -> /.../uji/resi1-gabungan.pdf
```

`resi1-gabungan.pdf` yang dihasilkan adalah PDF 2 halaman valid (diverifikasi dengan
`file resi1-gabungan.pdf` -> `PDF document, version 1.4, 2 page(s)`).
