# Paket Konten Sosmed Seminggu, Siap Tempel

**Isi profil usaha sekali, lalu dapat paket konten 5-7 hari lengkap dengan caption, naskah, dan brief foto setiap minggu.**

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

## Catatan revisi 1.0.7 (2026-10-02)
- Temuan uji ulang paket klinik (S3): agent masih menawarkan "testimoni pasien boleh asal ada izin tertulis" dan "diskon pasien baru". Kini untuk fasilitas kesehatan: tanpa testimoni pasien & klaim "sembuh" (walau ada izin), tanpa promo diskon/potongan tindakan medis, tanpa imbalan rujukan — sama dengan aturan klinik no. 6 di PANDUAN klinik. PERLU REVIEW tenaga medis/hukum. Script tidak berubah.

## Catatan revisi 1.0.6 (2026-10-02)
- Temuan uji gabungan paket klinik (S3): agent menawarkan merchandise/poin/voucher/"cek tensi gratis" untuk pasien yang mengajak teman. Kini ada aturan faskes tanpa imbalan rujukan & tanpa promo diskon tindakan medis (SKILL.md + `references/aturan-iklan.md`). PERLU REVIEW tenaga medis/hukum.

## Catatan revisi 1.0.5 (2026-10-01)
dari uji ulang OpenClaw: caption lengkap + hashtag setiap hari wajib tampil di chat (file hanya cadangan); produk pangan olahan/kosmetik/suplemen/obat tradisional diingatkan soal izin edar BPOM/SPP-IRT sebelum dipromosikan.
