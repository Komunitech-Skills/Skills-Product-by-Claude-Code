# Buka Reseller & Agen Tanpa Salah Harga

**Daftar harga bertingkat, syarat kemitraan, dan pesan rekrut yang jujur, dengan hitungan yang memastikan kamu dan resellermu sama-sama untung.**

## Manfaat
- ✅ Harga dropshipper, reseller, dan agen dihitung otomatis dari modal atau harga eceran, bukan kira-kira
- ✅ Langsung ketahuan kalau untung resellermu terlalu tipis (penyebab utama reseller banting harga atau berhenti)
- ✅ Dua versi daftar harga: versi internal (dengan margin kamu) dan versi siap kirim ke reseller (tanpa modal)
- ✅ Syarat & ketentuan siap tempel: minimal order, pembayaran, retur, harga minimum, penggunaan foto
- ✅ Pesan ajakan jadi reseller untuk WA dan Instagram dengan contoh untung yang jujur, tanpa skema piramida

## Cocok untuk siapa
- Produsen & pemilik brand UMKM (skincare, makanan, fashion, kopi, kerajinan) yang ingin memperluas penjualan lewat mitra
- Pemilik toko yang sudah punya reseller tapi harga dan aturannya masih berantakan
- Distributor kecil yang ingin merapikan harga agen dan sub-agen berdasarkan jumlah beli

## Contoh sebelum & sesudah
**Sebelum:** "Diskon reseller 15% aja." Setelah dipotong biaya marketplace, reseller hanya untung Rp 4.500 per botol, lalu mulai banting harga dan saling berebut pembeli.

**Sesudah (cukup ketik):** "Modal serum 28 ribu, eceran 89 ribu. Bikinin harga dropshipper, reseller min 12, agen min 60. Reseller saya kebanyakan jualan di Shopee."
→ Tabel harga tiap tier dengan untung reseller setelah potongan marketplace, peringatan tier yang terlalu tipis beserta usulan perbaikannya, daftar harga siap kirim, S&K kemitraan, dan pesan rekrut WA.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan price list reseller dan agen untuk 5 produk ini" (lalu tempel daftar produk, modal, dan harga eceran)
- "Diskon agen saya 35%, reseller 25%. Masih aman nggak buat saya dan buat mereka?"
- "Bikin pesan broadcast ajakan jadi dropshipper"

## Instalasi singkat
Salin folder `katalog-reseller` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

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
Bisa. Isi modal dan target margin per tier, lalu skill mengusulkan harga eceran agar reseller tetap punya ruang untung.

## Catatan revisi 1.0.4 (2026-10-01)
- Uji OpenClaw 2026-10-01: file CSV daftar harga mitra sempat tersimpan di folder `scripts/` skill tanpa lokasi disebut. Kini CSV ditulis ke folder kerja pengguna (path lengkap di `--csv-keluar`), script mencetak path absolut, dan agent wajib menyebut lokasi file di balasan (script `hitung_tier.py` 1.0.1).
