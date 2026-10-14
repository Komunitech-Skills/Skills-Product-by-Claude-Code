# Contoh 5: script dengan data skenario 1 & 2, data rusak, dan verifikasi angka independen (versi 1.0.1)

> Uji penguji independen, 14 Okt 2026, versi 1.0.1 (uji ulang terbatas). Data fiktif di `data/`. Semua perintah dijalankan dari folder skill (Windows: `python` atau `py`). Ringkasan versi 1.0.0 ada di bagian "Riwayat".

## 1. Uji regresi bawaan
`python3 tests/uji_regresi.py` → **139 cek OK, 0 gagal** ("SEMUA LULUS").

## 2. Data skenario 1 apa adanya (seperti dikirim pengguna)
```bash
python3 scripts/rencana_restok.py --file penjualan-90hari.csv --barang stok-sekarang.csv \
  --pemasok pemasok.csv --hari-ini 2026-10-14 --format teks      # pemasok.csv: CV Grosir Bunda;3 / PT Ceria Distribusi;10
```
- Tanggal campur (`2026-09-01` dan `01/09/2026`) dan nama huruf kecil terbaca benar; rentang 16 Jul–13 Okt (90 hari).
- **Nama beda tulis kini cocok otomatis:** "Kaos Kaki Bayi (isi 3)" (stok) = "Kaos Kaki Bayi isi 3" (penjualan); tidak ada lagi barang mati palsu (1.0.0: Rp900.000).
- Nama yang hanya mirip diuji terpisah: stok ditulis "Tisu Basah Bayi 50lembar" → masuk **MUNGKIN BARANG YANG SAMA** ("Belum dianggap barang mati") dan menjadi pertanyaan nomor 1 ("Apakah ini barang yang sama (beda tulis)?").
- Kelipatan dus 12 belum terpakai karena tidak ada kolomnya (disebut pengguna di chat); agent harus menambahkannya, dan memang melakukannya di kedua jalan uji.

