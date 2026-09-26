# Cek Kesehatan Akun Iklan dalam 15 Menit

**Tahu persis kenapa iklan Anda boros — dan apa yang dibenahi dulu minggu ini.**

Untuk Meta (Facebook/Instagram) Ads, TikTok Ads, Google Ads, Shopee Ads, dan iklan TikTok Shop/Tokopedia.
Tanpa memberi password, tanpa login, tanpa API: cukup screenshot, file ekspor, atau menjawab beberapa pertanyaan.

Versi 1.0.1.

## Manfaat
- ✅ **Skor kesehatan 0–100 yang bisa dipertanggungjawabkan** — dihitung script dengan bobot jelas, bukan "feeling" AI.
- ✅ **81 titik cek khusus pasar Indonesia**: iklan klik-ke-WhatsApp, target ROAS Shopee vs titik impas, anggaran habis sebelum jam ramai malam, tanggal kembar, kata kunci "gratis/pdf" di Google.
- ✅ **Urutan perbaikan paling masuk akal** — dampak × kemudahan, lengkap dengan "skor naik berapa kalau ini beres".
- ✅ **Rencana 7 hari siap jalan**, ±1–2 jam per hari, termasuk hari "jangan diutak-atik" agar iklan sempat belajar.
- ✅ **Hitung ROAS impas per produk** — berapa biaya iklan maksimal per pesanan sebelum Anda rugi.

## Cocok untuk siapa
- Pemilik toko online (Shopee, TikTok Shop, Tokopedia) yang beriklan sendiri.
- Klinik, salon, kursus, jasa lokal yang beriklan ke WhatsApp atau website.
- Agensi/freelancer iklan kecil yang butuh checklist audit rapi untuk klien baru.
- Tidak cocok bila Anda butuh laporan angka mingguan → pakai **Laporan Iklan Mingguan** (skill pasangan).

## Contoh sebelum & sesudah
**Sebelum (AI tanpa skill):** "Coba optimalkan target audiens, perbaiki materi iklan, dan pantau ROAS secara berkala."
Saran umum, tidak ada angka, tidak tahu harus mulai dari mana.

**Sesudah (cukup ketik):** "Tolong audit iklan Shopee toko gamis saya, anggaran 50rb/hari tapi ROAS jelek."
→ Skor **41,3/100 (Kritis)**, bukti 97%. Tiga masalah terbesar:
1. Target ROAS 2, padahal titik impas gamis Anda **2,92** — iklan laku tapi rugi per pesanan.
2. Anggaran habis **jam 14.00**, iklan mati saat pembeli ramai malam hari.
3. Kata kunci "gamis murah" menghabiskan **Rp212rb tanpa satu pesanan**.
Plus rencana Senin–Minggu apa yang dikerjakan tiap hari.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Audit akun Meta Ads klinik saya, ini screenshot Ads Manager-nya."
- "Iklan Google Ads kursus saya klik banyak tapi yang daftar sedikit, tolong cek."
- "Cek kesehatan iklan Shopee dan TikTok Shop saya, belanja Shopee 1,5 juta dan TikTok 3 juta sebulan."
- "Hitung ROAS impas: harga 149rb, modal 78rb, potongan Shopee 12%, kemas 2rb."

AI akan bertanya sekali bila ada info yang kurang. Jawab "tidak tahu" pun boleh — skor akan diberi tanda "sementara".

## Instalasi singkat
Salin folder `audit-akun-iklan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Script memakai Python bawaan, tanpa instal paket tambahan.

## FAQ
**Apakah saya harus memberikan password atau akses akun iklan?**
Tidak. Skill ini sengaja tidak login dan tidak memakai API. Semua perubahan tetap Anda lakukan sendiri. Jangan pernah mengirim password/OTP ke chat.

**Apakah skor ini dijamin membuat penjualan naik?**
Tidak ada yang bisa menjamin itu. Skor adalah alat untuk menentukan apa yang dibenahi dulu. Patokan angka (mis. frekuensi maksimal 3) adalah patokan awal, bukan aturan resmi platform, dan nama menu di aplikasi iklan bisa berubah.

**Apa bedanya dengan Laporan Iklan Mingguan?**
Laporan Iklan Mingguan menghitung angka (belanja, biaya per hasil, ROAS, dibanding minggu lalu). Audit Akun Iklan memeriksa **pengaturan dan struktur** akun: pelacakan, tujuan kampanye, audiens, anggaran, materi, halaman tujuan, frekuensi, pengecualian. Keduanya saling melengkapi: audit dulu, lalu pantau tiap minggu.

---
Sebagian metode skor diadaptasi dari proyek open-source claude-ads (MIT). Tidak berafiliasi dengan Meta, TikTok, Google, Shopee, maupun Tokopedia. Lihat `ATTRIBUTION.md`.
