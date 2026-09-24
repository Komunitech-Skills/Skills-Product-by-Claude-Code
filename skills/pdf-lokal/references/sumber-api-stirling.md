# Sumber endpoint & parameter API Stirling-PDF

Skill ini memanggil REST API Stirling-PDF. Semua nama endpoint & parameter di
`scripts/pdf.py` diambil dari dua sumber, keduanya dicek silang:

1. **Swagger/OpenAPI resmi server yang benar-benar dijalankan**: `GET /v1/api-docs`
   pada instance Stirling-PDF v2.14.3 (image `ghcr.io/stirling-tools/stirling-pdf:latest`,
   digest `sha256:3b3670fce70b396ec56ba380a3cc7858e0abf83fe13f31c88f7737847763a396`),
   dijalankan lewat Docker untuk memverifikasi skill ini. Diakses: **2026-09-24**.
2. Repo resmi **github.com/Stirling-Tools/Stirling-PDF** (kode sumber & rilis) dan
   **docs.stirlingpdf.com** untuk konteks fitur & batasan lisensi. Diakses: **2026-09-24**.

Tidak ada parameter yang ditebak - setiap field yang dikirim `scripts/pdf.py` sudah
dicoba langsung ke server sungguhan (lihat catatan uji di bawah).

## Dasar path
Semua endpoint di bawah `/api/v1/...` (bukan `/v1/...` - path itu khusus dokumen Swagger-nya
sendiri).

## Endpoint yang dipakai skill ini (diverifikasi berhasil ke server sungguhan)

| Perintah skill | Endpoint | Method | Skema request (nama di Swagger) |
|---|---|---|---|
| `cek` | `/api/v1/info/status` | GET | - |
| `ocr` (cek bahasa) | `/api/v1/ui-data/ocr-pdf` | GET | - (tidak didokumentasikan publik di docs.stirlingpdf.com, ini endpoint internal UI; dipakai sebagai pelengkap, ada fallback bila gagal/berubah) |
| `gabung` | `/api/v1/general/merge-pdfs` | POST | `MergePdfsRequest` |
| `pisah-halaman` | `/api/v1/general/split-pages` | POST | `SplitPagesRequest` |
| `pisah-rentang` | `/api/v1/general/rearrange-pages` (customMode=CUSTOM) | POST | `RearrangePagesRequest` |
| `kompres` | `/api/v1/misc/compress-pdf` | POST | `OptimizePdfRequest` |
| `ocr` | `/api/v1/misc/ocr-pdf` | POST | `ProcessPdfWithOcrRequest` |
| `foto-ke-pdf` | `/api/v1/convert/img/pdf` | POST | `ConvertToPdfRequest` |
| `putar` | `/api/v1/general/rotate-pdf` | POST | `RotatePDFRequest` |
| `watermark` | `/api/v1/security/add-watermark` | POST | `AddWatermarkRequest` |
| `kunci` | `/api/v1/security/add-password` | POST | `AddPasswordRequest` |
| `buka-kunci` | `/api/v1/security/remove-password` | POST | `PDFPasswordRequest` |
| `rapikan-resi` | `/api/v1/general/merge-pdfs` lalu `/api/v1/general/multi-page-layout` | POST | `MergePdfsRequest`, `MergeMultiplePagesRequest` |

Autentikasi (opsional, dipakai bila keamanan Stirling-PDF diaktifkan pengguna):
header `X-API-KEY` (skema `apiKey` di Swagger, `in: header`).

## Temuan penting saat verifikasi (2026-09-24, Docker, v2.14.3)

- **Image Docker Hub `stirlingtools/stirling-pdf` sempat kena rate-limit (429)** saat
  ditarik; berhasil lewat mirror resmi `ghcr.io/stirling-tools/stirling-pdf:latest`
  (disebutkan juga di README GitHub proyek).
