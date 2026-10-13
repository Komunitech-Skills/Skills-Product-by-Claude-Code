# Atribusi

## Jalur produksi
**Kreasi orisinal Komunitech.** Alur kerja, aturan prioritas, daftar tanda phishing, template, script, tes, dan semua contoh ditulis sendiri oleh Komunitech untuk pasar Indonesia (Rupiah, tagihan/invoice lokal, modus penipuan rekening dan transfer, WhatsApp/telepon sebagai jalur verifikasi).

## Sumber ide
Konsep umum "triase kotak masuk" dan tanda-tanda phishing yang dikenal luas dalam panduan keamanan publik. Tidak ada teks, contoh, template, atau kode dari proyek lain yang disalin. Tidak ada repositori yang di-clone dan tidak ada kode luar yang dijalankan.

## Audit keamanan (pedoman kurasi Komunitech)
`scripts/triase_email.py` (karya Komunitech) memakai pustaka standar saja (`argparse`, `csv`, `email`, `mailbox`, `re`, `json`, `datetime`, `decimal`, `pathlib`, `urllib.parse`); hanya membaca berkas yang diberikan pengguna, tidak membuka tautan, tidak ada akses jaringan, tidak ada `eval`/`exec`/`subprocess`, tidak menulis berkas kecuali `--keluar` yang diminta pengguna. Nama, perusahaan, alamat email, dan domain di `examples/` fiktif.

## Merek pihak ketiga
Nama bank, marketplace, dan kurir hanya disebut sebagai contoh penyamaran phishing. Tidak berafiliasi dengan merek mana pun.

## Riwayat versi
- 1.0.0 (2026-10-06): rilis awal (status uji).
