# Arsip Nota Otomatis, Tanpa Langganan

**Nota & struk yang berantakan di HP jadi arsip rapi di komputer sendiri - cukup ngobrol.**

Diuji AI penguji independen di OpenClaw: 5,75 → 8,75 dari 10 (tanpa skill nominal "38.5" dicatat apa adanya dan file asli dipindah ke Trash (tempat sampah); dengan skill nominal ditanyakan dulu dan file asli tidak dihapus; nota dobel terdeteksi di kedua sisi, bedanya dengan skill ada pratinjau dan izin Anda dulu).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ File foto/PDF nota diberi nama baku (`2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg`) dan tersusun otomatis per folder tahun/bulan - tidak perlu klik-klik Explorer/Finder satu-satu.
- ✅ Nota tercatat di satu indeks lokal (daftar catatan di komputer Anda): cari nota vendor tertentu atau rentang tanggal lewat satu pertanyaan, tanpa scroll ratusan foto.
- ✅ Ketahuan kalau ada nota yang kebetulan diarsipkan dua kali (isi file sama persis maupun kemungkinan dobel).
- ✅ Rekap pengeluaran per kategori/vendor sekali ketik, dan bisa diekspor langsung ke skill buku kas Komunitech, `kas-umkm`.
- ✅ Arsip dan indeks tersimpan di komputer sendiri, tanpa langganan bulanan; skill ini tidak mengunggah apa pun. File nota asli **tidak dihapus** oleh skill (mode bawaan menyalin).

## Cocok untuk siapa
- Pemilik UMKM/toko yang notanya menumpuk di galeri HP dan sulit dicari saat butuh (klaim garansi, cek harga beli, laporan pajak).
- Freelancer/pemilik usaha kecil yang ingin arsip pengeluaran rapi tanpa berlangganan aplikasi arsip dokumen berbayar.
- Siapa pun yang sudah pakai `ekstrak-nota-faktur` untuk membaca isi nota, dan ingin hasilnya langsung tersimpan rapi.

## Contoh sebelum & sesudah
**Sebelum:** folder unduhan/galeri berisi `IMG_20260920_1.jpg`, `WhatsApp Image 2026-09-21.jpeg`, `Scan001.pdf` — tidak jelas nota siapa, tanggal berapa, atau sudah pernah dicatat belum.

**Sesudah (cukup ketik):** "Arsipkan dua nota ini: IMG_20260920_1.jpg dari Toko Sembako Bu Yati tanggal 20 September, 150 ribu. Terus WhatsApp-Image-2026-09-22.jpeg dari Toko C Elektronik tanggal 22 September, 50 ribu, buat beli kabel."

Cuplikan balasan (contoh dengan data fiktif dari `examples/01-arsipkan-nota-baru.md`):
```
Saya akan arsipkan (belum disimpan, file asli belum disalin):
1. IMG_20260920_1.jpg → `2026/09/2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg` — 20/09/2026, Rp 150.000, kategori Bahan baku (ditebak dari nama vendor)
2. WhatsApp-Image-2026-09-22.jpeg → `2026/09/2026-09-22_Toko-C-Elektronik_50000.jpeg` — 22/09/2026, Rp 50.000, kategori Peralatan (ditebak dari nama vendor), catatan "beli kabel"

File asli tetap ada di tempatnya (mode salin). Simpan? Balas "ya".
```
Setelah Anda membalas "ya": "Sudah tersimpan, 2 nota. File asli masih ada di folder aslinya (disalin, bukan dipindah). …"

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Rapikan nota-nota ini, tanggal dan nominalnya begini: ..."
- "Cari nota Toko Sembako Bu Yati bulan lalu"
- "Rekap pengeluaran per kategori bulan September"
- "Ada nota yang keinput dobel nggak?"

Untuk membaca angka dari foto nota (bukan sekadar arsip nama file), gunakan bersama skill `ekstrak-nota-faktur` (hasilnya dapat langsung diarsipkan oleh skill ini).

