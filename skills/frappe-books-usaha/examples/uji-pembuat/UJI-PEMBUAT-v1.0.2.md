# UJI PEMBUAT v1.0.2 — bukti di Frappe Books v0.36.0 ASLI (pembuat skill, 26 Sep 2026)

Ini uji **pembuat**, bukan uji independen. Tujuannya membuktikan dua perbaikan v1.0.2 di aplikasi asli sebelum diuji ulang oleh penguji
independen. Semua nama **fiktif**; berkas kerja di scratchpad pembuat (`rt-pembuat102/`), tidak masuk repo.

## Lingkungan
- `Frappe-Books-v0.36.0-linux-x86_64.AppImage` (salinan unduhan penguji, sudah diekstrak). SHA-512 base64 dihitung ulang =
  `nFHZaPXph+L63yBvX4gQontVek2AZMDijuvPDFjQoOGQTJ4aTDxNxGNcCn/M4FcI33i01jdbhZpn8vkkqfBXmg==`, **cocok** dengan `latest-linux.yml`
  yang diunduh ulang oleh pembuat dari `github.com/frappe/books/releases/download/v0.36.0/latest-linux.yml`.
- Headless (Xvfb), `TZ=Asia/Jakarta`, HOME terpisah, proxy keluar diblokir; dikendalikan lewat Chrome DevTools Protocol lokal
  (harness penguji dipakai ulang, hanya port & HOME yang diganti).
- Perusahaan baru lewat Setup Wizard: "Toko Stok Pembuat v102 (fiktif)", Indonesia, IDR, bagan akun Indonesia; Inventory aktif; akun
  `Persediaan Toko - 1141.001` (tipe Stock) dibuat & dipasang sebagai Stock In Hand (bawaan bagan Indonesia tidak punya akun Stock
  yang bukan grup — script memberi peringatan bila Stock In Hand kosong).

## Alur
1. `csv-pelanggan` & `csv-barang` (v1.0.2, `--db` ke file asli) → Import Wizard asli lewat tombol "Select File"/"Import Data":
   Party 2/2, Item 2/2 sukses, tanpa galat. Barang berstok `Kopi Stok 250g` di file asli: `trackItem = true`,
   `expenseAccount = Stock Diterima Tapi Tidak Ditagih - 2115.000` (= `InventorySettings.stockReceivedButNotBilled`).
2. `csv-transaksi --jenis pembelian` (10 × 50.000) dan `csv-transaksi` penjualan (J-01 4 × 85.000, J-02 2 × 85.000) → Import Wizard
   asli, "Submit entries?" → No: PINV-1001, SINV-1001, SINV-1002 sukses.
3. Di aplikasi: Submit semua; Purchase Receipt dari PINV-1001 (PREC-1001); Shipment dari SINV-1001/1002 (SHPM-1001/1002); retur 1 unit
   atas SINV-1002 (SINV-1003, tanpa pembayaran).

## Buku besar asli (dibaca read-only, `reverted = 0`)
```text
PINV-1001 Stock Diterima Tapi Tidak Ditagih  D 500.000 | Hutang Dagang Dalam Negeri  K 500.000
PREC-1001 Persediaan Toko                    D 500.000 | Stock Diterima Tapi Tidak Ditagih  K 500.000
SHPM-1001 HPP Pembelian                      D 200.000 | Persediaan Toko  K 200.000
SHPM-1002 HPP Pembelian                      D 100.000 | Persediaan Toko  K 100.000
SINV-1001/1002 Piutang D 340.000/170.000 | Penjualan K 340.000/170.000
SINV-1003 (retur) Piutang K -85.000 | Penjualan D -85.000   <- tanda terbalik v0.36.0
```
HPP hanya tercatat sekali (saat Shipment). Dengan akun v1.0.1 (HPP untuk barang berstok) PINV-1001 akan men-debit HPP 500.000 lagi.

