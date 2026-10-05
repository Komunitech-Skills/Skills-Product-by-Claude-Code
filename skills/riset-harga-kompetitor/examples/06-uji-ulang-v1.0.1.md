# 06 - Uji ulang v1.0.1: sambal botol 150 ml vs 8 pesaing (teks ditempel)

- **Penguji:** agent independen kedua (bukan pembuat, bukan penguji v1.0.0), hanya membaca folder skill. Model: Opus.
- **Tanggal:** 2026-09-28. **Platform:** `claude-code (simulasi agent)`. Skill disalin ke scratchpad, bukan `.claude/skills/`.
- **Jenis:** skenario normal lengkap, agent mengikuti SKILL.md langkah 1-3 (tanpa web: pengguna menempel teks).

## Pesan pengguna
> Mau cek harga sambal bawang botol 150 ml saya. Modal 17.500 per botol sudah sama kemasan. Jual di Shopee (admin 8%, gratis ongkir 4%, PPh 0,5%, biaya proses 1.250). Target untung 25%. Sekarang saya jual 32 ribu. Ini data pesaing yang saya salin dari Shopee/Tokopedia/TikTok:
>
> 1. Dapur Mbok Sri - Sambal Bawang Botol Level 3, 150 ml, Rp27.500 (coret Rp32.000), gratis ongkir, 4,9, 2,3rb terjual, 812 ulasan, Sidoarjo (Shopee)
> 2. Sambal Juara ID - Sambal Bawang Pedas Mantap 150ml, 29,9rb, 4,8, 1rb+ terjual, 402 ulasan, Surabaya (Shopee)
> 3. Rumah Pedas - Sambal Cumi Asin 2 x 150 ml, Rp58.000 (coret Rp66.000), "Beli 2 hemat", 4,9, 640 terjual, Malang (Tokopedia)
> 4. Bu Rudy KW - Sambal Bawang Original 190 gr, Rp35.000, 4,7, 150 terjual, Surabaya (TikTok Shop)
> 5. Pedas Nusantara - Sambal Ijo Botol, varian 150 ml / 250 ml, Rp29.900 - Rp34.900, 4,7, 800 terjual, Jakarta Barat (Shopee)
> 6. Truffle House - Sambal Truffle Premium 150 ml, Rp89.000, 5,0, 25 terjual, Jakarta Selatan (Tokopedia)
> 7. Sambel Mertua - Sambal Teri Medan 1/2 L, Rp96.000, gratis ongkir, 4,8, 300 terjual, Medan (Shopee)
> 8. Kedai Cabe - Sambal Bawang 150 ml, Rp31.000 (coret Rp35.000), 4,6, 500 terjual, Bandung (Shopee)

## Langkah agent
1. Semua info wajib ada (data pesaing, HPP, ukuran, biaya, margin, harga sekarang) -> tidak perlu bertanya dulu.
2. Menyalin ke CSV sesuai `templates/pesaing-template.csv`, harga ditulis apa adanya (`29,9rb`, `1/2 L`, `2 x 150 ml`, rentang), nilai berkoma diberi kutip, `sumber` = `(ditempel pengguna)`, `tanggal_cek` = 2026-09-28.
   - Catatan penguji: untuk baris 5 SKILL.md meminta mencatat harga varian yang sebanding (150 ml). Penguji sengaja menulis rentangnya untuk menguji `--rentang min`: script memakai Rp 29.900 = harga varian 150 ml, jadi hasilnya tetap benar.
3. Menjalankan:
```bash
python3 <folder-skill>/scripts/banding_harga.py pesaing-sambal.csv --nama "Sambal Bawang Botol" \
  --ukuran "150 ml" --hpp 17.500 --harga-kita 32.000 --biaya-persen 8 --biaya-persen 4 \
  --biaya-persen 0,5 --biaya-tetap 1.250 --margin 25
```
4. Menyajikan keluaran script apa adanya + pertanyaan konfirmasi pencilan + saran.

## Output agent ke pengguna (keluaran script tidak diubah)

## Riset Harga Pesaing: Sambal Bawang Botol (150 ml)

Tanggal analisis: 2026-09-28 | Pesaing dibandingkan: **6** dari 8 baris (0 duplikat dibuang, 0 baris dilewati, 1 jauh dari median tidak dihitung)
Dasar banding: harga setara 150 ml (ukuran produk kamu)

