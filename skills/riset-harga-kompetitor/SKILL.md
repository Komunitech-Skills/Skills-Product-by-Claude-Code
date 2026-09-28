---
name: riset-harga-kompetitor
description: Riset harga pesaing untuk penjual UMKM - membuka link produk pesaing yang publik (atau membaca teks/screenshot yang ditempel), merapikan harga, harga coret, promo, rating, terjual, lokasi, menyetarakan ukuran (per gram/ml/pcs), lalu menghitung tabel pembanding (terendah, median, tertinggi), posisi harga kita, harga minimum dari HPP + biaya marketplace + target margin, dan rentang harga jual yang disarankan. Gunakan saat pengguna bilang "cek harga kompetitor", "bandingkan harga toko sebelah", "harga pasaran produk ini berapa", "harga saya kemahalan?", atau competitor price research, price benchmarking, market price comparison. Bukan untuk bot ubah harga otomatis, scraping yang perlu login, atau memantau harga terjadwal.
---

# Riset Harga Kompetitor

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
| HPP/modal per barang (termasuk kemasan) | Ya | Tanyakan; tawarkan skill `hitung-hpp` |
| Ukuran/isi produk sendiri (mis. 250 gr, 1 L, isi 12) | Ya bila ukuran pesaing berbeda-beda | Tanyakan |
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
- Pastikan varian yang dicatat **sebanding** dengan produk pengguna (ukuran/tipe sama atau bisa disetarakan). Jika ragu, tanyakan.

### 2. Hitung dengan script
Simpan tabel sebagai CSV di folder kerja pengguna, lalu jalankan (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
```bash
python3 <folder-skill-ini>/scripts/banding_harga.py pesaing.csv --nama "Kopi Gayo Bubuk" \
  --hpp 32.000 --ukuran "250 gr" --harga-kita 65.000 \
  --biaya-persen 8 --biaya-persen 4 --biaya-persen 0,5 --biaya-tetap 1.250 --margin 20
```
Opsi: `--strategi murah|tengah|premium`, `--rentang min|tengah|maks` (harga mana yang dipakai untuk "49.900-59.900", default terendah), `--tanggal YYYY-MM-DD`, `--format json`. Data produk sendiri juga bisa ditaruh di file JSON: `{"produk_kita": {"hpp": ..., "ukuran": ..., "biaya_persen": [8, 4, 0.5]}, "pesaing": [...]}`.

Script otomatis: membaca format harga Indonesia, membuang duplikat (link sama atau isi sama), melewati baris rusak dengan alasan, menyetarakan ukuran ke ukuran produk pengguna, menandai data > 30 hari dan harga yang jauh dari median, menghitung statistik & rekomendasi.

### 3. Sajikan hasil
- Tampilkan keluaran script **apa adanya** (tabel, ringkasan pasar, batas harga, rekomendasi, promo, "Perlu dicek", catatan & asumsi). Jangan mengubah angka.
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
                    premium = [median .. P75],  titik P75
                    setiap angka dinaikkan ke harga minimum bila lebih rendah
harga cantik      = harga berakhiran 900 di dalam rentang yang paling dekat ke titik
```
Nominal lain dibulatkan ke rupiah terdekat. Contoh: HPP 32.000, biaya tetap 1.250, biaya 12,5%, margin 20% → minimum = 33.250 / 0,675 = 49.259,26 → **Rp 49.260**.

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

## Checklist sebelum mengirim
- [ ] Tidak ada halaman yang dibuka lewat login/bypass; link gagal sudah dilaporkan & diminta teks/screenshot.
- [ ] Varian pesaing sebanding; ukuran produk sendiri disebut bila ukuran pesaing berbeda.
- [ ] HPP dari pengguna (bukan karangan); persen biaya marketplace dari pengguna atau asumsi 0% disebut.
- [ ] Angka dari script, tidak diubah; asumsi & tanggal cek tampil.
- [ ] Rekomendasi tidak di bawah harga minimum; tanda PERHATIAN dijelaskan.
- [ ] Format Rupiah `Rp 49.900`.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila: HPP kosong/0, biaya% + margin ≥ 100%, ukuran produk sendiri tidak dikenali, file tidak ada/kosong/JSON rusak, atau tidak ada satu pun harga pesaing yang terpakai. Jelaskan ke pengguna dan minta data yang benar.
- Harga ambigu seperti `49,9` (tanpa "rb") ditolak per baris; tanyakan maksudnya. Baris rusak lain dilewati dengan alasan di bagian "Perlu dicek".
- Satuan berbeda (gram vs ml vs pcs) tidak disetarakan dan tidak ikut dihitung. Kemasan tanpa isi jelas ("1 pack") perlu ukuran dari pengguna.
- Harga pesaing hanya potret saat dicek: belum termasuk ongkir, voucher platform, dan harga bisa berubah kapan saja. Data < 5 pesaing diberi peringatan.
- Rekomendasi adalah bahan keputusan, bukan jaminan laku atau untung. Keputusan akhir harga ada di pengguna.
