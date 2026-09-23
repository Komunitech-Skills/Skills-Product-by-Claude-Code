# Contoh laporan (hasil uji `scripts/susun_pesan.py`)

Semua contoh di bawah adalah hasil nyata menjalankan script skill ini dengan data contoh --
bukan karangan. Dipakai sebagai acuan format saat menyusun laporan baru.

## Penjualan harian

```
*Laporan Penjualan Harian*
2026-09-21 s/d 2026-09-22

Total omzet: Rp 469.000
Jumlah transaksi: 4
Rata-rata omzet/hari: Rp 234.500

*Produk terlaris*
- Kopi Susu -- 22 pcs -- Rp 330.000
- Roti Bakar -- 5 pcs -- Rp 75.000
- Teh Manis -- 8 pcs -- Rp 64.000
```

## Piutang jatuh tempo (contoh format, tanpa nama pelanggan)

```
*Piutang Jatuh Tempo Hari Ini*
Selasa, 23 Sep 2026

Jatuh tempo hari ini: 2 tagihan -- Rp 15.000.000
Terlambat: 1 tagihan -- Rp 12.500.000
H-1 (besok): 3 tagihan -- Rp 8.200.000

⚠️ Detail per pelanggan + draf pesan tagih ada di laporan/arsip/piutang-2026-09-23.csv -- buka manual untuk menindaklanjuti.
```

## Stok menipis (tidak ada yang menipis -- tetap dilaporkan, bukan diam)

```
*Stok Menipis*
Selasa, 23 Sep 2026, 07:00 WIB

Jumlah produk menipis: 0

⚠️ Tidak ada produk menipis hari ini. Data stok terakhir diperbarui 3 jam lalu.
```

## Data sumber belum ada (kegagalan yang ditangani dengan jujur)

```
Laporan penjualan hari ini BELUM dibuat.

Alasan: belum ada file penjualan (pola *.csv) di folder Dokumen/Laporan-AI/masuk/penjualan.
Ekspor data penjualan dari sumbernya (kasir/marketplace/bank) sebagai CSV, taruh di folder itu,
lalu laporan akan otomatis dibuat di jadwal berikutnya.

(Pesan ini dari cek_sumber_data.py -- TIDAK ada angka omzet yang dikirim karena datanya belum
ada, bukan karena omzetnya nol.)
```