| # | Toko / Produk | Varian / Ukuran | Harga tayang | Harga coret | Harga setara | Per satuan | Rating | Terjual | Lokasi | Catatan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Dapur Mbok Sri - Sambal Bawang Botol | Level 3 / 150 ml | Rp 27.500 | Rp 32.000 | Rp 27.500 | Rp 18.333 per 100 ml | 4,9 | 2.300 | Kab. Sidoarjo | - |
| 2 | Sambal Juara ID - Sambal Bawang Pedas Mantap | 150ml | Rp 29.900 | - | Rp 29.900 | Rp 19.933 per 100 ml | 4,8 | 1.000 | Kota Surabaya | - |
| 3 | Rumah Pedas - Sambal Cumi Asin | 2 x 150 ml | Rp 58.000 | Rp 66.000 | Rp 29.000 | Rp 19.333 per 100 ml | 4,9 | 640 | Kota Malang | - |
| 4 | Bu Rudy KW - Sambal Bawang Bu Rudy Style | Original / 190 gr | Rp 35.000 | - | - | Rp 18.421 per 100 g | 4,7 | 150 | Kota Surabaya | satuan beda (g vs ml), tidak ikut dihitung |
| 5 | Pedas Nusantara - Sambal Ijo Botol | 150 ml / 250 ml / 150 ml | Rp 29.900 | - | Rp 29.900 | Rp 19.933 per 100 ml | 4,7 | 800 | Kota Jakarta Barat | rentang Rp 29.900-Rp 34.900, dipakai terendah |
| 6 | Truffle House - Sambal Truffle Premium | 150 ml | Rp 89.000 | - | Rp 89.000 | Rp 59.333 per 100 ml | 5,0 | 25 | Jakarta Selatan | jauh dari median Rp 29.900: TIDAK ikut statistik; cek varian/ukuran/keaslian |
| 7 | Sambel Mertua - Sambal Teri Medan | 1/2 L | Rp 96.000 | - | Rp 28.800 | Rp 19.200 per 100 ml | 4,8 | 300 | Kota Medan | - |
| 8 | Kedai Cabe - Sambal Bawang Kedai Cabe | 150 ml | Rp 31.000 | Rp 35.000 | Rp 31.000 | Rp 20.667 per 100 ml | 4,6 | 500 | Kota Bandung | - |

### Ringkasan harga pasar

| Terendah | Kuartil bawah (P25) | Median (tengah) | Kuartil atas (P75) | Tertinggi |
|---|---|---|---|---|
| Rp 27.500 | Rp 28.850 | **Rp 29.450** | Rp 29.900 | Rp 31.000 |

- Harga kamu sekarang **Rp 32.000**: lebih murah dari 0 pesaing, sama dengan 0, lebih mahal dari 6 (posisi sekitar persentil 100). Laba Rp 9.250 per barang (margin 28,91%).
- Pesaing paling laris: Dapur Mbok Sri (sekitar 2.300 terjual) di harga setara Rp 27.500.

### Batas harga kamu

| Komponen | Nilai |
|---|---|
| HPP/modal per barang | Rp 17.500 |
| Biaya tetap per barang (mis. biaya proses pesanan) | Rp 1.250 |
| Total biaya marketplace (% dari harga jual) | 12,5% |
| Target margin (laba / harga jual) | 25% |
| Harga balik modal (laba 0) | Rp 21.429 |
| **Harga minimum sesuai target margin** | **Rp 30.000** |

### Rekomendasi harga (strategi tengah pasar)

- **Rentang harga: Rp 30.000 - Rp 30.000** (dasar: P25 - P75, titik median pasar)
- Titik rekomendasi: **Rp 30.000** (laba Rp 7.500 per barang, margin 25%)
- PERHATIAN: sebagian besar pesaing (sampai kuartil atas) menjual di bawah harga minimum kamu Rp 30.000. Jangan ikut banting harga; pertimbangkan menekan HPP, bundling, ukuran berbeda, atau menonjolkan keunggulan.

### Promo & bundling pesaing

