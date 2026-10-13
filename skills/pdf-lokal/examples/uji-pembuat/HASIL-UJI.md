# Hasil uji pdf-lokal (v1.0.0)

Tanggal: 2026-09-24. Diuji oleh: agent pembuat skill ini (belum oleh penguji independen
terpisah - lihat catatan di bawah).

## Ringkasan
- **Server sungguhan:** Stirling-PDF **v2.14.3** (Docker, `ghcr.io/stirling-tools/
  stirling-pdf:latest`, digest `sha256:3b3670fce...`), dijalankan ±20 menit untuk
  memverifikasi SEMUA 12 perintah `scripts/pdf.py` berhasil memanggil API asli:
  `cek`, `gabung`, `pisah-halaman`, `pisah-rentang`, `kompres`, `ocr`, `foto-ke-pdf`,
  `putar`, `watermark`, `kunci`, `buka-kunci`, `rapikan-resi`. Semua menghasilkan file
  PDF valid (dicek dengan `file namafile.pdf`).
- **Tes otomatis (`tests/uji_regresi.py`)** memakai server tiruan (`http.server`
  bawaan Python): **12/12 skenario lulus**, termasuk 3 skenario normal, input tidak
  lengkap, file tidak ada, server mati, sandi salah, URL non-lokal ditolak, dan urutan
  panggilan API 2-langkah untuk `rapikan-resi`.
- `python3 scripts/validate.py --skill pdf-lokal` (lewat pemanggilan fungsi validasi
  langsung, tanpa mengubah `catalog.csv`): tidak ada masalah format SKILL.md/README/
  ATTRIBUTION/frontmatter.

## Skor kualitas (perkiraan, belum final)
**7.5/10** - alasan:
- (+) Semua endpoint diverifikasi ke server sungguhan, bukan tebakan dari dokumentasi.
- (+) Penanganan error jujur & lengkap (server mati, 404, 413, password salah, bahasa
  OCR tidak tersedia, URL non-lokal).
- (+) Nilai tambah lokal jelas: "rapikan-resi" untuk kebutuhan cetak resi marketplace
  Indonesia, yang tidak ada di UI default Stirling-PDF (harus digabung dulu manual).
- (-) **Belum diuji A/B (dengan skill vs tanpa skill)** dan **belum diuji banding
  pesaing** secara formal sesuai pedoman kurasi Komunitech tahap 6 - keduanya butuh sesi terpisah
  dengan agent lain. Ditandai PERLU REVIEW di laporan sesi.
- (-) Belum diuji di aplikasi desktop resmi Stirling-PDF (.msi/.dmg) maupun di
  OpenClaw/Codex/Cursor sungguhan - baru simulasi agent + Docker.
- (-) Belum ada uji dengan file PDF nyata berukuran besar/kompleks (baru file uji
  minimal buatan sendiri, karena tidak ada sampel PDF nyata di lingkungan pembuatan).

## PERLU REVIEW (untuk pemilik / sesi berikutnya)
1. Uji A/B "tanpa skill vs dengan skill" (pedoman kurasi Komunitech) - belum dilakukan.
2. Uji banding pesaing (Tahap 6.5) - belum dicari skill publik sejenis untuk
   dibandingkan; kata kunci yang perlu dicoba: "stirling pdf skill", "pdf agent skill
   claude", "pdf mcp server".
3. Uji dengan sampel PDF nyata (kontrak, nota scan asli, resi Shopee/Tokopedia asli)
   dari member VIP (dengan izin & tanpa data pribadi tersimpan di repo).
4. Verifikasi perilaku aplikasi DESKTOP Stirling-PDF (bukan Docker) soal login/keamanan
   default - lihat catatan di `references/sumber-api-stirling.md`.
5. `bash scripts/uji_openclaw.sh` (uji muat OpenClaw otomatis) belum dijalankan pada
   sesi ini - jalankan sebelum status naik ke `uji`/`lulus`.
