# Rekap Penjualan Otomatis dari File Kasir

**Kirim file penjualan, dapat laporan omzet dan produk terlaris tanpa rekap manual.**

*Diuji AI penguji independen di OpenClaw: 7,5 → 9 dari 10 (angka sama-sama benar; dengan skill laporan lebih lengkap: persentase tiap produk, rata-rata harian, dan saran yang bisa dijalankan).*

*Jujur soal uji terakhir: pada uji di bot Telegram 17 Okt 2026 (versi 1.2.5), skill ini belum lulus, karena ada kalimat saran yang salah. Versi 1.2.6 dan 1.2.7 memperbaikinya, tetapi versi 1.2.7 belum diuji ulang di bot asli.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Total omzet, rata-rata harian, dan 5 produk terlaris
- ✅ Hari terbaik dan hari terendah terlihat jelas
- ✅ Angka dihitung dengan script, bukan dikira-kira
- ✅ Membaca format Indonesia: `Rp 15.000`, `15.000,50`, dan pemisah titik koma (`;`) seperti file Excel berbahasa Indonesia
- ✅ Produk terlaris dari dua sisi (omzet dan jumlah terjual), plus harga jual per pcs bila file punya kolom jumlah
- ✅ Saran yang bisa langsung dijalankan, masing-masing menyebut angka dari data Anda

## Cocok untuk siapa
- Pemilik toko atau usaha yang punya ekspor data kasir, Shopee, Tokopedia, atau spreadsheet
- Admin yang setiap minggu harus membuat laporan penjualan

## Contoh sebelum & sesudah
**Sebelum:** Rekap manual di Excel memakan waktu: menjumlah per produk, mengurutkan, lalu mencari hari terbaik satu per satu.

**Sesudah (cukup ketik):** "File ekspor Shopee September sudah ada di folder (penjualan-september.csv). Tolong direkap: omzet sebulan berapa, produk paling laku apa, hari paling ramai kapan?"

*Cuplikan balasan chat versi 1.2.7: keluaran skrip untuk chat, pada data fiktif yang angkanya sama dengan uji bot 17 Okt (produk peringkat 2–3 dipotong). Versi ini belum diuji ulang di bot Telegram.*
```
Rekap penjualan 1 Sep 2026 – 30 Sep 2026

Omzet: Rp 5.519.000 dari 66 pesanan Selesai
Rata-rata per hari: Rp 183.967 (omzet dibagi 30 hari kalender; 29 hari ada penjualan)
Tidak dihitung (batal/retur): Pengembalian Dana 2 pesanan Rp 272.000; Batal 4 pesanan Rp 238.000

Produk terlaris menurut omzet:
1. Kaos Oversize Abu: Rp 1.659.000 (30,1%), 21 pcs × Rp 79.000
…
4. Topi Baseball: Rp 990.000 (17,9%), 22 pcs × Rp 45.000
5. Tote Bag Natural: Rp 805.000 (14,6%), 23 pcs × Rp 35.000
Terlaris menurut jumlah: Tote Bag Natural, 23 pcs

Hari paling ramai:
Omzet tertinggi Sabtu, 5 Sep 2026 (Rp 549.000); terendah Jumat, 18 Sep 2026 (Rp 35.000)
Pesanan terbanyak: Selasa, 1 Sep 2026 dan Sabtu, 5 Sep 2026 (5 pesanan per hari, seri)
Pola hari dalam minggu (omzet hari itu dibagi jumlah hari itu di periode; hari tanpa penjualan dihitung Rp 0): tertinggi Senin Rp 288.750; terendah Kamis Rp 113.750.
```
Contoh saran sesuai aturan skill (setiap saran menyebut angka dari rekap di atas): "Tote Bag Natural paling banyak terjual (23 pcs) tapi harga jualnya termurah (Rp 35.000/pcs). Coba jual paket dengan Kaos Oversize Abu (Rp 79.000/pcs, terlaris menurut omzet) supaya nilai per pesanan naik."

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent Anda dan lampirkan file CSV-nya (file tabel sederhana yang bisa dibuka di Excel), misalnya:
- "Tolong rekap penjualan dari file penjualan-september.csv"
- "Ini ekspor kasir kedai kopi aku 2 minggu, menu mana yang paling laku sama hari apa yang paling rame?"
- "Rekap pesanan Shopee bulan ini, yang batal dan retur jangan dihitung."
- "Buatkan ringkasan penjualan minggu ini untuk ditempel di grup tim."

## Syarat
File berformat **CSV** yang punya kolom tanggal, nama produk, dan total atau harga. Kolom jumlah (qty) sebaiknya ada; tanpa kolom itu, rekap menghitung jumlah transaksi per produk, bukan jumlah pcs, dan harga per pcs tidak ditampilkan. Jika filenya Excel (.xlsx), simpan dulu sebagai CSV. Sebaiknya ada Python 3 di komputer (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org) agar angka dihitung skrip; tanpa Python, AI menghitung manual dan akan memberi tahu bahwa hasilnya belum diverifikasi skrip.