## 3. Data skenario 1 + kolom `Kelipatan` (12 untuk PT Ceria), nama asli dibiarkan
```
RENCANA RESTOK per 14 Okt 2026 | data 16 Jul 2026 - 13 Okt 2026 (90 hari, per hari)
Asumsi: tingkat layanan 95% (z 1,65), lead time default 7 hari, stok cukup 14 hari setelah barang datang, faktor musim 1, barang mati = tidak laku >= 60 hari

RINGKASAN: 12 barang | pesan sekarang 4 (Rp10.879.000) | minggu depan 3 (Rp3.351.000) | aman 3 | barang mati 1 (modal tertahan Rp2.775.000) | AKAN KOSONG sebelum barang datang 3

AKAN KOSONG SEBELUM BARANG DATANG (3) - sorot paling atas di balasan
- Teether Silikon Buah: habis ±6 hari, barang datang 10 hari setelah pesan -> kosong ±4 hari (laju sementara (data belum cukup)). Saran: pesan kecil hari ini (paling sedikit 12 pcs sesuai kemasan/minimal order); jumlah pasti belum bisa dihitung; cari pemasok yang lebih cepat atau ambil sebagian di pemasok terdekat; atau terima kosong ±4 hari (batasi jumlah per pembeli, tandai stok menyusul bila aturan platform mengizinkan)
- Botol Susu Anti Kolik 250ml: habis ±8 hari, barang datang 10 hari setelah pesan -> kosong ±2 hari (laju yang dipakai). Saran: pesan hari ini; cari pemasok yang lebih cepat atau ambil sebagian di pemasok terdekat; atau terima kosong ±2 hari (batasi jumlah per pembeli, tandai stok menyusul bila aturan platform mengizinkan)
- Bedak Bayi 150g: habis ±2 hari, barang datang 3 hari setelah pesan -> kosong ±1 hari (laju yang dipakai). Saran: pesan hari ini; cari pemasok yang lebih cepat atau ambil sebagian di pemasok terdekat; atau terima kosong ±1 hari (batasi jumlah per pembeli, tandai stok menyusul bila aturan platform mengizinkan)

PESAN SEKARANG (4)
- Bedak Bayi 150g | stok 9 | laku ±3,11/hari (TREN: stabil (4 minggu terakhir 3,39/hari vs sebelumnya 3,09/hari, beda 10 %, di bawah 20 %); dipakai rata-rata seluruh data 3,11/hari) | habis ±2 hari (16 Okt 2026) | AKAN KOSONG ±1 HARI sebelum barang datang | PESAN 49 pcs | Rp539.000 | pesan ulang bila stok ≤ 15, stok pengaman 5, stok target 58 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok)
- Popok Celana Bayi M isi 34 | stok 22 | laku ±5,53/hari (TREN: stabil (4 minggu terakhir 5,57/hari vs sebelumnya 5,59/hari, beda 0 %, di bawah 20 %); dipakai rata-rata seluruh data 5,53/hari) | habis ±3 hari (17 Okt 2026) | PESAN 79 pcs | Rp4.898.000 | pesan ulang bila stok ≤ 24, stok pengaman 7, stok target 101 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok)
- Botol Susu Anti Kolik 250ml | stok 38 | laku ±4,68/hari (TREN: naik 185 % (4 minggu terakhir 4,68/hari vs sebelumnya 1,64/hari); dipakai 4,68/hari) | habis ±8 hari (22 Okt 2026) | AKAN KOSONG ±2 HARI sebelum barang datang | PESAN 96 pcs = 8 x 12 (dibulatkan ke kelipatan 12) | Rp4.320.000 | pesan ulang bila stok ≤ 65, stok pengaman 18, stok target 130 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok)
- Tisu Basah Bayi 50 lembar | stok 110 | laku ±9,2/hari (TREN: stabil (4 minggu terakhir 9,5/hari vs sebelumnya 9,04/hari, beda 5 %, di bawah 20 %); dipakai rata-rata seluruh data 9,2/hari) | habis ±11 hari (25 Okt 2026) | PESAN 132 pcs = 11 x 12 (dibulatkan ke kelipatan 12) | Rp1.122.000 | pesan ulang bila stok ≤ 109, stok pengaman 17, stok target 238 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok)

PESAN MINGGU DEPAN (3)
- Sabun Cair Bayi 200ml | stok 70 | laku ±6,89/hari (TREN: naik 51 % (4 minggu terakhir 6,89/hari vs sebelumnya 4,57/hari); dipakai 6,89/hari) | habis ±10 hari (24 Okt 2026) | PESAN 94 pcs | Rp1.833.000 | pesan ±17 Okt 2026 | pesan ulang bila stok ≤ 46, stok pengaman 26, stok target 143 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok) | ada lonjakan 20 Sep 2026 (65 pcs, biasanya ±4); hitungan di atas TERMASUK lonjakan (tren naik). Tanpa lonjakan: tren stabil, laku ±4,63/hari, AMAN. Tren naik barang ini terjadi karena lonjakan tersebut
- Minyak Telon 60ml | stok 40 | laku ±4,28/hari (TREN: stabil (4 minggu terakhir 4,39/hari vs sebelumnya 4,3/hari, beda 2 %, di bawah 20 %); dipakai rata-rata seluruh data 4,28/hari) | habis ±9 hari (23 Okt 2026) | PESAN 57 pcs | Rp798.000 | pesan ±18 Okt 2026 | pesan ulang bila stok ≤ 19, stok pengaman 6, stok target 79 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok)
- Kaos Kaki Bayi (isi 3) | stok 60 | laku ±2,93/hari (TREN: naik 82 % (4 minggu terakhir 2,93/hari vs sebelumnya 1,61/hari); dipakai 2,93/hari) | habis ±20 hari (3 Nov 2026) | PESAN 48 pcs = 4 x 12 (dibulatkan ke kelipatan 12) | Rp720.000 | pesan ±20 Okt 2026 | pesan ulang bila stok ≤ 42, stok pengaman 13, stok target 83 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok)

AMAN (3)
- Selimut Bayi Bulu | stok 8 | laku ±0,39/hari (TREN: stabil (4 minggu terakhir 0,43/hari vs sebelumnya 0,38/hari, beda 14 %, di bawah 20 %); dipakai rata-rata seluruh data 0,39/hari) | habis ±20 hari (3 Nov 2026) | pesan ulang bila stok ≤ 4, stok pengaman 2, stok target 9 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok)
- Pelampung Leher Bayi | stok 55 | laku ±1,14/hari (TREN: turun 80 % (4 minggu terakhir 0,61/hari vs sebelumnya 3/hari); dipakai 1,14/hari karena laju dibatasi 0,5× rata-rata seluruh data (2,29/hari), padahal laju 4 minggu terakhir 0,61/hari — cek sendiri apakah perubahan ini akan bertahan) | habis ±48 hari (1 Des 2026) | pesan ulang bila stok ≤ 18, stok pengaman 6, stok target 34 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok)
- Dot Bayi Silikon isi 2 | stok 260 | laku ±1,86/hari (TREN: naik 27 % (4 minggu terakhir 1,86/hari vs sebelumnya 1,46/hari); dipakai 1,86/hari) | habis ±139 hari (2 Mar 2027) | pesan ulang bila stok ≤ 27, stok pengaman 8, stok target 53 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok) | STOK BERLEBIH, kelebihan 207 pcs (Rp1.863.000) | stok cukup untuk ±139 hari: jangan ditambah dulu

DATA BELUM CUKUP (1)
- Teether Silikon Buah | stok 24 | AKAN KOSONG ±4 HARI sebelum barang datang | pemasok PT Ceria Distribusi | barang ini baru tercatat sejak 4 Okt 2026 (10 hari); barang baru atau jarang laku | teramati 37 pcs dalam 10 hari (laju sementara ±3,7/hari); dengan laju itu stok habis ±6 hari; jumlah pesan belum dihitung

BARANG MATI (1)
- Gendongan Hipseat | stok 15 | pemasok CV Grosir Bunda | tidak terjual 70 hari (terakhir 4 Agu 2026) | modal tertahan Rp2.775.000

PESANAN PER PEMASOK
* CV Grosir Bunda - PESAN SEKARANG - total Rp5.437.000
    Bedak Bayi 150g: 49 pcs = Rp539.000
    Popok Celana Bayi M isi 34: 79 pcs = Rp4.898.000
  Draf WA:
    Halo CV Grosir Bunda, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
    1. Bedak Bayi 150g: 49 pcs, harga terakhir Rp11.000/pcs
    2. Popok Celana Bayi M isi 34: 79 pcs, harga terakhir Rp62.000/pcs
    Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Bila bisa, barang tiba paling lambat [isian: tanggal]. Terima kasih.
* PT Ceria Distribusi - PESAN SEKARANG - total Rp5.442.000
    Botol Susu Anti Kolik 250ml: 96 pcs = Rp4.320.000
    Tisu Basah Bayi 50 lembar: 132 pcs = Rp1.122.000
  Draf WA:
    Halo PT Ceria Distribusi, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
    1. Botol Susu Anti Kolik 250ml: 96 pcs, harga terakhir Rp45.000/pcs
    2. Tisu Basah Bayi 50 lembar: 132 pcs, harga terakhir Rp8.500/pcs
    Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Bila bisa, barang tiba paling lambat [isian: tanggal]. Terima kasih.
* CV Grosir Bunda - PESAN MINGGU DEPAN - total Rp2.631.000
    Sabun Cair Bayi 200ml: 94 pcs = Rp1.833.000
    Minyak Telon 60ml: 57 pcs = Rp798.000
* PT Ceria Distribusi - PESAN MINGGU DEPAN - total Rp720.000
    Kaos Kaki Bayi (isi 3): 48 pcs = Rp720.000

Barang paling laris (untuk paket bundling barang mati): Tisu Basah Bayi 50 lembar, Sabun Cair Bayi 200ml, Popok Celana Bayi M isi 34

PERTANYAAN USULAN (maks 3):
  1. Tanggal 20 Sep 2026 Sabun Cair Bayi 200ml terjual 65 (biasanya ±4). Itu promo atau borongan sekali? Dengan lonjakan: PESAN MINGGU DEPAN 94 pcs; tanpa lonjakan: AMAN.
  2. Apakah Teether Silikon Buah barang baru? Bila barang lama yang jarang laku, sebutkan agar dihitung dari awal data.
  3. Ada barang yang sudah dipesan tapi belum datang? Jumlahnya akan dikurangkan dari pesanan.

CATATAN
  - Tren per barang (4 minggu terakhir vs sebelumnya, ambang 20 %): naik: Botol Susu Anti Kolik 250ml (+185 %), Sabun Cair Bayi 200ml (+51 %), Kaos Kaki Bayi (isi 3) (+82 %), Dot Bayi Silikon isi 2 (+27 %); turun: Pelampung Leher Bayi (-80 %); stabil: Bedak Bayi 150g, Popok Celana Bayi M isi 34, Tisu Basah Bayi 50 lembar, Minyak Telon 60ml, Selimut Bayi Bulu
  - Kolom penjualan dipakai: tanggal='Tanggal', nama='Nama Produk', qty='Qty'

Rencana ini perkiraan dari pola penjualan sebelumnya, bukan jaminan. Cocokkan dulu dengan stok fisik, harga, dan kesanggupan pemasok sebelum memesan; promo, musim, dan libur bisa mengubah permintaan.
```

