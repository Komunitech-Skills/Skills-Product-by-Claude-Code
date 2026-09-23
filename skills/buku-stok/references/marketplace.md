# Impor pesanan marketplace: kolom & status

Nama kolom ekspor Seller Center **bisa berubah kapan saja** dan berbeda antar-versi. Script mendeteksi kolom dengan kata kunci di bawah (cocok persis lebih diutamakan; cocok sebagian hanya untuk kata ≥ 8 huruf), lalu agent **wajib** menunjukkan pemetaannya ke pengguna. Daftar ini adalah kata kunci umum, bukan spesifikasi resmi marketplace.

| Data | Kata kunci kolom (urutan prioritas) |
|---|---|
| No. pesanan (wajib) | No. Pesanan, Nomor Pesanan, Order ID, Order Number, Nomor Invoice, Invoice |
| SKU | Nomor Referensi SKU, Seller SKU, SKU Penjual, Nomor SKU, SKU, Kode SKU, SKU Induk |
| Nama produk / varian | Nama Produk, Product Name / Nama Variasi, Variation, Varian |
| Jumlah (wajib) | Jumlah, Quantity, Qty, Jumlah Produk Dibeli |
| Status | Status Pesanan, Order Status, Status Terakhir, Status |
| No. resi | No. Resi, Nomor Resi, Tracking ID, Tracking Number, ID Pelacakan*, Kode Booking, AWB |
| Kurir | Opsi Pengiriman, Shipping Provider Name, Nama Penyedia Pengiriman*, Kurir, Jasa Kirim, Ekspedisi |
| Tanggal | Waktu Pesanan Dibuat, Created Time, Waktu Dibuat*, Tanggal Pesanan, Tanggal Pembayaran, Paid Time |
| Batas kirim | "…Harus Dikirimkan Sebelum…", Ship By, Batas Kirim |
| Harga satuan (opsional, untuk omzet) | Harga Setelah Diskon, Harga Satuan, Harga Jual, Unit Price, Harga. Kolom berisi "asli/awal/original/sebelum diskon" **tidak** dipakai (itu harga sebelum diskon) |
| Subtotal baris (opsional; dipakai bila harga satuan tidak ada: harga = subtotal ÷ jumlah) | SKU Subtotal After Discount, Subtotal SKU Setelah Diskon*, Total Harga Produk, Subtotal |
| Tanda retur (opsional, hanya peringatan) | Cancelation/Return Type, Jenis Pembatalan/Pengembalian*; Returned Quantity, Sku Quantity of return, Jumlah Pengembalian SKU* |

\* **Nama kolom TikTok Shop versi bahasa Indonesia belum dicocokkan dengan file ekspor asli** (dari uji dengan file tiruan). Saat memakai ekspor TikTok berbahasa Indonesia, periksa pemetaan dengan teliti dan betulkan dengan `--kolom-…` bila perlu. Kirimkan contoh file asli (data pembeli disamarkan) ke Komunitech agar daftar ini bisa dipastikan.

Wajib ada: No. pesanan, Jumlah, dan SKU **atau** Nama produk. Jika SKU kosong, produk dicocokkan lewat nama (+ varian) persis, hanya bila hasilnya tunggal.

## Penanganan file
- CSV (`,` `;` tab `|`), encoding UTF-8/Excel Windows, dan **XLSX** (sheet pertama) dibaca langsung. `.xls` lama ditolak.
- Baris judul boleh tidak di baris pertama (script memindai 15 baris teratas).
- Baris keterangan di bawah judul (mis. penjelasan kolom), baris kosong, dan baris dengan jumlah tidak valid dilewati & dihitung.
- Nomor pesanan rusak karena dibuka di Excel (`2.40920E+17`) dilewati + peringatan. Apostrof di depan nomor (`'2409…`) dibuang.
- Baris tanpa nomor pesanan dianggap lanjutan pesanan di atasnya (beberapa ekspor hanya menulis nomor di baris pertama).
- Baris kembar persis (pesanan + SKU + jumlah sama) dalam satu file dihitung sekali.

## Kategori status
| Kategori | Kata kunci (tidak peka huruf besar/kecil, `_` dianggap spasi) | Efek pada impor baru | Efek pada pesanan yang sudah diimpor |
|---|---|---|---|
| batal | batal, dibatalkan, cancel(l)ed, gagal, failed, expired | diabaikan | stok **dikembalikan** (sekali) sesuai HPP saat keluar; penjualannya dikeluarkan dari laporan (omzet, HPP, terlaris) |
| retur | retur, return, refund, pengembalian, dikembalikan | diabaikan | hanya dilaporkan; cek fisik lalu `masuk --jenis retur-pembeli` |
| belum bayar | belum bayar, unpaid, menunggu pembayaran, awaiting payment | diabaikan & tidak dicatat (bisa diimpor setelah dibayar) | — |
| batal diajukan | kata batal/cancel + diajukan/requested/permintaan/pengajuan/menunggu (mis. "Pembatalan Diajukan", "Cancellation requested") | stok dipotong (pesanan masih sah) + peringatan, **tidak** masuk picking | stok **tidak** diubah, status diperbarui + peringatan |
| perlu kirim | akan dikirim*, menunggu pengiriman, menunggu konfirmasi (penjual), perlu dikirim, siap dikirim, sedang dikemas, to ship, awaiting shipment/collection, diproses | stok dipotong, masuk daftar picking | status diperbarui; bila dulu batal → **stok dipotong ulang** |
| dikirim / selesai | dikirim, shipped, in transit / selesai, completed, delivered | stok dipotong, tidak masuk picking | status diperbarui |
| lainnya | status lain | stok dipotong + **peringatan** | status diperbarui |

Pengecualian: status yang mengandung "ditolak"/"rejected" (mis. "Pengembalian Ditolak") tidak dianggap batal/retur.
`--abaikan-status "kata1,kata2"` mengganti seluruh daftar batal/retur bawaan dengan daftar pengguna.

Item yang dulu diimpor dengan `--lewati-tak-dikenal` dicocokkan ulang setiap kali file berisi pesanan itu diimpor lagi; bila SKU-nya sudah didaftarkan, stoknya dipotong sekali.

Nomor pesanan adalah kunci anti-ganda: pesanan yang nomornya sudah ada di database tidak memotong stok lagi, dari file mana pun.

Stok **tidak** tersinkron otomatis ke marketplace. Setelah restock/opname, pengguna tetap memperbarui stok di Seller Center (bisa dibantu dengan `laporan stok --csv`).
