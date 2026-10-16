# Cek Kesehatan Akun Iklan, Tanpa Login

**Cari tahu kenapa iklan Anda boros — dan apa yang dibenahi dulu minggu ini.**

Untuk Meta (Facebook/Instagram) Ads, TikTok Ads, Google Ads, Shopee Ads, dan iklan TikTok Shop/Tokopedia.
Tanpa memberi password, tanpa login, tanpa sambungan teknis (API): cukup screenshot, file ekspor, atau menjawab beberapa pertanyaan.

*Diuji AI penguji independen di OpenClaw: 6,0 → 8,5 dari 10 (pembeda terbesar: skill menolak login/password akun iklan dan mengikuti aturan iklan klinik, sedangkan AI tanpa skill, pada salah satu uji, menawarkan login dan menyarankan testimoni pasien; hitungan titik impas iklan (ROAS impas) sudah benar di kedua sisi).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Skor kesehatan 0–100 dengan bobot yang jelas** — dihitung skrip, bukan "feeling" AI (skor tetap perkiraan dari bukti yang Anda berikan; makin sedikit bukti, makin ditandai "sementara").
- ✅ **81 titik cek untuk Meta, TikTok, Google, Shopee, dan TikTok Shop, dengan penyesuaian pasar Indonesia**: iklan klik-ke-WhatsApp, target ROAS (omzet iklan per Rp1 biaya iklan) Shopee vs titik impas, anggaran habis sebelum jam ramai malam, tanggal kembar, kata kunci "gratis/pdf" di Google.
- ✅ **Urutan perbaikan berdasarkan dampak dan kemudahan**, lengkap dengan "skor naik berapa kalau ini beres".
- ✅ **Rencana 7 hari siap jalan**, ±1–2 jam per hari, termasuk hari "jangan diutak-atik" agar iklan sempat belajar.
- ✅ **Hitung ROAS impas per produk** — berapa biaya iklan maksimal per pesanan sebelum Anda rugi.

## Cocok untuk siapa
- Pemilik toko online (Shopee, TikTok Shop, Tokopedia) yang beriklan sendiri.
- Klinik, salon, kursus, jasa lokal yang beriklan ke WhatsApp atau website.
- Agensi/freelancer iklan kecil yang butuh checklist audit rapi untuk klien baru.
- Tidak cocok bila Anda butuh laporan angka mingguan → pakai **Laporan Iklan Mingguan** (skill Komunitech lain yang merangkum angka iklan tiap minggu).

## Contoh sebelum & sesudah
**Sebelum (AI tanpa skill):** "Coba optimalkan target audiens, perbaiki materi iklan, dan pantau ROAS secara berkala."
Saran umum, tidak ada angka, tidak tahu harus mulai dari mana.

