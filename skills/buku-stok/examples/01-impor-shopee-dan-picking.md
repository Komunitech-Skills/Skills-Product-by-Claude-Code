# 01 — Potong stok dari file pesanan Shopee + daftar ambil barang

**Skenario:** S1 (normal). Seller kaos & aksesori sudah memakai buku-stok (5 produk dari `templates/daftar-produk.csv`, stok awal 1 Sep 2026). Hari ini ia mengirim file ekspor pesanan Shopee (CSV, 35 kolom bergaya ekspor Seller Center; nama/telepon/alamat pembeli fiktif). Isi file: 7 pesanan dengan status campuran (Perlu Dikirim, Batal, Belum Bayar, Selesai, Pengembalian, Dikirim), 1 baris kembar persis, dan 1 baris yang nomor pesanannya rusak (`2.60923E+17`) karena file sempat dibuka di Excel.

**Input pengguna (persis):**
> Ini file pesanan Shopee hari ini (shopee-hari1.csv), potong stoknya dan buatkan daftar ambil barang ya

**Perintah yang dijalankan agent (sesuai SKILL.md bagian C–D):**
```bash
python3 scripts/stok.py impor-pesanan shopee-hari1.csv --json          # pratinjau
python3 scripts/stok.py impor-pesanan shopee-hari1.csv --ya --json     # setelah pengguna menjawab "ya"
python3 scripts/stok.py picking --json
```

## Output

**Balasan agent 1 (pratinjau, belum disimpan):**
```
Saya akan mencatat (belum disimpan):

Kolom yang saya pakai dari file Shopee (mohon dicek):
- No. pesanan  <- No. Pesanan
- SKU          <- Nomor Referensi SKU
- Jumlah       <- Jumlah
- Status       <- Status Pesanan
- No. resi     <- No. Resi   | Kurir <- Opsi Pengiriman
- Batas kirim  <- Pesanan Harus Dikirimkan Sebelum (Menghindari keterlambatan)
- Harga        <- Harga Setelah Diskon

Pesanan baru yang memotong stok: 4
Tidak dihitung: 1 batal, 1 pengembalian, 1 belum bayar

Stok yang akan berkurang (total 9 barang):
- KAOS-PT-M Kaos Putih M: -3 (stok 30 -> 27)
- KAOS-HT-M Kaos Hitam M: -2 (stok 24 -> 22)
- KAOS-HT-L Kaos Hitam L: -2 (stok 18 -> 16)
- TOTE-NAT Tote Bag Natural: -1 (stok 40 -> 39)
- MUG-KRM Mug Putih: -1 (stok 12 -> 11)

Catatan:
- 1 baris kembar (pesanan + SKU + jumlah sama) hanya dihitung sekali.
- 1 baris nomor pesanannya rusak (tampil seperti 2,6E+17 karena file dibuka di Excel) dan
  TIDAK diproses. Mohon ekspor ulang dari Seller Center tanpa membuka/menyimpan di Excel,
  lalu kirim lagi — pesanan yang sudah tercatat tidak akan terpotong dua kali.

Simpan? Balas "ya" untuk menyimpan.
```

**Pengguna:** ya

**Balasan agent 2 (tersimpan + picking):**
```
Sudah tersimpan. Backup sebelum perubahan:
~/KomunitechData/backup-stok/stok-20260923-180744-sebelum-impor-pesanan.db

DAFTAR AMBIL BARANG — 2 pesanan, 6 barang

A. Ambil di rak (urut lokasi)
[Rak A1]  [ ] KAOS-HT-M  Kaos Polos Cotton 30s - Hitam M  x 2 pcs (1 pesanan)
[Rak A2]  [ ] KAOS-PT-M  Kaos Polos Cotton 30s - Putih M  x 3 pcs (1 pesanan)
[Rak B1]  [ ] TOTE-NAT   Tote Bag Kanvas - Natural        x 1 pcs (1 pesanan)

B. Urutan kemas / tempel resi (urut kurir)
  1. [ ] 2609230002CD | J&T Express  | resi JX0000000022    | KAOS-PT-M x3
  2. [ ] 2609230001AB | SPX Standard | resi SPXID0000000011 | KAOS-HT-M x2; TOTE-NAT x1

Pesanan "Selesai" dan "Dikirim" tetap memotong stok tetapi tidak masuk daftar ambil
(barangnya sudah keluar). Mau saya buatkan file Excel-nya (ambil.csv & urutan.csv)?
Setelah semua dikemas, bilang "sudah dikemas semua" supaya daftar ini dikosongkan.
```

## Catatan penguji
- Angka diverifikasi manual terhadap isi file: pesanan sah 0001AB (HT-M 2, TOTE 1), 0002CD (PT-M 3, baris kembar dihitung sekali), 0005IJ Selesai (MUG 1), 0007MN Dikirim (HT-L 2) = 9 barang. Batal/Belum Bayar/Pengembalian dilewati. Cocok 100%.
- Pratinjau benar-benar tidak menyimpan: checksum md5 file DB sama persis sebelum & sesudah pratinjau.
- Impor ulang file yang sama → "Pesanan baru: 0 | sudah pernah diimpor: 4" (anti ganda bekerja).
- Hari berikutnya (file XLSX): pesanan 0002CD berubah "Batal" → stok PT-M dikembalikan +3; 0004GH yang kemarin "Belum Bayar" kini dibayar → terpotong sebagai pesanan baru; 0007MN berubah "Pengembalian" → hanya dilaporkan (tidak menambah stok). Semua sesuai `references/marketplace.md`.
- Kurang: data pribadi pembeli tidak pernah tampil di output (bagus), tetapi agent perlu disiplin tidak menempelkan isi file ke chat — ini hanya dijaga oleh instruksi.
