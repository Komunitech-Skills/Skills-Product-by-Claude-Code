# Buku Piutang Tanpa Langganan, Cukup Lewat Chat

**Tahu siapa yang belum bayar, berapa, dan sejak kapan (sesuai catatan Anda). Pesan tagihan yang sopan sudah disiapkan. Data tetap di komputer Anda sendiri.**

*Diuji AI penguji independen: 5,75 → 8,75 dari 10 (tanpa skill agent bersedia membuat jadwal WhatsApp tagihan otomatis; dengan skill ia menolak, menyiapkan draf untuk dikirim sendiri, dan kelebihan bayar ditanyakan dulu).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Bon tidak mudah terlupa.** Setiap pagi Anda tahu tagihan yang **terlewat**, yang **jatuh tempo hari ini**, dan yang **jatuh tempo minggu ini**, lengkap dengan sisa dan berapa kali sudah diingatkan. Bisa dikirim otomatis ke Telegram Anda (OpenClaw; jadwal otomatis diuji di bot Telegram uji 13 Okt 2026).
- ✅ **Pembayaran dicicil pun tetap rapi.** "Kafe Senja transfer 1 juta" langsung dipotong dari nota tertua dan sisanya dihitung. Kalau pelanggan membayar **lebih**, buku tidak diam-diam jadi minus: Anda ditanya dulu, lalu kelebihannya disimpan sebagai deposit atau dicatat sudah dikembalikan.
- ✅ **Pesan tagihan siap kirim dalam satu klik.** Nadanya menyesuaikan: pengingat halus sebelum jatuh tempo, "hari ini jatuh tempo", sampai menanyakan rencana bayar untuk yang lama menunggak. Tanpa ancaman, tanpa denda karangan. Klik tautan, WhatsApp terbuka dengan teks terisi, periksa, lalu tekan Kirim sendiri.
- ✅ **Laporan yang biasanya ada di aplikasi akuntansi berbayar.** Saldo per pelanggan, **umur piutang** (berapa lama tagihan tertunggak: belum jatuh tempo, 1–30, 31–60, 61–90, lebih dari 90 hari), rekap bulanan (piutang baru, uang masuk, posisi akhir bulan). Semua angka dihitung script dan rumusnya bisa ditampilkan.
- ✅ **Pindah dari buku/Excel tanpa ketik ulang.** Impor daftar bon dari Excel atau ekspor kasir (file CSV, tabel sederhana yang bisa dibuka di Excel). Baris yang bermasalah (tanggal ngawur, nominal minus, nota dobel) disebutkan nomor barisnya dan tidak ikut masuk. Ada cadangan otomatis.

## Cocok untuk siapa
- Toko grosir/sembako, distributor, agen, toko bangunan, supplier bahan kafe/katering yang menjual dengan **bon atau tempo** ke warung, kafe, atau kantor.
- Usaha jasa B2B (percetakan, konveksi, servis, konsultan) yang menagih invoice ke klien dengan termin 14/30 hari.
- Pemilik atau admin keuangan yang selama ini mencatat piutang di buku tulis, Excel, atau ingatan.
- Member yang memakai OpenClaw dan ingin ringkasan piutang masuk Telegram tiap pagi.

**Kurang cocok:** usaha yang butuh pembukuan lengkap (jurnal, neraca, hutang ke pemasok) atau dipakai banyak orang di banyak komputer sekaligus. Skill ini juga sengaja tidak mengirim pesan tagihan sendiri.

## Contoh sebelum & sesudah
**Sebelum:** bon ditulis di buku, sebagian di chat WA. Sudah dibayar sebagian atau belum, lupa. Akhir bulan tidak tahu total uang yang masih di luar, dan menagih terasa canggung karena tidak ada kalimat yang pas.

**Sesudah (cukup ketik):** "Tagihan yang jatuh tempo apa saja?"
```
JATUH TEMPO PIUTANG - Sabtu, 26 September 2026 (WIB)
Terlewat: Rp 1.400.000 (1 nota) | Hari ini: Rp 0 (0) | 7 hari ke depan: Rp 350.000 (1)

TERLEWAT (1 nota, Rp 1.400.000)
1. B-0905 | Kafe Senja (P0002) | sisa Rp 1.400.000 dari Rp 2.400.000 | JT 12 Sep 2026 (lewat 14 hari)

MINGGU INI (besok s.d. 3 Okt 2026) (1 nota, Rp 350.000)
1. B-0920 | Pak Joko (P0004) | sisa Rp 350.000 | JT 27 Sep 2026 (1 hari lagi)
```
Lalu: "Bikinin pesan tagihan buat Kafe Senja."
```
Halo Bapak/Ibu di Kafe Senja, semoga sehat selalu. Saya Sari dari Toko Sembako Berkah.

Kami ingin menanyakan tagihan berikut yang sudah melewati jatuh tempo:
- Nota B-0905 (5 Sep 2026): sisa Rp 1.400.000, jatuh tempo 12 Sep 2026

Pembayaran bisa ditransfer ke BCA 0000000000 a.n. Sari (contoh).
Mohon dibantu informasikan kapan rencana pembayarannya, supaya bisa kami catat. Kalau sudah
membayar, mohon kirimkan bukti transfernya.
Terima kasih atas perhatiannya.
```
(Contoh lengkap dengan data fiktif: `examples/contoh-sesi-toko-sembako.md`.)

