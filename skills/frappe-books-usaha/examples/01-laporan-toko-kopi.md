# Contoh 01 — Laporan dari file Frappe Books (keluaran NYATA script)

**Konteks:** pemilik "Toko Kopi Nusantara" (usaha & semua nama **fiktif**) bertanya: *"Penjualan September berapa, siapa yang
belum bayar, stok apa yang mau habis, dan untung rugi bulan ini?"*

**Data:** database Frappe Books **tiruan** berskema v0.36.0 (dibangun `tests/data/buat_db_contoh.py`) di
`~/Documents/Frappe Books/Toko Kopi Nusantara.books.db`, sehingga script menemukannya otomatis tanpa `--db`.
Isinya sengaja memuat kasus sulit: invoice tanggal 1 Sep pukul 00.00 WIB (tersimpan `2026-08-31T17:00:00.000Z`),
1 draf, 1 invoice batal, 1 retur, barang stok minus/habis, entri beban 1 Okt 00.30 WIB (tidak boleh masuk September).
Opsi `--hari-ini 2026-09-26` hanya dipakai agar contoh bisa diulang (dalam pemakaian nyata tidak perlu).

Dijalankan 26 September 2026 dengan `frappe_books.py` 1.0.0 (Python 3, Linux). Database tidak berubah (dicek SHA-256 di uji regresi).

```text
$ python3 scripts/frappe_books.py cek
FRAPPE BOOKS TERBACA (read-only): Toko Kopi Nusantara (fiktif)
Versi data Frappe Books: 0.36.0 | Mata uang: IDR | Fitur stok (Inventory): aktif
- pelanggan/pemasok: 5
- barang/jasa: 6
- invoice penjualan: 8
- invoice pembelian: 2
- akun: 15
Struktur cocok dengan versi yang diuji (Frappe Books v0.36.0 (skema juga dicocokkan dengan cabang main 0.37.0, 20 Sep 2026)).
(kode keluar 0)

$ python3 scripts/frappe_books.py penjualan --bulan 2026-09 --hari-ini 2026-09-26
PENJUALAN - Toko Kopi Nusantara (fiktif)
Periode: Sep 2026 (1 Sep 2026 s.d. 30 Sep 2026), zona WIB
Invoice final: 4 (termasuk 1 retur) | draf belum final: 1 (tidak dihitung) | dibatalkan: 1 (tidak dihitung)
DPP / sebelum pajak : Rp 905.000
Pajak               : Rp 28.050
TOTAL               : Rp 933.050
Sudah dibayar       : Rp 450.000 | Belum dibayar: Rp 483.050
Per pelanggan (terbesar dulu):
  1. Warung Bu Sari - 1 invoice - Rp 594.350
  2. Toko Sinar Abadi - 1 invoice - Rp 188.700
  3. CV Maju Jaya - 2 invoice - Rp 150.000
Catatan: 1 draf belum di-Submit di Frappe Books; belum masuk angka di atas.
Sumber: file Frappe Books (dibaca saja). Angka dibulatkan ke rupiah terdekat untuk tampilan.
(kode keluar 0)

$ python3 scripts/frappe_books.py penjualan --bulan 2026-09 --per barang --hari-ini 2026-09-26
PENJUALAN - Toko Kopi Nusantara (fiktif)
Periode: Sep 2026 (1 Sep 2026 s.d. 30 Sep 2026), zona WIB
Invoice final: 4 (termasuk 1 retur) | draf belum final: 1 (tidak dihitung) | dibatalkan: 1 (tidak dihitung)
DPP / sebelum pajak : Rp 905.000
Pajak               : Rp 28.050
TOTAL               : Rp 933.050
Sudah dibayar       : Rp 450.000 | Belum dibayar: Rp 483.050
Per barang (nilai sebelum pajak & diskon nota, terbesar dulu):
  1. Jasa Seduh Event - 1 - Rp 500.000
  2. Kopi Arabika 250g - 3 - Rp 255.000
  3. Kopi Robusta 1kg - 1 - Rp 150.000
Catatan: 1 draf belum di-Submit di Frappe Books; belum masuk angka di atas.
Sumber: file Frappe Books (dibaca saja). Angka dibulatkan ke rupiah terdekat untuk tampilan.
(kode keluar 0)

$ python3 scripts/frappe_books.py piutang --hari-ini 2026-09-26
PIUTANG (pelanggan belum bayar) - Toko Kopi Nusantara (fiktif) (per 26 Sep 2026)
Jatuh tempo dihitung = tanggal invoice + 30 hari (Frappe Books tidak menyimpan tanggal jatuh tempo).
Belum lunas: 4 invoice, total Rp 988.250
Telat 61-90 hari: 1 invoice, Rp 150.000
  - SINV-1007 | Warung Bu Sari | tgl 1 Jun 2026 | sisa Rp 150.000 | telat 87 hari
Telat 31-60 hari: 1 invoice, Rp 355.200
  - SINV-1001 | Toko Sinar Abadi | tgl 10 Jul 2026 | sisa Rp 355.200 | telat 48 hari
Belum jatuh tempo: 2 invoice, Rp 483.050
  - SINV-1003 | Warung Bu Sari | tgl 25 Sep 2026 | sisa Rp 294.350 | jatuh tempo 25 Okt 2026
  - SINV-1004 | Toko Sinar Abadi | tgl 26 Sep 2026 | sisa Rp 188.700 | jatuh tempo 26 Okt 2026
(kode keluar 0)

$ python3 scripts/frappe_books.py stok
STOK - Toko Kopi Nusantara (fiktif) (semua lokasi)
MINUS (cek pencatatan!):
  - Filter Kertas: -1 Unit
HABIS:
  - Paper Cup 8oz: 0 Unit
MENIPIS (<= 5):
  - Kopi Robusta 1kg: 1 Unit
  - Gula Aren 1kg: 2 Kg
Aman: 1 barang (tambahkan --semua untuk melihat daftarnya).
(kode keluar 0)

$ python3 scripts/frappe_books.py laba-rugi --bulan 2026-09 --hari-ini 2026-09-26
LABA RUGI RINGKAS - Toko Kopi Nusantara (fiktif)
Periode: Sep 2026 (1 Sep 2026 s.d. 30 Sep 2026), zona WIB
Pendapatan:
  Pendapatan Service: Rp 500.000
  Penjualan: Rp 405.000
Total pendapatan: Rp 905.000
Harga pokok penjualan (HPP):
  HPP Pembelian: Rp 250.000
LABA KOTOR: Rp 655.000
Beban:
  Biaya Sewa Kantor: Rp 1.000.000
  Biaya PLN Gudang & Kantor: Rp 250.000
Total beban: Rp 1.250.000
RUGI BERSIH: -Rp 595.000
Ringkasan dari buku besar Frappe Books (hanya transaksi final). Bukan laporan keuangan resmi; untuk laporan lengkap buka Reports > Profit And Loss di Frappe Books.
(kode keluar 0)

$ python3 scripts/frappe_books.py laporan-harian --hari-ini 2026-09-26
LAPORAN HARIAN Toko Kopi Nusantara (fiktif) - 26 Sep 2026
Penjualan final: 1 invoice, Rp 188.700 (draf belum final: 1)
Dibanding kemarin (Rp 594.350): -68,3%
Piutang telat (tempo 30 hari): 2 invoice, Rp 505.200
  - SINV-1007: Rp 150.000, telat 87 hari
  - SINV-1001: Rp 355.200, telat 48 hari
Stok habis/menipis (<= 5): 4 barang: Filter Kertas (-1), Paper Cup 8oz (0), Kopi Robusta 1kg (1), Gula Aren 1kg (2)
(Tanpa nama pelanggan. Detail: minta 'piutang' atau 'penjualan' ke asisten.)
(kode keluar 0)
```

