# Uji banding pesaing — skill SUMBER `frontend-slides` vs `presentasi-instan`

## Sumber pesaing
- **frontend-slides** oleh Zara Zhang — https://github.com/zarazhangrui/frontend-slides — lisensi **MIT** (commit teratas 9906a34, 23 Jun 2026). Ini skill sumber ATM kita, jadi menurut pedoman kurasi Komunitech tahap 2 hasil ATM **wajib menang telak**.
- Dibaca lewat `git clone --depth 1` ke /tmp: `SKILL.md` (380 baris), `html-template.md`, `viewport-base.css`, `STYLE_PRESETS.md`, `scripts/deploy.sh`, `scripts/export-pdf.sh` (hanya dibaca, **tidak dijalankan**). Tidak ada teks pesaing yang disalin ke skill kita (cek otomatis baris ≥35 karakter: hanya 3 baris boilerplate umum yang sama — `meta viewport`, reset `*{margin:0…}`, `@media (prefers-reduced-motion…)`).
- Pesaing lain yang relevan (anthropics/skills `pptx`) menghasilkan `.pptx` dan butuh pustaka tambahan — format berbeda, tidak dibandingkan di sini.

## Menjalankan S1 dengan instruksi pesaing (berperan sebagai agent yang memuat frontend-slides)
Alur yang diwajibkan SKILL.md sumber:
1. **Phase 1** — 4 pertanyaan (Purpose / Length / Content / Density), dalam bahasa Inggris di skill; agent menerjemahkan sendiri.
2. **Phase 2** — wajib membuat **3 preview HTML gaya** di `.frontend-slides/slide-previews/`, membukanya, lalu **menunggu pengguna memilih** (1 ronde tanya-jawab tambahan). Diasumsikan pengguna memilih preset "Swiss Modern".
3. **Phase 3** — deck penuh: "Use fonts from Fontshare or Google Fonts — never system fonts" → `<link>` Google Fonts Archivo + Nunito; animasi `.reveal`; mode edit inline (tombol ✏️ / tombol E, simpan ke localStorage).
4. **Phase 5–6** — buka file, lalu tawarkan **deploy ke Vercel** (Node.js + akun Vercel + `npm install -g vercel`) atau **ekspor PDF** lewat `export-pdf.sh` (Node.js + Playwright + unduh Chromium ±150MB, PDF dari screenshot).

Hasil (file uji: struktur & isi 13 slide sama dengan contoh 01, diberi gaya sesuai sumber; angka ditulis seperti kebiasaan agent tanpa aturan Rupiah: "Rp 38 juta", "Rp 450 juta", "Rp 3 miliar"):
- 1 request jaringan ke `fonts.googleapis.com`; offline → font jatuh ke `sans-serif` bawaan sehingga tampilan berubah.
- `validasi_html.py` → GAGAL (rujukan internet).
- HP 390px tegak: sama dengan kita (panggung 16:9 berskala 0,203 → teks ±6px).
- Cetak lewat menu Print Chromium: 13 halaman, **sisi kanan terpotong sama persis** dengan kita (blok `@media print` sumber juga tanpa `@page size`). Sumber menghindarinya lewat `export-pdf.sh` (screenshot), yang butuh instalasi.

## Output berdampingan (S1)

