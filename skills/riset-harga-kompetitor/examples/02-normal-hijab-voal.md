# Uji 02 (normal) - Hijab voal segi empat, 8 pesaing, rentang harga & promo, strategi premium

> Penguji independen, 2026-09-28. Semua data pesaing fiktif (teks tempelan).

**Input pengguna:**
> Saya mau jual hijab voal segi empat laser cut di TikTok Shop, modal 22 ribu. Komisi 6%, biaya layanan 2%. Target untung 25%, mau main premium. Ini 8 pesaing yang saya salin dari Shopee/Tokopedia/TikTok/Lazada: [teks tempelan: termasuk `Rp35.000 - Rp45.000`, `39,9rb`, `45rb–55rb`, harga coret lebih rendah dari harga, `49,9` tanpa rb, satu link Tokopedia dobel (dengan/tanpa www + parameter), paket 2 pcs, data Lazada tanggal 2026-08-10].

## Percobaan 1: agent tidak mengisi ukuran (hijab tak punya berat/isi)
Script jalan (rc 0) tetapi paket **2 pcs Rp89.000 dibandingkan apa adanya** sebagai Rp 89.000. Tidak ada peringatan "ukuran berbeda" karena hanya satu pesaing yang punya ukuran. Akibatnya P75 = **Rp 55.000** dan rekomendasi premium Rp 42.000 - Rp 55.000 (titik 55.000) ikut terdorong baris paket. Baris itu hanya diberi catatan "jauh dari median".

## Percobaan 2 (yang dikirim ke pengguna): agent menyetarakan per pcs
Agent mengikuti langkah 1 ("pastikan varian sebanding"): mengisi `1 pcs` untuk produk satuan dan `--ukuran "1 pcs"`.
```bash
python3 <folder-skill>/scripts/banding_harga.py pesaing-hijab.csv --nama "Hijab Voal Segi Empat Laser Cut" --ukuran "1 pcs" --hpp 22.000 --biaya-persen 6 --biaya-persen 2 --margin 25 --strategi premium --tanggal 2026-09-28
```

## Riset Harga Pesaing: Hijab Voal Segi Empat Laser Cut (1 pcs)

Tanggal analisis: 2026-09-28 | Pesaing dibandingkan: **7** dari 9 baris (1 duplikat dibuang, 1 baris dilewati)
Dasar banding: harga setara 1 pcs (ukuran produk kamu)

| # | Toko / Produk | Varian / Ukuran | Harga tayang | Harga coret | Harga setara | Per satuan | Rating | Terjual | Lokasi | Catatan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Hijabku Official - Hijab Segi Empat Voal Premium Laser Cut | Motif 115x115 / 1 pcs | Rp 35.000 | Rp 60.000 | Rp 35.000 | Rp 35.000 per pcs | 4,9 | 10.000 | Kota Bandung | rentang Rp 35.000-Rp 45.000, dipakai terendah |
| 2 | Zahra Scarf - Voal Ultrafine Segi Empat Polos | Polos / 1 pcs | Rp 39.900 | Rp 59.900 | Rp 39.900 | Rp 39.900 per pcs | 4,8 | 5.200 | Jakarta Timur | - |
| 3 | Nadia Hijab - Hijab Voal Printing Premium | 1 pcs | Rp 45.000 | - | Rp 45.000 | Rp 45.000 per pcs | 4,9 | 3.000 | Surabaya | rentang Rp 45.000-Rp 55.000, dipakai terendah |
| 4 | Aira Moslem - Segiempat Voal Lasercut | 1 pcs | Rp 42.000 | - | Rp 42.000 | Rp 42.000 per pcs | 4,7 | 1.000 | Kota Bekasi | harga coret <= harga, diabaikan |
| 5 | Rumah Jilbab - Paket 2 pcs Hijab Voal | 2 pcs | Rp 89.000 | - | Rp 44.500 | Rp 44.500 per pcs | 4,8 | 450 | Kab. Bogor | - |
| 6 | Hana Collection - Hijab Voal Premium Jahit Tepi | 1 pcs | Rp 65.000 | Rp 79.000 | Rp 65.000 | Rp 65.000 per pcs | 5,0 | 120 | Jakarta Selatan | data lama (2026-08-10) |
| 7 | Laila Store - Voal Segi Empat | 1 pcs | Rp 29.900 | - | Rp 29.900 | Rp 29.900 per pcs | 4,5 | 20.000 | Kota Tangerang | - |

