# Contoh 1: Roti sobek, buka reseller + rencana diskon 20%

> Contoh kerja pembuat skill (bukan hasil uji independen). Toko dan angka fiktif. Angka dari `scripts/strategi_harga.py`.

## Input pengguna
"Saya punya toko roti rumahan 'Roti Bu Ratna' di Bekasi. Roti sobek saya jual 28 ribu, modal per pcs 11.500 (sudah dihitung pakai hitung-hpp). Sewa + gaji 2 karyawan 6,5 juta sebulan, laku sekitar 600 pcs sebulan. Banyak yang minta jadi reseller. Terus bulan depan saya mau promo diskon 20% biar rame. Gimana harganya?"

## Perintah yang dijalankan
```
python3 scripts/strategi_harga.py bep --biaya-tetap 6,5jt --harga 28000 --hpp 11500 --hari-jual 26 --volume 600
python3 scripts/strategi_harga.py tangga --harga-ecer 28000 --hpp 11500 --margin-min 35 --level Eceran:1:0 --level Reseller:10:15 --level Grosir:50:25 --level Agen:200:=18000 --kelipatan 500
python3 scripts/strategi_harga.py diskon --harga 28000 --hpp 11500 --diskon 20 --volume 600 --margin-min 35
python3 scripts/strategi_harga.py diskon --harga 28000 --hpp 11500 --beli-gratis 5:1 --volume 600 --margin-min 35
```

## Output agent

**Ringkasan**
- Harga eceran **Rp28.000 dipertahankan** (berbasis nilai: roti rumahan tanpa pengawet, margin 58,93%).
- Buka tangga reseller: **Rp24.000 (≥10 pcs), Rp21.000 (≥50 pcs), Rp18.000 (≥200 pcs)**, semua di atas margin minimum 35%.
- Diskon 20% untuk semua pembeli **tidak disarankan**; ganti dengan "beli 5 gratis 1" khusus hari tertentu.

**Asumsi:** margin minimum 35% (Ibu tidak menyebut; untuk roti biasanya 40%, kami pakai 35% karena ada level agen). Jual langsung/WA, tanpa potongan marketplace. Bukan PKP, harga tanpa PPN.

**Kondisi sekarang**
| | Angka |
|---|---|
| Laba per pcs | Rp16.500 |
| Titik impas (BEP) | 394 pcs/bulan (±16 pcs per hari, 26 hari jual) |
| Penjualan sekarang | 600 pcs → laba ±Rp3.400.000/bulan |
| Batas aman | penjualan boleh turun 34,33% sebelum rugi |

**Tangga harga reseller**
| Level | Min beli | Harga/pcs | Diskon | Laba/pcs | Margin | Status |
|---|---|---|---|---|---|---|
| Eceran | 1 | Rp28.000 | 0% | Rp16.500 | 58,93% | OK |
| Reseller | 10 | Rp24.000 | 14,29% | Rp12.500 | 52,08% | OK |
| Grosir | 50 | Rp21.000 | 25% | Rp9.500 | 45,24% | OK |
| Agen | 200 | Rp18.000 | 35,71% | Rp6.500 | 36,11% | OK |

Harga terendah yang aman: **Rp17.693** (diskon maksimal 36,81%). Harga agen jangan diturunkan lagi.
Reseller mendapat selisih Rp4.000/pcs bila menjual di harga eceran anjuran Rp28.000.

**Promo diskon 20%**
- Harga promo Rp22.400 → laba per pcs turun dari Rp16.500 ke **Rp10.900**.
- Agar laba kotor sama, penjualan harus naik **51,38%**: dari 600 menjadi **minimal 909 pcs** sebulan. Kapasitas oven dan tenaga cukup?
- Diskon juga dinikmati pelanggan lama yang tetap akan membeli tanpa promo.

**Alternatif lebih aman: beli 5 gratis 1 (khusus Jumat)**
- Diskon efektif 16,67%, laba Rp11.833,33 per pcs; perlu penjualan naik 39,44% hanya pada transaksi promo, dan mendorong pembeli beli 6 sekaligus.

**Aturan promo:** maksimal 1 minggu, hanya hari Jumat, kuota 50 paket, tidak bisa digabung dengan harga reseller. Hentikan bila setelah 2 Jumat jumlah transaksi tidak naik.

**Langkah minggu ini**
1. Umumkan program reseller di status WA dengan daftar harga di bawah.
2. Tetapkan harga eceran anjuran Rp28.000 dan larangan jual di bawahnya.
3. Siapkan kuota 50 paket "Jumat Berkah beli 5 gratis 1".
4. Catat penjualan per hari untuk dibandingkan 2 minggu ke depan.

Teks siap tempel:
> *Daftar Harga Reseller Roti Sobek Bu Ratna* 🍞
> Eceran: Rp28.000/pcs
> Reseller (min 10 pcs): Rp24.000/pcs
> Grosir (min 50 pcs): Rp21.000/pcs
> Agen (min 200 pcs/bulan): Rp18.000/pcs
> Harga jual anjuran ke konsumen Rp28.000. Pesan H-1 sebelum jam 15.00, bayar lunas saat ambil.

_Angka dihitung dengan script dari data yang Ibu berikan. Keputusan harga tetap di tangan Ibu._
