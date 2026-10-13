# Arsip Nota Otomatis, Tanpa Langganan

**Nota & struk yang berantakan di HP jadi arsip rapi di komputer sendiri - cukup ngobrol.**

Diuji AI penguji independen di OpenClaw: 5,75 → 8,75 dari 10 (tanpa skill nominal "38,5" dicatat apa adanya dan file asli dipindah ke Trash; dengan skill nominal ditanyakan dulu, nota dobel diblokir, dan file asli tidak dihapus).

_Versi 1.0.6. Perubahan di 1.0.5 (30 Sep 2026): nominal yang meragukan seperti "1,5" atau "150,50" kini ditanyakan ulang, tidak lagi salah dibaca._

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ File foto/PDF nota diberi nama baku (`2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg`) dan tersusun otomatis per folder tahun/bulan - tidak perlu klik-klik Explorer/Finder satu-satu.
- ✅ Nota tercatat di satu indeks lokal (daftar catatan di komputer Anda): cari nota vendor tertentu atau rentang tanggal dalam hitungan detik, tanpa scroll ratusan foto.
- ✅ Ketahuan kalau ada nota yang kebetulan diarsipkan dua kali (isi file sama persis maupun kemungkinan dobel).
- ✅ Rekap pengeluaran per kategori/vendor sekali ketik, dan bisa diekspor langsung ke buku kas (`kas-umkm`).
- ✅ Data tersimpan di komputer sendiri, tanpa langganan bulanan dan tanpa upload ke internet. File nota asli **tidak dihapus** oleh skill (mode bawaan menyalin).

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

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.6; angka dari `examples/00-openclaw-sebelum-sesudah.md`), skor 1–10: tanpa skill **5,75** → dengan skill **8,75** (LULUS). Contoh nominal meragukan "38,5": dengan skill ditanyakan dulu apakah maksudnya Rp38.500 dan nota dobel diblokir (dikenali dari isi file yang sama); tanpa skill file asli dipindah ke Trash (tempat sampah). Terpisah dari uji OpenClaw: **44 dari 44** tes otomatis internal lolos (`examples/HASIL-UJI.md`).

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan Claude Code (simulasi agent). Belum uji bot Telegram asli. Codex dan Cursor belum uji platform asli. Bukan OCR — nominal dari pengguna/ekstrak-nota-faktur.

## FAQ
**File nota asli saya bisa hilang/terhapus?**
Tidak. Mode bawaan adalah **salin** — file asli tetap di tempatnya, hanya salinannya yang diarsipkan dan diberi nama baku. Ada juga mode "pindah" (opsional) yang hanya memindahkan file ke lokasi baru, dan skill tidak menghapus file.

**Skill ini bisa membaca angka di foto nota (OCR, membaca teks dari foto)?**
Tidak. arsip-nota khusus merapikan file & mencatat data yang sudah ada. Untuk membaca subtotal/PPN/total dari foto, pakai skill `ekstrak-nota-faktur`, lalu hasilnya dapat langsung diarsipkan oleh skill ini.

**Data saya dikirim ke internet?**
Tidak. Data (foto nota dan indeksnya) tersimpan di file di komputer Anda sendiri (indeksnya berupa satu file basis data SQLite), tidak ada langganan bulanan dan tidak ada yang diunggah.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