## Cara pakai
Setelah terpasang, cukup ketik ke AI agent Anda, misalnya:
- "Pakai buku piutang untuk toko saya, nama tokonya Toko Sembako Berkah, rekening BCA ..." (sekali di awal)
- "Catat bon Warung Bu Tini 1.250.000, nota B-0901, tempo 2 minggu"
- "Invoice CV Maju Jaya DPP 10 juta plus PPN, tempo 30 hari" (DPP = harga sebelum PPN)
- "Kafe Senja transfer 1 juta" / "Bu Tini bayar lunas" / "Pak Joko bayar 400 ribu, utangnya cuma 350"
- "Siapa saja yang belum bayar?" / "Umur piutang akhir bulan" / "Saldo Kafe Senja"
- "Bikinin pesan tagihan untuk Kafe Senja" → klik tautan, kirim sendiri, lalu bilang "sudah kukirim"
- "Masukkan daftar bon dari Excel ini" (kirim file CSV) / "Rekap piutang bulan ini" / "Ekspor ke Excel"
- "Kirim ringkasan piutang ke Telegram saya tiap pagi" (OpenClaw; jadwal otomatis diuji di bot Telegram uji 13 Okt 2026)

## Instalasi singkat
Salin folder `buku-piutang` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

Butuh **Python 3.8+** (gratis di python.org; Mac/Linux biasanya sudah ada). Tidak butuh internet, akun, atau API key. Data tersimpan di folder `KomunitechData/piutang/` di komputer Anda, dengan cadangan otomatis di `KomunitechData/piutang/backup-piutang/`. Tanpa Python pun skill tetap membantu dengan tabel piutang manual di Excel.

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, di OpenClaw (uji otomatis agent, 1 Oktober 2026; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 5,75 tanpa skill menjadi 8,75 dengan skill. Untuk mencatat bon dan mengecek yang telat, kedua sisi sama-sama benar (7 vs 8,5). Pembeda besarnya di keamanan dan pembukuan: tanpa skill agent bersedia membuat jadwal WhatsApp tagihan otomatis (berisiko nomor diblokir) dan salah mengganti nama pelanggan; dengan skill ia menolak kirim otomatis, menyiapkan draf dan tautan untuk dikirim sendiri, dan kelebihan bayar tidak ditebak (ditanyakan dulu, lalu piutang Rp 0 dan deposit Rp 50.000).

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Jadwal kirim otomatis ke Telegram: diuji di bot Telegram uji 13 Okt 2026 (ringkasan harian one-shot ~5 menit, angka Rp 1.300.000 / terlewat Rp 800.000 cocok; lihat `examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`).

## Yang perlu Anda tahu (jujur)
- **Tidak mengirim pesan sendiri.** Skill hanya menyiapkan draf + tautan WhatsApp (wa.me); Anda yang menekan Kirim. Ini disengaja: kiriman otomatis lewat WhatsApp tidak resmi bisa membuat nomor diblokir.
- **Tidak membaca mutasi bank otomatis.** Pembayaran dicatat dari cerita Anda atau bukti transfer yang Anda tempel.
- **Bukan pengganti faktur pajak.** PPN dihitung dari harga sebelum PPN (DPP) dan dibulatkan ke bawah, tapi pembulatannya belum dicocokkan dengan Coretax (sistem pajak online milik DJP). Faktur pajak resmi tetap lewat Coretax.
- **Bukan pembukuan lengkap.** Tidak ada jurnal, laba rugi, atau hutang ke pemasok.
- **Satu komputer, satu file data.** Jangan buka file yang sama dari dua komputer lewat Google Drive/Dropbox.
- **Data pribadi pelanggan.** Nama, nomor HP, dan utang pelanggan hanya tersimpan di komputer Anda. Ringkasan ke Telegram disarankan versi disamarkan (nama jadi inisial).
- Ringkasan terjadwal hanya berjalan saat komputer dan Gateway OpenClaw (program OpenClaw yang berjalan di latar belakang) menyala. Jadwal otomatis ke Telegram sudah diuji di bot uji 13 Okt 2026 (Gateway VM Cursor).
- Alat bantu pencatatan dan penagihan, bukan nasihat keuangan, pajak, atau hukum. Sengketa utang yang besar sebaiknya dibawa ke advokat.

## FAQ
**Kalau pelanggan membayar lebih dari utangnya, bagaimana?**
Buku tidak langsung mencatatnya. Anda ditanya dulu: kelebihannya disimpan sebagai deposit (otomatis bisa dipakai untuk bon berikutnya), sudah Anda kembalikan, atau untuk nota lain. Jadi saldo tidak menjadi minus tanpa sepengetahuan Anda.

**Saya sudah punya daftar bon di Excel. Harus ketik ulang?**
Tidak. Simpan sebagai CSV (Excel: *Save As → CSV*), kirim ke agent, lalu periksa pratinjaunya. Tanggal harus hari/bulan/tahun; kalau file Anda ternyata memakai format bulan/hari (gaya Amerika), impor ditolak dulu supaya tanggal tidak tertukar diam-diam. Impor ulang file yang sama tidak membuat data dobel.

**Apakah data pelanggan saya dikirim ke internet?**
Tidak. Script buku piutang tidak memakai internet sama sekali; semuanya ada di satu file di komputer Anda. Yang keluar hanya ringkasan yang Anda minta dikirim ke Telegram Anda sendiri (lewat OpenClaw) dan pesan yang Anda kirim sendiri lewat WhatsApp.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