- **Login/keamanan AKTIF secara default di image Docker** (log: `active profile: security`,
  ada user `admin` dibuat otomatis). Untuk pengujian lokal dipakai
  `SECURITY_ENABLELOGIN=false`. **Belum diverifikasi** apakah aplikasi desktop
  (.msi/.dmg, yang jadi target utama pembeli) berperilaku sama persis - lihat
  `docs/panduan-stirling-pdf.md` bagian Keamanan, dan script ini menangani kasus 401
  dengan pesan yang mengarahkan ke API key.
- **Bahasa OCR bawaan HANYA `eng, fra, deu, chi_sim, por`** (dicek lewat
  `docker exec ... find / -iname "*.traineddata"` dan endpoint `ui-data/ocr-pdf`).
  **Bahasa Indonesia (`ind`) TIDAK terpasang secara default** - harus diunduh manual
  lewat aplikasi Stirling-PDF. `scripts/pdf.py` mengecek ini dan otomatis memberi tahu
  pengguna + memakai bahasa yang tersedia saja, supaya tidak diam-diam OCR memakai
  bahasa Inggris padahal pengguna kira sudah bahasa Indonesia.
- **Field opsional pada `add-watermark` dan kemungkinan endpoint lain menyebabkan
  error 500 (`NullPointerException`) bila TIDAK dikirim sama sekali**, walau
  Swagger menandainya punya nilai `default` dan tidak wajib. Karena itu
  `scripts/pdf.py` selalu mengirim SEMUA field yang tercantum di skema, bukan
  hanya field wajib.
- **`multi-page-layout` (dasar fitur "rapikan resi") tidak punya parameter ukuran
  kertas keluaran (A4/A6) yang eksplisit** - hanya `pagesPerSheet`/`rows`x`cols`,
  margin, dan orientasi. Skill ini **tidak mengklaim** bisa memaksa ukuran A4/A6
  persis; pengguna diminta cek Print Preview sebelum cetak massal.
- **`split-pages` selalu membalas file `.zip`** (lewat header `Content-Disposition`),
  walau hasilnya cuma 1 file PDF. `rearrange-pages`, `merge-pdfs`,
  `multi-page-layout`, dll. selalu membalas 1 file PDF langsung
  (`Content-Type: application/pdf`). `scripts/pdf.py` membedakan keduanya dari
  header respons, bukan dari nama perintah.
- Error dari server datang dalam dua bentuk JSON: gaya lama `{"error": "..."}"`
  (kegagalan job/500) dan gaya baru RFC7807 `{"detail": "...", "status": ...,
  "errorCode": "..."}` (validasi/400, password/E004, 404). `scripts/pdf.py`
  membaca keduanya.

## Fitur yang SENGAJA TIDAK dipakai (di luar cakupan skill ini)

- Semua endpoint di bawah `/api/v1/proprietary/...`, `/api/v1/admin/...`, `/api/v1/team/...`,
  `/api/v1/audit/...`, tanda tangan sertifikat (`cert-sign`), SSO/MFA, dan fitur akun/tim -
  ini bagian **proprietary/berbayar** Stirling-PDF (folder `app/proprietary/` di
  kode sumber, lisensi bukan MIT) atau fitur server multi-pengguna yang tidak relevan
  untuk pemakaian di satu komputer. Skill ini **hanya memanggil endpoint inti (MIT)**.
- `pipeline/handleData` (pipeline otomatis Stirling) tidak dipakai - skill ini memanggil
  endpoint satuan langsung supaya lebih mudah ditelusuri bila gagal.

## Cara memverifikasi ulang (untuk audit di masa depan)

```
docker run -d --name stirling -p 8080:8080 -e SECURITY_ENABLELOGIN=false \
  ghcr.io/stirling-tools/stirling-pdf:latest
curl http://localhost:8080/api/v1/info/status
curl http://localhost:8080/v1/api-docs   # dokumen OpenAPI lengkap versi yang jalan
```