### Hitung ulang independen (aturan 1.0.1)
Skrip Python terpisah (tidak mengimpor script skill; kode di bawah) menghitung dari aturan yang tertulis di SKILL.md/references: deret harian 90 hari (hari tanpa penjualan = 0), rata-rata, simpangan baku sampel; **tren** = laju 28 hari terakhir ÷ laju s.d. 56 hari sebelumnya (ambang ±20 %); **laju dipakai** = laju 28 hari dibatasi 0,5–2× rata-rata (stabil → rata-rata); sd × (laju ÷ rata-rata); SS = 1,65 × sd × √LT; ROP & target dibulatkan ke atas; kelompok; jumlah → kelipatan 12; Rupiah; habis (ke bawah) + tanggal; **akan kosong** = ⌈LT − stok ÷ laju⌉ (barang data pendek memakai laju sementara); **lonjakan** = hari > rata-rata + 3 sd, ≥ 4× median hari laku dan ≥ median + 8, dengan hasil pembanding tanpa lonjakan; nama dinormalisasi.

**Hasil: 182 angka/label dibandingkan, 180 cocok, 2 beda.** Yang beda berasal dari satu bug presisi:

| Barang | Script | Hitung ulang | Sebab |
|---|---|---|---|
| Dot Bayi Silikon isi 2: habis | 139 hari | **140 hari** | laju dipakai = 52 ÷ 28 = 13/7; 260 ÷ 13/7 = 140 persis. Script menghitung laju = rata-rata × (laju baru ÷ rata-rata) dengan Decimal 40 digit → 1,857…858 → 260 ÷ laju = 139,999… → dibulatkan ke bawah 139 |
| Dot Bayi: perkiraan tanggal habis | 2 Mar 2027 | **3 Mar 2027** | ikut baris di atas |

