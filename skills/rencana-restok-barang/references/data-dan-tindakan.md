# Mengambil data, membaca hasil, dan tindakan (untuk agent)

Sampaikan ke pengguna dengan bahasa sehari-hari. Nama menu aplikasi bisa berubah; selalu tulis "nama menunya bisa berbeda".

## 1. Dari mana data penjualan
| Sumber | Cara yang sah |
|---|---|
| Buku stok (skill buku-stok) | Ekspor mutasi: `laporan mutasi --dari <tgl> --sampai <tgl> --csv mutasi.csv` → dipakai sebagai riwayat penjualan (penjualan, batal pesanan, retur pembeli, stok terakhir, HPP terbaca otomatis). Ekspor stok: `laporan stok --csv stok.csv` → dipakai sebagai data barang (stok, HPP sebagai harga beli) |
| Marketplace | Pengguna mengunduh sendiri file pesanan dari menu ekspor pesanan di pusat penjual (rentang 1–3 bulan), lalu mengirim filenya. Status batal/belum bayar/pengembalian dilewati otomatis. **Tidak** lewat login agent, kata sandi, OTP, atau scraping. Nama kolom berbeda per platform (lihat §1a); **stok tidak ada di file pesanan** dan diambil dari file produk terpisah |
| Aplikasi kasir | Laporan penjualan per barang per hari (atau per transaksi) → ekspor Excel/CSV |
| Buku tulis / catatan WA | Ketik atau foto ulang menjadi tabel: tanggal, barang, jumlah. Total per minggu/bulan juga bisa (hasil lebih kasar) |

Lama data: minimal 14 hari; ideal 8–12 minggu. Untuk persiapan musim, data periode yang sama tahun lalu sangat membantu.

Kolom yang dikenali (huruf besar/kecil bebas): tanggal (tanggal, tgl, date, waktu pesanan dibuat, created time, order date), barang (sku, nomor referensi sku, seller sku, sku id, kode barang, nama barang, nama produk, product name, menu; nama variasi/variation digabung), jumlah (qty, kuantitas, quantity, jumlah, terjual), status (status pesanan, order status), nomor pesanan (no. pesanan, order id; baris dobel dengan nomor pesanan sama dihitung sekali), dan opsional per barang: stok, lead time, harga beli/modal/hpp, pemasok/supplier, kelipatan/isi per dus, minimal order/moq, dalam pesanan, mulai dijual, satuan.

### 1a. Kolom ekspor per platform (dicocokkan ke pusat bantuan penjual, diakses 14 Okt 2026)
Nama menu dan kolom bisa bergeser sewaktu-waktu; bila judul kolom di file pengguna berbeda, baca kolom yang maknanya sama dan sebut di asumsi. Jangan menganggap satu platform memakai nama kolom platform lain.

| Platform | File | Kolom yang dipakai untuk restok | Catatan |
|---|---|---|---|
| Shopee | Ekspor **Pesanan** (Pesanan Saya → Export; nama menu bisa bergeser) | No. Pesanan, Status Pesanan, Waktu Pesanan Dibuat, Nomor Referensi SKU, Nama Produk, Nama Variasi, Jumlah | File memuat **dua** kolom SKU: «SKU Induk» (kode per produk) dan «Nomor Referensi SKU» (kode per variasi). Restok dihitung per variasi → pakai Nomor Referensi SKU; bila kosong, pakai Nama Produk + Nama Variasi |
| Shopee | **Stok**: template Mass Update bagian «Informasi Penjualan» (Produk Saya → Mass Update), **bukan** file pesanan | Kolom stok per variasi + identitas variasi (kode/nama variasi) | Judul kolom persis mengikuti template terbaru; jangan mengarang daftar kolom tanpa melihat file pengguna. Salin stok + kode/nama variasi ke tabel data barang (sku, nama barang, stok) |
| Tokopedia / TikTok Shop (Seller Centre) | **Export Orders** (Manage Orders → Export Orders; nama menu bisa bergeser) | Order ID, Order Status, SKU ID, Product Name, Variation, Quantity | Judul kolom berbahasa **Inggris**. Jangan mengasumsikan ada kolom «SKU Induk» seperti di Shopee; kode barang = SKU ID. «Seller SKU» (kode buatan penjual) disebut sumber pihak ketiga ada di data pesanan: **PERLU REVIEW** apakah selalu ada di ekspor terbaru; bila ada, kolom itu yang dipakai sebagai kode barang. Kolom waktu pesanan (yang dikenali mis. «Created Time», «Paid Time») tidak disebut di sumber yang dicek: baca dari file pengguna |
| Tokopedia / TikTok Shop | **Stok**: dari kelola produk / ekspor katalog produk, **bukan** file pesanan (file pesanan hanya berisi jumlah terjual) | Kolom stok per SKU/variasi + kode atau nama produk dan variasi | Cocokkan dengan kode yang sama dengan file pesanan (SKU ID atau Seller SKU), atau dengan nama produk + variasi |

