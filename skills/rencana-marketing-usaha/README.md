# Rencana Marketing Usaha Siap Jalan

**Tagline:** Satu kalimat dari Anda, satu rencana marketing lengkap dengan angka anggarannya.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- **Rencana lengkap dalam satu dokumen:** tujuan terukur, target pasar, pesan, kanal, kalender, anggaran, KPI.
- **Angka dihitung, bukan dikira:** pembagian anggaran per kanal, batas biaya per pelanggan (CAC), ROAS impas, dan anggaran iklan maksimal dihitung script dari margin Anda.
- **Cocok untuk modal kecil:** mulai dari WhatsApp, Google Maps, Instagram, TikTok, marketplace; iklan berbayar hanya bila margin sehat.
- **Kalender Indonesia:** gajian, 11.11/12.12, Ramadan-Lebaran, tahun ajaran baru, akhir tahun.
- **Terhubung ke skill lain:** kalender konten, promo, audit iklan, laporan iklan, KPI tim, riset pelanggan.

## Cocok untuk siapa
Pemilik warung/kedai/toko online, jasa lokal, reseller, freelancer, dan usaha mapan yang belum punya rencana marketing tertulis. Tidak butuh istilah teknis.

## Sebelum / sesudah
**Sebelum:** "Budget iklan Rp 6 juta saya taruh di mana ya? Posting kalau sempat saja."
**Sesudah:** rencana 12 bagian: tujuan 120 -> 200 pesanan/bulan, 5 kanal dengan Rp per kanal, kalender gajian/11.11/12.12, batas CAC Rp 10.000, KPI mingguan, aturan berhenti bila iklan tidak menguntungkan. Lihat `examples/01-kedai-kopi-q4.md`.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.4):** rata-rata nilai 6,0 tanpa skill menjadi 9,0 dengan skill (skala 10). Pada skenario nugget ayam (jual Rp30.000, modal Rp27.000, iklan Rp10 juta per bulan, blast WA ke 2.000 nomor beli list), skill menangkap margin Rp0 per produk setelah biaya lain, menolak membakar iklan Rp10 juta sebelum harga dibenahi, dan menolak blast ke nomor beli list dengan dasar UU PDP; tanpa skill, AI ikut menyusun rencana iklan dan cara blast tersebut. Catatan jujur: hitungan margin benar di kedua sisi, pembedanya ada di keamanan dan kelengkapan rencana. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Ketik contoh: *"Bikin rencana marketing 3 bulan untuk toko hijab saya, budget Rp 5 juta, target omzet Rp 40 juta."* Skill akan bertanya sekali soal harga, HPP, tempat jualan, dan waktu luang, lalu menyusun rencana. Jika Anda buru-buru, ia memakai asumsi yang disebut di awal dokumen.

## Instalasi singkat
Salin folder `rencana-marketing-usaha` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Script memakai Python standar (tanpa pemasangan paket); di Windows pakai `python` atau `py`. Skill tetap berguna bila script tidak bisa dijalankan.

## FAQ
1. **Apakah harus punya data penjualan?** Tidak wajib. Tanpa data, skill memakai angka contoh berlabel "asumsi" dan menjadikan pencatatan data sebagai tugas minggu pertama.
2. **Apakah ini menjamin omzet naik?** Tidak. Target adalah tujuan kerja; hasil tergantung produk, harga, dan eksekusi.
3. **Apakah skill menjalankan iklan untuk saya?** Tidak. Skill menyusun rencana dan angka batasnya; pemasangan iklan dikerjakan Anda/tim. Untuk audit iklan pakai `audit-akun-iklan`.

## Skill pendamping
`kalender-konten-30hari`, `promo-kalender`, `audit-akun-iklan`, `laporan-iklan-mingguan`, `kpi-tim`, `riset-calon-pelanggan`, `hitung-hpp`, `harga-jual-marketplace`.

## Asal-usul
Diadaptasi dan diperluas dari dua skill berlisensi MIT (marketing-plan oleh Corey Haines; gtm-strategy oleh Pawel Huryn); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan para pembuat sumber.
