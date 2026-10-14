# Mengambil data, membaca hasil, dan tindakan (untuk agent)

Sampaikan ke pengguna dengan bahasa sehari-hari. Nama menu aplikasi bisa berubah; selalu tulis "nama menunya bisa berbeda".

## 1. Dari mana data penjualan
| Sumber | Cara yang sah |
|---|---|
| Buku stok (skill buku-stok) | Ekspor mutasi: `laporan mutasi --dari <tgl> --sampai <tgl> --csv mutasi.csv` → dipakai sebagai riwayat penjualan (penjualan, batal pesanan, retur pembeli, stok terakhir, HPP terbaca otomatis). Ekspor stok: `laporan stok --csv stok.csv` → dipakai sebagai data barang (stok, HPP sebagai harga beli) |
| Marketplace | Pengguna mengunduh sendiri file pesanan dari menu ekspor pesanan di pusat penjual (rentang 1–3 bulan), lalu mengirim filenya. Status batal/belum bayar/pengembalian dilewati otomatis. **Tidak** lewat login agent, kata sandi, OTP, atau scraping |
| Aplikasi kasir | Laporan penjualan per barang per hari (atau per transaksi) → ekspor Excel/CSV |
| Buku tulis / catatan WA | Ketik atau foto ulang menjadi tabel: tanggal, barang, jumlah. Total per minggu/bulan juga bisa (hasil lebih kasar) |

Lama data: minimal 14 hari; ideal 8–12 minggu. Untuk persiapan musim, data periode yang sama tahun lalu sangat membantu.

Kolom yang dikenali (huruf besar/kecil bebas): tanggal (tanggal, tgl, date, waktu pesanan dibuat, created time, order date), barang (sku, nomor referensi sku, seller sku, kode barang, nama barang, nama produk, product name, menu; nama variasi digabung), jumlah (qty, kuantitas, quantity, jumlah, terjual), status, nomor pesanan (baris dobel dengan nomor pesanan sama dihitung sekali), dan opsional per barang: stok, lead time, harga beli/modal/hpp, pemasok/supplier, kelipatan/isi per dus, minimal order/moq, dalam pesanan, mulai dijual, satuan.

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
