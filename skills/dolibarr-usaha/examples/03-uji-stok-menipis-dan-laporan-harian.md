# 03 (uji independen) — Stok menipis + laporan harian (untuk jadwal Telegram pemilik)

**Penguji:** agent independen, 2026-09-24, Dolibarr **24.0.1 asli** (data sama dengan 01–02). 7 produk barang + 1 jasa; stok diisi lewat `stockmovements` (termasuk stok minus).

## Permintaan
> "Stok apa yang mau habis?" lalu "Kirim laporan harian Dolibarr."

## `stok --menipis`
```
STOK PRODUK (menipis/habis)
Minus 1 | habis 1 | menipis 2 | dari 7 produk barang
- KRM-40 Keramik 40x40 (dus): stok -2 (min 10) MINUS -> beli 12
- PKU-7 Paku 7cm (1kg): stok 0 (min 10) HABIS -> beli 30
- CAT-5 Cat Tembok Putih 5kg: stok 3 (min 5) MENIPIS -> beli 9
- SMN-40 Semen Tiga Roda 40kg: stok 25 (min 40) MENIPIS -> beli 95
Catatan: 1 produk belum punya batas stok minimum di Dolibarr, jadi tidak bisa dinilai menipis.
```
Verifikasi dari `llx_product` (stock, seuil_stock_alerte, desiredstock): SMN 25/40/120 → menipis, beli 120−25=95 ✅; CAT 3/5/12 → 9 ✅; PKU NULL(0)/10/30 → habis, 30 ✅; KRM −2/10/0 → minus, target = min 10 → 12 ✅; PSR 6/6 → aman (6 < 6 salah, sama aturan Dolibarr) ✅; PIP tanpa min → catatan ✅; jasa JSA-ANT tidak dihitung ✅. `stok semen` → 1 produk ✅.
Kosmetik: `stok` (tanpa `--menipis`) menulis "PSR-1 … stok 6 (min 6) aman -> beli 4" (status aman tapi ada saran beli ke stok ideal).

## `laporan-harian` (24/9)
```
LAPORAN HARIAN DOLIBARR
Kamis, 24 September 2026
Dibuat 2026-09-24 21:08 WIB

PENJUALAN (invoice tervalidasi bertanggal ini)
Total (termasuk PPN): Rp 1.764.317,25
DPP Rp 1.589.475 | PPN Rp 174.842,25
Invoice: 2
Belum dibayar dari penjualan ini: Rp 1.625.567,25
vs kemarin: Rp 230.325 -> naik 666,0%

PIUTANG
Belum lunas: 8 invoice, Rp 18.968.192,16
Terlambat: 5 invoice, Rp 17.032.379,91
- IN2606-0001 sisa Rp 4.971.874,91, lewat 91 hari
- IN2606-0009 sisa Rp 75.480, lewat 90 hari
- IN2608-0002 sisa Rp 324.475, lewat 40 hari

STOK
Perlu perhatian: 4 dari 7 produk
- KRM-40 Keramik 40x40 (dus): stok -2 MINUS
- PKU-7 Paku 7cm (1kg): stok 0 HABIS
- CAT-5 Cat Tembok Putih 5kg: stok 3 MENIPIS
- SMN-40 Semen Tiga Roda 40kg: stok 25 MENIPIS

PERLU PERHATIAN
1. 2 draf invoice bertanggal hari ini belum divalidasi (belum dihitung sebagai penjualan).
2. Ada 5 invoice terlambat. Rincian & nama pelanggan: perintah `piutang`.

Sumber: Dolibarr http://127.0.0.1:8098/dolibarr (hanya dibaca).
```
Tanpa nama pelanggan ✅ (cocok untuk Telegram pemilik).

### Verifikasi (SQL `GROUP BY datef, fk_statut`)
| Besaran | SQL/penguji | Script |
|---|---|---|
| 24/9 statut 1 (1.625.567,25) + statut 2 lunas (138.750) | 1.764.317,25 | ✅ |
| DPP 1.464.475 + 125.000 | 1.589.475 | ✅ |
| PPN 161.092,25 + 13.750 | 174.842,25 | ✅ |
| Draf 24/9 (PROV8, PROV11) | 2 | ✅ |
| Kemarin 23/9 | 230.325 | ✅ |
| (1.764.317,25 − 230.325) / 230.325 × 100 | 666,012 → 666,0% | ✅ |
| Terlambat 5 invoice | 17.032.379,91 | ✅ |
`--tanggal kemarin`: penjualan 230.325, "vs kemarin Rp 0 (persen tidak dihitung)" ✅. Catatan kosmetik: bagian PIUTANG pada laporan tanggal lampau memakai kondisi **saat ini** (termasuk invoice bertanggal 24/9) dengan umur dihitung ke 23/9; tidak diberi label.

## Ketahanan per bagian (galat)
| Kondisi | Hasil |
|---|---|
| Modul **Stok** dimatikan (`unActivateModule('modStock')`) | ❌ `stok` dan laporan: **"Minus 0 \| habis 7"**, semua produk "stok 0 HABIS -> beli 120/30/…". API produk tetap menjawab dengan stok kosong; script menganggapnya 0 (dolibarr.py:927-937). Pemilik menerima alarm palsu setiap malam + saran beli yang salah → cacat **S1** |
| Modul **API** dimatikan | Laporan tetap keluar, tiap bagian "Tidak bisa dibaca: Modul 'API …' belum aktif", **kode keluar 0** (jadwal OpenClaw akan tampil `status: ok`) → R5 |

**Hasil skenario: LULUS pada konfigurasi normal** (angka 100% cocok); S1 harus diperbaiki.
