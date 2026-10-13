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
- Screenshot v1.0 (PDF terpotong, teks kecil HP tegak) sudah diganti dengan screenshot v1.1.0 — lihat bagian di bawah. File HTML contoh kini hasil v1.1.0.

---

# Uji ulang v1.1.0

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi diuji:** 1.1.0 (commit 40f8908)
- **Lingkungan:** /tmp/uji-presentasi-instan/v11; Playwright 1.56 + Chromium 1194 (`/opt/pw-browsers`); pypdfium2.
- **Deck dibuat ulang dengan kerangka baru:** `kur-maju-jaya-motor.html` (10 slide), `laporan-agustus-2026.html` (8 slide), `pitch-bersih-kilat.html` (13 slide). Ketiganya menggantikan file v1.0 di folder ini.

## Verifikasi tiap klaim perbaikan

| # | Klaim | Cara uji | Hasil |
|---|---|---|---|
| 1 | `@page 1920×1080` + `print-color-adjust` → PDF tidak terpotong | Chromium `--print-to-pdf` **bawaan** (tanpa opsi, dengan & tanpa header), setelan **anjuran** (margin 0 + grafis latar), **tanpa** grafis latar, dan **dipaksa A4 lanskap**. Hitung halaman, ukuran, posisi teks paling kanan, dan cocokkan SEMUA nilai `Rp …`/persen di HTML dengan teks PDF | ✔ 10/8/13 halaman = jumlah slide; ukuran 1440×810pt (=1920×1080px); teks paling kanan 94,4% lebar (= batas padding 96px); **0 dari 19 (KUR) dan 0 dari 30 (laporan) nilai hilang** di semua setelan. Pembanding v1.0 dengan metode sama: 10–18 nilai hilang. Warna latar ikut tercetak walau "grafis latar" tidak dicentang (juga pada tema gelap). Lihat `ss-02-pdf-v1.1-halaman-utuh.png` |
| 2 | Panduan cetak baru tanpa "Lanskap/A4" | Baca SKILL.md Format output, contoh, README FAQ, `kerangka-html.md` aturan #5 | ✔ Tidak ada lagi anjuran A4/Lanskap; diganti "Simpan sebagai PDF → margin Tidak ada → centang Grafis latar" |
| 3 | Overlay "putar HP" (CSS) | 390×844 tegak | ✔ overlay tampil penuh layar (390×844) dengan pesan jelas (`ss-03-hp-tegak-overlay-putar.png`). Catatan: juga muncul di tablet 820px tegak (di sana slide sebenarnya sudah terbaca ±14px) dan tidak bisa ditutup — lihat cacat ringan |
| 4 | Kontrol tidak menutupi slide di HP mendatar | Cek tumpang-tindih kotak `.kontrol` & tombol Edit dengan setiap elemen teks, semua slide ketiga deck, di 844×390, 932×430, 667×375, 1280×720 | ✔ 0 tumpang-tindih; kontrol dikecilkan & dipudarkan (opacity 0,45) di HP mendatar |
| 5 | Angka KUR wajib via `pengajuan-kur`, CSV via `rekap-penjualan-csv` | Ikuti SKILL.md baru: jalankan `simulasi_kur.py --format json` & `rekap.py`, isi slide dari JSON | ✔ Aturan jelas & bisa diikuti (termasuk jalur `[isi]` bila skill tidak terpasang). Angka identik dengan verifikasi independen v1.0: cicilan Rp 4.563.291, rasio 46,6% (BERAT), total bunga Rp 14.278.462; omzet Rp 41.190.000, kategori 77,8/22,2%, mingguan berjumlah tepat |
| 6 | Validator diperluas + `tests/uji_validasi.py` 20 kasus | Jalankan tes bawaan + 27 file uji penguji (13 file lama dibuat ulang di atas kerangka baru + 14 kasus baru) | ✔ 20/20 tes bawaan OK. Semua 5 celah v1.0 kini tertangkap (tanpa kutip, `srcset`, `url(//…)`, `fetch`, `<img src="C:\…">`); baru juga tertangkap: tanpa `@page`, `@page` tanpa `size`, `<img src=logo.png>`, XHR, `@import "https://…"`, `SRC="HTTPS://…"` huruf besar, `<iframe src=https…>`. Kerangka asli & gambar base64 LULUS. Sisa celah/kekeliruan di cacat ringan |
| 7 | Komponen siap pakai + 4 tema | Bangun 3 deck hanya dengan kelas bawaan (`kartu-kpi`, `tabel-data` + `uang`, `dua-kolom`, `timeline`, `kutipan`, `isi`) | ✔ Semua komponen jalan, tidak ada yang meluber, kolom uang rata kanan sejajar. ✗ Tema **Hitam Emas Premium**: `--warna-teks-lembut` tidak didefinisikan untuk tema gelap → paragraf, poin, dan label kartu memakai `#475569` di atas `#111111` = kontras **2,49:1** (minimal 4,5:1) |
| 8 | Font stack sistem | Render di Linux (tanpa Segoe UI/Verdana) | ✔ Jatuh ke cadangan dengan rapi; klaim di `aturan-desain.md` #4 sudah jujur |
| 9 | Mode Edit (`contenteditable`) | Playwright: klik Edit, pilih angka di slide 4, ketik "Rp 43.000.000", simpan halaman, buka ulang | ✗ **Tombol Spasi dan panah kiri/kanan tetap menggerakkan slide saat mengetik** (handler `keydown` tidak mengecualikan elemen yang sedang diedit dan memanggil `preventDefault`). Hasil: ketik "Rp" → Spasi → slide pindah ke 5/10, spasi tidak masuk, teks jadi "Rp". File yang disimpan saat mode edit masih aktif dibuka ulang dengan 76 elemen `contenteditable="true"` (garis putus-putus tampil) dan tombol "✔ Selesai edit" |
| — | Tanpa internet & validator | 3 deck | ✔ 0 request jaringan; `validasi_html.py` LULUS tanpa peringatan |
| — | Teks meluber (1920×1080) | Bounding box semua elemen, 31 slide | ✔ tidak ada elemen di luar area aman |

