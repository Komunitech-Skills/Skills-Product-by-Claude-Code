# Daftar Ambil Barang (Picking)

Sumber pesanan: `input-pesanan.csv` (10 baris dibaca, encoding utf-8-sig)
Lokasi rak: dipakai (4 SKU terdaftar)
Cek stok: dipakai (dibandingkan dengan file stok yang diberikan)

**Total: 4 pesanan aktif, 4 jenis barang, 12 pcs.**

## Pesanan dengan catatan khusus (baca dulu sebelum packing)
- Pesanan #240901A1: "Tolong dibungkus rapi ya kak"

## Ambil di rak

### A1
- [ ] **KAOS-HT-M** Kaos Polos Pria - Hitam - M x 3 pcs (2 pesanan)

### A2
- [ ] **KAOS-HT-L** Kaos Polos Pria - Hitam - L x 3 pcs (1 pesanan)

### B3
- [ ] **TOPI-01** Topi Bucket - Krem x 1 pcs (1 pesanan)

### (lokasi belum diisi)
- [ ] **GANTUNGAN-X** Gantungan Kunci Lucu x 5 pcs (1 pesanan)  _(SKU tidak ada di file stok)_

## Peringatan
- SKU tidak ada di file stok (input-stok-buku-stok.csv): GANTUNGAN-X. Kemungkinan salah ketik atau produk baru.
- 1 baris 'jumlah tidak terbaca' dilewati (baris 9).
- 1 baris 'jumlah nol atau negatif' dilewati (baris 8).
- 1 baris 'baris duplikat' dilewati (baris 10).
- 1 baris 'baris ringkasan diabaikan' dilewati (baris 11).
- 1 pesanan tanpa nomor resi (lihat kelompok '(Resi belum ada)' di urutan-resi).
- Pesanan dilewati karena status: batal (1). Tidak masuk daftar ambil/urutan resi.
