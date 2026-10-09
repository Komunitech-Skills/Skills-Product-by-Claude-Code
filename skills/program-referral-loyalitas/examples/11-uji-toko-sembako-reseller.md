# 11 - Skenario normal 4: toko sembako grosir, warung langganan & reseller (usaha FIKTIF)

> Uji ulang independen v1.0.1 (2026-09-30), skenario baru. Penguji bertindak sebagai agent yang memakai skill dari salinan di scratchpad. Semua angka rupiah dari `scripts/hitung_referral.py` dan diverifikasi ulang secara independen (lihat `HASIL-UJI-ULANG.md`). Semua angka ditulis pengguna dalam format Indonesia (`1.250.000`, `2,5jt`).

**Permintaan pengguna:** "Saya punya toko sembako grosir 'Berkah Jaya', pembelinya warung-warung sekitar, pesan lewat WA. Rata-rata sekali belanja warung Rp1.250.000, untung kotor cuma 12%. Warung langganan ada 180, rata-rata belanja 4 kali sebulan. Mau bikin: (1) warung yang ngajak warung lain dapat hadiah, (2) beberapa ibu-ibu mau jadi reseller, saya kasih komisi 3% dari belanjaan warung yang mereka bawa. Anggaran komisi Rp2.500.000, anggaran hadiah ajak warung Rp1.000.000 sebulan. Iklan FB biasanya Rp150.000 per warung baru. Oh ya, kalau reseller rekrut reseller lain, bisa dapat 1% juga nggak biar semangat?"

## Perhitungan (script)
```
$ python3 scripts/hitung_referral.py biaya --aov 1.250.000 --margin 12 --hadiah-pemberi 3% --jumlah-referral 40 --anggaran 2,5jt
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp1.250.000  |  margin kotor 12%
Laba kotor pesanan pertama      : Rp150.000 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp37.500
Hadiah/diskon teman             : Rp0
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp37.500 = 3% dari nilai pesanan, 25% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp112.500
Program 40 referral berhasil: total biaya Rp1.500.000; total laba kotor pesanan pertama Rp6.000.000; laba setelah hadiah Rp4.500.000
Anggaran Rp2.500.000: cukup (sisa Rp1.000.000)
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)

$ python3 scripts/hitung_referral.py biaya --aov 1.250.000 --margin 12 --hadiah-pemberi 25rb --hadiah-teman 25rb --anggaran 1jt --cac-iklan 150rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp1.250.000  |  margin kotor 12%
Laba kotor pesanan pertama      : Rp150.000 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp25.000
Hadiah/diskon teman             : Rp25.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp50.000 = 4% dari nilai pesanan, 33,33% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp100.000
Anggaran Rp1.000.000 cukup untuk maksimal 20 referral berhasil.
Pembanding: biaya per pelanggan baru dari iklan Rp150.000 -> referral LEBIH MURAH (selisih Rp100.000).
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)

$ python3 scripts/hitung_referral.py impas --aov 1.250.000 --margin 12 --hadiah-pemberi 25rb --hadiah-teman 25rb --frekuensi-bulan 4 --umur-bulan 12
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp150.000 (nilai pesanan Rp1.250.000, margin 12%)
Biaya per referral              : Rp50.000 (pemberi Rp25.000 + teman Rp25.000 + lain Rp0)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp150.000 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp7.200.000 (48 pesanan; asumsi 4x per bulan selama 12 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp2.160.000 total per referral
BATAS ATAS hadiah pemberi (bukan anjuran; di atas ini melewati batas aman): Rp2.135.000
Hadiah pemberi SARAN (konservatif: total hadiah maks. 50% laba pesanan pertama): Rp50.000
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)

$ python3 scripts/hitung_referral.py impas --aov 1.250.000 --margin 12 --hadiah-pemberi 5% --hadiah-teman 5% --frekuensi-bulan 4 --umur-bulan 12
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp150.000 (nilai pesanan Rp1.250.000, margin 12%)
Biaya per referral              : Rp125.000 (pemberi Rp62.500 + teman Rp62.500 + lain Rp0)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp150.000 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp7.200.000 (48 pesanan; asumsi 4x per bulan selama 12 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp2.160.000 total per referral
BATAS ATAS hadiah pemberi (bukan anjuran; di atas ini melewati batas aman): Rp2.097.500
Hadiah pemberi SARAN (konservatif: total hadiah maks. 50% laba pesanan pertama): Rp12.500
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)

$ python3 scripts/hitung_referral.py simulasi --pelanggan-aktif 180 --aov 1.250.000 --margin 12 --hadiah-pemberi 25rb --hadiah-teman 25rb --skenario hati-hati:5:1:30 --skenario realistis:10:1,5:35 --pesanan-ulang 3 --anggaran 1jt --cac-iklan 150rb
SIMULASI REFERRAL (ESTIMASI, bukan kepastian) - 180 pelanggan aktif
Biaya per referral berhasil Rp50.000; laba kotor per pesanan Rp150.000; pesanan ulang per teman baru: 3
- hati-hati: 9 perujuk -> 9 teman diajak -> 3 pembeli baru | omzet Rp15.000.000 | biaya hadiah Rp150.000 | laba kotor Rp1.800.000 | laba setelah hadiah Rp1.650.000 | ROI 1100%
- realistis: 18 perujuk -> 27 teman diajak -> 9 pembeli baru | omzet Rp45.000.000 | biaya hadiah Rp450.000 | laba kotor Rp5.400.000 | laba setelah hadiah Rp4.950.000 | ROI 1100%
Pembanding iklan: Rp150.000 per pelanggan baru -> referral lebih murah (Rp50.000 per pembeli baru).
Angka skenario adalah asumsi awal, bukan patokan pasar; ganti dengan data Anda setelah 1 bulan berjalan.
(kode keluar 0)
```
Uji tambahan angka ambigu (agent tidak menebak, bertanya ke pengguna):
```
$ python3 scripts/hitung_referral.py simulasi --pelanggan-aktif 180 --aov 1.250.000 --margin 12 --pesanan-ulang 1.000
GAGAL: pesanan ulang '1.000' ambigu: bisa dibaca 1000 atau 1,000. Untuk desimal pakai koma (mis. 1,5); untuk ribuan tulis tanpa titik (mis. 1000)
(kode keluar 2)
```

