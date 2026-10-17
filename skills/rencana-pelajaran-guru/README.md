# Modul Ajar Jadi Cepat, Merujuk CP Resmi

**Ketik satu kalimat topik pelajaran, dapatkan Modul Ajar + LKPD (lembar kerja siswa) + soal & rubrik lengkap sesuai Kurikulum Merdeka — siap disalin ke Word/Google Docs.**

Diuji AI penguji independen di OpenClaw: 5,75 → 8,7 dari 10 (tanpa skill merujuk dasar CP yang sudah usang; dengan skill alokasi menit dihitung skrip dan CP ditandai "cek CP resmi").

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Modul Ajar lengkap (Capaian Pembelajaran/CP, Tujuan Pembelajaran, Alur Tujuan Pembelajaran/ATP, kegiatan, asesmen, diferensiasi,
  refleksi) sesuai struktur Kurikulum Merdeka — bukan sekadar contekan generik
- ✅ Alokasi waktu JP (jam pelajaran) dihitung, bukan dikira — otomatis cocok dengan jam pelajaran sekolah
  (SD 35 menit, SMP 40 menit, SMA/SMK 45 menit per JP)
- ✅ LKPD + soal evaluasi + kunci jawaban + rubrik penilaian dengan skor jelas, langsung
  siap dicetak/dibagikan ke siswa
- ✅ Contoh dan konteks khas Indonesia (pasar, sawah, UMKM, budaya lokal) — bukan terjemahan
  contoh dari luar negeri
- ✅ Jujur soal Capaian Pembelajaran: bila belum yakin bunyi CP resminya, skill ini menandai
  "cek CP resmi" — tidak mengarang seolah pasti benar

## Cocok untuk siapa
- Guru SD/MI, SMP/MTs, SMA/MA/SMK yang perlu membuat atau memperbarui Modul Ajar/RPP
- Guru les privat & bimbingan belajar yang butuh rencana sesi cepat
- Guru madrasah dan guru mapel apa pun (umum, agama, produktif SMK)
- Kepala sekolah/koordinator kurikulum yang membantu tim guru menyeragamkan format

## Contoh sebelum & sesudah
**Sebelum:** Guru begadang menyusun Modul Ajar dari nol, bingung istilah CP/ATP/Profil
Lulusan, dan sering lupa mencocokkan total menit kegiatan dengan jam pelajaran sekolah.

**Sesudah (cukup ketik):** "buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"

Cuplikan hasil (dipotong; contoh dengan data fiktif dari `examples/01-modul-ajar-ipa-kelas7-ekosistem.md`):
```
# MODUL AJAR — Ilmu Pengetahuan Alam (IPA)
| Jenjang / Kelas | SMP / VII |
| Fase | D |
| Topik | Ekosistem |
| Alokasi waktu | 2 pertemuan × 3 JP (120 menit/pertemuan) … |
…
### 1. Capaian Pembelajaran (CP)
*(cek CP resmi — cocokkan dengan dokumen resmi IPA Fase D dari BSKAP No. 046/H/KR/2025)*
…
### 2. Tujuan Pembelajaran
1. Menjelaskan komponen biotik dan abiotik pada ekosistem sawah/kebun di sekitar sekolah.
2. Menyusun rantai makanan dan jaring-jaring makanan dari hasil pengamatan sendiri.
…
#### Pertemuan 1 (120 menit — pembukaan 15’ + inti 90’ + penutup 15’, **status COCOK**)
```
Hasil lengkapnya juga memuat LKPD "Ekosistem Sawah di Sekitar Kita", 5 soal uraian + kunci jawaban + pedoman skor (20/10/0 per soal, nilai akhir maksimum 100). Contoh ini dibuat dengan versi awal skill yang menebak 3 JP (jam pelajaran) per pertemuan; sekarang, bila Anda tidak menyebut jam pelajaran, dipakai bawaan 2 JP per pertemuan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan modul ajar Matematika kelas 4 SD tentang pecahan, 3 pertemuan"
- "RPP 1 lembar Bahasa Indonesia kelas 8 tentang teks eksposisi"
- "LKPD IPS kelas 5 tentang koperasi, sekalian soal dan kuncinya"
- "Rencana sesi les privat Matematika SMA kelas 10 untuk 1 anak, topik trigonometri dasar"

Jika info penting (mapel/topik atau jenjang) belum disebut, skill akan menanyakannya
sekali saja dalam satu pesan — jawab seadanya atau bilang "buatkan saja default" untuk
hasil instan.

