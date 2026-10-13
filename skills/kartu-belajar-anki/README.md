# Kartu Hafalan Siap Anki

**Tagline:** Tempel catatan — dapat deck + jadwal belajar, tanpa ribet syntax.

## Manfaat
- Kartu basic atau cloze siap impor (tab-separated), plus tag per topik.
- Rencana harian realistis (berapa kartu baru per hari) otomatis dihitung.
- Pratinjau kartu langsung di chat; TSV lengkap bisa disalin.
- Cocok CPNS, UTBK, sertifikasi, bahasa, dan SOP karyawan baru.
- Menolak permintaan bocoran/hak cipta, tetap bantu dari materi Anda sendiri.

## Cocok untuk siapa
Pelajar dan mahasiswa, guru/bimbel, HR yang onboarding karyawan, profesional yang belajar sertifikasi.

## Sebelum / sesudah
- **Sebelum:** mengetik kartu satu per satu di Anki, bingung cloze/tag.
- **Sesudah:** agent menyusun puluhan kartu + jadwal; Anda tinggal impor.

- **Hasil uji (OpenClaw, uji otomatis agent, v1.0.1):** rata-rata nilai 5,75 tanpa skill menjadi 8,5 dengan skill (skala 10). Tanpa skill, kartu hanya disimpan sebagai berkas dan tidak sampai ke chat Telegram; dengan skill isi kartu, jadwal belajar, dan cara impor tampil utuh di chat. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Ketik permintaan biasa lalu tempel catatan Anda, misalnya: "Bikinin kartu belajar Anki dari SOP kasir toko kami buat karyawan baru ya" (lalu tempel SOP-nya). Info yang kurang (jumlah hari belajar, jenis kartu) ditanyakan sekali, atau agent memakai pilihan wajar dan menyebut asumsinya. Python bawaan hanya dipakai untuk memeriksa kartu dan menghitung jadwal; tanpa Python hasil tetap muncul di chat.

## Instalasi
Salin folder `kartu-belajar-anki` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## FAQ

**Apakah Anki wajib?**  
Tidak untuk menyusun kartu; impor paling mudah ke Anki desktop (gratis). Berkas TSV juga bisa dipakai di app flashcard lain.

**Bisa dari PDF buku?**  
Tempel ringkasan/ catatan **Anda**; skill tidak menyalin buku berbayar utuh.

**Apakah agent menginstal Anki?**  
Tidak. Anda impor manual lewat menu File → Import.
