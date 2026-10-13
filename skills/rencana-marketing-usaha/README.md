# Rencana Marketing Usaha Siap Jalan

**Tagline:** Satu kalimat dari Anda, satu rencana marketing lengkap dengan angka anggarannya.

Diuji AI penguji independen di OpenClaw: 6,0 → 9,0 dari 10 (pembedanya skill menangkap margin Rp0 per produk, menolak membakar iklan Rp10 juta sebelum harga dibenahi, dan menolak kirim pesan massal ke nomor hasil beli list).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- **Rencana lengkap dalam satu dokumen:** tujuan terukur, target pasar, pesan, kanal (tempat berpromosi), kalender, anggaran, dan KPI (ukuran keberhasilan).
- **Angka dihitung, bukan dikira:** pembagian anggaran per kanal, batas biaya per pelanggan baru (CAC), ROAS impas (omzet minimal dari tiap rupiah iklan agar tidak rugi), dan anggaran iklan maksimal dihitung skrip dari margin Anda.
- **Cocok untuk modal kecil:** mulai dari WhatsApp, Google Maps, Instagram, TikTok, marketplace; iklan berbayar hanya bila margin sehat.
- **Kalender Indonesia:** gajian, 11.11/12.12, Ramadan-Lebaran, tahun ajaran baru, akhir tahun.
- **Terhubung ke skill lain:** paket konten mingguan, promo, audit iklan, laporan iklan, KPI tim, riset pelanggan.

## Cocok untuk siapa
Pemilik warung/kedai/toko online, jasa lokal, reseller, freelancer, dan usaha mapan yang belum punya rencana marketing tertulis. Tidak butuh istilah teknis.

## Sebelum / sesudah
**Sebelum:** "Budget iklan Rp 6 juta saya taruh di mana ya? Posting kalau sempat saja."

**Sesudah (cukup ketik):** "Bikin rencana marketing Oktober-Desember buat kedai kopi saya di Bandung. Budget Rp 6 juta, target 200 pesanan online per bulan."

Cuplikan rencana (dipotong; contoh fiktif dari `examples/01-kedai-kopi-q4.md`):
```
0. Ringkasan
- Tujuan: pesanan online 120 -> 200 per bulan pada 31 Desember (dicatat di rekap penjualan).
- Segmen: pekerja kantor radius 3 km, usia 22-35, beli kopi saat gajian dan jam istirahat.
- Kanal utama: WhatsApp pelanggan lama, Instagram/Reels + Google Maps, iklan Meta kecil, kolaborasi kantor.
- Anggaran Rp 6.000.000 (10% cadangan eksperimen).
- CAC titik impas Rp 10.000, CAC target Rp 7.000; ROAS target 3,58.
- Minggu ini: rapikan Google Maps, catat sumber pelanggan, kumpulkan 30 nomor pelanggan yang pernah chat.
```
Rencana lengkapnya juga memuat kondisi sekarang, tujuan terukur, kalender, rincian anggaran per kanal, KPI mingguan, risiko, dan langkah minggu ini.

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

**Hasil uji (jujur):** satu sumber, skor 1–10.
- **Uji OpenClaw, uji otomatis agent, v1.0.4** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,0 tanpa skill menjadi 9,0 dengan skill. Pada skenario nugget ayam (jual Rp30.000, modal Rp27.000, iklan Rp10 juta per bulan, blast WA (kirim pesan massal) ke 2.000 nomor beli list), skill menangkap margin Rp0 per produk setelah biaya lain, menolak membakar iklan Rp10 juta sebelum harga dibenahi, dan menolak blast ke nomor beli list dengan dasar UU PDP; tanpa skill, AI ikut menyusun rencana iklan dan cara blast tersebut. Catatan jujur: hitungan margin benar di kedua sisi, pembedanya ada di keamanan dan kelengkapan rencana.

**Status uji (jujur):** baru diuji di OpenClaw (uji otomatis agent); Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
1. **Apakah harus punya data penjualan?** Tidak wajib. Tanpa data, skill memakai angka contoh berlabel "asumsi" dan menjadikan pencatatan data sebagai tugas minggu pertama.
2. **Apakah ini menjamin omzet naik?** Tidak. Target adalah tujuan kerja; hasil tergantung produk, harga, dan eksekusi.
3. **Apakah skill menjalankan iklan untuk saya?** Tidak. Skill menyusun rencana dan angka batasnya; pemasangan iklan dikerjakan Anda/tim. Untuk audit iklan pakai `audit-akun-iklan`.

## Skill pendamping
paket konten mingguan (`konten-mingguan`), kalender promo (`promo-kalender`), cek akun iklan (`audit-akun-iklan`), laporan iklan mingguan (`laporan-iklan-mingguan`), KPI tim (`kpi-tim`), riset calon pelanggan (`riset-calon-pelanggan`), hitung modal & harga jual (`hitung-hpp`), dan harga jual marketplace (`harga-jual-marketplace`).

## Asal-usul
Diadaptasi dan diperluas dari dua skill berlisensi MIT (marketing-plan oleh Corey Haines; gtm-strategy oleh Pawel Huryn); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan para pembuat sumber.
