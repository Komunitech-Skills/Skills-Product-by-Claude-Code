# Skenario 02 — Piutang & laporan harian (normal)

**Penguji:** pembuat skill (BUKAN penguji independen), 2026-09-24. Dolibarr **asli** 24.0.1 di container Linux (PHP 8.4, MariaDB 10.11), zona PHP Asia/Jakarta. Data fiktif.

Data: 5 invoice tervalidasi (satu dibayar sebagian Rp 500.000 via API pembayaran oleh admin; satu dibayar penuh tapi belum ditutup), beberapa draf, 3 produk barang + 1 jasa.

## "Siapa yang belum bayar?" → `piutang`
```
PIUTANG BELUM LUNAS per 2026-09-24
Total sisa tagihan: Rp 2.578.585 (4 invoice)

UMUR PIUTANG (dihitung dari tanggal jatuh tempo)
- belum jatuh tempo: 1 invoice, Rp 108.225
- lewat 1-30 hari: 2 invoice, Rp 1.083.360
- lewat 61-90 hari: 1 invoice, Rp 1.387.000

RINCIAN (paling lama terlambat di atas)
- IN2606-0003 | Toko Sinar Abadi | sisa Rp 1.387.000 (sudah dibayar Rp 500.000) | tempo 2026-07-01 (lewat 85 hari)
- IN2608-0001 | Toko Sinar Abadi | sisa Rp 749.250 | tempo 2026-09-01 (lewat 23 hari)
- IN2609-0005 | CV Maju Jaya | sisa Rp 334.110 | tempo 2026-09-23 (lewat 1 hari)
- IN2609-0004 | CV Maju Jaya | sisa Rp 108.225 | tempo 2026-10-10 (jatuh tempo 16 hari lagi)

CATATAN
- IN2609-0002 sudah terbayar penuh tetapi belum ditandai lunas di Dolibarr.
```
## Versi disamarkan (`piutang --samarkan --maks 2`)
```
PIUTANG BELUM LUNAS per 2026-09-24
Total sisa tagihan: Rp 2.578.585 (4 invoice)

UMUR PIUTANG (dihitung dari tanggal jatuh tempo)
- belum jatuh tempo: 1 invoice, Rp 108.225
- lewat 1-30 hari: 2 invoice, Rp 1.083.360
- lewat 61-90 hari: 1 invoice, Rp 1.387.000

RINCIAN (paling lama terlambat di atas)
- IN2606-0003 | T.S.A. | sisa Rp 1.387.000 (sudah dibayar Rp 500.000) | tempo 2026-07-01 (lewat 85 hari)
- IN2608-0001 | T.S.A. | sisa Rp 749.250 | tempo 2026-09-01 (lewat 23 hari)
... dan 2 invoice lainnya (pakai --maks).

CATATAN
- IN2609-0002 sudah terbayar penuh tetapi belum ditandai lunas di Dolibarr.
```
## "Laporan harian Dolibarr" → `laporan-harian --tanggal 2026-09-24`
```
LAPORAN HARIAN DOLIBARR
Kamis, 24 September 2026
Dibuat 2026-09-24 20:56 WIB

PENJUALAN (invoice tervalidasi bertanggal ini)
Total (termasuk PPN): Rp 477.127,95
DPP Rp 429.845 | PPN Rp 47.282,95
Invoice: 2
Belum dibayar dari penjualan ini: Rp 108.225
vs kemarin: Rp 0 (persen tidak dihitung)

PIUTANG
Belum lunas: 4 invoice, Rp 2.578.585
Terlambat: 3 invoice, Rp 2.470.360
- IN2606-0003 sisa Rp 1.387.000, lewat 85 hari
- IN2608-0001 sisa Rp 749.250, lewat 23 hari
- IN2609-0005 sisa Rp 334.110, lewat 1 hari

STOK
Perlu perhatian: 2 dari 3 produk
- CUP-12 Gelas Kertas 12oz (isi 50): stok 0 HABIS
- KPI-250 Kopi Bubuk Arabika 250g: stok 7 MENIPIS

PERLU PERHATIAN
1. 4 draf invoice bertanggal hari ini belum divalidasi (belum dihitung sebagai penjualan).
2. Ada 3 invoice terlambat. Rincian & nama pelanggan: perintah `piutang`.

Sumber: Dolibarr http://127.0.0.1:8088/dolibarr (hanya dibaca).
```
Teks yang sama dihasilkan oleh jadwal OpenClaw 2026.9.6 (`automations run --wait`, status ok) — lihat `references/openclaw-jadwal.md`.

## Verifikasi angka independen
- Umur: 24/9 − 1/7 = 30 + 31 + 24 = **85 hari** ✓; 24/9 − 1/9 = **23** ✓; 24/9 − 23/9 = **1** ✓; 10/10 − 24/9 = 16 hari lagi ✓.
- Total sisa: 1.387.000 + 749.250 + 334.110 + 108.225 = **2.578.585** ✓ (IN2609-0002 sisa 0 → catatan, tidak dihitung).
- Penjualan 24/9: IN2609-0002 368.902,95 + IN2609-0004 108.225 = **477.127,95** ✓; DPP 332.345 + 97.500 = **429.845** ✓. Draf tidak dihitung ✓.
- Laporan tanpa nama pelanggan ✓.
