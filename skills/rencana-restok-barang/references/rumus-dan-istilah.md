# Rumus dan istilah (bahasa awam)

Dimuat bila perlu. Isi ini untuk agent; sampaikan ke pengguna dengan kata-kata sehari-hari. Semua angka di balasan tetap diambil dari hasil hitungan, bukan dari contoh di sini.

## 1. Istilah
| Istilah | Arti sederhana untuk pemilik toko |
|---|---|
| Laku per hari (rata-rata permintaan harian) | Rata-rata barang terjual per hari, termasuk hari yang tidak ada penjualan (dihitung 0) |
| Naik-turunnya penjualan (simpangan) | Seberapa tidak menentu penjualan harian. Makin tidak menentu, makin besar cadangan yang perlu disiapkan |
| Lead time (waktu tunggu) | Hari sejak Anda memesan sampai barang siap dijual: tunggu konfirmasi, transfer, produksi, pengiriman, cek barang |
| Tingkat layanan | Peluang barang tidak kosong selama menunggu kiriman. 95 % = dari 20 kali pesan, kira-kira 19 kali tidak sempat kosong |
| Stok pengaman (safety stock) | Cadangan untuk berjaga bila penjualan lebih ramai atau kiriman telat |
| Titik pesan ulang (reorder point) | Bila stok sudah sampai angka ini, saatnya memesan |
| Stok target | Jumlah stok (sekarang + yang dipesan) yang membuat barang cukup sampai kiriman datang ditambah 14 hari sesudahnya, plus cadangan |
| Horizon | Berapa hari stok harus cukup setelah kiriman datang (default 14 hari = kira-kira belanja dua minggu sekali) |
| Kelipatan / isi per dus | Pemasok hanya menjual per dus/pak; jumlah pesan dibulatkan ke atas ke kelipatan ini |
| Minimal order (MOQ) | Jumlah paling sedikit yang mau dilayani pemasok untuk satu barang |
| Dalam pesanan | Barang yang sudah dipesan tapi belum datang; dikurangkan dari pesanan baru |
| Barang mati | Masih ada stok tetapi tidak laku 60 hari atau lebih: modal tertahan |
| Stok berlebih | Stok cukup untuk lebih dari 90 hari: jangan ditambah dulu |

## 2. Rumus (dihitung `scripts/rencana_restok.py`, Decimal)
| Ukuran | Rumus |
|---|---|
| Deret harian | penjualan bersih per hari di rentang data; hari tanpa penjualan = 0; retur/batal mengurangi penjualan di tanggal itu lalu hari sebelumnya; pesanan berstatus batal/belum bayar/retur di ekspor marketplace tidak dihitung |
| Rata-rata μ | total terjual ÷ jumlah hari rentang |
| Simpangan sd | simpangan baku sampel (dibagi n − 1) dari deret harian. Data mingguan/bulanan: dari laju per periode × √(panjang periode); kurang dari 4 periode penuh → sd = √μ (asumsi, disebut) |
| Faktor tren | rata-rata 28 hari terakhir ÷ μ (perlu data ≥ 42 hari; mingguan ≥ 6 minggu; bulanan ≥ 3 bulan memakai bulan terakhir). ≥ 1,2 = naik, ≤ 0,8 = turun |
| Laku/hari yang dipakai | naik/turun: μ × faktor tren (dibatasi 0,5–1,5) × faktor musim; stabil: μ × faktor musim. Simpangan dikali faktor yang sama |
| z | 90 % = 1,28; 95 % = 1,65; 99 % = 2,33 (tersedia juga 80 % = 0,84; 85 % = 1,04; 97 % = 1,88; 98 % = 2,05) |
| Stok pengaman SS | z × sd × √lead time → dibulatkan ke atas |
| Titik pesan ulang ROP | laku/hari × lead time + SS → dibulatkan ke atas |
| Stok target T | laku/hari × (lead time + horizon) + SS → dibulatkan ke atas |
| Posisi stok | stok sekarang + dalam pesanan |
| Habis dalam | stok ÷ laku/hari, dibulatkan ke bawah (hari) |
| PESAN SEKARANG | posisi ≤ ROP, atau ROP tercapai kurang dari 1 hari lagi. Jumlah = T − posisi |
| PESAN MINGGU DEPAN | ROP tercapai dalam 1–7 hari (hari = (posisi − ROP) ÷ laku/hari, dibulatkan ke bawah). Jumlah = T − (posisi − laku/hari × hari) |
| AMAN | ROP tercapai lebih dari 7 hari lagi |
| Pembulatan jumlah pesan | ke atas ke bilangan bulat → naik ke minimal order → ke atas ke kelipatan kemasan |
| Nilai pesanan | jumlah × harga beli, dibulatkan ke rupiah terdekat |
| Barang mati | hari sejak terakhir terjual ≥ 60 dan stok > 0 (atau stok belum diketahui). Modal tertahan = stok × harga beli |
| Data belum cukup | rentang data < 14 hari, atau barang baru tercatat < 14 hari terakhir (tanpa tanggal mulai dijual). Jumlah pesan tidak dihitung |
| Lonjakan | hari dengan penjualan ≥ 4 × median hari laku DAN ≥ median + 10 (perlu ≥ 5 hari laku). Hanya ditandai; dihapus bila pengguna membenarkan borongan sekali |
| Tanggal | 2026-09-01, 01/09/2026 (tanggal/bulan), 1 Sep 2026, 1 September 2026, nomor seri Excel. File yang jelas bulan/tanggal (≥ 2 baris seperti 09/13/2026, tidak ada satu pun yang jelas tanggal/bulan) dibaca bulan/tanggal seluruhnya |

## 3. Contoh hitung (angka contoh, bukan data pengguna)
Kaos hitam M: laku rata-rata 4/hari, simpangan 2,2, lead time 7 hari, tingkat layanan 95 %, horizon 14 hari, stok 20, isi per dus 12.
- Stok pengaman = 1,65 × 2,2 × √7 = 9,6 → **10**
- Titik pesan ulang = 4 × 7 + 9,6 = 37,6 → **38** (stok 20 sudah di bawahnya → PESAN SEKARANG)
- Stok target = 4 × (7 + 14) + 9,6 = 93,6 → **94**
- Jumlah pesan = 94 − 20 = 74 → kelipatan 12 → **84 pcs (7 dus)**
- Habis dalam = 20 ÷ 4 = **5 hari**, padahal kiriman butuh 7 hari → sorot "bisa kosong ±2 hari sebelum barang datang".
- Dengan tingkat layanan 90 % stok pengamannya 8; dengan 99 % menjadi 14. Makin tinggi tingkat layanan, makin besar modal di stok.

## 4. Kenapa rumus ini dan batasannya
- Rumus stok pengaman di atas adalah cara umum untuk penjualan harian yang naik-turun dengan waktu tunggu tetap. Bila waktu tunggu pemasok sering meleset, pakai lead time terlama yang wajar.
- Pola masa lalu tidak tahu ada promo, barang viral, pesaing kehabisan, atau libur panjang. Karena itu hasil disebut perkiraan dan faktor musim hanya dari pengguna.
- Barang yang lakunya sangat jarang (mis. 1 per bulan) lebih baik diputuskan manual: simpan sedikit atau pesan saat ada pembeli.
