---
name: strategi-harga-produk
description: Menyusun strategi harga produk/jasa UMKM Indonesia - memilih pendekatan (cost-plus, berbasis nilai, berbasis pesaing, penetrasi/skimming), paket good-better-best, bundling/hampers, harga cantik Rp x9.900, tangga harga reseller/grosir/agen dengan margin minimum, aturan promo & diskon yang menjaga margin, rencana naik harga, plus hitungan pasti (margin vs markup, BEP, volume tambahan saat diskon, cek harga paket, simulasi elastisitas berlabel estimasi, PPN untuk PKP). Gunakan saat pengguna bilang "harga yang pas berapa", "strategi harga", "harga reseller/grosir", "diskon 20% masih untung?", "bikin paket hemat", "mau naik harga", "harga 49.900 atau 50.000", atau pricing strategy, price tiers, discount impact, bundle pricing. Menghitung HPP pakai hitung-hpp; potongan marketplace pakai harga-jual-marketplace; harga pesaing pakai riset-harga-kompetitor.
---

# Strategi Harga Produk

## Tujuan
Membantu pemilik usaha memutuskan **berapa harga yang dipasang, untuk siapa, dan dalam bentuk apa** (satuan, paket, reseller, promo), dengan angka yang dihitung script, bukan dikira. Hasil akhirnya: **rekomendasi harga siap pakai + tabel angka + aturan promo + rencana uji**, dengan batas bawah yang tidak pernah bikin rugi.

## Kapan digunakan
- Menentukan harga produk/menu/jasa baru, atau menilai apakah harga sekarang terlalu murah/mahal.
- Menyusun harga eceran, reseller, grosir, agen, atau harga member.
- Merancang paket (hemat, hampers, good-better-best) dan harga cantik (Rp 49.900, Rp 99.000).
- Mengecek promo sebelum dijalankan: diskon %, potongan Rp, beli 2 gratis 1, flash sale, Harbolnas.
- Merencanakan kenaikan harga (bahan naik, UMR naik) tanpa kehilangan pelanggan.

## Kapan TIDAK digunakan (arahkan ke skill lain)
- Menghitung HPP/modal dari resep atau BOM → **hitung-hpp** (hasil HPP-nya dipakai di sini).
- Rincian potongan Shopee/Tokopedia/TikTok Shop (admin, gratis ongkir, PPh 22 0,5%) → **harga-jual-marketplace**. Di sini cukup satu angka `--biaya-persen` total.
- Mengumpulkan & membandingkan harga toko pesaing → **riset-harga-kompetitor** (median & rentang pasarnya dipakai di sini).
- Detail PPN/faktur → **hitung-ppn** / **buat-invoice**. Kalender promo setahun → **promo-kalender**.
- Harga saham/kripto, tarif jasa profesi yang diatur (notaris, dokter), atau kesepakatan harga antar-pesaing (kartel: melanggar UU 5/1999) → tolak dengan sopan.

## Input
| Data | Wajib? | Jika tidak ada |
|---|---|---|
| Produk/jasa + siapa pembelinya | Ya | Tanyakan |
| HPP/modal per unit | Ya untuk angka | Sarankan **hitung-hpp**; bila ingin cepat, pakai perkiraan pengguna dan tandai "HPP perkiraan" |
| Harga sekarang / rencana harga | Tidak | Hitung dari target margin |
| Target margin atau margin minimum | Tidak | Default: margin minimum **30%** (makanan/minuman **40%**, jasa **50%**), sebutkan asumsinya |
| Kanal jual & potongannya | Tidak | Anggap jual langsung (0%); marketplace → minta angka dari harga-jual-marketplace |
| Harga pesaing (terendah/median/tertinggi) | Tidak | Minta 3–5 harga, atau pakai riset-harga-kompetitor |
| Biaya tetap bulanan & penjualan per bulan | Tidak | Lewati BEP, sebutkan |
| Status PKP | Tidak | Anggap **bukan PKP** (harga tanpa PPN) dan beri pengingat |

Jika data wajib kurang, tanyakan **sekali** dalam satu pesan (maks. 5 pertanyaan singkat). Jika pengguna ingin cepat, pakai default di atas dan tulis asumsinya di bagian atas jawaban.

## Langkah kerja

### 1. Pahami tujuan harga
Tanyakan/tentukan satu tujuan utama: **masuk pasar** (cari pelanggan dulu), **untung maksimal**, **tahan harga pesaing**, **naik harga**, atau **habiskan stok**. Tujuan menentukan strategi.

