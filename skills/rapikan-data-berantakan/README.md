# Rapikan Data Pelanggan dan Penjualan Berantakan

**Nama, nomor HP, tanggal, dan harga yang kacau jadi seragam dalam satu perintah; setiap perubahan dilaporkan, dan data yang tidak bisa dibaca dibiarkan, tidak ditebak.**

Diuji AI penguji independen di OpenClaw: 3,5 → 9,0 dari 10 (nomor HP, tanggal, dan harga diseragamkan dengan ringkasan angka tetap, tanpa menggabungkan nama diam-diam); di bot Telegram asli selisihnya kecil (7 → 7,5), lihat bukti di bawah.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Nomor HP seragam:** `0812-3450-0101`, `+62 812 3450 0101`, `812 3450 0101` jadi satu bentuk, `6281234500101`.
- ✅ **Tanggal dan harga terbaca:** "7 Okt 2026", "05/10/26" jadi `2026-10-07`; "Rp 1.250.000,-", "150rb", "1,5jt" jadi angka biasa yang bisa dijumlah.
- ✅ **Pelanggan dobel ketahuan:** nama mirip ("Budi Santoso", "Santoso Budi", "Bpk. Budi Santosa") dan baris kembar ditandai. Anda yang memutuskan digabung atau tidak.
- ✅ **Hati-hati dan jujur:** skill dirancang tidak menimpa file asli; yang tidak bisa dibaca dibiarkan dan dilaporkan alasannya, tidak ditebak.
- ✅ **Alat perapi berjalan di komputer Anda:** tanpa akun dan tanpa aplikasi tambahan (isi data tetap dibaca AI agent yang Anda pakai; lihat FAQ).

## Cocok untuk siapa
- Pemilik toko online, kafe, katering, dan jasa yang daftar pelanggannya menumpuk dari WhatsApp, Shopee, Tokopedia, kasir, dan Excel yang diketik banyak orang.
- Admin yang harus menyatukan data sebelum membuat laporan atau memindahkannya ke aplikasi kasir/akuntansi.
- Siapa pun yang pernah melihat Excel penuh "Rp", titik, strip, dan tanggal campur aduk.

## Contoh sebelum & sesudah
**Sebelum** (ekspor asli, 5 baris dari 40):

| Nama | No HP | Tanggal | Total |
|---|---|---|---|
| budi santoso | 081234500101 | 05/10/2026 | Rp 150.000 |
| Bpk. Budi Santoso | 62812 3450 0101 | 7 Okt 2026 | 150rb |
| Muh. Rizal Pratama | 089900003030 | 2026/10/07 | 2,5jt |
| siti  rahmawati | +6285770000202 | Senin, 5 Oktober 2026 | 1.2jt |
| Joko Susilo | 6.28123E+11 | 15/10/2026 | 15.000 |

**Sesudah (cukup ketik):** "Tolong rapikan data pelanggan di ekspor-oktober.csv" (file tabel hasil ekspor)

| Nama | No HP | Tanggal | Total | Catatan |
|---|---|---|---|---|
| Budi Santoso | 6281234500101 | 2026-10-05 | 150000 | tanggal ambigu; nama mirip kelompok #1 |
| Bpk. Budi Santoso | 6281234500101 | 2026-10-07 | 150000 | nama mirip kelompok #1 |
| Muh. Rizal Pratama | 6289900003030 | 2026-10-07 | 2500000 | nama mirip kelompok #2 |
| Siti Rahmawati | 6285770000202 | 2026-10-05 | 1200000 | |
| Joko Susilo | 6.28123E+11 (dibiarkan) | 2026-10-15 | 15000 | nomor rusak karena Excel, perlu ekspor ulang |

→ Anda juga menerima ringkasan: berapa yang diperbaiki per jenis, nama mana yang tampaknya sama, baris kembar, dan sel yang tidak bisa dibaca beserta alasannya.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Tolong rapikan daftar pelanggan ini" (lalu kirim file tabel hasil ekspor Excel/aplikasi kasir, bentuk CSV)
- "Cek ada pelanggan dobel nggak di data ini?"
- "Seragamkan semua nomor HP jadi format 62"
- "Tanggalnya campur-campur, tolong dirapikan"

Agent akan merapikan dulu, menunjukkan hasilnya, lalu bertanya hanya hal yang perlu keputusan Anda (misalnya nama mana yang boleh digabung).

## Syarat
File berformat **CSV** (file tabel biasa; Excel: *File > Save As > CSV UTF-8*; Google Sheets: *File > Download > CSV*). Butuh Python di komputer (biasanya sudah ada di Mac/Linux; di Windows gratis dari python.org). Jika Python tidak ada, agent merapikan manual untuk data kecil.

## Instalasi singkat
Salin folder `rapikan-data-berantakan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw 5 Okt 2026 (uji otomatis agent, diuji pada v1.0.1, 2 skenario), skor 1–10 penguji independen: tanpa skill **3,5** → dengan skill **9,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md` dan `examples/HASIL-UJI.md`. Di bot Telegram asli selisihnya jauh lebih kecil (7 → 7,5, verdik BELUM; lihat bagian berikutnya): di sana AI tanpa skill sudah memberi tabel pelanggan bersih langsung di chat.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 11, 2026-10-06.
- Tanpa skill: https://t.me/c/4407409583/900/934 — skor 7
- Dengan skill: https://t.me/c/4407409583/901/936 — skor 7,5 (kirim ulang: 8)
Verdik gelombang: BELUM — Dengan skill tidak ada data yang digabung diam-diam dan ada pengingat opt-in, tetapi tanpa skill bot sudah memberi CSV 18 pelanggan bersih dengan angka benar langsung di chat, sedangkan dengan skill data bersih baru dikirim setelah "kirim file" dan contoh percobaan 1 salah satu digit.

## FAQ
**Apakah data pelanggan saya dikirim ke internet?**
Alat perapi berjalan di komputer Anda sendiri dan tidak mengakses internet. Isi data tetap dibaca oleh AI agent yang Anda pakai, jadi pilih agent yang sesuai kebijakan privasi usaha Anda. Nama dan nomor pelanggan adalah data pribadi (UU PDP No. 27/2022): jangan dibagikan ke grup atau pihak lain tanpa perlu, dan nomor yang sudah rapi bukan izin untuk mengirim promo.

**Apakah nama yang mirip langsung digabung?**
Tidak. Nama mirip hanya ditandai dan diusulkan nama bakunya. Baris kembar juga hanya ditandai, kecuali Anda minta dibuang (itu pun disimpan di berkas terpisah). Yang diubah otomatis hanya format: spasi, huruf besar-kecil, nomor HP, tanggal, dan harga.

**Nomor HP saya jadi 6,28E+11 saat dibuka di Excel. Kenapa?**
Itu kebiasaan Excel menampilkan angka panjang sebagai notasi ilmiah, bukan kesalahan data. Minta agent membuat versi "untuk Excel" (nomor ditulis khusus agar tampil utuh), atau impor file lewat *Data > From Text/CSV* dan atur kolom HP sebagai Teks.

## Catatan sumber
Gagasan pengelompokan nama mirip terinspirasi konsep "cluster and edit" di OpenRefine (BSD-3-Clause), dan prinsip tabel rapi diadaptasi dari pelajaran Data Carpentry oleh The Carpentries (CC BY 4.0). Kode dan teks ditulis ulang sendiri; keduanya tidak berafiliasi dengan skill ini. Rincian: `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.2**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