## Keluaran skill v1.0.2 pada file asli (SHA-256 file sama sebelum/sesudah)
```text
$ laba-rugi --bulan 2026-09
LABA RUGI RINGKAS - Toko Stok Pembuat v102 (fiktif)
Periode: Sep 2026 (1 Sep 2026 s.d. 30 Sep 2026), zona WIB
Pendapatan:
  Penjualan - 4110.000: Rp 425.000
Total pendapatan: Rp 425.000
Harga pokok penjualan (HPP):
  HPP Pembelian - 4210.000: Rp 300.000
LABA KOTOR: Rp 125.000
Beban:
  (tidak ada)
Total beban: Rp 0
LABA BERSIH: Rp 125.000
Catatan retur: 1 invoice retur di periode ini (SINV-1003). Frappe Books v0.36.0 mencatat retur di buku besar dengan tanda terbalik, sehingga retur justru menambah angka di buku besar. Angka di atas SUDAH DIKOREKSI (retur mengurangi pendapatan/beban), sejalan dengan perintah 'penjualan'. Menurut buku besar apa adanya (Reports > Profit And Loss Frappe Books): total pendapatan Rp 595.000, HPP Rp 300.000, beban Rp 0, laba Rp 295.000.
Ringkasan dari buku besar Frappe Books (hanya transaksi final). Bukan laporan keuangan resmi; untuk laporan lengkap buka Reports > Profit And Loss di Frappe Books.

$ piutang --hari-ini 2026-09-26
PIUTANG (pelanggan belum bayar) - Toko Stok Pembuat v102 (fiktif) (per 26 Sep 2026)
Jatuh tempo dihitung = tanggal invoice + 30 hari (Frappe Books tidak menyimpan tanggal jatuh tempo).
Belum lunas: 2 invoice, total Rp 510.000
Belum jatuh tempo: 2 invoice, Rp 510.000
  - SINV-1001 | Kedai Uji Stok | tgl 10 Sep 2026 | sisa Rp 340.000 | jatuh tempo 10 Okt 2026
  - SINV-1002 | Kedai Uji Stok | tgl 11 Sep 2026 | sisa Rp 170.000 | jatuh tempo 11 Okt 2026
Kredit retur belum dikembalikan/dipotong: 1 nota retur, total -Rp 85.000
  - SINV-1003 atas SINV-1002 | Kedai Uji Stok | tgl 12 Sep 2026 | kredit -Rp 85.000
PIUTANG BERSIH (setelah kredit retur, sama dengan saldo pihak di Frappe Books): Rp 425.000
Catatan: Frappe Books tidak otomatis memotong invoice asli saat retur; kredit ini dipakai saat pembayaran berikutnya atau dikembalikan. Tagihan per invoice di atas belum dikurangi kredit.

$ stok --semua
STOK - Toko Stok Pembuat v102 (fiktif) (semua lokasi)
MENIPIS (<= 5):
  - Kopi Stok 250g: 4 Unit
AMAN:
  (tidak ada)
```

## Verifikasi
| Besaran | Hitungan terpisah | Skill |
|---|---|---|
| Pendapatan (retur dikoreksi) | 340.000 + 170.000 − 85.000 = 425.000 | Rp 425.000 ✓ |
| HPP | 6 unit terkirim × 50.000 = 300.000 (sekali) | Rp 300.000 ✓ |
| Laba | 425.000 − 300.000 = **125.000** | LABA BERSIH Rp 125.000 ✓ (v1.0.1-style akun: rugi −375.000) |
| Saldo pelanggan Frappe (`Party.outstandingAmount`) | 425.000 (dibaca dari aplikasi) = jumlah outstanding semua invoice final | PIUTANG BERSIH Rp 425.000 ✓ |
| Stok | 10 − 4 − 2 = 4 | 4 Unit ✓ |

Retur ini tidak membuat pergerakan stok balik (tidak ada Shipment retur), sesuai data.
Uji regresi yang meniru alur ini: `tests/uji_regresi.py` test_40–42.
