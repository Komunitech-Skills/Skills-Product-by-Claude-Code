# Contoh 01 - Toko hijab online: program "ajak teman" (usaha FIKTIF)

> Contoh buatan Komunitech dengan usaha fiktif "Hijab Alya". Semua angka rupiah di bawah adalah keluaran nyata `scripts/hitung_referral.py`; margin, frekuensi beli, dan skenario adalah asumsi pengguna/skill.

**Permintaan pengguna:** "Toko hijab online saya di Shopee dan WA, pesanan rata-rata Rp180.000, untung kotor 40%. Mau program ajak teman, hadiahnya Rp15.000 untuk dua-duanya. Aman nggak? Pelanggan lama sekitar 300 orang, sekali beli kira-kira tiap 2 bulan. Biaya iklan sekarang Rp45.000 per pelanggan baru."

## Perhitungan (script)
```
$ python3 scripts/hitung_referral.py biaya --aov 180rb --margin 40 --hadiah-pemberi 15rb --hadiah-teman 15rb --anggaran 600rb --cac-iklan 45rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp180.000  |  margin kotor 40%
Laba kotor pesanan pertama      : Rp72.000 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp15.000
Hadiah/diskon teman             : Rp15.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp30.000 = 16,67% dari nilai pesanan, 41,67% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp42.000
Anggaran Rp600.000 cukup untuk maksimal 20 referral berhasil.
Pembanding: biaya per pelanggan baru dari iklan Rp45.000 -> referral LEBIH MURAH (selisih Rp15.000).
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)
```

```
$ python3 scripts/hitung_referral.py impas --aov 180rb --margin 40 --hadiah-pemberi 15rb --hadiah-teman 15rb --frekuensi-bulan 0,5 --umur-bulan 12
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp72.000 (nilai pesanan Rp180.000, margin 40%)
Biaya per referral              : Rp30.000 (pemberi Rp15.000 + teman Rp15.000 + lain Rp0)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp72.000 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp432.000 (6 pesanan; asumsi 0,5x per bulan selama 12 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp129.600 total per referral
Hadiah pemberi maksimal (bila hadiah teman & biaya lain tetap): Rp114.600
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)
```

Pembanding hadiah yang lebih besar (Rp50.000 + Rp30.000):
```
$ python3 scripts/hitung_referral.py biaya --aov 180rb --margin 40 --hadiah-pemberi 50rb --hadiah-teman 30rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp180.000  |  margin kotor 40%
Laba kotor pesanan pertama      : Rp72.000 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp50.000
Hadiah/diskon teman             : Rp30.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp80.000 = 44,44% dari nilai pesanan, 111,11% dari laba kotor
Laba pesanan pertama setelah hadiah: -Rp8.000
PERHATIAN: hadiah lebih besar dari laba kotor pesanan pertama (rugi Rp8.000 per referral). Balik modal hanya bila teman membeli lagi, minimal 1 pesanan ulang.
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)
```

```
$ python3 scripts/hitung_referral.py impas --aov 180rb --margin 40 --hadiah-pemberi 50rb --hadiah-teman 30rb --frekuensi-bulan 0,5 --umur-bulan 12
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp72.000 (nilai pesanan Rp180.000, margin 40%)
Biaya per referral              : Rp80.000 (pemberi Rp50.000 + teman Rp30.000 + lain Rp0)
Balik modal setelah             : pesanan ke-2 milik teman, sekitar bulan ke-2 bila belanja 0,5x per bulan
Hadiah maks agar impas di pesanan pertama: Rp72.000 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp432.000 (6 pesanan; asumsi 0,5x per bulan selama 12 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp129.600 total per referral
Hadiah pemberi maksimal (bila hadiah teman & biaya lain tetap): Rp99.600
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)
```

```
$ python3 scripts/hitung_referral.py simulasi --pelanggan-aktif 300 --aov 180rb --margin 40 --hadiah-pemberi 15rb --hadiah-teman 15rb --pesanan-ulang 0,5 --anggaran 600rb --cac-iklan 45rb
SIMULASI REFERRAL (ESTIMASI, bukan kepastian) - 300 pelanggan aktif
Biaya per referral berhasil Rp30.000; laba kotor per pesanan Rp72.000; pesanan ulang per teman baru: 0,5
- konservatif: 15 perujuk -> 15 teman diajak -> 3 pembeli baru | omzet Rp810.000 | biaya hadiah Rp90.000 | laba kotor Rp324.000 | laba setelah hadiah Rp234.000 | ROI 260%
- realistis: 30 perujuk -> 60 teman diajak -> 15 pembeli baru | omzet Rp4.050.000 | biaya hadiah Rp450.000 | laba kotor Rp1.620.000 | laba setelah hadiah Rp1.170.000 | ROI 260%
- optimis: 45 perujuk -> 90 teman diajak -> 27 pembeli baru | omzet Rp7.290.000 | biaya hadiah Rp810.000 | laba kotor Rp2.916.000 | laba setelah hadiah Rp2.106.000 | ROI 260%
  PERHATIAN: biaya Rp810.000 melebihi anggaran Rp600.000; pasang batas kuota hadiah.
Pembanding iklan: Rp45.000 per pelanggan baru -> referral lebih murah (Rp30.000 per pembeli baru).
Angka skenario adalah asumsi awal, bukan patokan pasar; ganti dengan data Anda setelah 1 bulan berjalan.
(kode keluar 0)
```


## Jawaban skill

