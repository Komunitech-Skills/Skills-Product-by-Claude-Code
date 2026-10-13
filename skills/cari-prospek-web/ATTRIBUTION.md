# Atribusi

## Jalur produksi
**Kreasi orisinal Komunitech.** Alur kerja, aturan bukti, daftar sumber publik, template, script, dan tes ditulis sendiri oleh Komunitech untuk pasar Indonesia. Tidak ada teks, contoh, atau kode dari proyek lain yang disalin. Lisensi: Proprietary Komunitech, tunduk pada `LISENSI.txt` di paket.

## Audit keamanan (pedoman kurasi Komunitech)
`scripts/saring_prospek.py` memakai pustaka standar saja (`argparse`, `csv`, `io`, `re`, `sys`, `difflib`, `urllib.parse`); hanya membaca berkas yang diberikan pengguna, tidak ada akses jaringan, tidak ada `eval`/`exec`/`subprocess`, menulis berkas hanya lewat `--keluar` yang diminta pengguna. Semua nama usaha, domain (`.example`), dan nomor di tes dan contoh adalah fiktif.

## Merek pihak ketiga
Nama platform dan marketplace (Google Maps, LinkedIn, Instagram, Indotrading, Indonetwork, dll.) hanya disebut sebagai contoh sumber atau padanan. Tidak berafiliasi dengan merek mana pun.

## Riwayat versi
- 1.0.0 (2026-10-06): rilis awal (status uji).
