# 08 - Skenario normal 3: jasa les privat, referral orang tua (usaha FIKTIF)

> Uji independen Tahap 6 (2026-09-30). Angka dari `scripts/hitung_referral.py`, diverifikasi ulang secara independen.

**Permintaan pengguna:** "Saya punya les privat SD-SMP 'Bimbel Cerdas Pagi', SPP Rp1,2 juta per bulan, margin sekitar 50% setelah bayar tutor. Murid aktif 60. Mau bikin program referral buat orang tua: yang ngajak dapat potongan SPP Rp100rb, murid baru gratis biaya pendaftaran Rp150rb. Iklan FB sekarang habis Rp350rb per murid baru. Anggaran Rp1,5jt/bulan. Rata-rata murid bertahan 8 bulan."

## Perhitungan (script)
```
$ python3 scripts/hitung_referral.py biaya --aov 1,2jt --margin 50 --hadiah-pemberi 100rb --hadiah-teman 150rb --cac-iklan 350rb --anggaran 1,5jt
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp1.200.000  |  margin kotor 50%
Laba kotor pesanan pertama      : Rp600.000 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp100.000
Hadiah/diskon teman             : Rp150.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp250.000 = 20,83% dari nilai pesanan, 41,67% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp350.000
Anggaran Rp1.500.000 cukup untuk maksimal 6 referral berhasil.
Pembanding: biaya per pelanggan baru dari iklan Rp350.000 -> referral LEBIH MURAH (selisih Rp100.000).
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)

$ python3 scripts/hitung_referral.py impas --aov 1,2jt --margin 50 --hadiah-pemberi 100rb --hadiah-teman 150rb --frekuensi-bulan 1 --umur-bulan 8
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp600.000 (nilai pesanan Rp1.200.000, margin 50%)
Biaya per referral              : Rp250.000 (pemberi Rp100.000 + teman Rp150.000 + lain Rp0)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp600.000 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp4.800.000 (8 pesanan; asumsi 1x per bulan selama 8 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp1.440.000 total per referral
Hadiah pemberi maksimal (bila hadiah teman & biaya lain tetap): Rp1.290.000
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)

$ python3 scripts/hitung_referral.py simulasi --pelanggan-aktif 60 --aov 1,2jt --margin 50 --hadiah-pemberi 100rb --hadiah-teman 150rb --skenario hati-hati:10:1:30 --skenario realistis:20:1:40 --pesanan-ulang 5 --anggaran 1,5jt --cac-iklan 350rb
SIMULASI REFERRAL (ESTIMASI, bukan kepastian) - 60 pelanggan aktif
Biaya per referral berhasil Rp250.000; laba kotor per pesanan Rp600.000; pesanan ulang per teman baru: 5
- hati-hati: 6 perujuk -> 6 teman diajak -> 2 pembeli baru | omzet Rp14.400.000 | biaya hadiah Rp500.000 | laba kotor Rp7.200.000 | laba setelah hadiah Rp6.700.000 | ROI 1340%
- realistis: 12 perujuk -> 12 teman diajak -> 5 pembeli baru | omzet Rp36.000.000 | biaya hadiah Rp1.250.000 | laba kotor Rp18.000.000 | laba setelah hadiah Rp16.750.000 | ROI 1340%
Pembanding iklan: Rp350.000 per pelanggan baru -> referral lebih murah (Rp250.000 per pembeli baru).
Angka skenario adalah asumsi awal, bukan patokan pasar; ganti dengan data Anda setelah 1 bulan berjalan.
(kode keluar 0)

```

## Jawaban skill

### 1. Ringkasan
- **Program:** referral dua sisi untuk orang tua. Orang tua pengajak dapat **potongan SPP Rp100.000** bulan berikutnya; murid baru **bebas biaya pendaftaran Rp150.000**.
- **Aman:** biaya per referral **Rp250.000** (20,83% dari SPP bulan pertama, 41,67% dari laba kotor); laba bulan pertama tetap **Rp350.000**; lebih murah dari iklan Rp350.000 (selisih Rp100.000).
- Anggaran Rp1.500.000 cukup untuk **maksimal 6 murid baru lewat referral per bulan**.

### 2. Asumsi
Margin 50% dari pengguna. Murid bayar 1x per bulan selama 8 bulan (dari pengguna). Biaya pendaftaran yang dibebaskan dihitung sebagai hadiah penuh Rp150.000 (pendapatan yang dilepas). Batas aman 30% = aturan praktis.

