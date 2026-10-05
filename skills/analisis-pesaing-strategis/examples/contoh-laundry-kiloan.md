# Contoh: Laundry kiloan "Bersih Sentosa" di Kota Sukamaju

> Semua nama, angka, dan kota di sini **fiktif** untuk contoh. Data pesaing dianggap dari papan harga, Google Maps publik, dan kunjungan sebagai pembeli biasa (dicek 2026-09-29). Skor dihitung `scripts/skor_matriks.py`; hitung tangan: Kita = (30x4 + 25x4 + 20x3 + 15x2 + 10x4)/100 = 3,50.

**Input pengguna:** "Laundry kiloan saya di kota kecil, sekarang Rp7.000/kg, cuci-setrika 2-3 hari. Ada 3 saingan yang saya tahu. Tolong analisis, saya mau tahu harus apa."

## Analisis Pesaing: Bersih Sentosa (Kota Sukamaju) - dicek 2026-09-29
**Ringkasan:** Kita murah dan hasilnya bagus, tetapi kalah cepat dan sulit dipesan. Ancaman terbesar: Laundry Express 24 (cepat, pesan lewat WA, katalog rapi). Peluang terbesar: langganan bulanan untuk kos-kosan dan keluarga yang belum dilayani rapi oleh siapa pun.

### 1. Peta pesaing
| Lingkaran | Pesaing | Alasan masuk |
|---|---|---|
| Langsung | Laundry Kinclong | Satu kecamatan, kiloan, harga Rp8.000/kg |
| Langsung | Laundry Express 24 | Paling sering disebut pelanggan; kilat 24 jam, Rp10.000/kg, antar-jemput |
| Tidak langsung | Laundry Koin Mandiri | Mesin koin swalayan dekat kos, murah tapi harus menunggu sendiri |
| Pengganti | Cuci sendiri / ART | Mayoritas keluarga; alasan utama: "hemat" |

### 2. Matriks perbandingan (ringkas)
| Toko | Layanan & harga | Kanal | Promo | Ulasan (Google) | Positioning | Sumber |
|---|---|---|---|---|---|---|
| Kita | Kiloan cuci-setrika Rp7.000/kg, 2-3 hari | Outlet, telepon | Tidak ada | 4,6 (58) tema: wangi, rapi | "Bersih dan murah" | data sendiri |
| Kinclong | Kiloan Rp8.000/kg, 2 hari | Outlet, WA | Diskon 10% hari Selasa | 4,0 (35) tema: kadang telat | "Laundry keluarga" | papan harga 2026-09-28 |
| Express 24 | Kiloan Rp10.000/kg, 1 hari; kilat 6 jam +Rp5.000/kg | WA, IG, antar-jemput gratis >5 kg | Member 10x gratis 1 | 4,5 (120) tema: cepat, admin ramah | "Cepat & praktis" | Maps + IG publik 2026-09-28 |
| Koin Mandiri | Rp15.000 per mesin 8 kg + pengering Rp10.000 | Outlet swalayan | - | (belum ada data) | "Cuci sendiri, murah" | kunjungan 2026-09-27 |

### 3. Skor berbobot & peta posisi (keluaran script)
```
## Skor berbobot (skala 1-5)
| Peringkat | Toko | Skor | Data terisi | Belum diketahui |
|---|---|---|---|---|
| 1 | Laundry Express 24 | 3,75 | 100% | - |
| 2 | Kita | 3,50 | 100% | - |
| 3 | Laundry Kinclong | 3,00 | 100% | - |
| 4 | Laundry Koin Mandiri | 2,44 | 90% | Reputasi & ulasan |

## Unggul dibanding rata-rata pesaing (urut prioritas = selisih x bobot)
- Harga: +1,33
- Kualitas hasil (bersih & wangi): +0,67
- Reputasi & ulasan: +0,5

## Tertinggal dibanding rata-rata pesaing
- Kemudahan pesan (WA/katalog): -1
- Kecepatan (selesai & antar): -0,33

Peta posisi (atas = Kecepatan (selesai & antar) tinggi, kanan = Harga tinggi)
5 |      .      2      .      .      .
4 |      .      .      .      .      .
3 |      .      .      1      0      .
2 |      .      .      3      .      .
1 |      .      .      .      .      .
  +--------------------------------------
         1      2      3      4      5   -> Harga
Kode: 0=Kita, 1=Laundry Kinclong, 2=Laundry Express 24, 3=Laundry Koin Mandiri (0 = kita)
Nilai dibulatkan ke 1-5 untuk peta; petak kosong = celah posisi yang belum diisi siapa pun.

Catatan: skor hanya secerdas nilai yang kamu isi; nilai 1-5 adalah penilaian subjektif berdasarkan bukti yang dicatat.
```
Catatan: Laundry Koin Mandiri belum punya data ulasan (cakupan 90%); skor dinormalkan ulang. Nilai adalah penilaian dari bukti di atas.
Celah pada peta: petak "harga menengah-rendah, kecepatan tinggi" kosong. Express 24 mengisi kecepatan tinggi tetapi dengan harga tinggi; pelanggan yang ingin cepat dan tidak mau bayar Rp10.000/kg belum dilayani.

