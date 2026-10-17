# Laporan Progres Klien, Tinggal Catat Lalu Tinggal Kirim

**Catat pekerjaan sekali jalan saat dikerjakan, minta "buatkan laporan mingguan untuk klien X",
langsung dapat draf siap tinjau — email, WA/Telegram, dan Markdown (teks berformat untuk disimpan sebagai dokumen), jam dihitung otomatis.**

Diuji AI penguji independen di OpenClaw: 8 → 8,5 dari 10 (setelah perbaikan v1.0.5; selisih kecil, karena tanpa skill pun jumlah jam sudah benar dan file CSV awam juga terbaca; pembedanya bagian "rencana berikutnya" tidak dikarang dan format laporan konsisten). Versi terkini 1.0.6 belum diuji ulang sebelum/sesudah di OpenClaw.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tidak ada lagi mengetik ulang laporan dari memori setiap minggu.** Cukup catat sekali tiap
  ada progres ("kelarin rekonsiliasi bank buat PT Maju, 2,5 jam"), sisanya dirakit otomatis saat
  diminta.
- ✅ **Total jam dihitung, bukan dikira-kira.** Rincian per proyek, dan entri yang lupa dicatat
  jamnya ditandai jelas — tidak dianggap diam-diam 0 jam.
- ✅ **Tiga versi siap pakai sekaligus**: email formal, WA/Telegram ringkas, dan Markdown untuk
  disimpan sebagai dokumen — tinggal salin sesuai kanal yang dipakai klien Anda.
- ✅ **Kendala dan kebutuhan dari klien otomatis terkumpul** dari catatan harian, tidak perlu
  diingat-ingat lagi saat menulis laporan.
- ✅ **Tetap Anda yang mengirim.** Tidak ada kiriman otomatis ke klien — draf ditinjau dan
  disalin manual oleh Anda, sehingga risiko salah kirim lebih kecil (tetap baca ulang sebelum dikirim).

## Cocok untuk siapa
- Konsultan pajak, konsultan hukum, akuntan lepas, freelancer IT/desain/marketing, dan jasa
  profesional lain yang menangani beberapa klien sekaligus dan harus rutin lapor progres.
- Anda yang selama ini menulis laporan klien dari ingatan atau menggali ulang chat WA lama.
- Member VIP komunitech.com yang sudah pakai OpenClaw — draf ini bisa dijadwalkan otomatis muncul
  di Telegram Anda tiap Jumat sore (panduan ada di dalam paket; tetap Anda yang mengirim ke klien). Satu draf terjadwal sekali jalan sudah terkirim ke grup uji Telegram Komunitech pada 13 Okt 2026 dengan total jam yang cocok; jadwal berulang tiap Jumat belum diuji (lihat `examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`).

**Kurang cocok:** ingin laporan otomatis langsung terkirim ke klien tanpa ditinjau (skill ini
sengaja tidak melakukan itu), atau butuh laporan internal ke atasan/tim sendiri (pakai skill
laporan internal Komunitech, `laporan-status-kantor`).

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

Minggu ini (21 September 2026 - 27 September 2026): 1 pekerjaan selesai, 1 sedang berjalan, 1 terkendala. Total jam tercatat: 4 jam.

*Selesai:*
- Rekonsiliasi bank September (Pembukuan bulanan, 2,5 jam)

*Berjalan:*
- Susun draf SPT Masa PPN (Pembukuan bulanan, 1,5 jam)

*Terkendala:*
- Diskusi strategi PPh Badan (Konsultasi pajak)

*Butuh dari Bapak/Ibu:*
- Faktur pajak masukan Oktober belum dikirim

