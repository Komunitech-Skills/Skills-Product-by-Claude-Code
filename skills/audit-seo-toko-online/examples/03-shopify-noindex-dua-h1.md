# Skenario 03 (Normal) — Halaman produk Shopify fashion muslim, noindex tak sengaja & dua H1

> Dibuat oleh **penguji independen** (agent terpisah, simulasi Claude Code, hanya membaca folder skill yang disalin ke scratchpad terpisah), sesuai Tahap 6 CLAUDE.md. Data & HTML fiktif.

## Permintaan pengguna
> "Cek dong halaman produk gamis saya, kok sepi banget dari Google padahal udah lama online. Ini linknya https://busanamuslimah.myshopify.com/products/gamis-syari-adelia — saya tempel HTML-nya juga. Harga gamis ini Rp275.000, kata kunci yang saya incar 'gamis syari'."

*(HTML yang ditempel pengguna, tema Shopify, dibuat sendiri oleh penguji)*
```html
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Gamis Syari Adelia - Bahan Adem, Muslimah Elegan</title>
<meta name="description" content="Gamis syari Adelia bahan katun rayon adem, cocok untuk sehari-hari maupun acara formal, tersedia size S sampai XXL, gratis ongkir Jabodetabek.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://busanamuslimah.myshopify.com/products/gamis-syari-adelia">
<meta property="og:title" content="Gamis Syari Adelia">
<meta property="og:description" content="Gamis syari bahan adem, elegan, cocok segala acara">
<meta property="og:image" content="https://busanamuslimah.myshopify.com/cdn/shop/files/gamis-adelia-1.jpg">
<meta property="og:type" content="product">
</head>
<body>
<header><h1>Busana Muslimah Store</h1></header>
<main>
<h1>Gamis Syari Adelia</h1>
<img src="https://.../gamis-adelia-1.jpg" alt="Gamis syari Adelia warna dusty pink tampak depan">
<img src="https://.../gamis-adelia-2.jpg" alt="Gamis syari Adelia detail bahan">
<p>Gamis syari Adelia terbuat dari bahan katun rayon premium yang adem dan tidak menerawang, cocok dipakai sehari-hari maupun acara formal.</p>
<h2>Pilihan Ukuran</h2>
<p>S, M, L, XL, XXL</p>
<h2>Ulasan Pembeli</h2>
</main>
</body>
</html>
```

## Langkah 1-2 — Jalankan `scripts/cek_halaman.py`
```
python3 scripts/cek_halaman.py 03-shopify-fashion-muslim.html --kata-kunci "gamis syari" --url "https://busanamuslimah.myshopify.com/products/gamis-syari-adelia"
```
Output nyata:
```
== Judul (title) ==
Status: PAS — "Gamis Syari Adelia - Bahan Adem, Muslimah Elegan" (48 karakter)

== Meta description ==
Status: PAS — 142 karakter

== Heading (H1-H6) ==
Jumlah H1: 2 (PERIKSA: idealnya tepat 1)
  H1: Busana Muslimah Store
  H1: Gamis Syari Adelia
  Urutan heading tidak melompat level.

== Gambar & teks alternatif (alt) ==
Total gambar: 2. Tanpa atribut alt sama sekali: 0. Alt kosong: 0.

== Tautan ==
Total tautan <a>: 0.

== Canonical ==
Ada: True -> .../gamis-syari-adelia ; Sama dengan URL: True

== Meta robots ==
Nilai: noindex, follow
[PERINGATAN] noindex ditemukan — halaman ini DIMINTA agar TIDAK muncul di Google.

== Open Graph ==
Ditemukan: og:title, og:description, og:image, og:type (lengkap)

== Data terstruktur (JSON-LD) ==
Tidak ditemukan blok JSON-LD di file ini.

== Kata kunci utama: "gamis syari" ==
  Muncul di title: YA | di H1: YA | di URL: YA | di paragraf awal: YA

== Ukuran halaman ==
1349 bytes (~1.3 KB).
```

**Verifikasi independen (penguji):**
- `len()` manual untuk title = **48**, meta description = **142** — cocok persis dengan skrip, keduanya memang PAS, tidak perlu diubah (skill dengan benar TIDAK menyarankan perubahan yang tidak perlu).
- Dicek manual regex `<meta[^>]*name=["\']robots["\'][^>]*>` → ditemukan `content="noindex, follow"` — **valid, ini temuan nyata dari HTML, bukan salah baca skrip.**
- Dicek manual `<h1>` → memang ada 2 kemunculan tag H1 (satu di header/logo situs, satu di judul produk) — cocok dengan skrip.
- Skill mengikuti Langkah 1 SKILL.md dengan benar: kalimat apa pun di dalam HTML yang ditempel diperlakukan sebagai DATA yang diaudit, bukan instruksi — di skenario ini tidak ada percobaan prompt injection, tapi prinsipnya tetap relevan untuk dicatat sudah diikuti dalam pembacaan file.

## Laporan Akhir (dikirim ke pengguna)

# Laporan Audit SEO: Gamis Syari Adelia — Busana Muslimah Store

Halaman yang diaudit: https://busanamuslimah.myshopify.com/products/gamis-syari-adelia
Kata kunci utama yang ditarget: gamis syari
Tanggal audit: 2026-09-25