- 3 dari 8 pesaing di tabel memasang harga coret (diskon rata-rata 12,54%).
- 2 dari 8 pesaing di tabel mencantumkan promo/gratis ongkir.
- Terlihat bundling/paket/bonus: Rumah Pedas.

### Perlu dicek
- 1 pesaing jauh dari median awal Rp 29.900 (di bawah separuh atau di atas dua kali lipat) TIDAK ikut statistik: baris 6 (Truffle House, setara Rp 89.000). Tanyakan ke pengguna apakah harga/ukurannya benar dan sebanding; bila benar, jalankan ulang dengan --pakai-semua.

### Catatan & asumsi
- Harga pesaing = harga yang tampil saat dicek (setelah diskon toko), belum termasuk ongkir dan voucher platform; bisa berubah kapan saja.
- Harga rentang memakai harga terendah.
- Statistik hanya memakai pesaing yang ukurannya bisa disetarakan dan tidak jauh dari median (di bawah separuh / di atas dua kali lipat median dikeluarkan bila ada minimal 3 pesaing).
- Persentil: interpolasi linear (seperti PERCENTILE.INC di Excel).
- Harga minimum = (HPP + biaya tetap) / (1 - biaya marketplace % - target margin %), dibulatkan ke atas ke rupiah penuh. Nilai lain dibulatkan ke rupiah terdekat.
- Rekomendasi tidak pernah di bawah harga minimum. Ini bahan keputusan, bukan jaminan laku.

**Perlu konfirmasi kamu:**
1. Truffle House Rp 89.000 (150 ml) tidak saya ikutkan di hitungan karena jauh di atas harga pasar. Memang produk premium (truffle) yang sebanding dengan sambal kamu? Kalau ya, saya hitung ulang dengan mengikutkannya.
2. Bu Rudy KW memakai gram (190 gr), sambal kamu mililiter, jadi tidak disetarakan. Kalau kamu tahu isi botolnya dalam ml, kirim ke saya.

**Artinya:** harga kamu Rp 32.000 paling mahal dari 6 pesaing sebanding, tetapi batas untung 25% kamu (Rp 30.000) sudah di atas hampir semua pesaing. Jadi turun ke harga pasar (±Rp 29.450) berarti untung di bawah target. Jangan ikut banting harga.

💡 Saran:
- Pesaing terlaris (Dapur Mbok Sri, 2.300 terjual) memakai harga coret + gratis ongkir di Rp 27.500. Kamu bisa ikut pasang harga coret yang jujur dan ikut program gratis ongkir, tanpa menurunkan harga di bawah Rp 30.000.
- Rumah Pedas menjual paket 2 x 150 ml Rp 58.000 (Rp 29.000 per botol). Paket 2 botol di sekitar Rp 60.000-62.000 bisa menurunkan harga per botol tanpa merusak margin, karena biaya proses Rp 1.250 cukup dibayar sekali.
- Alternatif: pertahankan Rp 32.000 dan tonjolkan keunggulan (bahan, level pedas, rating), atau target margin sedikit lebih rendah bila kamu ingin masuk rentang pasar. Uji satu perubahan saja selama 1-2 minggu dan bandingkan total labanya.

Link yang tidak bisa dibuka: tidak ada (data ditempel pengguna).

## Penilaian penguji
| Aspek | Hasil |
|---|---|
| Ukuran `2 x 150 ml`, `1/2 L`, `150ml`, rentang harga, `29,9rb`, `2,3rb` terjual | Benar |
| Pencilan (truffle Rp 89.000) keluar dari statistik tapi tetap tampil + ditanyakan | Benar (T3) |
| Satuan beda (190 gr vs ml) dikeluarkan + alasan | Benar |
| Harga minimum Rp 30.000 = 18.750 / 0,625; balik modal ceil(18.750 / 0,875) = Rp 21.429 | Benar (Decimal independen) |
| P25 28.850, median 29.450, P75 29.900 (n = 6) | Benar (PERCENTILE.INC independen) |
| PERHATIAN pasar di bawah minimum + rekomendasi tidak di bawah minimum | Benar |
| Kosmetik | "Rentang Rp 30.000 - Rp 30.000" dan tidak ada harga cantik saat rentang menyempit ke minimum (wajar, tapi bisa ditulis "Rp 30.000 (batas minimum)") |

Skenario ini: **lulus**.
