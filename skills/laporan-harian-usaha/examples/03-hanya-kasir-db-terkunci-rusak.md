# 03 — Hanya kasir terpasang, database terkunci, database rusak

**Input pengguna:** `rekap semua usaha hari ini`

## 3a. Folder skills hanya berisi `laporan-harian-usaha` + `kasir-lokal`
Folder data juga berisi `stok.db` (skill buku-stok belum terpasang) dan `absensi.db` yang **terpotong** (3.000 byte pertama). HOME kosong, pengingat tidak ada.

```
LAPORAN HARIAN USAHA
Kamis, 24 September 2026
Dibuat 2026-09-24 22:30 WIB

PENJUALAN
Omzet bersih: Rp 276.600
Uang diterima: Rp 304.260 (selisih Rp 27.660 = pajak/service yang dicatat kasir)
Nota: 8 (+1 dibatalkan) | rata-rata Rp 34.575
vs kemarin (Rab 23/9): Rp 237.500 -> naik 16,5%
vs Kamis lalu (17/9): Rp 0 -> naik dari Rp 0 (persen tidak dihitung)
Per metode bayar:
- Tunai Rp 250.800
- QRIS Rp 53.460
Terlaris:
1. Kopi Susu Gula Aren: 11 terjual, Rp 192.600
2. Kopi Hitam: 3 terjual, Rp 36.000
3. Roti Bakar Keju: 1 terjual, Rp 17.000
4. Roti Bakar Coklat: 1 terjual, Rp 15.000
5. Es Teh Manis: 2 terjual, Rp 12.000
Retur 1 | void 1 (-Rp 61.200)

STOK
Belum ada data: buku-stok tidak terbaca (lihat Perlu Perhatian).

KEHADIRAN
Belum ada data: absensi-lokal tidak terbaca (lihat Perlu Perhatian).

TAGIHAN & FOLLOW-UP
Belum ada data (pengingat-follow-up belum dipakai di komputer ini).

PERLU PERHATIAN
1. Selisih kas saat tutup kasir 2026-09-24 22:00: KURANG Rp 11.000 (seharusnya Rp 437.600, dihitung Rp 426.600).
2. Ada 1 void & 1 retur (-Rp 61.200). Cek alasannya di kasir.
3. buku-stok tidak terbaca: data ada, tetapi script stok.py tidak ditemukan. Pasang skill buku-stok di folder skills yang sama, atau beri --stok-script PATH.
4. absensi-lokal tidak terbaca: data ada, tetapi script absensi.py tidak ditemukan. Pasang skill absensi-lokal di folder skills yang sama, atau beri --absensi-script PATH.

Sumber: kasir-lokal (hanya dibaca).
```

## 3b. Semua alat terpasang. kasir.db **dikunci** proses lain (BEGIN EXCLUSIVE + tulis, 40 detik), absensi.db **rusak**

```
LAPORAN HARIAN USAHA
Kamis, 24 September 2026
Dibuat 2026-09-24 22:30 WIB

PENJUALAN
Belum ada data: kasir-lokal tidak terbaca (lihat Perlu Perhatian).

STOK
Posisi per 2026-09-24 22:30 WIB
Minus 4 | habis 0 | menipis 0
- RBK Roti Bakar Keju: stok -21 (min 10) MINUS
- RB Roti Bakar - Coklat: stok -13 (min 10) MINUS
- KH Kopi Hitam: stok -7 (min 15) MINUS
- AM600 Air Mineral - 600 ml: stok -5 (min 12) MINUS
Perlu restock (sampai batas minimum): RBK 31, RB 23, KH 22, AM600 17
Pesanan belum dikemas: 0

KEHADIRAN
Belum ada data: absensi-lokal tidak terbaca (lihat Perlu Perhatian).

TAGIHAN & FOLLOW-UP
Terlambat 3 | hari ini 1 | besok 1
Piutang tertunggak (terlambat + hari ini): Rp 6.200.000
- #8 piutang Rp 1.250.000, lewat 23 hari
- #1 piutang Rp 1.750.000, lewat 4 hari
- #4 prospek, lewat 1 hari
- #2 piutang Rp 3.200.000, hari ini
- #3 piutang Rp 850.000, besok
Nama & draf pesan: ketik "rekap pengingat".

PERLU PERHATIAN
1. Stok MINUS 4 barang (RBK, RB, KH, AM600). Lakukan stock opname.
2. 3 tagihan/follow-up terlambat, piutang Rp 3.000.000.
3. kasir-lokal tidak terbaca: database sedang dipakai program lain lebih dari 10 detik (mis. transaksi sedang disimpan). Data aman; jalankan laporan lagi sebentar lagi.
4. absensi-lokal tidak terbaca: file bukan database atau rusak (database disk image is malformed). Pulihkan dari folder backup alatnya.

Sumber: buku-stok, pengingat-follow-up (hanya dibaca).
```
Waktu jalan 10,2 detik (batas tunggu default 10 detik). Laporan tidak menggantung, alat lain tetap dilaporkan.

**Catatan penguji**
- Alat yang hilang, rusak, atau terkunci dilewati dengan pesan jelas. Tidak ada angka karangan. Kode keluar 0.
- Terkunci: hanya kunci tulis EXCLUSIVE yang memblokir. Kunci RESERVED/IMMEDIATE (transaksi baru dimulai) tetap bisa dibaca dengan data terakhir yang sudah tersimpan, dan itu benar.
- Kurang (RINGAN): saat kasir terkunci, pukul 21.00 laporan terkirim tanpa bagian penjualan dan tidak ada coba ulang otomatis. Sebaiknya coba ulang sekali lagi (mis. 30 detik) sebelum menyerah.
- Kurang (RINGAN): di 3a, butir 4/5 menyarankan "Pasang skill …". Itu benar, tetapi bagi pemilik yang memang tidak membeli buku-stok, pesan ini akan muncul setiap malam. Perlu cara menyembunyikannya (sudah ada `--tanpa stok`, tapi SKILL.md tidak menyarankannya di kasus ini).
- Hanya-baca pada kasus terkunci dan rusak ✔ (lihat HASIL-UJI §Hanya-baca).
