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

## 3. Fasilitas kesehatan (klinik, RS, praktik dokter/dokter gigi/bidan, apotek, lab, fisioterapi) - PERLU REVIEW tenaga medis/hukum
- **Dasar (dicek 2026-09-30):** Permenkes 1787/MENKES/PER/XII/2010 tentang Iklan dan Publikasi Pelayanan Kesehatan, Pasal 5: iklan/publikasi fasilitas pelayanan kesehatan dilarang memuat promosi penjualan **dalam bentuk apa pun**, termasuk potongan harga (diskon), imbalan atas pelayanan kesehatan, dan MLM; juga testimoni di media massa dan pujian berlebihan. Tetap berlaku lewat UU 17/2023 Pasal 453 (peraturan pelaksanaan lama berlaku sepanjang tidak bertentangan); tidak ditemukan pencabutan di PP 28/2024. Kode etik: KODEKGI (PDGI) Pasal 3 melarang dokter gigi promosi/janji agar pasien datang, termasuk diskon; KODEKI (IDI) melarang memuji diri. Sumber lengkap di catatan riset Komunitech.
- **Yang TIDAK dirancang skill:** hadiah/voucher/poin/cashback/komisi untuk pasien atau pihak lain yang merujuk pasien; diskon tindakan, obat, atau layanan kefarmasian; hadiah "non-medis" untuk pengajak (frasa "dalam bentuk apa pun" membuat ini berisiko); testimoni hasil; membagikan data pasien.
- **Alternatif patuh (tanpa imbalan untuk merujuk):**
  1. **Program edukasi:** kelas/materi kesehatan umum (mis. "cara sikat gigi anak", "persiapan kehamilan"), boleh dibagikan pasien ke keluarganya; tanpa janji hasil, tanpa promo harga.
  2. **Pengingat kontrol:** draf pesan yang dikirim staf satu per satu kepada pasien yang setuju dihubungi (skill `pengingat-pasien-klinik`); data minimal, tanpa diagnosis.
  3. **Kartu info klinik:** alamat, jam praktik, nama tenaga kesehatan berizin, layanan yang tersedia; disediakan di klinik untuk pasien sendiri, **tanpa kode dan tanpa hadiah**; bila pasien atas kemauan sendiri memberikannya ke kenalan, itu bukan program klinik. Untuk praktik dokter gigi/dokter, klinik **tidak meminta atau mendorong** pasien membagikan kartu ini (KODEKGI 2020 Pasal 3 butir 1.2.4 & Pasal 5; KODEKI Pasal 3, PERLU REVIEW).
  4. **Kartu anggota/kartu kontrol keluarga** untuk mencatat jadwal kontrol, bukan untuk poin atau potongan.
  5. **Pelayanan yang membuat pasien bercerita sendiri:** waktu tunggu jelas, penjelasan tarif di awal, tindak lanjut ramah.
- **Bila pemilik tetap ingin hadiah:** minta dulu konfirmasi **tertulis** dari dinas kesehatan setempat dan organisasi profesi; skill hanya mencatat keputusan itu, tidak mengiklankannya.
- **Toko produk umum di luar fasilitas kesehatan** (mis. toko perlengkapan bayi, kosmetik terdaftar) memakai pola ritel biasa tanpa klaim kesehatan; bila toko itu bagian dari apotek/klinik, perlakukan sebagai fasilitas kesehatan.
- **Salon/spa/barbershop tanpa tindakan medis:** pakai pola jasa (bagian 4).
- **Data:** minimal (nama panggilan, nomor WA, jadwal kontrol). Tanpa diagnosis, rekam medis, atau alasan kunjungan.

## 4. Jasa (laundry, bengkel, salon, servis AC, les)
- **Pola:** referral + paket langganan. Hadiah berupa gratis 1 kali layanan kecil atau potongan kiloan.
- **Contoh angka:** laundry Rp45.000 margin 50%, hadiah Rp5.000 + Rp5.000 -> biaya Rp10.000 (44,44% dari laba kotor); pelanggan belanja 4x per bulan selama 6 bulan -> batas hadiah aman Rp162.000. Angka itu **batas atas, bukan anjuran**; hadiah yang disarankan tetap kecil (baris "SARAN" di `impas`) karena laba satu nota hanya Rp22.500.
- **Catatan:** jasa bergantung kepercayaan; hadiah kecil + pelayanan baik lebih efektif daripada hadiah besar.

## 5. Reseller / dropship
- **Pola:** komisi satu tingkat dari **penjualan barang nyata** yang dibawa reseller; harga khusus reseller mengikuti skill `strategi-harga-produk` dan `katalog-reseller`.
- **Jangan:** biaya pendaftaran, target rekrut anggota, komisi dari hasil rekrutmen (masuk ranah skema piramida/MLM yang dilarang UU 7/2014).
- **Hitung:** komisi persen dimasukkan ke `--hadiah-pemberi 10%`; gunakan `biaya` untuk memastikan laba setelah komisi tetap sehat.
