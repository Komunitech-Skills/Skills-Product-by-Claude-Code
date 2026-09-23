# Aturan desain (wajib dipatuhi agar aman untuk pengguna awam)

Tujuan aturan ini: presentasi tetap **enak dilihat dan mudah dibaca** meski dibuat
otomatis dan tanpa desainer, termasuk saat dibuka di layar HP kecil atau dicetak
hitam-putih.

## 1. Batas kata per slide

- **Judul slide:** maksimal 8 kata.
- **Isi per slide:** maksimal ±70 kata (skrip `scripts/validasi_html.py` akan menandai
  jika lebih). Untuk slide "speaker-led" (dipresentasikan langsung, bukan dibaca
  sendiri seperti laporan), usahakan jauh lebih sedikit: 3–5 poin pendek per slide.
- Jika kontennya banyak, **pecah jadi beberapa slide**, jangan mengecilkan ukuran teks
  sampai sulit dibaca.
- Poin (bullet) maksimal 6 per slide; kalau lebih, gunakan dua kolom atau slide lanjutan.

## 2. Keterbacaan di HP

Karena panggung 16:9 (1920×1080) diskalakan utuh ke layar berapa pun (lihat
`kerangka-html.md`), teks tetap proporsional di HP asal ukuran font dasarnya besar:

- Judul: minimal `72px` (skala 1920×1080), idealnya `88–120px` untuk slide pembuka.
- Isi: minimal `28px`, jangan pernah di bawah `24px`.
- Beri jarak antar elemen (padding/gap) minimal `32px` supaya tidak berdesakan saat
  discroll/dizoom di HP.

## 3. Kontras warna (wajib dicek manual)

Pasangan warna latar & teks harus kontras tinggi. Aturan sederhana yang aman dipakai
tanpa alat ukur:

- **Latar terang** (putih/krem/abu sangat muda) → **teks gelap pekat** (`#0f172a`,
  `#111827`, hitam), bukan abu-abu muda.
- **Latar gelap** (navy, hitam, hijau tua) → **teks putih/krem terang**, bukan abu-abu
  gelap.
- **Hindari:** teks abu-abu sedang di atas latar abu-abu sedang, teks warna cerah
  (kuning muda, pink muda) di atas latar putih, teks berwarna di atas foto tanpa lapisan
  gelap/terang transparan di belakangnya (overlay).
- Warna aksen brand (`--warna-aksen`) dipakai untuk judul kecil, garis, ikon, tombol —
  **jangan** dipakai untuk paragraf panjang kecuali sudah pasti kontrasnya tinggi.

## 4. Tumpukan font aman (tanpa internet)

Karena file harus mandiri (lihat `kerangka-html.md`), pakai tumpukan font sistem
berikut — dipilih agar punya cadangan yang aman di semua OS (Windows, macOS, Linux,
Android), bukan karena satu font yang sama persis terpasang di semua OS itu (mis.
`Segoe UI` hanya ada di Windows, `Roboto` umum di Android/Chrome OS, `Verdana`/`Georgia`
belum tentu ada di Linux/Android) — cadangan `system-ui`/`sans-serif`/`serif` di akhir
daftar memastikan tampilan tetap rapi meski font pertama tidak tersedia, walau bentuknya
tidak akan identik 100% di setiap perangkat:

| Gaya | Untuk judul (`--font-judul`) | Untuk isi (`--font-isi`) |
|---|---|---|
| Formal / korporat (investor, bank, B2B) | `Georgia, 'Times New Roman', serif` | `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` |
| Modern / bersih (profil perusahaan, produk) | `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` (bold) | `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` |
| Hangat / bersahabat (pelatihan karyawan, laporan internal) | `Verdana, Tahoma, system-ui, sans-serif` | `Verdana, Tahoma, system-ui, Arial, sans-serif` |

Jangan menulis nama font tunggal tanpa cadangan (mis. hanya `'Poppins'`) — kalau font
itu tidak ada di komputer pembaca, browser mengganti diam-diam ke font lain yang bisa
merusak proporsi ukuran yang sudah dihitung.

## 5. Palet warna siap pakai (boleh diganti sesuai warna brand pengguna)

Jika pengguna **tidak** menyebutkan warna brand, pakai salah satu palet netral berikut
sesuai konteks (dari `--warna-latar-slide`, `--warna-teks`, `--warna-aksen`):

