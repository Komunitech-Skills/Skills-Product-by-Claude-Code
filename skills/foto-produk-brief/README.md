# Foto Produk Kelas Toko Besar, Cukup Pakai HP

**Dapatkan daftar foto, cara menata cahaya jendela, dan ide video 15–30 detik yang tinggal dikerjakan, tanpa studio dan tanpa alat mahal.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

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

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1 Okt 2026 (v1.0.3), skor 1–10 penguji independen: tanpa skill **6,5** → dengan skill **8,8** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dengan skill: brief shot-list per angle, props, dan cahaya HP; tanpa skill: daftar generik tanpa urutan kerja.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung.

## FAQ
**Harus beli lampu studio atau kamera?**
Tidak. Semua panduan dirancang untuk HP, cahaya jendela, dan properti murah seperti kertas karton dan styrofoam. Kalau kamu punya tripod atau lampu, skill akan memakainya.

**Apakah skill ini mengedit foto saya?**
Tidak. Skill membuat brief dan daftar foto yang tinggal kamu kerjakan, lalu memberi checklist sebelum upload.

**Bolehkah foto dibuat lebih bagus dari aslinya?**
Foto boleh dibuat terang dan rapi, tapi warna, ukuran, dan isi harus sesuai barang asli. Foto yang berlebihan memicu ulasan "tidak sesuai foto" dan retur.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
