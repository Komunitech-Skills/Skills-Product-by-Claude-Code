# Hitung Modal & Harga Jual yang Pas

**Dari resep dan daftar belanja, langsung dapat HPP per produk, harga jual ideal, dan target penjualan minimal.**

## Manfaat
- ✅ HPP per unit akurat: bahan, tenaga kerja, overhead, kemasan, sampai penyusutan alat
- ✅ Konversi satuan otomatis: beli 1 kg pakai 250 g, kain per yard dipakai per meter, lusin, kodi
- ✅ Harga jual dari target margin atau markup, lengkap penjelasan bedanya
- ✅ BEP: tahu berapa produk minimal harus terjual per bulan agar tidak rugi
- ✅ Cocok untuk makanan, fashion, kerajinan, dan jasa

## Cocok untuk siapa
- Pelaku usaha kuliner rumahan, katering, dan kue
- Konveksi, penjahit, dan brand fashion lokal
- Pengrajin, serta penyedia jasa (desainer, fotografer, jasa servis) yang ingin tarif tidak asal tebak

## Contoh sebelum & sesudah
**Sebelum:** "Modal brownies kira-kira 30 ribuan lah, jual 50 ribu." Ternyata upah, gas, box, dan oven belum dihitung.

**Sesudah (cukup ketik):** daftar bahan, upah, dan biaya bulanan brownies kamu
→ HPP Rp47.158 per loyang, harga rekomendasi Rp79.000 untuk margin 40%, dan BEP 17 loyang per bulan, lengkap rinciannya.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Hitung HPP kemeja: kain 1,6 meter (beli 45 ribu per yard), kancing 7 biji, ongkos jahit 35 ribu."
- "Tarif jasa foto produk saya per sesi berapa kalau mau markup 100%?"
- "Harga jual saya 65 ribu, masih untung? Berapa BEP-nya?"

## Instalasi singkat
Salin folder `hitung-hpp` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apa bedanya margin dan markup?**
Margin dihitung dari harga jual, markup dari modal. Modal Rp70.000 dijual Rp100.000: margin 30%, markup 42,86%. Skill menampilkan keduanya supaya tidak tertukar.

**Bahan saya pakai sendok, bukan gram. Bisa?**
Takaran sendok berbeda-beda, jadi skill meminta kamu menimbang sekali (gram/ml) supaya hitungannya akurat. Atau samakan satuan beli dan pakai, misalnya beli 1 sachet, pakai 1 sachet.

**Setelah dapat HPP, bagaimana harga di marketplace?**
Pakai HPP ini sebagai modal di skill `harga-jual-marketplace` untuk menghitung potongan admin, gratis ongkir, dan PPh 22.