Dampak: barang AMAN/stok berlebih, keputusan tidak berubah; tetapi angka yang tampil di jawaban agent ("habis ±139 hari") meleset 1 hari. Perbaikan: pakai laju baru langsung bila tidak kena batas, atau bulatkan laju (mis. 20 desimal) sebelum membagi/membulatkan ke bawah.

Angka yang dicek cocok, antara lain:
- **Hari habis vs lead time / akan kosong:** Bedak 9 ÷ 3,111 = 2,89 < 3 → ⌈0,11⌉ = **1 hari**; Botol Susu 38 ÷ 4,679 = 8,12 < 10 → ⌈1,88⌉ = **2 hari**; Teether 24 ÷ 3,7 = 6,49 < 10 → ⌈3,51⌉ = **4 hari**; Popok 22 ÷ 5,53 = 3,98 ≥ 3 → tidak kosong (benar tidak tercantum).
- **Faktor tren + batas:** Botol Susu 4,679 ÷ 1,643 = 2,85 (naik 185 %); laju 4,679 = 1,79× rata-rata 2,611 → tidak kena batas 2×. Kaos Kaki 2,929 ÷ 1,607 = 1,82 (naik 82 %). Sabun 6,893 ÷ 4,571 = 1,51 (naik 51 %). Dot 1,857 ÷ 1,464 = 1,27 (naik 27 %). Pelampung 0,607 ÷ 3,000 = 0,20 (turun 80 %) → 0,607 < 0,5 × 2,289 → **dibatasi ke 1,144**. Popok/Tisu/Bedak/Minyak Telon/Selimut stabil (beda 0–14 %).
- **Qty per kelipatan dus & Rupiah:** Botol Susu SS = 1,65 × 1,894 × 1,792 × √10 = 17,7 → 18; ROP = 4,679 × 10 + 17,7 = 64,5 → 65; target = 4,679 × 24 + 17,7 = 130,0 → 130; 130 − 38 = 92 → kelipatan 12 → **96 pcs (8 dus)** × Rp45.000 = **Rp4.320.000**. Tisu 238 − 110 = 128 → **132 (11 dus)** Rp1.122.000; Kaos Kaki minggu depan 41 → **48 (4 dus)** Rp720.000. Total pesan sekarang **Rp10.879.000**, minggu depan **Rp3.351.000**, stok berlebih Dot 207 pcs Rp1.863.000, barang mati Gendongan Rp2.775.000.
- **Lonjakan:** hanya Sabun 20 Sep (65; batas rata-rata + 3 sd = 5,31 + 3 × 6,75 = 25,6; median hari laku 4 → 65 ≥ 16 dan ≥ 12). Tren Sabun naik 51 % hanya karena lonjakan: tanpa lonjakan stabil, 4,63/hari, ROP 21, target 86, habis 15 hari → **AMAN** (cocok dengan `tanpa_lonjakan` dan dengan `--abaikan-lonjakan`, yang menurunkan pesan minggu depan ke Rp1.518.000).
- **Pencocokan nama Kaos Kaki:** stok 60, harga Rp15.000, kelipatan 12 terbawa ke barang penjualan → MINGGU DEPAN 48 pcs (bukan barang mati/stok belum diketahui seperti 1.0.0).

