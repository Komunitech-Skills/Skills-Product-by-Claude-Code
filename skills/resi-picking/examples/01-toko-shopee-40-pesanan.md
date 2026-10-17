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

## Penyegaran v1.0.5 (2026-10-17)
> Hasil, angka, dan skor uji asli di atas (v1.0.0) **tidak diubah**. File input skenario ini (`in_shopee_40.csv`, `lokasi_rak.csv`) tidak disimpan di repo, jadi skrip v1.0.5 **tidak dijalankan ulang** untuk skenario ini.

Yang kini wajib ada di balasan (SKILL.md v1.0.5, "Balasan ke pengguna - wajib memuat"): baris **Pesanan di file** dari `jumlah_pesanan_di_file`, baris **Dilewati:** yang menyebut setiap nomor pesanan + alasannya (dari `dilewati_rinci`, maks. 10 nomor di chat), dan bagian **Stok setelah dikemas** (di skenario ini: "Stok tidak dicek (tidak ada file stok)."). Dari angka uji asli di atas (40 pesanan terbaca = 34 aktif + 3 batal + 3 belum bayar, tanpa pesanan bermasalah yang dilaporkan), baris itu menjadi: "Pesanan di file: 40 (34 diproses, 3 batal, 3 belum bayar)". Nomor pesanan yang dilewati tidak tercatat di contoh ini, jadi tidak bisa ditulis di sini.

Contoh balasan v1.0.5 dari data yang ada di repo (`01-picking-dasar/`, output dibuat ulang dengan skrip v1.0.5 pada 2026-10-17), kanal chat:
```
Total: 4 pesanan aktif, 4 jenis barang, 12 pcs. Kurir: JNE 2, SiCepat 1, J&T 1.
Pesanan di file: 7 (4 diproses, 1 batal, 2 datanya bermasalah).
Dilewati: #240901A5 batal; #240901A6 jumlah 0; #240901A7 jumlah tidak terbaca. Dua yang terakhir perlu dicek di Seller Center.
Diabaikan tapi pesanannya tetap diproses: 1 baris dobel #240901A1 (dihitung sekali) dan baris Total.

Catatan pembeli (baca dulu):
- #240901A1: "Tolong dibungkus rapi ya kak"

Ambil di rak:
- A1: KAOS-HT-M Kaos Polos Pria Hitam - M x 3 pcs (2 pesanan)
- A2: KAOS-HT-L Kaos Polos Pria Hitam - L x 3 pcs (1 pesanan)
- B3: TOPI-01 Topi Bucket Krem x 1 pcs (1 pesanan)
- Lokasi belum diisi: GANTUNGAN-X Gantungan Kunci Lucu x 5 pcs (1 pesanan)

Urutan kemas per kurir:
- JNE: #240901A1 resi JX00112233 (KAOS-HT-M x2, TOPI-01 x1, ada catatan); #240901A3 resi KOSONG, cek Seller Center (KAOS-HT-M x1)
- SiCepat: #240901A2 resi SC5566778 (KAOS-HT-L x3)
- J&T: #240901A4 resi JT9988776 (GANTUNGAN-X x5)

Stok setelah dikemas:
- KAOS-HT-M: stok 3 -> 0, HABIS (minimum 10)
- GANTUNGAN-X tidak ada di file stok, stoknya tidak bisa dicek.

Balas "kirim file" bila ingin versi siap cetak dan Excel.
```
Angka dicek ulang terhadap CSV input (Decimal, 2026-10-17): aktif #A1 (2 + 1), #A2 (3), #A3 (1), #A4 (5) = 12 pcs, 4 SKU; 7 nomor pesanan = 4 + 1 batal + 2 bermasalah; stok KAOS-HT-M 3 − 3 = 0, KAOS-HT-L 20 − 3 = 17 (aman, min 10), TOPI-01 10 − 1 = 9 (aman, min 5). Semua cocok dengan `output-ringkasan.json`.

Rujukan bot Telegram asli (data yang sama, v1.0.5): `koordinasi/telegram-gelombang-A1-2026-10-17.md` — topik 1888/1889, TANPA 7,5 → DENGAN 8,5 (+1,0) **BELUM** (selisih < 1,5). Semua syarat tambahan terpenuhi; selisih kecil karena model dasar sudah kuat pada data ini. Saran di sana: "Pemetaan kolom" dibuat satu kalimat awam, tanpa pembuka proses, dan SKU yang tidak ada di daftar rak maupun stok ditulis "cek fisik di gudang".
