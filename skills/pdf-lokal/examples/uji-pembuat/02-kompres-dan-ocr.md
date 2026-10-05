# Contoh 2 (normal): kompres PDF & OCR dengan fallback bahasa

Diuji ke Stirling-PDF v2.14.3 sungguhan.

```
$ python3 scripts/pdf.py kompres multi4.pdf --level 6
Berhasil dikompres: 1 KB -> 1 KB
  -> /.../uji/multi4-kompres.pdf
```
(File uji sengaja sangat kecil untuk verifikasi jalur API, bukan mengukur rasio kompresi.)

```
$ python3 scripts/pdf.py ocr resi1.pdf --keluaran resi1-ocr2.pdf
Catatan: bahasa ind belum terpasang di Stirling-PDF-mu, OCR hanya memakai: eng. Untuk
memasang bahasa Indonesia: buka aplikasi Stirling-PDF > menu OCR > unduh paket bahasa
'ind' (lihat docs/panduan-stirling-pdf.md).
Berhasil OCR (PDF sekarang bisa dicari/di-copy teksnya) -> /.../uji/resi1-ocr2.pdf
```

Temuan penting: instalasi default Stirling-PDF (Docker) **tidak menyertakan bahasa
Indonesia** untuk OCR (hanya eng/fra/deu/chi_sim/por). Script mendeteksi ini lewat
`/api/v1/ui-data/ocr-pdf` sebelum memproses, dan memberi tahu pengguna secara jujur -
bukan diam-diam memakai bahasa Inggris.
