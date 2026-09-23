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
   Bahasa Indonesia dengan struktur yang disederhanakan. Versi 1.1.0 menambahkan mode
   edit teks langsung di browser (tombol "Edit" yang men-toggle `contenteditable` pada
   elemen teks, lalu pengguna menyimpan lewat `Ctrl+S`/`Cmd+S` bawaan browser) — ditulis
   sendiri dari nol tanpa `localStorage`/auto-save dan tanpa melihat kode sumber; jauh
   lebih sederhana daripada mode edit sumber, sesuai kebutuhan pengguna awam untuk kasus
   penggunaan sekali-jadi (buat → cetak/kirim).
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

## Riwayat perubahan

### v1.1.1 (2026-09-23) — revisi hasil uji ulang v1.1.0 (skor 6, lihat "Uji ulang v1.1.0" di `examples/HASIL-UJI.md`)
- **Perbaikan cacat berat mode Edit:** handler `keydown`/`touchstart`/`touchend` di
  `references/kerangka-html.md` kini berhenti lebih dulu (`return`) bila target sedang
  diedit (`e.target.isContentEditable`) atau mode edit aktif (`document.body` punya kelas
  `mode-edit`) — Spasi/panah kiri-kanan tidak lagi memindah slide saat mengetik teks.
  "Selesai edit" kini melepas atribut `contenteditable` sepenuhnya (`removeAttribute`,
  bukan set ke `"false"`), dan file yang dibuka ulang membersihkan sisa `contenteditable`
  saat load (mencegah file tersimpan-tengah-edit terbuka dalam kondisi aneh). Outline
  putus-putus mode edit disembunyikan di `@media print`. README/SKILL.md menjelaskan
  bahwa menyimpan (Ctrl+S/Cmd+S) hanya bisa di laptop/komputer, bukan di HP.
- **Kontras tema gelap:** tabel palet di `aturan-desain.md` #5 kini mewajibkan
  `--warna-teks-lembut` per tema (mis. `#cfc8b8` untuk Hitam Emas Premium, kontras
  11,3:1), bukan memakai default `#475569` yang hanya 2,5:1 di atas latar gelap.
  `scripts/validasi_html.py` menambahkan pemeriksaan kontras WCAG otomatis (ERROR bila
  `--warna-teks`/`--warna-teks-lembut` vs `--warna-latar-slide` di bawah 4,5:1).
- **Validator disempurnakan:** tautan `<a href="https://wa.me/...">` (navigasi, bukan
  pemuatan sumber daya) kini hanya PERINGATAN, bukan ERROR; `<link href>` ke internet
  tetap ERROR. Ditambahkan deteksi path lokal (bukan `data:`) pada `<video src>`,
  `<audio src>`, `<source src>`, dan CSS `url("foto-lokal.jpg")` — sama seperti `<img>`
  sebelumnya. `tests/uji_validasi.py` bertambah 6 kasus (kini 26 total): tautan wa.me
  (lulus+peringatan), tema gelap kontras cukup (lulus), tema gelap kontras kurang
  (gagal), CSS url() lokal, `<video src>` lokal, `<source src>` lokal.
- **Overlay "putar HP":** ditambah tombol "Tetap lihat" untuk menutup overlay (mis. HP
  yang kunci rotasinya aktif), dan ambang lebar diperketat ke `max-width: 600px` (dari
  900px) supaya tidak lagi muncul di layar tablet tegak yang sebenarnya sudah terbaca.
- **Label kelayakan KUR ("BERAT"/"AMAN") tidak lagi ditaruh di slide** yang akan dilihat
  bank — SKILL.md & `templates/pengajuan-kur.md` kini memisahkan: slide berisi nominal
  cicilan & rasio saja, sedangkan label kategori dan perkiraan plafon aman disampaikan ke
  pengguna di ringkasan akhir (Format output).

### v1.1.0 (2026-09-23) — revisi hasil uji independen (skor 6, lihat `examples/HASIL-UJI.md`)
- **Perbaikan cacat berat PDF terpotong:** tambah `@page { size: 1920px 1080px; margin: 0; }`
  dan `print-color-adjust: exact` di `references/kerangka-html.md`; hapus anjuran memilih
  kertas A4/orientasi Lanskap di SKILL.md & README (sudah otomatis lewat `@page`).
- Overlay "Putar HP ke posisi mendatar" untuk layar HP tegak (CSS `orientation: portrait`
  murni, tanpa JS eksternal); kontrol navigasi dikecilkan/dipudarkan di HP mendatar layar
  pendek agar tidak menutupi isi slide.
- Angka cicilan/rasio KUR dan rekap CSV kini wajib lewat skill `pengajuan-kur` /
  `rekap-penjualan-csv` (atau script Python eksplisit) — SKILL.md &
  `templates/pengajuan-kur.md` diperbarui, tidak boleh lagi dihitung kira-kira.
- `scripts/validasi_html.py` diperluas: mendeteksi href/src/srcset tanpa tanda kutip,
  `url(//...)`/`url(http...)` di CSS, `@import`, `fetch()`/`XMLHttpRequest`/`import()` ke
  internet, `<img src>` yang bukan `data:` URI (path lokal), dan memberi ERROR bila
  `@page` dengan `size` tidak ada. Ditambahkan `tests/uji_validasi.py` (unittest, 18 kasus
  rusak + 2 kasus benar).
- Komponen siap pakai baru di `references/kerangka-html.md`: kartu angka (KPI), tabel
  dengan kolom uang rata kanan (`tabular-nums`), dua kolom, penanda `[isi]` mencolok,
  timeline/langkah, kutipan/testimoni, plus panduan turunan warna kartu/garis untuk tiap
  tema di `aturan-desain.md`.
- Klaim tumpukan font diperbaiki (tidak lagi mengklaim identik di semua OS; tambah
  `system-ui`/`Roboto` untuk cakupan Linux/Android). README tidak lagi mengklaim angka
  "dihitung" oleh skill ini sendiri — diperjelas berasal dari data pengguna/skill hitung
  lain.
- Ditambahkan mode edit teks langsung di browser (`contenteditable` + simpan via
  `Ctrl+S`/`Cmd+S` bawaan browser), ditulis dari nol tanpa library.

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
