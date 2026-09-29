# Pilihan Strategi Harga (untuk UMKM Indonesia)

Dimuat saat langkah 3 SKILL.md. Kerangka "harga di antara alternatif terdekat dan nilai yang dirasakan pembeli; biaya hanya lantai" diadaptasi dari skill `pricing` (coreyhaines31/marketingskills, MIT) dan `pricing-strategy` (phuryn/pm-skills, MIT), ditulis ulang untuk usaha fisik, F&B, fesyen, dan jasa di Indonesia.

## 1. Tiga angka dasar
| Angka | Artinya | Cara dapat |
|---|---|---|
| **Lantai** | Harga terendah yang masih memenuhi margin minimum setelah semua potongan | `strategi_harga.py margin --hpp X --margin <min> --biaya-persen <potongan>` |
| **Pagar** | Harga pasar untuk produk setara (terendah, median, tertinggi) | riset-harga-kompetitor, atau 3–5 harga dari pengguna |
| **Atap** | Nilai di mata pembeli: berapa biaya alternatifnya + manfaat tambahan | Tanya: "kalau tidak beli di Anda, pembeli beli di mana dan berapa? Apa yang mereka dapat lebih dari Anda?" |

Harga ideal ada di antara pagar dan atap. Jika lantai di atas pagar tertinggi: produk ini tidak bisa menang di harga, jadi menangkan di nilai (ukuran, rasa, layanan, antar cepat) atau tekan HPP.

## 2. Strategi dan kapan dipakai

### Cost-plus (HPP + margin)
- **Cocok:** pesanan custom (kue ulang tahun, seragam, katering), jasa proyek, produk baru tanpa pembanding.
- **Cara:** `margin --hpp X --margin 40`. Untuk F&B margin kotor 40–65% lazim; untuk jasa 50–70%; barang jual-beli (reseller) 15–35%. (Rentang kebiasaan pasar, bukan aturan.)
- **Bahaya:** mengabaikan nilai. Kue custom yang dipesan untuk acara penting sering bisa dihargai lebih tinggi dari cost-plus.

### Berbasis nilai
- **Cocok:** ada keunggulan nyata: resep khas, bahan premium (butter asli, tanpa pengawet), custom nama, garansi, pengiriman hari yang sama, testimoni banyak.
- **Cara:** mulai dari median pesaing, tambah "premi" 10–30% bila keunggulannya **terlihat dan dijelaskan** di listing/menu/WA. Sebutkan alasannya di kalimat jualan.
- **Uji:** tawarkan ke 10–20 pelanggan; bila hampir semua langsung setuju tanpa menawar, harga kemungkinan masih terlalu murah.

### Berbasis pesaing
- **Cocok:** produk mirip dan mudah dibandingkan (mis. roti tawar, kopi susu literan, kaos polos).
- **Cara:** pasang di sekitar median, bukan terendah. Harga termurah menarik pembeli yang paling mudah pindah.
- **Jangan:** mengikuti harga pesaing yang di bawah lantai Anda. Harga pesaing adalah data, bukan target; biaya dan skala mereka berbeda.

### Penetrasi (harga perkenalan)
- **Cocok:** produk baru di pasar ramai, ingin cepat dicoba.
- **Cara:** harga perkenalan **dengan batas jelas**: "Harga perkenalan Rp24.900 untuk 100 pembeli pertama / sampai 31 Oktober, harga normal Rp28.000". Harga normal diumumkan sejak awal.
- **Bahaya:** harga murah permanen sulit dinaikkan dan menarik pembeli yang paling sensitif harga (paling cepat pindah).

### Skimming (mulai tinggi)
- **Cocok:** produk unik/musiman/edisi terbatas (kue Lebaran edisi khusus, kolaborasi, produk viral).
- **Cara:** mulai di atas pasar untuk pembeli awal, lalu buat versi lebih kecil/sederhana yang lebih murah daripada memotong harga produk utama.

### Good-better-best (3 pilihan)
- **Cocok:** pembeli beragam daya beli; jasa dengan paket (desain, foto produk, katering).
- **Cara:** 3 pilihan; pilihan tengah dirancang paling menarik (pilihan yang Anda harap paling laku). Pilihan termahal ±1,5–2,5× tengah dan membuat tengah terlihat masuk akal. Perbedaan antar-pilihan = isi/ukuran/layanan yang jelas, bukan nama saja. Detail: `psikologi-dan-paket.md`.