## Skor v1.1.0
| Kriteria | v1.0 | v1.1.0 | Alasan |
|---|---|---|---|
| Pemicu (description) | 8 | 8 | Tidak berubah, tetap tepat |
| Kemudahan awam | 7 | 7 | PDF & HP kini beres; tetapi mode Edit yang dianjurkan di setiap balasan langsung "loncat slide" saat menekan spasi |
| Kualitas output | 6 | 8 | Komponen rapi & konsisten, PDF utuh; tema gelap kontras buruk |
| Akurasi (angka/fakta) | 8 | 9 | Angka KUR & CSV kini wajib dari script |
| Penanganan input kurang | 9 | 9 | Ada kalimat "cukup jawab nomor 1" |
| Penanganan di luar cakupan | 9 | 9 | — |
| Keamanan | 9 | 9 | Bersih; mode edit tanpa localStorage/jaringan |

## SKOR AKHIR v1.1.0: **6 / 10 — REVISI**
Semua cacat v1.0 (PDF terpotong, teks HP, validator bocor, KUR tanpa `pengajuan-kur`, tanpa komponen) **terbukti sudah diperbaiki**. Skor tetap dibatasi ≤ 6 karena fitur baru yang **dianjurkan ke setiap pembeli di Format output** ("Mau edit teks langsung? Klik tombol ✏️ Edit…") rusak pada ketikan paling dasar (spasi), sehingga melanggar prinsip "reliable". Perbaikannya kecil (±3 baris); dengan perbaikan cacat berat + tema gelap, perkiraan skor **8**.

## Cacat v1.1.0 & saran perbaikan

### Berat
1. **Mode Edit: Spasi/panah memindah slide dan menelan ketikan** — `references/kerangka-html.md`, handler `document.addEventListener('keydown', …)`. Tambahkan di baris pertama handler: `if (e.target.isContentEditable) return;` (dan sama untuk `touchstart/touchend` bila target sedang diedit). Saat `btnEdit` diklik untuk selesai, pastikan semua `contenteditable` dilepas; tambahkan `beforeprint`/`@media print { [contenteditable] { outline: none !important; } }` dan ingatkan "klik ✔ Selesai edit dulu sebelum Ctrl+S". Tambahkan catatan bahwa Ctrl+S tidak tersedia di HP (edit hanya di laptop).

### Sedang
2. **Tema Hitam Emas Premium tidak terbaca** — `aturan-desain.md` #5 dan `kerangka-html.md` bagian "Tema warna": tambahkan kolom `--warna-teks-lembut` untuk tiap tema (mis. `#cfc8b8` untuk Hitam Emas; kontras ≥ 4,5:1), lalu tambahkan cek kontras sederhana ke validator (bandingkan `--warna-teks-lembut` vs `--warna-latar-slide`).

