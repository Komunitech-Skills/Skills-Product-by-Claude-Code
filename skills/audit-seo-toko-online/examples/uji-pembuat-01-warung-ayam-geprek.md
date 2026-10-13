# Contoh 01 (Normal) — "Audit SEO website warung ayam geprek saya"

> Dibuat oleh **pembuat skill** untuk verifikasi awal (menjalankan skrip sungguhan dan memeriksa hasilnya), **bukan pengganti** pengujian independen pedoman kurasi Komunitech tahap 6.

## Permintaan pengguna
> "Tolong audit SEO website warung ayam geprek saya. Saya tempel isi halamannya ya. Kata kunci yang saya mau ditarget: 'ayam geprek Cibiru'. Nama usaha di Google Bisnisku: Ayam Geprek Bu Sri, alamatnya Jl. Cibiru Indah No. 12, Kec. Cibiru, Kota Bandung, Jawa Barat 40615, telepon 0812-3456-7890."
>
> *(HTML yang ditempel pengguna — hasil "Lihat Sumber Halaman" dari websitenya):*
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Home</title>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Ayam Geprek Bu Sri"
}
</script>
</head>
<body>
<h1>Selamat Datang di Website Kami</h1>
<h3>Menu Favorit</h3>
<p>Kami menjual berbagai macam ayam geprek dengan level kepedasan 1 sampai 10, cocok untuk pecinta pedas di daerah Cibiru.</p>
<img src="geprek1.jpg">
<img src="geprek2.jpg" alt="">
<img src="warung.jpg" alt="Warung Ayam Geprek Bu Sri tampak depan">
<h2>Alamat</h2>
<p>Jl. Cibiru Indah No 12, Bandung</p>
<a href="https://wa.me/6281234567890">Pesan via WhatsApp</a>
<a href="#">Lihat Menu Lengkap</a>
<a href="javascript:void(0)">Lokasi Kami</a>
</body>
</html>
```
URL asli: `https://ayamgeprekbusri.example.com/`

## Langkah 1-2 — Ambil HTML & jalankan analisis teknis
HTML disimpan ke file sementara, lalu dijalankan:
```
python3 scripts/cek_halaman.py warung-ayam-geprek.html --kata-kunci "ayam geprek Cibiru" --url "https://ayamgeprekbusri.example.com/"
```
Output nyata (dijalankan sungguhan, bukan dikarang):
```
== Judul (title) ==
Status: PENDEK
Teks : Home
Judul cuma 4 karakter — kemungkinan kurang deskriptif, ruang di hasil pencarian belum dipakai maksimal.

== Meta description ==
Status: KOSONG
Tidak ada meta description.

== Heading (H1-H6) ==
Jumlah H1: 1 (baik)
  H1: Selamat Datang di Website Kami
  [PERINGATAN] Lompat dari H1 ke H3 di heading: "Menu Favorit"

== Gambar & teks alternatif (alt) ==
Total gambar: 3
Tanpa atribut alt sama sekali: 1  -> geprek1.jpg
Atribut alt ada tapi kosong: 1    -> geprek2.jpg

== Tautan (format saja) ==
Total tautan <a>: 3
Format bermasalah: 2  -> '#' (kosong_atau_pagar), 'javascript:void(0)' (javascript_pseudo_link)

== Canonical ==
Ada: False

== Meta robots ==
Tidak ada meta robots (default: boleh diindeks).

== Open Graph ==
Ditemukan: (tidak ada)
[PERINGATAN] Tag penting belum ada: og:title, og:description, og:image, og:type

== Data terstruktur (JSON-LD) ==
  Blok #1: valid JSON. Tipe: LocalBusiness
    - LocalBusiness: field 'address' tidak ada.
    - LocalBusiness: field 'telephone' tidak ada.
    - LocalBusiness: jam operasional tidak ada — opsional tapi disarankan.

== Kata kunci utama: "ayam geprek Cibiru" ==
  Muncul di title: TIDAK
  Muncul di H1: TIDAK
  Muncul di URL: TIDAK
  Muncul di paragraf awal: TIDAK

== Ukuran halaman (HTML mentah saja) ==
757 bytes (~0.7 KB). Kecil, kemungkinan bukan penyebab lambat.
```

