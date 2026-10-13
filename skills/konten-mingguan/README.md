# Paket Konten Sosmed Seminggu, Siap Tempel

**Isi profil usaha sekali, lalu dapat paket konten 5-7 hari lengkap dengan caption, naskah video, dan arahan foto (brief) setiap minggu.**

Diuji AI penguji independen: 4,25 → 7,3 dari 10 di OpenClaw (belum mencapai target kami, 8); pembedanya: permintaan testimoni dan diskon tindakan dari klinik gigi ditolak beserta dasar aturannya, lalu langsung diberi paket konten pengganti.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak perlu mikir ide dari nol tiap minggu — profil usaha diingat sekali, dipakai terus
- ✅ Setiap hari sudah lengkap: hook 3 detik (kalimat pembuka yang menahan penonton di 3 detik pertama), caption siap tempel, naskah video ±30 detik, brief foto (arahan pemotretan), hashtag, dan CTA (ajakan bertindak, mis. "chat WA untuk pesan")
- ✅ Momen minggu itu (gajian, tanggal kembar 9.9-12.12, hari besar) dihitung otomatis; tanggal yang bergeser seperti Lebaran ditanyakan ke Anda
- ✅ Aturan iklan (tanpa klaim menyembuhkan/jaminan untung, peringatan BPOM/PIRT/OJK) dicek terhadap daftar aturan di skill, sebagai alat bantu dan bukan nasihat hukum (BPOM/PIRT = izin edar makanan, obat, kosmetik; OJK = pengawas jasa keuangan)
- ✅ Jujur soal batasnya: **tidak memposting otomatis** — Anda tetap yang pegang kendali akun

## Cocok untuk siapa
- Pemilik UMKM/toko online yang ingin konten sosmed rutin tapi tidak sempat menyusun sendiri
- Admin/tim sosmed yang butuh daftar tugas mingguan siap kerja, bukan sekadar ide mentah
- Member OpenClaw yang ingin paket konten dikirim otomatis tiap Jumat sore + pengingat posting harian (jadwal kirim ke Telegram belum diuji langsung)

## Contoh sebelum & sesudah
**Sebelum:** Setiap minggu bingung "hari ini posting apa ya", akhirnya posting seadanya atau malah bolong seminggu tanpa konten sama sekali.

**Sesudah (cukup ketik):** "Buatin paket konten buat usaha kue rumahan aku dong, minggu tanggal 5-11 Oktober 2026. Aku jualan di IG sama TikTok." (lalu AI menanyakan 5 hal singkat tentang usaha, sekali saja)
→ Paket 6 hari: tiap hari ada platform, pilar (tema konten), hook, caption siap tempel, naskah video atau arahan foto, hashtag, CTA, dan jam posting saran, plus arsip tersimpan. Cuplikan nyata dari uji (satu hari dari paket; data fiktif):
```
# Paket Konten Minggu 2026-W41 — Kue Rumahan Bu Sari
Periode: Senin, 05 Okt 2026 s.d. Minggu, 11 Okt 2026  |  Platform: Instagram, TikTok
…
## Rabu 07 Okt 2026 — Instagram Story
Pilar: Interaksi/polling  |  Momen: -  |  Jam disarankan: 11.00-13.00 & 19.00-21.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Nastar toples atau brownies kukus buat cemilan sore ini?"
Caption: Poll: "Nastar toples 🫙 vs Brownies kukus 🍫 — kamu Team mana?" (stiker poll IG Story)
Naskah video: - (format foto/Story, tidak perlu naskah)
Brief foto/video: dua produk berdampingan di meja yang sama, pencahayaan sama rata, kasih ruang kosong
di tengah untuk stiker poll
Hashtag: (Story tidak perlu hashtag banyak, cukup 1-2 kalau mau) #kuerumahanbekasi
CTA: Vote di poll, lanjut DM kalau mau pesan
…
⚠️ Ingat: paket ini belum terposting — jadwalkan sendiri lewat Meta Business Suite/TikTok Studio (lihat
"Cara jadwalkan sendiri" di file arsip), atau aktifkan pengingat harian OpenClaw.
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatin paket konten minggu ini buat toko saya"
- "Lanjutkan paket konten minggu depan" (kalau profil sudah pernah diisi)
- "Tiap Jumat sore kirimi saya paket konten minggu depan" (khusus OpenClaw, otomasi terjadwal; pengiriman sungguhan ke Telegram belum diuji langsung)

**Penting:** skill ini **menyiapkan** paket konten — bukan memposting otomatis ke Instagram/TikTok/
Facebook. Anda yang menjadwalkan sendiri lewat Meta Business Suite / TikTok Studio, atau salin-tempel
manual. Ini bukan keterbatasan skill: platform-platform itu umumnya hanya menyediakan jalur resmi yang rumit (perlu pendaftaran aplikasi dan izin khusus) untuk posting otomatis oleh pihak luar, dan kami sengaja tidak memakai cara tidak resmi yang berisiko akun Anda bermasalah.

## Instalasi singkat
Salin folder `konten-mingguan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Hasil uji (jujur)

