# Atribusi

## Jalur produksi
**Karya orisinal Komunitech** (tulis ulang bersih). Alur kerja, daftar periksa, template, script, tes, dan semua contoh ditulis sendiri untuk pasar Indonesia (Rupiah, NIB, notaris/PPAT, konsultan pajak, usaha warung/kafe/bengkel/toko online).

## Sumber ide
Ide umum tentang perencanaan penjualan dan suksesi usaha kecil yang terinspirasi materi publik pemerintah Amerika Serikat (FDIC Money Smart for Small Business, hanya ringkasan tema pada halaman indeks). Tidak ada teks, struktur, contoh, atau gambar yang disalin; agen pembuat tidak membaca sumber aslinya, hanya daftar ide. Catatan asal ide ada di `research/sources/` repo kurator. Tidak ada klaim "berbasis" atau berafiliasi dengan penerbit sumber.

## Audit keamanan
`scripts/nilai_usaha.py` hanya memakai pustaka standar (`argparse`, `json`, `decimal`, `sys`), tanpa jaringan, tanpa membaca atau menulis berkas, tanpa `eval`/`exec`/`subprocess`. Semua data contoh fiktif.

## Lisensi
Tunduk pada `LISENSI.txt` dalam paket pembelian. Bukan nasihat hukum, pajak, atau penilaian resmi.

## Riwayat versi
- 1.0.0 (2026-10-09): rilis awal (status uji).
- 1.0.1 (2026-10-10): perbaikan dari uji isi agent 2026-10-09 (biaya sekali per tahun, utang konsisten, porsi sekutu, dasar aturan di `references/dasar-aturan.md`). Rujukan aturan ditulis sendiri dari situs instansi/ulasan publik, tidak disalin.