Angka yang dikutip agent di jawaban SESUDAH 1.0.1 (lokal & Telegram) sama dengan output script di atas, termasuk "Dot ±139 hari".

## 4. Data skenario 2 (mingguan, 8 minggu, stok 3 barang)
```bash
python3 scripts/rencana_restok.py --file s2-panjang.csv --barang s2-barang.csv --data-per minggu --lead-time 3 --hari-ini 2026-10-14 --format teks
```
```
RENCANA RESTOK per 14 Okt 2026 | data 17 Agu 2026 - 11 Okt 2026 (56 hari, per minggu)
Asumsi: tingkat layanan 95% (z 1,65), lead time umum dari pengguna 3 hari, stok cukup 14 hari setelah barang datang, faktor musim 1, barang mati = tidak laku >= 60 hari

RINGKASAN: 5 barang | pesan sekarang 2 ([isian: harga beli belum ada]) | minggu depan 1 ([isian: harga beli belum ada]) | aman 0 | barang mati 0 (modal tertahan Rp0) | AKAN KOSONG sebelum barang datang 1

AKAN KOSONG SEBELUM BARANG DATANG (1) - sorot paling atas di balasan
- Beras 5 kg (karung): habis ±2 hari, barang datang 3 hari setelah pesan -> kosong ±1 hari (laju yang dipakai). Saran: pesan hari ini; cari pemasok yang lebih cepat atau ambil sebagian di pemasok terdekat; atau terima kosong ±1 hari (batasi jumlah per pembeli, tandai stok menyusul bila aturan platform mengizinkan)

PESAN SEKARANG (2)
- Beras 5 kg (karung) | stok 9 | laku ±3,14/hari (TREN: stabil (4 minggu terakhir 3,29/hari vs sebelumnya 3/hari, beda 10 %, di bawah 20 %); dipakai rata-rata seluruh data 3,14/hari) | habis ±2 hari (16 Okt 2026) | AKAN KOSONG ±1 HARI sebelum barang datang | PESAN 47 karung | nilai: [isian: harga beli] | pesan ulang bila stok ≤ 12, stok pengaman 3, stok target 56 | pemasok -, lead time 3 hari (lead time umum dari pengguna)
- Minyak Goreng 2 L | stok 25 | laku ±5,89/hari (TREN: naik 27 % (4 minggu terakhir 5,89/hari vs sebelumnya 4,64/hari); dipakai 5,89/hari) | habis ±4 hari (18 Okt 2026) | PESAN 82 pcs | nilai: [isian: harga beli] | pesan ulang bila stok ≤ 25, stok pengaman 7, stok target 107 | pemasok -, lead time 3 hari (lead time umum dari pengguna)

PESAN MINGGU DEPAN (1)
- Gula Pasir 1 kg | stok 30 | laku ±5,68/hari (TREN: stabil (4 minggu terakhir 5,71/hari vs sebelumnya 5,64/hari, beda 1 %, di bawah 20 %); dipakai rata-rata seluruh data 5,68/hari) | habis ±5 hari (19 Okt 2026) | PESAN 75 pcs | nilai: [isian: harga beli] | pesan ±15 Okt 2026 | pesan ulang bila stok ≤ 19, stok pengaman 2, stok target 99 | pemasok -, lead time 3 hari (lead time umum dari pengguna)

STOK BELUM DIKETAHUI (2)
- Mie Instan (dus) | laku ±1,07/hari (TREN: naik 25 % (4 minggu terakhir 1,07/hari vs sebelumnya 0,86/hari); dipakai 1,07/hari) | pesan ulang bila stok ≤ 5, stok pengaman 2, stok target 20 | pemasok -, lead time 3 hari (lead time umum dari pengguna) | pesan bila stok tinggal 5 atau kurang; jumlah pesan = 20 - stok sekarang
- Telur (kg) | laku ±7,95/hari (TREN: stabil (4 minggu terakhir 8,21/hari vs sebelumnya 7,68/hari, beda 7 %, di bawah 20 %); dipakai rata-rata seluruh data 7,95/hari) | pesan ulang bila stok ≤ 28, stok pengaman 4, stok target 139 | pemasok -, lead time 3 hari (lead time umum dari pengguna) | pesan bila stok tinggal 28 atau kurang; jumlah pesan = 139 - stok sekarang

PESANAN PER PEMASOK
* Pemasok belum diisi - PESAN SEKARANG - total [isian: harga beli belum ada]
    Beras 5 kg (karung): 47 karung = [isian: harga beli]
...
```
Hitung ulang independen (μ = total ÷ 56; sd harian = sd laju mingguan × √7; tren = 4 minggu terakhir ÷ 4 minggu sebelumnya; batas 0,5–2×): **63 angka/label, 0 beda.** Minyak (30,32,35,33 | 38,40,42,45): 165 ÷ 28 = 5,893 vs 130 ÷ 28 = 4,643 → naik 27 % → laju 5,893; sd 1,984 × 5,893/5,268 = 2,219; SS = 1,65 × 2,219 × √3 = 6,34 → 7; ROP = 17,68 + 6,34 = 24,0 → 25; target = 5,893 × 17 + 6,34 = 106,5 → 107; 107 − 25 = **82**. `--lead-time 3` kini dilabeli "lead time umum dari pengguna" dan tidak ditanyakan lagi; satuan "(karung)" terbawa. Tabel lebar dengan tanggal tanpa tahun ("17 Agu") masih ditolak script dengan saran format (agent menambahkan tahun sendiri sesuai SKILL.md). Kecil: ringkasan masih "barang mati 0 (modal tertahan Rp0)".

