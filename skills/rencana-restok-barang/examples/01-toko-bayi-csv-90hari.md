# Contoh 1: toko perlengkapan bayi online, CSV 90 hari + stok + 2 pemasok

> Hasil uji penguji independen di OpenClaw 2026.10.2 (model claude-sonnet-5), 14 Okt 2026. Data fiktif. Jawaban SEBELUM (tanpa skill) dan penilaian lengkap ada di `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
> Saya jualan perlengkapan bayi online. Ini penjualan 3 bulan terakhir (penjualan-90hari.csv) sama stok sekarang (stok-sekarang.csv). Pemasok saya dua: CV Grosir Bunda barangnya datang 3 hari setelah pesan, PT Ceria Distribusi datang 10 hari dan harus kelipatan dus isi 12. Minggu ini saya harus pesan apa aja dan berapa?

File: `data/penjualan-90hari.csv` (777 baris, tanggal campur `2026-09-01` & `01/09/2026`, sebagian nama huruf kecil) dan `data/stok-sekarang.csv` (12 barang; "Kaos Kaki Bayi (isi 3)" ditulis beda dari data penjualan).

## Keluaran di chat (SESUDAH, skill aktif)

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

## Catatan penguji
- Semua angka cocok dengan hitungan ulang independen (lihat `05-script-dan-data-rusak.md`).
- Yang sudah benar: nama barang yang beda tulis disamakan dan disebut di asumsi; kelipatan dus 12 hanya untuk PT Ceria; lonjakan Sabun 20 Sep ditanyakan, tidak dibuang; barang mati & stok berlebih dirupiahkan; dua draf WA siap kirim.
- Konteks Telegram (pesan & data sama): format otomatis berganti ke satu baris per barang, angka identik (lihat `00-openclaw-sebelum-sesudah.md`).
- Kekurangan: Teether (habis ±6 hari, pemasok 10 hari) tidak disorot akan kosong sebelum barang datang; Botol Susu dihitung dengan tren yang dibatasi 1,5× (3,92/hari, padahal 28 hari terakhir 4,68/hari).
- Nilai: SEBELUM 7 (Telegram 6) → SESUDAH 8,5 (Telegram 8,5).
