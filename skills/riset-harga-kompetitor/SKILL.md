---
name: riset-harga-kompetitor
description: Riset harga pesaing untuk penjual UMKM - membuka link produk pesaing yang publik (atau membaca teks/screenshot yang ditempel), merapikan harga, harga coret, promo, rating, terjual, lokasi, menyetarakan ukuran (per gram/ml/pcs), lalu menghitung tabel pembanding (terendah, median, tertinggi), posisi harga kita, harga minimum dari HPP + biaya marketplace + target margin, dan rentang harga jual yang disarankan. Gunakan saat pengguna bilang "cek harga kompetitor", "bandingkan harga toko sebelah", "harga pasaran produk ini berapa", "harga saya kemahalan?", atau competitor price research, price benchmarking, market price comparison. Bukan untuk bot ubah harga otomatis, scraping yang perlu login, atau memantau harga terjadwal.
---

# Riset Harga Kompetitor

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menjawab pertanyaan penjual: "Harga pasaran produk seperti punya saya berapa, posisi harga saya di mana, dan sebaiknya saya pasang harga berapa supaya tetap untung?" Hasil akhirnya tabel pembanding + rekomendasi harga yang **tidak pernah di bawah batas untung** pengguna.

## Kapan digunakan
- Pengguna memberi link produk pesaing (Tokopedia, Shopee, TikTok Shop, Lazada, website toko) dan/atau menempel teks/screenshot halaman produk.
- Mau menentukan harga produk baru, atau mengecek apakah harga sekarang kemahalan/kemurahan.
- Mau tahu promo dan bundling yang dipakai pesaing.

## Kapan TIDAK digunakan (tolak dengan sopan, tawarkan alternatif)
- Memprediksi kapan/berapa pesaing akan mengubah harga, atau menebak strategi mereka → di luar cakupan; tawarkan cek ulang manual berkala.
- Bot yang mengubah harga otomatis, memantau harga terjadwal, atau mengambil ratusan halaman → tidak didukung.
- Membuka halaman yang butuh login, melewati captcha/blokir, atau memakai akun marketplace pengguna → **dilarang**; minta pengguna menempel teks/screenshot.
- Hanya butuh hitung potongan marketplace secara rinci → skill `harga-jual-marketplace`. Hanya butuh hitung modal → skill `hitung-hpp`.

## Input
| Info | Wajib? | Default / cara dapat |
|---|---|---|
| Data pesaing: link publik, teks yang ditempel, atau screenshot | Ya (min. 1, ideal 5-20) | — |
| HPP/modal per barang (termasuk kemasan) | Ya untuk batas untung & rekomendasi | Tanyakan; tawarkan skill `hitung-hpp`. Bila pengguna hanya tanya "harga pasaran berapa", boleh jalan tanpa HPP (mode pasar saja) |
| Ukuran/isi produk sendiri (mis. 250 gr, 1 L, isi 12; produk satuan = `1 pcs`) | Ya bila ukuran pesaing berbeda-beda | Tanyakan |
| Jual di marketplace? Persen biaya admin, layanan/ongkir, pembayaran, PPh 22 0,5% | Tidak | 0% (jualan langsung) — **sebut asumsinya**; tawarkan `harga-jual-marketplace` untuk rincian |
| Biaya tetap per barang (mis. biaya proses pesanan Rp1.250) | Tidak | 0 |
| Target margin (% laba dari harga jual) | Tidak | 20% |
| Harga jual sekarang | Tidak | — (tanpa ini posisi harga tidak ditampilkan) |
| Strategi: murah / tengah / premium | Tidak | tengah |

Jika HPP atau data pesaing belum ada, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna ingin cepat, pakai default di atas dan sebutkan asumsinya. **Jangan mengarang HPP, harga pesaing, atau persen biaya marketplace.**

## Langkah kerja