## 5. Data rusak (`data/penjualan-rusak.csv`)
Sama seperti 1.0.0: rc 0, **6 baris dilewati dengan alasan per baris** (tanggal kosong, qty "lima", tanggal "32/13/2026", qty kosong, nama kosong, baris TOTAL); "2 pcs" → 2 dan "1 lusin" → 12 (Tisu 830, Popok 510 → Popok pesan 83, Tisu 132; cocok dengan hitung ulang atas baris sah). Kolom qty/tanggal hilang, semua tanggal kosong, file kosong → kode keluar 2 dengan pesan & saran yang jelas.

## 6. Konsistensi rumus SKILL.md / references / script (1.0.1)
- Tren (28 hari vs s.d. 56 hari sebelumnya; mingguan 4 vs s.d. 8 minggu), batas 0,5–2×, sd ikut rasio, akan kosong ⌈LT − stok ÷ laju⌉ (termasuk barang data pendek), lonjakan (> rata-rata + 3 sd, ≥ 4× & ≥ median + 8, ≥ 5 hari laku), pencocokan nama, kelompok, pembulatan: **sama** di SKILL.md, `references/rumus-dan-istilah.md`, dan kode.
- Ketidaktepatan teks: di SKILL.md "Rumus (persis)" ROP/target/habis masih ditulis dengan "μ" (yang didefinisikan sebagai rata-rata seluruh data), padahal script dan references memakai **laju yang dipakai** (setelah tren). Dengan tren 1.0.1 selisihnya besar (Botol Susu 2,61 vs 4,68/hari); sebaiknya SKILL.md ditulis "laku/hari dipakai".

