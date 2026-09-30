# 07 - Skenario normal 2: kafe dengan poin + kartu stempel + "traktir teman" (usaha FIKTIF)

> Uji ulang independen v1.0.1 (2026-09-30; versi awal diuji pada v1.0.0). Angka dari `scripts/hitung_referral.py`, diverifikasi ulang secara independen.

**Permintaan pengguna:** "Kafe saya Kopi Lereng, rata-rata sekali datang Rp38.500, margin 65%, omzet Rp45jt sebulan. Sudah jalan poin: tiap Rp10rb dapat 1 poin, 1 poin = Rp300, minimal tukar 50 poin. Poin yang belum ditukar sekarang 52.340 poin, kira-kira 25% nggak pernah ditukar. Mau tambah kartu stempel (beli 8 gratis 1, minuman Rp28rb modalnya Rp9rb) dan 'traktir teman' 1 minuman gratis. Aman? Utang poin saya berapa?"

## Perhitungan (script)
Angka poin beredar ditulis persis seperti pengguna (`52.340`, format Indonesia); v1.0.1 membacanya sebagai 52.340 poin:
```
$ python3 scripts/hitung_referral.py poin --belanja-per-poin 10rb --nilai-poin 300 --margin 65 --aov 38.500 --omzet-bulan 45jt --breakage 25 --poin-beredar 52.340 --minimum-tukar 50
NILAI POIN LOYALITAS
Aturan: tiap belanja Rp10.000 = 1 poin; 1 poin ditukar senilai Rp300
Hadiah poin = 3% dari belanja = 4,62% dari margin kotor 65%
STATUS: OK
Bila 25% poin tidak pernah ditukar (perkiraan): biaya efektif 2,25% dari belanja.
Pesanan Rp38.500: dapat 3 poin (dibulatkan ke bawah) = Rp900 (2,34% dari pesanan). Laba kotor pesanan Rp25.025; setelah poin ditukar Rp24.125.
Omzet Rp45.000.000/bulan: biaya poin maksimal (semua ditukar) Rp1.350.000; perkiraan Rp1.012.500 (ESTIMASI).
LIABILITY (kewajiban) poin beredar 52.340 poin: maksimal Rp15.702.000 bila semua ditukar; perkiraan Rp11.776.500 (ESTIMASI).
Sisihkan dana sebesar liability maksimal bila ingin aman; bila pembukuan formal, tanyakan akuntan cara mencatatnya.
Minimum tukar 50 poin = belanja kumulatif Rp500.000, hadiah Rp15.000.
(kode keluar 0)

$ python3 scripts/hitung_referral.py poin --belanja-per-poin 28rb --nilai-poin 1.125 --margin 65 --aov 38.500 --minimum-tukar 8
NILAI POIN LOYALITAS
Aturan: tiap belanja Rp28.000 = 1 poin; 1 poin ditukar senilai Rp1.125
Hadiah poin = 4,02% dari belanja = 6,18% dari margin kotor 65%
STATUS: OK
Pesanan Rp38.500: dapat 1 poin (dibulatkan ke bawah) = Rp1.125 (2,92% dari pesanan). Laba kotor pesanan Rp25.025; setelah poin ditukar Rp23.900.
Minimum tukar 8 poin = belanja kumulatif Rp224.000, hadiah Rp9.000.
(kode keluar 0)

$ python3 scripts/hitung_referral.py biaya --aov 38.500 --margin 65 --hadiah-teman 9rb --jumlah-referral 30 --anggaran 300rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp38.500  |  margin kotor 65%
Laba kotor pesanan pertama      : Rp25.025 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp0
Hadiah/diskon teman             : Rp9.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp9.000 = 23,38% dari nilai pesanan, 35,96% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp16.025
Program 30 referral berhasil: total biaya Rp270.000; total laba kotor pesanan pertama Rp750.750; laba setelah hadiah Rp480.750
Anggaran Rp300.000: cukup (sisa Rp30.000)
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)

$ python3 scripts/hitung_referral.py impas --aov 38.500 --margin 65 --hadiah-teman 9rb --frekuensi-bulan 3 --umur-bulan 6
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp25.025 (nilai pesanan Rp38.500, margin 65%)
Biaya per referral              : Rp9.000 (pemberi Rp0 + teman Rp9.000 + lain Rp0)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp25.025 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp450.450 (18 pesanan; asumsi 3x per bulan selama 6 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp135.135 total per referral
BATAS ATAS hadiah pemberi (bukan anjuran; di atas ini melewati batas aman): Rp126.135
Hadiah pemberi SARAN (konservatif: total hadiah maks. 50% laba pesanan pertama): Rp3.512
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)

```
Catatan: kartu stempel "beli 8 gratis 1" dimodelkan sebagai poin: 1 stempel per belanja Rp28.000, nilai tukar = modal hadiah Rp9.000 / 8 stempel = Rp1.125 per stempel (skill: hadiah produk dihitung dengan modal/HPP). Traktir teman dihitung dengan modal minuman Rp9.000.

## Jawaban skill

