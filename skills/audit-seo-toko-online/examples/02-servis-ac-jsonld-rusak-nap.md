# Skenario 02 (Normal) — Beranda jasa servis AC Bekasi, JSON-LD LocalBusiness salah format & NAP tidak konsisten

> Dibuat oleh **penguji independen** (agent terpisah, simulasi Claude Code, hanya membaca folder skill yang disalin ke scratchpad terpisah), sesuai pedoman kurasi Komunitech tahap 6. Data & HTML fiktif.

## Permintaan pengguna
> "Tolong audit SEO website servis AC saya, ini HTML halaman utamanya saya tempel. Google Bisnisku saya: CV Sejuk Selalu Teknik, alamat Jl. Raya Bekasi Timur No. 45, Bekasi Timur, Kota Bekasi, Jawa Barat 17111, telepon 0812-9988-7766. Kata kunci yang saya incar: 'servis AC Bekasi'."

*(HTML yang ditempel pengguna, dibuat sendiri oleh penguji)*
```html
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Servis AC Bekasi</title>
<meta name="description" content="Servis AC">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness"
  "name": "CV Sejuk Selalu Teknik",
  "telephone": "021-88991122",
  "address": "Jl. Raya Bekasi Timur No. 45"
}
</script>
</head>
<body>
<h1>Servis AC Panggilan Area Bekasi &amp; Sekitarnya</h1>
<p>Kami melayani cuci AC, isi freon, dan perbaikan AC rumah/kantor di seluruh Bekasi, datang hari yang sama.</p>
<h2>Kenapa Pilih Kami</h2>
<h2>Area Layanan</h2>
<p>Bekasi Timur, Bekasi Barat, Bekasi Selatan, Cikarang</p>
<h2>Hubungi Kami</h2>
<p>Alamat: Jln. Raya Bekasi Timur No 45, Bekasi</p>
<p>Telepon/WA: 0812-9988-7766</p>
<img src="ac-cuci.jpg" alt="teknisi sedang">
<img src="ac-freon.jpg">
<a href="https://wa.me/6281299887766">Chat WhatsApp</a>
<a href="tel: 02188991122">Telepon Kami</a>
</body>
</html>
```
Usaha punya lokasi fisik/area layanan (servis panggilan) → bagian lokal/GMB dijalankan (Langkah 5 SKILL.md).

## Langkah 1-2 — Jalankan `scripts/cek_halaman.py`
```
python3 scripts/cek_halaman.py 02-servis-ac-bekasi.html --kata-kunci "servis AC Bekasi" --url "https://sejukselalu.co.id/"
```
Output nyata:
```
== Judul (title) ==
Status: PENDEK — "Servis AC Bekasi" (16 karakter)

== Meta description ==
Status: PENDEK — "Servis AC" (9 karakter)

== Heading (H1-H6) ==
Jumlah H1: 1 (baik). Urutan heading tidak melompat level.

== Gambar & teks alternatif (alt) ==
Total gambar: 2. Tanpa atribut alt sama sekali: 1 -> ac-freon.jpg

== Tautan ==
Total tautan <a>: 2. Format bermasalah: 1 -> 'tel: 02188991122' (mengandung_spasi_mentah)

== Canonical ==
Ada: False

== Meta robots ==
Tidak ada (default: boleh diindeks).

== Open Graph ==
Ditemukan: (tidak ada)
[PERINGATAN] Tag penting belum ada: og:title, og:description, og:image, og:type

== Data terstruktur (JSON-LD) ==
  Blok #1: [ERROR] JSON tidak valid: Expecting ',' delimiter (baris 4, kolom 3)

== Kata kunci utama: "servis AC Bekasi" ==
  Muncul di title: YA | di H1: TIDAK | di URL: TIDAK | di paragraf awal: TIDAK

== Ukuran halaman ==
954 bytes (~0.9 KB).
```