### Bundling / paket hemat / hampers
- **Cocok:** menaikkan nilai belanja, menghabiskan produk lambat laku dengan produk laris, musim hampers (Lebaran, Natal, Imlek).
- **Cara:** cek dengan `bundel`. Hemat untuk pembeli 8–15% biasanya cukup menarik; margin paket tetap ≥ margin minimum.

### Tangga harga reseller/grosir/agen
- **Cocok:** ingin dijualkan orang lain (reseller WA, warung, kantin, toko oleh-oleh).
- **Cara:** `tangga`. Aturan praktis: selisih harga reseller ke eceran harus cukup untuk untung reseller (umumnya 15–30%), minimal beli naik bertahap, dan **harga eceran anjuran** ditetapkan agar reseller tidak banting harga di marketplace. **Harga eceran anjuran reseller = harga eceran toko yang berlaku**; bila harga naik bertahap, perbarui harga toko, anjuran, dan daftar harga reseller bersamaan (jangan toko Rp47.900 tetapi reseller disuruh jual Rp49.900). Untung reseller = anjuran − harga beli reseller; `tangga` menampilkannya dan memberi PERHATIAN bila ≤ 0 atau di bawah `--margin-reseller-min` (default 10%). Tulis syarat: minimal beli, cara bayar (lunas/DP), retur, wilayah.
- **Periksa:** level tertinggi (agen) tetap ≥ margin minimum Anda. Laba per unit kecil tidak apa bila volume besar dan biaya layanannya kecil (tanpa kemasan satuan, ambil sendiri).

## 3. Harga untuk kanal berbeda
- **Offline vs marketplace:** boleh berbeda. Harga marketplace biasanya lebih tinggi untuk menutup potongan (hitung dengan harga-jual-marketplace), atau harga sama tapi ongkir ditanggung pembeli.
- **Ojol/GoFood/GrabFood:** komisi besar; umumnya harga di aplikasi dinaikkan. Masukkan potongan ke `--biaya-persen`.
- **QRIS:** MDR (biaya merchant) kecil tapi tetap potongan; masukkan bila ingin teliti.

## 4. Kenaikan harga (bahan naik, UMR naik)
Urutan aman (diadaptasi dari metode rollout di sumber MIT, disesuaikan untuk pelanggan UMKM):
1. Hitung harga baru dengan `margin` dari HPP baru; cek dampak dengan `elastisitas` (volume impas = pasti; hasil per elastisitas = perkiraan).
2. Coba ke **pelanggan baru / produk baru** dulu bila memungkinkan.
3. Umumkan 1–2 minggu sebelumnya dengan alasan jujur (harga bahan naik), ucapkan terima kasih, beri kesempatan beli/pre-order harga lama terbatas.
4. Naikkan bertahap bila pelanggan sensitif (≤ 10% per langkah), atau tahan harga tapi sesuaikan ukuran **dengan terbuka** (jangan diam-diam mengecilkan isi).
5. Pelanggan reseller: beri pemberitahuan lebih lama (2–4 minggu) karena mereka perlu mengubah harga jualnya.
6. Terima bahwa sebagian kecil pelanggan paling sensitif harga akan pergi; pantau penjualan 2–4 minggu.

## 5. Uji harga sederhana (tanpa alat khusus)
- **Dua pilihan di WA:** kirim daftar harga dengan 2–3 paket ke pelanggan baru; catat pilihan 20–30 pembeli pertama.
- **Harga baru untuk pelanggan baru saja** selama 2 minggu, bandingkan jumlah order dengan 2 minggu sebelumnya (perhatikan musim/gajian).
- **Pre-order** produk baru dengan harga yang direncanakan; bila kuota penuh cepat, harga bisa dinaikkan.
- **4 pertanyaan harga** (versi sederhana metode Van Westendorp) ke 20+ pelanggan: harga berapa terasa terlalu murah sampai meragukan kualitas? murah/worth it? mulai mahal tapi masih mau? terlalu mahal sampai tidak mau beli? Rentang aman kira-kira antara jawaban "murah" dan "mulai mahal". Hasil survei kecil = petunjuk, bukan kepastian.
