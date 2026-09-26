# Skenario 01 — Toko Shopee, 40 pesanan, multi-SKU & multi-varian (normal)

Diuji oleh: penguji independen (Akun B), lintas akun dari pembuat skill.
Data: rekaan (bukan data toko asli), 40 pesanan Shopee (81 baris item), 8 SKU/varian,
4 kurir, termasuk 3 pesanan batal & 3 belum bayar. File lokasi rak disertakan.

## Perintah
```
python3 scripts/resi.py in_shopee_40.csv --lokasi lokasi_rak.csv --json
```

## Hasil skrip (ringkasan JSON)
- `jumlah_pesanan_total`: 40, `jumlah_pesanan_aktif`: 34
- `jumlah_sku_unik`: 8, `total_barang`: 133 pcs
- `kurir`: SiCepat 9, JNE 10, J&T Express 10, AnterAja 5 (pesanan aktif)
- `dilewati_status`: batal 3, belum bayar 3 (dikeluarkan dari daftar, tetap dilaporkan)
- `pemetaan_kolom` terdeteksi otomatis dengan benar untuk semua kolom (header ala Shopee: "Opsi
  Pengiriman", "Nomor Referensi SKU", "Nama Variasi", dst.)

## Verifikasi independen (dihitung ulang dari CSV mentah, tanpa membaca kode skrip)
Total qty per SKU+varian (hanya status "Perlu Dikirim"), dihitung dengan skrip Python terpisah:
```
CELANA-JN-32 (32)      16
CELANA-JN-34 (34)      23
JAKET-BB-L (L)         17
KAOS-HT-L (Hitam - L)  13
KAOS-HT-M (Hitam - M)  13
KAOS-PT-M (Putih - M)  19
SANDAL-42 (42)         13
TOPI-01                19
Total                 133
```
Cocok **persis** dengan `daftar-ambil.md` per SKU (13, 13, 19, 19, 16, 23, 17, 13) dan grup rak
(A1/A2/B1/C1/C2/D1) juga sesuai `lokasi_rak.csv`.

Jumlah pesanan aktif per kurir dihitung ulang dari CSV (pesanan unik, hanya "Perlu Dikirim"):
JNE 10, J&T Express 10, SiCepat 9, AnterAja 5 — cocok persis dengan `urutan-resi.md`.

## Kesimpulan skenario 01
Angka 100% akurat pada uji ini (qty per SKU, grup rak, jumlah pesanan per kurir). Pesanan batal/belum
bayar benar-benar dikeluarkan dari daftar ambil & urutan resi tapi tetap dilaporkan jumlahnya —
sesuai klaim SKILL.md.
