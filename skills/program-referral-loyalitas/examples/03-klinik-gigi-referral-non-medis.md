# Contoh 03 - Klinik gigi: referral yang aman (usaha FIKTIF)

> Contoh buatan Komunitech dengan usaha fiktif "Klinik Gigi Sehat Dua". Angka = keluaran nyata script; margin 60% dan frekuensi kunjungan adalah asumsi. Bukan nasihat hukum atau etika profesi.

**Permintaan pengguna:** "Klinik gigi kami mau bikin program ajak teman. Kepikiran diskon 20% pembersihan karang gigi untuk pasien yang ajak teman, dan simpan nomor teman-temannya biar kami WA satu-satu. Rata-rata layanan Rp350.000, untung kotor 60%, pasien datang tiap 4 bulan."

## Yang skill lakukan
1. **Menahan dua hal** dan menjelaskan dengan sopan:
   - Diskon/insentif untuk **tindakan medis** berisiko melanggar aturan profesi dan etika iklan layanan kesehatan; tanyakan dulu ke organisasi profesi atau dinas kesehatan. Skill menyarankan hadiah **non-medis** (produk perawatan umum, paket edukasi keluarga).
   - **Mengumpulkan nomor teman** tanpa persetujuan teman itu bertentangan dengan prinsip UU PDP (data pribadi pihak ketiga). Solusi: pasien membagikan kartu/teks sendiri; teman yang menghubungi klinik lebih dulu.
2. **Menghitung** program alternatif: hadiah produk perawatan bermodal Rp20.000 untuk pengajak dan Rp20.000 untuk teman + Rp3.000 kartu/kemasan.

## Perhitungan (script)
```
$ python3 scripts/hitung_referral.py biaya --aov 350rb --margin 60 --hadiah-pemberi 20rb --hadiah-teman 20rb --biaya-lain 3rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp350.000  |  margin kotor 60%
Laba kotor pesanan pertama      : Rp210.000 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp20.000
Hadiah/diskon teman             : Rp20.000
Biaya lain per referral         : Rp3.000
BIAYA PER REFERRAL              : Rp43.000 = 12,29% dari nilai pesanan, 20,48% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp167.000
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)
```

```
$ python3 scripts/hitung_referral.py impas --aov 350rb --margin 60 --hadiah-pemberi 20rb --hadiah-teman 20rb --biaya-lain 3rb --frekuensi-bulan 0,25 --umur-bulan 24
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp210.000 (nilai pesanan Rp350.000, margin 60%)
Biaya per referral              : Rp43.000 (pemberi Rp20.000 + teman Rp20.000 + lain Rp3.000)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp210.000 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp1.260.000 (6 pesanan; asumsi 0,25x per bulan selama 24 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp378.000 total per referral
Hadiah pemberi maksimal (bila hadiah teman & biaya lain tetap): Rp355.000
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)
```


## Jawaban skill

### 1. Ringkasan
- **Program:** "Kartu Sehat Keluarga". Pasien yang mengajak teman/keluarga mendapat produk perawatan gigi umum (bukan obat) setelah temannya menyelesaikan kunjungan pertama; teman mendapat produk yang sama saat kunjungan pertama. **Tidak ada potongan tindakan medis.**
- Biaya per referral Rp43.000 (12,29% dari nilai layanan, 20,48% dari laba kotor). Laba kunjungan pertama setelah hadiah Rp167.000; balik modal langsung.
- Batas hadiah aman Rp378.000 per referral (asumsi 0,25x per bulan selama 24 bulan), status AMAN, jadi klinik masih punya ruang tanpa perlu diskon tindakan.

### 2. Aturan program
- Hadiah dihitung dari **modal** produk (Rp20.000), bukan harga jual.
- Teman = pasien baru yang belum pernah berkunjung; hadiah diberikan setelah kunjungan pertama selesai.
- Data yang dicatat: nama panggilan, nomor WA, kode, tanggal; **tanpa diagnosis, alasan kunjungan, atau rekam medis**.
- Pesan ke pasien dikirim staf satu per satu kepada pasien yang setuju dihubungi (lihat skill `pengingat-pasien-klinik` untuk pengingat kontrol).
- Jangan klaim hasil ("gigi putih pasti", "tanpa sakit"). Jangan testimoni yang menjanjikan hasil.

### 3. Teks ajakan (kartu yang dibagikan pasien)
> Klinik Gigi Sehat Dua: pemeriksaan gigi keluarga dengan dokter berizin. Sebut nama [PENGAJAK] saat mendaftar; setelah kunjungan pertama, Anda mendapat [PRODUK PERAWATAN] sebagai ucapan selamat datang. Info: [NOMOR KLINIK]. Syarat berlaku.

### 4. Catatan kepatuhan
- Tanyakan ke organisasi profesi/dinas kesehatan setempat sebelum meluncurkan (aturan promosi layanan kesehatan bervariasi). Skill ini menandai bagian ini **PERLU REVIEW** oleh pemilik klinik/tenaga medis.
- S&K memakai `templates/syarat-ketentuan.md` dengan hadiah non-medis dan klausul data pribadi.

### 5. Langkah minggu ini
1. Konsultasi singkat ke organisasi profesi tentang bentuk hadiah.
2. Siapkan 20 paket produk perawatan dan cetak kartu.
3. Isi lembar catatan (tanpa data medis).
4. Uji ke 15 pasien rutin selama 30 hari.
5. Tinjau biaya per referral (script) di akhir bulan.

Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda.
