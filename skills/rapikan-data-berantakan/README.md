# Rapikan Data Pelanggan dan Penjualan Berantakan

**Nama, nomor HP, tanggal, dan harga yang kacau jadi seragam dalam satu perintah, tanpa ada data yang hilang diam-diam.**

## Manfaat
- ✅ **Nomor HP seragam:** `0812-3450-0101`, `+62 812 3450 0101`, `812 3450 0101` jadi satu bentuk, `6281234500101`.
- ✅ **Tanggal dan harga terbaca:** "7 Okt 2026", "05/10/26" jadi `2026-10-07`; "Rp 1.250.000,-", "150rb", "1,5jt" jadi angka biasa yang bisa dijumlah.
- ✅ **Pelanggan dobel ketahuan:** nama mirip ("Budi Santoso", "Santoso Budi", "Bpk. Budi Santosa") dan baris kembar ditandai. Anda yang memutuskan digabung atau tidak.
- ✅ **Aman dan jujur:** file asli tidak pernah ditimpa; yang tidak bisa dibaca dibiarkan dan dilaporkan alasannya, tidak ditebak.
- ✅ **Data tetap di komputer Anda:** tanpa akun, tanpa instalasi aplikasi tambahan.

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

**Sesudah (cukup ketik):** "Tolong rapikan data pelanggan di ekspor-oktober.csv"

| Nama | No HP | Tanggal | Total | Catatan |
|---|---|---|---|---|
| Budi Santoso | 6281234500101 | 2026-10-05 | 150000 | tanggal ambigu; nama mirip kelompok #1 |
| Bpk. Budi Santoso | 6281234500101 | 2026-10-07 | 150000 | nama mirip kelompok #1 |
| Muh. Rizal Pratama | 6289900003030 | 2026-10-07 | 2500000 | nama mirip kelompok #2 |
| Siti Rahmawati | 6285770000202 | 2026-10-05 | 1200000 | |
| Joko Susilo | 6.28123E+11 (dibiarkan) | 2026-10-15 | 15000 | nomor rusak karena Excel, perlu ekspor ulang |

→ Anda juga menerima ringkasan: berapa yang diperbaiki per jenis, nama mana yang tampaknya sama, baris kembar, dan sel yang tidak bisa dibaca beserta alasannya.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Tolong rapikan daftar pelanggan ini" (lalu kirim file CSV)
- "Cek ada pelanggan dobel nggak di data ini?"
- "Seragamkan semua nomor HP jadi format 62"
- "Tanggalnya campur-campur, tolong dirapikan"

Agent akan merapikan dulu, menunjukkan hasilnya, lalu bertanya hanya hal yang perlu keputusan Anda (misalnya nama mana yang boleh digabung).

## Syarat
File berformat **CSV** (Excel: *File > Save As > CSV UTF-8*; Google Sheets: *File > Download > CSV*). Butuh Python di komputer (biasanya sudah ada di Mac/Linux; di Windows gratis dari python.org). Jika Python tidak ada, agent merapikan manual untuk data kecil.

## Instalasi singkat
Salin folder `rapikan-data-berantakan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah data pelanggan saya dikirim ke internet?**
Alat perapi berjalan di komputermu sendiri dan tidak mengakses internet. Isi data tetap dibaca oleh AI agent yang kamu pakai, jadi pilih agent yang sesuai kebijakan privasi usahamu. Nama dan nomor pelanggan adalah data pribadi (UU PDP No. 27/2022): jangan dibagikan ke grup atau pihak lain tanpa perlu, dan nomor yang sudah rapi bukan izin untuk mengirim promo.

**Apakah nama yang mirip langsung digabung?**
Tidak. Nama mirip hanya ditandai dan diusulkan nama bakunya. Baris kembar juga hanya ditandai, kecuali kamu minta dibuang (itu pun disimpan di berkas terpisah). Yang diubah otomatis hanya format: spasi, huruf besar-kecil, nomor HP, tanggal, dan harga.

**Nomor HP saya jadi 6,28E+11 saat dibuka di Excel. Kenapa?**
Itu kebiasaan Excel menampilkan angka panjang sebagai notasi ilmiah, bukan kesalahan data. Minta agent membuat versi "untuk Excel" (nomor ditulis khusus agar tampil utuh), atau impor file lewat *Data > From Text/CSV* dan atur kolom HP sebagai Teks.

## Catatan versi
- **1.0.1 (2026-10-05):** nomor baris di balasan kini selalu disalin dari laporan alat (bukan kolom "No" atau dihitung sendiri); telepon rumah/kantor (021, 022, 0274, ...) tidak lagi masuk kolom HP/WhatsApp, dipisah ke kolom `_telepon_rumah`; sel berisi dua nomor dipisah (nomor seluler pertama jadi HP, sisanya dicatat); ringkasan angka tetap ("blok angka") yang wajib disalin utuh, juga di chat Telegram/WhatsApp; daftar baris kembar tetap dari alat walau sebagian permintaan ditolak.
- **1.0.0:** rilis awal.

## Catatan sumber
Gagasan pengelompokan nama mirip terinspirasi konsep "cluster and edit" di OpenRefine (BSD-3-Clause), dan prinsip tabel rapi diadaptasi dari pelajaran Data Carpentry oleh The Carpentries (CC BY 4.0). Kode dan teks ditulis ulang sendiri; keduanya tidak berafiliasi dengan skill ini. Rincian: `ATTRIBUTION.md`.
