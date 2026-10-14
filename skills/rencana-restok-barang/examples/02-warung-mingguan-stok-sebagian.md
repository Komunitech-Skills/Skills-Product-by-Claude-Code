# Contoh 2: warung sembako, total mingguan 8 minggu ditempel di chat, stok sebagian belum dihitung

> Hasil uji penguji independen di OpenClaw 2026.10.2 (model claude-sonnet-5), 14 Okt 2026. Data fiktif. Jawaban SEBELUM (tanpa skill) dan penilaian lengkap ada di `00-openclaw-sebelum-sesudah.md`.

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

## Keluaran di chat (SESUDAH, skill aktif)

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

## Catatan penguji
- Angka cocok dengan hitungan independen: Beras ROP 12, target 56 → 47 karung; Minyak ROP 22, target 96 → 71; Gula ROP 19, target 99, pesan ±15 Okt → 75; Telur ROP 28/target 139; Mie ROP 5/target 18.
- Barang tanpa stok (Telur, Mie) tidak dikarang jumlahnya; diberi aturan "pesan bila stok ≤ …; jumlah = … − stok".
- **Kekurangan penting:** asumsi menulis "tren tidak naik/turun tajam", padahal Minyak naik terus 30→45 per minggu. Aturan tren skill (4 minggu terakhir ÷ rata-rata 8 minggu = 1,12) menilai itu "stabil", sehingga Minyak dipesan dengan laju 5,27/hari padahal minggu terakhir 6,43/hari. Model tanpa skill justru menangkap kenaikan ini.
- Nilai: SEBELUM 6,5 → SESUDAH 7,5.
