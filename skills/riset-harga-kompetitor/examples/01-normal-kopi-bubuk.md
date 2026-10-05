# Uji 01 (normal) - Kopi gayo bubuk 250 g vs pesaing 200 g / 500 g / 1/2 kg / 1 kg

> Penguji independen, 2026-09-28. Agent disimulasikan mengikuti SKILL.md. Satu pesaing (Toko Kopi Sidikalang Jaya) adalah **data nyata** hasil web fetch; sisanya teks tempelan fiktif gaya Shopee/Tokopedia.

**Input pengguna:**
> Tolong cek harga kopi gayo bubuk 250 gr. Ini link & teks pesaing yang saya kumpulkan: https://infokopi.com/product/jual-kopi-aceh-gayo/ , https://shopee.co.id/BUBUK-KOPI-ARABIKA-GAYO-250-GRAM-i.450270972.28311393933 , https://azakopigayo.co.id/product/kopi-arabika-gayo-super-premium/ , plus 6 teks produk yang saya tempel di bawah. Modal saya 30 ribu sudah sama kemasan. Jual di Shopee: admin 8%, gratis ongkir xtra 4%, PPh 0,5%, biaya proses 1.250. Sekarang saya jual 58 ribu.

## Langkah 1 - buka link (jalur web, apa adanya)
| Link | Hasil WebFetch penguji | Tindakan sesuai SKILL.md |
|---|---|---|
| infokopi.com (website toko) | **Berhasil**: "Kopi Arabika Aceh Gayo 250gr", Rp 80.000, tanpa harga coret, 0 ulasan | Dicatat, sumber = link |
| shopee.co.id (produk) | **Gagal**: halaman kosong (render JavaScript / perlu login) | Tidak dicoba cara lain; minta pengguna tempel teks |
| azakopigayo.co.id | **Gagal**: HTTP 503 | Tidak dicoba ulang berkali-kali; minta tempel teks |

Pesan agent ke pengguna (sesuai langkah 1): "2 link tidak bisa saya buka (Shopee: halaman kosong, azakopigayo: server error). Tolong tempel teks halaman produknya atau kirim screenshot bagian harga, ukuran, terjual, dan lokasi." Untuk uji ini dianggap pengguna tidak mengirim ulang keduanya; dipakai 6 teks tempelan.

## Langkah 2 - CSV yang ditulis agent (percobaan pertama)
Agent menulis harga apa adanya. Dua kesalahan realistis terjadi: (a) teks tempelan menulis ukuran `1/2 kg`, (b) `1,2RB terjual` ditulis tanpa tanda kutip sehingga kolom bergeser.

Hasil script percobaan pertama (dipersingkat):
- Kedai Seduh `1/2 kg` Rp96.000 dibaca **2.000 g** -> harga setara **Rp 12.000** (seharusnya Rp 48.000). Baris hanya diberi catatan "jauh dari median", **tetap ikut dihitung** (terendah pasar tampil Rp 12.000).
- Gayo Roastery: terjual tampil **1**, lokasi tampil "2RB terjual" (kolom bergeser). Script **tidak memberi peringatan** jumlah kolom tidak cocok.

Agent yang teliti melihat catatan "jauh dari median", mengecek, lalu memperbaiki CSV (`500 gr`, dan nilai berkoma diberi tanda kutip). Kebetulan pada data ini P25/median/P75 tidak berubah (baris itu tetap peringkat terbawah), hanya "Terendah" yang salah. Pada data lain bisa menggeser rekomendasi (lihat HASIL-UJI temuan T1).

## Langkah 3 - Perintah & output script setelah diperbaiki (apa adanya)
```bash
python3 <folder-skill>/scripts/banding_harga.py pesaing.csv --nama "Kopi Arabika Gayo Bubuk" --hpp 30.000 --ukuran "250 gr" --harga-kita 58.000 --biaya-persen 8 --biaya-persen 4 --biaya-persen 0,5 --biaya-tetap 1.250 --margin 20 --tanggal 2026-09-28
```

## Riset Harga Pesaing: Kopi Arabika Gayo Bubuk (250 g)

Tanggal analisis: 2026-09-28 | Pesaing dibandingkan: **7** dari 8 baris (1 duplikat dibuang, 0 baris dilewati)
Dasar banding: harga setara 250 g (ukuran produk kamu)

