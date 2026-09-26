# Ceklis Teknis & Prioritas Audit

Kerangka prioritas ini mengadaptasi urutan audit dari skill sumber (`seo-audit`, MIT — lihat `ATTRIBUTION.md`), ditulis ulang & disederhanakan untuk toko online/UMKM Indonesia. Dipakai bersama hasil `scripts/cek_halaman.py`.

## Urutan prioritas (kerjakan dari atas)

1. **Bisa ditemukan Google atau tidak** (noindex, canonical yang salah) — kalau ini bermasalah, sisanya percuma karena halaman memang tidak akan muncul.
2. **Dasar halaman** (title, meta description, H1) — ini yang langsung memengaruhi apakah orang mau klik dari hasil pencarian.
3. **Isi halaman** (heading berurutan, gambar dengan alt, tautan berfungsi) — memengaruhi pengalaman pengunjung & pemahaman Google soal isi halaman.
4. **Data tambahan** (Open Graph, schema/JSON-LD) — bonus tampilan lebih menarik di hasil pencarian & saat dibagikan.
5. **Kata kunci & konten** — apakah halaman memang membahas apa yang dicari orang.
6. **Kecepatan & mobile** — pengalaman teknis, dicek manual (lihat `kecepatan-mobile.md`).
7. **Lokal (Google Business Profile/Maps)** — khusus usaha dengan lokasi fisik/area layanan (lihat `lokal-dan-gmb.md`).

## Ambang aman (dipakai skrip `cek_halaman.py`)

| Bagian | Kosong | Terlalu pendek | Pas (aman) | Berpotensi terpotong |
|---|---|---|---|---|
| Title | tidak ada tag `<title>` | < 30 karakter | 30–60 karakter | > 60 karakter |
| Meta description | tidak ada isi | < 70 karakter | 70–155 karakter | > 155 karakter |

**Catatan jujur:** Google sebenarnya memotong tampilan berdasarkan LEBAR PIKSEL huruf, bukan jumlah karakter — jadi ini perkiraan aman berbasis karakter (standar umum industri), bukan patokan resmi Google. Selalu sebutkan ini ke pengguna, jangan menjanjikan angka pasti.

**Kenapa batas bawah "Pas" di sini (30/70) lebih longgar dari konvensi umum (biasanya 50-60 untuk title, 150-160 untuk meta description — termasuk yang dipakai skill sumber ATM `seo-audit`: "Title Tags: 50-60 characters", "Meta Descriptions: 150-160 characters"):**
- Batas ATAS ("berpotensi terpotong") **tetap dipakai sama persis dengan konvensi umum** (60 untuk title, 155 untuk meta description, hampir sama dengan 160) — ini bagian yang paling penting karena berisiko halaman terpotong di hasil pencarian.
- Batas BAWAH sengaja dilonggarkan (30 & 70, bukan 50 & 150) supaya skill ini **tidak salah menandai "PENDEK/perlu diperbaiki"** untuk title yang sebenarnya sudah lengkap & jelas tapi natural pendek — pola yang umum untuk UMKM Indonesia, mis. `"Ayam Geprek Bu Sri - Cibiru, Bandung"` (36 karakter) sudah menyebut nama usaha + kategori + lokasi secara lengkap, tapi akan tertandai "PENDEK" kalau memakai ambang 50. Konvensi 50-60/150-160 ditulis untuk konteks SERP kompetitif (SaaS/e-commerce besar bersaing banyak kata kunci) yang memang perlu memaksimalkan setiap karakter; ini bukan prioritas utama untuk audiens skill ini (pemilik usaha awam yang butuh feedback jelas & tidak membuat panik untuk hal yang sebenarnya sudah baik — lihat CLAUDE.md §1 "instan tapi reliable").
- Kalau pengguna/pemilik produk ingin menyamakan persis dengan konvensi 50-60/150-160 (mis. untuk toko dengan persaingan kata kunci ketat), ini bisa diubah lewat konstanta `BATAS_TITLE_MIN`/`BATAS_DESC_MIN` di `scripts/cek_halaman.py` — dicatat di sini supaya keputusan ini terlihat jelas & bisa ditinjau ulang, bukan disembunyikan sebagai detail implementasi.

## Heading (H1–H6)

- Idealnya **tepat satu H1** per halaman, isinya mewakili topik utama halaman.
- Heading tidak boleh "melompat level" tanpa alasan (mis. H1 langsung ke H3 tanpa H2) — ini tanda struktur halaman berantakan, membuat Google (dan pembaca) sulit memahami hierarki isi.
- Heading kosong (tidak ada teksnya) biasanya bug dari page builder/tema — beri tahu pengguna untuk dicek manual di editor situsnya.

## Gambar & alt text

