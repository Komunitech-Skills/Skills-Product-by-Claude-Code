# Contoh 7 (uji independen) — Ekspor CSV & impor nyata ke kas-umkm

Diuji oleh penguji independen, 26 September 2026. Menggunakan data skenario warung (10 nota, lihat contoh normal 1) di database `kas-umkm` sementara terpisah.

## Ekspor
```bash
python3 scripts/arsip.py ekspor --db data/arsip.db --bulan 09/2026 --csv nota-09-2026.csv --json
```
```json
{"ok": true, "mode": "baca", "jumlah": 10, "total_nominal": 2422500, "file_csv": "nota-09-2026.csv", ...}
```
Isi CSV (header + 2 baris contoh):
```
Tanggal;Keterangan;Masuk;Keluar;Kategori
01/09/2026;Pasar Induk;;150000;lain-lain
03/09/2026;Toko Sembako Bu Yati;;220000;beli-stok
```
Format persis sesuai yang didokumentasikan SKILL.md (`Tanggal;Keterangan;Masuk;Keluar;Kategori`), kategori sudah dipetakan lewat `PETA_KATEGORI_KAS_UMKM` (mis. `bahan-baku` → `beli-stok`, kode kategori kas-umkm yang valid).

## Impor ke `kas-umkm` (database sementara baru, terpisah dari data arsip-nota)
```bash
python3 <kas-umkm>/scripts/kas.py init --db kasdb/kas.db --nama-usaha "Warung Uji" --kas-awal 0 --mulai 01/09/2026 --ya --json
python3 <kas-umkm>/scripts/kas.py impor "nota-09-2026.csv" --db kasdb/kas.db --akun "Laci kas" --jenis-file buku-kas --json
```
Pratinjau pertama (tanpa `--ya`) berhasil membaca **10 baris**, total keluar Rp 2.422.500, dan meminta izin `--izinkan-minus` (wajar: baru diimpor pengeluaran, belum ada pemasukan penjualan pada database uji ini — bukan bug, sesuai desain kas-umkm memperingatkan saldo minus). Setelah `--izinkan-minus --ya`:
```json
{"ok": true, "jumlah_baru": 10, "keluar": 2422500}
```
Rekap `kas-umkm` bulan 09/2026 menunjukkan `keluar: 2422500`, per kategori `beli-stok: 395000` (2 baris) dan `lain-lain: 2027500` (8 baris) — **cocok persis** dengan rekap arsip-nota asal (kategori arsip-nota `bahan-baku` → `beli-stok`, kategori lain → `lain-lain`).

**Verifikasi independen:** 150000+220000+45000+1250000+80000+300000+45000+175000+95000+62500 = 2.422.500, sama di kedua sisi (arsip-nota dan kas-umkm setelah impor). CSV yang diekspor arsip-nota **benar-benar bisa diimpor apa adanya** oleh `kas-umkm impor --jenis-file buku-kas`, tanpa perlu diedit manual.

## Kesimpulan
Integrasi ekspor→impor antara `arsip-nota` dan `kas-umkm` berfungsi seperti didokumentasikan di kedua SKILL.md, terverifikasi dengan menjalankan `kas-umkm` yang sesungguhnya (bukan simulasi), pada database sementara terpisah.
