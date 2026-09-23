# HASIL UJI — presentasi-instan

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Jalur:** KURASI (ATM) dari https://github.com/zarazhangrui/frontend-slides (MIT)
- **Lingkungan uji:** folder kerja /tmp/uji-presentasi-instan; Playwright 1.56 + Chromium 1194 (headless); Chromium `--print-to-pdf`; pypdfium2 untuk menghitung/merender halaman PDF.

## Ringkasan uji
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B tanpa skill vs dengan skill (S1) | Dengan skill jelas lebih baik (offline, Rupiah, tidak mengarang angka) |
| 00 | Banding pesaing = skill sumber frontend-slides | Kita menang jelas (7,5 vs 4) tapi **belum menang telak**: jalur PDF rusak, desain polos |
| 01 | Pitch investor laundry (13 slide) | Isi bagus; PDF terpotong |
| 02 | Pengajuan KUR bengkel, angka Rupiah (10 slide) | Angka benar (diverifikasi); skill tidak merujuk `pengajuan-kur`; PDF: semua nominal hilang |
| 03 | Laporan bulanan dari CSV, permintaan singkat (8 slide) | Angka benar (diverifikasi independen); PDF A4 lanskap: kolom "Porsi" hilang |
| 04 | Input kurang | Bertanya sekali, 5 pertanyaan bernomor ✔ |
| 05 | Di luar cakupan (.pptx) | Menolak jujur + alternatif ✔ |

## Pemeriksaan teknis
| Pemeriksaan | Hasil |
|---|---|
| Tanpa internet (request jaringan saat dibuka, 3 deck) | ✔ 0 request; tidak ada `<link>`/`<script src>`/font online |
| `validasi_html.py` pada 3 deck | ✔ LULUS tanpa peringatan |
| Teks meluber pada kanvas 1920×1080 (cek bounding box semua elemen) | ✔ 0 slide meluber di 31 slide |
| HP 390×844 tegak | Tidak meluber, tetapi skala 0,203 → teks isi 28–32px menjadi **±5,7–6,5px**. HP lanskap 844×390: skala 0,361 → ±10–11,6px, terbaca |
| Cetak PDF, jumlah halaman | ✔ 13/10/8 halaman = 1 slide per halaman |
| Cetak PDF, isi halaman | ✗ **Sisi kanan terpotong** di Letter tegak (bawaan) dan A4 lanskap (yang dianjurkan skill). Contoh: slide "Rencana penggunaan dana" KUR kehilangan seluruh kolom Rupiah; laporan kehilangan kolom "Porsi" |
| Perbaikan diuji penguji | Menambah `@page { size: 1920px 1080px; margin: 0; }` + `* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }` → 13 halaman 1440×810pt, utuh, warna latar ikut tercetak |
| Format Rupiah | ✔ semua `Rp 1.250.000`, persen pakai koma desimal |
| Angka | ✔ diverifikasi independen: aset 113.000.000; cicilan anuitas 4.563.291 (cocok `simulasi_kur.py`); rasio 46,6%; rekap CSV 41.190.000 / 91,5% / per produk, kategori, minggu |

### validasi_html.py dengan file rusak (13 file)
| File uji | Hasil | Benar? |
|---|---|---|
| `<link href="https://fonts.googleapis.com…">` | GAGAL, exit 1 | ✔ |
| tanpa `@media print` | GAGAL | ✔ |
| file kosong | GAGAL (tidak ada slide & print) | ✔ |
| bukan UTF-8 | pesan jelas, exit 2 | ✔ |
| file tidak ada | pesan jelas, exit 2 | ✔ |
| tanpa class="slide" | GAGAL | ✔ |
| teks 267–307 kata/slide | LULUS + peringatan | ✔ (peringatan) |
| `<link href=https://…>` **tanpa tanda kutip** | LULUS | ✗ lolos |
| `srcset="https://…"` | LULUS | ✗ lolos |
| `url("//cdn…")` di CSS | LULUS | ✗ lolos |
| `fetch("https://…")` di JavaScript | LULUS | ✗ lolos |
| `<img src="C:\Users\…\logo.png">` (gambar lokal, bukan base64 — rusak saat file dikirim via WA) | LULUS | ✗ lolos |
| slide yang benar-benar meluber (terdeteksi Playwright) | hanya peringatan jumlah kata, status LULUS | ~ |

### Audit keamanan
`validasi_html.py` hanya membaca file lokal, pustaka standar, tanpa jaringan/penulisan/perintah shell. SKILL.md & referensi bebas prompt injection. Kerangka JS hanya navigasi (tanpa localStorage, tanpa jaringan). ✔

### ATTRIBUTION.md
- Teks MIT identik byte-per-byte dengan `LICENSE` sumber (dicek `diff`) ✔; nama pembuat, URL, tanggal tinjau ✔.
- 9 poin perubahan disebut dan dicek kebenarannya terhadap repo sumber (Google Fonts wajib, deploy.sh Vercel, export-pdf.sh Playwright, 3 preview gaya, mode edit) ✔.
- Tidak ada teks sumber disalin utuh: dari semua baris ≥35 karakter hanya 3 baris boilerplate umum yang sama. Logika skala panggung (JS `Math.min(innerWidth/1920, …)`) dan blok `@media print` adalah turunan struktural yang sudah diatribusikan — sah menurut MIT ✔.

