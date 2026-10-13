# Laporan Progres Klien, Tinggal Catat Lalu Tinggal Kirim

**Catat pekerjaan sekali jalan saat dikerjakan, minta "buatkan laporan mingguan untuk klien X",
langsung dapat draf siap tinjau — email, WA/Telegram, dan Markdown, jam dihitung otomatis.**

## Manfaat
- ✅ **Tidak ada lagi mengetik ulang laporan dari memori setiap minggu.** Cukup catat sekali tiap
  ada progres ("kelarin rekonsiliasi bank buat PT Maju, 2,5 jam"), sisanya dirakit otomatis saat
  diminta.
- ✅ **Total jam dihitung, bukan dikira-kira.** Rincian per proyek, dan entri yang lupa dicatat
  jamnya ditandai jelas — tidak pernah dianggap diam-diam 0 jam.
- ✅ **Tiga versi siap pakai sekaligus**: email formal, WA/Telegram ringkas, dan Markdown untuk
  disimpan sebagai dokumen — tinggal salin sesuai kanal yang dipakai klien Anda.
- ✅ **Kendala dan kebutuhan dari klien otomatis terkumpul** dari catatan harian, tidak perlu
  diingat-ingat lagi saat menulis laporan.
- ✅ **Tetap Anda yang mengirim.** Tidak ada kiriman otomatis ke klien — draf selalu ditinjau dan
  disalin manual, aman dari salah kirim atau kesalahan yang tidak sempat dicek.

## Cocok untuk siapa
- Konsultan pajak, konsultan hukum, akuntan lepas, freelancer IT/desain/marketing, dan jasa
  profesional lain yang menangani beberapa klien sekaligus dan harus rutin lapor progres.
- Anda yang selama ini menulis laporan klien dari ingatan atau menggali ulang chat WA lama.
- Member VIP komunitech.com yang sudah pakai OpenClaw — draf ini bisa dijadwalkan otomatis muncul
  di Telegram Anda tiap Jumat sore (panduan ada di dalam paket; tetap Anda yang mengirim ke klien). Jadwal otomatis memakai pola OpenClaw yang sudah terbukti di skill lain; kombinasi dengan skill ini belum diuji di Gateway sungguhan.

**Kurang cocok:** ingin laporan otomatis langsung terkirim ke klien tanpa ditinjau (skill ini
sengaja tidak melakukan itu), atau butuh laporan internal ke atasan/tim sendiri (pakai skill
`laporan-status-kantor`).

## Contoh sebelum & sesudah
**Sebelum:** akhir minggu baru mulai mengingat-ingat apa saja yang dikerjakan untuk tiap klien,
menghitung jam manual dari catatan berserakan, dan menulis ulang format laporan dari nol setiap
kali.

**Sesudah (cukup ketik sepanjang minggu, lalu minta laporannya):**
"Catat: kelarin rekonsiliasi bank buat PT Maju Jaya, 2,5 jam." → "Buatkan laporan mingguan untuk
PT Maju Jaya."
```
=== VERSI WA/TELEGRAM ===

*Laporan Progres -- PT Maju Jaya*
_Minggu ini (21 September 2026 - 27 September 2026)_

Minggu ini (...): 1 pekerjaan selesai, 1 sedang berjalan, 1 terkendala.
Total jam tercatat: 4 jam.

*Selesai:*
- Rekonsiliasi bank September (Pembukuan bulanan, 2,5 jam)

*Berjalan:*
- Susun draf SPT Masa PPN (Pembukuan bulanan, 1,5 jam)

*Butuh dari Bapak/Ibu:*
- Faktur pajak masukan Oktober belum dikirim
```
(Contoh lengkap tiga versi + Markdown: `examples/uji-pembuat-01-konsultan-pajak.md`.)

