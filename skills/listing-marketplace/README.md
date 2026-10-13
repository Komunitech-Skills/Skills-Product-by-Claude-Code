# Listing Shopee, Tokopedia, TikTok Shop Sekali Jadi

**Ceritakan produkmu, dapat judul, deskripsi, dan kata kunci yang siap tempel ke tiga marketplace.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Judul otomatis disesuaikan batas karakter tiap platform, jadi tidak terpotong atau ditolak
- ✅ Kata kunci yang biasa diketik pembeli ditaruh di awal judul agar lebih mudah ditemukan
- ✅ Deskripsi rapi dan lengkap: keunggulan, spesifikasi, isi paket, cara pakai, siap tempel
- ✅ Dicek otomatis: nomor WA, link, @akun, dan klaim berisiko ("halal", "BPOM", "termurah") yang bisa bikin produk diturunkan
- ✅ Tidak mengarang: data yang belum kamu berikan ditandai `[isi: ...]`

## Cocok untuk siapa
- Seller Shopee, Tokopedia, dan TikTok Shop yang upload produk baru setiap minggu
- Pemilik toko yang listingnya sepi pengunjung dan ingin diperbaiki
- Admin toko online yang mengelola satu produk di beberapa marketplace

## Contoh sebelum & sesudah
**Sebelum:** Judul "SAMBAL ENAK MURAH!!! 🔥🔥 ORDER WA 0812xxxx" — terpotong di Tokopedia dan berisiko kena penalti.

**Sesudah (cukup ketik):** "Bikinin listing sambal cumi asin 200 ml, 2 level pedas, tanpa pengawet, sudah PIRT, buat Shopee dan Tokopedia"
→ Judul "Sambal Cumi Asin Pedas 200 ml Tanpa Pengawet Oleh Oleh Sidoarjo" (63/70 karakter), deskripsi lengkap, daftar kata kunci, dan hasil pengecekan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatin judul dan deskripsi Shopee buat gamis busui bahan ceruty, size M–XXL"
- "Perbaiki listing Tokopedia ini biar lebih gampang dicari: <tempel judul & deskripsi lama>"
- "Cariin kata kunci buat jual tumbler stainless 500 ml di TikTok Shop"

## Instalasi singkat
Salin folder `listing-marketplace` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji Claude Code (simulasi agent, 5 skenario + A/B skenario 1): skor penguji independen **8/10** (LULUS). Tanpa skill: judul 141 karakter (melewati batas Shopee/Tokopedia/TikTok), klaim karangan (“tidak menerawang”, “wudhu friendly”); dengan skill: judul per platform + batas karakter, deskripsi polos siap tempel, cek kata terlarang. Sumber: `examples/HASIL-UJI.md`, `examples/00-pembanding-tanpa-skill.md`. Uji muat OpenClaw 2026.9.5–9.7 dan uji sebelum/sesudah otomatis 2026-10-01 tercatat di katalog; berkas skor numerik OpenClaw belum ada di `examples/`.

**Status uji (jujur):** sudah diuji di Claude Code (simulasi agent) dan OpenClaw (uji muat CLI + uji sebelum/sesudah otomatis 2026-10-01). Codex dan Cursor belum kami uji langsung.

## FAQ
**Apakah batas karakternya pasti sesuai aturan terbaru marketplace?**
Skill memakai batas aman yang sama atau lebih ketat dari batas yang pernah berlaku, dan selalu mengingatkan kamu untuk cek batas terbaru di Seller Center. Kalau kamu tahu angka terbarunya, sebutkan saja dan skill akan memakainya.

**Kalau produk saya belum punya sertifikat halal atau BPOM?**
Skill tidak akan menuliskannya. Klaim tanpa bukti bisa membuat produk diturunkan dan melanggar aturan perlindungan konsumen.

**Harus pakai Python?**
Tidak wajib. Kalau Python ada, pengecekan panjang teks dan kata terlarang berjalan otomatis. Kalau tidak ada, AI agent akan mengecek manual dan memberi tahu kamu.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