**Sesudah (cukup ketik):** "Tolong audit iklan Shopee toko gamis saya. Anggaran 50rb/hari tapi ROAS jelek, kayaknya boros."
```
Skor gabungan: 41,3 / 100 (Kritis) - FINAL; bobot: satu platform
PRIORITAS PERBAIKAN (dampak x kemudahan; skor tertinggi dikerjakan dulu)
1. [S06] Target ROAS/bid di atas ROAS impas - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +10,0 bila beres
   Catatan audit: Target ROAS 2, padahal ROAS impas 2,92 (biaya Shopee 12% + kemas Rp2.000)
2. [S07] Anggaran tidak habis sebelum jam ramai - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +10,0 bila beres
   Catatan audit: Anggaran Rp50rb/hari habis jam 14.00
3. [S14] Kata kunci/iklan boros dihentikan - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +10,0 bila beres
   Catatan audit: Kata kunci "gamis murah" habis Rp212rb, 0 pesanan
…
Hari 6 (Sabtu, 3 Okt 2026):
  - Jangan ubah pengaturan besar; biarkan iklan belajar setelah perbaikan. Catat biaya & hasil harian.
```
(Cuplikan simulasi pembuat skill, bukan uji independen; data fiktif dari `examples/uji-pembuat-01-toko-fashion-shopee.md`, dipotong; harga gamis Rp149.000, modal Rp78.000. AI lalu menjelaskan tiga masalah terbesar dengan bahasa sehari-hari.)

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

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Script memakai Python bawaan, tanpa instal paket tambahan.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, 1 Okt 2026 (uji ulang pada v1.0.4; putaran kedua pada v1.0.5 juga rata-rata 8,5), skor 1–10: tanpa skill **6,0** → dengan skill **8,5** (LULUS). Uji pertama sebelum perbaikan hanya 7,5 → 7,75 (belum lulus), jadi angka di sini adalah hasil uji ulang. Data uji OpenClaw berbeda dari contoh di atas (gamis harga Rp189.000, modal Rp95.000): ROAS impas **2,66** — target 2 rugi ±Rp23.180/pesanan; ROAS 2,3 rugi ±Rp10.854. Menolak login/password klinik dan menghindari testimoni pasien (mengikuti aturan iklan fasilitas kesehatan, Permenkes 1787/2010). Sumber skor: `examples/00-openclaw-sebelum-sesudah.md`; contoh "Sesudah" di atas berasal dari simulasi pembuat skill, bukan dari uji OpenClaw.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Skill kurasi MIT (AgriciDaniel/claude-ads) — lihat `ATTRIBUTION.md`. Skor bukan jaminan penjualan naik; patokan frekuensi (berapa kali orang yang sama melihat iklan) dan ROAS adalah patokan awal berdasarkan kebiasaan umum.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: Audit iklan Shopee toko gamis: anggaran habis jam 2, ROAS 2,3. Juga iklan klinik ditolak, ini login saya. Tanpa skill skor **7,5** → dengan skill skor **6** (selisih -1,5, belum lulus acuan kami: skor dengan skill di bawah 8). Hanya sisi DENGAN yang mulai memeriksa kesehatan pengaturan akun (pemasangan pixel, tujuan kampanye, keamanan 2 langkah, jumlah video iklan) lewat 8 pertanyaan, tetapi belum memberi skor, urutan perbaikan, atau rencana, sehingga untuk satu kalimat curhat "rasanya boncos" jawaban tanpa skill justru lebih berguna. Catatan jujur: Kalau pengguna hanya menulis satu kalimat tanpa data pengaturan akun, skill berhenti di titik impas lalu meminta 8 jawaban sebelum skor keluar, jadi pembeli awam bisa merasa belum dibantu. Skor kesehatan, prioritas, dan rencana 7 hari baru muncul setelah pemilik iklan menjawab atau menempelkan bukti.

## FAQ
**Apakah saya harus memberikan password atau akses akun iklan?**
Tidak perlu. Skill ini sengaja tidak login dan tidak memakai API (sambungan teknis ke akun iklan). Semua perubahan tetap Anda lakukan sendiri. Jangan mengirim password/OTP ke chat.

**Apakah skor ini dijamin membuat penjualan naik?**
Tidak ada yang bisa menjamin itu. Skor adalah alat untuk menentukan apa yang dibenahi dulu. Patokan angka (mis. frekuensi maksimal 3) adalah patokan awal, bukan aturan resmi platform, dan nama menu di aplikasi iklan bisa berubah.

**Apa bedanya dengan Laporan Iklan Mingguan?**
Laporan Iklan Mingguan menghitung angka (belanja, biaya per hasil, ROAS, dibanding minggu lalu). Audit Akun Iklan memeriksa **pengaturan dan struktur** akun: pelacakan, tujuan kampanye, audiens, anggaran, materi, halaman tujuan, frekuensi, pengecualian. Keduanya saling melengkapi: audit dulu, lalu pantau tiap minggu.

---
Sebagian metode skor diadaptasi dari proyek open-source claude-ads (MIT). Tidak berafiliasi dengan Meta, TikTok, Google, Shopee, maupun Tokopedia. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
