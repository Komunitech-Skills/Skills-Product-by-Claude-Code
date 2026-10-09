# Uji 03 (normal) - Dimsum frozen 500 g isi 20, HPP + biaya Shopee, strategi murah

> Penguji independen, 2026-09-28. Data pesaing fiktif (teks tempelan).

**Input pengguna:**
> Dimsum ayam frozen saya 500 gr isi 20, modal 28.500. Jual di Shopee: admin 8%, gratis ongkir 4%, PPh 0,5%, biaya proses 1.250. Target untung 25%. Mau pasang harga murah biar cepat laku. Sekarang 45 ribu. Ini 7 pesaing: [teks tempelan termasuk `isi 10 pcs 250 gr`, `250 g x 2`, `isi 20` tanpa berat, `36,5rb` untuk 450 gr, `1kg isi 40`].

## Percobaan 1 (CSV apa adanya)
- `250 g x 2` (Frozenku, Rp 44.000) dibaca **250 g** -> harga setara **Rp 88.000** (seharusnya 500 g -> Rp 44.000). Baris diberi catatan "jauh dari median" tetapi **tetap dihitung**: P75 = Rp 55.000, tertinggi Rp 88.000 (salah).
- `isi 10 pcs 250 gr` dibaca sebagai **10 pcs** (pola pcs ditemukan lebih dulu) -> "satuan beda (pcs vs g)" dan dikeluarkan, padahal beratnya 250 g tersedia.
- `isi 20` tanpa berat -> dikeluarkan (wajar, satu dimensi saja).
Karena strategi murah dan median di bawah minimum, rekomendasi tetap Rp 47.600 (angka ini kebetulan tidak terpengaruh bug), tetapi tabel ringkasan pasar yang dilihat pengguna salah.

## Percobaan 2 (agent memperbaiki penulisan ukuran: `2 x 250 g`, `250 gr (isi 10)`)
```bash
python3 <folder-skill>/scripts/banding_harga.py pesaing-dimsum.csv --nama "Dimsum Ayam Frozen isi 20" --ukuran "500 gr" --hpp 28.500 --harga-kita 45.000 --biaya-persen 8 --biaya-persen 4 --biaya-persen 0,5 --biaya-tetap 1.250 --margin 25 --strategi murah --tanggal 2026-09-28
```

## Riset Harga Pesaing: Dimsum Ayam Frozen isi 20 (500 g)

Tanggal analisis: 2026-09-28 | Pesaing dibandingkan: **6** dari 7 baris (0 duplikat dibuang, 0 baris dilewati)
Dasar banding: harga setara 500 g (ukuran produk kamu)

| # | Toko / Produk | Varian / Ukuran | Harga tayang | Harga coret | Harga setara | Per satuan | Rating | Terjual | Lokasi | Catatan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Dimsum Mama Ika - Dimsum Ayam Frozen isi 20 | 500 gr | Rp 42.000 | Rp 48.000 | Rp 42.000 | Rp 8.400 per 100 g | 4,9 | 2.000 | Jakarta Barat | - |
| 2 | Frozen Mart - Siomay Dimsum Ayam Udang | 250 gr (isi 10) | Rp 24.500 | - | Rp 49.000 | Rp 9.800 per 100 g | 4,7 | 900 | Kota Depok | - |
| 3 | Dapur Bunda Frozen - Dimsum Ayam 1kg isi 40 | 1 kg | Rp 79.900 | Rp 95.000 | Rp 39.950 | Rp 7.990 per 100 g | 4,8 | 1.000 | Kota Tangerang | - |
| 4 | Kedai Dimsum 88 - Dimsum Mentai isi 20 | 500gr | Rp 55.000 | - | Rp 55.000 | Rp 11.000 per 100 g | 5,0 | 300 | Jakarta Utara | - |
| 5 | Frozenku - Dimsum Ayam Premium | 2 x 250 g | Rp 44.000 | - | Rp 44.000 | Rp 8.800 per 100 g | 4,8 | 700 | Bekasi | - |
| 6 | Siomay Pak Kumis - Dimsum Ayam isi 20 | isi 20 | Rp 38.000 | - | - | Rp 1.900 per pcs | 4,6 | 1.500 | Bogor | satuan beda (pcs vs g), tidak ikut dihitung |
| 7 | Chef Frozen - Dimsum Ayam Jamur | 450 gr | Rp 36.500 | - | Rp 40.556 | Rp 8.111 per 100 g | 4,8 | 1.100 | Kota Bandung | - |

