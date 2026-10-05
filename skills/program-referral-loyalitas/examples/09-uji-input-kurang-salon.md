# 09 - Skenario input tidak lengkap: salon (usaha FIKTIF)

> Uji ulang independen v1.0.1 (2026-09-30; versi awal diuji pada v1.0.0).

**Pesan 1 pengguna:** "Bikin program member buat salon saya dong, biar pelanggan balik lagi."

## Jawaban skill (bertanya SEKALI, satu pesan, maks. 5 pertanyaan)
> Siap, saya bantu buatkan program member yang untungnya dihitung pasti. Boleh jawab singkat 5 hal ini?
> 1. Rata-rata sekali datang pelanggan bayar berapa? (perkiraan boleh, mis. Rp150rb)
> 2. Untung kotornya kira-kira berapa persen? (kalau belum tahu, saya pakai 50% untuk jasa dan saya sebutkan sebagai asumsi)
> 3. Pelanggan biasanya datang berapa kali sebulan, dan bertahan berapa lama?
> 4. Mau model apa: poin/stempel, ajak teman, atau dua-duanya?
> 5. Ada anggaran hadiah per bulan?
> Kalau mau cepat, jawab nomor 1 saja; sisanya saya isi dengan asumsi yang saya tulis di awal jawaban.

**Pesan 2 pengguna:** "Rata-rata 150rb lah. Sisanya terserah, yang penting cepat. Poin sama ajak teman."

## Jawaban skill (pakai default, asumsi ditulis di atas)
**Asumsi:** margin 50% (default jasa, **belum dari data Anda**; cek dengan skill `hitung-hpp`), datang 1x per bulan selama 6 bulan (default), hadiah referral Rp15.000 dua sisi dan poin Rp25.000 = 1 poin, 1 poin = Rp1.000 adalah **usulan awal**.

```
$ python3 scripts/hitung_referral.py poin --belanja-per-poin 25rb --nilai-poin 1rb --margin 50 --aov 150rb --minimum-tukar 20
NILAI POIN LOYALITAS
Aturan: tiap belanja Rp25.000 = 1 poin; 1 poin ditukar senilai Rp1.000
Hadiah poin = 4% dari belanja = 8% dari margin kotor 50%
STATUS: OK
Pesanan Rp150.000: dapat 6 poin (dibulatkan ke bawah) = Rp6.000 (4% dari pesanan). Laba kotor pesanan Rp75.000; setelah poin ditukar Rp69.000.
Minimum tukar 20 poin = belanja kumulatif Rp500.000, hadiah Rp20.000.
(kode keluar 0)

$ python3 scripts/hitung_referral.py biaya --aov 150rb --margin 50 --hadiah-pemberi 15rb --hadiah-teman 15rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp150.000  |  margin kotor 50%
Laba kotor pesanan pertama      : Rp75.000 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp15.000
Hadiah/diskon teman             : Rp15.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp30.000 = 20% dari nilai pesanan, 40% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp45.000
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)

$ python3 scripts/hitung_referral.py impas --aov 150rb --margin 50 --hadiah-pemberi 15rb --hadiah-teman 15rb
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp75.000 (nilai pesanan Rp150.000, margin 50%)
Biaya per referral              : Rp30.000 (pemberi Rp15.000 + teman Rp15.000 + lain Rp0)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp75.000 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp450.000 (6 pesanan; asumsi 1x per bulan selama 6 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp135.000 total per referral
BATAS ATAS hadiah pemberi (bukan anjuran; di atas ini melewati batas aman): Rp120.000
Hadiah pemberi SARAN (konservatif: total hadiah maks. 50% laba pesanan pertama): Rp22.500
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)

```

### Ringkasan
- **Poin member:** tiap belanja Rp25.000 = 1 poin, 20 poin (belanja Rp500.000) ditukar hadiah Rp20.000. Biaya 4% dari belanja = 8% dari margin (STATUS OK).
- **Ajak teman:** teman baru potongan Rp15.000, pengajak voucher Rp15.000 setelah teman selesai perawatan. Biaya per referral Rp30.000 (20% dari transaksi, 40% dari laba kotor), laba kunjungan pertama tetap Rp45.000, AMAN (batas Rp135.000). Voucher pengajak Rp15.000 di bawah angka SARAN konservatif Rp22.500; batas atas Rp120.000 bukan anjuran.
- Semua angka bergantung pada asumsi margin 50%; kirim angka modal (bahan + upah) kalau mau dihitung ulang.

### Aturan, S&K, teks
(Mengikuti template yang sama seperti contoh 06: teman = belum pernah datang, hadiah cair setelah layanan selesai, maks. 5 per pengajak per bulan, voucher bukan uang tunai, data minimal nama panggilan + nomor WA.)

> Halo Kak Maya, makasih sudah perawatan di salon kami. Sekarang tiap belanja Rp25.000 dapat 1 poin; 20 poin bisa ditukar senilai Rp20.000. Kalau ada teman yang belum pernah ke sini, temannya dapat potongan Rp15.000 dan Kakak dapat voucher Rp15.000 setelah temannya selesai perawatan. Balas "STOP" kalau tidak mau info seperti ini.

### Langkah minggu ini
1. Cek modal per layanan (skill `hitung-hpp`) lalu hitung ulang.
2. Siapkan buku/lembar catatan poin dan referral.
3. Umumkan ke 20 pelanggan tetap satu per satu.

## Uji tambahan: angka ambigu
Bila pengguna menulis nominal "150.5" (maksudnya tidak jelas), script menolak dan skill wajib bertanya, bukan menebak:
```
$ python3 scripts/hitung_referral.py biaya --aov 150.5 --margin 50
GAGAL: nilai pesanan '150.5' ambigu: titik dipakai sebagai pemisah ribuan. Tulis mis. 12.500 (dua belas ribu lima ratus) atau 12,5rb
(kode keluar 2)
```
> Maaf, angka "150.5" belum jelas bagi saya: maksudnya Rp150.500 atau Rp150.000-an? Tolong tulis ulang, mis. 150.500 atau 150rb.

## Catatan penguji
- Lulus (uji ulang v1.0.1): bertanya sekali, 5 pertanyaan, menawarkan jalur cepat, asumsi ditandai jelas, tidak menghitung sebelum AOV ada.
- Angka ambigu `150.5` tetap ditolak `GAGAL` kode 2 dengan pesan yang sama; tambahan uji ulang: `--aov 12,5` (Rp12,5?) ditolak dengan saran "12,5rb", `--frekuensi-bulan 1.000` ditolak ambigu. Tidak ada regresi.
- Salon di sini adalah perawatan rambut/wajah non-medis (pola jasa). Bila salon melakukan tindakan medis (suntik, laser, peeling medis), skill mengarahkan ke bagian fasilitas kesehatan (tanpa imbalan untuk merujuk).
