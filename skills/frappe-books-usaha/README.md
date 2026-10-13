# Frappe Books Usaha: Pembukuan Gratis, Laporan Tinggal Tanya

**Pakai Frappe Books (software akuntansi gratis, offline, di komputer sendiri) lalu cukup ketik "penjualan bulan ini berapa?",
"siapa yang belum bayar?", atau "masukkan daftar pelanggan ini". AI Anda membaca datanya tanpa mengubah data Anda dan
menyiapkan file impor yang rapi, tanpa biaya bulanan.**

Diuji AI penguji independen di OpenClaw (dengan data contoh): 5,5 → 9,0 dari 10 pada uji ulang v1.0.8 (2 Okt 2026; uji sebelumnya v1.0.7 5,0 → 7,5 belum lulus). Dengan skill: PPN masukan diperhitungkan sehingga lebih bayar Rp93.500, dan file database tidak disentuh. Tanpa skill: disuruh menyetor PPN Rp511.500 dan nota dihapus langsung dari file database.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Laporan dalam satu kalimat.** Penjualan & pembelian per bulan/hari/pelanggan/barang, laba rugi ringkas, lengkap dengan
  DPP (harga sebelum pajak), pajak, dan sisa tagihan. Draf, invoice batal, dan retur (pengembalian barang) dipisahkan dari angka final, dan jam UTC (waktu standar internasional) di file dikonversi ke WIB/WITA/WIT.
- ✅ **Tahu siapa yang telat bayar.** Piutang (tagihan pelanggan yang belum dibayar) & utang dikelompokkan per umur (belum jatuh tempo, telat 1–30, 31–60, 61–90, >90 hari),
  yang paling lama di atas. Tempo pembayaran bisa diatur.
- ✅ **Stok tidak kecolongan.** Barang minus, habis, dan menipis langsung terlihat, per gudang bila perlu.
- ✅ **Pindah dari Excel tanpa ketik ulang.** Daftar pelanggan, barang, dan nota dari Excel diubah jadi file untuk fitur impor (Import Wizard) bawaan
  Frappe Books. Harga "Rp 85.000", "18rb", "1,5jt" dibaca benar; nama dobel, satuan belum ada, tanggal mustahil ditolak sebelum
  merusak data. Ada pratinjau total per nota untuk dicocokkan.
- ✅ **Dirancang hati-hati untuk pembukuan.** File data hanya **dibaca** (dikunci hanya-baca) dan skrip tidak punya perintah menulis ke file itu. Laporan harian ke Telegram
  lewat OpenClaw (belum diuji langsung) tanpa nama pelanggan. PPN 12% × DPP 11/12 dihitung dengan pembulatan yang tidak memungut lebih dari tarif (belum dicocokkan dengan Coretax, sistem pajak resmi DJP), termasuk PPN bulanan (keluaran = dipungut dari pembeli, masukan = dibayar ke pemasok; selisihnya kurang/lebih bayar) langsung dari data, penjualan tanpa PPN dipisah.

## Cocok untuk siapa
- UMKM yang ingin berhenti bayar Jurnal/Kledo/Paper.id dan memakai **Frappe Books** di laptop/PC sendiri.
- Pemilik yang ingin cukup bertanya ke AI (OpenClaw, Claude Code, Codex, Cursor) tanpa menghafal menu laporan.
- Admin yang punya data lama di Excel dan ingin memindahkannya ke Frappe Books.

**Kurang cocok:** butuh e-Faktur/Coretax (sistem faktur pajak resmi DJP; Frappe Books tidak membuatnya), multi-cabang online, atau sudah memakai Dolibarr/hledger
(pakai skill **Dolibarr Usaha** untuk Dolibarr atau **hledger Usaha** untuk hledger, program pembukuan berbasis teks).

## Contoh sebelum & sesudah
**Sebelum:** buka Frappe Books → daftar Sales Invoice → filter tanggal → jumlahkan manual, pisahkan draf & batal, hitung sendiri
berapa hari tiap invoice telat. Pindah dari Excel: ketik ulang pelanggan dan barang satu per satu.