Sumber (diakses 2026-10-14):
- Shopee, filter & nomor pesanan: https://seller.shopee.co.id/edu/article/15486
- Shopee, SKU Induk (kode per produk): https://seller.shopee.co.id/edu/article/16726
- Shopee, ubah stok lewat Mass Update (Informasi Penjualan) dan kolom stok per variasi di Mass Upload: https://seller.shopee.co.id/edu/article/6944 , https://seller.shopee.co.id/edu/article/1944
- Tokopedia/TikTok Shop Seller Centre, dimensi Order ID, Order Status, SKU ID, Quantity: https://seller-id.tokopedia.com/university/essay?knowledge_id=4494325455079170&lang=id
- Tokopedia/TikTok Shop Seller Centre, isi spreadsheet Export Orders (Order ID, SKU ID, Product Name, Variation, Quantity): https://seller-id.tokopedia.com/university/essay?knowledge_id=3659692639586050
- Daftar lengkap kolom file ekspor pesanan Shopee (Status Pesanan, Waktu Pesanan Dibuat, Nomor Referensi SKU, Nama Variasi, Jumlah) tidak dimuat di halaman bantuan resmi; dicocokkan dengan ringkasan kolom pihak ketiga (https://ngulikdata.com/blog/laporan-penjualan-shopee) dan contoh file uji.
- «Seller SKU» Tokopedia: hanya sumber pihak ketiga (https://rekapcepat.id/blog/perbedaan-data-transaksi-settlement-data-order-pesanan) → PERLU REVIEW.

## 2. Menentukan lead time dan tingkat layanan bersama pengguna
- Lead time = hari dari "saya kirim pesanan" sampai "barang siap dijual" (konfirmasi, bayar, produksi, kirim, cek). Bila sering meleset, pakai yang terlama yang wajar. "2–3 hari" dihitung 3 hari.
- Tingkat layanan: 90 % untuk barang pelengkap atau yang mudah dicari gantinya; 95 % (default) untuk barang biasa; 99 % untuk barang laris utama yang membuat pembeli datang. Makin tinggi, makin besar stok pengaman dan modal yang tertahan.

## 3. Musim dan faktor musim (jangan menebak angka)
Momen yang sering mengubah penjualan di Indonesia: Ramadan dan Lebaran, tahun ajaran baru (sekitar Juli), tanggal kembar dan Harbolnas di marketplace (mis. 11.11, 12.12), Natal dan tahun baru, tanggal gajian (akhir/awal bulan), musim hujan. Arah dan besarnya berbeda tiap jenis barang. Faktor musim hanya dipakai bila pengguna menyebut angkanya atau memberi data tahun lalu: faktor = rata-rata laku/hari pada periode itu tahun lalu ÷ rata-rata laku/hari pada bulan biasa tahun lalu. Tanpa itu, tanyakan sebagai satu dari maksimal 3 pertanyaan.

## 4. Barang mati dan stok berlebih: pilihan tindakan
Pilih 1–2 yang paling cocok per barang, sebut modal tertahannya, dan jangan sarankan pesan ulang.
1. **Paket bundling** dengan barang terlaris (daftar terlaris tersedia di hasil hitungan), mis. "beli kaos hitam + topi hemat Rp10.000".
2. **Diskon bertahap**, mis. 10 % → 20 % → 30 % tiap dua minggu. Sebut harga modalnya agar pengguna sadar bila menjual di bawah modal; keputusan di tangan pengguna.
3. **Tanya retur atau tukar ke pemasok** (sebagian pemasok mau menukar dengan barang yang laku). Draf WA di `templates/pesan-wa-pemasok.md`.
4. **Jual ke reseller, grosir, atau obral** untuk mengembalikan modal lebih cepat.
5. **Hadiah pembelian minimum** atau bonus untuk pelanggan setia.
6. **Perbaiki tampilan**: foto ulang, judul produk, pindah ke rak depan, sebelum memutuskan diskon besar.
Stok berlebih (> 90 hari): hentikan pesan dulu, promo ringan, dan alihkan modal ke barang yang sering habis.

## 5. Bila barang akan kosong sebelum kiriman datang
Jumlah hari kosong dihitung (stok ÷ laku/hari dibanding lead time), termasuk untuk barang baru dengan laju sementara. Tulis paling atas di balasan, lalu beri pilihan: pesan hari ini (barang data pendek: pesanan kecil, misalnya satu dus atau minimal order, tanpa jumlah pasti), pesan sebagian ke pemasok yang lebih dekat/cepat walau sedikit lebih mahal, minta kiriman dipercepat (draf WA), batasi jumlah per pembeli, atau tandai pre-order/stok menyusul **bila aturan platform mengizinkan** (pengguna yang mengecek aturannya).

## 6. Data pribadi
File ekspor marketplace sering memuat nama, nomor HP, dan alamat pembeli. Itu tidak diperlukan untuk rencana restok: jangan dikutip, diringkas, atau disimpan di balasan.