### Ringan
3. **Validator menolak tautan WA/website yang sah** — `<a href="https://wa.me/62…">` diberi ERROR padahal tautan tidak memuat apa pun saat dibuka offline. Kecualikan `<a href>` (cukup peringatan), fokus ERROR pada `src`/`srcset`/`<link href>`/CSS.
4. **Validator belum menangkap** `url("foto-toko.jpg")` lokal di CSS dan `<video src="promo.mp4">`/`<source src>` lokal — perlakukan sama seperti `<img>` non-`data:`.
5. **Overlay "putar HP" tidak bisa ditutup** dan muncul juga di tablet tegak (≤900px). Tambahkan tombol "Tetap lihat" (untuk HP yang kunci rotasinya aktif) dan batasi ke `max-width: 600px`.
6. **Label "BERAT" di slide ke bank** — SKILL.md bagian KUR menyuruh memasukkan hasil `pengajuan-kur` "apa adanya" ke slide. Sebaiknya: kategori BERAT dan plafon aman disampaikan ke **pengguna** di ringkasan akhir (untuk dipertimbangkan sebelum ke bank), sedangkan slide cukup berisi cicilan & rasio.

## Screenshot v1.1.0
- `ss-01-laporan-slide4-laptop.png` — tabel per produk dengan komponen `tabel-data`.
- `ss-02-pdf-v1.1-halaman-utuh.png` — halaman PDF (cetak bawaan Chromium) slide "Rencana penggunaan dana": semua nominal & porsi tampil.
- `ss-03-hp-tegak-overlay-putar.png` — overlay "Putar HP" di 390×844.

---

# Uji ulang v1.1.1

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi diuji:** 1.1.1 (commit b7caab9)
- **Lingkungan:** /tmp/uji-presentasi-instan/v111; Playwright 1.56 + Chromium 1194 (`/opt/pw-browsers`); pypdfium2.
- **Dibangun ulang dengan kerangka v1.1.1:** `kur-maju-jaya-motor.html` (Hijau Amanah), **`kur-maju-jaya-motor-gelap.html` (Hitam Emas Premium, baru)**, `laporan-agustus-2026.html`, `pitch-bersih-kilat.html`. Angka KUR dari `simulasi_kur.py --format json`, angka laporan dari `rekap.py`.

## Verifikasi tiap klaim perbaikan

