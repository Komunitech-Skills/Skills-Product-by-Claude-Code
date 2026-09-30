# Rumus Penawaran

## Empat tuas nilai
Nilai di mata pembeli naik bila: **hasil yang diinginkan** makin jelas dan besar, **keyakinan berhasil** makin tinggi (bukti, garansi), **waktu sampai hasil** makin cepat, dan **kerepotan/risiko** makin kecil. Harga hanyalah pembanding. Diagnosis cepat: beri tiap tuas nilai 1-10 berdasarkan info pengguna (perkiraan, bukan data); tuas terendah diperbaiki dulu.

| Tuas lemah | Perbaikan yang wajar untuk UMKM |
|---|---|
| Hasil kurang jelas | Sebut hasil konkret ("sarapan pedas siap 2 menit"), bukan sifat produk |
| Kurang yakin | Foto proses, ulasan asli, garansi ganti rusak, sampel kecil |
| Lama | Kirim same-day/next-day, siap saji, panduan pakai 1 langkah |
| Repot/berisiko | Gratis ganti bila rusak, panduan singkat, COD (bila tersedia), konsultasi WA |

## Enam komponen
1. Inti, 2. Bonus, 3. Garansi, 4. Kelangkaan/batas waktu jujur, 5. Nama penawaran, 6. Harga & cara bayar.

## Bonus yang sehat
- Biaya modal kecil, manfaat nyata: kartu resep/panduan, stiker, contoh kecil produk lain, konsultasi 10 menit, prioritas kirim.
- Bonus harus berhubungan dengan inti; bonus acak membuat penawaran tampak murahan.
- Tulis biaya **modal** bonus di script (bukan harga jual). Jangan menulis "senilai Rp..." kecuali bonus itu memang dijual terpisah dengan harga itu.
- Maksimal 3 bonus.

## Jenis garansi
| Jenis | Contoh kalimat | Cocok bila | Hati-hati |
|---|---|---|---|
| Ganti barang | "Rusak/salah kirim? Kami kirim ulang gratis, kirim video buka paket maks. 2 hari" | Barang fisik | Tulis syarat bukti |
| Uang kembali bersyarat | "Belum cocok? Kabari dalam 7 hari, uang kembali dikurangi ongkir" | Harga kecil-menengah | Hitung refund% di script |
| Coba dulu | "Ukuran 100 g Rp15.000 untuk mencoba" | Produk baru | Margin kecil, jaga stok |
| Jaminan layanan | "Telat lebih dari 2 hari dari jadwal, gratis jasa antar" | Jasa | Ukurannya harus jelas |
| Tanpa garansi | "Barang pesanan khusus tidak bisa dikembalikan" | Custom | Wajib ditulis di awal, bukan setelah bayar |
Garansi yang ditulis harus dipenuhi. Garansi berlebihan yang ternyata tidak dipenuhi melanggar aturan dan merusak nama usaha.

## Rumus laba per unit (dipakai script `hitung_penawaran.py`)
```
harga_tayang   = harga x (1 - diskon/100)          -> bulatkan ke rupiah terdekat
biaya_platform = harga_tayang x platform/100       -> bulatkan
biaya_bonus    = jumlah biaya MODAL bonus per unit
biaya_refund   = harga_tayang x refund/100         -> bulatkan (barang kembali tidak dihitung)
laba           = harga_tayang - biaya_platform - HPP - biaya_bonus - biaya_refund
margin         = laba / harga_tayang
ruang_bonus    = (harga_tayang - biaya_platform - HPP - biaya_refund) - harga_tayang x margin_minimal/100
```
Contoh: harga 38.000, HPP 17.000, platform 8% (3.040), bonus 500 + 800, refund 2% (760): laba = 38.000 - 3.040 - 17.000 - 1.300 - 760 = 15.900 (margin 41,8%).
Potongan platform berbeda tiap toko dan waktu; pengguna mengisi dari pusat penjual, tidak ditebak. Pajak (PPh final UMKM dan lainnya) tidak dihitung di sini; gunakan skill pajak.

## Uji kecil 7 hari
Dua versi (A: diskon, B: bonus), masing-masing ke kelompok kecil berbeda; catat balasan, pembeli, dan **laba total** (bukan jumlah balasan). Ulangi 1 kali sebelum menetapkan.
