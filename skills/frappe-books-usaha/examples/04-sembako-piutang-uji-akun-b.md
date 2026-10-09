# Skenario 4 (normal 2) — Distributor sembako, piutang jatuh tempo — uji Akun B

Data: "UD Sembako Makmur (fiktif)", file asli Frappe Books v0.36.0 (zona Asia/Jakarta), partial payment diaktifkan.
Permintaan: *"Siapa saja warung yang telat bayar? Tempo saya 14 hari. Utang ke pemasok juga."* Tanggal acuan `--hari-ini 2026-09-26`.

| Invoice | Tgl (WIB) | Pihak | Total | Dibayar | Sisa |
|---|---|---|---|---|---|
| SINV-1001 | 1 Jun | Warung Bu Sari | 4 × 75.000 = 300.000 | 150.000 | 150.000 |
| SINV-1002 | 10 Jul | Toko Berkah | 12 × 38.000 + 20 × 17.500 = 806.000 | 0 | 806.000 |
| SINV-1003 | 12 Agu | Kios Pak Joko | 12,5 kg × 28.000 = 350.000 | 0 | 350.000 |
| SINV-1004 | 27 Agu 00:15 (UTC 26 Agu) | Minimarket Sejahtera | 10 × 74.000 = 740.000 | 240.000 | 500.000 |
| SINV-1005 | 20 Sep | Warung Bu Sari | 6 × 17.500 + 2,25 × 28.000 = 168.000 | 0 | 168.000 |
| SINV-1006 | 5 Sep | Toko Berkah | 190.000 | lunas | 0 |
| PINV-1001 | 15 Jul | PT Pangan Nusantara | 3.250.000 | 1.000.000 | 2.250.000 |
| PINV-1002 | 10 Sep | CV Telur Segar | 720.000 | 0 | 720.000 |

## Hasil (skill vs independen)
`piutang --tempo 14 --samarkan` (skill):
```
Belum lunas: 5 invoice, total Rp 1.974.000
Telat >90 hari: 1 invoice, Rp 150.000     - SINV-1001 | W. B. S. (. | telat 103 hari
Telat 61-90 hari: 1 invoice, Rp 806.000   - SINV-1002 | T. B. (. | telat 64 hari
Telat 31-60 hari: 1 invoice, Rp 350.000   - SINV-1003 | K. P. J. (. | telat 31 hari
Telat 1-30 hari: 1 invoice, Rp 500.000    - SINV-1004 | M. S. (. | telat 16 hari
Belum jatuh tempo: 1 invoice, Rp 168.000  - SINV-1005 | jatuh tempo 4 Okt 2026
```
Independen (tempo 14): >90 (1; 150.000), 61-90 (1; 806.000), 31-60 (1; 350.000), 1-30 (1; 500.000), belum (1; 168.000). **Cocok.**
Hitung manual contoh: SINV-1001 jatuh tempo 1 Jun + 14 = 15 Jun → 26 Sep − 15 Jun = 103 hari. SINV-1004 memakai tanggal WIB 27 Agu (bukan UTC 26 Agu): 27 Agu + 14 = 10 Sep → 16 hari. Benar.

Tempo bawaan 30: 61-90 (150.000; 87 hari), 31-60 (806.000; 48), 1-30 (350.000; 15), belum (668.000). Cocok.
`utang` (tempo 30): 2 invoice Rp 2.970.000; PINV-1001 telat 43 hari; PINV-1002 belum jatuh tempo. Cocok.
`penjualan --bulan 2026-08 --per barang`: Rp 1.090.000, belum dibayar 850.000; Telur Ayam "12,5" ditampilkan dengan koma. Cocok.
`laporan-harian --tanggal 2026-09-20`: 1 invoice Rp 168.000; 3 piutang telat Rp 1.306.000; tanpa nama pelanggan. Cocok.
SHA-256 file sama sebelum/sesudah.

## Catatan
- (rendah) `--samarkan` untuk nama berkurung menghasilkan "W. B. S. (." — kurung ikut jadi inisial. Kosmetik.
- Asumsi tempo selalu ditulis di laporan (bagus, sesuai SKILL.md).
