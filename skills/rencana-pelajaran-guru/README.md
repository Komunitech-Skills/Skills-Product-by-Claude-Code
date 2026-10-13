# Modul Ajar Jadi dalam Semenit, Guru Tinggal Mengajar

**Ketik satu kalimat topik pelajaran, dapatkan Modul Ajar + LKPD + soal & rubrik lengkap sesuai Kurikulum Merdeka — siap disalin ke Word/Google Docs.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Modul Ajar lengkap (CP, Tujuan Pembelajaran, ATP, kegiatan, asesmen, diferensiasi,
  refleksi) sesuai struktur Kurikulum Merdeka — bukan sekadar contekan generik
- ✅ Alokasi waktu JP dihitung, bukan dikira — otomatis cocok dengan jam pelajaran sekolah
  (SD 35 menit, SMP 40 menit, SMA/SMK 45 menit per JP)
- ✅ LKPD + soal evaluasi + kunci jawaban + rubrik penilaian dengan skor jelas, langsung
  siap dicetak/dibagikan ke siswa
- ✅ Contoh dan konteks 100% Indonesia (pasar, sawah, UMKM, budaya lokal) — bukan terjemahan
  contoh dari luar negeri
- ✅ Jujur soal Capaian Pembelajaran: bila belum yakin bunyi CP resminya, skill ini menandai
  "cek CP resmi" — tidak pernah mengarang seolah pasti benar

## Cocok untuk siapa
- Guru SD/MI, SMP/MTs, SMA/MA/SMK yang perlu membuat atau memperbarui Modul Ajar/RPP
- Guru les privat & bimbingan belajar yang butuh rencana sesi cepat
- Guru madrasah dan guru mapel apa pun (umum, agama, produktif SMK)
- Kepala sekolah/koordinator kurikulum yang membantu tim guru menyeragamkan format

## Contoh sebelum & sesudah
**Sebelum:** Guru begadang menyusun Modul Ajar dari nol, bingung istilah CP/ATP/Profil
Lulusan, dan sering lupa mencocokkan total menit kegiatan dengan jam pelajaran sekolah.

**Sesudah (cukup ketik):** "buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"
→ Modul Ajar 2 pertemuan lengkap (kegiatan pembuka-inti-penutup dengan konteks ekosistem
sawah/pasar lokal), LKPD "Ekosistem Sawah di Sekitar Kita", 5 soal uraian + kunci jawaban +
rubrik skor 1–4 — total menit tiap pertemuan sudah dicocokkan dengan 3 JP (120 menit).
Contoh lengkap: `examples/01-modul-ajar-ipa-kelas7-ekosistem.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan modul ajar Matematika kelas 4 SD tentang pecahan, 3 pertemuan"
- "RPP 1 lembar Bahasa Indonesia kelas 8 tentang teks eksposisi"
- "LKPD IPS kelas 5 tentang koperasi, sekalian soal dan kuncinya"
- "Rencana sesi les privat Matematika SMA kelas 10 untuk 1 anak, topik trigonometri dasar"

Jika info penting (mapel/topik atau jenjang) belum disebut, skill akan menanyakannya
sekali saja dalam satu pesan — jawab seadanya atau bilang "buatkan saja default" untuk
hasil instan.

## Instalasi singkat
Salin folder `rencana-pelajaran-guru` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket, atau
`docs/instalasi.md` di repo Komunitech.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 6, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/678/697 — skor 6
- Dengan skill: https://t.me/c/4407409583/819/820 — skor 5 (uji ulang versi 1.0.6; versi sebelumnya 7,5)
Verdik gelombang: BELUM — Versi 1.0.6 menangani capaian pembelajaran dengan jujur tetapi hanya mengirim ringkasan modul dan menyebut isi lengkap ada di file yang tidak bisa dibuka dari Telegram; TANPA mengirim modul utuh dan DOCX meski CP-nya keliru.

## FAQ

**Apakah CP (Capaian Pembelajaran) yang dihasilkan pasti sesuai dokumen resmi?**
Tidak selalu kata demi kata — kurikulum resmi bisa direvisi kapan saja. Bila kamu tidak
menempelkan teks CP resmi, skill ini menulis ringkasan umum dan menandainya "cek CP resmi"
supaya kamu tahu harus mencocokkan dengan dokumen resmi mapel & fasemu. Kalau kamu tempel
CP resmi dari dokumen sekolah, skill akan memakainya persis.

**Sekolah saya punya format Modul Ajar sendiri, bisa dipakai?**
Bisa. Lampirkan atau ceritakan format sekolahmu, skill akan mengisi format itu dengan hasil
yang sama (CP, tujuan, kegiatan, asesmen), bukan memaksakan format bawaan skill ini.

**Hasilnya dalam bentuk file Word langsung atau teks biasa?**
Selalu tampil utuh di chat sebagai teks terstruktur (judul `#`, tabel, daftar) yang bisa
disalin-tempel ke Word/Google Docs. Bila kamu bilang "untuk dicetak/supervisi" dan komputer
punya Python 3, skill juga membuat file `.docx` lewat `scripts/buat_docx.py` (tanpa instal
paket tambahan); jika tidak bisa, teks di chat tetap lengkap.

**Apakah lembar siswa memuat jawaban?**
Tidak. LKPD dan soal siswa bersih; kunci jawaban utuh ada di bagian "Kunci Jawaban (untuk
guru)" di akhir, jadi lembar siswa bisa langsung digandakan.

**Bisa minta kode dan bunyi CP resmi persis?**
Skill tidak mengarang CP. Ia merujuk Keputusan Kepala BSKAP No. 046/H/KR/2025 dan memberi
langkah mengambil bunyi CP dari dokumen resminya, plus tempat isian di modul.

## Riwayat perubahan

Versi terkini: **1.0.11**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
