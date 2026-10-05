# 06 — Uji independen: penjualan harian (skenario normal 1)

> **Sumber keluaran:** penguji independen, 30 Sep 2026, `scripts/odoo.py` v1.0.0 terhadap **Odoo Community ASLI** yang dijalankan lokal dari image Docker resmi `odoo:18.0` (build 18.0-20260926, XML-RPC) dan `odoo:19.0` (build 19.0-20260926, JSON-2) + `postgres:16`. Data fiktif diisi penguji lewat API admin (bukan server tiruan pembuat). Kunci API dibuat untuk pengguna `bot-laporan` (Sales: User All Documents, Accounting: Read-only, Inventory: User). Path kunci disingkat.

**Permintaan pengguna:** "Penjualan hari ini di Odoo berapa?"

## Data uji (disiapkan penguji; tanggal hari ini 30 Sep 2026 WIB)
| SO | Status | date_order (UTC di Odoo) | Jam WIB | Total | Masuk "hari ini"? |
|---|---|---|---|---|---|
| S00001 | sale | 29-09 17:30:00 | 30-09 00:30 | 355.200 | Ya |
| S00002 | sale | 30-09 03:00:00 | 30-09 10:00 | 849.150 (diskon 10%) | Ya |
| S00003 | sale | 30-09 16:59:59 | 30-09 23:59:59 | 41.111,08 (harga 12.345,67) | Ya |
| S00004 | sale | 29-09 16:30:00 | 29-09 23:30 | 471.750 | Kemarin |
| S00005 | draft | 30-09 05:00 | | 22.200 | Tidak (draf) |
| S00006 | cancel | 30-09 06:00 | | 44.400 | Tidak (batal) |
| S00007 | sale | 30-09 17:00:00 | 01-10 00:00 | 94.350 | Tidak (besok) |

Faktur terposting tanggal 30-09: INV/2026/00001 Rp 355.200 dan nota kredit RINV/2026/00001 −Rp 55.500. Satu faktur draf Rp 862.470 (tidak boleh dihitung).

## Hitungan independen penguji
- Pesanan: 355.200 + 849.150 + 41.111,08 = **Rp 1.245.461,08** (3 pesanan); DPP 320.000 + 765.000 + 37.037,01 = 1.122.037,01; pajak 123.424,07.
- Kemarin 471.750 → (1.245.461,08 − 471.750) / 471.750 = **+164,0%**. Rata-rata 1.245.461,08 / 3 = 415.153,69 → **Rp 415.154**.
- Terlaris: Kopi 13 unit (3×85.000 + 10×85.000×90%) = **1.020.000**; Gula 2 → 65.000; Sirup 3 → 37.037,01.
- Faktur: 355.200 − 55.500 = **Rp 299.700** (DPP 270.000, pajak 29.700).

## Keluaran skill (Odoo 19, JSON-2; Odoo 18 XML-RPC identik baris per baris)
```
$ python3 scripts/odoo.py penjualan --rinci
RINGKASAN PENJUALAN ODOO
Rabu, 30 September 2026

PESANAN PENJUALAN TERKONFIRMASI (Sales)
Jumlah pesanan: 3
Total (termasuk pajak): Rp 1.245.461,08
Sebelum pajak Rp 1.122.037,01 | Pajak Rp 123.424,07
Kemarin: Rp 471.750 (+164,0%)
Rata-rata per pesanan: Rp 415.154
Produk terlaris (nilai sebelum pajak):
1. [KP-250] Kopi Robusta 250g: 13 unit, Rp 1.020.000
2. [GA-1] Gula Aren 1kg: 2 unit, Rp 65.000
3. [SRP-VNL] Sirup Vanila 750ml: 3 unit, Rp 37.037,01
Rincian:
- S00001 CV Maju Jaya Abadi: Rp 355.200
- S00002 Toko Berkah Sentosa: Rp 849.150
- S00003 PT Sinar Harapan Mulia: Rp 41.111,08

FAKTUR PELANGGAN DIPOSTING (Invoicing)
Faktur: 1, nota kredit: 1
Total (termasuk pajak, dikurangi nota kredit): Rp 299.700
Sebelum pajak Rp 270.000 | Pajak Rp 29.700

Pesanan dan faktur adalah dua sudut pandang yang sama; JANGAN dijumlahkan (bisa dobel).
(kode keluar: 0)
```
Tambahan: `--tanggal kemarin` → 1 pesanan Rp 471.750, faktur 2 Rp 777.000 (cocok). `--tz WITA` → 3 pesanan Rp 1.676.100 (S00004 00:30 WITA masuk, S00003 00:59 WITA besok keluar) — cocok hitungan penguji. `--protokol xmlrpc` ke Odoo 19 juga menghasilkan angka sama.

## Temuan dari skenario ini
- **Semua angka COCOK** di Odoo 18 & 19 asli. Nama field `sale.order` (`state`, `date_order`, `amount_untaxed/tax/total`, `currency_id`), `sale.order.line` (`product_uom_qty`, `price_subtotal`), `account.move` (`move_type`, `invoice_date`, `amount_*_signed`) benar. `res.users/context_get` via JSON-2 memberi uid (pengguna terbaca).
- Batas hari WIB/WITA (konversi UTC) benar di keempat kasus tepi; draf, batal, dan besok tidak terhitung.
- Saat seed awal pesanan masih berpricelist USD, skill **tidak** menjumlahkannya dan menulis `CATATAN: S00001 memakai USD ... tidak dijumlahkan` — perilaku aman yang benar.
- **TEMUAN TINGGI (lihat HASIL-UJI):** dengan kunci pengguna ber-hak *Sales: User: Own Documents* (`bot-own`), perintah yang sama mencetak `Jumlah pesanan: 0 / Rp 0` dengan kode 0 tanpa peringatan; `cek` hanya menulis "Penjualan (Sales): bisa dibaca (0 data)".