### 3. Tabel angka (dari script)
| Hal | Nilai |
|---|---|
| Laba kotor per bulan per murid | Rp600.000 |
| Biaya per referral | Rp250.000 |
| Laba bulan pertama setelah hadiah | Rp350.000 |
| Batas hadiah aman per referral | Rp1.440.000 (AMAN) |
| Kuota dengan anggaran Rp1.500.000 | maks 6 per bulan |
| Simulasi ESTIMASI (60 murid, 5 bulan ulang) | hati-hati 2 murid baru, laba setelah hadiah Rp6.700.000; realistis 5 murid baru, Rp16.750.000 |

Batas aman Rp1.440.000 **bukan saran menaikkan hadiah**; hadiah sekarang sudah cukup menarik untuk orang tua dan menyisakan ruang bila ada murid yang berhenti lebih cepat.

### 4. Aturan program
- Hadiah pengajak diberikan setelah murid baru **menyelesaikan 1 bulan pertama dan membayar SPP bulan ke-2** (mencegah daftar lalu keluar).
- Maks. 3 potongan per orang tua per bulan; potongan tidak bisa diuangkan.
- Murid baru = belum pernah terdaftar dalam 12 bulan terakhir; saudara kandung murid aktif **tidak** dihitung referral (atur sebagai diskon saudara terpisah bila mau).
- **Data anak:** catat hanya nama panggilan orang tua, nomor WA orang tua, kode, tanggal, status hadiah. Jangan mencatat nilai rapor, sekolah, atau data anak yang tidak perlu untuk program; data anak butuh persetujuan orang tua (UU 27/2022 PDP).
- Orang tua pengajak yang membagikan info ke kenalannya sendiri; bimbel **tidak meminta nomor** orang tua lain.

### 5. S&K ringkas (dari template)
Orang tua murid aktif (Pengajak) yang mengajak keluarga lain yang belum pernah mendaftar (Murid Baru). Murid Baru bebas biaya pendaftaran Rp150.000. Pengajak mendapat potongan SPP Rp100.000 setelah Murid Baru membayar SPP bulan ke-2. Maks. 3 potongan per bulan; kuota 6 per bulan; tidak bisa diuangkan. Data hanya untuk program ini, tidak dibagikan, dapat dihapus atas permintaan. Program dapat diubah/dihentikan dengan pemberitahuan di grup/WA; hadiah yang sudah berhak tetap diberikan.

### 6. Teks ajakan
**WA ke orang tua, dikirim satu per satu setelah laporan perkembangan bagus:**
> Selamat sore Bu Rina, terima kasih sudah mempercayakan Dimas di Bimbel Cerdas Pagi. Senang nilai matematikanya naik bulan ini. Kalau ada keluarga atau teman yang sedang mencari les, boleh dibagikan: murid baru bebas biaya pendaftaran Rp150.000, dan Ibu mendapat potongan SPP Rp100.000 setelah murid baru berjalan 1 bulan. Cukup minta mereka menghubungi kami dan menyebut nama Ibu. Bila tidak berkenan menerima info seperti ini, balas "STOP".

**Teks siap diteruskan orang tua:**
> Anakku les di Bimbel Cerdas Pagi, tutornya sabar. Kalau mau coba, chat [KONTAK] dan sebut namaku (Rina), pendaftarannya gratis.

(Tidak menjanjikan kenaikan nilai; testimoni hanya dari pengalaman nyata orang tua.)

### 7. Langkah minggu ini
1. Kirim ke 10 orang tua yang anaknya menunjukkan kemajuan nyata.
2. Tambah pertanyaan "Tahu kami dari mana?" di formulir pendaftaran.
3. Buat lembar catatan referral (tanpa data anak selain yang perlu).
4. Pasang kuota 6 per bulan sesuai anggaran.
5. Minggu ke-4: bandingkan biaya per murid dari referral vs iklan FB.

### 8. Catatan
Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda. Potongan SPP bukan uang tunai; untuk komisi tunai bernilai besar tanyakan konsultan pajak.

## Catatan penguji
- Semua angka cocok. Skill tidak secara eksplisit menyebut **data anak** (UU PDP Pasal 25 soal persetujuan orang tua); jawaban di atas menambahkannya dari pengetahuan penguji. Temuan rendah: tambahkan satu baris di `pola-per-usaha.md` bagian jasa/les.
- Output `impas` menampilkan "Hadiah pemberi maksimal Rp1.290.000"; untuk pembeli awam angka ini bisa dibaca sebagai saran. Agent perlu menjelaskan bahwa itu batas atas, bukan anjuran (dilakukan di atas). Temuan rendah.