### 1. Ringkasan
- **Program:** referral dua sisi. Teman baru dapat voucher Rp15.000 untuk pesanan pertama; pengajak dapat voucher Rp15.000 **setelah pesanan teman selesai dan lewat 7 hari tanpa retur**.
- **Aman?** Ya. Biaya per referral Rp30.000 (16,67% dari pesanan, 41,67% dari laba kotor). Laba pesanan pertama tetap Rp42.000, balik modal langsung di pesanan pertama.
- **Lebih murah dari iklan** (Rp45.000 per pelanggan baru), selisih Rp15.000 per pelanggan.

### 2. Asumsi
Margin 40% dari pengguna. Frekuensi beli 0,5x per bulan (tiap 2 bulan) dan umur pelanggan 12 bulan: asumsi. Batas aman 30% dari laba seumur pelanggan adalah aturan praktis. Anggaran hadiah Rp600.000 per bulan (usulan: cukup untuk maksimal 20 referral berhasil).

### 3. Tabel angka
| Hal | Nilai (dari script) |
|---|---|
| Laba kotor per pesanan | Rp72.000 |
| Biaya per referral | Rp30.000 |
| Laba pesanan pertama setelah hadiah | Rp42.000 |
| Batas hadiah aman per referral | Rp129.600 (status AMAN) |
| Hadiah pengajak maksimal (hadiah teman tetap Rp15.000) | Rp114.600 |
| Pilihan lebih besar (Rp50.000 + Rp30.000 = Rp80.000) | biaya Rp80.000; laba pesanan pertama setelah hadiah -Rp8.000 (rugi di pesanan pertama), balik modal di pesanan ke-2 (sekitar bulan ke-2), status AMAN terhadap laba seumur pelanggan; cocok hanya untuk momen khusus dengan kuota kecil |

### 4. Aturan program
- Teman = nomor/akun yang belum pernah beli. Nomor, alamat, dan akun yang sama dengan pengajak tidak sah.
- Maksimal 5 hadiah per pengajak per bulan; kuota 20 per bulan; voucher berlaku 30 hari.
- Hadiah berupa **voucher toko / potongan**, bukan uang tunai.
- Shopee: ikuti aturan platform; jangan mengajak pindah transaksi di luar Shopee. Untuk pembeli di WA (toko sendiri) program berjalan penuh. Untuk pembeli Shopee, berikan kartu ucapan berisi ajakan dan gunakan voucher toko yang tersedia di Shopee (bila fitur dan aturan platform mengizinkan).
- Data yang dicatat: nama panggilan, nomor WA, kode, tanggal, status hadiah (`templates/lembar-catatan-referral.csv`).

### 5. Syarat & ketentuan (ringkas; versi lengkap dari `templates/syarat-ketentuan.md`)
1. Berlaku untuk pelanggan Hijab Alya dan Teman Baru yang belum pernah berbelanja.
2. Teman Baru menghubungi kami lebih dulu dan menyebut nama pengajak sebelum memesan.
3. Teman Baru: potongan Rp15.000 untuk pesanan pertama. Pengajak: voucher Rp15.000 per Teman Baru setelah pesanan selesai dan lewat 7 hari tanpa retur.
4. Maksimal 5 hadiah per pengajak per bulan; kuota 20 hadiah per bulan; voucher berlaku 30 hari; tidak dapat diuangkan.
5. Tidak berlaku bila nomor/alamat/akun sama, pesanan dibatalkan/diretur, atau ada indikasi akun ganda. Kami menjelaskan alasan penolakan.
6. Data (nama panggilan, nomor WA, kode, tanggal, status hadiah) hanya untuk program ini, tidak dibagikan, dan dapat dihapus atas permintaan.

### 6. Teks ajakan (kirim satu per satu ke pelanggan yang sudah puas)
> Halo Kak Ratna, terima kasih sudah belanja di Hijab Alya. Senang kalau pashminanya cocok ya.
> Kalau Kakak punya teman yang mungkin suka, boleh dibagikan. Teman Kakak dapat potongan Rp15.000 untuk pesanan pertama, dan Kakak dapat voucher Rp15.000 setelah pesanannya selesai. Cukup suruh temannya chat kami dan sebut nama Kakak.
> Syarat lengkap: balas "S&K". Tidak ingin dapat info seperti ini? Balas "STOP" ya.

Story IG: "Ajak teman, dapat voucher! Teman baru potongan Rp15.000, kamu voucher Rp15.000 setelah pesanannya selesai. Syarat berlaku. DM @hijabalya."

### 7. Simulasi (ESTIMASI)
Dengan 300 pelanggan lama: skenario realistis (10% mengajak, 2 teman tiap pengajak, 25% teman membeli) = 15 pembeli baru, biaya hadiah Rp450.000 (masih dalam anggaran Rp600.000). Skenario optimis Rp810.000 melewati anggaran, jadi pasang kuota 20 hadiah. Ini asumsi awal, bukan patokan pasar; ganti dengan data setelah 1 bulan.

### 8. Langkah minggu ini
1. Isi lembar catatan dan tempel S&K.
2. Kirim teks ajakan ke 15 pelanggan terbaik (satu per satu, bukan blast).
3. Tanyakan "Tahu kami dari mana?" di setiap pesanan baru.
4. Tinjau angka di hari ke-30; hentikan atau ubah bila perujuk aktif < 3.
5. Cek aturan Shopee sebelum menyebar ke pembeli marketplace.

Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda.
