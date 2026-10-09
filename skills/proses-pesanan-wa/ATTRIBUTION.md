# Atribusi

## Jalur produksi
**Kreasi orisinal Komunitech.** Alur kerja, aturan hitung, template pesan/nota/label, script, tes, dan semua contoh ditulis sendiri oleh Komunitech untuk toko Indonesia yang berjualan lewat WhatsApp/DM (Rupiah, kurir lokal, COD, transfer bank/QRIS).

## Sumber ide
Praktik umum pengelolaan pesanan toko online (rekap order, konfirmasi, label, serah-terima kurir). Tidak ada teks, contoh, template, atau kode dari proyek lain yang disalin. Tidak ada repositori yang di-clone dan tidak ada kode luar yang dijalankan.

## Audit keamanan (Tahap 3 CLAUDE.md)
`scripts/rekap_pesanan.py` (karya Komunitech) memakai pustaka standar saja (`argparse`, `csv`, `io`, `json`, `re`, `sys`, `datetime`, `decimal`, `pathlib`); hanya membaca file pesanan & katalog yang diberikan, tanpa akses jaringan, tanpa `eval`/`exec`/`subprocess`, dan tidak menulis file. Semua nama, nomor HP, dan alamat di tes dan dokumentasi fiktif.

## Merek pihak ketiga
JNE, J&T, SiCepat, AnterAja, Pos Indonesia, GoSend, GrabExpress, WhatsApp, dan nama bank hanya disebut sebagai penyebut layanan. Tidak berafiliasi dengan merek mana pun.

## Lisensi
Proprietary Komunitech; tunduk pada `LISENSI.txt` di paket pembelian.

## Riwayat versi
- 1.0.0 (2026-10-06): rilis awal (draft).
