# Skenario 01 (Normal) — Halaman produk WooCommerce, title kepanjangan & alt kosong

> Dibuat oleh **penguji independen** (agent terpisah, simulasi Claude Code, hanya membaca folder `audit-seo-toko-online/` yang disalin ke scratchpad terpisah — bukan pembuat skill), sesuai pedoman kurasi Komunitech tahap 6. Data & HTML fiktif, dibuat sendiri oleh penguji.

## Permintaan pengguna
> "Audit SEO halaman produk toko saya dong: https://tokorenyahjaya.co.id/produk/keripik-pedas-bandung-250gr/ — saya tempel HTML-nya juga (dari Lihat Sumber Halaman). Kata kunci yang saya incar: 'keripik pedas Bandung'."

*(HTML yang ditempel pengguna, WooCommerce, dibuat sendiri oleh penguji untuk kasus ini)*
```html
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Jual Keripik Pedas Bandung Original Enak Renyah Level 1 sampai 10 Terlaris Harga Murah Grosir Eceran Kirim Seluruh Indonesia</title>
<link rel="canonical" href="https://tokorenyahjaya.co.id/produk/keripik-pedas-bandung-250gr/">
<meta property="og:title" content="Keripik Pedas Bandung 250gr">
<meta property="og:type" content="product">
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Keripik Pedas Bandung 250gr",
  "offers": { "@type": "Offer", "price": "22000", "priceCurrency": "IDR" }
}
</script>
</head>
<body>
<div class="woocommerce">
<h1>Keripik Pedas Bandung 250gr</h1>
<img src="https://tokorenyahjaya.co.id/wp-content/uploads/2026/01/IMG_20260114_093022.jpg">
<img src="https://tokorenyahjaya.co.id/wp-content/uploads/2026/01/IMG_20260114_093101.jpg" alt="">
<img src="https://tokorenyahjaya.co.id/wp-content/uploads/2026/01/logo-toko.png" alt="">
<p>Keripik pedas Bandung asli, digoreng renyah setiap hari, tersedia level 1 sampai 10, tanpa pengawet, cocok untuk hadiah dan oleh-oleh.</p>
<h3>Detail Produk</h3>
<ul><li>Berat: 250 gram</li><li>Level pedas: 1-10 (bisa custom campur)</li></ul>
<a href="#">Tambah ke Keranjang</a>
<a href="javascript:void(0)">Beli Sekarang</a>
<a href="/keranjang">Lihat Keranjang</a>
</div>
</body>
</html>
```

## Langkah 1-2 — Jalankan `scripts/cek_halaman.py`
```
python3 scripts/cek_halaman.py 01-woocommerce-keripik.html --kata-kunci "keripik pedas Bandung" --url "https://tokorenyahjaya.co.id/produk/keripik-pedas-bandung-250gr/"
```
Output nyata (dijalankan sungguhan oleh penguji):
```
== Judul (title) ==
Status: PANJANG
Teks : Jual Keripik Pedas Bandung Original Enak Renyah Level 1 sampai 10 Terlaris Harga Murah Grosir Eceran Kirim Seluruh Indonesia
Panjang 124 karakter, kemungkinan terpotong (...).

== Meta description ==
Status: KOSONG

== Heading (H1-H6) ==
Jumlah H1: 1 (baik)
  H1: Keripik Pedas Bandung 250gr
  [PERINGATAN] Lompat dari H1 ke H3 di heading: "Detail Produk"

== Gambar & teks alternatif (alt) ==
Total gambar: 3
Tanpa atribut alt sama sekali: 1  -> IMG_20260114_093022.jpg
Atribut alt ada tapi kosong: 2    -> IMG_20260114_093101.jpg, logo-toko.png

== Tautan ==
Total tautan <a>: 3
Format bermasalah: 2  -> '#' (kosong_atau_pagar), 'javascript:void(0)' (javascript_pseudo_link)

== Canonical ==
Ada: True -> ...produk/keripik-pedas-bandung-250gr/ ; Sama dengan URL: True

== Meta robots ==
Tidak ada (default: boleh diindeks).

== Open Graph ==
Ditemukan: og:title, og:type
[PERINGATAN] Tag penting belum ada: og:description, og:image

== Data terstruktur (JSON-LD) ==
  Blok #1: valid JSON. Tipe: Product
    - Product: field 'image' tidak ada.
    - Product.offers: 'availability' tidak ada.

== Kata kunci utama: "keripik pedas Bandung" ==
  Muncul di title: YA | di H1: YA | di URL: YA | di paragraf awal: YA

== Ukuran halaman ==
1400 bytes (~1.4 KB).
```

**Verifikasi independen (penguji, bukan mengutip skrip mentah-mentah):**
- Panjang title dihitung ulang dengan `python3 -c "print(len(...))"` → **124 karakter**, cocok persis dengan output skrip.
- Dicek ulang manual dengan regex `<title>(.*?)</title>` terpisah dari parser skrip → hasil sama: 124 karakter, status PANJANG (>60) sudah benar.
- Dicek manual dengan regex `<h[1-6]>` → ditemukan H1 lalu H3 langsung (tidak ada H2), cocok dengan "lompatan level" yang dilaporkan.
- Dicek manual atribut `alt` tiap `<img>` → 1 gambar tanpa atribut `alt` sama sekali, 2 gambar dengan `alt=""` — cocok persis.
- JSON-LD `Product` diverifikasi dengan `json.loads()` manual: valid, memang tidak ada field `image` dan `offers.availability` — cocok.

