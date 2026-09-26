# Skenario 02 (normal) — Rapikan 8 resi Shopee/TikTok jadi 4 per lembar A4

**Permintaan pengguna (simulasi):** "Resi Shopee & TikTok-ku hari ini ada 8, mau diprint
hemat kertas, 4 per lembar ya."

**Lingkungan:** Stirling-PDF v2.14.3 asli via Docker (sama seperti skenario 01).
Data: 8 PDF resi satu-halaman dibuat sendiri (`resi-01.pdf` ... `resi-08.pdf`), berselang-seling
toko Shopee/TikTok Shop, nomor resi & alamat fiktif.

## Perintah
```
$ python3 scripts/pdf.py rapikan-resi bahan/resi-*.pdf --per-lembar 4 --keluaran hasil/resi-rapi.pdf
Berhasil disusun 4 resi per lembar (8 file sumber) -> /tmp/.../hasil/resi-rapi.pdf
Catatan: cek dulu di Print Preview sebelum cetak massal - Stirling-PDF menyusun ukuran
lembar otomatis berdasarkan ukuran halaman asli, bukan dipaksa persis A4/A6.
```

## Verifikasi independen
| Cek | Alat | Hasil |
|---|---|---|
| Jumlah halaman hasil | `pdfinfo` | **2 halaman** (8 resi ÷ 4/lembar = 2, benar) |
| Ukuran kertas | `pdfinfo` | **595×842 pt = A4** (kebetulan cocok karena resi sumber dibuat di A4; skill sudah benar mengingatkan ini **tidak dijamin** untuk resi asli marketplace yang biasanya berukuran thermal 10×15/10×20 cm) |
| Isi & urutan | `pdftotext` + render `pdftoppm` (lihat cuplikan gambar di sesi uji) | 4 resi per halaman tersusun rapi 2×2, urutan sesuai urutan file diketik (resi 1–4 di halaman 1, resi 5–8 di halaman 2), tidak ada teks terpotong/tertumpuk |
| File resi asli (8 file) sha256 sebelum vs sesudah | `sha256sum` | **Identik** — tidak ada penimpaan |
| Path hasil | manual | Path lengkap benar & bisa dibuka |

## Catatan penting untuk pembeli awam
Peringatan bawaan skill ("cek Print Preview dulu... ukuran lembar bukan dipaksa A4/A6")
**akurat dan penting**: resi marketplace asli sering berukuran thermal kecil (10×15 cm),
bukan A4 seperti data uji kami. Kalau pengguna memasukkan 8 resi thermal asli, hasil
`multi-page-layout` bisa jadi mengikuti ukuran kertas thermal tsb (bukan otomatis jadi A4
biasa), jadi peringatan di README/SKILL.md sudah tepat dan sebaiknya **dipertegas** dengan
contoh konkret "kalau resi kamu ukuran kecil/thermal, cetak percobaan 1 lembar dulu" —
lihat catatan **R1** di `HASIL-UJI.md`.

## Kesimpulan
Fitur unggulan (dan paling relevan untuk pasar Indonesia) ini bekerja benar untuk kasus
normal: jumlah halaman tepat, urutan benar, file asli aman. Nilai tambah dibanding fitur
generik "N-up" pesaing (lihat `00-banding-pesaing.md`) adalah kontekstualisasi eksplisit
untuk resi Shopee/TikTok, bukan cuma "N-up PDF" generik.
