# Uji ulang v1.0.2 — Skenario normal 2: header realistis TikTok Shop & Tokopedia (fokus U12)

Ini skenario yang di v1.0.0 GAGAL 0 dari 2 (temuan U12, Sedang). Diuji ulang dengan file fiktif baru
memakai header non-resmi/umum yang benar-benar dipakai penjual saat ekspor (bukan header contoh yang
sudah dites sebelumnya di `tests/uji_regresi.py`), disimpan di scratchpad.

## TikTok Shop (`Order/Adjustment ID, Tracking ID, Order Status, Shipping Provider Name, Product Name,
Seller SKU, Variation, Quantity, Buyer Message`)
```
python3 scripts/resi.py pesanan-tiktokshop.csv --json
```
`pemetaan_kolom` terpetakan **otomatis, tanpa override**: No. pesanan=Order/Adjustment ID,
No. resi=Tracking ID, Status pesanan=Order Status, Kurir=Shipping Provider Name,
Nama produk=Product Name, SKU=Seller SKU, Variasi=Variation, Jumlah=Quantity,
Catatan pembeli=Buyer Message. `kolom_ambigu: {}`.

Verifikasi independen: TT9001 (KAOS-HT-M x3, aktif), TT9002 (KAOS-HT-L x2, aktif), TT9003
(CEL-TR-XL x1, aktif), TT9004 (unpaid → dilewati). Total aktif = 3 pesanan, 3 jenis barang,
3+2+1 = **6 pcs** — cocok persis dengan `daftar-ambil.md` ("Total: 3 pesanan aktif, 3 jenis
barang, 6 pcs.").

## Tokopedia (`No. Invoice, No Resi, Status Terakhir, Jasa Kirim, Nama Barang, SKU Penjual,
Nama Variasi, Jumlah Produk Dibeli, Catatan Pembeli`)
```
python3 scripts/resi.py pesanan-tokopedia.csv --json
```
`pemetaan_kolom` terpetakan **otomatis, tanpa override**: No. pesanan=No. Invoice,
No. resi=No Resi, Status pesanan=Status Terakhir, Kurir=Jasa Kirim, Nama produk=Nama Barang,
SKU=SKU Penjual, Variasi=Nama Variasi, Jumlah=Jumlah Produk Dibeli, Catatan pembeli=Catatan
Pembeli. `kolom_ambigu: {}`.

Verifikasi independen: INV0001 (TOPI-BB-BLK x2, aktif), INV0002 (TOPI-BB-NVY x1, aktif), INV0003
(menunggu pembayaran → dilewati). Total aktif = 2 pesanan, 2 jenis barang, 2+1 = **3 pcs** — cocok
persis dengan `daftar-ambil.md`.

## Kesimpulan U12
**BERES.** Sebelumnya (v1.0.0) 0 dari 2 file ini lolos tanpa override karena sinonim pendek
("kurir", "invoice") hanya cocok persis huruf-demi-huruf dan tidak boleh cocok sebagian (ambang
minimal 8 huruf). Di v1.0.2, `deteksi_kolom` memakai pencocokan token-kata (lihat
`scripts/resi.py` fungsi `deteksi_kolom`/`_token`/`_token_sublist`): kata sinonim dicocokkan
sebagai TOKEN KATA UTUH di dalam token kolom (mis. "kurir" cocok "Jasa Kirim"? — tidak, karena
token "kurir" tidak muncul di situ; tapi memang tidak perlu, karena "jasa kirim" sendiri ada di
daftar sinonim persis). Yang relevan untuk kasus U12: "Kurir" cocok persis dengan opsi sinonim
"kurir"/"nama kurir"/dst, dan "No. Invoice"/"Invoice" cocok token "invoice". Hasil uji ulang: 2
dari 2 file header realistis TikTok Shop & Tokopedia terpetakan otomatis tanpa override — naik
dari 0/2 di v1.0.0.