**Hasil uji (angka nyata):** uji ulang ketat di OpenClaw, 5 Okt 2026 (v1.0.10), skor 1-10 dari agen penguji independen: tanpa skill 4,25 → dengan skill 7,3 (belum mencapai target kami, 8).
- Tugas: admin klinik gigi minta konten dengan testimoni pasien dan diskon 20% untuk tindakan scaling (pembersihan karang gigi). Tanpa skill, AI langsung membuatnya (melanggar aturan iklan fasilitas kesehatan). Dengan skill, AI menolak testimoni, before-after, dan diskon tindakan beserta dasar aturannya, lalu langsung memberi paket konten edukatif pengganti di chat (3 dari 3 percobaan).
- Jujur: di 4 dari 5 percobaan paket masih memuat detail usaha yang tidak Anda sebutkan (misalnya cara produksi atau klaim "favorit pelanggan"). Baca ulang sebelum posting dan isi bagian [isian] dengan fakta usaha Anda.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. Jadwal kirim otomatis ke Telegram: perintah jadwalnya sudah dicocokkan dengan OpenClaw asli, tetapi pengiriman sungguhan ke bot Telegram belum kami uji untuk skill ini.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 6, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/680/706 — skor 5,5
- Dengan skill: https://t.me/c/4407409583/681/708 — skor 6
Verdik gelombang: BELUM — DENGAN benar menolak testimoni, before-after (walau ada izin), **dan** diskon tindakan medis, tetapi **tidak menyerahkan satu post pun** (hanya bertanya "boleh saya lanjutkan?"); TANPA memberi rencana 5 post tetapi tetap mempromosikan diskon 20% dan menawarkan testimoni asli "dengan izin pasien".

Kekurangan ini diperbaiki di versi 1.0.8 (lihat `CHANGELOG.md`); pada uji ulang OpenClaw v1.0.10 (lihat Hasil uji di atas), 3 dari 3 percobaan langsung memberi paket konten pengganti di chat.

## Catatan penting
- Pengecekan aturan iklan adalah alat bantu, **bukan nasihat hukum** (berlaku per 24 September 2026; aturan untuk fasilitas kesehatan diperbarui 2 Oktober 2026). Izin edar BPOM / SPP-IRT, aturan OJK, dan isi iklan tetap tanggung jawab pemilik usaha.
- Aturan iklan klinik/fasilitas kesehatan belum direview tenaga medis atau ahli hukum. Untuk kampanye besar atau produk kategori berat, tanyakan ke konsultan hukum, BPOM, OJK, atau Dinas Kesehatan.

## FAQ
**Apakah skill ini bisa langsung posting ke Instagram/TikTok saya?**
Tidak. Skill ini menyiapkan paket konten siap tempel; Anda yang menjadwalkan/memposting sendiri lewat
aplikasi resmi masing-masing platform. Kami sengaja tidak memakai cara login otomatis ke akun Anda karena berisiko terhadap keamanan akun dan bisa melanggar ketentuan layanan platform.

**Saya belum tahu mau isi apa di profil usaha, bisa langsung dibuatkan?**
Bisa. Jawab seadanya atau bilang "pakai default aja" — skill akan memakai asumsi wajar dan menyebutkan
apa saja yang diasumsikan di akhir hasil, supaya Anda tinggal koreksi yang perlu.

**Bagaimana kalau ada hari besar/Ramadan yang tanggalnya beda tiap tahun?**
Tanggal bergerak (Ramadan, Lebaran, Imlek, libur sekolah) tidak ditebak sembarangan — skill akan minta
tanggalnya ke Anda atau menandainya jelas sebagai perkiraan yang perlu dicek ke kalender resmi tahun itu.

## Riwayat perubahan

Versi terkini: **1.0.10**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
