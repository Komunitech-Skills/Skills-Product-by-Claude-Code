# PDF Lokal: Olah PDF di Komputer Sendiri, Tanpa Upload

**Gabung, kompres, OCR, kunci, dan rapikan PDF - di laptopmu sendiri, bukan situs online. Belum pasang Stirling-PDF? Tugas umum tetap jalan dengan alat PDF yang sudah ada di komputermu.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Privasi terjaga** - script ini hanya bicara ke Stirling-PDF di komputer sendiri
  (`localhost`), tidak pernah mengunggah file ke situs "PDF online" mana pun. Untuk
  dokumen sensitif (slip gaji, KTP, kontrak), skill ini tidak akan menyarankan upload
  ke situs online mana pun sebagai jalan pintas, sekalipun Stirling-PDF belum terpasang.
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

**Syarat:** paling lengkap dengan aplikasi gratis **Stirling-PDF** yang menyala di komputer
yang sama (panduan ringkas: `references/pasang-stirling.md` di folder skill ini).
**Belum ada Stirling-PDF?** Untuk gabung, pisah, kompres, putar, dan kunci/buka sandi,
AI agent otomatis memakai alat PDF yang **sudah** terpasang di komputermu (qpdf,
Ghostscript, atau pdftk - umum ada di Linux/macOS dan sebagian Windows), tanpa memasang
apa pun. OCR, watermark, foto ke PDF, dan rapikan resi tetap butuh Stirling-PDF.

## Instalasi singkat
Salin folder `pdf-lokal` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap memasang skill (termasuk Windows): `docs/instalasi.md` di ZIP paket.
Cara memasang Stirling-PDF: `references/pasang-stirling.md` di dalam folder skill ini.

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi, qpdf/Ghostscript tersedia), 1 Okt 2026 (v1.0.5), skor 1–10 penguji independen: tanpa skill **8,75** → dengan skill **9,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Pembeda bukan “mustahil tanpa skill”, melainkan konsistensi aman: tanpa pip install, tanpa unggah PDF sensitif, file asli tidak ditimpa, verifikasi ukuran/hasil. Script juga diuji ke Stirling-PDF 2.14.3 & 3.0.0 (Docker) — detail di `examples/HASIL-UJI.md` (16/16 regresi tiruan).

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01; uji muat CLI) dan Claude Code (simulasi agent). Belum uji manusia di installer desktop Stirling-PDF (.msi/.dmg). Codex dan Cursor belum uji platform asli.

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
Tidak. Gabung, pisah, kompres, putar, dan kunci sandi tetap dikerjakan dengan alat PDF
yang sudah ada di komputermu (qpdf/Ghostscript/pdftk), tanpa memasang apa pun. Kalau alat
itu juga tidak ada, AI memandu cara manual (Preview di Mac, "Microsoft Print to PDF" di
Windows) dan `references/pasang-stirling.md` menuntun pemasangan Stirling-PDF (gratis).

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
