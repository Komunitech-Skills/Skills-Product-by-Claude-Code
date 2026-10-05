# 07 — Uji independen: piutang, umur piutang, laporan harian Telegram (skenario normal 2)

> **Sumber keluaran:** penguji independen, 30 Sep 2026, Odoo Community ASLI 18.0 (XML-RPC) & 19.0 (JSON-2) lokal (Docker resmi), data fiktif penguji. Keluaran 18 dan 19 identik (`diff` kosong).

**Permintaan pengguna:** "Siapa yang belum bayar? Umur piutangnya gimana?" lalu "Kirim laporan harian ke Telegram saya."

## Data faktur (per 30-09-2026)
| Faktur | Status | Jatuh tempo | Total | Sisa | Hari lewat (hitung penguji) | Kelompok |
|---|---|---|---|---|---|---|
| INV/00001 | posted, not_paid | 30-09 | 355.200 | 355.200 | 0 | belum jatuh tempo |
| INV/00009 | posted, not_paid | 29-10 | 444.000 | 444.000 | −29 | belum jatuh tempo |
| INV/00007 | posted, not_paid | 10-10 | 111.000 | 111.000 | −10 | belum jatuh tempo |
| INV/00002 | posted, partial (bayar 500.000) | 15-09 | 1.110.000 | 610.000 | 15 | 1–30 |
| INV/00003 | posted, not_paid | 31-08 | 222.000 | 222.000 | 30 | 1–30 (batas) |
| INV/00004 | posted, not_paid | 30-08 | 111.000 | 111.000 | 31 | 31–60 (batas) |
| INV/00005 | posted, not_paid | 02-07 | 555.000 | 555.000 | 90 | 61–90 (batas) |
| INV/00006 | posted, not_paid | 01-07 | 999.000 | 999.000 | 91 | >90 (batas) |
| INV/00008 | posted, **paid** | 29-10 | 333.000 | 0 | – | tidak dihitung |
| (draf) | draft | 30-09 | 862.470 | – | – | tidak dihitung |
| RINV/00001 | nota kredit posted | – | −55.500 | −55.500 | – | catatan terpisah |

Hitungan penguji: 8 faktur **Rp 3.407.200**; lewat jatuh tempo 5 faktur **Rp 2.497.000**; bucket: belum JT 3/910.200, 1–30 2/832.000, 31–60 1/111.000, 61–90 1/555.000, >90 1/999.000.

## Keluaran skill
```
$ python3 scripts/odoo.py piutang
PIUTANG PELANGGAN ODOO (per Rabu, 30 September 2026)
Belum lunas: 8 faktur, Rp 3.407.200
Lewat jatuh tempo: 5 faktur, Rp 2.497.000

UMUR PIUTANG (dari tanggal jatuh tempo)
- belum jatuh tempo: 3 faktur, Rp 910.200
- 1-30 hari: 2 faktur, Rp 832.000
- 31-60 hari: 1 faktur, Rp 111.000
- 61-90 hari: 1 faktur, Rp 555.000
- >90 hari: 1 faktur, Rp 999.000

PELANGGAN TERBESAR
- CV Maju Jaya Abadi: Rp 1.354.200 (2 faktur, terlama lewat 91 hari)
- Toko Berkah Sentosa: Rp 1.054.000 (2 faktur, terlama lewat 15 hari)
- PT Sinar Harapan Mulia: Rp 777.000 (2 faktur, terlama lewat 90 hari)
- Ibu Ratna Dewi: Rp 222.000 (2 faktur, terlama lewat 31 hari)

RINCIAN (terlama dulu, maks. 30)
- INV/2026/00006 CV Maju Jaya Abadi: sisa Rp 999.000 | tempo 2026-07-01 | lewat 91 hari
- INV/2026/00005 PT Sinar Harapan Mulia: sisa Rp 555.000 | tempo 2026-07-02 | lewat 90 hari
- INV/2026/00004 Ibu Ratna Dewi: sisa Rp 111.000 | tempo 2026-08-30 | lewat 31 hari
- INV/2026/00003 PT Sinar Harapan Mulia: sisa Rp 222.000 | tempo 2026-08-31 | lewat 30 hari
- INV/2026/00002 Toko Berkah Sentosa: sisa Rp 610.000 (dibayar sebagian) | tempo 2026-09-15 | lewat 15 hari
- INV/2026/00001 CV Maju Jaya Abadi: sisa Rp 355.200 | tempo 2026-09-30 | jatuh tempo hari ini
- INV/2026/00007 Ibu Ratna Dewi: sisa Rp 111.000 | tempo 2026-10-10 | jatuh tempo 10 hari lagi
- INV/2026/00009 Toko Berkah Sentosa: sisa Rp 444.000 | tempo 2026-10-29 | jatuh tempo 29 hari lagi
CATATAN: ada 1 nota kredit belum dipakai, Rp 55.500; piutang bersih bisa lebih kecil.
Status bayar = kondisi SAAT INI di Odoo. Faktur draf tidak dihitung.
(kode keluar: 0)
```
`--per-tanggal 2026-10-31` → bucket 1–30 Rp 555.000, 31–60 Rp 965.200, 61–90 Rp 333.000, >90 Rp 1.554.000 — cocok hitungan penguji.