## Instalasi singkat
Salin folder `rencana-pelajaran-guru` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket
bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** dua sumber, skor 1–10 penguji independen.
- **Uji OpenClaw (lingkungan uji terpisah), Okt 2026** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): tanpa skill **5,75** (uji v1.0.5) → dengan skill **8,7** (uji ulang v1.0.11 dengan setelan kanal Telegram tanpa kirim sungguhan, rata-rata tiga percobaan), lulus. Tanpa skill merujuk dasar CP yang sudah usang (aturan lama yang sudah diganti); dengan skill modul + LKPD + kunci + rubrik tampil utuh di chat, alokasi menit dihitung skrip, dan CP tidak dikarang.
- **Uji bot Telegram asli, 5 Okt 2026 (v1.0.9):** tanpa skill **6** → dengan skill **8,5**, lulus acuan kami. Rinciannya ada di bagian "Bukti uji di bot Telegram" di bawah.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01; uji muat CLI). Claude Code (simulasi agent). Codex dan Cursor memakai format SKILL.md yang sama; belum uji platform asli di kedua platform itu.

## Bukti uji di bot Telegram

Uji terakhir di bot Telegram OpenClaw asli milik Komunitech (grup uji internal), 5 Okt 2026, versi skill 1.0.9, dengan pesan yang sama untuk bot tanpa skill dan bot dengan skill: tanpa skill **6** → dengan skill **8,5** dari 10 (selisih +2,5). Lulus acuan kami (dengan skill 8 ke atas dan selisih minimal 1,5). Nilai tanpa skill diambil dari uji sebelumnya dengan pesan yang sama, tidak dikirim ulang.
- Dengan skill: guru langsung menerima modul ringkas utuh di chat (tujuan, langkah 80 menit, asesmen), lembar kerja siswa tanpa jawaban, rubrik, dan kunci jawaban guru yang terpisah. Permintaan "bunyi CP persis" dijawab dengan merujuk aturan kurikulum terbaru (BSKAP 046/H/KR/2025) tanpa mengarang bunyinya.
- Tanpa skill: bot mengutip CP dari aturan 2022 yang sudah dicabut sebagai "redaksi resmi".
- Catatan jujur: file Word hanya tersimpan di komputer bot dan belum terkirim ke guru. Versi 1.0.10 dan 1.0.11 mengubah cara file Word diserahkan di chat (isi utuh selalu di chat, file dikirim bila guru membalas "kirim file"), tetapi perubahan itu baru dicoba di komputer uji, belum diuji ulang di bot Telegram.
- Uji sebelumnya di bot Telegram belum lulus: versi lama 6 → 7,5 (di bawah 8, jawaban LKPD tercetak di lembar siswa) dan versi 1.0.6 hanya 5 (modul tidak utuh di chat). Dua hasil itu yang mendorong perbaikan di atas.

## FAQ

**Apakah CP (Capaian Pembelajaran) yang dihasilkan pasti sesuai dokumen resmi?**
Tidak selalu kata demi kata — kurikulum resmi bisa direvisi kapan saja. Bila Anda tidak
menempelkan teks CP resmi, skill ini menulis ringkasan umum dan menandainya "cek CP resmi"
supaya Anda tahu harus mencocokkan dengan dokumen resmi mapel & fase Anda. Kalau Anda tempel
CP resmi dari dokumen sekolah, skill akan memakainya persis.

**Sekolah saya punya format Modul Ajar sendiri, bisa dipakai?**
Bisa. Lampirkan atau ceritakan format sekolah Anda, skill akan mengisi format itu dengan hasil
yang sama (CP, tujuan, kegiatan, asesmen), bukan memaksakan format bawaan skill ini.

**Hasilnya dalam bentuk file Word langsung atau teks biasa?**
Hasil ditampilkan utuh di chat sebagai teks terstruktur (judul, tabel, daftar) yang bisa
disalin-tempel ke Word/Google Docs. Bila Anda bilang "untuk dicetak/supervisi" dan komputer
punya Python 3, skill juga membuat file Word (.docx) tanpa instal paket tambahan; jika tidak
bisa, teks di chat tetap lengkap.

**Apakah lembar siswa memuat jawaban?**
Tidak. LKPD dan soal siswa bersih; kunci jawaban utuh ada di bagian "Kunci Jawaban (untuk
guru)" di akhir, jadi lembar siswa bisa langsung digandakan.

**Bisa minta kode dan bunyi CP resmi persis?**
Skill tidak mengarang CP. Ia merujuk Keputusan Kepala BSKAP No. 046/H/KR/2025 dan memberi
langkah mengambil bunyi CP dari dokumen resminya, plus tempat isian di modul; tetap cocokkan
dengan dokumen resmi sekolah Anda.

## Riwayat perubahan

Versi terkini: **1.0.12**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.

Skill ini diadaptasi dari ide struktur modul ajar (Apache-2.0, proyek referensi pendidikan); implementasi, script, dan contoh Indonesia milik Komunitech. Komunitech tidak berafiliasi dengan pembuat sumber referensi.