| Nama | Latar slide | Teks | Aksen | Cocok untuk |
|---|---|---|---|---|
| Biru Korporat | `#ffffff` | `#0f172a` | `#2563eb` | Investor, B2B, KUR/bank |
| Hijau Amanah | `#ffffff` | `#14231b` | `#15803d` | KUR/bank, laporan keuangan, koperasi |
| Hitam Emas Premium | `#111111` | `#f5f1e6` | `#c9a227` | Profil perusahaan, produk premium |
| Putih Minimalis | `#ffffff` | `#1f2937` | `#111827` | Laporan bulanan, materi pelatihan |

Jika pengguna memberi warna brand (mis. kode HEX logo), pakai warna itu sebagai
`--warna-aksen` dan tetap jaga kontras sesuai aturan #3 (jangan pakai warna brand
sebagai warna teks paragraf jika kontrasnya lemah terhadap latar).

## 6. Angka Rupiah

- Format wajib: `Rp 1.250.000` — simbol "Rp", spasi, titik sebagai pemisah ribuan, tanpa
  desimal kecuali memang perlu (mis. harga per unit kecil).
- Jangan menyingkat ("1,2jt", "500rb") kecuali pengguna secara eksplisit minta gaya
  ringkas untuk slide highlight besar — jika begitu, tetap tulis angka lengkapnya di
  keterangan kecil di bawahnya.
- Jangan mengarang angka. Jika pengguna belum memberi angka, tulis placeholder yang
  jelas, misalnya `Rp [isi angka]`, dan sebutkan di ringkasan akhir bahwa angka itu
  masih perlu diisi pengguna.

## 7. Logo & warna brand

- Jika pengguna mengirim file logo, sisipkan sebagai `base64` (lihat aturan #3 di
  `kerangka-html.md`) di slide pembuka dan slide penutup saja — jangan diulang di setiap
  slide karena mengganggu fokus konten.
- Jika pengguna hanya memberi nama warna brand (mis. "biru navy kami"), tanyakan kode
  HEX-nya kalau ada; kalau tidak ada, pakai perkiraan warna yang wajar dan sebutkan itu
  sebagai asumsi di ringkasan akhir.

## 8. Jumlah slide wajar per konteks

Sebagai patokan (boleh disesuaikan permintaan pengguna):

| Konteks | Jumlah slide wajar |
|---|---|
| Pitch investor/angel | 10–15 |
| Proposal kerja sama B2B | 8–12 |
| Pengajuan KUR/bank | 8–12 |
| Laporan bulanan ke atasan | 6–10 |
| Profil perusahaan | 8–12 |
| Presentasi produk ke reseller | 8–15 |
| Materi pelatihan karyawan | 10–20 (boleh lebih banyak karena per-topik) |

## 9. Mode cetak (Print → Save as PDF)

- Blok `@page { size: 1920px 1080px; margin: 0; }` dan `@media print` di
  `kerangka-html.md` **wajib** ada persis seperti contoh — kombinasi keduanya yang
  membuat setiap slide jadi satu halaman PDF penuh **tanpa terpotong di sisi kanan**,
  dengan warna latar/aksen ikut tercetak, dan tanpa tombol navigasi ikut tercetak.
  Tanpa `@page` dengan ukuran yang cocok, browser memakai ukuran kertas default (mis.
  Letter tegak/A4) sehingga sisi kanan kanvas 1920×1080 terpotong — inilah cacat yang
  wajib dihindari.
- Ingatkan pengguna: di dialog cetak browser (Chrome/Edge — `Ctrl+P` Windows/Linux atau
  `Cmd+P` Mac), pilih tujuan **"Simpan sebagai PDF" / "Save as PDF"**, margin
  **"Tidak ada" / "None"**, dan centang **"Grafis latar" / "Background graphics"** agar
  warna latar & aksen ikut tercetak. **Jangan** menyuruh pengguna memilih ukuran kertas
  (A4/Letter) atau orientasi (Lanskap/Landscape) secara manual — ukuran halaman sudah
  diatur otomatis lewat `@page` di file HTML-nya, browser akan mengikutinya sendiri.
  Matikan juga "Print headers and footers" bila tersedia agar tidak ada tanggal/URL
  kecil di pojok halaman.