## Laporan harian (untuk Telegram, nama disamarkan)
```
$ python3 scripts/odoo.py laporan-harian
LAPORAN HARIAN ODOO
Rabu, 30 September 2026

PENJUALAN
Pesanan terkonfirmasi: 3, total Rp 1.245.461,08 (+164,0% vs kemarin)
Sebelum pajak Rp 1.122.037,01 | Pajak Rp 123.424,07
Terlaris: [KP-250] Kopi Robusta 250g (13); [GA-1] Gula Aren 1kg (2); [SRP-VNL] Sirup Vanila 750ml (3)
Faktur diposting: 1 (+1 nota kredit), total Rp 299.700

PIUTANG (per 2026-09-30)
Belum lunas: 8 faktur, Rp 3.407.200
Lewat jatuh tempo: 5 faktur, Rp 2.497.000
- INV/2026/00006 (C.M.J.) sisa Rp 999.000, lewat 91 hari
- INV/2026/00005 (P.S.H.) sisa Rp 555.000, lewat 90 hari
- INV/2026/00004 (I.R.D.) sisa Rp 111.000, lewat 31 hari
- ... 2 faktur telat lainnya

STOK
- [SRP-VNL] Sirup Vanila 750ml: -2 (MINUS)
- [GA-1] Gula Aren 1kg: 5 (MENIPIS)
- [TH-100] Teh Melati 100g: 0 (HABIS)

PERLU PERHATIAN
1. Ada faktur lewat 60+ hari. Rincian & nama pelanggan: perintah `piutang`.
2. 2 barang habis/minus. Cek pembelian.
(Nama pelanggan disamarkan. Angka dihitung script dari Odoo.)
(kode keluar: 0)
```
Pemeriksaan: `grep "Maju|Berkah|Sinar|Ratna"` pada laporan teks & `--json` = 0 hasil (nama tersamar). 870 karakter (< 3.500).

## Temuan dari skenario ini
- Angka & batas bucket (30/31, 90/91) **benar** di Odoo asli; `payment_state` `not_paid/partial/paid`, `invoice_date_due`, `amount_residual_signed` benar.
- **TEMUAN SEDANG:** `--per-tanggal` di masa lalu tidak menyaring `invoice_date <= tanggal acuan`. `piutang --per-tanggal 2026-06-15` menghasilkan "8 faktur, Rp 3.407.200, semua belum jatuh tempo", padahal per 15 Juni hanya ada 2 faktur (INV/00005, INV/00006) = Rp 1.554.000.
