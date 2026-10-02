# Frappe Books Usaha: Pembukuan Gratis, Laporan Tinggal Tanya

**Pakai Frappe Books (software akuntansi gratis, offline, di komputer sendiri) lalu cukup ketik "penjualan bulan ini berapa?",
"siapa yang belum bayar?", atau "masukkan daftar pelanggan ini". AI Anda membaca datanya tanpa mengubah apa pun dan
menyiapkan file impor yang rapi, tanpa biaya bulanan.**

## Manfaat
- ✅ **Laporan dalam satu kalimat.** Penjualan & pembelian per bulan/hari/pelanggan/barang, laba rugi ringkas, lengkap dengan
  DPP, pajak, dan sisa tagihan. Draf, invoice batal, dan retur ditangani dengan benar, jam UTC di file sudah dikonversi ke WIB/WITA/WIT.
- ✅ **Tahu siapa yang telat bayar.** Piutang & utang dikelompokkan per umur (belum jatuh tempo, telat 1–30, 31–60, 61–90, >90 hari),
  yang paling lama di atas. Tempo pembayaran bisa diatur.
- ✅ **Stok tidak kecolongan.** Barang minus, habis, dan menipis langsung terlihat, per gudang bila perlu.
- ✅ **Pindah dari Excel tanpa ketik ulang.** Daftar pelanggan, barang, dan nota dari Excel diubah jadi file Import Wizard resmi
  Frappe Books. Harga "Rp 85.000", "18rb", "1,5jt" dibaca benar; nama dobel, satuan belum ada, tanggal mustahil ditolak sebelum
  merusak data. Ada pratinjau total per nota untuk dicocokkan.
- ✅ **Aman untuk pembukuan.** File data hanya **dibaca** (dikunci read-only), tidak pernah diubah. Laporan harian ke Telegram
  lewat OpenClaw tanpa nama pelanggan. PPN 12% DPP 11/12 dihitung dengan standar pembulatan yang tidak memungut lebih, termasuk PPN bulanan (keluaran − masukan = kurang/lebih bayar) langsung dari data, penjualan tanpa PPN dipisah.

## Cocok untuk siapa
- UMKM yang ingin berhenti bayar Jurnal/Kledo/Paper.id dan memakai **Frappe Books** di laptop/PC sendiri.
- Pemilik yang ingin cukup bertanya ke AI (OpenClaw, Claude Code, Codex, Cursor) tanpa menghafal menu laporan.
- Admin yang punya data lama di Excel dan ingin memindahkannya ke Frappe Books.

**Kurang cocok:** butuh e-Faktur/Coretax (Frappe Books tidak membuatnya), multi-cabang online, atau sudah memakai Dolibarr/hledger
(pakai skill **Dolibarr Usaha** / **hledger Usaha**).

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
(Keluaran nyata script dari data contoh fiktif; lengkapnya di `examples/`.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa:
- "Cek file Frappe Books saya"
- "Penjualan bulan lalu per pelanggan", "barang apa yang paling laku bulan ini"
- "Siapa yang belum bayar? Tempo pelanggan saya 14 hari"
- "Stok apa yang mau habis di gudang Stores?"
- "Untung rugi September"
- "Ini daftar pelanggan dan barang dari Excel, siapkan untuk diimpor ke Frappe Books"
- "Kirim laporan harian Frappe Books ke Telegram saya tiap jam 9 malam" (OpenClaw)

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

Panduan lengkap (termasuk Windows): `CARA-INSTAL.md` di paket. Butuh **Python 3.8+** (gratis di python.org).
Tidak butuh internet, akun, kunci API, atau paket tambahan.

**Status uji jujur (laporan diuji pada versi 1.0.3; versi 1.0.8 menambah `ppn-periode`):** laporan (penjualan, piutang, stok, laba rugi) sudah diuji penguji independen pada file
**asli** buatan Frappe Books v0.36.0 dan angkanya cocok; file CSV pelanggan, barang, penjualan, dan pembelian diterima Import Wizard
asli; akun barang berstok & kredit retur sudah beres. Versi 1.0.3 menghitung laba rugi dengan cara yang sama seperti laporan
Profit And Loss Frappe Books (termasuk barang retur yang kembali ke gudang); di aplikasi asli angkanya sama persis dengan P&L
bawaan dan lolos 46 uji otomatis, **menunggu uji ulang penguji independen**. Jadwal Telegram belum diuji di OpenClaw untuk skill ini. Catatan: per 20 Sep 2026 proyek Frappe Books mengumumkan pembaruan aplikasi sedang tertahan
(masalah sertifikat penanda tangan); versi yang sudah dirilis tetap bisa dipakai.

## FAQ
**Apakah AI bisa merusak atau mengubah pembukuan saya?**
Tidak lewat skill ini. File data dibuka dalam mode baca-saja yang dikunci, dan script tidak punya perintah menulis ke file itu.
Data baru hanya masuk lewat Import Wizard di aplikasi Frappe Books yang Anda klik sendiri — disarankan sebagai draf dulu, setelah backup.

**Kenapa PPN di Frappe Books kadang beda pecahan rupiah dengan hitungan skill?**
Frappe Books menghitung pajak per baris tanpa pembulatan, sedangkan standar Komunitech menghitung persis lalu membulatkan ke bawah
sekali (agar tidak memungut melebihi tarif). Skill menampilkan keduanya dan tidak mengubah apa pun. Pembulatan belum dicocokkan
dengan Coretax; nilai resmi mengikuti faktur di Coretax. Ini alat bantu, bukan nasihat pajak.

**Frappe Books tidak punya tanggal jatuh tempo, lalu bagaimana skill tahu siapa yang telat?**
Jatuh tempo dihitung dari tanggal invoice + tempo pembayaran yang Anda sebutkan (bawaan 30 hari). Asumsi ini selalu ditulis di laporan.

---
Komunitech tidak berafiliasi dengan Frappe Technologies maupun proyek Frappe Books. Frappe Books (AGPL-3.0) tidak disertakan
dalam paket; "Frappe" dan "Frappe Books" adalah merek milik pemiliknya.
