# Foto Produk Kelas Toko Besar, Cukup Pakai HP

**Dapatkan daftar foto, cara menata cahaya jendela, dan ide video 15–30 detik yang tinggal dikerjakan, tanpa studio dan tanpa alat mahal.**

## Manfaat
- ✅ Shot list 8–10 foto yang menjawab pertanyaan pembeli: bentuk, detail, ukuran, cara pakai, isi paket, varian
- ✅ Panduan cahaya jendela, latar kertas karton, dan pemantul styrofoam, jadi hasilnya terang dan bersih
- ✅ Pengaturan kamera HP langkah demi langkah (fokus, kunci exposure, lensa yang tepat)
- ✅ Rasio yang benar untuk tiap tempat: 1:1 marketplace, 3:4/4:5 feed, 9:16 TikTok & Reels
- ✅ 2–3 ide video pendek dengan storyboard per detik, plus checklist sebelum upload

## Cocok untuk siapa
- Seller marketplace yang memotret produk sendiri di rumah
- Pemilik UMKM kuliner, fashion, kecantikan, kerajinan yang ingin foto lebih meyakinkan
- Pemilik usaha yang ingin memberi brief jelas ke staf, teman, atau fotografer freelance

## Contoh sebelum & sesudah
**Sebelum:** Foto produk di meja makan dengan lampu kuning, latar berantakan, warna tidak sesuai aslinya. Pembeli sering bertanya "ukurannya berapa?" dan ada ulasan "warna beda dengan foto".

**Sesudah (cukup ketik):** "Saya jual sambal botol 150 ml, 3 level pedas. Mau foto sendiri pakai HP untuk Shopee dan TikTok."
→ Brief satu halaman: daftar alat & properti murah, sketsa posisi jendela–produk–pemantul, pengaturan HP, tabel 9 foto (sudut, jarak, latar, rasio, catatan), 2 storyboard video 15 detik, dan checklist sebelum upload.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Bikinin shot list foto untuk hijab voal 4 warna"
- "Cara foto produk skincare pakai HP biar kelihatan premium tapi tetap jujur"
- "Ide video 15 detik untuk kopi susu botolan"

## Instalasi singkat
Salin folder `foto-produk-brief` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Harus beli lampu studio atau kamera?**
Tidak. Semua panduan dirancang untuk HP, cahaya jendela, dan properti murah seperti kertas karton dan styrofoam. Kalau kamu punya tripod atau lampu, skill akan memakainya.

**Apakah skill ini mengedit foto saya?**
Tidak. Skill membuat brief dan daftar foto yang tinggal kamu kerjakan, lalu memberi checklist sebelum upload.

**Bolehkah foto dibuat lebih bagus dari aslinya?**
Foto boleh dibuat terang dan rapi, tapi warna, ukuran, dan isi harus sesuai barang asli. Foto yang berlebihan memicu ulasan "tidak sesuai foto" dan retur.

## Catatan revisi 1.0.3 (2026-10-01)
- Pemicu baru di deskripsi: foto produk kosmetik/skincare/serum/pemutih/obat/suplemen/jamu, foto before-after, edit foto produk, logo BPOM/halal di foto (uji OpenClaw 2026-10-01: skill tidak terbaca pada permintaan serum pemutih).
- Aturan "produk wajib izin edar": tidak menyarankan before-after (termasuk "versi realistis"), klaim hasil, logo BPOM/halal yang belum dimiliki, maupun menjual/pre-order/teaser atau menulis "BPOM dalam proses" sebelum izin edar terbit (PerBPOM 18/2024: promosi & iklan hanya untuk kosmetik bernotifikasi).
- Teks di layar video hanya fakta dari pengguna; selebihnya `[ISI: ...]`.
