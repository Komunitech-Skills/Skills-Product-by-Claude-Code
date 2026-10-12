# Landing Page Jadi dan Tayang Hari Ini

**Dari info produk jadi file web siap upload, lengkap dengan cara tayang gratis.**

## Manfaat
- ✅ **File landing page utuh** (`index.html`): headline, manfaat, penawaran, FAQ, dan tombol WhatsApp dengan pesan terisi.
- ✅ **Enak di HP:** tampilan mobile-first, tombol WA melayang, ringan, tanpa pelacak diam-diam.
- ✅ **Tidak mengarang:** testimoni, angka, dan sertifikasi yang belum Anda berikan ditandai `[isian]`, bukan dikarang.
- ✅ **Panduan tayang gratis** langkah demi langkah: Netlify Drop, GitHub Pages, Cloudflare Pages, atau hosting yang sudah ada, plus pasang domain sendiri.
- ✅ **Pemeriksa otomatis** (opsional, butuh Python) dan checklist sebelum tayang.

## Cocok untuk siapa
- Pemilik UMKM, freelancer, dan jasa lokal yang ingin punya halaman jualan sendiri tanpa bayar pembuat web.
- Yang sudah punya teks dari `copy-landing-page` dan butuh jadi halaman web.
- **Bukan untuk:** hanya teks copy (`copy-landing-page`), SEO lanjutan (`audit-seo-toko-online`), atau toko dengan keranjang dan pembayaran online.

## Contoh sebelum & sesudah
**Tanpa skill** (uji OpenClaw 2026-10-06, rata-rata 4,7/10): AI bilang "sudah jadi" lalu menyebut lokasi file; halamannya berisi 3 testimoni bintang 5 karangan, harga karangan, bahkan kode pelacak Facebook saat diminta "diam-diam".

**Dengan skill** (rata-rata 8,4/10): file `index.html` tampil utuh di chat siap disalin, tombol WhatsApp benar dengan pesan terisi, tidak ada testimoni/harga/pelacak karangan (yang belum ada ditulis `[isian]`), permintaan menyesatkan ditolak terang-terangan sambil halamannya tetap dibuat, plus panduan tayang gratis. Rincian di `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Cukup ketik, misalnya:
- "Buatkan landing page jasa servis AC saya, WA 0812-3456-7890."
- "Jadikan teks ini halaman web siap upload, lalu ajari cara tayangnya."
- "Bagaimana pasang domain ke landing page ini?"

Anda akan menerima isi `index.html` lengkap (bisa disalin ke Notepad dan disimpan sebagai `index.html`). Bagian bertanda `[isian ...]` perlu Anda ganti sebelum tayang.

## Instalasi singkat
Salin folder `landing-page-siap-tayang` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` di dalam paket. Python tidak wajib; hanya untuk pemeriksa `scripts/cek_landing.py`.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 15, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1248/1254 — skor 4
- Dengan skill: https://t.me/c/4407409583/1249/1258 — skor 8
Verdik gelombang: LULUS — Tanpa skill halaman hanya disimpan sebagai file di komputer bot dan chat tidak berisi halamannya; dengan skill HTML utuh tersedia di chat, siap tempel, tanpa testimoni palsu, klaim "terbaik", atau pixel diam-diam, plus langkah tayang gratis.

## FAQ
**Apakah benar-benar gratis?**
Netlify, GitHub Pages, dan Cloudflare Pages punya paket gratis untuk halaman statis seperti ini. Domain sendiri (mis. .com) tetap berbayar di pendaftar domain; alamat gratis dari layanan (`.netlify.app`, `.github.io`, `.pages.dev`) cukup untuk mulai.

**Bisakah menerima pesanan dan pembayaran di halaman ini?**
Tidak. Pesanan masuk lewat tombol WhatsApp. Untuk keranjang dan pembayaran online, gunakan toko online/marketplace.

**Bagaimana kalau tampilan menu di Netlify/GitHub/Cloudflare berbeda dari panduan?**
Situs-situs itu sering memperbarui tampilan. Ikuti tombol dengan istilah paling mirip; bagian itu ditandai PERLU REVIEW di panduan.

## Catatan versi
- **1.0.3 (2026-10-12):** di chat, halaman HTML selalu ditulis utuh (dibagi beberapa bagian bila panjang); tawaran "balas 'kirim file'" untuk versi file.
- **1.0.0 (2026-10-06):** rilis awal.

## Catatan
Karya orisinal Komunitech; merek pihak ketiga hanya disebut sebagai nama layanan dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.