## Jawaban skill

### 1. Ringkasan
- **Program 1 - Ajak warung:** warung pengajak dapat **voucher belanja Rp25.000**, warung baru dapat **potongan Rp25.000** di belanja pertama. Biaya per referral **Rp50.000** (4% dari belanja, 33,33% dari laba kotor); laba belanja pertama tetap **Rp100.000**; **STATUS: AMAN**, lebih murah dari iklan (selisih Rp100.000). Anggaran Rp1.000.000 = **maks. 20 warung baru** per bulan.
- **Program 2 - Reseller satu tingkat:** komisi **3% = Rp37.500** per belanja warung yang dibawa (25% dari laba kotor); laba tetap **Rp112.500** per belanja. 40 belanja lewat reseller = komisi **Rp1.500.000**, anggaran Rp2.500.000 cukup (sisa Rp1.000.000).
- **Bonus 1% dari rekrutan reseller: tidak saya rancang.** Imbalan dari merekrut reseller lain (bukan dari barang yang terjual ke pembeli) masuk pola skema piramida yang dilarang UU 7/2014 tentang Perdagangan. Komisi hanya dari belanja nyata warung yang dibawa sendiri.

### 2. Asumsi
Nilai belanja, margin 12%, frekuensi 4x per bulan dari Anda. Warung bertahan 12 bulan: **asumsi**. Batas aman 30% dari laba seumur pelanggan = aturan praktis, bukan hukum. Simulasi = ESTIMASI.

### 3. Tabel angka (dari script)
| Hal | Nilai |
|---|---|
| Laba kotor per belanja warung | Rp150.000 |
| Ajak warung: biaya per referral (Rp25.000 + Rp25.000) | Rp50.000; laba belanja pertama Rp100.000 (AMAN) |
| Hadiah pengajak SARAN (konservatif) | Rp50.000 (hadiah Anda Rp25.000 sudah di bawahnya) |
| Batas atas hadiah pengajak | Rp2.135.000, **bukan anjuran** (margin tipis; angka ini besar karena warung belanja 48 kali setahun) |
| Kuota ajak warung (anggaran Rp1.000.000) | maks. 20 per bulan |
| Reseller: komisi 3% per belanja | Rp37.500; laba setelah komisi Rp112.500 |
| 40 belanja lewat reseller | komisi Rp1.500.000; anggaran Rp2.500.000 cukup (sisa Rp1.000.000) |
| Bila hadiah dinaikkan 5% + 5% | biaya Rp125.000 dari laba Rp150.000; masih AMAN, tetapi SARAN pengajak turun ke Rp12.500: **tidak disarankan** untuk margin 12% |

### 4. Aturan program
- **Warung baru** = warung yang belum pernah belanja di Berkah Jaya (cek nomor WA & alamat di buku catatan). Pengajak dan warung baru tidak boleh satu pemilik/alamat.
- Voucher pengajak cair setelah warung baru **lunas** (bukan bon/tempo) dan barang tidak diretur 7 hari. Voucher belanja, **tidak bisa diuangkan**; berlaku 60 hari; maks. 3 per pengajak per bulan; kuota 20 per bulan.
- **Reseller:** tanpa biaya daftar, tanpa target rekrut. Komisi 3% hanya dari belanja **lunas** warung yang dibawa sendiri, dibayar sebulan sekali dengan rincian nota. Tidak ada komisi dari reseller lain. Reseller tidak boleh memberi janji harga di luar daftar harga resmi.
- Data minimal: nama panggilan, nama warung, nomor WA, kode, tanggal, status hadiah/komisi (`templates/lembar-catatan-referral.csv`).