### 2. Tetapkan lantai, pagar, dan atap
- **Lantai (tidak boleh ditembus):** harga minimum dari HPP + potongan + margin minimum → `margin --margin <min>`.
- **Pagar (pasar):** harga pesaing terendah–median–tertinggi, untuk produk yang **setara**.
- **Atap (nilai):** berapa yang rela dibayar pembeli karena manfaat/alternatifnya (hemat waktu, rasa, gengsi, garansi, antar cepat). Harga bagus = di antara pagar dan atap, **tidak pernah** di bawah lantai.
- Bila lantai > atap: jangan turunkan harga; sarankan tekan HPP, ubah ukuran/isi, atau ganti segmen.

### 3. Pilih strategi (lihat `references/pilihan-strategi.md`)
| Situasi | Strategi utama |
|---|---|
| Produk sejenis banyak, pembeli membandingkan harga | Berbasis pesaing (di sekitar median) + beda kecil yang terlihat |
| Punya keunggulan jelas (resep khas, custom, garansi, cepat) | **Berbasis nilai**: di atas median, tonjolkan alasannya |
| Pesanan custom/proyek/jasa | Cost-plus (HPP + margin) sebagai lantai, lalu naik sesuai nilai |
| Produk baru, ingin cepat dikenal | Penetrasi **terbatas waktu/kuota** (harga perkenalan), bukan harga murah permanen |
| Produk unik/langka, pembeli awal fanatik | Skimming: mulai tinggi, turun bertahap / buat varian lebih murah |
| Pembeli beragam daya beli | Good-better-best (3 pilihan) |
| Ingin naikkan nilai transaksi | Bundling/paket hemat/hampers |
| Punya jaringan penjual | Tangga harga reseller/grosir/agen |

Gabungan wajar (mis. berbasis nilai + 3 pilihan + tangga reseller). Jangan menyarankan harga di bawah lantai demi "perang harga".

### 4. Hitung dengan script (wajib untuk semua angka uang)
```
python3 <folder-skill-ini>/scripts/strategi_harga.py <perintah> [opsi]
```
Windows: ganti `python3` dengan `py` atau `python`. Semua uang pakai Decimal; angka boleh ditulis `28.000`, `28rb`, `1,2jt`. Persen ditulis angka biasa (`15` = 15%).

| Kebutuhan | Perintah |
|---|---|
| Margin vs markup, harga dari target | `margin --hpp 11500 --harga 28000` / `--margin 40` / `--markup 100` [`--biaya-persen 12`] |
| Titik impas & target laba | `bep --biaya-tetap 6,5jt --harga 28000 --hpp 11500 [--target-laba 3jt --hari-jual 26 --volume 600]` |
| Tangga reseller/grosir | `tangga --harga-ecer 28000 --hpp 11500 --margin-min 35 --level Eceran:1:0 --level Reseller:10:15 --level Agen:200:=17000 [--kelipatan 500]` |
| Dampak promo | `diskon --harga 28000 --hpp 11500 --diskon 20` / `--potongan 5000` / `--beli-gratis 2:1` `[--volume 600 --margin-min 35]` |
| Cek harga paket | `bundel --item "Roti Sobek:28000:11500" --item "Bolu:45000:19000[:jumlah]" --harga-bundel 65000 [--biaya-tambahan 6000 --margin-min 40]` |
| Simulasi naik/turun harga | `elastisitas --harga 28000 --volume 600 --hpp 11500 --ubah 10 --ubah -10` atau `--harga-baru 29.900` `[--elastisitas -1,5 --biaya-tetap 6,5jt]` |
| Harga cantik | `cantik --harga 52300 [--hpp 30000 --margin-min 40 --harga-min 50000]` |
| Harga + PPN (PKP) | `ppn --harga 49900 --mode termasuk --status-pkp pkp` |

Aturan penting:
- **HPP** di `bep`, `diskon`, `elastisitas` = biaya yang ikut bertambah per unit (bahan, kemasan, upah borongan). Sewa/gaji tetap masuk `--biaya-tetap`.
- `--biaya-persen` = total potongan persen dari harga jual (admin marketplace, komisi, MDR QRIS). Dapatkan dari **harga-jual-marketplace**.
- **Margin ≠ markup.** Margin = laba ÷ harga jual; markup = laba ÷ HPP. Selalu sebutkan keduanya bila pengguna memakai kata "untung 50%" (tanyakan maksudnya bila ragu).
- Bila script tidak bisa dijalankan: hitung manual dengan rumus di `references/rumus.md`, tampilkan rumusnya, dan tulis "dihitung manual".
- Hasil `elastisitas` adalah **ESTIMASI**: selalu tulis kata "perkiraan" dan sarankan uji kecil. Yang pasti hanya "volume impas".

