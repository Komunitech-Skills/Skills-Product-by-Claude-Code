# UJI PEMBUAT v1.0.3 — laba-rugi skill = Profit And Loss Frappe Books v0.36.0 ASLI (pembuat, 26 Sep 2026)

Uji **pembuat** (bukan uji independen) untuk temuan A di `09-uji-ulang-v102-akun-b.md`. Semua nama **fiktif**; berkas kerja di
scratchpad pembuat (`rt-pembuat103/`), tidak masuk repo.

## Lingkungan
- `Frappe-Books-v0.36.0-linux-x86_64.AppImage` (terekstrak). SHA-512 base64 `nFHZaPXph+L63yBvX4gQontVek2AZMDijuvPDFjQoOGQTJ4aTDxNxGNcCn/M4FcI33i01jdbhZpn8vkkqfBXmg==`
  cocok dengan `latest-linux.yml` yang diunduh pembuat dari `github.com/frappe/books/releases/download/v0.36.0/` (dicek di UJI-PEMBUAT-v1.0.2).
- Headless Xvfb, `TZ=Asia/Jakarta`, HOME terpisah, proxy keluar diblokir, kendali lewat Chrome DevTools Protocol lokal.
- Kode sumber tag v0.36.0: `reports/LedgerReport.ts` (Math.abs per kolom), `models/inventory/StockTransfer.ts`.

## Siklus lengkap di aplikasi asli
1. Setup Wizard: "Toko Siklus Retur v103 (fiktif)", Indonesia, IDR, bagan akun Indonesia; Inventory aktif; akun `Persediaan Toko - 1141.001`
   sebagai Stock In Hand.
2. **Impor lewat Import Wizard asli** (tombol Select File → Import Data → "Submit entries?" No) dari CSV skill v1.0.3: Party 2/2,
   Item 2/2 (barang berstok → `Stock Diterima Tapi Tidak Ditagih - 2115.000`), PurchaseInvoice PINV-1001 (10 × 50.000 + PPN; kolom
   pajak ditulis pengguna "PPN" → dicocokkan ke satu-satunya template), SalesInvoice SINV-1001 (4 × 85.000) & SINV-1002 (2 × 85.000). 0 gagal.
3. Submit → **beli→terima**: Purchase Receipt PREC-1001 → **jual→kirim**: Shipment SHPM-1001, SHPM-1002 → **retur**: SINV-1003 (1 unit
   atas SINV-1002, 20 Sep) → **retur pengiriman**: SHPM-1003 (Shipment `isReturn`, `returnAgainst = SHPM-1002`) → jurnal beban sewa 60.000.

Buku besar retur (read-only):
```text
SINV-1003 Piutang Dagang  debit 0 / credit -85.000 | Penjualan  debit -85.000 / credit 0
SHPM-1003 Persediaan Toko debit -85.000 / credit 0 | HPP Pembelian  debit 0 / credit -85.000   (dinilai harga jual)
```

## Profit And Loss BAWAAN Frappe Books (dijalankan di aplikasi: `/report/ProfitAndLoss`, 1–30 Sep 2026, Monthly)
```text
Penjualan - 4000.000                    210.000
Penjualan Barang Dagangan - 4100.000    425.000
Penjualan - 4110.000                    425.000
Harga Pokok Pembelian - 4200.000       -215.000
HPP Pembelian - 4210.000               -215.000
Total Income (Credit)                   210.000
Beban - 5000.000                         60.000
Beban Langsung - 5100.000                60.000
Biaya Kantor & Gudang - 5130.000         60.000
Biaya Sewa Kantor - 5130.013             60.000
Total Expense (Debit)                    60.000
Total Profit                            150.000
```