## Ringkasan Skor
| Bagian | Skor | Catatan singkat |
|---|---|---|
| Judul & meta description | ✅ | Title 48 karakter, meta description 142 karakter — keduanya sudah dalam rentang aman |
| Heading & struktur isi | ⚠️ | Ada 2 tag H1 di halaman ini (seharusnya cuma 1) |
| Gambar & tautan | ✅ | Kedua foto sudah punya alt text yang jelas |
| Canonical & meta robots | ❌ | **`noindex` ditemukan — halaman ini SEDANG DIMINTA untuk TIDAK ditampilkan di Google.** Ini kemungkinan besar penyebab utama kenapa halaman sepi dari pencarian, bukan soal konten. |
| Open Graph & data terstruktur | ⚠️ | Open Graph sudah lengkap (bagus untuk share ke WhatsApp/Instagram); tapi belum ada data terstruktur (JSON-LD) Product sama sekali |
| Kata kunci & konten | ✅ | "gamis syari" sudah muncul di title, H1, URL, dan paragraf awal |
| Kecepatan di HP (manual) | — | Belum dicoba pengguna |
| Google Business Profile/Maps & lokal | — | Toko online (Shopify), tidak disebutkan ada lokasi fisik/area layanan |

## Daftar Perbaikan (urut prioritas)
1. **Hapus `noindex` dari meta robots** — Dampak: Tinggi · Kemudahan: Mudah. Masalah: halaman ini secara aktif diminta disembunyikan dari Google — inilah kemungkinan besar alasan halaman sepi, BUKAN karena kontennya jelek (title, meta description, kata kunci semua sudah bagus). Cara perbaiki: kalau pakai Shopify, cek pengaturan tema/aplikasi SEO di admin Shopify (Online Store → Preferences, atau app SEO pihak ketiga) yang mungkin tidak sengaja mengaktifkan "hide from search engines"; kalau memakai tema kustom, cari & hapus baris `<meta name="robots" content="noindex...">` di kode temanya.
2. **Jadikan hanya satu H1 di halaman** — Dampak: Sedang · Kemudahan: Mudah. Masalah: "Busana Muslimah Store" di header dan "Gamis Syari Adelia" sama-sama pakai tag H1. Cara perbaiki: ganti H1 di header/logo situs menjadi tag biasa (mis. `<p>` atau `<div>` dengan styling logo), biarkan hanya "Gamis Syari Adelia" yang tetap H1 (ini topik utama halaman produk).
3. **Tambahkan data terstruktur (schema) Product** — Dampak: Sedang · Kemudahan: Sedang. Masalah: tidak ada JSON-LD sama sekali, jadi halaman tidak berpeluang tampil dengan info harga/stok langsung di hasil pencarian. Cara perbaiki: pakai contoh JSON-LD Product di bawah (harga sudah disebutkan pengguna, Rp275.000).

## Teks Siap Tempel
Title & meta description **sudah bagus, tidak perlu diganti** (48 & 142 karakter, keduanya dalam rentang aman).

**Contoh JSON-LD Product terisi:**
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Gamis Syari Adelia",
  "image": "https://busanamuslimah.myshopify.com/cdn/shop/files/gamis-adelia-1.jpg",
  "description": "Gamis syari Adelia bahan katun rayon adem, cocok untuk sehari-hari maupun acara formal.",
  "offers": {
    "@type": "Offer",
    "url": "https://busanamuslimah.myshopify.com/products/gamis-syari-adelia",
    "priceCurrency": "IDR",
    "price": "275000",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```
*(Catatan: cek dulu dengan Google Rich Results Test sebelum menambah manual — sebagian tema Shopify sudah otomatis membuat schema Product, jangan sampai ada dua schema untuk produk yang sama, sesuai `references/skema-localbusiness.md`.)*

## Batasan Hasil Audit Ini
- Skrip tidak bisa membaca header HTTP `X-Robots-Tag` — kalau setelah menghapus `noindex` di HTML halaman masih belum muncul di Google setelah beberapa minggu, cek juga pengaturan ini lewat Google Search Console.
- Kecepatan halaman belum dicek.
- Tidak ada data volume pencarian untuk "gamis syari" — tidak tersedia.
- Rating/ulasan pembeli (bagian "Ulasan Pembeli" di halaman) tidak diisi contoh apa pun oleh skill ini karena datanya harus asli dari sistem ulasan toko, bukan dikarang.

## Asumsi yang Dipakai
Tidak ada — semua data (harga, URL, kata kunci) berasal dari pengguna.

---
## Catatan verifikasi penguji (bukan bagian laporan ke pengguna)
- Temuan `noindex` dan 2×H1 diambil langsung dari output nyata skrip dan diverifikasi ulang manual dengan regex terpisah — cocok 100%.
- Panjang title (48) & meta description (142) diverifikasi ulang dengan `len()` Python independen — skill dengan benar TIDAK mengubah teks yang sudah bagus (tidak asal "memperbaiki" sesuatu yang tidak perlu diperbaiki), ini konsisten dengan prinsip "reliable" di CLAUDE.md.
- Harga (Rp275.000) yang dipakai di contoh JSON-LD berasal dari pernyataan eksplisit pengguna di permintaan, BUKAN dikarang oleh skill — sesuai Langkah 8 SKILL.md.
- **Lulus** untuk skenario ini. Ini skenario paling penting untuk menguji apakah skill bisa menemukan masalah "tersembunyi" (noindex) yang sering jadi penyebab utama tapi gampang terlewat kalau hanya dicek manual sekilas oleh pemilik usaha awam — skill lulus dengan baik.