### Ringkasan harga pasar

| Terendah | Kuartil bawah (P25) | Median (tengah) | Kuartil atas (P75) | Tertinggi |
|---|---|---|---|---|
| Rp 39.950 | Rp 40.917 | **Rp 43.000** | Rp 47.750 | Rp 55.000 |

- Harga kamu sekarang **Rp 45.000**: lebih murah dari 2 pesaing, sama dengan 0, lebih mahal dari 4 (posisi sekitar persentil 67). Laba Rp 9.625 per barang (margin 21,39%).
- Pesaing paling laris: Dimsum Mama Ika (sekitar 2.000 terjual) di harga setara Rp 42.000.

### Batas harga kamu

| Komponen | Nilai |
|---|---|
| HPP/modal per barang | Rp 28.500 |
| Biaya tetap per barang (mis. biaya proses pesanan) | Rp 1.250 |
| Total biaya marketplace (% dari harga jual) | 12,5% |
| Target margin (laba / harga jual) | 25% |
| Harga balik modal (laba 0) | Rp 34.000 |
| **Harga minimum sesuai target margin** | **Rp 47.600** |

### Rekomendasi harga (strategi murah (bersaing harga))

- **Rentang harga: Rp 47.600 - Rp 47.600**
- Titik rekomendasi: **Rp 47.600** (laba Rp 11.900 per barang, margin 25%)
- PERHATIAN: median pasar Rp 43.000 di bawah harga minimum kamu Rp 47.600. Rekomendasi dinaikkan ke batas minimum; kamu akan tampil lebih mahal dari separuh pesaing.
- PERHATIAN: harga kamu sekarang di bawah harga minimum; margin target tidak tercapai.

### Promo & bundling pesaing

- 2 dari 7 pesaing memasang harga coret (diskon rata-rata 14,2%).
- 2 pesaing mencantumkan promo/gratis ongkir.
- Terlihat bundling/paket/bonus: Kedai Dimsum 88.

### Catatan & asumsi
- Harga pesaing = harga yang tampil saat dicek (setelah diskon toko), belum termasuk ongkir dan voucher platform; bisa berubah kapan saja.
- Harga rentang memakai harga terendah.
- Harga minimum = (HPP + biaya tetap) / (1 - biaya marketplace % - target margin %), dibulatkan ke atas ke rupiah penuh. Nilai lain dibulatkan ke rupiah terdekat.
- Persentil: interpolasi linear (seperti PERCENTILE.INC di Excel).
- Rekomendasi tidak pernah di bawah harga minimum. Ini bahan keputusan, bukan jaminan laku.

💡 Saran (agent, menjelaskan PERHATIAN):
- Dengan modal 28.500 + biaya Shopee 12,5% + 1.250, harga **Rp 45.000 hanya memberi margin 21,39%** (target 25% butuh minimal Rp 47.600). Median pasar Rp 43.000, jadi strategi "murah" tidak bisa dijalankan tanpa mengorbankan target.
- Pilihan tanpa banting harga: tekan modal (beli bahan grosir), jual paket 2 x 500 g (biaya proses 1.250 terbagi dua), atau turunkan target margin secara sadar (mis. 21% di Rp 45.000).
- Kedai Dimsum 88 dijual Rp 55.000 dengan bonus saus dan rating 5,0: ada ruang harga di atas median bila ada pembeda.

## Verifikasi independen
17 nilai per percobaan, **0 selisih**. Minimum = 29.750 / 0,625 = 47.600 (pas, tanpa pembulatan) ✓; laba di 45.000 = 45.000 x 0,875 - 29.750 = 9.625 ✓ (21,39%); setara 36.500/450x500 = 40.555,56 ✓; P25 (data benar) = 40.555,56 + 0,25 x 1.444,44 = 40.916,67 -> 40.917 ✓.

**Penilaian skenario:** lulus setelah koreksi penulisan ukuran; logika PERHATIAN & batas minimum sangat baik. Parser ukuran bundel lemah.
