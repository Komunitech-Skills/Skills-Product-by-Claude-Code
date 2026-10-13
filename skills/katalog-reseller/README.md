# Buka Reseller & Agen Tanpa Salah Harga

**Daftar harga bertingkat, syarat kemitraan, dan pesan rekrut yang jujur, dengan hitungan yang membantu Anda dan reseller Anda sama-sama untung.**

Diuji AI penguji independen di OpenClaw: 3,0 → 8,5 dari 10 (tanpa skill menyusun skema bonus rekrut berjenjang dan mengabaikan potongan Shopee; dengan skill skema itu ditolak dan harga tiap tingkat dihitung dari modal serta untung mitra).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Harga dropshipper (penjual tanpa stok sendiri), reseller, dan agen dihitung otomatis dari modal atau harga eceran, bukan kira-kira
- ✅ Langsung ketahuan kalau untung reseller Anda terlalu tipis (penyebab utama reseller banting harga atau berhenti)
- ✅ Dua versi daftar harga: versi internal (dengan margin Anda) dan versi siap kirim ke reseller (tanpa modal)
- ✅ Syarat & ketentuan siap tempel: minimal order, pembayaran, retur, harga minimum, penggunaan foto
- ✅ Pesan ajakan jadi reseller untuk WA dan Instagram dengan contoh untung yang jujur, tanpa skema piramida

## Cocok untuk siapa
- Produsen & pemilik brand UMKM (skincare, makanan, fashion, kopi, kerajinan) yang ingin memperluas penjualan lewat mitra
- Pemilik toko yang sudah punya reseller tapi harga dan aturannya masih berantakan
- Distributor kecil yang ingin merapikan harga agen dan sub-agen berdasarkan jumlah beli

## Contoh sebelum & sesudah
**Sebelum:** "Diskon reseller 15% aja." Setelah dipotong biaya marketplace, reseller hanya untung Rp 4.500 per botol, lalu mulai banting harga dan saling berebut pembeli.

**Sesudah (cukup ketik):** "Aku roasting kopi bubuk robusta 250 gr, modal 32rb + kemasan & label 2rb, jual eceran 79rb. Mau buka dropshipper, reseller min 10, agen min 50. Rencananya diskon 15%, 25%, 35%. Reseller2 biasanya jualan di Shopee/TikTok, potongannya katanya sekitar 10%. Ongkir ke reseller rata2 1.500/bungkus mereka yang tanggung. Boleh diskon ke konsumen maks 5%. Bikinin price list, S&K, sama pesan rekrutnya ya." (S&K = syarat dan ketentuan)

Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-kopi-bubuk-3-tier.md`):
> **Kenapa diperbaiki:** dengan diskon 15%, dropshipper hanya untung Rp 2.500–4.000 per bungkus setelah potongan marketplace. Mitra seperti ini biasanya cepat berhenti atau banting harga. …
>
> | Produk | Harga eceran anjuran | Dropshipper (1 pcs) | Reseller (≥ 10 pcs) | Agen (≥ 50 pcs) |
> |---|---|---|---|---|
> | Kopi Robusta 250 g | Rp 79.000 | Rp 63.200 | Rp 55.300 | Rp 48.900 |
>
> - Harga minimum anjuran untuk iklan/etalase online: **Rp 75.000**.
> - Contoh reseller: beli 10 pcs = modal Rp 553.000. Jika semua terjual di harga eceran, untung ±Rp 143.000 (setelah potongan marketplace ±10% dan ongkir).

Hasil lengkapnya juga memuat tabel untung per tingkat, syarat dan ketentuan kemitraan siap tempel, serta pesan ajakan rekrut.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan price list reseller dan agen untuk 5 produk ini" (lalu tempel daftar produk, modal, dan harga eceran)
- "Diskon agen saya 35%, reseller 25%. Masih aman nggak buat saya dan buat mereka?"
- "Bikin pesan broadcast ajakan jadi dropshipper"

## Instalasi singkat
Salin folder `katalog-reseller` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1 Okt 2026 (v1.0.4), skor 1–10 penguji independen: tanpa skill **3,0** → dengan skill **8,5** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill: skema bonus rekrut berjenjang dibuatkan dan potongan Shopee tidak diperhitungkan; dengan skill: tingkat dropship/reseller/agen dihitung dari modal (HPP) + untung mitra setelah biaya Shopee, dan skema bonus rekrut ditolak.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent) dan bot Telegram uji. Bonus dari merekrut downline (piramida) sengaja ditolak — hanya skema reseller sah.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 5, 2026-10-03.
- Tanpa skill: https://t.me/c/4407409583/627/637 — skor 5
- Dengan skill: https://t.me/c/4407409583/628/640 — skor 8,5
Verdik gelombang: LULUS — DENGAN menghitung harga dari diskon atas harga eceran + untung mitra setelah biaya Shopee dan tidak menyuruh reseller jual di bawah harga eceran sendiri; TANPA menyarankan reseller jual Rp20–22 rb (merusak harga eceran Rp25 rb) tanpa memperhitungkan potongan Shopee.

## FAQ
**Bisa dibuatkan bonus untuk reseller yang merekrut reseller lain?**
Tidak. Bonus dari merekrut adalah ciri skema piramida yang dilarang UU Perdagangan. Sebagai gantinya, skill menawarkan cara sah: diskon lebih besar untuk pembelian lebih banyak, atau bonus barang dari pembelian sendiri.

**Boleh melarang reseller banting harga?**
Boleh ditulis sebagai "harga minimum anjuran" dengan konsekuensi kebijakan kemitraan (teguran sampai penghentian kerja sama). Skill tidak memakai denda uang, dan untuk jaringan usaha yang sudah besar skill menyarankan konsultasi hukum.

**Saya belum menentukan harga eceran. Bisa?**
Bisa. Isi modal dan target margin per tingkat (dropshipper, reseller, agen), lalu skill mengusulkan harga eceran agar reseller tetap punya ruang untung.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
