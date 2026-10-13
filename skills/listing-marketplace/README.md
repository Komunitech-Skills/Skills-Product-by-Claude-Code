# Listing Shopee, Tokopedia, TikTok Shop Sekali Jadi

**Ceritakan produk Anda, dapat judul, deskripsi, dan kata kunci yang siap tempel ke tiga marketplace.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Judul disusun mengikuti batas karakter aman tiap platform, supaya lebih kecil kemungkinan terpotong atau ditolak (batas terbaru tetap Anda cek di Seller Center)
- ✅ Kata kunci yang biasa diketik pembeli ditaruh di awal judul agar lebih mudah ditemukan
- ✅ Deskripsi rapi dan lengkap: keunggulan, spesifikasi, isi paket, cara pakai, siap tempel
- ✅ Dicek dengan skrip hitung kecil: nomor WA, link, @akun, dan klaim berisiko ("halal", "BPOM", "termurah") yang bisa bikin produk diturunkan
- ✅ Diupayakan tanpa karangan: data yang belum Anda berikan ditandai `[isi: ...]` supaya Anda lengkapi sendiri

## Cocok untuk siapa
- Seller Shopee, Tokopedia, dan TikTok Shop yang upload produk baru setiap minggu
- Pemilik toko yang listingnya sepi pengunjung dan ingin diperbaiki
- Admin toko online yang mengelola satu produk di beberapa marketplace

## Contoh sebelum & sesudah
**Sebelum:** Judul "SAMBAL ENAK MURAH!!! 🔥🔥 ORDER WA 0812xxxx" — terpotong di Tokopedia dan berisiko kena penalti.

**Sesudah (cukup ketik):** "Bikinin listing buat gamis busui aku, namanya Gamis Alya dari Rumah Alya (Solo). Bahan katun rayon, ada resleting depan buat menyusui. Ukuran M (LD 100, PB 135), L (LD 106, PB 137), XL (LD 112, PB 139). Warna navy, sage, mocca. Mau upload di Shopee, Tokopedia, sama TikTok Shop." (LD = lingkar dada, PB = panjang badan)

Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-gamis-busui-tiga-platform.md`):
```
| Platform | Judul | Panjang / batas aman |
|---|---|---|
| Shopee | Gamis Busui Katun Rayon Resleting Depan Gamis Alya Ukuran M L XL Navy Sage Mocca | 80/100 |
| Tokopedia | Gamis Busui Katun Rayon Resleting Depan Gamis Alya M L XL | 57/70 |
| TikTok Shop | Gamis Busui Katun Rayon Resleting Depan Ramah Menyusui Ukuran M L XL | 68/100 (min. 25) |
…
Gamis busui katun rayon dengan resleting depan — adem, praktis untuk menyusui.

✅ Resleting depan untuk menyusui
✅ Katun rayon, adem & jatuh
✅ Ukuran M / L / XL (LD 100 / 106 / 112 cm)
✅ Warna: Navy, Sage, Mocca
…
```
Hasil lengkapnya juga memuat deskripsi untuk Shopee dan Tokopedia, daftar kata kunci, dan hasil pengecekan batas karakter serta kata berisiko.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatin judul dan deskripsi Shopee buat gamis busui bahan ceruty, size M–XXL"
- "Perbaiki listing Tokopedia ini biar lebih gampang dicari: <tempel judul & deskripsi lama>"
- "Cariin kata kunci buat jual tumbler stainless 500 ml di TikTok Shop"

## Instalasi singkat
Salin folder `listing-marketplace` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji Claude Code (simulasi agent, 5 skenario + A/B skenario 1): skor penguji independen **8/10** (LULUS). Tanpa skill: judul 141 karakter (melewati batas Shopee/Tokopedia/TikTok), klaim karangan (“tidak menerawang”, “wudhu friendly”); dengan skill: judul per platform + batas karakter, deskripsi polos siap tempel, cek kata terlarang. Sumber: `examples/HASIL-UJI.md`, `examples/00-pembanding-tanpa-skill.md`. Uji muat OpenClaw 2026.9.5–9.7 dan uji sebelum/sesudah otomatis OpenClaw 2026-10-01 sudah dijalankan, tetapi skor angkanya belum didokumentasikan di folder `examples/`.

**Status uji (jujur):** sudah diuji di Claude Code (simulasi agent) dan OpenClaw (uji muat CLI + uji sebelum/sesudah otomatis 2026-10-01). Codex dan Cursor belum kami uji langsung.

## FAQ
**Apakah batas karakternya pasti sesuai aturan terbaru marketplace?**
Skill memakai batas aman yang sama atau lebih ketat dari batas yang pernah berlaku, dan mengingatkan Anda untuk cek batas terbaru di Seller Center. Kalau Anda tahu angka terbarunya, sebutkan saja dan skill akan memakainya.

**Kalau produk saya belum punya sertifikat halal atau BPOM?**
Skill tidak menuliskannya. Klaim tanpa bukti bisa membuat produk diturunkan dan melanggar aturan perlindungan konsumen.

**Harus pakai Python?**
Tidak wajib. Kalau Python (program gratis untuk menjalankan skrip) ada, pengecekan panjang teks dan kata terlarang berjalan otomatis. Kalau tidak ada, AI agent mengecek manual dan memberi tahu Anda.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