**Verifikasi independen (penguji):**
- `len("Servis AC Bekasi")` = **16**, `len("Servis AC")` = **9** — dihitung ulang manual, cocok persis dengan skrip.
- JSON-LD dicoba `json.loads()` manual di luar skrip: **gagal** dengan pesan identik `Expecting ',' delimiter: line 4 column 3` — memang ada baris `"@type": "LocalBusiness"` tanpa koma sebelum `"name": ...` berikutnya. Skrip melaporkan error dengan benar, tidak crash, tidak mengarang isi JSON yang gagal di-parse.
- "di_h1" dilaporkan TIDAK meski H1 secara makna membahas "Servis AC ... Bekasi" — ini SESUAI penjelasan `checklist-teknis.md` soal pencarian literal (kata kunci "servis ac bekasi" tidak persis berurutan di H1 "Servis AC Panggilan Area Bekasi"). Bukan bug, harus dijelaskan ke pengguna sesuai Langkah 3 & Batasan SKILL.md.
- **NAP dicek manual (Langkah 5, `references/lokal-dan-gmb.md`):** ditemukan **3 versi telepon berbeda** dalam satu halaman — `021-88991122` (JSON-LD, gagal parse), `tel: 02188991122` (tombol telepon, sama nomor tapi ada spasi mentah bikin formatnya bermasalah), dan `0812-9988-7766` (teks halaman + WhatsApp, **cocok** dengan Google Bisnisku). Alamat juga berbeda 3 versi: JSON-LD "Jl. Raya Bekasi Timur No. 45" (tanpa kota/provinsi), teks halaman "Jln. Raya Bekasi Timur No 45, Bekasi" (singkatan "Jln." beda dari "Jl.", tanpa titik di "No 45"), dan Google Bisnisku "Jl. Raya Bekasi Timur No. 45, Bekasi Timur, Kota Bekasi, Jawa Barat 17111" (paling lengkap). Ini temuan NAP nyata, bukan dikarang — jadi prioritas tinggi sesuai `lokal-dan-gmb.md`.

## Laporan Akhir (dikirim ke pengguna)

# Laporan Audit SEO: CV Sejuk Selalu Teknik

