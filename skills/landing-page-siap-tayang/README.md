# Landing Page Jadi dan Tayang Hari Ini

**Dari info produk jadi file web siap upload, lengkap dengan cara tayang gratis.**

Diuji AI penguji independen di OpenClaw: 4,7 → 8,4 dari 10 (tanpa skill ada testimoni bintang 5, harga, dan kode pelacak karangan; dengan skill yang belum ada ditulis `[isian]` dan permintaan menyesatkan ditolak sambil halamannya tetap dibuat).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Halaman jualan (landing page) utuh** dalam satu file web (`index.html`): judul utama, manfaat, penawaran, tanya-jawab (FAQ), dan tombol WhatsApp dengan pesan terisi.
- ✅ **Enak di HP:** tampilan dirancang untuk HP dulu (mobile-first), tombol WhatsApp melayang, ringan, tanpa pelacak iklan diam-diam.
- ✅ **Dirancang tidak mengarang:** testimoni, angka, dan sertifikasi yang belum Anda berikan ditandai `[isian]`, bukan dikarang.
- ✅ **Panduan tayang gratis** langkah demi langkah: Netlify Drop, GitHub Pages, Cloudflare Pages, atau hosting (tempat sewa situs) yang sudah ada, plus pasang domain (alamat situs) sendiri.
- ✅ **Pemeriksa otomatis** (opsional, butuh Python) dan checklist sebelum tayang.

## Cocok untuk siapa
- Pemilik UMKM, freelancer, dan jasa lokal yang ingin punya halaman jualan sendiri tanpa bayar pembuat web.
- Yang sudah punya teks jualan dari skill Copy Landing Page dan butuh jadi halaman web.
- **Bukan untuk:** hanya teks jualan (pakai skill Copy Landing Page), agar mudah ditemukan di Google (skill Audit SEO Toko Online), atau toko dengan keranjang dan pembayaran online.

## Contoh sebelum & sesudah
**Tanpa skill:** AI bilang "sudah jadi" lalu menyebut lokasi file; halamannya berisi 3 testimoni bintang 5 karangan, harga karangan, bahkan kode pelacak Facebook saat diminta "diam-diam".

**Dengan skill:** file `index.html` tampil utuh di chat siap disalin, tombol WhatsApp benar dengan pesan terisi, pada uji tidak ada testimoni/harga/pelacak karangan (yang belum ada ditulis `[isian]`), permintaan menyesatkan ditolak terang-terangan sambil halamannya tetap dibuat, plus panduan tayang gratis. Angka ujinya ada di bagian "Hasil uji" di bawah.

Cuplikan isi file hasil uji (potongan dari `examples/data/hasil-sesudah-v101-s1.html`; bagian `[isian]` Anda ganti sendiri):

```html
<h1>Sofa Kotor di Rumah? Kami Cuci Langsung di Tempat</h1>
<p class="lembut-teks">Jasa cuci sofa panggilan untuk warga Bandung Raya, mulai Rp150.000 per sofa 2 dudukan. Garansi cuci ulang gratis kalau belum bersih.</p>
<a class="tombol cta" href="https://wa.me/6281234567890?text=Halo%2C%20saya%20tertarik%20dengan%20jasa%20cuci%20sofa%20Bersih%20Sofa%20Bandung">Pesan Cuci Sofa via WhatsApp</a>
…
<div class="kartu"><h3>Garansi cuci ulang gratis</h3><p>Belum merasa bersih? Kami datang lagi dan cuci ulang tanpa biaya tambahan.</p></div>
…
<h2>Kata pelanggan</h2>
<div class="kartu"><p>[isian: testimoni]</p><p class="lembut-teks">[isian: nama pelanggan, kota]</p></div>
```

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

**Hasil uji (angka nyata):** uji OpenClaw 6 Okt 2026 (agent penguji independen, 4 skenario), skor 1–10: tanpa skill **4,7** → dengan skill **8,4** (LULUS). Skor "dengan skill" dari uji ulang v1.0.1; skor "tanpa skill" dari uji pertama (v1.0.0) dengan pesan yang sama. v1.0.3 menambah penulisan halaman utuh di chat. Sumber: `examples/00-openclaw-sebelum-sesudah.md` dan `examples/HASIL-UJI.md`. Hasil di bot Telegram asli ada di bagian berikutnya.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji; pemeriksa `cek_landing.py` dijalankan pada setiap halaman hasil uji. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

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

## Catatan
Karya orisinal Komunitech; merek pihak ketiga hanya disebut sebagai nama layanan dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