**Hasil uji:** skor kualitas 9/10 pada uji penguji independen (simulasi agent). Uji A/B (skenario PT Maju Jaya): tanpa skill, catatan hilang begitu sesi berganti, hanya ada satu versi teks, dan total jam dikira-kira agent; dengan skill, tiga versi (email, WA/Telegram, Markdown) lahir dari data yang sama dan total 4 jam dihitung script. Di OpenClaw 2026.9.6 (uji otomatis agent, bukan manusia): 6 dari 6 butir lulus (terpasang, terpicu otomatis, permintaan malas, hitungan script, tidak salah picu, kualitas). Rincian: `examples/00-pembanding-tanpa-skill.md` dan `examples/UJI-PLATFORM.md`. Uji OpenClaw 2026-10-01: 8 → 7 sebelum perbaikan, 8 → 8,5 setelah perbaikan v1.0.5 (lihat `examples/00-openclaw-sebelum-sesudah.md`). Claude Code diuji lewat simulasi agent; Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Setelah terpasang, cukup ketik ke AI agent Anda, misalnya:
- "Catat: hari ini kelarin desain logo buat Kopi Senja, 3 jam."
- "Lagi ngerjain draf SPT Masa PPN buat PT Maju Jaya, masih nunggu faktur pajak dari mereka."
- "Buatkan laporan mingguan untuk PT Maju Jaya" / "laporan bulanan Kopi Senja"
- "Klien saya siapa saja yang tercatat?"
- "Bikinin laporan 22–26 Sep buat PT Sentosa dari file catatan-kerja.csv" (file catatan Anda
  sendiri dari Excel/Sheets langsung dibaca: pemisah koma/titik koma, "2,5 jam", "90 menit")
- "Kirim draf laporan tiap Jumat sore ke Telegram saya" (OpenClaw, opsional)

## Syarat
Butuh Python di komputer (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari
python.org) untuk pencatatan & perhitungan jam otomatis. Tanpa Python pun, skill tetap bisa
membantu merakit laporan dari catatan yang Anda sampaikan langsung di chat (jam tidak diverifikasi
script — akan diberi tahu).

## Instalasi singkat
Salin folder `laporan-klien-konsultan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## FAQ
**Data pekerjaan klien saya dikirim ke internet?**
Tidak. Semua catatan tersimpan di satu file CSV di komputer Anda sendiri. Yang mengalir ke
penyedia model AI hanya teks percakapan biasa, sama seperti chat lainnya.

**Bisa langsung terkirim otomatis ke klien tiap minggu?**
Tidak, dan memang sengaja. Draf hanya disiapkan untuk Anda tinjau dan kirim sendiri — bahkan bila
dijadwalkan lewat OpenClaw, draf itu masuk ke Telegram/WhatsApp **Anda sendiri**, bukan langsung
ke klien (lihat `references/openclaw-jadwal.md`).

**Bagaimana kalau saya lupa mencatat jam suatu pekerjaan?**
Boleh dikosongkan — laporan tetap dibuat, dan bagian Total Jam menandai jelas berapa entri yang
tidak ikut dihitung, supaya tidak disalahartikan sebagai 0 jam.

## Catatan revisi 1.0.5 (2026-10-01)
Perbaikan dari uji OpenClaw asli 2026-10-01 (skenario laporan progres dari file CSV):
- **Jam tidak lagi dibulatkan 1 desimal.** 3,25 jam tampil "3,25 jam" (sebelumnya "3,2"), total
  tampil "9,75 jam (9 jam 45 menit)" dan selalu sama persis dengan jumlah jam per pekerjaan.
- **File catatan Anda sendiri langsung terbaca** (`--file`): pemisah koma/titik koma/tab, desimal
  koma, "90 menit"/"1 jam 30 menit"/"1:30", tanggal 22/09/2026, header Indonesia/Inggris, file
  dari Excel (BOM, UTF-16, Windows-1252). Bila tetap gagal, pesan error menyebut baris & cara
  memperbaikinya.
- **Teks "Periode periode kustom" diperbaiki** -- rentang kustom cukup menampilkan tanggalnya.
- **"Rencana berikutnya" tidak lagi mengulang judul tugas.** Diisi dari rencana Anda (ucapan,
  `--rencana`, atau kolom Rencana di file); bila belum ada, muncul isian `[isi: ...]` untuk Anda
  lengkapi sebelum dikirim.
- Agent diarahkan memakai script di folder skill sendiri, tidak mencari file ke seluruh disk.
- Uji regresi: 45/45 lolos (termasuk file contoh skenario `tests/data/catatan-kerja.csv`).