## Instalasi singkat
Salin folder `arsip-nota` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, 1 Okt 2026 (v1.0.6; angka dari `examples/00-openclaw-sebelum-sesudah.md`), skor 1–10: tanpa skill **5,75** → dengan skill **8,75** (LULUS). Contoh nominal meragukan "38.5": dengan skill ditanyakan dulu apakah maksudnya Rp38.500 dan nota dobel ditahan sebelum disimpan (dikenali dari isi file yang sama; tanpa skill dobelnya juga terdeteksi, tetapi langsung dipindah tanpa pratinjau); tanpa skill file asli dipindah ke Trash (tempat sampah). Catatan jujur: untuk satu struk, AI bisa meminta konfirmasi sampai 3 giliran chat sebelum tersimpan. Terpisah dari uji OpenClaw: pada uji awal v1.0.0, **44 dari 44** tes otomatis internal lolos (`examples/HASIL-UJI.md`); sejak itu tesnya ditambah.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan Claude Code (simulasi agent). Belum uji bot Telegram asli. Codex dan Cursor belum uji platform asli. Skill ini bukan OCR (pembaca teks dari foto): nominal berasal dari Anda atau dari skill `ekstrak-nota-faktur`.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: "tolong rapiin nota2 di folder nota/ ya. IMG_20260920_101.jpg itu nota Toko Bangunan Sinar Jaya 20/9/2026 Rp 1.250.000 beli semen. IMG_20260922_102.jpg bensin SPBU Pertamina 22/9/2026 150rb. faktur_listrik_sept.pdf tagihan…". Tanpa skill skor **7** → dengan skill skor **8** (selisih +1, belum lulus acuan kami: selisih 1 di bawah 1,5). DENGAN menyalin 3 nota ke arsip setelah konfirmasi dan membiarkan file asli utuh, sedangkan TANPA langsung mengganti nama file asli; nota dobel terdeteksi lewat isi file di kedua sisi dan rekapnya sama (Rp1.887.500). Catatan jujur: Perbandingan ini tidak bersih: kedua sisi memakai folder nota yang sama, dan sisi tanpa skill lebih dulu mengganti nama file asli, sehingga sisi dengan skill harus menjelaskan nama yang tidak cocok sebelum mengarsipkan. Rekap pengeluaran kedua sisi sama (Rp1.887.500); nota dobel terdeteksi di kedua sisi. Uji internal dengan skenario yang sama: 7 → 9. Akan diuji ulang dengan folder terpisah per sisi sebelum disimpulkan.

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: "tolong rapiin nota2 di folder nota/ ya. IMG_20260920_101.jpg itu nota Toko Bangunan Sinar Jaya 20/9/2026 Rp 1.250.000 beli semen. IMG_20260922_102.jpg bensin SPBU Pertamina 22/9/2026 150rb. faktur_listrik_sept.pdf tagihan…". Tanpa skill skor **7** → dengan skill skor **8,5** (selisih +1,5, tepat di batas lulus acuan kami). Dengan skill, bot lebih dulu menunjukkan rencana (nama file lama → nama baru di folder arsip/2026/09) dan baru menyalin setelah dijawab "ya". File asli tetap utuh dan foto dobel dilewati. Tanpa skill, bot langsung mengganti nama file asli dan memindahkan foto dobel tanpa bertanya. Catatan jujur: Perlu dua kali balas: bot menunjukkan rencana dulu, lalu menunggu jawaban "ya". Kategori ditebak dari nama penjual (semen masuk "Bahan baku") dan lokasi lengkap folder arsip di komputer tidak disebut di chat, jadi pembeli mungkin perlu menanyakannya atau mengoreksi kategorinya.

## FAQ
**File nota asli saya bisa hilang/terhapus?**
Skill ini tidak menghapus file Anda. Mode bawaan adalah **salin** — file asli tetap di tempatnya, hanya salinannya yang diarsipkan dan diberi nama baku. Ada juga mode "pindah" (opsional) yang hanya memindahkan file ke lokasi baru, dan skill tidak menghapus file.

**Skill ini bisa membaca angka di foto nota (OCR, membaca teks dari foto)?**
Tidak. arsip-nota khusus merapikan file & mencatat data yang sudah ada. Untuk membaca subtotal/PPN/total dari foto, pakai skill `ekstrak-nota-faktur`, lalu hasilnya dapat langsung diarsipkan oleh skill ini.

**Data saya dikirim ke internet?**
Skill ini sendiri tidak mengunggah apa pun: foto nota dan indeksnya tersimpan di komputer Anda sendiri (indeksnya berupa satu file basis data SQLite), tanpa langganan bulanan. Namun teks yang Anda ketik di chat tetap diproses oleh layanan AI yang Anda pakai.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
