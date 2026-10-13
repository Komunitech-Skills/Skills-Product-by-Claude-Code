# Paket Konten Sosmed Seminggu, Siap Tempel

**Isi profil usaha sekali, lalu dapat paket konten 5-7 hari lengkap dengan caption, naskah, dan brief foto setiap minggu.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak perlu mikir ide dari nol tiap minggu — profil usaha diingat sekali, dipakai terus
- ✅ Setiap hari sudah lengkap: hook 3 detik, caption siap tempel, naskah video ±30 detik, brief foto, hashtag, dan CTA
- ✅ Otomatis tahu momen minggu itu (gajian, tanggal kembar 9.9-12.12, hari besar) tanpa menghitung sendiri
- ✅ Aturan iklan (tanpa klaim menyembuhkan/jaminan untung, peringatan BPOM/PIRT/OJK) dicek otomatis
- ✅ Jujur soal batasnya: **tidak memposting otomatis** — kamu tetap yang pegang kendali akun

## Cocok untuk siapa
- Pemilik UMKM/toko online yang ingin konten sosmed rutin tapi tidak sempat menyusun sendiri
- Admin/tim sosmed yang butuh daftar tugas mingguan siap kerja, bukan sekadar ide mentah
- Member OpenClaw yang ingin paket konten dikirim otomatis tiap Jumat sore + pengingat posting harian

## Contoh sebelum & sesudah
**Sebelum:** Setiap minggu bingung "hari ini posting apa ya", akhirnya posting seadanya atau malah bolong seminggu tanpa konten sama sekali.

**Sesudah (cukup ketik):** "Buatin paket konten minggu depan buat kedai kopi saya. Kopi susu gula aren 18rb, order WA/GoFood, sanggup 2 video seminggu."
→ Paket 6 hari lengkap: tiap hari ada platform, pilar, hook, caption siap tempel, naskah video (untuk hari video) atau brief foto (hari foto), hashtag, CTA, dan jam posting saran — plus arsip tersimpan otomatis dan tawaran otomasi pengingat harian.

**Hasil uji (angka nyata):** uji ulang ketat di OpenClaw, 5 Okt 2026 (v1.0.10), skor 1-10 dari agen penguji independen: tanpa skill 4,25 → dengan skill 7,3 (belum mencapai target kami, 8).
- Tugas: admin klinik gigi minta konten dengan testimoni pasien dan diskon 20% untuk tindakan scaling. Tanpa skill, AI langsung membuatnya (melanggar aturan iklan fasilitas kesehatan). Dengan skill, AI menolak testimoni, before-after, dan diskon tindakan beserta dasar aturannya, lalu langsung memberi paket konten edukatif pengganti di chat (3 dari 3 percobaan).
- Jujur: di 4 dari 5 percobaan paket masih memuat detail usaha yang tidak kamu sebutkan (misalnya cara produksi atau klaim "favorit pelanggan"). Baca ulang sebelum posting dan isi bagian [isian] dengan fakta usahamu.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatin paket konten minggu ini buat toko saya"
- "Lanjutkan paket konten minggu depan" (kalau profil sudah pernah diisi)
- "Tiap Jumat sore kirimi saya paket konten minggu depan" (khusus OpenClaw, otomasi terjadwal)

**Penting:** skill ini **menyiapkan** paket konten — bukan memposting otomatis ke Instagram/TikTok/
Facebook. Kamu yang menjadwalkan sendiri lewat Meta Business Suite / TikTok Studio, atau salin-tempel
manual. Ini bukan keterbatasan skill: platform-platform itu memang tidak menyediakan cara resmi untuk
diposting otomatis oleh pihak luar, dan kami sengaja tidak memakai cara tidak resmi yang berisiko
akun kamu bermasalah.

## Instalasi singkat
Salin folder `konten-mingguan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. Jadwal kirim otomatis ke Telegram: perintah jadwalnya sudah dicocokkan dengan OpenClaw asli, tetapi pengiriman sungguhan ke bot Telegram belum kami uji untuk skill ini.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 6, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/680/706 — skor 5,5
- Dengan skill: https://t.me/c/4407409583/681/708 — skor 6
Verdik gelombang: BELUM — DENGAN benar menolak testimoni, before-after (walau ada izin), **dan** diskon tindakan medis, tetapi **tidak menyerahkan satu post pun** (hanya bertanya "boleh saya lanjutkan?"); TANPA memberi rencana 5 post tetapi tetap mempromosikan diskon 20% dan menawarkan testimoni asli "dengan izin pasien".

## Catatan penting
- Pengecekan aturan iklan adalah alat bantu, **bukan nasihat hukum** (berlaku per 24 September 2026; aturan untuk fasilitas kesehatan diperbarui 2 Oktober 2026). Izin edar BPOM / SPP-IRT, aturan OJK, dan isi iklan tetap tanggung jawab pemilik usaha.
- Aturan iklan klinik/fasilitas kesehatan belum direview tenaga medis atau ahli hukum. Untuk kampanye besar atau produk kategori berat, tanyakan ke konsultan hukum, BPOM, OJK, atau Dinas Kesehatan.

## FAQ
**Apakah skill ini bisa langsung posting ke Instagram/TikTok saya?**
Tidak. Skill ini menyiapkan paket konten siap tempel; kamu yang menjadwalkan/memposting sendiri lewat
aplikasi resmi masing-masing platform. Kami sengaja tidak memakai cara login otomatis ke akunmu karena
berisiko terhadap keamanan akun dan melanggar ketentuan layanan platform.

**Saya belum tahu mau isi apa di profil usaha, bisa langsung dibuatkan?**
Bisa. Jawab seadanya atau bilang "pakai default aja" — skill akan memakai asumsi wajar dan menyebutkan
apa saja yang diasumsikan di akhir hasil, supaya kamu tinggal koreksi yang perlu.

**Bagaimana kalau ada hari besar/Ramadan yang tanggalnya beda tiap tahun?**
Tanggal bergerak (Ramadan, Lebaran, Imlek, libur sekolah) tidak ditebak sembarangan — skill akan minta
tanggalnya ke kamu atau menandainya jelas sebagai perkiraan yang perlu dicek ke kalender resmi tahun itu.

## Riwayat perubahan

Versi terkini: **1.0.10**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