| # | Klaim | Cara uji (Playwright/Chromium) | Hasil |
|---|---|---|---|
| 1 | Keydown/swipe diabaikan saat mengedit | Mode Edit → pilih angka slide 4 → ketik `Rp 43.000.000` → ←, ←, →, PageDown → End → ketik ` ok` → klik di luar teks lalu Spasi → swipe (TouchEvent 600→300px) di 844×390 | ✔ Halaman tetap 4/10 setelah semua ketikan, panah, PageDown, dan Spasi di luar teks; teks jadi `Rp 43.000.000 ok` (spasi masuk). Swipe saat edit tidak memindah slide; tombol ‹ › tetap bisa dipakai. Setelah "Selesai edit", panah & swipe kembali normal |
| 2 | "Selesai edit" menghapus semua `contenteditable` | Hitung elemen `[contenteditable]` | ✔ 76 saat edit → **0** setelah selesai; class `mode-edit` terlepas |
| 3 | Sisa `contenteditable` dibersihkan saat dibuka | Simpan halaman (DOM) **saat mode edit masih aktif**, buka ulang | ✔ 0 elemen editable, panah kanan berfungsi, perubahan teks tetap tersimpan. ✗ ringan: label tombol masih "✔ Selesai edit" (hijau) walau mode lihat — lihat cacat ringan 1 |
| 4 | Outline disembunyikan saat print | `outline-style` elemen editable di media print; cetak PDF saat mode edit aktif | ✔ `none`; PDF saat mode edit 10 halaman, utuh |
| 5 | Catatan Ctrl+S hanya laptop | Baca teks `alert` | ✔ Menyebut: Spasi/panah tidak memindah slide, klik "Selesai edit" dulu, Ctrl+S/Cmd+S hanya di laptop, di HP minta AI agent mengubah & mengirim ulang |
| 6 | `--warna-teks-lembut` per tema | Tabel `aturan-desain.md` #5; bangun deck KUR tema gelap; hitung ulang kontras dengan rumus WCAG sendiri | ✔ Kolom baru; `#cfc8b8`/`#111111` = 11,34:1, `#475569`/`#ffffff` = 7,58:1 (cocok dengan tabel). Deck gelap terbaca di layar & PDF (label kartu, tabel, timeline, `[isi]`) |
| 7 | Cek kontras WCAG di validator | Tema gelap dengan teks-lembut bawaan; kuning muda `#fde68a` di putih; tema gelap benar | ✔ ERROR pada dua kasus buruk, LULUS pada tema gelap benar. Celah ringan: warna `rgb()` dan latar yang diganti lewat CSS kelas tidak dicek (tanpa peringatan) |
| 8 | wa.me → peringatan | `<a href="https://wa.me/…">` dengan & tanpa kutip | ✔ exit 0 + peringatan "tautan navigasi" |
| 9 | CSS `url()` lokal & video/audio/source lokal → error | `url("foto-toko.jpg")`, `<video src="promo.mp4">`, `<audio><source src="jingle.mp3">` | ✔ ketiganya ERROR; `url(#grad)` & `url("data:…")` tetap LULUS (tidak salah tangkap) |
| 10 | Overlay "Tetap lihat" + max-width 600px | 390×844, 412×915, 600×960, 768×1024, 820×1180; klik "Tetap lihat"; putar ke lanskap & kembali | ✔ Overlay muncul di ≤600px, hilang setelah "Tetap lihat" (slide bisa dinavigasi); tidak muncul di tablet 768/820 (teks di sana ±12,8–13,7px, terbaca). Lanskap: overlay hilang otomatis |
| 11 | Label BERAT/AMAN tidak di slide, disampaikan ke pengguna + plafon aman | SKILL.md bagian KUR + Format output; deck KUR | ✔ Aturan & baris "Catatan kelayakan pinjaman (…TIDAK ditaruh di slide)" ada; deck berisi 0 kata "BERAT"; ringkasan ke pengguna memuat plafon aman Rp 96.640.000 dari `simulasi_kur.py` (lihat contoh 02) |
| 12 | 26 tes validator | `python3 tests/uji_validasi.py` | ✔ 26/26 OK |

### Validator: 38 file uji penguji
- Semua 27 kasus v1.1.0 tetap benar (regresi nol): internet via `<link>`/`src`/`srcset`/tanpa kutip/huruf besar/iframe/`@import`/`url(//)`/fetch/XHR → ERROR; gambar lokal → ERROR; tanpa `@media print`/`@page size` → ERROR; kosong/tanpa slide → ERROR; bukan UTF-8 & file hilang → exit 2; slide padat → peringatan; kerangka asli & base64 → LULUS.
- Kasus baru: kontras (3 kasus) ✔, wa.me tanpa kutip ✔, `url(#…)`/`url(data:)` tidak salah tangkap ✔, `<audio><source>` lokal ✔.
- Masih lolos (ringan): `poster="sampul.jpg"` pada `<video>`, `<a href="brosur.pdf">` lokal, `<link rel="icon" href="favicon.png">` (tidak merusak tampilan), warna non-hex.

### Regresi (semua deck v1.1.1)
| Pemeriksaan | Hasil |
|---|---|
| Request jaringan | ✔ 0 di 4 deck |
| `validasi_html.py` | ✔ LULUS tanpa peringatan di 4 deck |
| Teks meluber / dekat tepi (1920×1080) | ✔ tidak ada |
| Kontrol & tombol Edit menutupi teks (844×390, 932×430, 667×375, 1280×720, semua slide) | ✔ 0 tumpang-tindih |
| PDF: Chromium bawaan, anjuran (margin 0 + latar), tanpa grafis latar, dipaksa A4 lanskap | ✔ jumlah halaman = jumlah slide (10/10/8/13), 1440×810pt; **0 nilai Rupiah/persen hilang** (KUR terang 19, KUR gelap 19, laporan 30); latar gelap ikut tercetak walau "grafis latar" tidak dicentang |