| | frontend-slides (sumber) | presentasi-instan (kita) |
|---|---|---|
| Jumlah ronde sebelum file jadi | 2 (4 pertanyaan → 3 preview → pilih) | 0–1 (langsung jadi bila info cukup; maks 5 pertanyaan sekali) |
| Bahasa interaksi & instruksi | Inggris, istilah desainer ("density", "bold template", "wildcard") | Indonesia sehari-hari |
| Tanpa internet | ✗ font online wajib | ✔ font sistem, divalidasi script |
| Struktur isi konteks Indonesia | ✗ tidak ada template isi (hanya preset visual) | ✔ 7 template: investor, KUR/bank, B2B, laporan bulanan, profil, reseller, pelatihan |
| Format Rupiah / larangan mengarang angka | ✗ tidak diatur | ✔ `Rp 1.250.000`, placeholder `[isi]`, daftar "perlu dilengkapi" |
| Disclaimer KUR/bank | ✗ | ✔ |
| Keindahan/variasi desain | ✔ lebih kaya: 12 preset + ±30 template "bold", animasi, preview visual | ~ 4 palet netral, tanpa komponen siap pakai (kartu/tabel dirancang agent sendiri) |
| Edit teks langsung di browser | ✔ (mode edit + localStorage) | ✗ (sengaja dihapus) |
| PDF | ✔ lewat script (butuh Node + Playwright ±150MB + internet); menu Print terpotong | ✗ menu Print terpotong (tidak ada jalur lain) |
| HP tegak | teks ±6px | teks ±6px |
| Setup / akun | Vercel (akun + CLI), Node.js | tidak ada |
| Privasi | menawarkan publikasi ke URL publik (berisiko untuk data omzet/KUR) | file lokal saja |

## Tabel penilaian (1–10, untuk pembeli awam Indonesia)

| Kriteria | frontend-slides | presentasi-instan |
|---|---|---|
| Kualitas output (isi + tampilan) | 7 (tampilan lebih "wah", isi generik) | 7 (isi lebih tepat sasaran, tampilan polos) |
| Kesesuaian konteks Indonesia | 2 | 9 |
| Akurasi (angka, tidak mengarang) | 5 | 8 |
| Siap pakai tanpa setup (offline, tanpa akun) | 3 | 7 (dikurangi karena PDF terpotong) |
| **Keseluruhan** | **4** | **7,5** |

## Kesimpulan
`presentasi-instan` **menang jelas** atas sumbernya untuk target pembeli (offline, Indonesia, template isi lokal, disiplin angka Rupiah, tanpa setup). Namun **belum "menang telak" di semua dimensi**: (1) jalur PDF kita — satu-satunya jalur ekspor — rusak (terpotong), sedangkan sumber punya jalur PDF yang berfungsi walau berat; (2) desain kita jauh lebih polos dan tanpa komponen siap pakai; (3) mode edit di browser dihapus tanpa pengganti; (4) masalah teks kecil di HP tegak diwarisi dari sumber tanpa perbaikan/peringatan.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- Sediakan **komponen siap pakai** (kartu angka, tabel uang rata kanan, dua kolom, kotak kesimpulan, penanda `[isi]`) di kerangka supaya hasil antar-agent konsisten dan tidak polos.
- Jalur PDF yang **pasti** berhasil: tambahkan `@page { size: 1920px 1080px; margin: 0 }` + `print-color-adjust: exact` (sudah diuji penguji: 13 halaman 1440×810pt, tidak terpotong).
- Mode baca untuk HP tegak (mis. saat lebar < tinggi, tampilkan slide bertumpuk yang bisa digulir, atau pesan "putar HP ke lanskap").
- Opsi ringan untuk mengedit teks (mis. `contenteditable` tanpa penyimpanan otomatis + petunjuk "Simpan halaman"), karena pengguna awam sering hanya ingin mengganti satu angka.
- Pemeriksaan visual setelah jadi (sumber mewajibkan cek screenshot overflow) — validator kita hanya menghitung kata.

---

## Uji ulang v1.1.0 (2026-09-23)

Skenario sama (S1 + deck KUR & laporan dibuat ulang dengan kerangka v1.1.0). Sumber tidak berubah (commit 9906a34).