**Sesudah:** ketik *"Penjualan September berapa dan siapa yang belum bayar?"*
```
PENJUALAN - Toko Kopi Nusantara (fiktif)
Periode: Sep 2026 (1 Sep 2026 s.d. 30 Sep 2026), zona WIB
Invoice final: 4 (termasuk 1 retur) | draf belum final: 1 (tidak dihitung) | dibatalkan: 1 (tidak dihitung)
DPP / sebelum pajak : Rp 905.000
Pajak               : Rp 28.050
TOTAL               : Rp 933.050
Terbayar (bersih)   : Rp 450.000 | Belum dibayar: Rp 483.050

PIUTANG ... Telat 61-90 hari: 1 invoice, Rp 150.000
  - SINV-1007 | Warung Bu Sari | tgl 1 Jun 2026 | sisa Rp 150.000 | telat 87 hari
```
(Keluaran nyata skrip pada database tiruan dengan data fiktif, dijalankan pembuat skill, bukan hasil uji independen; sebagian baris dipotong. Lengkapnya di `examples/01-laporan-toko-kopi.md`.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa:
- "Cek file Frappe Books saya"
- "Penjualan bulan lalu per pelanggan", "barang apa yang paling laku bulan ini"
- "Siapa yang belum bayar? Tempo pelanggan saya 14 hari"
- "Stok apa yang mau habis di gudang Stores?"
- "Untung rugi September"
- "Ini daftar pelanggan dan barang dari Excel, siapkan untuk diimpor ke Frappe Books"
- "Kirim laporan harian Frappe Books ke Telegram saya tiap jam 9 malam" (OpenClaw; belum diuji langsung)

## Instalasi singkat
1. **Frappe Books** sudah terpasang (gratis, dari https://frappe.io/books). Belum? Ikuti `references/panduan-pasang.md`
   atau pakai **jasa setup Komunitech**.
2. Salin folder `frappe-books-usaha` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Butuh **Python 3.8+** (gratis di python.org). Tidak butuh internet, akun, kunci API, atau paket tambahan.

**Hasil uji (angka nyata):** dua sumber, skor 1–10 penguji independen.
- **Uji OpenClaw dengan data contoh, 2 Okt 2026** (diuji pada v1.0.8; versi terkini 1.0.10; angka dari `examples/00-openclaw-sebelum-sesudah.md`): tanpa skill **5,5** → dengan skill **9,0** (LULUS). Catatan jujur: uji pertama pada v1.0.7 hanya 5,0 → 7,5 (belum lulus, PPN dihitung dari penjualan yang sebagian tanpa PPN); angka di atas dari uji ulang setelah perbaikan. Contoh PPN: tanpa skill disuruh setor Rp511.500; dengan skill PPN masukan diperhitungkan sehingga **lebih bayar Rp93.500**, tanpa menyentuh file database.
- **Uji pada Frappe Books v0.36.0 asli, 26 Sep 2026** (`examples/HASIL-UJI.md`, uji ulang v1.0.3, skor 9 dari 10, LULUS): laba rugi, penjualan, piutang, utang, dan stok yang dihitung skill cocok dengan laporan Profit and Loss (laba rugi), Buku Besar, dan Stock Balance (saldo stok) di aplikasinya. Versi skill saat itu lebih lama dari versi terkini.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis dengan data contoh 2026-10-02). Aplikasi Frappe Books asli diuji penguji di Linux; uji OpenClaw memakai database contoh, bukan file Frappe Books milik pengguna sungguhan, dan uji manusia di komputer pembeli sungguhan (Windows/Mac) belum dilakukan. Belum uji bot Telegram/jadwal untuk skill ini. Codex, Claude Code, Cursor belum uji platform asli penuh. Komunitech tidak berafiliasi dengan Frappe Technologies.

## FAQ
**Apakah AI bisa merusak atau mengubah pembukuan saya?**
Tidak lewat skill ini. File data dibuka dalam mode baca-saja yang dikunci, dan script tidak punya perintah menulis ke file itu.
Data baru hanya masuk lewat Import Wizard (fitur impor) di aplikasi Frappe Books yang Anda klik sendiri — disarankan sebagai draf dulu, setelah backup.

**Kenapa PPN di Frappe Books kadang beda pecahan rupiah dengan hitungan skill?**
Frappe Books menghitung pajak per baris tanpa pembulatan, sedangkan standar Komunitech menghitung persis lalu membulatkan ke bawah
sekali (agar tidak memungut melebihi tarif). Skill menampilkan keduanya dan tidak mengubah apa pun. Pembulatan belum dicocokkan
dengan Coretax; nilai resmi mengikuti faktur di Coretax. Ini alat bantu, bukan nasihat pajak.

**Frappe Books tidak punya tanggal jatuh tempo, lalu bagaimana skill tahu siapa yang telat?**
Jatuh tempo dihitung dari tanggal invoice + tempo pembayaran yang Anda sebutkan (bawaan 30 hari). Asumsi ini ditulis di laporan.

---
Komunitech tidak berafiliasi dengan Frappe Technologies maupun proyek Frappe Books. Frappe Books (AGPL-3.0) tidak disertakan
dalam paket; "Frappe" dan "Frappe Books" adalah merek milik pemiliknya.

## Riwayat perubahan

Versi terkini: **1.0.10**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
