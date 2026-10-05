# Uji 02 - Toko online sepatu lokal vs brand besar (normal)

**Prompt:** "Saya jual sepatu kulit sintetis lokal di Shopee dan IG, Rp199.000-299.000. Pesaing: dua brand besar (data fiktif: Brand Besar A Rp450-700 rb, Brand Besar B Rp350-600 rb). Pelanggan bilang brand besar 'lebih terpercaya'. Bagaimana caranya menang?"

**Kepatuhan aturan marketplace:** agen tidak membuka Shopee lewat akun pengguna; tidak login. Harga pesaing dari tempelan pengguna/halaman toko resmi publik. Skill juga mengarahkan harga per produk ke `riset-harga-kompetitor` (skill ada di repo).

## Hasil (ringkas)
- Peta: langsung = toko sepatu lokal lain di Shopee; tidak langsung = brand besar (Rp450 rb+) dan sepatu thrift; pengganti = tidak beli/pakai yang lama.
- Skor (script; CSV pakai `;` dan sel kosong, keduanya ditangani): Brand Besar A 3,65 (100%), Brand Besar B 3,33 (data 90%: kecepatan kirim kosong), Kita 3,25.
- Unggul: harga +2, kecepatan kirim +1. Tertinggal: garansi/retur -2,5, desain -1,5, bahan -1.
- Aturan "pesaing raksasa" diterapkan: bukan adu skala; fokus pada apa yang tidak bisa mereka tiru: harga, kirim cepat, respons personal. Agen menolak saran "turunkan harga" tanpa cek margin (`hitung-hpp`).
- Battlecard: keberatan "brand besar lebih terpercaya" -> jawab: akui reputasi, tawarkan garansi tukar ukuran 7 hari (tindakan yang harus benar-benar dilakukan), foto asli bahan/ulasan asli; dilarang: "brand itu mahal cuma bayar merek", "produk mereka palsu".
- Tindakan: (1) kebijakan retur/tukar ukuran tertulis, (2) video unboxing asli, (3) ulasan asli lewat kartu terima kasih (tanpa imbalan yang mengharuskan bintang 5), (4) jadwal cek 1 bulan.
- Catatan etika muncul: klaim perbandingan hanya dari sumber publik bertanggal.

**Verdict:** lulus. Skill jujur soal kelemahan (garansi, desain) dan tidak menyarankan perang harga.
