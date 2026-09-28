# Contoh pembuat skill: kopi arabika gayo bubuk 250 gr

> Contoh dari pembuat skill (bukan hasil uji independen). Nama toko, link, dan angka **fiktif** untuk ilustrasi.

**Input pengguna:**
> Tolong cek harga kopi gayo bubuk 250 gr punya pesaing, ini 8 link/teks yang saya kumpulkan. Modal saya 32 ribu sudah sama kemasan. Saya jual di Shopee: admin 8%, gratis ongkir 4%, PPh 0,5%, biaya proses 1.250 per pesanan. Target untung 20%. Sekarang saya jual 65 ribu, kemahalan nggak?

**Yang dilakukan agent:**
1. Membuka link publik satu per satu. Dua link Shopee terblokir, jadi agent meminta pengguna menempel teks halaman; pengguna menempel 4 produk.
2. Mencatat semuanya ke `contoh-pesaing-kopi.csv` (harga ditulis apa adanya, termasuk `49.900-59.900` dan `99,9rb`). Satu link Tokopedia ternyata dobel (sekali dengan `www.`, sekali tanpa).
3. Menjalankan:
```bash
python3 <folder-skill>/scripts/banding_harga.py contoh-pesaing-kopi.csv --nama "Kopi Arabika Gayo Bubuk" \
  --hpp 32.000 --ukuran "250 gr" --harga-kita 65.000 --biaya-persen 8 --biaya-persen 4 --biaya-persen 0,5 \
  --biaya-tetap 1.250 --margin 20 --tanggal 2026-09-28
```

## Output script v1.0.1 (apa adanya)

## Riset Harga Pesaing: Kopi Arabika Gayo Bubuk (250 g)

Tanggal analisis: 2026-09-28 | Pesaing dibandingkan: **6** dari 8 baris (1 duplikat dibuang, 0 baris dilewati)
Dasar banding: harga setara 250 g (ukuran produk kamu)

| # | Toko / Produk | Varian / Ukuran | Harga tayang | Harga coret | Harga setara | Per satuan | Rating | Terjual | Lokasi | Catatan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Kopi Nusantara Jaya - Kopi Arabika Gayo Bubuk | Medium roast / 250 gr | Rp 62.000 | Rp 75.000 | Rp 62.000 | Rp 24.800 per 100 g | 4,9 | 1.000 | Kota Medan | - |
| 2 | Roastery Pagi - Arabika Gayo 500gr | 500 gr | Rp 115.000 | - | Rp 57.500 | Rp 23.000 per 100 g | 4,8 | 750 | Kab. Bandung | - |
| 3 | Warung Kopi Kita - Kopi Gayo Bubuk | 250 gr | Rp 49.900 | - | Rp 49.900 | Rp 19.960 per 100 g | 4,7 | 2.300 | Jakarta Barat | rentang Rp 49.900-Rp 59.900, dipakai terendah |
| 4 | Gayo Asli Official - Kopi Arabika Gayo 1kg | 1 kg | Rp 210.000 | Rp 240.000 | Rp 52.500 | Rp 21.000 per 100 g | 5,0 | 120 | Kab. Aceh Tengah | ukuran dibaca dari nama |
| 5 | Kedai Bean - Paket Hemat Kopi Gayo 2x250gr + bonus V60 paper | 2 x 250 gr | Rp 99.900 | - | Rp 49.950 | Rp 19.980 per 100 g | 4,9 | 300 | Surabaya | - |
| 6 | Toko Serba Ada - Kopi Gayo Sachet | isi 10 sachet | Rp 25.000 | - | - | Rp 2.500 per pcs | 4,5 | 5.000 | Tangerang | satuan beda (pcs vs g), tidak ikut dihitung |
| 7 | Kopi Mantap - Kopi Gayo Bubuk | 200 gr | Rp 45.000 | - | Rp 56.250 | Rp 22.500 per 100 g | 4,6 | 90 | Yogyakarta | - |

### Ringkasan harga pasar