### 4. SWOT (Bersih Sentosa terhadap pesaing)
| | |
|---|---|
| **Kekuatan** | Harga terendah di antara laundry penuh layanan (Rp7.000 vs 8.000-10.000). Ulasan bagus (4,6) tema wangi dan rapi. |
| **Kelemahan** | Belum ada WA/katalog (skor kemudahan 2 dari 5). Selesai 2-3 hari, kalah dari Express 24. |
| **Peluang** | Kos-kosan dan keluarga sibuk mau langganan mingguan. Celah "cepat tapi terjangkau". |
| **Ancaman** | Express 24 bisa menurunkan harga atau menambah promo. Cuci sendiri sebagai kebiasaan. |

### 5. Battlecard ringkas: Laundry Express 24
| Pelanggan bilang | Jawab dengan |
|---|---|
| "Express 24 lebih cepat." | "Betul, mereka kilat 1 hari. Kami 2 hari, tapi Rp3.000 lebih murah per kg. Kalau butuh besok, kami ada pilihan ekspres 1 hari [setelah pemilik memastikan bisa]. Cucian biasa lebih hemat di kami." |
| "Di sana bisa diantar." | "Kami antar gratis di atas 5 kg untuk radius 3 km mulai bulan depan." (hanya bila benar-benar akan dijalankan) |
| "Sudah langganan di sana." | "Baik, kalau ada cucian besar atau selimut boleh dicoba sekali, hasilnya bisa dilihat sendiri." |
Klaim terlarang: "Express 24 sering merusak baju" (tanpa bukti), menyebut nama pemilik mereka.
Kapan tidak dikejar: pelanggan yang butuh selesai hari yang sama.

### 6. Peluang & tindakan
| # | Tindakan | Kenapa (bukti) | Pemilik | Tenggat | Ukuran berhasil | Biaya | Dampak/Usaha |
|---|---|---|---|---|---|---|---|
| 1 | Pasang WA Bisnis: katalog, jam buka, harga, balasan otomatis | Kemudahan pesan skor 2 vs 5 | Pemilik | 3 hari | Pesanan via WA >= 30% dalam sebulan | Rp0 | Tinggi/Kecil |
| 2 | Tambah opsi kilat 1 hari (+Rp3.000/kg), cek kapasitas dulu | Kecepatan tertinggal, celah peta | Pemilik + karyawan | 2 minggu | 10 pesanan kilat/bulan | Lembur | Tinggi/Sedang |
| 3 | Paket langganan kos-kosan (min. 20 kg/minggu, diskon 5%) | Belum ada yang melayani; cek margin di `hitung-hpp` | Pemilik | 1 bulan | 3 kos berlangganan | Brosur | Sedang/Kecil |
| 4 | Minta ulasan Google dari pelanggan puas (tanpa imbalan yang menyesatkan, tanpa ulasan buatan) | Express 24 punya 120 ulasan vs 58 | Kasir | Berjalan | 20 ulasan baru/3 bulan | Rp0 | Sedang/Kecil |

### 7. Jadwal pantau
Cek ulang tiap 2 bulan (harga, promo, ulasan baru, kanal baru); segera cek bila ada laundry baru atau promo besar. Berikutnya: 2026-11-29.

### Data belum diketahui
Ulasan Koin Mandiri; kapasitas mesin Express 24; kapasitas kita untuk layanan kilat.

### Catatan etika & asumsi
Hanya sumber publik dan kunjungan sebagai pembeli biasa; tanpa login atau data pribadi pelanggan. Bukan nasihat hukum; aturan (UU ITE, UU 5/1999, UU 8/1999, UU 27/2022) dicek per 2026-09-29.
