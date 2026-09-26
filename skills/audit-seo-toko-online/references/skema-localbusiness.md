# Contoh Data Terstruktur (JSON-LD) untuk Usaha Indonesia

Tempel kode ini di dalam `<head>` halaman website, di antara tag `<script type="application/ld+json">` dan `</script>`. Ganti semua nilai contoh dengan data usaha yang sebenarnya — **jangan pernah menempel apa adanya tanpa diganti**.

## LocalBusiness — usaha dengan lokasi fisik (toko, bengkel, klinik, warung, servis panggilan)

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "GANTI: Nama Usaha Persis Sama dengan Google Business Profile",
  "image": "https://GANTI-domain-kamu.com/logo-atau-foto-usaha.jpg",
  "telephone": "+62GANTI-nomor-telepon-usaha",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "GANTI: Jl. Contoh No. 10",
    "addressLocality": "GANTI: Nama Kota/Kabupaten",
    "addressRegion": "GANTI: Nama Provinsi",
    "postalCode": "GANTI: Kode Pos",
    "addressCountry": "ID"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday"],
      "opens": "08:00",
      "closes": "14:00"
    }
  ],
  "priceRange": "GANTI: mis. Rp15.000 - Rp150.000"
}
</script>
```

**Catatan penting untuk field di atas:**
- `name` — HARUS sama persis (huruf besar/kecil, singkatan) dengan nama di Google Business Profile. Beda sedikit bisa membingungkan Google soal apakah ini usaha yang sama.
- `address` — inilah bagian **NAP (Nama-Alamat-Telepon)** yang wajib konsisten di semua tempat (website, Google Business Profile/Maps, media sosial, marketplace). Alamat yang beda-beda antar platform adalah kesalahan lokal SEO paling umum untuk UMKM.
- `addressCountry` untuk Indonesia selalu `"ID"` (kode 2 huruf ISO), bukan `"Indonesia"`.
- `openingHoursSpecification` bisa dihapus kalau usaha tidak punya jam operasional tetap (mis. servis panggilan 24 jam bisa pakai format berbeda — tanyakan ke pemilik daripada mengarang jam buka).
- Kalau usaha punya area layanan tanpa alamat toko fisik (mis. jasa servis AC panggilan), pertimbangkan `@type: "LocalBusiness"` dengan tambahan `areaServed` berisi nama kota/kecamatan yang dilayani, dan JANGAN mencantumkan alamat rumah pribadi kalau memang tidak ingin dipublikasikan — tanyakan dulu ke pemilik.

## Product — halaman produk toko online

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "GANTI: Nama Produk Persis Seperti di Halaman",
  "image": "https://GANTI-domain-kamu.com/foto-produk.jpg",
  "description": "GANTI: deskripsi singkat produk, sama dengan isi halaman",
  "offers": {
    "@type": "Offer",
    "url": "https://GANTI-domain-kamu.com/produk/nama-produk",
    "priceCurrency": "IDR",
    "price": "GANTI: harga angka saja, mis. 25000",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

**Catatan penting:**
- `priceCurrency` untuk toko Indonesia selalu `"IDR"`.
- `price` diisi angka saja tanpa "Rp" dan tanpa titik/koma pemisah ribuan (mis. `"25000"`, bukan `"Rp25.000"`).
- `availability` pakai nilai baku dari schema.org: `https://schema.org/InStock` (tersedia), `https://schema.org/OutOfStock` (habis), `https://schema.org/PreOrder` (pre-order).
- **`aggregateRating`/`review` HANYA ditambahkan kalau usaha benar-benar punya data rating/ulasan asli** (mis. dari sistem ulasan toko sendiri). Jangan pernah mengisi angka rating/jumlah ulasan karangan — ini melanggar Pedoman Konten Terstruktur Google dan berisiko dianggap ulasan palsu.

## Cara memasang untuk pengguna awam

1. Kalau website pakai **WordPress + plugin SEO** (Yoast, RankMath, AIOSEO): biasanya ada form isian "Local SEO"/"Business Info" di pengaturan plugin — lebih aman diisi lewat form itu daripada tempel kode manual, karena plugin yang mengatur penempatannya. Kode di atas berguna untuk verifikasi/perbandingan, bukan wajib ditempel manual kalau plugin sudah menyediakan form.
2. Kalau website **Shopify**: sebagian tema sudah otomatis menghasilkan schema `Product` — cek dulu dengan Google Rich Results Test sebelum menambah manual (menambah schema ganda untuk hal yang sama bisa membingungkan Google).
3. Kalau website **buatan sendiri/HTML statis**: tempel langsung kode di atas ke dalam `<head>`, setelah diisi datanya.
4. Setelah dipasang, **selalu tes** dengan Google Rich Results Test (https://search.google.com/test/rich-results) — gratis, tanpa akun, tempel URL halaman lalu lihat apakah schema terbaca tanpa error.