### 1. Kumpulkan data pesaing (sopan & legal)
- Jika kamu (agent) punya kemampuan bawaan membuka halaman web (web fetch/browser), buka link **satu per satu**, maksimal ±20 link per permintaan, hanya halaman publik tanpa login. Hormati robots.txt dan ketentuan situs; jangan mengulang terus-menerus, jangan menjadwalkan, jangan memakai cara melewati blokir.
- Jika halaman gagal dibuka, kosong, minta login, atau diblokir (Shopee dan Tokopedia sering begitu), **jangan mencoba cara lain**. Catat link itu, lalu minta pengguna: "Link ini tidak bisa saya buka. Tolong tempel teks halaman produknya atau kirim screenshot bagian harga, ukuran/varian, terjual, dan lokasi."
- Jika kamu tidak punya kemampuan membuka web, langsung minta teks/screenshot. Jangan menginstal alat scraping apa pun.
- Dari tiap produk, catat ke tabel: `toko, nama, platform, varian, ukuran, harga, harga_coret, promo, rating, terjual, ulasan, lokasi, sumber, tanggal_cek` (template: `templates/pesaing-template.csv`). Tulis **harga apa adanya** seperti tampil (mis. `Rp49.900`, `49,9rb`, `Rp 1,2 jt`, `49.900-59.900`); script yang merapikan.
- `harga` = harga yang dibayar pembeli sebelum ongkir (setelah diskon toko). `harga_coret` = harga yang dicoret. Voucher/gratis ongkir → kolom `promo`. `sumber` = link, atau "(ditempel pengguna)" / "(screenshot)". `tanggal_cek` = hari ini (YYYY-MM-DD).
- Pastikan varian yang dicatat **sebanding** dengan produk pengguna (ukuran/tipe sama atau bisa disetarakan). Jika ragu, tanyakan. Bila halaman menampilkan daftar varian dengan harga berbeda, catat **harga varian yang sebanding**, bukan rentangnya.
- `ukuran` ditulis seperti tampil: `250 gr`, `1/2 kg`, `setengah kilo`, `2 x 250 gr`, `250 gr x 2`, `isi 2 @250gr`, `250 g + 250 g`, `500 gr isi 2`, `2 pack 500 gr` (dua yang terakhir dikalikan + diberi catatan cek). Produk satuan tanpa berat/isi (hijab, kaos, dll.) → tulis `1 pcs` untuk produk pengguna **dan** pesaing; paket → `2 pcs`, `isi 3`.
- Di CSV, nilai yang mengandung koma (`"4,9"`, `"1,2RB terjual"`) **wajib diberi tanda kutip**, atau simpan sebagai JSON. Baris yang kolomnya bergeser dilewati script dengan alasan.

