# Skenario 3 (normal 1) — Toko kopi, file Frappe Books ASLI — uji Akun B

Data: "Kopi Senja (fiktif)", dibuat oleh aplikasi Frappe Books v0.36.0 (lihat `00-pembanding-tanpa-skill.md` untuk daftar invoice).
Tambahan: Inventory diaktifkan, stok masuk lewat Stock Movement (Biji Kopi 20, Croissant 30), keluar lewat Shipment
(Biji Kopi 1 + 3), pembelian PINV-1001 (28 Agu, Rp 1.200.000, belum dibayar) & PINV-1002 (3 Sep, Rp 360.000, lunas),
jurnal sewa Rp 1.500.000 (5 Sep). Perintah dijalankan dengan `--db` ke salinan file; SHA-256 file sama sebelum/sesudah
semua perintah.

## Keluaran script vs verifikasi independen (Decimal, kode penguji sendiri)
| Perintah | Keluaran skill | Independen | Status |
|---|---|---|---|
| `penjualan --bulan 2026-09` | total Rp 564.000, belum dibayar Rp 410.000 | 564.000 / 410.000 | OK |
| `penjualan --per barang` | Biji 3 = 255.000; Kopi Susu 13 = 234.000; Americano 5 = 75.000; Croissant 0 | sama | OK |
| `penjualan --per hari` | 1 Sep 76.000; 2 Sep -22.000; 15 Sep 255.000; 30 Sep 255.000 | sama | OK (batas 00:30 & 23:45 WIB benar) |
| `pembelian --bulan 2026-09` | Rp 360.000, lunas | 360.000 | OK |
| `pembelian --dari 2026-08-01 --sampai 2026-09-30` | Rp 1.560.000, belum dibayar 1.200.000 | sama | OK |
| `piutang --hari-ini 2026-09-26` | 4 invoice Rp 525.000, semua belum jatuh tempo | 4 / 525.000 | OK |
| `utang` | PINV-1001 Rp 1.200.000, jatuh tempo 27 Sep | sama | OK |
| `stok --min 20` | Biji Kopi 16 (menipis), 1 aman | Biji 16, Croissant 30 | OK |
| `laba-rugi --bulan 2026-09` | Pendapatan 608.000; HPP 600.000; beban 1.500.000; rugi -1.492.000 | sama dari buku besar | OK terhadap buku besar, lihat catatan |
| `laporan-harian --tanggal 2026-09-01` | 1 invoice Rp 76.000; kemarin 85.000; -10,6% | 76.000; (76−85)/85 = -10,59% | OK |
| `cek` | "Fitur stok (Inventory): **tidak aktif**" | di file: `enableInventory = '1.0'` (aktif) | **SALAH** |

## Uji zona waktu (UTC → lokal) di batas hari
| Invoice (disimpan UTC) | WIB | WITA/WIT | Masuk Sep? (WIB / WITA) |
|---|---|---|---|
| 2026-08-31T16:50Z | 31 Agu 23:50 | 1 Sep 00:50 / 01:50 | tidak / ya |
| 2026-08-31T17:30Z | 1 Sep 00:30 | 1 Sep | ya / ya |
| 2026-09-30T16:45Z | 30 Sep 23:45 | 1 Okt 00:45 | ya / tidak |
| 2026-09-30T17:10Z | 1 Okt 00:10 | 1 Okt | tidak / tidak |
Skill: WIB Rp 564.000, WITA & WIT Rp 394.000 (= 564.000 − 255.000 + 85.000). Cocok. Entri buku besar di file asli disimpan
sebagai tengah malam UTC tanggal lokal (`2026-09-01T00:00:00.000Z`, lihat `LedgerPosting.timezoneDateTimeAdjuster`) — skill tetap benar untuk WIB/WITA/WIT.

## Catatan temuan dari skenario ini
1. **(sedang) `cek` salah membaca Inventory.** File asli menyimpan centang di SingleValue sebagai `'1.0'`/`'0.0'`; script hanya
   menerima `'1'`/`'true'`. Akibat: `cek` bilang tidak aktif, dan `csv-barang --lacak-stok` akan memberi peringatan palsu
   "fitur Inventory belum aktif". Fixture pembuat memakai `'1'` sehingga tidak tertangkap.
2. **(sedang) Retur: `penjualan` dan `laba-rugi` tidak sejalan.** Frappe Books v0.36.0 memposting invoice retur dengan nilai
   negatif **di sisi yang ditukar** (`SalesInvoice.getPosting`: `posting.debit(item.account, amount)` dengan amount negatif),
   sehingga di buku besar retur Rp 22.000 malah **menambah** akun Penjualan (608.000 = 564.000 + 2 × 22.000). Skill membaca buku
   besar apa adanya (sama dengan laporan P&L Frappe Books sendiri), tetapi tidak memberi tahu pengguna mengapa pendapatan di
   `laba-rugi` beda dengan `penjualan`. Fixture pembuat memodelkan retur "ideal" (mengurangi pendapatan), jadi perilaku file asli
   belum pernah diuji. Perlu minimal catatan otomatis bila ada retur di periode itu.
3. (rendah) Data uji: pembelian barang ber-stok yang diarahkan ke akun HPP + Shipment membuat HPP ganda (600.000). Ini pilihan
   data penguji, bukan kesalahan skill; skill menampilkan buku besar dengan benar.
