# Riwayat perubahan — frappe-books-usaha

Catatan teknis per versi.

## Catatan revisi 1.0.10 (2026-10-02)
- Aturan baru di SKILL.md: bila pengguna menempel kunci/token/password di chat, agent tidak boleh menulis ulang satu karakter pun darinya dan cukup menyebut "kunci yang Anda tempel".

## Catatan revisi 1.0.9 (2026-10-02)
- Temuan uji OpenClaw: status PKP (Pengusaha Kena Pajak) kini ditanyakan lebih dulu sebelum menghitung PPN apa pun (`ppn`, `ppn-periode`, atau PPN per nota). Usaha yang belum PKP tidak dihitung PPN setornya dan diberi penjelasan.
- Panduan menghapus nota batal diberi catatan bahwa ia berdasarkan kode sumber v0.36 dan belum dicoba langsung di aplikasi.

## Catatan revisi 1.0.8 (2026-10-02)
- Perintah baru `ppn-periode`: PPN keluaran, PPN masukan, dan selisih (kurang/lebih bayar) satu periode langsung dari data. Pemicu diperjelas: "PPN yang harus saya setor bulan ini" memakai `ppn-periode`, sedangkan "hitung PPN harga ini" memakai `ppn`.
- Panduan merapikan draf dan invoice batal (jangan hapus lewat database; hapus lewat menu aplikasi atau biarkan sebagai jejak). Uji regresi menjadi 51 tes.

## Catatan revisi 1.0.7 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.6 (2026-09-30)
- Format angka Indonesia diperbaiki: jumlah barang "1.500" dan "38.000" tidak lagi terbaca 1,5 dan 38 secara diam-diam. Format `1.500`, `1.250.000`, `1.500,5`, `1,5`, dan `2.5` dibaca benar; bentuk ambigu seperti "1,500" ditolak dengan pesan jelas. Ditambah uji regresi.

## Catatan revisi 1.0.5 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.4 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.
- Uji ulang independen v1.0.3 di aplikasi Frappe Books asli: 9/10, dua siklus cocok dengan P&L, General Ledger, dan Stock Balance Frappe.

## Catatan revisi 1.0.3 (2026-09-26)
- Laba rugi dihitung dari buku besar (ledger) sehingga angkanya sama dengan laporan Profit And Loss Frappe Books (retur dan retur pengiriman diperhitungkan). Diverifikasi di Frappe Books v0.36.0 asli oleh pembuat.

## Catatan revisi 1.0.2 (2026-09-26)
- Akun pembelian untuk barang berstok diperbaiki (tidak lagi memicu HPP ganda) dan piutang dihitung netto setelah retur. Diverifikasi di Frappe Books v0.36.0 asli lewat Import Wizard, termasuk alur beli, terima, jual, kirim, dan retur.

## Catatan revisi 1.0.1 (2026-09-26)
- Revisi atas temuan uji pertama (5/10) yang dijalankan pada file Frappe Books asli: jalur impor CSV transaksi ditolak Import Wizard, akun penjualan/utang otomatis salah pada bagan akun Indonesia, dan `--keluar` bisa menimpa file database. Rincian perbaikan ada di riwayat git.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): asisten Frappe Books (akuntansi desktop gratis, offline). Membaca file `.books.db` secara hanya-baca untuk laporan penjualan/pembelian, piutang dan utang jatuh tempo, stok menipis, laba rugi ringkas, dan laporan harian ke Telegram; menyiapkan CSV impor pelanggan, barang, dan nota; menghitung PPN 12% dengan DPP 11/12.
