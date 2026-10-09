# Pasang & nyalakan Stirling-PDF (ringkas, untuk dibacakan agent ke pengguna)

Stirling-PDF = aplikasi PDF gratis (inti berlisensi MIT) yang jalan **di komputer sendiri**.
Wajib hanya untuk: **OCR, watermark, foto ke PDF, rapikan resi**. Untuk gabung, pisah,
kompres, putar, kunci/buka sandi, skill ini bisa memakai jalur cadangan (`scripts/pdf_cadangan.py`)
bila qpdf/Ghostscript/pdftk sudah ada. **Agent tidak memasang apa pun sendiri**: bacakan
langkah di bawah, pengguna yang menjalankan. Tidak mau repot → jasa setup berbayar Komunitech.

Sumber: docs.stirlingpdf.com (Installation, Configuration/Security; diakses 2026-09-24) +
uji langsung Komunitech dengan image Docker resmi v2.14.3 & v3.0.0.

## Jalur A — Aplikasi desktop (±5 menit, TANPA OCR)
Unduh hanya dari tautan resmi:
- Windows: https://files.stirlingpdf.com/win-installer.exe → jalankan → buka "Stirling PDF" dari Start Menu.
  SmartScreen memblokir → **More info → Run anyway** (sumber resmi).
- macOS: https://files.stirlingpdf.com/mac-installer.dmg → seret ke Applications. Muncul
  "pengembang tidak dikenal" → System Settings → Privacy & Security → **Open Anyway**.
- Linux Debian/Ubuntu: unduh `https://files.stirlingpdf.com/linux-installer.deb` lalu
  `sudo apt install ./linux-installer.deb` (Fedora: `.rpm` + `sudo dnf install`).

Catatan: mode bawaan desktop ("Local-only") **tidak menyertakan OCR** dan konversi dokumen.
Butuh OCR → Jalur B. Belum diuji klik langsung oleh Komunitech (hanya dari dokumentasi resmi).

## Jalur B — Docker (±5–10 menit bila Docker Desktop sudah ada; ±20–40 menit bila belum)
1. Pasang Docker Desktop dari https://www.docker.com/products/docker-desktop/ (Windows sering
   minta pasang WSL2 + restart sekali). Buka Docker Desktop sampai status "Running".
2. Di Terminal/PowerShell, salin persis (baris `SECURITY_ENABLELOGIN=false` **wajib**; tanpa
   itu server tampak hidup tapi semua operasi ditolak 401):
   ```
   docker run -d --name stirling-pdf --restart unless-stopped -p 8080:8080 -e SECURITY_ENABLELOGIN=false -v stirling-data:/configs ghcr.io/stirling-tools/stirling-pdf:3.0.0
   ```
   Tag dipin ke `3.0.0` (sudah diuji) supaya versi tidak berganti diam-diam.
3. Sudah pernah dipasang tapi mati → `docker start stirling-pdf` (atau buka Docker Desktop).

## Cek berhasil
`python3 scripts/pdf.py cek` (Windows: `py scripts\pdf.py cek`) harus berakhir dengan
**"Operasi PDF diizinkan. Siap dipakai."** — "HIDUP" saja belum cukup.

## Masalah umum
| Gejala | Solusi |
|---|---|
| "Tidak bisa menghubungi" | Aplikasi belum dibuka / container mati → buka aplikasi atau `docker start stirling-pdf` |
| HIDUP tapi "menolak operasi PDF" (401/403) | Container dibuat tanpa `-e SECURITY_ENABLELOGIN=false` → `docker rm -f stirling-pdf`, jalankan ulang perintah langkah 2 (data tidak hilang). Login sengaja aktif → Settings ⚙️ → Account Settings → salin API Key → set `STIRLING_API_KEY` |
| `ocr` 404 | Memakai desktop Local-only → pakai Jalur B, lalu (opsional) desktop: Settings → Connection → Self-hosted server → `http://localhost:8080` |
| "port is already allocated" | Ganti `-p 8090:8080` dan set `STIRLING_URL=http://localhost:8090` |
| OCR Indonesia kurang akurat | Paket bahasa `ind` belum ada di server; script otomatis memakai `eng` dan memberi tahu |

## Keamanan
- Port `8080` hanya untuk komputer sendiri; **jangan** dibuka ke internet lewat router.
- Komputer dipakai bersama → ganti ke `-e SECURITY_ENABLELOGIN=true`, login awal `admin`/`admin`
  (segera ganti sandi), lalu pakai API key seperti di tabel.