| | frontend-slides (sumber) | presentasi-instan v1.1.0 |
|---|---|---|
| PDF lewat menu Print (tanpa instalasi) | ✗ terpotong (print CSS tanpa `@page size`, diuji v1.0 dengan CSS yang sama) | ✔ utuh di semua setelan, 1 slide/halaman, warna ikut tercetak |
| PDF jalur lain | script Playwright (Node + unduh Chromium ±150MB + internet) | tidak perlu |
| HP tegak | teks ±6px tanpa petunjuk | overlay "putar HP"; mendatar terbaca ±11px, kontrol tidak menutupi isi |
| Komponen siap pakai | ✔ banyak (preset + template bold) | ✔ KPI, tabel uang, dua kolom, timeline, kutipan, `[isi]` (lebih sedikit, tapi cukup untuk konteks bisnis) |
| Angka uang | tidak diatur | wajib dari `pengajuan-kur` / `rekap-penjualan-csv`, format `Rp 1.250.000` |
| Tanpa internet | ✗ font online wajib | ✔ divalidasi (validator kini menutup 5 celah lama) |
| Mode edit | ✔ ada (localStorage) | ✗ ada tapi **rusak**: Spasi/panah memindah slide saat mengetik |
| Tema gelap | ✔ beberapa preset gelap | ✗ Hitam Emas: teks sekunder kontras 2,49:1 |

| Kriteria (1–10, pembeli awam Indonesia) | frontend-slides | v1.0 | v1.1.0 |
|---|---|---|---|
| Kualitas output | 7 | 7 | 8 |
| Kesesuaian konteks Indonesia | 2 | 9 | 9 |
| Akurasi | 5 | 8 | 9 |
| Siap pakai tanpa setup | 3 | 7 | 9 |
| **Keseluruhan** | **4** | **7,5** | **8,5** |

**Kesimpulan:** untuk alur utama pembeli (minta → file jadi → buka offline di laptop/HP → cetak PDF), v1.1.0 kini **menang telak** atas sumbernya: sumber gagal di offline, konteks Indonesia, angka, dan PDF tanpa instalasi. Dua dimensi yang masih kalah: **mode edit** (punya kita rusak pada tombol Spasi) dan **variasi desain/tema gelap**. Mode edit harus diperbaiki sebelum rilis karena dianjurkan di setiap balasan. Setelah itu, kemenangan telak berlaku di semua dimensi yang relevan untuk pembeli.

---

## Uji ulang v1.1.1 (2026-09-23)

| | frontend-slides (sumber) | presentasi-instan v1.1.1 |
|---|---|---|
| Mode edit | ✔ ada (localStorage) | ✔ **kini berfungsi**: Spasi/panah/swipe tidak memindah slide saat mengetik, sisa mode edit dibersihkan saat dibuka ulang, outline tidak ikut tercetak, petunjuk simpan jelas (laptop saja) |
| Tema gelap | ✔ beberapa preset | ✔ Hitam Emas Premium terbaca (kontras teks sekunder 11,34:1) + validator memeriksa kontras WCAG |
| PDF tanpa instalasi | ✗ terpotong | ✔ utuh di semua setelan, termasuk tema gelap |
| HP tegak | teks ±6px tanpa petunjuk | overlay putar HP + "Tetap lihat"; tablet tidak diganggu |
| Offline / angka Rupiah / konteks Indonesia | ✗ / ✗ / ✗ | ✔ / ✔ / ✔ |
| Variasi desain | ✔ lebih kaya (12 preset + template bold, animasi) | ~ 4 tema + 6 komponen, tanpa animasi |

| Kriteria (1–10, pembeli awam Indonesia) | frontend-slides | v1.0 | v1.1.0 | v1.1.1 |
|---|---|---|---|---|
| Kualitas output | 7 | 7 | 8 | 8 |
| Kesesuaian konteks Indonesia | 2 | 9 | 9 | 9 |
| Akurasi | 5 | 8 | 9 | 9 |
| Siap pakai tanpa setup | 3 | 7 | 9 | 9 |
| **Keseluruhan** | **4** | **7,5** | **8,5** | **9** |

**Kesimpulan:** v1.1.1 **menang telak** atas sumbernya. Keunggulan sumber yang tersisa hanya variasi visual/animasi, yang bukan prioritas pembeli awam yang butuh deck bank/investor/laporan yang rapi, offline, dan bisa dicetak. Mode edit dan tema gelap, dua dimensi yang kalah di v1.1.0, kini setara.