| # | Toko / Produk | Varian / Ukuran | Harga tayang | Harga coret | Harga setara | Per satuan | Rating | Terjual | Lokasi | Catatan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Toko Kopi Sidikalang Jaya - Kopi Arabika Aceh Gayo 250gr | Medium Grind / 250gr | Rp 80.000 | - | Rp 80.000 | Rp 32.000 per 100 g | - | - | online | - |
| 2 | Gayo Roastery - Kopi Gayo Bubuk Arabika | 200 gr | Rp 42.500 | Rp 55.000 | Rp 53.125 | Rp 21.250 per 100 g | 4,8 | 1.200 | Kab. Aceh Tengah | - |
| 3 | Kopi Pak Darmo - Arabika Gayo Bubuk Halus | 250 gr | Rp 54.900 | - | Rp 54.900 | Rp 21.960 per 100 g | 4,9 | 850 | Kota Medan | rentang Rp 54.900-Rp 62.900, dipakai terendah |
| 4 | Bean Station ID - Arabika Gayo Wine 500gr | 500 gr | Rp 109.500 | Rp 125.000 | Rp 54.750 | Rp 21.900 per 100 g | 4,9 | 500 | Jakarta Selatan | - |
| 5 | Kedai Seduh - Kopi Gayo Bubuk | 500 gr | Rp 96.000 | - | Rp 48.000 | Rp 19.200 per 100 g | 4,7 | 300 | Bandung | - |
| 6 | Aroma Gayo - Kopi Arabika Gayo 1kg | 1 kg | Rp 199.000 | - | Rp 49.750 | Rp 19.900 per 100 g | 5,0 | 1.000 | Takengon | - |
| 7 | Kopi Rakyat - Kopi Gayo Bubuk 250g | 250 g | Rp 49.000 | Rp 59.000 | Rp 49.000 | Rp 19.600 per 100 g | 4,6 | 3.000 | Jakarta Timur | - |

### Ringkasan harga pasar

| Terendah | Kuartil bawah (P25) | Median (tengah) | Kuartil atas (P75) | Tertinggi |
|---|---|---|---|---|
| Rp 48.000 | Rp 49.375 | **Rp 53.125** | Rp 54.825 | Rp 80.000 |

- Harga kamu sekarang **Rp 58.000**: lebih murah dari 1 pesaing, sama dengan 0, lebih mahal dari 6 (posisi sekitar persentil 86). Laba Rp 19.500 per barang (margin 33,62%).
- Pesaing paling laris: Kopi Rakyat (sekitar 3.000 terjual) di harga setara Rp 49.000.

### Batas harga kamu

| Komponen | Nilai |
|---|---|
| HPP/modal per barang | Rp 30.000 |
| Biaya tetap per barang (mis. biaya proses pesanan) | Rp 1.250 |
| Total biaya marketplace (% dari harga jual) | 12,5% |
| Target margin (laba / harga jual) | 20% |
| Harga balik modal (laba 0) | Rp 35.715 |
| **Harga minimum sesuai target margin** | **Rp 46.297** |

### Rekomendasi harga (strategi tengah pasar)

- **Rentang harga: Rp 49.375 - Rp 54.825**
- Titik rekomendasi: **Rp 53.125** (laba Rp 15.234 per barang, margin 28,68%)
- Harga cantik terdekat (masih di dalam rentang): **Rp 52.900** (laba Rp 15.038, margin 28,43%)

### Promo & bundling pesaing

- 3 dari 7 pesaing memasang harga coret (diskon rata-rata 17,36%).
- 3 pesaing mencantumkan promo/gratis ongkir.

### Perlu dicek
- baris 8 (Kopi Rakyat) sama dengan baris 7

### Catatan & asumsi
- Harga pesaing = harga yang tampil saat dicek (setelah diskon toko), belum termasuk ongkir dan voucher platform; bisa berubah kapan saja.
- Harga rentang memakai harga terendah.
- Harga minimum = (HPP + biaya tetap) / (1 - biaya marketplace % - target margin %), dibulatkan ke atas ke rupiah penuh. Nilai lain dibulatkan ke rupiah terdekat.
- Persentil: interpolasi linear (seperti PERCENTILE.INC di Excel).
- Rekomendasi tidak pernah di bawah harga minimum. Ini bahan keputusan, bukan jaminan laku.

💡 Saran:
- Harga kamu Rp 58.000 lebih mahal dari 6 dari 7 pesaing (median Rp 53.125). Turun ke **Rp 52.900** masih memberi laba Rp 15.038 (margin 28,43%), di atas target 20%.
- Pesaing terlaris (Kopi Rakyat, 3rb+ terjual) ada di Rp 49.000 dengan harga coret Rp 59.000 + gratis ongkir. Kalau bertahan di atas median, pakai harga coret yang jujur dan tonjolkan keunggulan (mis. roasting segar, asal kebun).
- Kemasan 500 g dan 1 kg pesaing lebih murah per 100 g (Rp 19.200-21.900): pertimbangkan varian 500 g.

Link yang tidak bisa dibuka: shopee.co.id/BUBUK-KOPI-ARABIKA-GAYO-250-GRAM-... (halaman kosong), azakopigayo.co.id/... (HTTP 503).

## Verifikasi angka independen (Decimal, `verif.py` penguji)
19 nilai (5 statistik, balik modal, minimum, rentang, titik, laba/margin titik, harga cantik + laba/margin, laba/margin harga kita, posisi) -> **0 selisih**. Contoh manual: minimum = 31.250 / 0,675 = 46.296,30 -> ceil **46.297**; balik modal = 31.250 / 0,875 = 35.714,29 -> ceil 35.715; urutan setara 48.000; 49.000; 49.750; 53.125; 54.750; 54.900; 80.000 -> P25 = 49.000 + 0,5 x 750 = **49.375**, median **53.125**, P75 = 54.750 + 0,5 x 150 = **54.825**; laba di 52.900 = 52.900 x 0,875 - 31.250 = 15.037,5 -> Rp 15.038.

**Penilaian skenario:** lulus setelah koreksi input. Nilai jual kuat (fallback link gagal tertangani dengan benar, angka tepat). Dua kelemahan parser/CSV dicatat.