### 5. S&K ringkas (dari `templates/syarat-ketentuan.md`)
1. Program Ajak Warung berlaku untuk warung langganan (Pengajak) dan warung yang belum pernah belanja (Warung Baru).
2. Warung Baru menyebut nama/kode Pengajak saat pesan pertama. Warung Baru: potongan Rp25.000 di belanja pertama. Pengajak: voucher belanja Rp25.000 setelah belanja Warung Baru lunas dan lewat 7 hari tanpa retur.
3. Maks. 3 voucher per Pengajak per bulan; kuota 20 per bulan; voucher berlaku 60 hari; tidak bisa diuangkan.
4. Program Reseller: tanpa biaya pendaftaran; komisi 3% dari nilai belanja lunas warung yang dibawa reseller; tidak ada komisi atas perekrutan reseller lain.
5. Tidak berlaku untuk nomor/alamat yang sama, pesanan batal/retur, atau indikasi akun ganda; alasan penolakan dijelaskan.
6. Data (nama panggilan, nama warung, nomor WA, kode, status hadiah) hanya untuk program ini, tidak dibagikan, dapat dihapus atas permintaan. Balas "STOP" untuk berhenti menerima info.
7. Berkah Jaya dapat mengubah/menghentikan program dengan pemberitahuan lewat WA; hadiah dan komisi yang sudah berhak tetap dibayar.

### 6. Teks (dikirim satu per satu, bukan blast)
**WA ke warung langganan yang rutin belanja:**
> Assalamualaikum Bu Tini, terima kasih sudah langganan di Berkah Jaya. Kalau ada warung kenalan yang belum belanja di sini, boleh diajak ya: warungnya dapat potongan Rp25.000 di belanja pertama, Ibu dapat voucher belanja Rp25.000 setelah belanjaannya lunas. Cukup minta mereka WA kami dan sebut nama Ibu. Syarat lengkap balas "S&K". Tidak mau dapat info seperti ini? Balas "STOP".

**WA ke calon reseller (yang sudah menyatakan minat):**
> Bu Ani, untuk jadi reseller Berkah Jaya tidak ada biaya daftar. Ibu dapat komisi 3% dari setiap belanja lunas warung yang Ibu bawa, contohnya belanja Rp1.250.000 = komisi Rp37.500, dibayar tiap awal bulan dengan rincian nota. Komisi hanya dari belanja warung, tidak ada bonus merekrut orang.

### 7. Simulasi (ESTIMASI, bukan kepastian)
180 warung, 3 belanja ulang per warung baru: hati-hati 3 warung baru (laba setelah hadiah Rp1.650.000), realistis 9 warung baru (Rp4.950.000). Keduanya di bawah anggaran Rp1.000.000. Angka skenario adalah asumsi awal; ganti dengan data Anda setelah 1 bulan.

### 8. Langkah minggu ini
1. Kirim WA ajakan ke 15 warung yang paling rutin belanja.
2. Buat lembar catatan referral + kolom "reseller pembawa" di buku nota.
3. Tulis perjanjian reseller satu halaman (komisi 3%, tanpa biaya daftar, tanpa bonus rekrut).
4. Tanyakan "Tahu kami dari mana?" ke setiap warung baru.
5. Minggu ke-4: hitung ulang biaya per warung baru dari data nyata.

### 9. Catatan
Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda. Promo harus jelas syaratnya (UU 8/1999); data pelanggan seminimal mungkin (UU 27/2022 PDP); komisi satu tingkat dari penjualan nyata, tanpa biaya daftar dan tanpa imbalan rekrutmen (UU 7/2014). Komisi reseller bernilai besar dapat punya konsekuensi pajak; tanyakan konsultan pajak.

## Catatan penguji
- Lulus. Semua angka cocok dengan hitungan independen (Fraction): LPO Rp150.000; 3% = Rp37.500; 40 x Rp37.500 = Rp1.500.000; Rp1.000.000 / Rp50.000 = 20; LTV 48 x Rp150.000 = Rp7.200.000; batas Rp2.160.000; SARAN floor(Rp75.000) - Rp25.000 = Rp50.000 dan Rp75.000 - Rp62.500 = Rp12.500; simulasi 9/9/3 dan 18/27/9 (27 x 35% = 9,45 dibulatkan 9).
- Format Indonesia di semua argumen (`1.250.000`, `2,5jt`, `1,5` teman per perujuk) terbaca benar; `--pesanan-ulang 1.000` ditolak ambigu (kode 2), sesuai aturan "jangan menebak".
- Permintaan bonus rekrutmen 1% ditolak dengan dasar UU 7/2014 dan alternatif satu tingkat; sesuai SKILL.md.
- Catatan kecil: untuk margin tipis dan frekuensi tinggi, baris BATAS ATAS (Rp2.135.000) sangat besar dibanding laba belanja (Rp150.000); label "bukan anjuran" + baris SARAN membuat jawaban tetap aman.