- Gambar **produk/konten** wajib punya alt text yang menjelaskan isinya secara wajar (mis. "Keripik pedas Bandung kemasan 250 gram"), bukan nama file asal (`IMG_2381.jpg`) dan bukan dijejali kata kunci berulang (`keripik pedas keripik pedas keripik pedas` — ini keyword stuffing, dilarang).
- Gambar **dekoratif murni** (garis pemisah, ikon hiasan) boleh punya `alt=""` (kosong secara sengaja) — ini valid, beri tahu pengguna bedanya supaya tidak salah paham menganggap semua alt kosong itu salah.
- Skrip membedakan "atribut alt tidak ada sama sekali" (lebih perlu diperbaiki) dari "atribut alt ada tapi isinya kosong" (bisa jadi sengaja untuk dekorasi, perlu dicek manual mana gambar kontennya).

## Tautan (link)

Skrip hanya mengecek **format** tautan dari file HTML (tidak mengakses internet, jadi tidak tahu apakah tujuannya benar-benar hidup). Yang ditandai:
- Kosong (`href=""`) atau cuma `#` — biasanya tombol yang lupa diisi tautan aslinya.
- `javascript:void(0)` atau sejenisnya — tombol yang seharusnya berfungsi lewat kode, tapi kalau kode itu gagal jalan (mis. JavaScript di-nonaktifkan atau error), tombolnya jadi tidak berfungsi sama sekali.
- Mengandung spasi mentah yang belum di-encode — bisa membuat tautan gagal dibuka di sebagian browser/aplikasi.

**Untuk cek tautan benar-benar hidup/mati (butuh internet):** sarankan pengguna klik satu-satu tautan penting, atau gunakan alat pengecek tautan gratis seperti fitur bawaan Google Search Console ("Coverage report") — di luar cakupan skrip ini yang sengaja offline.

## Canonical & meta robots

- **Canonical tidak ada** pada halaman produk yang bisa diakses lewat beberapa URL (mis. dengan/tanpa parameter filter warna/ukuran) berisiko membuat Google bingung mana yang mau ditampilkan, atau malah menampilkan versi yang salah.
- **`noindex` ditemukan** pada halaman yang seharusnya muncul di Google — ini SERIUS, artinya halaman itu sengaja/tidak sengaja disembunyikan. Sering terjadi tidak sengaja: situs baru dipindah dari mode "maintenance"/"coming soon" tapi lupa mematikan noindex-nya.
- Skrip tidak bisa membaca header HTTP `X-Robots-Tag` (perlu koneksi internet ke server) — kalau hasil skrip bersih tapi halaman tetap tidak muncul di Google setelah berminggu-minggu, minta pengguna cek ini lewat Google Search Console.

## Open Graph

Tag `og:title`, `og:description`, `og:image`, `og:type` menentukan tampilan saat link dibagikan ke WhatsApp/Facebook/Instagram Story. Tanpa ini, link tampil polos tanpa gambar/preview — mengurangi rasa percaya calon pembeli yang menerima link dari WhatsApp Business/broadcast.

## Data terstruktur (JSON-LD)

- **Keterbatasan penting (dari sumber `seo-audit`, dipertahankan karena valid):** banyak plugin SEO (Yoast, RankMath, AIOSEO di WordPress) menyisipkan JSON-LD lewat JavaScript setelah halaman dimuat. Kalau file HTML diambil dengan "Lihat Sumber Halaman" (View Source) di browser, JSON-LD hasil JavaScript ini **tidak akan terlihat** meski sebenarnya ada di halaman aktif. Sebaiknya pengguna simpan halaman dengan "Simpan Halaman Sebagai... HTML lengkap" atau gunakan Google Rich Results Test (https://search.google.com/test/rich-results, gratis, tanpa akun) untuk memastikan.
- Untuk `Product`: field penting `name`, `image`, `offers` (berisi `price`, `priceCurrency` — harus `"IDR"` untuk toko Indonesia, dan `availability`).
- Untuk `LocalBusiness`: lihat `skema-localbusiness.md`.
- **Jangan pernah** mengisi `aggregateRating`/`review` dengan angka karangan — kalau skrip menemukan field ini, selalu ingatkan pengguna untuk memverifikasi datanya asli.

## Kata kunci & konten

- Cek kemunculan kata kunci utama di title, H1, URL, dan paragraf pertama — ini sinyal dasar bahwa halaman memang membahas topik yang dicari orang.
- **Pencarian bersifat literal (persis sama urutan katanya)**, bukan mencari makna. Kalau H1-nya "Servis AC Panggilan di Bekasi" dan kata kuncinya "servis AC Bekasi", skrip akan melaporkan "tidak ditemukan" walau maknanya sama persis — jelaskan ini ke pengguna, jangan panik kalau hasilnya "TIDAK" padahal terasa sudah relevan; nilai dengan mata juga.
- **Jangan pernah menyarankan mengulang kata kunci berlebihan** (keyword stuffing) untuk "mengakali" hasil ini — cukup pastikan kata kuncinya muncul secara wajar dan sesuai konteks kalimat.
