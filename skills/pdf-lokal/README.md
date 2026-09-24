# PDF Lokal: Olah PDF di Komputer Sendiri, Tanpa Upload

**Gabung, kompres, OCR, kunci, dan rapikan PDF - lewat Stirling-PDF di laptopmu sendiri, bukan situs online.**

## Manfaat
- ✅ **Privasi terjaga** - file PDF (kontrak, slip gaji, KTP) tidak pernah diunggah ke
  situs "PDF online" pihak ketiga. Semua diproses di komputer sendiri.
- ✅ **Tanpa langganan** - Stirling-PDF gratis (inti open-source), tidak seperti Adobe
  Acrobat Pro (±USD20/bulan) atau situs kompres PDF berlangganan.
- ✅ **Cukup ngomong biasa** - "gabungin nota-nota ini" atau "kompres biar muat WA",
  AI agent yang urus perintah teknisnya.
- ✅ **Untuk kebutuhan usaha nyata**: kompres biar muat batas upload marketplace,
  rapikan resi biar hemat kertas print, OCR nota scan biar bisa dicari, kunci PDF
  slip gaji biar tidak sembarangan dibuka.
- ✅ **File asli aman** - hasil selalu file baru, file asli tidak pernah ditimpa.

## Cocok untuk siapa
- Pemilik toko online yang cetak banyak resi Shopee/Tokopedia setiap hari.
- Admin kantor/usaha yang sering gabung-pisah-kompres kontrak, nota, laporan.
- Siapa pun yang perlu kunci PDF berisi data sensitif (gaji, kontrak) sebelum dikirim.
- Yang scan dokumen fisik dan butuh hasilnya bisa dicari/di-copy teksnya (OCR).

## Contoh sebelum & sesudah
**Sebelum:** Buka Adobe Acrobat / cari-cari situs kompres PDF online, upload satu-satu,
was-was data ikut ke server orang, hasil kadang ada watermark iklan situsnya.

**Sesudah (cukup ketik):** "Kompres PDF laporan-keuangan.pdf ini biar bisa dikirim WA"
→ AI agent menjalankan skill ini, PDF diproses **di komputer sendiri** lewat
Stirling-PDF, hasil langsung ada di folder yang sama:
```
Berhasil dikompres: 4200 KB -> 850 KB
  -> /Users/sari/Dokumen/laporan-keuangan-kompres.pdf
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Gabungin nota-nota supplier ini jadi satu PDF"
- "Kompres PDF ini biar bisa diupload ke marketplace"
- "PDF hasil scan ini teksnya nggak bisa dicari, tolong OCR"
- "Ubah 5 foto struk ini jadi satu PDF"
- "Kunci PDF slip gaji karyawan pakai kata sandi"
- "Susun 8 resi Shopee ini jadi 4 per lembar biar hemat kertas"

**Syarat:** aplikasi **Stirling-PDF** harus sudah terpasang & menyala di komputer yang
sama (gratis, sekali pasang ±5 menit). Panduan lengkap ada di `docs/panduan-stirling-pdf.md`
yang ikut dalam paket. Kalau belum sempat memasangnya, skill ini tetap memandu langkah
manual klik-klik di aplikasinya (lihat SKILL.md bagian "Cara manual tanpa script").

## Instalasi singkat
Salin folder `pdf-lokal` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` dan
`docs/panduan-stirling-pdf.md` (pasang Stirling-PDF-nya) di dalam paket.

## Status pengujian (jujur, biar tidak salah ekspektasi)
- Script **sudah diuji nyala ke Stirling-PDF sungguhan versi 2.14.3** (lewat Docker,
  karena lingkungan pembuatan skill ini tidak punya installer desktop) untuk SEMUA
  perintah: cek, gabung, pisah-halaman, pisah-rentang, kompres, OCR, foto-ke-pdf,
  putar, watermark, kunci, buka-kunci, rapikan-resi - semua berhasil memanggil API asli
  dan menghasilkan file PDF nyata. Detail di `references/sumber-api-stirling.md`.
- Selain itu ada rangkaian tes otomatis (`tests/uji_regresi.py`) yang memakai server
  tiruan, supaya bisa dijalankan ulang kapan saja tanpa perlu memasang Stirling-PDF.
- **Belum diuji oleh manusia di aplikasi desktop resmi Stirling-PDF (.msi Windows /
  .dmg macOS)**, dan belum diuji di OpenClaw/Codex/Cursor sungguhan - baru simulasi
  agent (Claude Code). Uji platform asli & beta tester menyusul sebelum status `rilis`.

## FAQ
**Apakah file PDF-ku dikirim ke internet?**
Tidak. Skill ini hanya berbicara ke `http://localhost:8080` - alamat Stirling-PDF di
komputermu sendiri. Tidak ada data yang keluar dari komputer kamu, selama kamu tidak
sengaja mengarahkannya ke server lain.

**Stirling-PDF itu apa, harus bayar tidak?**
Aplikasi PDF gratis & open-source yang jalan di komputer sendiri (bukan situs web).
Fitur yang dipakai skill ini semuanya gratis (bagian inti/MIT). Ada fitur tambahan
berbayar milik Stirling-Tools sendiri (tanda tangan sertifikat, SSO, tim) yang **tidak**
dipakai/dibutuhkan skill ini.

**Kalau saya belum pasang Stirling-PDF, skill ini percuma?**
Tidak - skill tetap memandu kamu langkah demi langkah lewat aplikasi Stirling-PDF
secara manual (klik-klik), dan `docs/panduan-stirling-pdf.md` menuntun pemasangannya
dari nol (±5-10 menit, gratis).