### 1. Ringkasan
- **Poin yang berjalan sehat:** hadiah poin 3% dari belanja = 4,62% dari margin (STATUS OK). Setelah 25% poin tidak ditukar, biaya efektif 2,25% dari belanja.
- **"Utang poin" (liability) Anda:** maksimal **Rp15.702.000** bila semua 52.340 poin ditukar; perkiraan Rp11.776.500 (ESTIMASI). Sisihkan dana sebesar angka maksimal bila ingin aman.
- **Tambahan:** kartu stempel (4,02% dari belanja, OK) dan traktir teman (biaya Rp9.000 per teman baru yang datang, laba kunjungan pertama tetap Rp16.025). Saran: **jangan jalankan poin dan stempel bersamaan** untuk pelanggan yang sama; pilih satu agar kasir dan pelanggan tidak bingung.

### 2. Asumsi
Margin 65%, omzet, breakage 25% dari pengguna (breakage = perkiraan). Pelanggan datang 3x per bulan selama 6 bulan: asumsi. Batas aman 30% dan batas "separuh margin" poin = aturan praktis.

### 3. Tabel angka (dari script)
| Hal | Nilai |
|---|---|
| Hadiah poin | 3% dari belanja; 4,62% dari margin (OK) |
| Biaya poin per bulan (omzet Rp45.000.000) | maks Rp1.350.000; perkiraan Rp1.012.500 (ESTIMASI) |
| Liability poin beredar (52.340 poin) | maks Rp15.702.000; perkiraan Rp11.776.500 (ESTIMASI) |
| Minimum tukar 50 poin | belanja kumulatif Rp500.000, hadiah Rp15.000 |
| Kartu stempel (8 stempel) | 4,02% dari belanja; 6,18% dari margin (OK); hadiah Rp9.000 (modal) setelah belanja Rp224.000 |
| Traktir teman (1 minuman, modal Rp9.000) | biaya Rp9.000 per teman baru; laba kunjungan pertama Rp16.025; batas aman Rp135.135 (AMAN) |
| Bila nanti pengajak ikut diberi hadiah | SARAN konservatif paling besar Rp3.512 per teman (batas atas Rp126.135 bukan anjuran) |
| 30 teman baru/bulan, anggaran Rp300.000 | total Rp270.000, cukup (sisa Rp30.000) |

### 4. Aturan program
- Poin: kedaluwarsa jelas (mis. 6 bulan sejak diperoleh) dan diumumkan di kasir; poin tidak bisa diuangkan. Poin yang kedaluwarsa tetap dihitung dengan jujur; jangan memendekkan masa berlaku diam-diam (UU 8/1999).
- Traktir teman: teman = orang yang belum pernah terdaftar/datang; datang bersama pengajak; 1 minuman gratis per teman, maks. 3 teman per pengajak per bulan, kuota 30 per bulan.
- Data minimal: nama panggilan + nomor WA untuk poin. Pelanggan boleh ikut tanpa memberi nomor (kartu fisik).

### 5. S&K ringkas (dari template)
Tiap belanja Rp10.000 = 1 poin; 50 poin ditukar senilai Rp15.000; poin berlaku 6 bulan; tidak bisa diuangkan. Traktir teman: 1 minuman gratis untuk teman yang pertama kali datang bersama pengajak; maks. 3 per pengajak per bulan; kuota 30 per bulan. Data (nama panggilan, nomor WA, saldo poin) hanya untuk program ini dan dapat dihapus atas permintaan.

### 6. Teks
**Pengumuman di meja kasir / status WA:**
> Sekarang tiap belanja Rp10.000 dapat 1 poin. 50 poin bisa ditukar senilai Rp15.000. Poin berlaku 6 bulan. Datang pertama kali bareng teman yang sudah langganan? Kamu dapat 1 minuman gratis. Syarat berlaku, tanya kasir ya.

**WA personal ke pelanggan tetap (satu per satu):**
> Halo Kak Bima, makasih sudah sering mampir ke Kopi Lereng. Poin Kakak sekarang cukup buat tukar minuman lho. Kalau mau ajak teman yang belum pernah ke sini, temannya dapat 1 minuman gratis waktu datang bareng Kakak. Balas "STOP" kalau tidak mau info seperti ini.

### 7. Langkah minggu ini
1. Cetak pengumuman poin + masa berlaku di kasir.
2. Pisahkan dana cadangan liability (acuan: Rp15.702.000 maks) atau minimal pantau tiap bulan.
3. Latih kasir: cek "teman baru" di buku catatan sebelum memberi minuman gratis.
4. Pilih salah satu: poin **atau** stempel untuk pelanggan baru.
5. Akhir bulan: catat poin ditukar vs kedaluwarsa untuk mengganti angka breakage 25% dengan data nyata.

### 8. Catatan
Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda. Pembukuan liability poin secara formal: tanyakan akuntan.

## Catatan penguji
- Uji ulang v1.0.1: temuan lama T1 **teratasi**. `--poin-beredar 52.340` kini dibaca 52.340 poin (liability Rp15.702.000, sama dengan input `52340`); agent tidak perlu lagi menulis ulang angka pengguna. Angka ambigu seperti `52,340` atau `52.3` ditolak `GAGAL` (kode 2) dengan pesan jelas.
- Semua angka cocok dengan hitungan independen (Fraction), termasuk baris baru SARAN Rp3.512 = floor(Rp25.025 x 50%) - Rp9.000.
- "Poin kedaluwarsa" tetap hanya bisa dimodelkan lewat `--breakage`; rendah, cukup untuk UMKM.
