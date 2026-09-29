# Contoh 3: Harga butter & telur naik, perlu naik harga?

> Contoh kerja pembuat skill (bukan hasil uji independen). Toko dan angka fiktif. Angka dari `scripts/strategi_harga.py`.

## Input pengguna
"Modal roti sobek saya naik dari 11.500 jadi 13.200 karena butter sama telur naik. Harga masih 28 ribu, laku 600 sebulan, biaya tetap 6,5 juta. Takut pelanggan kabur kalau naik harga. Naik ke 29.900 atau 31.000?"

## Perintah yang dijalankan
```
python3 scripts/strategi_harga.py margin --hpp 13200 --harga 28000
python3 scripts/strategi_harga.py elastisitas --harga 28000 --volume 600 --hpp 13200 --harga-baru 29.900 --harga-baru 31000 --biaya-tetap 6,5jt
python3 scripts/strategi_harga.py cantik --harga 26400 --hpp 13200 --margin-min 50
```

## Output agent

**Ringkasan:** Naikkan ke **Rp29.900** sekarang (naik 6,79%, masih "di bawah 30 ribu"), umumkan seminggu sebelumnya. Rp31.000 lebih untung bila pelanggan tidak terlalu peka, tapi lebih berisiko.

**Kondisi sekarang (HPP baru, harga lama):** laba per pcs Rp14.800 (margin 52,86%), laba bulanan ±Rp2.380.000 (turun dari ±Rp3.400.000).

**Angka PASTI — berapa pcs boleh hilang sebelum laba lebih buruk dari sekarang:**
| Harga baru | Laba/pcs | Penjualan minimal agar laba sama |
|---|---|---|
| Rp29.900 | Rp16.700 | 532 pcs (boleh turun 68 pcs) |
| Rp31.000 | Rp17.800 | 499 pcs (boleh turun 101 pcs) |

**PERKIRAAN (ESTIMASI, bukan kepastian)** — laba bulanan pada tiga tingkat kepekaan pembeli:
| Kepekaan pembeli | Rp29.900 | Rp31.000 |
|---|---|---|
| Tidak peka (−0,5) | ±Rp3.186.000 | ±Rp3.610.400 |
| Sedang (−1) | ±Rp2.835.300 | ±Rp3.040.800 |
| Sangat peka (−2) | ±Rp2.167.300 | ±Rp1.883.800 |

Artinya: kalau pelanggan Ibu cukup setia (roti rumahan langganan), kedua harga lebih untung dari sekarang. Kalau pelanggan sangat peka (banyak roti serupa di dekat situ), Rp31.000 bisa lebih buruk. Rp29.900 lebih aman.

**Harga cantik:** margin minimum 50% dengan HPP baru → lantai Rp26.400. Kandidat Rp26.900 / Rp27.000 / **Rp29.900** semua di atas lantai; Rp29.900 dipilih karena memulihkan sebagian besar laba.

**Rencana kenaikan**
1. Umumkan 7 hari sebelumnya di status WA & grup pelanggan, alasan jujur: harga butter dan telur naik.
2. Selama 7 hari itu, pelanggan boleh pre-order harga lama (maks. 10 pcs per orang).
3. Reseller: beri tahu 2 minggu sebelumnya; harga reseller disesuaikan dengan tangga baru.
4. Pantau 4 minggu: bila penjualan tetap di atas 532 pcs/bulan, laba sudah lebih baik dari sekarang.
5. Jangan diam-diam mengecilkan ukuran roti.

Teks siap tempel:
> Pelanggan setia Roti Bu Ratna 🙏 Karena harga butter & telur naik, mulai Senin 12 Oktober roti sobek menjadi Rp29.900. Sampai Minggu 11 Oktober masih bisa pre-order harga lama Rp28.000 (maks. 10 pcs). Terima kasih sudah terus mendukung usaha kami.

_Angka dihitung dengan script dari data yang Ibu berikan. Simulasi kepekaan pembeli adalah perkiraan. Keputusan harga tetap di tangan Ibu._
