# Atribusi

Skill `presentasi-instan` **diadaptasi dan diubah secara substansial** dari skill
**frontend-slides** karya **Zara Zhang**:

- Sumber: https://github.com/zarazhangrui/frontend-slides
- Lisensi sumber: MIT (teks lengkap di bawah)
- Ditinjau: 2026-09-23

Adaptasi oleh Komunitech (komunitech.com). Penggunaan versi adaptasi ini tunduk pada
`LISENSI.txt` yang disertakan dalam paket pembelian, **tanpa mengurangi** ketentuan
lisensi MIT di bawah untuk bagian yang berasal dari karya asli.

## Yang diambil dari sumber
- Gagasan inti: presentasi HTML mandiri (single-file, CSS/JS inline, tanpa build tool)
  yang dibuka langsung di browser.
- Pola "panggung tetap 16:9" — slide ditulis pada kanvas berukuran tetap (1920×1080)
  lalu seluruh panggung diskalakan dengan satu transform CSS, bukan disusun ulang per
  perangkat, supaya tata letak tidak pernah berantakan di layar kecil.
- Gagasan navigasi keyboard (panah/spasi) dan geser jari (swipe) di HP.
- Gagasan blok CSS `@media print` untuk mencetak satu slide per halaman PDF.
- Gagasan alur wawancara singkat di awal untuk menentukan tujuan & kepadatan konten
  sebelum membuat slide.

## Yang diubah / ditambahkan oleh Komunitech
1. **100% Bahasa Indonesia**, termasuk seluruh instruksi, komentar kode, nama kelas CSS
   (`slide`, `aktif`, `panggung`, dst.), dan wawancara pengguna — sumber sepenuhnya
   berbahasa Inggris dan ditujukan untuk pengguna teknis (developer/desainer).
2. **Jalur inti sepenuhnya tanpa instalasi apa pun**, sesuai prinsip "instan" library
   ini. Sumber mewajibkan `<link>` ke Google Fonts/Fontshare di setiap presentasi
   (`html-template.md` sumber: "Use fonts from Fontshare or Google Fonts — never system
   fonts") dan menyediakan `scripts/deploy.sh` (memasang Vercel CLI global, perlu login
   akun) serta `scripts/export-pdf.sh` (memasang Playwright + mengunduh Chromium
   ~150MB) sebagai bagian alur utama. Versi ini **melarang** rujukan internet sama
   sekali (font sistem saja) dan **menghapus** deploy Vercel & ekspor Playwright dari
   alur inti — export PDF cukup lewat menu Print bawaan browser (`@media print`), tanpa
   instalasi apa pun. `scripts/validasi_html.py` yang baru justru **menolak** file yang
   masih mengandung rujukan CDN/internet (lihat kode: daftar `POLA_EKSTERNAL`).
3. **Wawancara dibatasi maksimal 5 pertanyaan** dengan default masuk akal untuk pengguna
   awam non-teknis, digabung dalam satu pesan bernomor. Sumber memakai 4 pertanyaan
   plus alur eksplorasi visual 3-opsi bergaya desainer (Phase 2: "Style Discovery" —
   3 preview HTML berbeda, pemilihan preset dari `STYLE_PRESETS.md`/`bold-template-pack`)
   yang mengasumsikan pengguna teknis dan familier istilah desain; versi ini
   menggantinya dengan palet warna siap pakai bernama Indonesia (`references/aturan-desain.md`).
4. **7 template struktur slide konteks lokal ditulis dari nol** di `templates/`: pitch
   investor/angel, proposal kerja sama B2B, pengajuan KUR/bank, laporan bulanan ke
   atasan/owner, profil perusahaan, presentasi produk ke reseller, dan materi pelatihan
   karyawan — masing-masing dengan urutan slide, hal wajib ada, dan kesalahan umum yang
   dihindari sesuai konteks bisnis Indonesia. Sumber tidak memiliki template konten
   per-industri sama sekali; sumber hanya menyediakan preset **visual** (warna/font)
   generik untuk audiens internasional.
5. **Aturan desain baru untuk pengguna awam** (`references/aturan-desain.md`): batas
   kata per slide, panduan kontras warna sederhana tanpa alat ukur, tumpukan font
   sistem aman lintas OS, format angka Rupiah (`Rp 1.250.000`), dan jumlah slide wajar
   per konteks. Sumber menargetkan desainer/developer yang paham prinsip desain sendiri
   dan tidak membahas format mata uang.
6. **Script `scripts/validasi_html.py` ditulis dari nol** (Python 3 standar, tanpa
   dependensi): memeriksa tidak ada rujukan internet/CDN, ada blok `@media print`,
   jumlah slide, dan slide dengan teks terlalu panjang. Sumber tidak memiliki script
   validasi konten sama sekali — script sumber (`deploy.sh`, `export-pdf.sh`,
   `extract-pptx.py`) hanya untuk deploy, ekspor PDF via Playwright, dan konversi
   `.pptx`, yang semuanya membutuhkan instalasi paket/CLI tambahan.
7. **Kerangka HTML ditulis ulang dari nol** (`references/kerangka-html.md`) dalam
   Bahasa Indonesia dengan struktur yang disederhanakan: tanpa fitur edit inline di
   browser (localStorage auto-save, mode edit teks langsung) yang ada di sumber, karena
   menambah kerumitan yang tidak dibutuhkan pengguna awam untuk kasus penggunaan
   sekali-jadi (buat → cetak/kirim).
8. **Disebutkan opsi integrasi** dengan skill lain di library ini
   (`rekap-penjualan-csv`, `laporan-keuangan-emkm`, `hitung-hpp`) agar angka penjualan/
   keuangan/margin tidak dihitung ulang manual — fitur ini tidak ada di sumber karena
   sumber berdiri sendiri, bukan bagian dari library skill bisnis Indonesia.
9. **Dihapus:** frontmatter field `license`/deskripsi Inggris, seluruh konsep
   "bold-template-pack" (template visual berbayar/eksklusif ala desainer), pipeline
   pemrosesan gambar dengan Pillow (`crop_circle`, `resize_max` — di luar cakupan
   "tanpa instalasi"), dan seluruh rujukan ke `npx`/`npm`/Node.js.

Seluruh teks SKILL.md, README, referensi, template, dan script ditulis ulang dalam
Bahasa Indonesia dengan struktur dan penekanan berbeda untuk pengguna bisnis Indonesia
yang awam teknologi; tidak ada bagian teks sumber yang disalin utuh — hanya konsep
struktural (panggung 16:9 berskala, mode cetak per-slide) yang dipelajari lalu ditulis
ulang dengan implementasi sendiri.

## Teks lisensi asli (MIT)

Disalin persis dari https://raw.githubusercontent.com/zarazhangrui/frontend-slides/main/LICENSE:

```
MIT License

Copyright (c) 2025 Zara Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