## Langkah 3-6 — Terjemahkan, cek data terstruktur, lokal/GMB, kecepatan
- **Data terstruktur:** `LocalBusiness` valid tapi kurang `address` & `telephone` — disiapkan contoh JSON-LD terisi dari `references/skema-localbusiness.md`.
- **NAP:** alamat di HTML ("Jl. Cibiru Indah No 12, Bandung") berbeda dari alamat Google Bisnisku yang disebut pengguna ("Jl. Cibiru Indah No. 12, Kec. Cibiru, Kota Bandung, Jawa Barat 40615") — kurang lengkap (tanpa kecamatan/provinsi/kode pos) dan beda titik pada "No." vs "No". Ini ditandai sebagai temuan prioritas tinggi sesuai `references/lokal-dan-gmb.md`.
- **Kecepatan:** tidak diukur (di luar cakupan skrip); ditanyakan ke pengguna "sudah coba buka pakai data seluler?" — belum dijawab, jadi bagian ini ditandai "—" dan disebut di batasan.

## Laporan Akhir (dikirim ke pengguna)

# Laporan Audit SEO: Ayam Geprek Bu Sri

Halaman yang diaudit: https://ayamgeprekbusri.example.com/ (HTML ditempel manual)
Kata kunci utama yang ditarget: ayam geprek Cibiru
Tanggal audit: 2026-09-25

## Ringkasan Skor

| Bagian | Skor | Catatan singkat |
|---|---|---|
| Judul & meta description | ❌ | Title cuma "Home", meta description kosong |
| Heading & struktur isi | ⚠️ | Ada 1 H1 (bagus), tapi lompat ke H3 tanpa H2 |
| Gambar & tautan | ⚠️ | 1 gambar tanpa alt sama sekali, 2 tautan format bermasalah |
| Canonical & meta robots | ⚠️ | Canonical tidak ada; meta robots aman (tidak ada noindex) |
| Open Graph & data terstruktur | ❌ | Open Graph tidak ada sama sekali; LocalBusiness ada tapi alamat & telepon kosong |
| Kata kunci & konten | ❌ | "ayam geprek Cibiru" tidak muncul di title/H1/URL/paragraf awal |
| Kecepatan di HP (manual) | — | Belum dicoba pengguna, lihat Batasan |
| Google Business Profile/Maps & lokal (manual) | ❌ | Alamat website TIDAK konsisten dengan Google Bisnisku (NAP) |

## Daftar Perbaikan (urut prioritas)

1. **Samakan alamat website dengan Google Bisnisku (NAP)** — Dampak: Tinggi · Kemudahan: Mudah
   - Masalah: website tertulis "Jl. Cibiru Indah No 12, Bandung", Google Bisnisku "Jl. Cibiru Indah No. 12, Kec. Cibiru, Kota Bandung, Jawa Barat 40615". Beda ini bisa membingungkan Google soal apakah dua sumber ini usaha yang sama.
   - Cara perbaiki: ganti teks alamat di website persis sama dengan yang di Google Bisnisku (lihat teks siap tempel di bawah).

2. **Ganti judul (title) halaman** — Dampak: Tinggi · Kemudahan: Mudah
   - Masalah: title cuma "Home", tidak menyebut nama usaha atau kata kunci apa pun.
   - Cara perbaiki: pakai title baru di bawah (36 karakter, dalam rentang aman 30-60).

3. **Tambahkan meta description** — Dampak: Tinggi · Kemudahan: Mudah
   - Masalah: tidak ada sama sekali, Google akan ambil cuplikan acak.
   - Cara perbaiki: pakai teks siap tempel di bawah (141 karakter, dalam rentang aman 70-155).

4. **Lengkapi data terstruktur LocalBusiness (address & telephone)** — Dampak: Sedang · Kemudahan: Mudah
   - Masalah: schema LocalBusiness sudah ada tapi kosong alamat & telepon, jadi tidak banyak membantu tampilan di Google.
   - Cara perbaiki: pakai contoh JSON-LD siap isi di bawah.

5. **Tambah alt text untuk foto `geprek1.jpg`** — Dampak: Sedang · Kemudahan: Mudah
   - Masalah: foto produk tanpa keterangan sama sekali.
   - Cara perbaiki: `alt="Ayam geprek level 5 dengan sambal bawang, disajikan dengan nasi hangat"` (sesuaikan dengan foto aslinya).