| Terendah | Kuartil bawah (P25) | Median (tengah) | Kuartil atas (P75) | Tertinggi |
|---|---|---|---|---|
| Rp 49.900 | Rp 50.588 | **Rp 54.375** | Rp 57.188 | Rp 62.000 |

- Harga kamu sekarang **Rp 65.000**: lebih murah dari 0 pesaing, sama dengan 0, lebih mahal dari 6 (posisi sekitar persentil 100). Laba Rp 23.625 per barang (margin 36,35%).
- Pesaing paling laris: Warung Kopi Kita (sekitar 2.300 terjual) di harga setara Rp 49.900.

### Batas harga kamu

| Komponen | Nilai |
|---|---|
| HPP/modal per barang | Rp 32.000 |
| Biaya tetap per barang (mis. biaya proses pesanan) | Rp 1.250 |
| Total biaya marketplace (% dari harga jual) | 12,5% |
| Target margin (laba / harga jual) | 20% |
| Harga balik modal (laba 0) | Rp 38.000 |
| **Harga minimum sesuai target margin** | **Rp 49.260** |

### Rekomendasi harga (strategi tengah pasar)

- **Rentang harga: Rp 50.588 - Rp 57.188** (dasar: P25 - P75, titik median pasar)
- Titik rekomendasi: **Rp 54.375** (laba Rp 14.328 per barang, margin 26,35%)
- Harga cantik terdekat (masih di dalam rentang): **Rp 53.900** (laba Rp 13.913, margin 25,81%)

### Promo & bundling pesaing

- 2 dari 7 pesaing di tabel memasang harga coret (diskon rata-rata 14,92%).
- 2 dari 7 pesaing di tabel mencantumkan promo/gratis ongkir.
- Terlihat bundling/paket/bonus: Kedai Bean.

### Perlu dicek
- baris 5 (Kopi Nusantara Jaya) sama dengan baris 1

### Catatan & asumsi
- Harga pesaing = harga yang tampil saat dicek (setelah diskon toko), belum termasuk ongkir dan voucher platform; bisa berubah kapan saja.
- Harga rentang memakai harga terendah.
- Statistik hanya memakai pesaing yang ukurannya bisa disetarakan dan tidak jauh dari median (di bawah separuh / di atas dua kali lipat median dikeluarkan bila ada minimal 3 pesaing).
- Persentil: interpolasi linear (seperti PERCENTILE.INC di Excel).
- Harga minimum = (HPP + biaya tetap) / (1 - biaya marketplace % - target margin %), dibulatkan ke atas ke rupiah penuh. Nilai lain dibulatkan ke rupiah terdekat.
- Rekomendasi tidak pernah di bawah harga minimum. Ini bahan keputusan, bukan jaminan laku.

💡 Saran:
- Harga kamu Rp 65.000 paling mahal dari semua pesaing (median Rp 54.375). Turun ke **Rp 53.900** masih memberi margin 25,81%, di atas target 20%.
- Pesaing terlaris (Warung Kopi Kita, 2.300+ terjual) ada di harga terendah Rp 49.900, dan pesaing termahal (Rp 62.000) memakai harga coret + gratis ongkir. Kalau mau bertahan di atas median, pakai harga coret yang jujur dan tonjolkan keunggulan (mis. roasting segar).
- Kedai Bean menjual paket 2 x 250 gr + bonus: pertimbangkan paket hemat 500 gr.

Link yang tidak bisa dibuka: 2 link Shopee (sudah diganti teks tempelan pengguna).

**Cek angka manual (pembuat):** 33.250 / 0,675 = 49.259,26 → Rp 49.260. Harga setara urut: 49.900; 49.950; 52.500; 56.250; 57.500; 62.000 → median (52.500 + 56.250) / 2 = 54.375; P25 = 49.950 + 0,25 × 2.550 = 50.587,5 → Rp 50.588; P75 = 56.250 + 0,75 × 1.250 = 57.187,5 → Rp 57.188. Laba di 53.900 = 53.900 × 0,875 − 33.250 = 13.912,5 → Rp 13.913.
