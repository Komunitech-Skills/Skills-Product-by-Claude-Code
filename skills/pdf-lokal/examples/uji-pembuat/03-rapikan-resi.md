# Contoh 3 (normal): rapikan beberapa resi jadi 1 lembar

Diuji ke Stirling-PDF v2.14.3 sungguhan, dengan 3 file "resi" (PDF 1 halaman) berbeda.

```
$ python3 scripts/pdf.py rapikan-resi resi1.pdf resi2.pdf multi4.pdf --per-lembar 4
Berhasil disusun 4 resi per lembar (3 file sumber) -> /.../uji/resi-rapi-4-per-lembar.pdf
Catatan: cek dulu di Print Preview sebelum cetak massal - Stirling-PDF menyusun ukuran
lembar otomatis berdasarkan ukuran halaman asli, bukan dipaksa persis A4/A6.
```

Di balik layar, script memanggil 2 endpoint berurutan:
1. `POST /api/v1/general/merge-pdfs` - gabungkan 3 file resi jadi 1 PDF multi-halaman.
2. `POST /api/v1/general/multi-page-layout` (`pagesPerSheet=4`) - susun 4 halaman per
   lembar.

File sementara hasil langkah 1 dihapus otomatis setelah langkah 2 selesai.
