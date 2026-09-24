# Uji banding pesaing — skenario normal 1 (gabung 3 nota foto + kompres < 2 MB)

## Pesaing yang dibandingkan
**`anthropics/skills` — skill `pdf`** (folder `skills/pdf` di repo
`github.com/anthropics/skills`, dibaca via GitHub raw pada 2026-09-24). Dipilih karena
merupakan skill PDF paling kredibel yang tersedia secara publik untuk tugas ini
(pembuat resmi Anthropic, dipakai untuk fitur dokumen Claude.ai sendiri).

**Lisensi:** frontmatter skill ini menyatakan `license: Proprietary. LICENSE.txt has
complete terms`. Isinya **hanya dibaca untuk dinilai berdampingan**, tidak disalin satu
baris pun ke `pdf-lokal` — sesuai aturan Tahap 3/CLAUDE.md ("Tanpa lisensi/proprietary
→ DILARANG disalin, hanya inspirasi lalu tulis ulang dari nol"). `pdf-lokal` memang
sudah ditulis dari nol dengan pendekatan arsitektur yang sama sekali berbeda (REST API
ke Stirling-PDF lokal, bukan library Python langsung), jadi tidak ada risiko duplikasi.

## Cara kerja pesaing untuk skenario ini
Skill `pdf` (anthropics) mengarahkan agent menulis kode Python langsung:
```python
from pypdf import PdfWriter, PdfReader
writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
writer.write(output)
```
Untuk foto → PDF dan kompres, pesaing **tidak punya alur bawaan yang setara** dalam
`SKILL.md`-nya: "Quick Start" hanya mencontohkan baca/gabung/split/rotate PDF yang
**sudah** berupa PDF, bukan foto JPEG. Kompres ukuran file juga **tidak dicontohkan
sama sekali** di isi yang terbaca (tidak ada bagian "compress"/target ukuran KB/MB).

## Perbandingan berdampingan untuk skenario "gabung 3 foto nota + kompres < 2 MB"

| Aspek | `pdf-lokal` (kita) | `pdf` (anthropics/skills) |
|---|---|---|
| Foto → PDF (nota/struk) | Ada langsung: `foto-ke-pdf` | **Tidak dicontohkan** di SKILL.md yang terbaca; agent harus mengarang sendiri lewat `Pillow`/`img2pdf` yang tidak disebut sama sekali di skill ini |
| Kompres ke target ukuran (mis. "< 2 MB") | Ada langsung: `kompres --target 2MB`, terukur & diverifikasi | **Tidak ada** fitur/contoh kompres ukuran file sama sekali di SKILL.md yang terbaca |
| Dependensi yang harus terpasang | Tidak ada di sisi agent (hanya `urllib` bawaan Python); Stirling-PDF terpasang **sekali** di komputer pengguna, dipakai untuk semua skill PDF selanjutnya | `pypdf`, `pdfplumber`, `reportlab`, `pytesseract`, `pdf2image` (untuk OCR) — beberapa perlu `pip install` + `pytesseract` perlu **Tesseract terpasang di sistem** (bukan cuma pip); untuk PDF form perlu baca `FORMS.md` terpisah |
| Lokalisasi Indonesia | Bahasa Indonesia penuh, contoh kasus lokal (nota warung, resi Shopee/TikTok, kontrak sewa ruko), OCR bahasa Indonesia dibahas eksplisit | Bahasa Inggris, tidak ada konteks Indonesia sama sekali |
| Fitur khusus pasar Indonesia (rapikan resi marketplace N-up) | Ada (`rapikan-resi`) | Tidak ada padanan; hanya contoh generik "merge" |
| Keamanan/privasi ditulis eksplisit | Ya — menolak URL non-localhost, penjelasan file tidak diunggah | Tidak dibahas (fokus ke library, bukan ke privasi/lokasi eksekusi) |
| Verifikasi/pengujian tertulis dalam skill itu sendiri | Ada `tests/uji_regresi.py` + `references/sumber-api-stirling.md` yang mencatat versi server yang diuji | Tidak terlihat ada test bawaan dalam isi yang terbaca |
| Ketergantungan pada jalannya proses eksternal (server) | Ya — perlu Stirling-PDF berjalan (kelemahan: 1 titik gagal tambahan, lihat `HASIL-UJI.md`) | Tidak — semua diproses dalam proses Python yang sama (kelebihan: tidak ada "server mati") |

## Penilaian
Untuk **skenario spesifik ini** (foto nota → PDF → kompres terukur, dipakai UMKM
Indonesia awam yang tidak paham `pip install`), `pdf-lokal` **unggul jelas**: pesaing
publik yang paling kredibel bahkan tidak mendokumentasikan foto→PDF maupun kompres
bertarget di isi yang terbaca, dan mengasumsikan pengguna (via agent) bisa/boleh
`pip install` beberapa paket plus Tesseract sistem — sesuatu yang tidak realistis untuk
"tanpa setup" versi CLAUDE.md.

Namun perlu dicatat jujur **kelemahan arsitektural** `pdf-lokal` dibanding pendekatan
pesaing: pendekatan "panggil library Python langsung" milik pesaing **tidak punya
titik gagal server terpisah** — tidak ada skenario "server mati" atau "server minta
login tiba-tiba" seperti yang ditemukan pada `pdf-lokal` (lihat cacat **T1** di
`HASIL-UJI.md`). Trade-off ini sepadan selama panduan pemasangan Stirling-PDF benar2
teruji dan reliable — yang saat ini **belum** sepenuhnya terbukti (lihat T1).

**Kata kunci & sumber yang dicari (untuk kelengkapan, sesuai Tahap 6.5):** "stirling-pdf
skill claude", "clawhub pdf skill indonesia", "skills.sh pdf merge compress" — tidak
ditemukan skill PDF publik lain yang menyaingi cakupan/lokalisasi `pdf-lokal` selain
`anthropics/skills` di atas pada saat pengujian (2026-09-24).

## Kesimpulan uji banding
`pdf-lokal` **unggul** untuk skenario normal 1 dibanding pesaing publik terbaik yang
ditemukan → bukan kandidat skor maksimal 6 dari aturan ini. Skor final tetap
mempertimbangkan cacat T1 (server minta login default) secara terpisah di `HASIL-UJI.md`.
