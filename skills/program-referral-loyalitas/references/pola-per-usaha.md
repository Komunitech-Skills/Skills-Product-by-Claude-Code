# Pola Program per Jenis Usaha

Semua usaha di bawah fiktif; angka di kolom "hasil script" berasal dari `scripts/hitung_referral.py` (lihat `examples/`). Margin dan frekuensi adalah asumsi.

## 1. Toko online / fesyen (mis. hijab, tas, skincare)
- **Pola:** referral dua sisi. Teman dapat voucher belanja pertama; perujuk dapat voucher/saldo setelah pesanan teman selesai (lewat masa retur).
- **Momen:** barang diterima dan cocok; setelah ulasan bintang 5.
- **Contoh angka:** pesanan Rp180.000, margin 40%, hadiah Rp15.000 + Rp15.000 -> biaya Rp30.000, laba pesanan pertama Rp42.000, balik modal di pesanan pertama; lebih murah dari iklan Rp45.000 per pelanggan baru.
- **Marketplace (Shopee, Tokopedia, TikTok Shop dsb.):** ikuti aturan platform; kartu ucapan dalam paket boleh, tetapi jangan mengajak pindah transaksi ke luar platform bila dilarang. Voucher toko dari platform dapat dipakai bila tersedia.

## 2. Kafe / warung / F&B
- **Pola:** poin atau kartu stempel (mis. beli 8 gratis 1) + "traktir teman" (teman dapat 1 minuman gratis saat pertama datang bersama perujuk).
- **Kartu stempel:** hitung hadiah dengan **modal (HPP) minuman**, bukan harga jual. Poin lebih mudah dihitung ke script.
- **Contoh angka:** tiap belanja Rp10.000 = 1 poin, 1 poin = Rp300 -> hadiah 3% dari belanja = 4,62% dari margin 65%; poin beredar 30.000 -> liability maksimal Rp9.000.000.
- **Bahaya:** hadiah poin sebesar margin atau lebih membuat rugi tiap penukaran. Contoh: margin 30%, tiap belanja Rp10.000 = 1 poin, 1 poin = Rp3.000 -> hadiah 30% dari belanja = 100% margin, status RUGI. Sisihkan juga dana untuk poin yang beredar (liability).

## 3. Klinik / perawatan
- **Pola:** referral **non-medis dan edukatif**: hadiah produk perawatan umum bermodal rendah, atau "paket edukasi keluarga". Tambah pengingat kontrol yang dikirim staf satu per satu (lihat skill `pengingat-pasien-klinik`).
- **Jangan:** diskon/insentif untuk tindakan medis, resep, atau obat; testimoni klinis yang menjanjikan hasil; membagikan data pasien. Tanyakan organisasi profesi atau dinas kesehatan sebelum meluncurkan.
- **Data:** minimal (nama panggilan, nomor WA, kode). Tanpa diagnosis, rekam medis, atau alasan kunjungan.
- **Contoh angka:** layanan Rp350.000 margin 60%, hadiah produk bermodal Rp20.000 + Rp20.000 + biaya kartu Rp3.000 -> biaya Rp43.000 (20,48% dari laba kotor).

## 4. Jasa (laundry, bengkel, salon, servis AC, les)
- **Pola:** referral + paket langganan. Hadiah berupa gratis 1 kali layanan kecil atau potongan kiloan.
- **Contoh angka:** laundry Rp45.000 margin 50%, hadiah Rp5.000 + Rp5.000 -> biaya Rp10.000 (44,44% dari laba kotor); pelanggan belanja 4x per bulan selama 6 bulan -> batas hadiah aman Rp162.000, jadi masih ada ruang untuk hadiah lebih menarik.
- **Catatan:** jasa bergantung kepercayaan; hadiah kecil + pelayanan baik lebih efektif daripada hadiah besar.

## 5. Reseller / dropship
- **Pola:** komisi satu tingkat dari **penjualan barang nyata** yang dibawa reseller; harga khusus reseller mengikuti skill `strategi-harga-produk` dan `katalog-reseller`.
- **Jangan:** biaya pendaftaran, target rekrut anggota, komisi dari hasil rekrutmen (masuk ranah skema piramida/MLM yang dilarang UU 7/2014).
- **Hitung:** komisi persen dimasukkan ke `--hadiah-pemberi 10%`; gunakan `biaya` untuk memastikan laba setelah komisi tetap sehat.
