# Contoh 04 - Input kurang dan angka salah ketik: laundry kiloan (usaha FIKTIF)

> Contoh buatan Komunitech. Bagian angka = keluaran nyata script.

**Permintaan pengguna:** "Bikinin program biar pelanggan laundry saya ngajak teman dong."

## Skill bertanya SEKALI (satu pesan)
> Supaya angkanya pas, mohon jawab singkat ya:
> 1. Rata-rata satu nota Rp berapa?
> 2. Untung kotor kira-kira berapa persen (kalau tidak tahu, saya pakai 50% untuk jasa)?
> 3. Pelanggan biasa datang berapa kali sebulan, dan sudah berapa lama rata-rata langganan?
> 4. Berapa pelanggan tetap yang ada sekarang?
> 5. Pelanggan Anda kebanyakan lewat WhatsApp atau datang langsung?

**Jawaban pengguna:** "Rata-rata nota Rp 45.5 mungkin ya. Untung nggak tahu. Datang seminggu sekali. Pelanggan tetap 120. Kebanyakan WA. Buru-buru, pakai default aja."

## Data rusak: angka ambigu ditolak, bukan ditebak
```
$ python3 scripts/hitung_referral.py biaya --aov 45.5 --margin 50 --hadiah-pemberi 5rb --hadiah-teman 5rb
GAGAL: nilai pesanan '45.5' ambigu: titik dipakai sebagai pemisah ribuan. Tulis mis. 12.500 (dua belas ribu lima ratus) atau 12,5rb
(kode keluar 2)
```

Skill menyampaikan dengan bahasa awam: "Nota Rp 45.5 bisa berarti Rp45.500 atau Rp45 lebih sedikit; supaya tidak salah hitung, mohon tulis lengkap, mis. 45.500 atau 45,5rb." Pengguna menjawab: "Maksudnya Rp45.000 saja deh."

## Asumsi (pengguna ingin cepat)
Margin **50%** (default jasa), nota Rp45.000, hadiah kecil Rp5.000 untuk dua-duanya, frekuensi 4x per bulan (seminggu sekali), umur pelanggan 6 bulan (default), anggaran belum ditentukan.

## Perhitungan (script)
```
$ python3 scripts/hitung_referral.py biaya --aov 45rb --margin 50 --hadiah-pemberi 5rb --hadiah-teman 5rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp45.000  |  margin kotor 50%
Laba kotor pesanan pertama      : Rp22.500 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp5.000
Hadiah/diskon teman             : Rp5.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp10.000 = 22,22% dari nilai pesanan, 44,44% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp12.500
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)
```

```
$ python3 scripts/hitung_referral.py impas --aov 45rb --margin 50 --hadiah-pemberi 5rb --hadiah-teman 5rb --frekuensi-bulan 4 --umur-bulan 6
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp22.500 (nilai pesanan Rp45.000, margin 50%)
Biaya per referral              : Rp10.000 (pemberi Rp5.000 + teman Rp5.000 + lain Rp0)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp22.500 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp540.000 (24 pesanan; asumsi 4x per bulan selama 6 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp162.000 total per referral
Hadiah pemberi maksimal (bila hadiah teman & biaya lain tetap): Rp157.000
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)
```

```
$ python3 scripts/hitung_referral.py simulasi --pelanggan-aktif 120 --aov 45rb --margin 50 --hadiah-pemberi 5rb --hadiah-teman 5rb
SIMULASI REFERRAL (ESTIMASI, bukan kepastian) - 120 pelanggan aktif
Biaya per referral berhasil Rp10.000; laba kotor per pesanan Rp22.500; pesanan ulang per teman baru: 0
- konservatif: 6 perujuk -> 6 teman diajak -> 1 pembeli baru | omzet Rp45.000 | biaya hadiah Rp10.000 | laba kotor Rp22.500 | laba setelah hadiah Rp12.500 | ROI 125%
- realistis: 12 perujuk -> 24 teman diajak -> 6 pembeli baru | omzet Rp270.000 | biaya hadiah Rp60.000 | laba kotor Rp135.000 | laba setelah hadiah Rp75.000 | ROI 125%
- optimis: 18 perujuk -> 36 teman diajak -> 11 pembeli baru | omzet Rp495.000 | biaya hadiah Rp110.000 | laba kotor Rp247.500 | laba setelah hadiah Rp137.500 | ROI 125%
Angka skenario adalah asumsi awal, bukan patokan pasar; ganti dengan data Anda setelah 1 bulan berjalan.
(kode keluar 0)
```


## Jawaban skill (ringkas)
- **Ringkasan:** program "Ajak Tetangga": teman dapat potongan Rp5.000 di nota pertama, pengajak dapat potongan Rp5.000 di nota berikutnya setelah nota teman lunas. Biaya per referral Rp10.000 (22,22% dari nota, 44,44% dari laba kotor), laba nota pertama Rp12.500.
- Batas aman Rp162.000 per referral (asumsi 4x per bulan, 6 bulan), jadi hadiah masih bisa dinaikkan bila perlu; mulai kecil, lihat respons 2 minggu.
- **Asumsi yang perlu diganti:** margin sebenarnya, umur langganan, dan skenario simulasi (asumsi awal, bukan patokan pasar). Simulasi 120 pelanggan tetap: skenario realistis 12 perujuk -> 24 teman diajak -> 6 pembeli baru, biaya hadiah Rp60.000 (ESTIMASI).
- **Aturan:** teman = nomor baru; nomor sama dengan pengajak tidak sah; potongan hanya untuk nota lunas; maksimal 3 hadiah per pengajak per bulan.
- **Teks WA:** "Halo Kak [NAMA], terima kasih sudah langganan [LAUNDRY]. Kalau ada tetangga/teman yang butuh laundry, suruh chat kami dan sebut nama Kakak. Temannya potongan Rp5.000 di nota pertama, Kakak potongan Rp5.000 setelah nota temannya lunas. Balas STOP kalau tidak ingin info seperti ini."
- Kirim teks itu satu per satu ke pelanggan yang aktif; jangan blast.
- Langkah minggu ini: isi lembar catatan, hitung margin sebenarnya (skill `hitung-hpp`), uji ke 20 pelanggan terbaik.

Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda.
