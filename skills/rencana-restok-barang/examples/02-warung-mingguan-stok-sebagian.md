# Contoh 2: warung sembako, total mingguan 8 minggu ditempel di chat, stok sebagian belum dihitung

> Hasil uji penguji independen di OpenClaw 2026.10.2 (model claude-sonnet-5), 14 Okt 2026, **versi 1.0.1** (uji ulang terbatas). Data fiktif. Jawaban SEBELUM (tanpa skill, putaran 1) dan penilaian lengkap ada di `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
> Ini penjualan warung sembako saya per minggu, 8 minggu terakhir (minggu mulai hari Senin):
>
> Minggu | Beras 5 kg (karung) | Minyak Goreng 2 L | Gula Pasir 1 kg | Telur (kg) | Mie Instan (dus)
> 17 Agu | 20 | 30 | 40 | 55 | 6
> 24 Agu | 22 | 32 | 38 | 50 | 5
> 31 Agu | 19 | 35 | 41 | 58 | 7
> 7 Sep | 23 | 33 | 39 | 52 | 6
> 14 Sep | 21 | 38 | 42 | 60 | 8
> 21 Sep | 24 | 40 | 40 | 57 | 6
> 28 Sep | 22 | 42 | 37 | 54 | 7
> 5 Okt | 25 | 45 | 41 | 59 | 9
>
> Stok sekarang: beras 9 karung, minyak 25, gula 30. Telur sama mie belum sempat saya hitung. Grosir langganan antar 2-3 hari. Saya harus belanja apa dan berapa?

Tabel lebar ditempel di chat (kolom = barang, baris = minggu mulai Senin, tanpa tahun).

## Keluaran di chat (SESUDAH, versi 1.0.1)

> **Rencana restok per 14 Okt 2026** (data 17 Agu – 11 Okt 2026, 8 minggu)
>
> Dari pola 8 minggu terakhir: 2 barang perlu dipesan **sekarang**, 1 minggu depan, dan Beras berisiko kosong sebelum kiriman datang. Telur & Mie Instan belum bisa dihitung jumlah pesannya karena stok sekarangnya belum ada datanya.
>
> **⚠️ AKAN KOSONG SEBELUM BARANG DATANG**
> - Beras 5 kg: stok 9 karung, laku ±3,14/hari, perkiraan habis ±2 hari (16 Okt). Grosir antar 2–3 hari → kalau pesan sekarang pun, bisa kosong ±1 hari. Pilihan: pesan hari ini juga, minta kirim cepat/ambil sebagian ke pemasok lain, atau terima kosong ±1 hari (batasi jual per pembeli sementara).
>
> **PESAN SEKARANG**
> - Beras 5 kg: stok 9, laku ±3,14/hari (stabil), habis ±2 hari (16 Okt) → **pesan 47 karung**, nilai [isian: harga beli]
> - Minyak Goreng 2 L: stok 25, laku ±5,89/hari (naik 27% dibanding 4 minggu sebelumnya), habis ±4 hari (18 Okt) → **pesan 82 botol**, nilai [isian: harga beli]
>
> **PESAN MINGGU DEPAN**
> - Gula Pasir 1 kg: stok 30, laku ±5,68/hari (stabil), habis ±5 hari (19 Okt), pesan sekitar 15 Okt → **pesan 75 kg**, nilai [isian: harga beli]
>
> **AMAN**
> - Tidak ada barang yang masih aman untuk saat ini — semua butuh perhatian minggu ini.
>
> **Belum bisa dihitung (stok belum ada datanya)**
> - Mie Instan: laku ±1,07 dus/hari (naik 25%). Pesan kalau stok tinggal ≤5 dus; jumlahnya = 20 − stok sekarang.
> - Telur: laku ±7,95 kg/hari (stabil). Pesan kalau stok tinggal ≤28 kg; jumlahnya = 139 − stok sekarang.
>
> **Daftar pesanan ke grosir langganan (siap kirim)**
> Pesan sekarang: Beras 5 kg 47 karung, Minyak Goreng 2 L 82 botol
> Minggu depan (±15 Okt): Gula Pasir 1 kg 75 kg
>
> Draf WA:
> > Halo [isian: nama pemasok], saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
> > 1. Beras 5 kg: 47 karung
> > 2. Minyak Goreng 2 L: 82 botol
> > Mohon dikonfirmasi ketersediaan, harga, dan perkiraan tanggal kirim. Kalau bisa barang sampai paling lambat 16 Okt. Terima kasih.
>
> **Barang mati**
> - Tidak ada, semua barang masih laku rutin.
>
> **Asumsi yang dipakai**
> - Lead time 3 hari (dari "antar 2–3 hari", saya pakai angka yang lebih aman)
> - Tingkat layanan 95%, stok dijaga cukup 14 hari setelah barang datang
> - Data penjualan dibaca per total mingguan (bukan harian), jadi perkiraan variasi harian agak kasar
> - Satuan: Beras per karung, Minyak per botol 2L, Gula per kg, Telur per kg, Mie per dus
> - Minyak Goreng naik 27% dan Mie Instan naik 25% dalam 4 minggu terakhir dibanding 4 minggu sebelumnya — kalau ini karena promo/musim tertentu, sebaiknya dicek, bukan cuma tren biasa.
>
> **Pertanyaan (maks 3):**
> 1. Berapa stok Mie Instan dan Telur sekarang, biar jumlah pesannya bisa dihitung pasti?
> 2. Berapa harga beli terakhir Beras, Minyak, dan Gula, biar saya hitung nilai Rupiah pesanannya?
> 3. Ada barang yang sudah dipesan ke grosir tapi belum datang (biar tidak dobel hitung)?
>
> Catatan: ini perkiraan dari pola penjualan 8 minggu terakhir, bukan jaminan — cocokkan dulu dengan stok fisik dan kesanggupan grosir sebelum benar-benar memesan.

## Catatan penguji
- Angka 63/63 cocok dengan hitung ulang independen: Beras ROP 12, target 56 → 47 karung (kosong ±1 hari); **Minyak naik 27 %** (5,89 vs 4,64/hari) → ROP 25, target 107 → **82**; Gula ROP 19, target 99, pesan ±15 Okt → 75; Mie naik 25 % → ROP 5/target 20; Telur ROP 28/target 139.
- Perbaikan dari 1.0.0: kenaikan Minyak kini terbaca dan dipakai (1.0.0 menulis "tren tidak naik/turun tajam" dan memesan 71); Beras disorot akan kosong; satuan sesuai barang (karung, botol, kg, dus).
- Barang tanpa stok (Telur, Mie) tetap tidak dikarang jumlahnya.
- Kekurangan kecil: agent menjalankan `find /` untuk mencari lokasi script.
- Nilai: SEBELUM 6,5 → SESUDAH 1.0.1 **9** (versi 1.0.0: 7,5).

## Riwayat
- Versi 1.0.0: angka benar menurut rumus lama, tetapi Minyak (30→45 per minggu) dinilai "stabil" dan asumsi menulis "tren tidak naik/turun tajam"; Minyak dipesan 71. Nilai 7,5.

<details><summary>Keluaran SESUDAH versi 1.0.0</summary>

> **Rencana restok per 14 Okt 2026** (data 17 Agu – 11 Okt 2026, 8 minggu)
>
> Beras dan Minyak Goreng harus dipesan sekarang karena stoknya diperkirakan habis sebelum barang baru datang. Gula Pasir aman untuk beberapa hari lagi, tapi pesan minggu depan. Telur dan Mie Instan belum bisa dihitung karena stok sekarangnya belum saya tahu.
>
> **PESAN SEKARANG**
> | Barang | Stok | Laku/hari | Habis ± | Pesan | Perkiraan nilai |
> |---|---|---|---|---|---|
> | Beras 5 kg (karung) | 9 | 3,14 | 2 hari (16 Okt) | 47 karung | [isian: harga beli] |
> | Minyak Goreng 2 L | 25 | 5,27 | 4 hari (18 Okt) | 71 pcs | [isian: harga beli] |
>
> ⚠️ Beras diperkirakan habis dalam 2 hari, padahal lead time grosir 2-3 hari — ada risiko kosong 1-2 hari sebelum barang tiba. Kalau bisa, hubungi grosir hari ini juga atau minta kirim sebagian dulu.
>
> **PESAN MINGGU DEPAN**
> | Barang | Stok | Laku/hari | Habis ± | Pesan | Tanggal pesan |
> |---|---|---|---|---|---|
> | Gula Pasir 1 kg | 30 | 5,68 | 5 hari (19 Okt) | 75 pcs | ±15 Okt |
>
> **AMAN**
> Tidak ada barang di kelompok ini saat ini (semua yang stoknya diketahui sudah masuk kelompok di atas).
>
> **Daftar pesanan ke grosir (siap kirim)**
>
> Sekarang — Beras 5 kg: 47 karung; Minyak Goreng 2 L: 71 pcs. Total: [isian: harga beli belum ada]
> Minggu depan — Gula Pasir 1 kg: 75 pcs.
>
> Draf WA:
> > Halo [isian: nama pemasok], saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
> > 1. Beras 5 kg: 47 karung
> > 2. Minyak Goreng 2 L: 71 pcs
> > Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Bila bisa, barang tiba paling lambat 16 Okt 2026. Terima kasih.
>
> (Untuk Gula Pasir, kirim susulan sekitar 15 Okt: "Mau tambah pesan Gula Pasir 1 kg: 75 pcs.")
>
> **Barang mati**
> Tidak ada — semua barang masih laku rutin.
>
> **Belum bisa dihitung**
> - Telur: laku ±7,95/kg per hari. Pesan ulang kalau stok tinggal ≤ 28 kg; jumlah pesan = 139 − stok sekarang.
> - Mie Instan: laku ±0,96 dus per hari. Pesan ulang kalau stok tinggal ≤ 5 dus; jumlah pesan = 18 − stok sekarang.
>
> **Asumsi:** lead time dipakai 3 hari (sesuai info grosir 2-3 hari), tingkat layanan 95%, stok harus cukup 14 hari setelah barang datang, tren penjualan tidak naik/turun tajam dalam 8 minggu ini, belum ada faktor musim tambahan.
>
> Pertanyaan saya:
> 1. Stok Telur dan Mie Instan sekarang berapa? (biar jumlah pesannya pasti, bukan rumus)
> 2. Harga beli terakhir Beras, Minyak Goreng, dan Gula Pasir berapa per satuan? (biar nilai belanja total kelihatan)
> 3. Lead time grosirnya pasti 2 atau 3 hari? (saya pakai 3 hari, kalau bisa 2 hari risiko Beras kosong sedikit lebih kecil)
>
> Catatan: ini perkiraan dari pola penjualan 8 minggu terakhir, bukan jaminan — cocokkan dulu dengan stok fisik dan kesanggupan grosir sebelum belanja.
</details>