6. **Perbaiki heading yang lompat dari H1 ke H3** — Dampak: Rendah · Kemudahan: Mudah
   - Masalah: "Menu Favorit" pakai H3, padahal tidak ada H2 sebelumnya.
   - Cara perbaiki: ubah "Menu Favorit" jadi H2.

7. **Perbaiki 2 tombol dengan tautan format bermasalah** — Dampak: Rendah · Kemudahan: Sedang
   - Masalah: "Lihat Menu Lengkap" (href="#") dan "Lokasi Kami" (href="javascript:void(0)") tidak mengarah ke mana pun.
   - Cara perbaiki: isi dengan tautan sungguhan (mis. link Google Maps untuk "Lokasi Kami", link halaman menu untuk "Lihat Menu Lengkap"). Perlu diisi pengguna karena skill ini tidak tahu URL tujuan sebenarnya.

8. **Tambahkan tag Open Graph** — Dampak: Sedang · Kemudahan: Sedang
   - Masalah: tidak ada `og:title`/`og:image`/dst., jadi tampilan link polos saat dibagikan ke WhatsApp.
   - Cara perbaiki: tambahkan 4 tag Open Graph dasar (perlu akses edit `<head>` website — tanyakan ke pembuat website kalau bukan dikerjakan sendiri).

## Teks Siap Tempel

**Title baru (36 karakter):**
```
Ayam Geprek Bu Sri - Cibiru, Bandung
```

**Meta description baru (141 karakter):**
```
Ayam geprek Cibiru level 1-10, sambal bawang pedas mantap. Warung Ayam Geprek Bu Sri, Jl. Cibiru Indah, Bandung. Pesan langsung via WhatsApp.
```

**Alamat (samakan persis dengan Google Bisnisku):**
```
Jl. Cibiru Indah No. 12, Kec. Cibiru, Kota Bandung, Jawa Barat 40615
```

**Contoh JSON-LD LocalBusiness terisi:**
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Ayam Geprek Bu Sri",
  "telephone": "+6281234567890",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Jl. Cibiru Indah No. 12",
    "addressLocality": "Kota Bandung",
    "addressRegion": "Jawa Barat",
    "postalCode": "40615",
    "addressCountry": "ID"
  }
}
</script>
```

## Batasan Hasil Audit Ini
- Tautan hanya dicek formatnya, bukan apakah benar-benar berfungsi (skill ini tidak mengakses internet).
- Kecepatan halaman & skor mobile belum dicek — belum dicoba pengguna dengan data seluler. Ikuti ceklis di `references/kecepatan-mobile.md` lalu kirim hasilnya kalau mau dibantu diartikan.
- Tidak ada data volume pencarian untuk "ayam geprek Cibiru" — skill ini tidak punya akses ke tool riset kata kunci berbayar, jadi tidak ditampilkan angka apa pun untuk itu.
- Pencarian kata kunci bersifat literal — kata "ayam geprek Cibiru" memang belum muncul persis di mana pun, ini valid (bukan salah baca), karena paragraf awal cuma menyebut "ayam geprek... di daerah Cibiru" (urutan kata beda).

## Asumsi yang Dipakai
Tidak ada asumsi tambahan — semua data (alamat, telepon, kata kunci) berasal langsung dari pengguna.

---

## Catatan pembuat skill (verifikasi, bukan bagian laporan ke pengguna)
- Semua temuan teknis (title "Home", meta description kosong, 1 H1, lompatan heading H1→H3, 1 gambar tanpa alt & 1 alt kosong, 2 tautan format bermasalah, canonical tidak ada, LocalBusiness kurang address/telephone, kata kunci tidak ditemukan di 4 lokasi) diambil **langsung dari output nyata `cek_halaman.py`** di atas, bukan dikarang.
- Panjang title & meta description baru diverifikasi independen dengan `python3 -c "print(len('...'))"`: title baru = **36 karakter** (bukan 34 seperti draf awal — dikoreksi), meta description baru = **141 karakter** (bukan 140 — dikoreksi). Keduanya dalam rentang aman.
- Contoh ini menunjukkan pentingnya Langkah 9 (verifikasi angka, bukan kira-kira) — draf pertama laporan sempat salah hitung manual sebelum dicek ulang dengan `len()` yang sebenarnya.