*Rencana berikutnya:*
- [isi: langkah berikutnya untuk "Susun draf SPT Masa PPN" + target tanggal]
- [isi: langkah berikutnya untuk "Diskusi strategi PPh Badan" + target tanggal]
```
(Keluaran asli skrip versi 1.0.6 pada data fiktif yang sama dengan `examples/uji-pembuat-01-konsultan-pajak.md`, bagian WA/Telegram. Berkas contoh itu masih memuat keluaran versi lama: judul periode, kalimat ringkasan, dan bagian "Rencana berikutnya"-nya berbeda, sisanya sama. Isian `[isi: ...]` sengaja dibiarkan supaya Anda yang melengkapi, tidak dikarang AI. Contoh tiga versi + Markdown ada di berkas itu.)

## Cara pakai
Setelah terpasang, cukup ketik ke AI agent Anda, misalnya:
- "Catat: hari ini kelarin desain logo buat Kopi Senja, 3 jam."
- "Lagi ngerjain draf SPT Masa PPN buat PT Maju Jaya, masih nunggu faktur pajak dari mereka."
- "Buatkan laporan mingguan untuk PT Maju Jaya" / "laporan bulanan Kopi Senja"
- "Klien saya siapa saja yang tercatat?"
- "Bikinin laporan 22–26 Sep buat PT Sentosa dari file catatan-kerja.csv" (file catatan Anda
  sendiri dari Excel/Sheets langsung dibaca: pemisah koma/titik koma, "2,5 jam", "90 menit")
- "Kirim draf laporan tiap Jumat sore ke Telegram saya" (OpenClaw, opsional; satu pengiriman terjadwal sekali jalan sudah diuji 13 Okt 2026, jadwal berulang belum)

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

**Hasil uji (angka nyata):** tiga sumber yang terpisah, skor 1–10.
- **Uji perbandingan oleh penguji independen (simulasi agent):** skor kualitas 9/10. Uji A/B (skenario PT Maju Jaya): tanpa skill, catatan hilang begitu sesi berganti, hanya ada satu versi teks, dan total jam dikira-kira agent; dengan skill, tiga versi (email, WA/Telegram, Markdown) lahir dari data yang sama dan total 4 jam dihitung script. Rincian: `examples/00-pembanding-tanpa-skill.md`.
- **Uji pemasangan di OpenClaw 2026.9.6** (uji otomatis agent, bukan manusia): 6 dari 6 butir lulus (terpasang, terpicu otomatis, permintaan malas, hitungan script, tidak salah picu, kualitas). Rincian: `examples/UJI-PLATFORM.md`.
- **Uji sebelum/sesudah OpenClaw, 2026-10-01** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): 8 → 7 sebelum perbaikan (skill sempat kalah dari AI tanpa skill), 8 → 8,5 setelah perbaikan v1.0.5. Versi 1.0.6 (versi terkini) belum diuji ulang sebelum/sesudah di OpenClaw; menurut `CHANGELOG.md`, cara kerjanya tidak berubah dari 1.0.5.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Satu draf terjadwal sekali jalan terkirim sungguhan ke grup uji Telegram Komunitech pada 13 Okt 2026, tiba tepat waktu dengan total jam yang cocok; jadwal berulang tiap Jumat belum diuji (`examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`).

## FAQ
**Data pekerjaan klien saya dikirim ke internet?**
Tidak. Semua catatan tersimpan di satu file CSV di komputer Anda sendiri. Yang mengalir ke
penyedia model AI hanya teks percakapan biasa, sama seperti chat lainnya.

**Bisa langsung terkirim otomatis ke klien tiap minggu?**
Tidak, dan memang sengaja. Draf hanya disiapkan untuk Anda tinjau dan kirim sendiri — bahkan bila
dijadwalkan lewat OpenClaw, draf itu masuk ke Telegram **Anda sendiri**, bukan langsung
ke klien (WhatsApp hanya dengan nomor terpisah; lihat `references/openclaw-jadwal.md`).

**Bagaimana kalau saya lupa mencatat jam suatu pekerjaan?**
Boleh dikosongkan — laporan tetap dibuat, dan bagian Total Jam menandai jelas berapa entri yang
tidak ikut dihitung, supaya tidak disalahartikan sebagai 0 jam.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
