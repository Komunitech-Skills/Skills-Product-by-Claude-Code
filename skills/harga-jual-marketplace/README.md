# Harga Jual Marketplace Anti Boncos

**Tahu harga tayang yang pas di Shopee, Tokopedia, dan TikTok Shop supaya tetap untung setelah semua potongan.**

## Manfaat
- ✅ Harga minimal (balik modal) dan harga rekomendasi sesuai target margin atau laba
- ✅ Semua potongan dihitung: admin, gratis ongkir, pembayaran, biaya per pesanan, voucher toko, PPh 22 0,5%
- ✅ Mode kebalikan: masukkan harga jual, langsung tahu untung bersih per barang
- ✅ Bandingkan beberapa marketplace dalam satu tabel
- ✅ Angka dihitung script, rincian potongan jelas per baris

## Cocok untuk siapa
- Penjual online di Shopee, Tokopedia, TikTok Shop, Lazada, dan marketplace lain
- Brand/UMKM yang mau ikut program gratis ongkir atau pasang voucher toko
- Reseller dan dropshipper yang marginnya tipis

## Contoh sebelum & sesudah
**Sebelum:** Pasang harga Rp50.000 karena "modal 35 ribu, untung 15 ribu", ternyata setelah potongan marketplace untungnya tinggal separuh.

**Sesudah (cukup ketik):** "Modal 35 ribu, admin Shopee 8%, gratis ongkir 4%, biaya pembayaran 1,5%, biaya proses 1.250 per pesanan. Mau margin 20%, harga jualnya berapa?"
→ Harga minimal Rp42.152, harga rekomendasi Rp55.000, uang diterima Rp46.050, laba bersih Rp11.050 per barang, lengkap rincian potongannya (termasuk PPh 22 0,5%).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Kalau saya jual Rp59.900 di Tokopedia, untung bersihnya berapa?"
- "Bandingkan harga ideal produk ini di Shopee, Tokopedia, dan TikTok Shop."
- "Kalau pasang voucher 10% maks 5 ribu, harga jualnya harus naik berapa?"

## Instalasi singkat
Salin folder `harga-jual-marketplace` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## FAQ
**Kenapa saya harus mengisi sendiri persentase biaya admin?**
Biaya marketplace berbeda per kategori dan program, dan sering berubah. Supaya hasilnya akurat, ambil angka terbaru dari Seller Center kamu. Kalau cuma ingin gambaran, skill bisa memakai angka contoh yang diberi label jelas.

**Apa itu PPh 22 0,5% yang ikut dipotong?**
Sejak 1 Agustus 2026 marketplace yang ditunjuk memungut PPh 22 sebesar 0,5% dari omzet penjual. Penjual perorangan dengan omzet setahun sampai Rp500 juta bisa dikecualikan jika sudah menyerahkan surat pernyataan ke marketplace.

**Modal saya belum tahu pasti, bagaimana?**
Hitung dulu dengan skill `hitung-hpp` (bahan, tenaga kerja, kemasan, dll.), lalu pakai hasilnya sebagai modal di sini.

## Catatan revisi 1.0.3 (2026-10-01)
- AI wajib menyalin blok "Catatan & asumsi" dari script **kata per kata** ke balasan: dasar aturan PPh 22 marketplace (PMK 37/2025, berlaku 1 Agustus 2026), syarat pengecualian omzet ≤ Rp500 juta, tanggal berlaku, dan disclaimer (temuan uji OpenClaw: sempat diringkas jadi "per PMK terbaru").
- Perbaikan: `harga_marketplace.py --help` sebelumnya error; kini tampil normal.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill. 3 tes otomatis baru (`tests/`).

## Catatan revisi 1.0.5 (2026-10-01)

- Catatan PPh 22 di keluaran script tidak lagi menampilkan teks perintah (`--pph22 tidak`) yang ikut tersalin ke chat member; kini berbunyi "bila sudah, minta hitung ulang tanpa PPh 22". Temuan uji ulang OpenClaw putaran 2.

## Catatan revisi 1.0.4 (2026-10-01)
- Script kini mencetak **status target** ("MEMENUHI target …" / "DI BAWAH target … laba kurang Rp …") pada harga rekomendasi dan pada mode cek harga bila target disebut (`--harga-jual 62.900 --target-margin 25`).
- Opsi baru `--banding-harga "62.900;59.900"`: cek beberapa harga lain (mis. harga psikologis) sekaligus terhadap target, lengkap dengan laba, margin, dan status. AI wajib mengutip status ini, tidak menilai sendiri (temuan uji ulang OpenClaw: Rp62.900 disebut "di bawah target" padahal margin 25,1% ≥ 25%).
- 4 tes otomatis baru (`tests/`), semua lulus.