## Skor
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 8 | Kata kunci ID/EN lengkap (pitch deck, slide, KUR, company profile); tumpang-tindih dengan `pengajuan-kur` tidak diatur |
| Kemudahan awam | 7 | Tanpa setup, petunjuk jelas; tapi HP tegak nyaris tak terbaca dan tidak ada anjuran memutar HP |
| Kualitas output | 6 | Isi & struktur bagus, desain polos, PDF terpotong |
| Akurasi (angka/fakta) | 8 | Tidak mengarang, Rupiah benar; perhitungan cicilan/rasio tidak dipandu skill |
| Penanganan input kurang | 9 | Sekali tanya, bernomor, ada jalur default |
| Penanganan di luar cakupan | 9 | .pptx ditolak jujur + alternatif |
| Keamanan | 9 | Bersih; file lokal saja |

## SKOR AKHIR: **6 / 10 — REVISI**
Dibatasi ≤ 6 karena **cacat berat**: janji utama "cetak jadi PDF satu slide per halaman" menghasilkan halaman yang terpotong dan membuang angka Rupiah penting (tidak disadari pengguna awam sampai PDF sudah dikirim ke bank/investor). Selain itu, sebagai hasil ATM belum **menang telak** atas sumber (sumber punya jalur PDF yang berfungsi, desain lebih kaya, mode edit).

## Daftar cacat & saran perbaikan

### Berat
1. **PDF terpotong di sisi kanan** — `references/kerangka-html.md` blok "MODE CETAK" (dan `aturan-desain.md` #9). Tambahkan sebelum `@media print`: `@page { size: 1920px 1080px; margin: 0; }` dan `* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }`. Hapus anjuran "pilih orientasi Lanskap" di SKILL.md Format output & README (ukuran halaman sudah diatur file); tambahkan "centang Grafis latar/Background graphics bila warna tidak muncul". Tambahkan ke `validasi_html.py` ERROR bila `@page` dengan `size` tidak ada.

### Sedang
2. **Teks ±6px di HP tegak** — kerangka `skalakan()`/README "buka di HP pun bisa". Tambahkan overlay kecil saat `innerHeight > innerWidth`: "Putar HP ke posisi mendatar agar teks terbaca", dan sebutkan di Format output & README. (Opsional: mode baca bertumpuk untuk layar tegak.)
3. **Tidak merujuk skill `pengajuan-kur`** — SKILL.md "Kapan TIDAK digunakan" & "Integrasi dengan skill lain", serta `templates/pengajuan-kur.md` slide 7. Wajibkan: cicilan, rasio cicilan/laba, dan cek plafon/agunan diambil dari `pengajuan-kur` (atau rumus anuitas eksplisit berlabel asumsi); bila rasio "BERAT", beri tahu pengguna sebelum membuat slide.
4. **Validator bisa dilewati** — `scripts/validasi_html.py` `POLA_EKSTERNAL`: tangani atribut tanpa kutip (`(?:href|src|srcset)\s*=\s*["']?(?:https?:)?//`), `url\(\s*["']?//`, `fetch(`/`XMLHttpRequest`/`import(` ke http, dan beri ERROR untuk `src` gambar yang bukan `data:` (path lokal seperti `C:\…` atau `logo.png` akan hilang saat file dikirim).
5. **Tidak ada komponen siap pakai** — `kerangka-html.md` hanya h1/h2/p/li. Tambahkan kelas standar (kartu angka, tabel dengan kolom uang rata kanan `white-space:nowrap`, dua kolom, kotak kesimpulan, penanda `[isi]` berwarna, slide sampul berwarna) agar hasil konsisten antar-agent.

### Ringan
6. `aturan-desain.md` #4: klaim font "terpasang bawaan di Windows, macOS, atau Linux" tidak akurat (Segoe UI hanya Windows; Verdana/Georgia tidak ada di Linux/Android) — ubah jadi "dengan cadangan yang aman di semua OS".
7. `kerangka-html.md`: `.slide` tidak punya `overflow: hidden`; `.kontrol` menutupi ±60px bawah slide di layar lanskap HP — beri `opacity` lebih rendah / sembunyikan otomatis.
8. SKILL.md langkah 1: bila pengguna mengirim CSV/Excel, jadikan langkah wajib "rekap dulu dengan `rekap-penjualan-csv`" (sekarang hanya bagian integrasi opsional).
9. SKILL.md contoh pertanyaan (Input): tambahkan "Kalau mau cepat, cukup jawab nomor 1" agar pengguna terburu-buru langsung dapat hasil.
10. README "Angka Rupiah dihitung" — skill tidak punya script hitung; ganti menjadi "ditulis dengan format yang benar; angka diambil dari data Anda/skill hitung lain".

## File di folder ini
- `00-pembanding-tanpa-skill.md`, `00-banding-pesaing.md`, `01`–`05` skenario.
- Hasil nyata: `pitch-bersih-kilat.html`, `kur-maju-jaya-motor.html`, `laporan-agustus-2026.html`, data fiktif `penjualan-agustus-2026.csv`.
- Screenshot: `ss-01-laporan-slide4-laptop.png`, `ss-02-cacat-pdf-a4-lanskap-kolom-terpotong.png`, `ss-03-hp-390px-tegak-teks-kecil.png`.