## Instalasi singkat
Salin folder `rekap-penjualan-csv` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, dua sumber yang terpisah.
- **Uji OpenClaw, 1 Oktober 2026** (angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario ekspor Shopee): skor tanpa skill 7,5 → dengan skill 8,5, lalu 9 setelah perbaikan v1.2.3. Selisihnya kecil dan terutama pada kelengkapan format, bukan ketepatan angka.
- **Uji simulasi agent (perbandingan tanpa dan dengan skill), 23 September 2026** (`examples/00-pembanding-tanpa-skill.md`): pada file yang rapi, angka agent tanpa skill sama benarnya. Nilai tambahnya ada di format Indonesia yang berantakan: pada file dengan harga `68.500,00`, cara "ambil digit saja" menghasilkan Rp 1.389.910.000 padahal yang benar Rp 13.899.100 (100 kali lipat), tanpa peringatan. Pada ekspor marketplace, bila pesanan batal dan retur ikut dihitung, omzet contoh membengkak menjadi Rp 10.793.000 dari yang seharusnya Rp 9.006.000; dengan skill keduanya benar.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Format ekspor Tokopedia, kasir kedai, dan angka berformat campur belum diuji di OpenClaw. Bot Telegram asli: diuji 17 Okt 2026 dan belum lulus acuan kami (lihat bagian berikut).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, data fiktif) pada 17 Oktober 2026, versi 1.2.5, dengan pesan yang sama untuk kedua sisi (tanpa skill dan dengan skill): pemilik toko online kaos dan aksesori menulis bahwa file ekspor penjualan September dari Shopee (72 baris: 66 selesai, 4 batal, 2 pengembalian dana) sudah ada di folder kerja, lalu minta direkap: omzet sebulan berapa, produk paling laku apa, dan hari paling ramai kapan. Skor 1–10 dari penilai independen: tanpa skill **8** → dengan skill **6,5** (selisih −1,5): **belum lulus acuan kami** (dengan skill di bawah 8, dan di uji ini skill kalah); pemeriksa kedua setuju.

Kedua sisi menghitung omzet Rp5.519.000 dari 66 pesanan selesai, produk terlaris menurut omzet (Kaos Oversize Abu), dan hari tertinggi dengan benar. Dengan skill, Anda juga mendapat nilai pesanan batal dan pengembalian dana serta persentase tiap produk. Namun bagian saran (insight) salah: Topi Baseball disebut paling banyak terjual dan paling murah, padahal yang paling banyak terjual (23 pcs) dan paling murah (Rp35.000) adalah Tote Bag, sehingga saran "cek apakah harga topi kurang kompetitif" menyesatkan. Istilah "margin per unit" juga keliru, karena data tidak memuat modal. Tanpa skill, semua angkanya benar, ringkas, dan membedakan produk terlaris menurut omzet dan menurut jumlah terjual.

Catatan jujur: kesalahan ini ada pada kalimat saran, bukan pada hitungan omzet. Perbaikannya (lihat Riwayat perubahan) belum diuji ulang di bot Telegram; sampai itu, cocokkan setiap kalimat saran dengan daftar angka di atasnya. Ini satu pesan uji per sisi, bukan uji berulang.

Versi 1.2.7 memperbaiki temuan-temuan di atas dan belum diuji ulang di bot Telegram asli.

## FAQ
**Apakah data saya dikirim ke internet?**
Script berjalan di komputer Anda sendiri. Isi data tetap dibaca oleh AI agent yang Anda pakai.

**Nama kolom di file saya berbeda. Tetap bisa?**
Biasanya bisa: AI agent mencocokkan kolom berdasarkan isi file. Syaratnya ada kolom tanggal, nama produk, dan total atau harga.

**Bagaimana kalau ada baris yang rusak?**
Baris yang rusak dilewati, lalu jumlah dan alasannya dilaporkan.

> **Catatan:** rekap ini menghitung omzet dari file penjualan yang Anda kirim. Bukan laporan laba rugi dan bukan perhitungan pajak; hasilnya sebaik kualitas datanya.

## Riwayat perubahan

Versi terkini: **1.2.7** (26 Okt 2026): rekap kini menulis nama hari bersama tanggal (mis. "Sabtu, 5 Sep 2026"), menambah satu baris pola hari dalam minggu (hanya bila data minimal 14 hari, dihitung skrip), memasukkan setiap peringatan data ke bagian "Catatan data" dengan bahasa sehari-hari, dan menyebut berapa baris tanpa jumlah yang dihitung 1 pcs. Angka lainnya sama dengan 1.2.6. Sebelumnya, versi 1.2.6 (17 Okt 2026): saran kini hanya ditulis bila ada angka hitungan yang mendukung, produk terlaris ditampilkan menurut omzet dan menurut jumlah, tanpa istilah "margin" bila tidak ada data modal, balasan chat lebih ringkas (tanpa judul, satu rata-rata), dan file tanpa kolom jumlah tidak lagi ditulis seolah-olah jumlah pcs. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
