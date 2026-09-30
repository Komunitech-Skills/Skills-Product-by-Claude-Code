# Contoh 02 - Kedai kopi: poin loyalitas + "traktir teman" (usaha FIKTIF)

> Contoh buatan Komunitech dengan usaha fiktif "Kopi Senja". Angka rupiah/persen = keluaran nyata script; margin 65%, tingkat poin tidak ditukar (25%), dan jumlah poin beredar adalah asumsi/data contoh.

**Permintaan pengguna:** "Kedai kopi saya, rata-rata bon Rp35.000, untung kotor 65%. Omzet Rp45 juta per bulan. Saya mau bikin poin: tiap belanja Rp10.000 dapat 1 poin, 1 poin senilai Rp300, tukar minimal 50 poin. Kayaknya 25% poin nggak pernah ditukar. Sekarang sudah ada 30.000 poin beredar di buku. Poin saya jadi utang berapa? Sekalian ide teman diajak."

## Perhitungan (script)
```
$ python3 scripts/hitung_referral.py poin --belanja-per-poin 10rb --nilai-poin 300 --margin 65 --aov 35rb --omzet-bulan 45jt --breakage 25 --poin-beredar 30000 --minimum-tukar 50
NILAI POIN LOYALITAS
Aturan: tiap belanja Rp10.000 = 1 poin; 1 poin ditukar senilai Rp300
Hadiah poin = 3% dari belanja = 4,62% dari margin kotor 65%
STATUS: OK
Bila 25% poin tidak pernah ditukar (perkiraan): biaya efektif 2,25% dari belanja.
Pesanan Rp35.000: dapat 3 poin (dibulatkan ke bawah) = Rp900 (2,57% dari pesanan). Laba kotor pesanan Rp22.750; setelah poin ditukar Rp21.850.
Omzet Rp45.000.000/bulan: biaya poin maksimal (semua ditukar) Rp1.350.000; perkiraan Rp1.012.500 (ESTIMASI).
LIABILITY (kewajiban) poin beredar 30.000 poin: maksimal Rp9.000.000 bila semua ditukar; perkiraan Rp6.750.000 (ESTIMASI).
Sisihkan dana sebesar liability maksimal bila ingin aman; bila pembukuan formal, tanyakan akuntan cara mencatatnya.
Minimum tukar 50 poin = belanja kumulatif Rp500.000, hadiah Rp15.000.
(kode keluar 0)
```

Pembanding kalau nilai poin dibuat Rp1.000 (supaya terasa besar):
```
$ python3 scripts/hitung_referral.py poin --belanja-per-poin 10rb --nilai-poin 1rb --margin 65 --aov 35rb --minimum-tukar 50
NILAI POIN LOYALITAS
Aturan: tiap belanja Rp10.000 = 1 poin; 1 poin ditukar senilai Rp1.000
Hadiah poin = 10% dari belanja = 15,38% dari margin kotor 65%
STATUS: OK
Pesanan Rp35.000: dapat 3 poin (dibulatkan ke bawah) = Rp3.000 (8,57% dari pesanan). Laba kotor pesanan Rp22.750; setelah poin ditukar Rp19.750.
Minimum tukar 50 poin = belanja kumulatif Rp500.000, hadiah Rp50.000.
(kode keluar 0)
```

Hadiah "traktir teman" (satu minuman gratis untuk kedua orang, dihitung dari modal minuman Rp12.000, bukan harga jual):
```
$ python3 scripts/hitung_referral.py biaya --aov 35rb --margin 65 --hadiah-pemberi 12rb --hadiah-teman 12rb --anggaran 400rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp35.000  |  margin kotor 65%
Laba kotor pesanan pertama      : Rp22.750 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp12.000
Hadiah/diskon teman             : Rp12.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp24.000 = 68,57% dari nilai pesanan, 105,49% dari laba kotor
Laba pesanan pertama setelah hadiah: -Rp1.250
PERHATIAN: hadiah lebih besar dari laba kotor pesanan pertama (rugi Rp1.250 per referral). Balik modal hanya bila teman membeli lagi, minimal 1 pesanan ulang.
Anggaran Rp400.000 cukup untuk maksimal 16 referral berhasil.
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)
```


## Jawaban skill

### 1. Ringkasan
- **Poin Anda aman:** hadiah 3% dari belanja = 4,62% dari margin 65% (status OK). Poin di tiap bon Rp35.000: 3 poin (dibulatkan ke bawah) = Rp900.
- **Liability:** 30.000 poin beredar = **maksimal Rp9.000.000** bila semua ditukar; perkiraan Rp6.750.000 bila 25% tidak pernah ditukar (ESTIMASI). Sisihkan dana sebesar angka maksimal bila ingin aman.
- **Biaya bulanan poin:** maksimal Rp1.350.000 (semua ditukar), perkiraan Rp1.012.500.

### 2. Aturan program yang disarankan
- 10.000 = 1 poin; 1 poin = Rp300; tukar minimal 50 poin (belanja kumulatif Rp500.000, hadiah Rp15.000 berupa minuman/voucher).
- **Poin kedaluwarsa** 12 bulan sejak diperoleh (tulis jelas di S&K dan umumkan sebelum berlaku); ini yang membuat sebagian poin tidak menjadi biaya, jangan dipakai untuk menjebak pelanggan.
- Poin tidak dapat diuangkan, tidak dapat dipindahtangankan, hanya untuk pembelian sendiri.
- Bandingkan: bila 1 poin = Rp1.000 hadiah menjadi 10% belanja = 15,38% dari margin; status masih OK, tetapi nilai poin beredar (liability) menjadi jauh lebih besar, jadi tidak disarankan untuk usaha kecil tanpa dana cadangan (hitung ulang dengan `--poin-beredar` bila ingin memakainya).

### 3. "Traktir teman"
Teman yang datang pertama kali bersama pelanggan mendapat 1 minuman gratis; pelanggan mendapat 1 minuman gratis di kunjungan berikutnya. Biaya per referral Rp24.000 (modal minuman Rp12.000 x 2) = 68,57% dari nilai pesanan, 105,49% dari laba kotor pesanan pertama Rp22.750, jadi **laba pesanan pertama negatif (rugi Rp1.250)** dan skrip menandai PERHATIAN. Saran: teman mendapat minuman gratis, pengajak mendapat poin bonus atau voucher kecil; jalankan ulang script dengan angka barunya sebelum dipakai. Anggaran Rp400.000 cukup untuk 16 referral berhasil.

### 4. Kartu poin siap cetak (teks)
"Kartu Poin Kopi Senja: tiap belanja Rp10.000 = 1 poin. 50 poin = voucher Rp15.000. Poin berlaku 12 bulan. Syarat: tanya kasir."

### 5. Langkah minggu ini
1. Rekap poin beredar per akhir bulan dan sisihkan Rp9.000.000 secara bertahap (bukan sekaligus).
2. Cetak kartu poin dan tempel S&K di meja kasir.
3. Uji "traktir teman" selama 2 minggu dengan kuota 10.
4. Catat siapa yang menukar poin untuk memperbaiki perkiraan 25%.
5. Data pelanggan: nama panggilan dan nomor WA saja, dengan persetujuan.

Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda.