### 2. Hitung dengan script
Simpan tabel sebagai CSV di folder kerja pengguna, lalu jalankan (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
```bash
python3 <folder-skill-ini>/scripts/banding_harga.py pesaing.csv --nama "Kopi Gayo Bubuk" \
  --hpp 32.000 --ukuran "250 gr" --harga-kita 65.000 \
  --biaya-persen 8 --biaya-persen 4 --biaya-persen 0,5 --biaya-tetap 1.250 --margin 20
```
Opsi: `--strategi murah|tengah|premium`, `--rentang min|tengah|maks` (harga mana yang dipakai untuk "49.900-59.900", default terendah), `--pakai-semua` (ikutkan pesaing yang jauh dari median, **hanya setelah pengguna mengonfirmasi datanya benar**), `--tanggal YYYY-MM-DD`, `--format json`. Tanpa `--hpp` script berjalan dalam **mode pasar saja** (statistik pasar tanpa batas untung & rekomendasi). Data produk sendiri juga bisa ditaruh di file JSON: `{"produk_kita": {"hpp": ..., "ukuran": ..., "biaya_persen": [8, 4, 0.5]}, "pesaing": [...]}`.

Script otomatis: membaca format harga Indonesia (harga < Rp 100 ditolak sebagai salah tulis), membaca CSV UTF-8/ANSI Excel, membuang duplikat (link sama atau isi sama, beda harga disebut), melewati baris rusak dengan alasan, menyetarakan ukuran ke ukuran produk pengguna (bila teks memuat beberapa ukuran, dipilih yang satuannya sama dengan produk pengguna), menandai data > 30 hari, **mengeluarkan dari statistik** harga setara yang di bawah separuh atau di atas dua kali median (min. 3 pesaing; tetap tampil di tabel), lalu menghitung statistik & rekomendasi.

### 3. Sajikan hasil
- Tampilkan keluaran script **apa adanya** (tabel, ringkasan pasar, batas harga, rekomendasi, promo, "Perlu dicek", catatan & asumsi). Jangan mengubah angka.
- Jika ada baris bercatatan **"jauh dari median: TIDAK ikut statistik"**, tanyakan ke pengguna dalam pesan yang sama: "Harga/ukuran baris ini benar dan sebanding?" Bila benar (mis. memang produk premium), jalankan ulang dengan `--pakai-semua`; bila salah, perbaiki barisnya.
- Mode pasar saja (tanpa HPP): sajikan statistik pasar, lalu minta HPP untuk menghitung batas untung & rekomendasi. Jangan menyarankan harga jual tanpa HPP.
- Tambahkan 2-3 saran praktis berbasis data, mis.: "Pesaing terlaris di Rp49.900 memakai harga coret + gratis ongkir", "Rating kamu 4,9 dan lebih tinggi dari median: strategi tengah-atas masuk akal", "Dua pesaing memakai paket 2 x 250 gr; pertimbangkan bundling".
- Jika ada tanda **PERHATIAN** (pasar/median di bawah harga minimum), jelaskan dengan bahasa sederhana: jangan ikut banting harga; pilihan = tekan HPP, bundling, ukuran berbeda, tonjolkan keunggulan, atau pilih kanal lain.
- Sebutkan link yang gagal dibuka dan data yang dilewati.

### 4. Fallback tanpa Python
Hitung manual dengan rumus di bawah, urutkan harga setara dari kecil ke besar, dan beri tahu pengguna bahwa hasil dihitung manual.

## Rumus
```
harga setara      = harga pesaing / isi pesaing x isi produk kita   (satuan sama: g, ml, atau pcs)
per 100 g/ml      = harga / isi x 100 ; per pcs = harga / jumlah pcs
persentil p       = interpolasi linear, posisi = (n - 1) x p   (sama dengan PERCENTILE.INC)
harga balik modal = (HPP + biaya tetap) / (1 - biaya%)
harga minimum     = (HPP + biaya tetap) / (1 - biaya% - margin%)   → dibulatkan KE ATAS ke rupiah penuh
laba di harga P   = P - P x biaya% - HPP - biaya tetap ; margin = laba / P
rekomendasi       : murah   = [terendah .. P25], titik P25
                    tengah  = [P25 .. P75],     titik median
                    premium = [P75 .. P90],     titik P75
                    setiap angka dinaikkan ke harga minimum bila lebih rendah
harga cantik      = harga berakhiran 900 di dalam rentang yang paling dekat ke titik
```
Nominal lain dibulatkan ke rupiah terdekat. Statistik hanya memakai pesaing yang ikut dihitung (satuan sama, tidak jauh dari median). Contoh: HPP 32.000, biaya tetap 1.250, biaya 12,5%, margin 20% → minimum = 33.250 / 0,675 = 49.259,26 → **Rp 49.260**.

## Format output
```
## Riset Harga Pesaing: <produk> (<ukuran>)
Tanggal analisis | jumlah pesaing dipakai / duplikat / dilewati | dasar banding
| # | Toko / Produk | Varian / Ukuran | Harga tayang | Harga coret | Harga setara | Per satuan | Rating | Terjual | Lokasi | Catatan |
### Ringkasan harga pasar   (terendah, P25, median, P75, tertinggi + posisi harga kamu + pesaing terlaris)
### Batas harga kamu        (HPP, biaya, margin, harga balik modal, harga minimum)
### Rekomendasi harga       (rentang, titik, harga cantik, PERHATIAN bila ada)
### Promo & bundling pesaing
### Perlu dicek             (duplikat, baris dilewati, peringatan)
### Catatan & asumsi
💡 Saran: <2-3 saran berbasis data>
Link yang tidak bisa dibuka: <daftar, bila ada>
```

## Contoh
**Input:** "Tolong cek harga kopi gayo bubuk 250 gr di 8 link ini [link...]. Modal saya 32 ribu, jual di Shopee (admin 8%, gratis ongkir 4%, PPh 0,5%, biaya proses 1.250). Sekarang saya jual 65 ribu."

**Output (dipersingkat, dari script):** 6 pesaing dibandingkan (1 duplikat, 1 sachet tidak bisa disetarakan). Median setara 250 g **Rp 54.375** (P25 Rp 50.588, P75 Rp 57.188). Harga kamu Rp 65.000 lebih mahal dari 6 pesaing. Harga minimum Rp 49.260. **Rekomendasi Rp 50.588 - Rp 57.188**, titik Rp 54.375, harga cantik **Rp 53.900** (laba Rp 13.913, margin 25,81%). Contoh lengkap: `examples/contoh-pembuat-kopi-gayo.md`.

## Cara menguji harga baru (sampaikan singkat ke pengguna)
1. Ubah **satu hal saja** (harga, atau harga coret, atau paket), jangan sekaligus.
2. Jalankan 1-2 minggu; catat kunjungan produk, pesanan, dan konversi (pesanan / kunjungan) dari dashboard toko, lalu bandingkan dengan periode sebelumnya yang sepanjang itu (hindari tanggal gajian/hari besar yang berbeda).
3. Yang dinilai **total laba** (laba per barang x jumlah terjual), bukan hanya jumlah terjual. Tetap di atas harga minimum.
4. Harga coret harus jujur (pernah benar-benar dipakai). Cek ulang harga pesaing sebelum uji berikutnya.

## Checklist sebelum mengirim
- [ ] Tidak ada halaman yang dibuka lewat login/bypass; link gagal sudah dilaporkan & diminta teks/screenshot.
- [ ] Varian pesaing sebanding; ukuran produk sendiri disebut bila ukuran pesaing berbeda (produk satuan = `1 pcs`).
- [ ] Setiap baris bercatatan "jauh dari median" dan setiap peringatan di "Perlu dicek" sudah dikonfirmasi ke pengguna.
- [ ] HPP dari pengguna (bukan karangan); persen biaya marketplace dari pengguna atau asumsi 0% disebut.
- [ ] Angka dari script, tidak diubah; asumsi & tanggal cek tampil.
- [ ] Rekomendasi tidak di bawah harga minimum; tanda PERHATIAN dijelaskan.
- [ ] Format Rupiah `Rp 49.900`.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila: HPP 0/negatif/bukan angka, margin atau biaya negatif, biaya% + margin ≥ 100%, ukuran produk sendiri tidak dikenali, file tidak ada/kosong/hanya judul kolom/JSON rusak/file Excel/encoding tak dikenal, kolom harga tidak ditemukan, atau tidak ada satu pun harga pesaing yang terpakai. Jelaskan ke pengguna dan minta data yang benar (CSV dari Excel: Save As > "CSV UTF-8").
- Harga ambigu seperti `49,9` (tanpa "rb") dan harga di bawah Rp 100 ditolak per baris; tanyakan maksudnya. Baris rusak lain dilewati dengan alasan di bagian "Perlu dicek".
- Satuan berbeda (gram vs ml vs pcs) tidak disetarakan dan tidak ikut dihitung. Kemasan tanpa isi jelas ("1 pack"), pecahan tak lazim (`1/3 kg`), atau penjumlahan beda satuan (`250 g + 250 ml`) perlu ukuran dari pengguna.
- Harga pesaing hanya potret saat dicek: belum termasuk ongkir, voucher platform, dan harga bisa berubah kapan saja. Data < 5 pesaing diberi peringatan.
- Rekomendasi adalah bahan keputusan, bukan jaminan laku atau untung. Keputusan akhir harga ada di pengguna.

## Riwayat versi
- **1.0.4** (2026-09-29): aturan kerja standar library: tidak menginstal paket, tidak membuka/mencari file di luar yang diberikan, lokasi file baru disebut, hasil di folder kerja yang disepakati (bukan /tmp).
- **1.0.3** (2026-09-29): satuan kemasan/jumlah mengalikan ukuran: `10 sachet 25 gr` = 250 g, `2 karung 1 kg` = 2 kg, `1 lusin 100 gr` = 1.200 g (12 x 100 g), `2 kodi 50 gr` = 2 kg, `100 gr x 2 lusin` = 2.400 g (dengan catatan "cek"); `1 lusin` sendiri = 12 pcs, `1 kodi` = 20 pcs, `1 rim` = 500 lembar. Jumlah butir di dalam (`isi 10 sachet 25 gr`) tidak dikalikan. Uji regresi 44.
- **1.0.2** (2026-09-29): ukuran `500 gr isi 2`, `250gr (isi 2)`, `2 pack 500 gr`, `3 botol 250 ml` dibaca sebagai isi total (1 kg / 500 g / 1 kg / 750 ml) dengan catatan "cek: bila angka itu sudah total, tulis ulang ukurannya"; jumlah butir di dalam (`isi 10 pcs 250 gr`, `250 gr isi 20 sachet`) tidak dikalikan; `isi 2 pack 500 gr` dibaca total 500 g dengan catatan cek. Sampaikan catatan "cek" ke pengguna bila harga setara pesaing itu memengaruhi rekomendasi.
- **1.0.1** (2026-09-28): perbaikan hasil uji independen - ukuran pecahan (`1/2 kg`, `setengah kilo`) dan paket (`250 g x 2`, `isi 2 @250gr`, `250 g + 250 g`, `2 pcs @ 250 gr`) dibaca benar; pesaing jauh dari median dikeluarkan dari statistik (`--pakai-semua` untuk mengikutkan); strategi premium kini P75-P90; mode pasar saja tanpa HPP; CSV ANSI/UTF-16 & kolom bergeser ditangani; harga < Rp 100 ditolak; pilih satuan yang sama bila teks memuat beberapa ukuran; pesan error lebih jelas; bagian "Cara menguji harga baru".
- **1.0.0** (2026-09-28): rilis awal.
