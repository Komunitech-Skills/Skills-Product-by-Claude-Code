# Ikut Tender Pemerintah Tanpa Gugur Konyol

**Asisten persiapan tender untuk UMKM: cek layak ikut, dokumen lengkap, jadwal tidak telat, harga dihitung benar.**

## Manfaat
- ✅ **Tahu layak ikut atau tidak dalam 5 menit** — cek kualifikasi usaha kecil, KBLI di NIB, NPWP/PKP, SBU/SKK, pengalaman, dan sisa kemampuan paket.
- ✅ **Checklist dokumen siap centang** per metode: tender, pengadaan langsung, e-katalog/e-purchasing.
- ✅ **Jadwal mundur otomatis** dari batas unggah (H-7, H-5, H-3, H-2, H-1), menghitung hari kerja & libur yang Anda sebut.
- ✅ **Harga penawaran diperiksa script**: volume × harga, PPN 12% × 11/12 (bila PKP), total, terbilang, persen terhadap HPS, dan peringatan otomatis bila melebihi HPS atau di bawah 80% HPS.
- ✅ **20 kesalahan yang paling sering menggugurkan** — ditunjukkan yang relevan dengan paket Anda.

## Cocok untuk siapa
- Pemilik CV/PT kecil, koperasi, atau usaha perorangan yang ingin mulai ikut pengadaan pemerintah di LPSE/SPSE.
- Admin tender yang ingin memeriksa ulang dokumen & harga sebelum unggah.
- Penyedia di e-katalog/toko daring pemerintah yang ingin rapi soal harga & dokumen.

## Contoh sebelum & sesudah
**Sebelum:** total di Excel salah karena satu baris terlewat, terbilang tidak sama dengan angka, dan unggah jam 13.55 untuk batas 14.00 — gagal karena server padat. Penawaran gugur.

**Sesudah (cukup ketik):** "Batas unggah 15 Oktober jam 14.00, HPS 45 juta, ini rincian harga saya: ..."
→ Tabel harga dihitung ulang (Rp39.750.000 = 88,33% HPS, aman), terbilang siap tempel, daftar tugas H-7 Selasa 6/10 s.d. unggah H-1 Rabu 14/10, checklist dokumen, dan 5 kesalahan gugur yang perlu diwaspadai.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Saya mau ikut tender pengadaan seragam di LPSE provinsi, apa saja yang harus disiapkan?"
- "Cek rincian penawaran ini, HPS Rp250 juta, saya PKP." (tempel tabel)
- "Bikinin jadwal persiapan, batas unggah 20 November jam 15.00, tanggal 25 libur."
- "CV saya KBLI 41012, SBU kecil, lagi pegang 3 proyek. Masih bisa ikut tender konstruksi?"

## Instalasi singkat
Salin folder `tender-checklist` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Script hanya butuh Python bawaan; tanpa Python pun skill tetap bekerja memakai rumus yang tertulis.

## FAQ
**Apakah skill ini menjamin saya menang tender?**
Tidak. Skill ini mengurangi risiko gugur karena kesalahan administrasi, dokumen, jadwal, dan hitungan. Menang-kalah tetap ditentukan evaluasi pokja dan harga pesaing.

**Aturannya kan sering berubah?**
Ringkasan aturan dicek per 25 September 2026 (Perpres 16/2018 jo. 12/2021 jo. 46/2025, Peraturan LKPP terbaru) lengkap dengan sumbernya. Acuan utama tetap dokumen pemilihan di SPSE — skill selalu mengingatkan hal ini.

**Bisa dipakai untuk "mengatur" pemenang atau pinjam bendera?**
Tidak. Skill akan menolak permintaan persekongkolan, pinjam bendera, dokumen palsu, atau gratifikasi karena melanggar hukum (UU 5/1999, UU Tipikor) dan berujung daftar hitam. Skill akan menawarkan jalur yang sah.

---
*Bukan nasihat hukum/pajak. Pembulatan PPN belum dicocokkan dengan Coretax.*