### Ringkasan harga pasar

| Terendah | Kuartil bawah (P25) | Median (tengah) | Kuartil atas (P75) | Tertinggi |
|---|---|---|---|---|
| Rp 29.900 | Rp 37.450 | **Rp 42.000** | Rp 44.750 | Rp 65.000 |

- Pesaing paling laris: Laila Store (sekitar 20.000 terjual) di harga setara Rp 29.900.

### Batas harga kamu

| Komponen | Nilai |
|---|---|
| HPP/modal per barang | Rp 22.000 |
| Biaya tetap per barang (mis. biaya proses pesanan) | Rp 0 |
| Total biaya marketplace (% dari harga jual) | 8% |
| Target margin (laba / harga jual) | 25% |
| Harga balik modal (laba 0) | Rp 23.914 |
| **Harga minimum sesuai target margin** | **Rp 32.836** |

### Rekomendasi harga (strategi premium)

- **Rentang harga: Rp 42.000 - Rp 44.750**
- Titik rekomendasi: **Rp 44.750** (laba Rp 19.170 per barang, margin 42,84%)
- Harga cantik terdekat (masih di dalam rentang): **Rp 43.900** (laba Rp 18.388, margin 41,89%)

### Promo & bundling pesaing

- 3 dari 7 pesaing memasang harga coret (diskon rata-rata 30,93%).
- 1 pesaing mencantumkan promo/gratis ongkir.
- Terlihat bundling/paket/bonus: Hijabku Official, Nadia Hijab, Rumah Jilbab.

### Perlu dicek
- baris 6 (Sofia Kerudung): harga: '49,9' ambigu. Tulis lengkap, mis. 49.900 atau 49,9rb
- baris 5 (Aira Moslem) sama dengan baris 4

### Catatan & asumsi
- Harga pesaing = harga yang tampil saat dicek (setelah diskon toko), belum termasuk ongkir dan voucher platform; bisa berubah kapan saja.
- Harga rentang memakai harga terendah.
- Harga minimum = (HPP + biaya tetap) / (1 - biaya marketplace % - target margin %), dibulatkan ke atas ke rupiah penuh. Nilai lain dibulatkan ke rupiah terdekat.
- Persentil: interpolasi linear (seperti PERCENTILE.INC di Excel).
- Rekomendasi tidak pernah di bawah harga minimum. Ini bahan keputusan, bukan jaminan laku.

💡 Saran:
- 3 dari 7 pesaing memasang harga coret dengan diskon rata-rata ~31%. Kalau memakai harga coret, pakai harga normal yang benar-benar pernah berlaku.
- Pesaing terlaris (Laila Store, 20rb+ terjual) justru termurah Rp 29.900; di posisi premium, tonjolkan pembeda (laser cut rapi, bahan ultrafine, kemasan box).
- Hijabku Official, Nadia Hijab, dan Rumah Jilbab memakai paket/bonus: pertimbangkan "beli 2 lebih hemat" atau bonus inner.
- Zahra/Sofia: satu harga `49,9` tidak jelas (49.900?), tolong pastikan agar bisa ikut dihitung.

## Catatan penguji
- Rentang `Rp35.000 - Rp45.000` dan `45rb–55rb` terbaca benar (dipakai terendah); `39,9rb`/`59,9rb` benar; harga coret 38.000 < harga 42.000 diabaikan dengan catatan; duplikat Tokopedia (www + parameter) terdeteksi; `49,9` ditolak dengan alasan; data 2026-08-10 ditandai "data lama".
- Bundling terdeteksi dari "Beli 3 hemat", "Beli 2 gratis 1", "Paket".
- **Strategi premium** hanya menghasilkan Rp 42.000 - Rp 44.750 dan harga cantik Rp 43.900, **di bawah** harga dua pesaing (Rp 45.000 dan Rp 65.000). "Premium" di skill ini = median..P75, bukan harga atas pasar (lihat HASIL-UJI T4).
- Verifikasi independen: 15 nilai per percobaan, **0 selisih** (keduanya). Minimum = 22.000 / 0,67 = 32.835,82 -> 32.836 ✓.

**Penilaian skenario:** lulus, dengan catatan desain strategi premium dan perlunya panduan "isi 1 pcs" untuk produk tanpa berat/isi.
