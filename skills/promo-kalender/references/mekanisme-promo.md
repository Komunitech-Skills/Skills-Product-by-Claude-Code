# Mekanisme Promo — Kapan Dipakai & Dampaknya ke Margin

| Mekanisme | Cocok untuk | Dampak margin | Risiko | Cara input ke script |
|---|---|---|---|---|
| **Diskon %** | Menarik perhatian di halaman kampanye | Paling besar menggerus laba (setiap unit) | Pembeli menunggu promo; harga normal terasa mahal | `--diskon-persen 20` |
| **Harga promo / flash sale** | Produk pemancing (traffic) dengan kuota & jam terbatas | Besar tapi terbatas kuota | Wajib penuhi kuota & jam yang diumumkan (UU 8/1999 Ps. 12) | `--harga-promo 59.000` + `--target-unit` = kuota |
| **Potongan Rp** | Harga kecil, lebih mudah dipahami dari % | Sama dengan diskon | — | `--potongan-rp 5.000` |
| **Bundling** (3 = Rp X) | Menaikkan nilai belanja per pesanan; produk pelengkap | Lebih ringan: biaya per pesanan & ongkir dibagi ke banyak unit | Stok varian harus cukup | `--bundling "3=Rp 229.000"` |
| **Beli X gratis Y** | Produk murah/konsumsi cepat habis | Setara diskon besar (2+1 = hemat 33%) | Sering tidak terasa mahalnya bagi penjual → wajib cek | `--beli-gratis 2+1` |
| **Voucher toko** (Rp/% + min. belanja) | Mendorong belanja di atas nominal tertentu | Terkendali (ada maks. & min. belanja) | Kuota voucher harus sesuai pengumuman | `--voucher 10.000 --min-belanja 100.000` atau `--voucher 10% --maks-voucher 15.000` |
| **Gratis ongkir (subsidi penjual)** | Pembeli luar kota; produk ringan | Biaya tetap per pesanan → berat untuk produk murah | Ongkir berat/jauh bisa melebihi laba | `--subsidi-ongkir 10.000` (rata-rata per pesanan) |
| **Cashback (ditanggung penjual)** | Pelanggan setia/pembelian ulang | Seperti diskon | Aturan cashback platform berubah | `--cashback 5` |
| **Hadiah/gift with purchase** | Margin tipis, ingin terasa "lebih" tanpa diskon | Kecil (biaya hadiah) | Hadiah harus benar-benar diberikan (Ps. 13) | `--biaya-lain 2.000` |

## Aturan praktis
- Jika script memberi status **RUGI**: jangan lanjut. Tawarkan alternatif yang dihitung ulang (diskon lebih kecil, bundling, hadiah).
- Jika **TIPIS** (< batas aman, default 10%): boleh hanya untuk produk pemancing dengan kuota terbatas, dan sebutkan risikonya.
- **Program gratis ongkir/cashback dari platform** biasanya berupa potongan % tambahan: masukkan ke `--biaya-platform` (angka dari Seller Center).
- Klaim di materi promo pakai `diskon_boleh_diklaim_persen` dari script (dibulatkan ke bawah): "hemat 24%" bukan "hemat 25%" bila nyatanya 24,9%.
- "Harga normal" harus harga jual yang benar-benar berlaku sebelumnya. Menaikkan harga dulu lalu "didiskon" dilarang (UU 8/1999 Ps. 11 huruf f).
