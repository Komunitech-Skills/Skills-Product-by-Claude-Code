# 01 — Laporan harian lengkap (4 alat terpasang)

**Skenario:** Kafe fiktif "Kafe Senja Fiktif" memakai keempat alat Komunitech. Kasir-lokal mode **PBJT 10% belum termasuk**. Data 7–24 Sep 2026 dibuat dengan menjalankan script alat asli: 155 nota jual, 4 void, 3 retur, tutup kasir tiap hari (24/9 kurang Rp 11.000). Satu nota pukul 23.50 tanggal 23/9 dan satu pukul 00.10 tanggal 24/9. Tanggal 17/9 tidak ada penjualan (listrik padam), jadi pembanding "Kamis lalu" bernilai Rp 0. Buku-stok mengimpor ekspor kasir kecuali 22/9 dan 24/9, stok minus. Absensi 5 karyawan, shift PAGI dan SORE: terlambat, izin, alpa, lembur disetujui, dan pulang lewat jadwal tanpa persetujuan. Pengingat berisi 8 baris: piutang terlambat, jatuh tempo hari ini dan besok, satu nominal ditulis "1.250.000", nama, nomor HP, dan NIK fiktif.
Dijalankan `TZ=Asia/Jakarta`, `--sekarang 2026-09-24T22:30+07:00` (setelah tutup kasir 22.00), folder kerja berisi `pengingat/DAFTAR.csv`.

**Input pengguna:** `laporan usaha hari ini dong`

**Output** (agent menjalankan `python3 scripts/laporan.py`, mengirim teks apa adanya, lalu menambah 3 saran sesuai SKILL.md langkah A.1):

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
Posisi per 2026-09-24 22:30 WIB
Minus 4 | habis 0 | menipis 0
- RBK Roti Bakar Keju: stok -21 (min 10) MINUS
- RB Roti Bakar - Coklat: stok -13 (min 10) MINUS
- KH Kopi Hitam: stok -7 (min 15) MINUS
- AM600 Air Mineral - 600 ml: stok -5 (min 12) MINUS
Perlu restock (sampai batas minimum): RBK 31, RB 23, KH 22, AM600 17
Pesanan belum dikemas: 0

KEHADIRAN
Hadir 3 dari 5 terjadwal
Terlambat (1): Andi 07.18 (18 mnt)
Izin/sakit/cuti/dinas (1): Sari (izin)
Alpa: 1 (Rina)
Lembur disetujui: Budi 1,5 jam
Lembur perlu keputusan (belum disetujui):
- Joko 24/09: pulang 21.40, 1 jam 40 menit setelah jadwal, tanpa lembur disetujui

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
1. Selisih kas saat tutup kasir 2026-09-24 22:00: KURANG Rp 11.000 (seharusnya Rp 437.600, dihitung Rp 426.600).
2. Ada 1 void & 1 retur (-Rp 61.200). Cek alasannya di kasir.
3. Penjualan kasir tanggal 2026-09-24 belum diimpor ke buku-stok (stok belum terpotong).
4. Stok MINUS 4 barang (RBK, RB, KH, AM600). Lakukan stock opname.
5. 1 kejadian pulang lewat jadwal/masuk hari libur tanpa lembur disetujui. Putuskan: catat lembur atau abaikan.
6. 1 data absen ganjil perlu dicek (mis. tap tidak lengkap).
7. 3 tagihan/follow-up terlambat, piutang Rp 3.000.000.

Sumber: kasir-lokal, buku-stok, absensi-lokal, pengingat-follow-up (hanya dibaca).
```

Saran untuk besok:
- Hitung ulang laci dan tanyakan kasir soal kurang Rp 11.000. Cek juga alasan void dan retur di kasir-lokal.
- Impor penjualan kasir tanggal 22 dan 24/9 ke buku-stok, lalu lakukan stock opname untuk 4 barang yang minus.
- Putuskan lembur Joko (pulang 21.40). Ketik "rekap pengingat" untuk menagih #8, #1, dan #2.

**Catatan penguji**
- **Semua angka cocok**: 21 pemeriksaan independen (`verif.py`: SQL langsung ke tabel `nota`/`bayar`/`nota_item`/`sesi` salinan kasir.db, tabel `produk` stok.db, dan CSV pengingat), 0 selisih. Angka juga sama dengan `kasir.py rekap --tanggal 2026-09-24`: penjualan_bersih 276.600, total_diterima 304.260, per metode, per produk. Kehadiran sama dengan `absensi.py harian`, tagihan sama dengan `cek_jatuh_tempo.py rekap`.
- Hitung manual: 16,5% = (276.600 − 237.500) ÷ 237.500 × 100 = 16,463 → 16,5 ✔. Rata-rata 276.600 ÷ (9 − 1) = 34.575 ✔. Pembanding Rp 0 (17/9) tidak dibagi ✔. Nota 00.10 masuk 24/9 dan nota 23.50 masuk 23/9 ✔.
- Stok minus dicek ulang dari saldo awal + masuk − penjualan yang sudah diimpor − rusak. KH −7, RB −13, RBK −21, AM600 −5 cocok. ETM beda 2 dari hitungan naif karena retur "tumpah" tidak mengembalikan stok. Itu perilaku buku-stok, bukan salah laporan.
- Privasi ✔: nama pelanggan, nomor HP, NIK, perihal INV, dan "anak sakit" tidak muncul di teks maupun JSON.
- Kurang: (1) "Rata-rata Rp 34.575" berbeda dengan "Rata-rata/nota Rp 40.508" di rekap resmi kasir-lokal untuk hari yang sama. Kasir menghitung dari uang diterima termasuk PBJT dan belum dikurangi retur. Pemilik akan melihat dua angka "rata-rata" yang berbeda. (2) "Per metode bayar" berjumlah Rp 304.260 (termasuk PBJT), padahal ditaruh di bawah omzet Rp 276.600 tanpa keterangan. (3) Butir 6 "1 data absen ganjil perlu dicek (mis. tap tidak lengkap)" sebenarnya soal "lembur disetujui 1,5 jam, absen hanya 40 menit (Budi)". Teksnya generik dan tidak menyebut siapa atau apa.
- Bila komputer/VPS memakai zona UTC (umum di VPS), muncul butir tambahan "Jam komputer ini bukan Asia/Jakarta … Kasir & absensi mencatat jam komputer". Untuk kasir-lokal 1.1.0 kalimat ini tidak benar, karena kasir mencatat dalam zona toko. Butir ini juga akan muncul **setiap hari** di VPS UTC.