Halaman yang diaudit: (HTML ditempel manual, URL diasumsikan https://sejukselalu.co.id/ dari konteks — **asumsi**, lihat bawah)
Kata kunci utama yang ditarget: servis AC Bekasi
Tanggal audit: 2026-09-25

## Ringkasan Skor
| Bagian | Skor | Catatan singkat |
|---|---|---|
| Judul & meta description | ❌ | Title cuma 16 karakter, meta description cuma 9 karakter — keduanya terlalu pendek |
| Heading & struktur isi | ✅ | 1 H1, urutan heading tidak melompat |
| Gambar & tautan | ⚠️ | 1 foto tanpa alt; 1 tombol telepon formatnya bermasalah (spasi di `tel:`) |
| Canonical & meta robots | ⚠️ | Canonical tidak ada; meta robots aman (tidak ada noindex) |
| Open Graph & data terstruktur | ❌ | Open Graph tidak ada sama sekali; JSON-LD LocalBusiness **rusak (bukan JSON valid)** karena kurang tanda koma |
| Kata kunci & konten | ⚠️ | Muncul di title, tapi belum di H1/paragraf awal (lihat catatan pencarian literal) |
| Kecepatan di HP (manual) | — | Belum dicoba pengguna |
| Google Business Profile/Maps & lokal | ❌ | **NAP tidak konsisten**: 3 versi nomor telepon & 3 versi alamat berbeda di halaman ini saja |

## Daftar Perbaikan (urut prioritas)
1. **Perbaiki JSON-LD yang rusak** — Dampak: Tinggi · Kemudahan: Mudah. Masalah: ada baris `"@type": "LocalBusiness"` tanpa tanda koma setelahnya, membuat SELURUH kode ini dianggap error oleh Google (bukan cuma diabaikan — bisa bikin Search Console menandai error). Cara perbaiki: pakai contoh JSON-LD yang sudah benar & lengkap di bawah.
2. **Samakan NAP (Nama-Alamat-Telepon) di semua tempat** — Dampak: Tinggi · Kemudahan: Mudah. Masalah: nomor telepon di JSON-LD/tombol telepon (021-88991122) BEDA dari yang di teks halaman & Google Bisnisku (0812-9988-7766); alamat juga ditulis 3 versi berbeda (lihat detail di atas). Cara perbaiki: pakai SATU nomor & SATU format alamat di semua tempat — ikuti persis yang ada di Google Bisnisku.
3. **Perpanjang title** — Dampak: Tinggi · Kemudahan: Mudah. 16 karakter, pakai title baru (51 karakter).
4. **Perpanjang meta description** — Dampak: Tinggi · Kemudahan: Mudah. 9 karakter, pakai teks baru (144 karakter).
5. **Tambah alt text foto `ac-freon.jpg`** — Dampak: Sedang · Kemudahan: Mudah.
6. **Perbaiki tombol telepon** — Dampak: Rendah · Kemudahan: Mudah. `href="tel: 02188991122"` ada spasi setelah `tel:` yang bisa membuatnya gagal di sebagian HP — sekalian ganti ke nomor yang benar (lihat poin 2): `href="tel:+6281299887766"`.
7. **Tambahkan Open Graph** — Dampak: Sedang · Kemudahan: Sedang.

## Teks Siap Tempel
**Title baru (51 karakter):**
```
Servis AC Panggilan Bekasi - CV Sejuk Selalu Teknik
```
**Meta description baru (144 karakter):**
```
Servis AC panggilan area Bekasi: cuci AC, isi freon, perbaikan AC rumah & kantor. Teknisi datang hari yang sama, hubungi CV Sejuk Selalu Teknik.
```
**Contoh JSON-LD LocalBusiness terisi (perbaikan dari yang rusak):**
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "CV Sejuk Selalu Teknik",
  "telephone": "+6281299887766",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Jl. Raya Bekasi Timur No. 45",
    "addressLocality": "Kota Bekasi",
    "addressRegion": "Jawa Barat",
    "postalCode": "17111",
    "addressCountry": "ID"
  },
  "areaServed": ["Bekasi Timur", "Bekasi Barat", "Bekasi Selatan", "Cikarang"]
}
</script>
```
*(Nomor telepon di atas memakai versi yang cocok dengan Google Bisnisku pengguna, bukan nomor landline lama yang beda — sesuai perbaikan NAP poin 2.)*

## Batasan Hasil Audit Ini
- URL asli halaman tidak disebutkan pengguna secara eksplisit; dipakai sebagai asumsi dari konteks penamaan usaha untuk pengecekan kata kunci di URL — **cek ulang** apakah domain sungguhannya cocok.
- Pencarian kata kunci bersifat literal — "servis AC Bekasi" belum ditemukan persis di H1/paragraf awal walau maknanya sudah dekat ("Servis AC Panggilan Area Bekasi"); ini valid, bukan salah baca.
- Tautan hanya dicek formatnya, bukan apakah nomor telepon aktif.
- Kecepatan halaman belum dicek — belum dicoba pengguna dengan data seluler.
- Tidak ada data volume pencarian untuk "servis AC Bekasi" — tidak tersedia.

## Asumsi yang Dipakai
URL halaman diasumsikan `https://sejukselalu.co.id/` (tidak disebutkan eksplisit oleh pengguna) — dipakai hanya untuk cek kata kunci di URL, bukan bagian keputusan lain.

---
## Catatan verifikasi penguji (bukan bagian laporan ke pengguna)
- Semua temuan teknis diambil dari output nyata skrip (dijalankan sungguhan di atas), termasuk pesan error JSON-LD yang diverifikasi ulang independen dengan `json.loads()` manual — pesan error identik.
- **Temuan NAP tidak konsisten adalah temuan asli dari HTML yang dibuat penguji secara sengaja** untuk menguji apakah skill benar-benar membandingkan NAP lintas sumber sesuai `references/lokal-dan-gmb.md` — skill (mengikuti instruksinya) berhasil mendeteksinya dengan benar ketika dijalankan langkah demi langkah.
- Skill dengan benar TIDAK menjanjikan ranking, TIDAK mengarang volume pencarian, dan menjelaskan keterbatasan pencarian kata kunci literal secara eksplisit di laporan — sesuai Batasan SKILL.md.
- **Lulus** untuk skenario ini.