## Verifikasi angka (dihitung terpisah dari data mentah)
- Penjualan final Sep: 300.000 (SINV-1002, 1 Sep 00.00 WIB) + 594.350 (585.000 + PPN 9.350) + 188.700 (170.000 + 18.700) − 150.000 (retur) = **933.050** ✔. Draf SINV-1005 & batal SINV-1006 tidak dihitung ✔.
- Piutang SINV-1001: 10 Jul + 30 hari = 9 Agu → 26 Sep = **48 hari** telat ✔.
- Stok Kopi Arabika: 10 − 3 + 20 − 1 − 2 = **24** ✔ (masuk "Aman").
- Laba rugi Sep: pendapatan 905.000 − HPP 250.000 − beban 1.250.000 = **−595.000** ✔ (beban 999.999 tanggal 1 Okt WIB tidak ikut).

## Jawaban agent ke pemilik (ringkas)
> Penjualan September (final) **Rp 933.050**, sudah dibayar Rp 450.000, sisa Rp 483.050. Ada 1 draf yang belum di-Submit
> sehingga belum dihitung. Dua invoice sudah telat (dengan asumsi tempo 30 hari): SINV-1007 Warung Bu Sari Rp 150.000 (87 hari)
> dan SINV-1001 Toko Sinar Abadi Rp 355.200 (48 hari). Stok **Filter Kertas minus 1** (cek pencatatan), Paper Cup habis,
> Robusta & Gula Aren menipis. September **rugi Rp 595.000** karena sewa Rp 1 juta masuk bulan ini.
> *Saran:* tagih dua invoice telat minggu ini; periksa kenapa Filter Kertas minus.