<details><summary>Kode hitung ulang independen 1.0.1 (dipakai penguji)</summary>

```python
# Hitung ulang independen untuk aturan 1.0.1 (tidak mengimpor script skill)
import csv, math, re, datetime as dt, statistics as st
def parse_date(s):
    s=s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}",s): return dt.date.fromisoformat(s)
    d,m,y=s.split('/'); return dt.date(int(y),int(m),int(d))
def norm(s): return ' '.join(re.sub(r'[^0-9a-z]+',' ',s.lower()).split())
def load(path):
    sales={}
    for r in csv.DictReader(open(path)):
        t=parse_date(r['Tanggal']); n=norm(r['Nama Produk']); q=int(r['Qty'])
        sales.setdefault(n,{}); sales[n][t]=sales[n].get(t,0)+q
    return sales
CEIL=lambda x: math.ceil(x-1e-9)
def core(deret, stok, L, kel, harga, acuan, z=1.65, H=14, weekly=None):
    N=len(deret); mu=sum(deret)/N
    if weekly is None:
        sd=st.stdev(deret)
        last=deret[-28:]; prev=deret[max(0,N-84):N-28]
        mu_b=sum(last)/len(last); mu_s=sum(prev)/len(prev)
    else:
        sd=st.stdev([w/7 for w in weekly])*math.sqrt(7)
        mu_b=sum(weekly[-4:])/28; pw=weekly[max(0,len(weekly)-12):-4]; mu_s=sum(pw)/(7*len(pw))
    f=mu_b/mu_s; tren='naik' if f>=1.2 else 'turun' if f<=0.8 else 'stabil'
    laju=min(max(mu_b,0.5*mu),2*mu) if tren!='stabil' else mu
    dibatasi = tren!='stabil' and abs(laju-mu_b)>1e-12
    sdp=sd*laju/mu
    r=dict(mu=mu,sd=sd,mu_b=mu_b,mu_s=mu_s,f=f,tren=tren,laju=laju,dibatasi=dibatasi)
    ss=z*sdp*math.sqrt(L); SS,ROP,T=CEIL(ss),CEIL(laju*L+ss),CEIL(laju*(L+H)+ss)
    r.update(SS=SS,ROP=ROP,T=T)
    if stok is None: r['kelompok']='STOK_BELUM_DIKETAHUI'; return r
    hx=stok/laju; r['habis']=math.floor(hx); r['tgl_habis']=(acuan+dt.timedelta(days=math.floor(hx))).isoformat()
    if hx<L: r['akan_kosong']=CEIL(L-hx)
    hk=0 if stok<=ROP else math.floor((stok-ROP)/laju)
    if hk<1: r['kelompok']='PESAN_SEKARANG'; kur=T-stok
    elif hk<=7: r['kelompok']='PESAN_MINGGU_DEPAN'; kur=T-(stok-laju*hk); r['tgl_pesan']=(acuan+dt.timedelta(days=hk)).isoformat()
    else:
        r['kelompok']='AMAN'
        if math.floor(hx)>90: r['kelebihan']=stok-T; r['nilai_kelebihan']=round((stok-T)*harga) if harga else None
        return r
    q=CEIL(kur); k=kel or 1; q2=CEIL(q/k)*k
    r.update(qty=q2, dus=(q2//kel if kel else None), nilai=(q2*harga if harga else None))
    return r
def spikes(deret):
    isi=[x for x in deret if x>0]
    if len(isi)<5: return [],None
    med=st.median(isi); bt=st.mean(deret)+3*st.stdev(deret)
    return [i for i,x in enumerate(deret) if x>bt and x>=4*med and x>=med+8], med
```
</details>

## Riwayat: versi 1.0.0
- Regresi 113/113 OK. Data skenario 1 setelah dirapikan: **125 angka, 0 beda**; dengan `--abaikan-lonjakan` 121 angka, 0 beda; skenario 2 cocok semua.
- Temuan yang diperbaiki di 1.0.1: nama "(isi 3)" tidak cocok → barang mati palsu Rp900.000; tren 28 hari ÷ rata-rata seluruh data dibatasi 1,5× (Botol Susu 3,92/hari, Minyak "stabil"); lonjakan di 28 hari terakhir membuat "tren naik" tanpa penjelasan; `--lead-time` pengguna dilabeli "default"; satuan selalu "pcs".
