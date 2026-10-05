# Urutan Kemas / Tempel Resi

Sumber pesanan: `input-pesanan.csv`. Dikelompokkan per kurir, diurutkan per nomor resi dalam tiap kurir.

**Total: 4 pesanan, 3 kurir.**

## JNE (2 pesanan)
1. [ ] Pesanan #240901A1 | Resi JX00112233 | KAOS-HT-M x2; TOPI-01 x1 | CATATAN: "Tolong dibungkus rapi ya kak"
2. [ ] Pesanan #240901A3 | Resi (KOSONG - cek Seller Center) | KAOS-HT-M x1

## SiCepat (1 pesanan)
1. [ ] Pesanan #240901A2 | Resi SC5566778 | KAOS-HT-L x3

## J&T (1 pesanan)
1. [ ] Pesanan #240901A4 | Resi JT9988776 | GANTUNGAN-X x5

## Peringatan
- SKU tidak ada di file stok (input-stok-buku-stok.csv): GANTUNGAN-X. Kemungkinan salah ketik atau produk baru.
- 1 baris 'jumlah tidak terbaca' dilewati (baris 9).
- 1 baris 'jumlah nol atau negatif' dilewati (baris 8).
- 1 baris 'baris duplikat' dilewati (baris 10).
- 1 baris 'baris ringkasan diabaikan' dilewati (baris 11).
- 1 pesanan tanpa nomor resi (lihat kelompok '(Resi belum ada)' di urutan-resi).
- Pesanan dilewati karena status: batal (1). Tidak masuk daftar ambil/urutan resi.
