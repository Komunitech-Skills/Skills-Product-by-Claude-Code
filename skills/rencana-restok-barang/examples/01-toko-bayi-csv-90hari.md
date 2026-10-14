# Contoh 1: toko perlengkapan bayi online, CSV 90 hari + stok + 2 pemasok

> Hasil uji penguji independen di OpenClaw 2026.10.2 (model claude-sonnet-5), 14 Okt 2026, **versi 1.0.1** (uji ulang terbatas). Data fiktif. Jawaban SEBELUM (tanpa skill, putaran 1) dan penilaian lengkap ada di `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
> Saya jualan perlengkapan bayi online. Ini penjualan 3 bulan terakhir (penjualan-90hari.csv) sama stok sekarang (stok-sekarang.csv). Pemasok saya dua: CV Grosir Bunda barangnya datang 3 hari setelah pesan, PT Ceria Distribusi datang 10 hari dan harus kelipatan dus isi 12. Minggu ini saya harus pesan apa aja dan berapa?

File: `data/penjualan-90hari.csv` (777 baris, tanggal campur `2026-09-01` & `01/09/2026`, sebagian nama huruf kecil) dan `data/stok-sekarang.csv` (12 barang; "Kaos Kaki Bayi (isi 3)" ditulis beda dari data penjualan).

## Keluaran di chat (SESUDAH, versi 1.0.1)

> **Rencana restok per 14 Okt 2026** (data penjualan 16 Jul–13 Okt 2026, 90 hari)
>
> Dari 12 barang: 4 dipesan **sekarang** (±Rp10.879.000), 3 **minggu depan** (±Rp3.351.000), 3 **aman**, 1 **barang mati** (modal nganggur Rp2.775.000), dan 3 barang berisiko **kosong sebelum kiriman tiba**.
>
> **⚠️ AKAN KOSONG SEBELUM BARANG DATANG — urus duluan**
> - **Bedak Bayi 150g**: stok 9, habis ±2 hari, CV Grosir Bunda kirim 3 hari → bisa kosong ±1 hari. Pesan hari ini.
> - **Botol Susu Anti Kolik 250ml**: stok 38, habis ±8 hari, PT Ceria 10 hari → bisa kosong ±2 hari. Pesan hari ini.
> - **Teether Silikon Buah**: stok 24, data penjualannya baru 10 hari (terjual 37 pcs, laju sementara ±3,7/hari) → bisa kosong ±4 hari. Jumlah pesan pasti belum bisa dihitung (data terlalu pendek); minimal pesan 1 dus (12 pcs) sebagai jaga-jaga, atau cek apakah bisa ambil sebagian dari pemasok lain lebih cepat.
>
> **PESAN SEKARANG**
> | Barang | Stok | Laku/hari | Habis ± | Pesan | Nilai |
> |---|---|---|---|---|---|
> | Bedak Bayi 150g | 9 | 3,11 (stabil) | 2 hari (16 Okt) | 49 pcs | Rp539.000 |
> | Popok Celana Bayi M isi 34 | 22 | 5,53 (stabil) | 3 hari (17 Okt) | 79 pcs | Rp4.898.000 |
> | Botol Susu Anti Kolik 250ml | 38 | 4,68 (naik 185%*) | 8 hari (22 Okt) | 96 pcs = 8 dus | Rp4.320.000 |
> | Tisu Basah Bayi 50 lembar | 110 | 9,2 (stabil) | 11 hari (25 Okt) | 132 pcs = 11 dus | Rp1.122.000 |
>
> *Botol Susu: naiknya tajam karena 4 minggu terakhir jauh lebih laku dari sebelumnya (4,68 vs 1,64/hari) — bukan lonjakan satu hari, tapi tren beneran naik. Cek sendiri apakah ini wajar atau ada promo/musim tertentu.
>
> **PESAN MINGGU DEPAN**
> | Barang | Stok | Laku/hari | Habis ± | Pesan | Pesan sekitar tgl |
> |---|---|---|---|---|---|
> | Sabun Cair Bayi 200ml | 70 | 6,89 (naik 51%) | 10 hari (24 Okt) | 94 pcs | 17 Okt |
> | Minyak Telon 60ml | 40 | 4,28 (stabil) | 9 hari (23 Okt) | 57 pcs | 18 Okt |
> | Kaos Kaki Bayi (isi 3) | 60 | 2,93 (naik 82%) | 20 hari (3 Nov) | 48 pcs = 4 dus | 20 Okt |
>
> Catatan Sabun Cair: ada lonjakan 20 Sep (terjual 65, biasanya ±4). Hitungan di atas **termasuk** lonjakan itu — tanpa lonjakan tren-nya stabil dan barang ini sebetulnya **AMAN**, bukan minggu depan. Kalau 20 Sep itu borongan/promo sekali, saya bisa hitung ulang tanpa lonjakan tersebut.
>
> **AMAN**
> - Selimut Bayi Bulu — habis ±20 hari
> - Pelampung Leher Bayi — habis ±48 hari (lagi turun tajam, 4 minggu terakhir cuma 0,61/hari vs sebelumnya 3/hari — cek apakah penurunan ini permanen)
> - Dot Bayi Silikon isi 2 — habis ±139 hari, **stok berlebih 207 pcs (±Rp1.863.000 nganggur)**, jangan ditambah dulu
>
> **Barang mati**
> - Gendongan Hipseat: stok 15, tidak laku 70 hari (terakhir 4 Agu), modal tertahan Rp2.775.000. Saran: bundling dengan barang laris (Tisu Basah/Sabun Cair/Popok), diskon bertahap, atau tanya pemasok soal retur/tukar.
>
> **Daftar pesanan per pemasok (siap kirim)**
>
> *CV Grosir Bunda — total Rp5.437.000 (sekarang)*
> - Bedak Bayi 150g: 49 pcs = Rp539.000
> - Popok Celana Bayi M isi 34: 79 pcs = Rp4.898.000
>
> Draf WA:
> > Halo CV Grosir Bunda, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
> > 1. Bedak Bayi 150g: 49 pcs, harga terakhir Rp11.000/pcs
> > 2. Popok Celana Bayi M isi 34: 79 pcs, harga terakhir Rp62.000/pcs
> > Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Bila bisa, barang tiba paling lambat [isian: tanggal]. Terima kasih.
>
> *PT Ceria Distribusi — total Rp5.442.000 (sekarang)*
> - Botol Susu Anti Kolik 250ml: 96 pcs = Rp4.320.000
> - Tisu Basah Bayi 50 lembar: 132 pcs = Rp1.122.000
>
> Draf WA:
> > Halo PT Ceria Distribusi, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
> > 1. Botol Susu Anti Kolik 250ml: 96 pcs, harga terakhir Rp45.000/pcs
> > 2. Tisu Basah Bayi 50 lembar: 132 pcs, harga terakhir Rp8.500/pcs
> > Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Bila bisa, barang tiba paling lambat [isian: tanggal]. Terima kasih.
>
> *Minggu depan:* CV Grosir Bunda — Sabun Cair 94 pcs + Minyak Telon 57 pcs (±Rp2.631.000); PT Ceria — Kaos Kaki Bayi 48 pcs (±Rp720.000).
>
> **Asumsi yang dipakai:** tingkat layanan 95%, stok harus cukup 14 hari setelah barang datang (selain lead time dari Anda), tidak ada faktor musim tambahan (1x), lead time persis seperti Anda sebutkan (CV Grosir Bunda 3 hari, PT Ceria 10 hari), kelipatan dus 12 hanya diterapkan ke PT Ceria.
>
> **3 hal yang mengubah hasil kalau dijawab:**
> 1. Penjualan Sabun Cair 20 Sep (65 pcs) itu promo/borongan sekali atau memang lagi naik terus?
> 2. Teether Silikon Buah baru mulai dijual 10 hari lalu, atau sudah lama tapi jarang laku?
> 3. Ada barang yang sudah dipesan ke pemasok tapi belum datang? (biar dikurangi dari jumlah pesan ini)
>
> Catatan: ini perkiraan dari pola penjualan sebelumnya, bukan jaminan — cocokkan dengan stok fisik dan konfirmasi ke pemasok sebelum pesan beneran.

## Catatan penguji
- Angka: 180 dari 182 angka/label cocok dengan hitung ulang independen; yang beda hanya Dot Bayi "habis ±139 hari" (seharusnya tepat 140, bug presisi script; barang AMAN, tanpa dampak keputusan). Rincian `05-script-dan-data-rusak.md`.
- Perbaikan dari 1.0.0 yang terlihat: bagian **AKAN KOSONG** paling atas (Bedak ±1 hari, Botol Susu ±2, Teether ±4 dengan saran 1 dus tanpa jumlah karangan); tren per barang (Botol Susu naik 185 % → dipesan 96 pcs, bukan 72); lonjakan Sabun dibandingkan dengan hasil tanpa lonjakan (AMAN) dan ditanyakan "promo/borongan?"; nama Kaos Kaki cocok otomatis. Pesan sekarang naik dari Rp9.799.000 ke **Rp10.879.000** karena Botol Susu kini memakai laju terbaru.
- Konteks Telegram (pesan & data sama): satu baris per barang, angka sama; satu keterangan keliru ("Botol Susu dibatasi maksimal 2×", padahal batas tidak terpakai).
- Kekurangan kecil: untuk Pelampung tidak disebut bahwa habis ±48 hari memakai laju yang dibatasi (1,14 vs nyata 0,61/hari).
- Nilai: SEBELUM 7 (Telegram 6) → SESUDAH 1.0.1 **9** (Telegram **8,5**); versi 1.0.0: 8,5 / 8,5.

## Riwayat
- Versi 1.0.0: semua angka benar, tetapi Teether (habis ±6 hari, pemasok 10 hari) tidak disorot dan Botol Susu dihitung dengan tren yang dibatasi 1,5× (72 pcs). Nilai 8,5 (Telegram 8,5).

<details><summary>Keluaran SESUDAH versi 1.0.0</summary>

> # Rencana Restok Minggu Ini (14 Okt 2026)
>
> Data penjualan dibaca dari 16 Jul – 13 Okt 2026 (90 hari). Dari 12 barang: **4 pesan sekarang** (±Rp9.799.000), **3 pesan minggu depan** (±Rp3.351.000), **3 aman**, **1 barang mati** (modal tertahan Rp2.775.000), dan 1 barang datanya belum cukup.
>
> ## 🔴 PESAN SEKARANG
>
> | Barang | Stok | Laku/hari | Habis ± | Pesan | Nilai |
> |---|---|---|---|---|---|
> | Bedak Bayi 150g | 9 | 3,11 | **2 hari (16 Okt)** | 49 pcs | Rp539.000 |
> | Popok Celana Bayi M isi 34 | 22 | 5,53 | 3 hari (17 Okt) | 79 pcs | Rp4.898.000 |
> | Botol Susu Anti Kolik 250ml | 38 | 3,92 (tren naik 79%) | **9 hari (23 Okt)** | 72 pcs = 6 dus × 12 | Rp3.240.000 |
> | Tisu Basah Bayi 50 lembar | 110 | 9,2 | 11 hari (25 Okt) | 132 pcs = 11 dus × 12 | Rp1.122.000 |
>
> ⚠️ **Bedak Bayi** dan **Botol Susu Anti Kolik** diperkirakan habis *sebelum* barang baru datang (lead time pemasoknya 3 hari dan 10 hari). Pesan hari ini juga.
>
> ## 🟡 PESAN MINGGU DEPAN
>
> | Barang | Stok | Laku/hari | Habis ± | Pesan ±tanggal | Jumlah | Nilai |
> |---|---|---|---|---|---|---|
> | Sabun Cair Bayi 200ml | 70 | 6,89 (tren naik 30%) | 10 hari (24 Okt) | 17 Okt | 94 pcs | Rp1.833.000 |
> | Minyak Telon 60ml | 40 | 4,28 | 9 hari (23 Okt) | 18 Okt | 57 pcs | Rp798.000 |
> | Kaos Kaki Bayi (isi 3) | 60 | 2,93 (tren naik 46%) | 20 hari (3 Nov) | 20 Okt | 48 pcs = 4 dus × 12 | Rp720.000 |
>
> Catatan: Sabun Cair ada lonjakan 1 hari (20 Sep, terjual 65 vs biasanya ±4) — kemungkinan borongan sekali. Dihitung tetap masuk, jadi angka ini agak konservatif ke atas. Beri tahu saya kalau itu memang borongan, bisa dihitung ulang tanpa lonjakan itu.
>
> ## 🟢 AMAN
>
> - **Selimut Bayi Bulu**: stok 8, habis ±20 hari
> - **Pelampung Leher Bayi**: stok 55, habis ±48 hari (tren turun 73%)
> - **Dot Bayi Silikon isi 2**: stok 260, habis ±157 hari — **stok berlebih**, kelebihan 213 pcs (±Rp1.917.000 modal tertahan), jangan ditambah dulu
>
> ## 📦 Daftar pesanan per pemasok (siap kirim)
>
> **CV Grosir Bunda** — pesan sekarang, total Rp5.437.000
> - Bedak Bayi 150g: 49 pcs
> - Popok Celana Bayi M isi 34: 79 pcs
>
> > Halo CV Grosir Bunda, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
> > 1. Bedak Bayi 150g: 49 pcs, harga terakhir Rp11.000/pcs
> > 2. Popok Celana Bayi M isi 34: 79 pcs, harga terakhir Rp62.000/pcs
> > Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Terima kasih.
>
> **PT Ceria Distribusi** — pesan sekarang, total Rp4.362.000
> - Botol Susu Anti Kolik 250ml: 72 pcs (6 dus)
> - Tisu Basah Bayi 50 lembar: 132 pcs (11 dus)
>
> > Halo PT Ceria Distribusi, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
> > 1. Botol Susu Anti Kolik 250ml: 72 pcs (6 dus), harga terakhir Rp45.000/pcs
> > 2. Tisu Basah Bayi 50 lembar: 132 pcs (11 dus), harga terakhir Rp8.500/pcs
> > Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Terima kasih.
>
> *(Untuk minggu depan: CV Grosir Bunda tambahan Sabun Cair + Minyak Telon ±Rp2.631.000; PT Ceria Distribusi tambahan Kaos Kaki ±Rp720.000 — bisa digabung sekalian ke pesanan sekarang kalau mau sekali kirim, karena kelipatan dus PT Ceria sudah terpenuhi masing-masing.)*
>
> ## ⚫ Barang mati
>
> - **Gendongan Hipseat**: stok 15, tidak laku 70 hari (terakhir 4 Agu), modal tertahan Rp2.775.000. Saran: bundling dengan Popok/Tisu (barang terlaris), atau diskon bertahap; cek juga apakah CV Grosir Bunda bisa retur/tukar.
>
> ## ⚪ Belum bisa dihitung
>
> - **Teether Silikon Buah**: baru tercatat sejak 4 Okt (10 hari), data belum cukup untuk hitungan penuh. Laju sementara ±3,7/hari dari stok 24 → perkiraan habis ±6 hari. Kalau ini barang lama yang memang jarang laku (bukan baru), kasih tahu saya biar dihitung dari awal data.
>
> **Asumsi yang dipakai:** tingkat layanan 95%, stok dijaga cukup 14 hari setelah barang tiba, lead time 3 hari (CV Grosir Bunda) dan 10 hari (PT Ceria Distribusi) sesuai info Anda, kelipatan dus 12 untuk PT Ceria Distribusi, nama "Kaos Kaki Bayi isi 3" di data penjualan disamakan dengan "Kaos Kaki Bayi (isi 3)" di data stok (ejaan beda tipis, barangnya sama).
>
> **Pertanyaan (maks 3):**
> 1. Lonjakan Sabun Cair Bayi 20 Sep (65 pcs vs biasanya 4) — itu borongan sekali atau penjualan normal?
> 2. Teether Silikon Buah: barang baru atau lama yang jarang laku?
> 3. Ada barang yang sudah dipesan tapi belum datang (di jalan)? Kalau ada, jumlahnya harus dikurangi dari pesanan di atas.
>
> Catatan: perkiraan dari pola penjualan sebelumnya, bukan jaminan; cocokkan dengan stok fisik dan kesanggupan pemasok sebelum memesan.
</details>
