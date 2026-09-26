# Sumber nama kolom ekspor pesanan per marketplace (untuk `SINONIM_PESANAN`)

Catatan jujur untuk pembeli & penguji: mengecek nama kolom "resmi" itu sulit karena kebanyakan
Seller Center menyembunyikan detail ekspor di balik login, dan berubah-ubah tanpa pengumuman.
Daftar di bawah membedakan **VERIFIKASI** (dicek langsung ke halaman bantuan resmi platform,
dengan URL + tanggal) dari **BEST-EFFORT** (dugaan masuk akal dari forum/dokumentasi integrator
pihak ketiga, BELUM dicocokkan ke ekspor asli). Ini alasan `scripts/resi.py` **selalu** menampilkan
`pemetaan_kolom` yang terdeteksi ke pengguna sebelum daftar dipakai, dan pesan error selalu
menyebut kolom yang ada di file + flag `--kolom-...` yang persis untuk membetulkannya.

## TikTok Shop - VERIFIKASI (resmi)
Sumber: [Exporting Orders - Seller Center](https://seller-sg.tiktok.com/university/essay?knowledge_id=1955916023072514&lang=en)
(TikTok Shop Seller University, dicek 2026-09-26). Kolom yang disebutkan resmi di halaman ini:
`Order ID`, `Order Status`, `Order Substatus`, `Cancellation/Return Type`, `SKU ID`,
`Tracking ID`, `Warehouse Name`, `Delivery Option`, `Payment Method`, `Package ID`,
`Purchase Channel`, dan beberapa kolom nilai uang (di luar cakupan skill ini).

Dipakai di `SINONIM_PESANAN`: `Order ID` (no_pesanan, sudah ada sejak v1.0.0), `SKU ID` (sku,
ditambah v1.0.1), `Order Substatus` (status, ditambah v1.0.1), `Tracking ID` (resi, sudah ada).
**Tidak** dipakai: `Delivery Option` sengaja TIDAK dipetakan ke field kurir walau namanya mirip -
di dokumentasi ini artinya opsi pengiriman (mis. reguler/instan), bukan nama kurir/ekspedisi;
memetakannya ke kurir berisiko menampilkan label yang salah/menyesatkan di urutan resi.

`Order/adjustment ID` dan `SKU Reference No.` (dipakai di `examples/02-tiktok-tokopedia-gabung.md`
dan test `test_tiktok_shop_header_realistis`) **BEST-EFFORT** - varian yang dilaporkan komunitas
untuk laporan pesanan "adjustment/return" TikTok Shop, tidak disebut di halaman resmi yang berhasil
dicek. `Shipping Provider Name` dan `Buyer Message` juga **BEST-EFFORT**, disebut di dokumentasi
integrator pihak ketiga (mis. ProductsUp, OrderDesk) tapi bukan halaman resmi TikTok.

## Shopee - BEST-EFFORT
Halaman resmi yang ditemukan ([Pusat Edukasi Penjual Shopee](https://seller.shopee.co.id/edu/article/15682),
dicek 2026-09-26, dan [panduan ekspor pihak ketiga](https://ultimasolusindo.com/manual-book/pendalaman-fitur/fitur-penjualan/faktur-penjualan/import-penjualan/e-commerce/ekspor-data-penjualan-dari-e-commerce/ekspor-data-penjualan-shopee/))
menjelaskan CARA mengekspor tapi tidak mencantumkan daftar nama kolom yang muncul di file hasil
ekspor. Nama kolom Shopee ID di `SINONIM_PESANAN` (`No. Pesanan`, `Nomor Referensi SKU`, `Opsi
Pengiriman`, dst.) tetap **BEST-EFFORT** seperti v1.0.0 - berasal dari contoh yang beredar di
forum/skill `buku-stok`, sudah dipakai di `examples/01-toko-shopee-40-pesanan.md` dan cocok dengan
laporan pengguna, tapi belum ada tangkapan layar/file ekspor asli terbaru untuk dicocokkan satu-satu.

## Tokopedia - BEST-EFFORT
Halaman resmi ([Cara Mudah Memproses Pesanan](https://seller.tokopedia.com/edu/cara-proses-pesanan/),
dicek 2026-09-26) menyebut proses ekspor ("order ID, SKU ID, quantity, customer shipping details")
tapi tanpa nama kolom Excel persis. Header di `examples/02-tiktok-tokopedia-gabung.md`
(`No. Invoice`, `Kode SKU`, `Nama Barang`, `Nama Kurir`, dst.) adalah **BEST-EFFORT** - pola umum
ekspor Tokopedia berbahasa Indonesia yang dilaporkan pengguna, ditambahkan ke `SINONIM_PESANAN`
v1.0.1 (`no. invoice`, `nama barang`, dan deteksi otomatis `nama kurir` lewat perbaikan token).

## Lazada - BEST-EFFORT (belum ada pengguna Lazada yang menguji)
Tidak ditemukan halaman bantuan resmi yang mencantumkan nama kolom CSV. Sumber terdekat:
[GitHub issue field-parity Lazada (pihak ketiga)](https://github.com/nongmelt/naff-warehouse-application/issues/126)
menyebut field API `orderNumber`, `status`, `shippingProvider` (bukan nama kolom CSV export asli).
`SINONIM_PESANAN` v1.0.1 menambahkan dugaan nama kolom CSV yang wajar (`Order Number`, `Item Name`,
`Order Item Status`, `Shipping Provider`) sebagai **BEST-EFFORT** murni - tandai ke pembeli Lazada
pertama bahwa pemetaan kolom WAJIB dicek manual, dan minta contoh file ekspor asli (data pembeli
disamarkan) untuk Komunitech agar bisa dipastikan.

## Blibli - BEST-EFFORT
[Panduan ekspor pihak ketiga](https://ultimasolusindo.com/manual-book/pendalaman-fitur/fitur-penjualan/faktur-penjualan/import-penjualan/e-commerce/ekspor-data-penjualan-dari-e-commerce/ekspor-data-penjualan-blibli/)
(dicek 2026-09-26) menjelaskan cara mengunduh pesanan tapi isi halaman yang berhasil diambil TIDAK
mengonfirmasi nama kolom persis (walau ringkasan pencarian awal sempat menyebut "No Pesanan",
"Seller SKU", "Logistik" - klaim itu TIDAK bisa diverifikasi ulang langsung dari halamannya, jadi
diperlakukan sebagai dugaan, bukan fakta terverifikasi). `logistik` tetap ditambahkan ke sinonim
kurir v1.0.1 sebagai **BEST-EFFORT** murni karena istilah itu umum dipakai di ekspor gudang
Indonesia, dengan catatan jelas ini belum diverifikasi resmi.

## Kesimpulan untuk pengguna
Auto-deteksi kolom skill ini adalah **bantuan**, bukan jaminan. Selalu cek `pemetaan_kolom` di hasil
JSON sebelum memakai daftar ambil/urutan resi. Kalau salah tebak atau tidak terdeteksi, pesan error
& hasil sukses sama-sama menyebutkan kolom yang ada di file dan flag `--kolom-...` yang persis untuk
membetulkannya secara manual - tidak perlu menunggu update skill.
