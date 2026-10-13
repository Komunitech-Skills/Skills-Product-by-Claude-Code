# Cek Harga Pesaing, Pasang Harga Tetap Untung

**Tempel link atau screenshot produk pesaing, dapatkan harga pasaran dan harga jual yang disarankan tanpa merusak margin.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tabel pembanding rapi: harga, harga coret, promo, rating, terjual, lokasi tiap pesaing
- ✅ Adil walau ukurannya beda: 200 gr, 1/2 kg, 1 kg, paket "2 x 250 gr" atau "isi 2 @250gr" disetarakan ke ukuran produkmu (plus harga per 100 g/ml/pcs); harga yang janggal (jauh dari pasaran) dipisahkan dan ditanyakan dulu, tidak merusak hitungan
- ✅ Tahu posisi hargamu: termurah, tengah, atau termahal dibanding pasar (terendah, median, tertinggi)
- ✅ Harga minimum dihitung dari modal + biaya marketplace + target untung, jadi rekomendasi **tidak pernah bikin rugi**
- ✅ Peringatan jelas kalau harga pasaran sudah di bawah batas untungmu, plus ide promo & bundling dari pesaing

## Cocok untuk siapa
- Penjual online di Shopee, Tokopedia, TikTok Shop, Lazada, atau website sendiri
- UMKM makanan/minuman, fesyen, kosmetik, kerajinan yang mau meluncurkan produk baru
- Reseller yang bingung kenapa tokonya sepi padahal "harga sudah murah"

## Contoh sebelum & sesudah
**Sebelum:** Buka 8 tab satu per satu, catat harga di kertas, bingung karena ada yang 200 gr, 500 gr, dan 1 kg. Akhirnya pasang Rp65.000 "biar untung", ternyata paling mahal sepasar.

**Sesudah (cukup ketik):** "Cek harga kopi gayo 250 gr di link-link ini. Modal saya 32 ribu, jual di Shopee admin 8%, gratis ongkir 4%. Sekarang saya jual 65 ribu."
→ 6 pesaing dibandingkan setara 250 g, median Rp54.375, harga kamu termahal. Harga minimum Rp49.260, **rekomendasi Rp50.588 - Rp57.188**, harga cantik **Rp53.900** (untung Rp13.913 per bungkus, margin 25,81%). Plus catatan: pesaing terlaris pakai harga Rp49.900, dua pesaing pasang harga coret, satu pesaing jual paket 2 bungkus.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Harga pasaran keripik singkong 250 gr berapa? Ini link-link pesaing saya."
- "Saya tempel screenshot 5 toko pesaing, harga saya 45 ribu kemahalan nggak? Modal 27 ribu."
- "Mau jual serum 20 ml, modal 38 ribu, target untung 30%. Bandingkan dengan produk-produk ini."

Kalau link Shopee/Tokopedia tidak bisa dibuka AI (sering diblokir), cukup tempel teks halamannya atau kirim screenshot. Skill ini tidak pernah memakai akun/login marketplace kamu.

## Instalasi singkat
Salin folder `riset-harga-kompetitor` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Tidak perlu API key, akun, atau instalasi tambahan (hitungan memakai Python bawaan; tanpa Python pun tetap bisa dengan hitung manual).

**Hasil uji (angka nyata):** uji Claude Code simulasi agent (v1.0.5), skor **8,5/10** (LULUS) — **117** angka diverifikasi Decimal independen, **0 selisih**; contoh kopi Gayo median Rp54.375, rekomendasi Rp50.588–Rp57.188, harga cantik Rp53.900 (laba Rp13.913). Belum ada file `00-openclaw-sebelum-sesudah.md` di repo; muat OpenClaw CLI tercatat di `catalog.csv`. Sumber: `examples/HASIL-UJI.md`, `examples/06-uji-ulang-v1.0.1.md`.

**Status uji (jujur):** sudah diuji Claude Code (simulasi agent) dan muat OpenClaw CLI. OpenClaw sebelum/sesudah otomatis belum tercatat di `examples/`. Codex dan Cursor belum uji platform asli. Tidak login/scrape marketplace; link sering diblokir → tempel teks/screenshot.

## FAQ
**Apakah AI bisa otomatis mengambil harga dari Shopee/Tokopedia?**
Kalau AI agent kamu punya fitur membuka halaman web, ia akan mencoba membuka link publik satu per satu (maks. ±20). Banyak marketplace memblokir akses seperti ini; kalau begitu, AI akan minta kamu menempel teks atau screenshot. Skill ini sengaja tidak login, tidak melewati blokir, dan tidak memantau harga terjadwal supaya aman dan sesuai aturan situs.

**Kenapa harga rekomendasinya bisa lebih mahal dari pasaran?**
Karena rekomendasi tidak pernah di bawah harga minimum (modal + biaya + target untung). Kalau pasaran memang lebih murah, kamu akan dapat PERHATIAN beserta pilihan: tekan modal, buat paket/bundling, ganti ukuran, atau tonjolkan keunggulan, daripada ikut perang harga lalu rugi.

**Saya belum tahu modal saya, bisa tetap dipakai?**
Bisa. Tanpa modal, kamu tetap dapat tabel pesaing dan harga pasaran (terendah, median, tertinggi). Rekomendasi harga jual baru muncul setelah modal diisi, supaya tidak menyarankan harga yang bikin rugi.

**Biaya marketplace saya belum tahu, bagaimana?**
Bisa dianggap 0% dulu (jualan langsung) dan AI akan menyebut asumsi itu. Untuk angka potongan Shopee/Tokopedia/TikTok Shop yang rinci, pakai skill `harga-jual-marketplace`; untuk menghitung modal, pakai skill `hitung-hpp`.