### 5. Susun aturan promo yang menjaga margin (lihat `references/aturan-promo.md`)
Untuk setiap promo yang diusulkan, tulis: batas diskon maksimal (dari script), volume tambahan yang dibutuhkan, durasi/kuota, siapa yang dapat, dan kapan dihentikan. Tandai **TIDAK DISARANKAN** bila promo rugi per unit atau butuh kenaikan penjualan > 100%.

### 6. Harga cantik & tampilan
Pilih akhiran sesuai citra (lihat `references/psikologi-dan-paket.md`): x.900 / x9.900 untuk kesan hemat, angka bulat untuk kesan premium/jasa. Kandidat di bawah lantai tidak boleh dipilih. Untuk PKP: margin dihitung dari harga **sebelum** PPN; bila ingin harga tayang cantik termasuk PPN, pakai `ppn --mode termasuk`.

### 7. Rencana uji & naik harga
Beri 1–2 uji kecil yang bisa dilakukan tanpa alat khusus (mis. 2 minggu harga baru untuk pelanggan baru saja, tawarkan 2 pilihan paket di WA dan catat mana yang dipilih, pre-order dengan harga baru). Untuk kenaikan harga: umumkan 1–2 minggu sebelumnya dengan alasan jujur, beri kesempatan beli harga lama terbatas, naikkan bertahap (≤ 10% per langkah bila pelanggan sensitif).

## Format output
Selalu dengan urutan ini, bahasa sederhana:
1. **Ringkasan 3 baris:** harga yang disarankan, strategi, alasan utama.
2. **Asumsi** (HPP perkiraan? margin minimum default? potongan 0%? non-PKP?).
3. **Tabel harga** (per pilihan/level/paket): harga, laba per unit, margin, status OK/di bawah minimum.
4. **Aturan promo** (bila relevan): batas diskon, volume tambahan yang dibutuhkan, durasi.
5. **Simulasi** (bila diminta) berlabel **ESTIMASI**.
6. **Langkah minggu ini** (maks. 5 butir) + teks siap tempel bila perlu (pengumuman harga, daftar harga reseller untuk WA).
7. Catatan: "Angka dihitung dengan script dari data yang Anda berikan. Keputusan harga tetap di tangan Anda." + catatan PPN bila relevan.

## Contoh
**Input:** "Toko roti saya jual roti sobek 28 ribu, modal 11.500. Mau buka reseller dan bikin promo 20% bulan depan. Sewa+gaji 6,5 juta sebulan, laku ±600 per bulan."

**Output (ringkas):**
- Ringkasan: Harga eceran Rp28.000 dipertahankan (berbasis nilai, margin 58,93%). Reseller Rp24.000 (≥10 pcs), grosir Rp21.000 (≥50 pcs). Diskon 20% **tidak disarankan** sebagai promo umum.
- BEP 394 pcs/bulan (16 pcs/hari kerja); sekarang 600 pcs → laba ±Rp3.400.000, batas aman 34,33%.
- Diskon 20% → harga Rp22.400, laba per pcs turun dari Rp16.500 ke Rp10.900; agar laba kotor sama, penjualan harus naik 51,38% (600 → minimal 909 pcs). Alternatif: beli 5 gratis 1 khusus hari Jumat, atau paket hemat.
- Tangga: level agen Rp17.000 di bawah margin minimum 35% (batas aman Rp17.693) → naikkan ke Rp18.000 atau minimal beli lebih besar.

Contoh lengkap: `examples/`.

## Batasan & penanganan error
- Script keluar dengan `GAGAL: ...` (kode 2) untuk input yang tidak terbaca atau mustahil (HPP ≥ harga, target margin + potongan ≥ 100%, format level/item salah). Jelaskan ke pengguna dengan bahasa awam dan minta angka yang benar; **jangan menebak**.
- Elastisitas pasar tidak diketahui pasti; jangan menyajikan hasil simulasi sebagai kepastian.
- Tidak memberi nasihat pajak rinci. PPN: hanya PKP yang boleh memungut; tarif 12% × DPP nilai lain 11/12 (efektif 11%) untuk non-mewah, dasar PMK 131/2024 (berlaku 1 Jan 2025). Pembulatan PPN: dari DPP persis, dibulatkan ke bawah sekali; **belum dicocokkan dengan Coretax** — bila berbeda, ikuti Coretax. Cek aturan terbaru di pajak.go.id atau konsultan pajak.
- Jangan menyarankan harga coret palsu (harga "sebelum diskon" yang tidak pernah berlaku) atau klaim "termurah" tanpa bukti: menyesatkan konsumen (UU 8/1999 Perlindungan Konsumen).
- Jangan menyarankan kesepakatan harga dengan pesaing (UU 5/1999).
- Nama marketplace hanya penyebut kanal; skill ini tidak berafiliasi dengan marketplace mana pun.