## Keluaran skill v1.0.3 pada file yang sama (SHA-256 file sama sebelum/sesudah)
```text
$ laba-rugi --bulan 2026-09
LABA RUGI RINGKAS - Toko Siklus Retur v103 (fiktif)
Periode: Sep 2026 (1 Sep 2026 s.d. 30 Sep 2026), zona WIB
Pendapatan:
  Penjualan - 4110.000: Rp 425.000
Total pendapatan: Rp 425.000
Harga pokok penjualan (HPP):
  HPP Pembelian - 4210.000: Rp 215.000
LABA KOTOR: Rp 210.000
Beban:
  Biaya Sewa Kantor - 5130.013: Rp 60.000
Total beban: Rp 60.000
LABA BERSIH: Rp 150.000
Catatan retur: 2 dokumen retur di periode ini (SHPM-1003, SINV-1003) sudah MENGURANGI pendapatan/HPP, sama dengan cara Profit And Loss Frappe Books membacanya.
Dihitung dari buku besar Frappe Books (hanya transaksi final) dengan cara yang sama seperti Reports > Profit And Loss, jadi totalnya semestinya sama. Bukan laporan keuangan resmi.

$ penjualan --bulan 2026-09
PENJUALAN - Toko Siklus Retur v103 (fiktif)
Periode: Sep 2026 (1 Sep 2026 s.d. 30 Sep 2026), zona WIB
Invoice final: 3 (termasuk 1 retur) | draf belum final: 0 (tidak dihitung) | dibatalkan: 0 (tidak dihitung)
DPP / sebelum pajak : Rp 425.000
Pajak               : Rp 0
TOTAL               : Rp 425.000
Terbayar (bersih)   : Rp 0 | Belum dibayar: Rp 425.000 (sudah dikurangi kredit retur -Rp 85.000)
Per pelanggan (terbesar dulu):
  1. Kedai Uji Stok - 3 invoice - Rp 425.000
Catatan: retur sudah mengurangi angka di atas. 'Belum dibayar' = sisa tagihan dikurangi kredit retur yang belum dikembalikan (sama dengan PIUTANG BERSIH di perintah 'piutang').
Sumber: file Frappe Books (dibaca saja). Angka dibulatkan ke rupiah terdekat untuk tampilan.

$ piutang --hari-ini 2026-09-26
PIUTANG (pelanggan belum bayar) - Toko Siklus Retur v103 (fiktif) (per 26 Sep 2026)
Jatuh tempo dihitung = tanggal invoice + 30 hari (Frappe Books tidak menyimpan tanggal jatuh tempo).
Belum lunas: 2 invoice, total Rp 510.000
Belum jatuh tempo: 2 invoice, Rp 510.000
  - SINV-1001 | Kedai Uji Stok | tgl 10 Sep 2026 | sisa Rp 340.000 | jatuh tempo 10 Okt 2026
  - SINV-1002 | Kedai Uji Stok | tgl 11 Sep 2026 | sisa Rp 170.000 | jatuh tempo 11 Okt 2026
Kredit retur belum dikembalikan/dipotong: 1 nota retur, total -Rp 85.000
  - SINV-1003 atas SINV-1002 | Kedai Uji Stok | tgl 20 Sep 2026 | kredit -Rp 85.000
PIUTANG BERSIH (setelah kredit retur, sama dengan saldo pihak di Frappe Books): Rp 425.000
Catatan: Frappe Books tidak otomatis memotong invoice asli saat retur; kredit ini dipakai saat pembayaran berikutnya atau dikembalikan. Tagihan per invoice di atas belum dikurangi kredit.

$ laporan-harian --tanggal 2026-09-20 --hari-ini 2026-09-26
LAPORAN HARIAN Toko Siklus Retur v103 (fiktif) - 20 Sep 2026
Penjualan final: 0 invoice, Rp 0
Retur penjualan: 1 nota, -Rp 85.000 -> penjualan bersih hari ini -Rp 85.000
Kemarin: belum ada penjualan final.
Piutang telat: tidak ada.
Stok habis/menipis (<= 5): 1 barang: Kopi Stok 250g (5)
(Tanpa nama pelanggan. Detail: minta 'piutang' atau 'penjualan' ke asisten.)

$ stok --semua
STOK - Toko Siklus Retur v103 (fiktif) (semua lokasi)
MENIPIS (<= 5):
  - Kopi Stok 250g: 5 Unit
AMAN:
  (tidak ada)
```

## Perbandingan
| Besaran | P&L Frappe | Hitungan terpisah | Skill v1.0.3 | v1.0.2 (lama) |
|---|---|---|---|---|
| Penjualan | 425.000 | 340.000 + 170.000 − 85.000 | Rp 425.000 ✓ | 425.000 |
| HPP | 215.000 | 200.000 + 100.000 − 85.000 (retur kirim) | Rp 215.000 ✓ | 385.000 (retur kirim menambah HPP) |
| Beban | 60.000 | 60.000 | Rp 60.000 ✓ | 60.000 |
| **Laba** | **150.000** | 150.000 | **Rp 150.000** ✓ | −20.000 |
| Piutang bersih | saldo pihak 425.000 | 340.000 + 170.000 − 85.000 | Rp 425.000 ✓ | sama |
| `penjualan` Belum dibayar | — | Σ outstanding 425.000 | Rp 425.000 (dikurangi kredit retur) ✓ | 510.000 |
| `laporan-harian` 20 Sep | — | hanya retur | "Retur penjualan: 1 nota, -Rp 85.000" ✓ | "Penjualan final: 1 invoice, -Rp 85.000" |

Kolom v1.0.2 dihitung ulang dari buku besar yang sama dengan aturan lama (koreksi hanya entri invoice retur).
Uji regresi yang meniru skenario penguji 09 (HPP 850.000, laba 60.000): `tests/uji_regresi.py` test_43.