## Terjemahan & laporan (mengikuti `references/checklist-teknis.md`, `templates/laporan-audit.md`)
Karena ini toko online murni tanpa lokasi fisik yang disebutkan pengguna, bagian **Google Business Profile/lokal** ditandai "—" (tidak berlaku) sesuai Langkah 5 SKILL.md. Bagian **kecepatan HP** ditandai "—" karena pengguna belum mencoba (tidak ditanya balik karena bukan info wajib, cukup disebut di Batasan sesuai tabel Input SKILL.md).

# Laporan Audit SEO: Keripik Pedas Bandung 250gr — Toko Renyah Jaya

Halaman yang diaudit: https://tokorenyahjaya.co.id/produk/keripik-pedas-bandung-250gr/ (HTML ditempel manual)
Kata kunci utama yang ditarget: keripik pedas Bandung
Tanggal audit: 2026-09-25

## Ringkasan Skor
| Bagian | Skor | Catatan singkat |
|---|---|---|
| Judul & meta description | ❌ | Title 124 karakter (kemungkinan terpotong di Google), meta description kosong |
| Heading & struktur isi | ⚠️ | 1 H1 (bagus), tapi lompat ke H3 tanpa H2 |
| Gambar & tautan | ⚠️ | 1 foto tanpa alt sama sekali, 2 foto dengan alt kosong, 2 tombol tautan format bermasalah |
| Canonical & meta robots | ✅ | Canonical ada & cocok URL; tidak ada noindex |
| Open Graph & data terstruktur | ⚠️ | Open Graph belum lengkap (belum ada og:description/og:image); schema Product ada tapi belum ada gambar & status stok |
| Kata kunci & konten | ✅ | "keripik pedas Bandung" sudah muncul di title, H1, URL, dan paragraf awal |
| Kecepatan di HP (manual) | — | Belum dicoba pengguna, lihat Batasan |
| Google Business Profile/Maps & lokal | — | Toko online murni, tidak ada lokasi fisik/area layanan yang disebutkan |

## Daftar Perbaikan (urut prioritas)
1. **Persingkat title** — Dampak: Tinggi · Kemudahan: Mudah. Masalah: 124 karakter, kemungkinan terpotong "..." di hasil pencarian. Cara perbaiki: pakai title baru di bawah (50 karakter).
2. **Tambahkan meta description** — Dampak: Tinggi · Kemudahan: Mudah. Masalah: kosong, Google ambil cuplikan acak. Cara perbaiki: pakai teks siap tempel di bawah (143 karakter).
3. **Tambah alt text untuk foto `IMG_20260114_093022.jpg`** — Dampak: Sedang · Kemudahan: Mudah. Foto produk utama tanpa keterangan sama sekali.
4. **Cek 2 foto dengan `alt=""` (kosong)** — Dampak: Rendah · Kemudahan: Mudah. Kalau itu foto produk (bukan hiasan), isi alt-nya; kalau memang dekoratif (mis. logo kecil), boleh dibiarkan kosong sesuai `references/checklist-teknis.md`.
5. **Lengkapi schema Product** — Dampak: Sedang · Kemudahan: Sedang. Tambahkan `image` dan `offers.availability` (mis. `https://schema.org/InStock`) di JSON-LD.
6. **Perbaiki heading yang lompat H1→H3** — Dampak: Rendah · Kemudahan: Mudah. Ubah "Detail Produk" jadi H2.
7. **Perbaiki 2 tautan bermasalah** — Dampak: Rendah · Kemudahan: Sedang. "Tambah ke Keranjang" (`#`) dan "Beli Sekarang" (`javascript:void(0)`) — perlu diisi fungsi sungguhan oleh developer/plugin toko, di luar kendali teks halaman.
8. **Lengkapi Open Graph** — Dampak: Sedang · Kemudahan: Sedang. Tambahkan `og:description` dan `og:image` supaya tampilan bagus saat dibagikan ke WhatsApp.

## Teks Siap Tempel
**Title baru (50 karakter):**
```
Keripik Pedas Bandung Original 250gr | Renyah Jaya
```
**Meta description baru (143 karakter):**
```
Keripik pedas Bandung original 250 gram, level 1-10, digoreng renyah setiap hari tanpa pengawet. Kirim seluruh Indonesia dari Toko Renyah Jaya.
```
**Alt text (foto tanpa alt sama sekali):**
- `IMG_20260114_093022.jpg` → `"Keripik pedas Bandung 250 gram dalam kemasan berdiri siap kirim"` (63 karakter)

## Batasan Hasil Audit Ini
- Tautan hanya dicek formatnya, bukan apakah tombol keranjang/beli benar-benar berfungsi (butuh akses ke sistem toko, di luar kendali teks HTML).
- Kecepatan halaman & skor mobile belum dicek — belum dicoba pengguna dengan data seluler (lihat `references/kecepatan-mobile.md`).
- Tidak ada data volume pencarian untuk "keripik pedas Bandung" — tidak tersedia tool berbayar untuk itu.

## Asumsi yang Dipakai
Tidak ada — semua data (URL, kata kunci) berasal dari pengguna.

---
## Catatan verifikasi penguji (bukan bagian laporan ke pengguna)
Semua temuan di atas diambil langsung dari output nyata `cek_halaman.py` (dijalankan sungguhan, lihat di atas) dan diverifikasi ulang independen dengan `len()` Python dan regex terpisah — tidak ada angka dikarang. **Lulus** untuk skenario ini: instruksi SKILL.md diikuti tahap demi tahap, hasil skrip diterjemahkan akurat, dan skill dengan benar tidak mengarang data volume pencarian atau skor kecepatan.
