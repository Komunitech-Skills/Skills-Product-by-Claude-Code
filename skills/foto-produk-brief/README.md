# Foto Produk Kelas Toko Besar, Cukup Pakai HP

**Dapatkan daftar foto, cara menata cahaya jendela, dan ide video 15–30 detik yang tinggal dikerjakan, tanpa studio dan tanpa alat mahal.**

Diuji AI penguji independen di OpenClaw: 6,5 → 8,8 dari 10 (brief lengkap berisi daftar foto per sudut, properti, dan pengaturan cahaya HP; tanpa skill hanya daftar umum tanpa urutan kerja).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Daftar foto (shot list) 8–10 foto yang menjawab pertanyaan pembeli: bentuk, detail, ukuran, cara pakai, isi paket, varian
- ✅ Panduan cahaya jendela, latar kertas karton, dan pemantul styrofoam, jadi hasilnya terang dan bersih
- ✅ Pengaturan kamera HP langkah demi langkah (fokus, kunci kecerahan atau exposure, lensa yang tepat)
- ✅ Rasio yang benar untuk tiap tempat: 1:1 marketplace, 3:4/4:5 feed, 9:16 TikTok & Reels
- ✅ 2–3 ide video pendek dengan urutan adegan per detik (storyboard), plus checklist sebelum upload

## Cocok untuk siapa
- Seller marketplace yang memotret produk sendiri di rumah
- Pemilik UMKM kuliner, fashion, kecantikan, kerajinan yang ingin foto lebih meyakinkan
- Pemilik usaha yang ingin memberi brief jelas ke staf, teman, atau fotografer freelance

## Contoh sebelum & sesudah
**Sebelum:** Foto produk di meja makan dengan lampu kuning, latar berantakan, warna tidak sesuai aslinya. Pembeli sering bertanya "ukurannya berapa?" dan ada ulasan "warna beda dengan foto".

**Sesudah (cukup ketik):** "Aku jual hijab voal segi empat 115x115, ada 4 warna: hitam, mocca, dusty pink, sage. Mau foto sendiri pake HP (android, ga punya tripod) buat Shopee sama TikTok Shop. Sering dapet review “warnanya beda sama foto”. Kamar aku ada jendela gede hadap timur. Bikinin brief fotonya dong."

Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-hijab-voal-4-warna.md`):
> ## 2. Setup cahaya & pengaturan HP
> 1. **Matikan semua lampu kamar.** Lampu kuning + cahaya jendela membuat warna mocca dan dusty pink bergeser. Ini sumber utama keluhan "warna beda".
> 2. Lap lensa. Nyalakan **grid/garis bantu** di pengaturan kamera.
> 3. Pakai lensa **1x** (jangan 0,5x). Jangan zoom digital; dekatkan HP bila perlu.
> …
> 8. **Tes warna:** jepret 1 foto uji tiap warna, lalu bandingkan layar HP dengan kain asli di dekat jendela. Kalau beda, ubah kecerahan, bukan filter.
>
> …
>
> | No | Nama foto | Dipakai di | Rasio | Sudut & jarak | Latar & properti | Catatan |
> |---|---|---|---|---|---|---|
> | 1 | **Foto utama**: hijab dilipat rapi (lipatan segitiga/persegi), warna terlaris | Shopee & TikTok Shop slot 1 | 1:1 | Dari atas 90°, HP ±50 cm | Karton putih polos | Produk mengisi ±70–85% bingkai; **tanpa teks promo, tanpa nomor WA/watermark besar** |
> | 2 | Hijab dipakai: tampak depan | Slot 2 | 1:1 (& 3:4 bila tersedia di kategori) | Setinggi dada model, ±1,5 m | Dinding polos terang dekat jendela | Model menghadap jendela (cahaya dari samping depan); izin model |

Brief lengkapnya juga memuat daftar alat dan properti murah, 9 foto, 2 ide video pendek, dan checklist sebelum upload.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bikinin shot list foto untuk hijab voal 4 warna"
- "Cara foto produk skincare pakai HP biar kelihatan premium tapi tetap jujur"
- "Ide video 15 detik untuk kopi susu botolan"

## Instalasi singkat
Salin folder `foto-produk-brief` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1 Okt 2026 (v1.0.3), skor 1–10 penguji independen: tanpa skill **6,5** → dengan skill **8,8** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dengan skill: brief berisi daftar foto per sudut pengambilan, properti, dan pengaturan cahaya HP; tanpa skill: daftar umum tanpa urutan kerja.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung.

## FAQ
**Harus beli lampu studio atau kamera?**
Tidak harus. Panduan dirancang untuk HP, cahaya jendela, dan properti murah seperti kertas karton dan styrofoam. Kalau Anda punya tripod atau lampu, skill akan memakainya.

**Apakah skill ini mengedit foto saya?**
Tidak. Skill membuat brief dan daftar foto yang tinggal Anda kerjakan, lalu memberi checklist sebelum upload.

**Bolehkah foto dibuat lebih bagus dari aslinya?**
Foto boleh dibuat terang dan rapi, tapi warna, ukuran, dan isi harus sesuai barang asli. Foto yang berlebihan memicu ulasan "tidak sesuai foto" dan retur.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