## Skor v1.1.1
| Kriteria | v1.0 | v1.1.0 | v1.1.1 | Alasan |
|---|---|---|---|---|
| Pemicu (description) | 8 | 8 | 8 | Tepat, kata kunci ID/EN |
| Kemudahan awam | 7 | 7 | 9 | Buka offline, HP (overlay + "Tetap lihat"), PDF tanpa atur kertas, edit teks bekerja |
| Kualitas output | 6 | 8 | 8 | Komponen rapi, 4 tema terbaca; desain tetap sederhana dibanding sumber |
| Akurasi (angka/fakta) | 8 | 9 | 9 | Angka wajib dari `pengajuan-kur`/`rekap-penjualan-csv`; penilaian kelayakan ke pengguna, bukan ke bank |
| Penanganan input kurang | 9 | 9 | 9 | — |
| Penanganan di luar cakupan | 9 | 9 | 9 | — |
| Keamanan | 9 | 9 | 9 | Tanpa jaringan/localStorage |

## SKOR AKHIR v1.1.1: **8 / 10 — LULUS**
Semua klaim perbaikan terbukti bekerja di Chromium, tanpa regresi. Tidak ada cacat berat atau sedang yang tersisa. Sisa cacat ringan di bawah tidak menghalangi uji platform asli oleh pemilik.

## Cacat ringan tersisa (saran)
1. `kerangka-html.md` blok "Bersihkan sisa mode edit": saat file yang disimpan dalam mode edit dibuka ulang, label tombol masih "✔ Selesai edit" + kelas `aktif`. Tambahkan reset `btnEdit.textContent = '✏️ Edit'; btnEdit.classList.remove('aktif');` di blok pembersih tersebut.
2. Komponen timeline (`.langkah p` 22px, nomor 18px) dan `.kutipan .sumber` (22px) di bawah batas "jangan pernah di bawah 24px" di `aturan-desain.md` #2 — naikkan ke 24–26px.
3. Validator: cek kontras hanya untuk hex di `:root`; beri peringatan bila warna memakai `rgb()`/nama warna, atau bila `.slide { background: … }` ditimpa di luar variabel. Tambahkan `poster=` dan `<a href>` ke file lokal (mis. `brosur.pdf`) sebagai peringatan.

## Screenshot v1.1.1
- `ss-01-laporan-slide4-laptop.png` — tabel per produk (tidak berubah dari v1.1.0).
- `ss-02-pdf-v1.1-halaman-utuh.png` — kini halaman PDF **tema gelap** (cetak tanpa "grafis latar"): cicilan, rasio, sisa laba, tanpa label BERAT.
- `ss-03-hp-tegak-overlay-putar.png` — overlay 390×844 dengan tombol "Tetap lihat".

## Catatan koordinator — v1.1.2 (setelah uji ulang v1.1.1, skor 8 LULUS)
Cacat ringan 1–2 diperbaiki langsung di `references/kerangka-html.md`: blok pembersih saat load kini juga mengembalikan label & kelas tombol Edit ke "✏️ Edit"; teks timeline, nomor timeline, dan sumber kutipan dinaikkan ke 24px (lingkaran nomor 40px) sesuai aturan-desain #2. Cacat ringan 3 (kontras rgb()/latar kelas, poster= dan tautan PDF lokal) dicatat untuk versi berikutnya.

---
## Uji ulang v1.1.5 (2026-10-13, penguji independen, OpenClaw sebelum/sesudah)
- OpenClaw 2026.10.2 lokal, skenario pitch investor laundry kiloan yang sama (pesan identik); SEBELUM tanpa skill, SESUDAH hanya skill ini. Rincian di `00-openclaw-sebelum-sesudah.md`.
- Skor tanpa skill **6,0** -> dengan skill **8,5** (selisih +2,5), **LULUS** acuan (sesudah >= 8 dan selisih >= 1,5). Validator skill: SESUDAH LULUS tanpa peringatan.
- Perbaikan v1.1.5 terbukti: klaim "selesai 1-2 hari" dan "repeat order rutin tiap minggu" tidak muncul lagi; rincian dana, tarif, dan kontak ditulis `[isi ...]`. Tanpa skill, rincian dana Rp 250 juta dan klaim "profitable/terbukti" dikarang sebagai fakta.
- Sisa temuan ringan: tagline "terpercaya" dan satu kalimat pasar umum di slide 2; chat hanya memuat urutan judul slide, angka kunci, asumsi, dan daftar yang harus dilengkapi (teks tiap slide hanya di berkas HTML); tidak ada PDF otomatis.
