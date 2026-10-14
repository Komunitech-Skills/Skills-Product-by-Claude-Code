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
| Rata-rata seluruh data | total terjual ÷ jumlah hari rentang |
| Simpangan | simpangan baku sampel (dibagi n − 1) dari deret harian. Data mingguan/bulanan: dari laju per periode × √(panjang periode); kurang dari 4 periode penuh → simpangan = √rata-rata (asumsi, disebut) |
| Faktor tren | laju 28 hari terakhir ÷ laju sampai 56 hari sebelumnya (perlu data ≥ 42 hari). Mingguan: 4 minggu terakhir ÷ sampai 8 minggu sebelumnya (≥ 6 minggu). Bulanan: bulan terakhir ÷ sampai 2 bulan sebelumnya (≥ 3 bulan). ≥ 1,2 = naik, ≤ 0,8 = turun, selain itu stabil |
| Laku/hari yang dipakai | naik/turun: laju 4 minggu terakhir, tetapi paling banyak 2× dan paling sedikit 0,5× rata-rata seluruh data (batas disebut hanya bila benar-benar terpakai; selain itu kalimat tren berbunyi "tidak kena batas"); stabil: rata-rata seluruh data. Lalu × faktor musim. Simpangan dikali perbandingan yang sama (laku/hari dipakai ÷ rata-rata seluruh data) |
| z | 90 % = 1,28; 95 % = 1,65; 99 % = 2,33 (tersedia juga 80 % = 0,84; 85 % = 1,04; 97 % = 1,88; 98 % = 2,05) |
| Stok pengaman SS | z × sd × √lead time → dibulatkan ke atas |
| Titik pesan ulang ROP | laku/hari × lead time + SS → dibulatkan ke atas |
| Stok target T | laku/hari × (lead time + horizon) + SS → dibulatkan ke atas |
| Posisi stok | stok sekarang + dalam pesanan |
| Habis dalam | stok ÷ laku/hari, dibulatkan ke bawah (hari). Hasil bagi dirapikan ke 12 desimal sebelum dibulatkan, sehingga kelipatan tepat (mis. 260 ÷ 52/28 = 140) tidak menjadi 139. Bila laju dibatasi, ditampilkan juga hari habis dengan laju 4 minggu terakhir, dan penanda "akan kosong" memakai yang lebih cepat habis |
| Akan kosong sebelum barang datang | stok ÷ laku/hari < lead time → kosong ±(lead time − stok ÷ laku/hari) hari, dibulatkan ke atas. Barang "data belum cukup" memakai laju sementara (terjual ÷ hari tercatat) |
| PESAN SEKARANG | posisi ≤ ROP, atau ROP tercapai kurang dari 1 hari lagi. Jumlah = T − posisi |
| PESAN MINGGU DEPAN | ROP tercapai dalam 1–7 hari (hari = (posisi − ROP) ÷ laku/hari, dibulatkan ke bawah). Jumlah = T − (posisi − laku/hari × hari) |
| AMAN | ROP tercapai lebih dari 7 hari lagi |
| Pembulatan jumlah pesan | ke atas ke bilangan bulat → naik ke minimal order → ke atas ke kelipatan kemasan |
| Nilai pesanan | jumlah × harga beli, dibulatkan ke rupiah terdekat |
| Barang mati | hari sejak terakhir terjual ≥ 60 dan stok > 0 (atau stok belum diketahui). Modal tertahan = stok × harga beli |
| Data belum cukup | rentang data < 14 hari, atau barang baru tercatat < 14 hari terakhir (tanpa tanggal mulai dijual). Jumlah pesan tidak dihitung |
| Lonjakan | hari dengan penjualan > rata-rata + 3 simpangan DAN ≥ 4 × median hari laku DAN ≥ median + 8 (perlu ≥ 5 hari laku). Ditandai; hasil tanpa lonjakan (hari itu diganti median) dihitung sebagai pembanding; dihapus dari hitungan hanya bila pengguna membenarkan promo/borongan sekali |
| Pencocokan nama | huruf besar/kecil, tanda kurung, tanda baca, dan spasi ganda diabaikan ("Kaos Kaki Bayi (isi 3)" = "kaos kaki bayi isi 3"); SKU juga tanpa tanda baca/spasi. Nama yang hanya mirip (kata satu memuat kata lainnya atau kemiripan ≥ 85 %, dengan angka dan ukuran S/M/L sama) → "mungkin barang yang sama", ditanyakan, tidak disebut barang mati |
| Per hari/minggu/bulan | dideteksi otomatis bila `--data-per` tidak diberikan: judul kolom Minggu/Mgg/Pekan/Week → minggu, Bulan/Bln/Month → bulan; tanggal hanya bulan → bulan; jarak antar tanggal ada yang 1 hari → hari, semua kelipatan 7 dengan median 7 → minggu, median 28–31 hari → bulan, semua < 7 hari → hari. Judul dan jarak bertentangan, satu tanggal saja, atau jarak tidak konsisten → berhenti (kode 3), tanyakan ke pengguna |
| Tanggal | 2026-09-01, 01/09/2026 (tanggal/bulan), 1 Sep 2026, 1 September 2026, nomor seri Excel. File yang jelas bulan/tanggal (≥ 2 baris seperti 09/13/2026, tidak ada satu pun yang jelas tanggal/bulan) dibaca bulan/tanggal seluruhnya |

## 3. Contoh hitung (angka contoh, bukan data pengguna)
Kaos hitam M: laku rata-rata 4/hari, simpangan 2,2, lead time 7 hari, tingkat layanan 95 %, horizon 14 hari, stok 20, isi per dus 12.
- Stok pengaman = 1,65 × 2,2 × √7 = 9,6 → **10**
- Titik pesan ulang = 4 × 7 + 9,6 = 37,6 → **38** (stok 20 sudah di bawahnya → PESAN SEKARANG)
- Stok target = 4 × (7 + 14) + 9,6 = 93,6 → **94**
- Jumlah pesan = 94 − 20 = 74 → kelipatan 12 → **84 pcs (7 dus)**
- Habis dalam = 20 ÷ 4 = **5 hari**, padahal kiriman butuh 7 hari → **akan kosong ±2 hari** (7 − 5) sebelum barang datang; ditulis paling atas.
- Tren: bila 4 minggu terakhir laku 5/hari dan 8 minggu sebelumnya 4/hari → naik 25 % → dipakai 5/hari (bukan rata-rata 90 hari).
- Dengan tingkat layanan 90 % stok pengamannya 8; dengan 99 % menjadi 14. Makin tinggi tingkat layanan, makin besar modal di stok.

## 4. Kenapa rumus ini dan batasannya
- Rumus stok pengaman di atas adalah cara umum untuk penjualan harian yang naik-turun dengan waktu tunggu tetap. Bila waktu tunggu pemasok sering meleset, pakai lead time terlama yang wajar.
- Pola masa lalu tidak tahu ada promo, barang viral, pesaing kehabisan, atau libur panjang. Karena itu hasil disebut perkiraan dan faktor musim hanya dari pengguna.
- Barang yang lakunya sangat jarang (mis. 1 per bulan) lebih baik diputuskan manual: simpan sedikit atau pesan saat ada pembeli.
