# 02 — Laporan mingguan Senin pagi (nama disamarkan)

**Skenario:** Jadwal OpenClaw Senin 07.00 WIB. `--periode mingguan --samarkan`, `--sekarang 2026-09-21T07:00+07:00` → minggu 14–20 Sep dibanding 7–13 Sep. Data sama dengan 01.

**Input pengguna:** `laporan minggu lalu dibanding minggu sebelumnya ya, nama karyawan disamarkan aja`

**Output:**

```
LAPORAN MINGGUAN USAHA
14 September 2026 - 20 September 2026
Dibuat 2026-09-21 07:00 WIB

PENJUALAN
Omzet bersih: Rp 2.143.600
Uang diterima: Rp 2.357.960 (selisih Rp 214.360 = pajak/service yang dicatat kasir)
Nota: 61 (+2 dibatalkan) | rata-rata Rp 35.141
vs 7/9-13/9: Rp 2.669.900 -> turun 19,7%
Per metode bayar:
- QRIS Rp 1.079.100
- Tunai Rp 994.840
- Transfer Rp 284.020
Terlaris:
1. Kopi Susu Gula Aren: 52 terjual, Rp 928.800
2. Roti Bakar Keju: 25 terjual, Rp 423.300
3. Kopi Hitam: 30 terjual, Rp 357.600
4. Roti Bakar Coklat: 15 terjual, Rp 223.500
5. Es Teh Manis: 32 terjual, Rp 182.400
Retur 1 | void 2 (-Rp 120.400)

STOK
Posisi per 2026-09-21 07:00 WIB
Minus 4 | habis 0 | menipis 0
- RBK Roti Bakar Keju: stok -21 (min 10) MINUS
- RB Roti Bakar - Coklat: stok -13 (min 10) MINUS
- KH Kopi Hitam: stok -7 (min 15) MINUS
- AM600 Air Mineral - 600 ml: stok -5 (min 12) MINUS
Perlu restock (sampai batas minimum): RBK 31, RB 23, KH 22, AM600 17
Pesanan belum dikemas: 0

KEHADIRAN
5 karyawan | hadir 30 dari 30 hari terjadwal
Terlambat 2 kali (34 menit) | izin 0, sakit 1, cuti 0, dinas 0
Alpa 0 | tanpa keterangan 0 hari | lembur disetujui 2 jam
Paling sering terlambat: A. 2x
Lembur perlu keputusan (belum disetujui):
- J. 18/09: pulang 00.30, 4 jam 30 menit setelah jadwal, tanpa lembur disetujui

TAGIHAN & FOLLOW-UP
Terlambat 2 | hari ini 0 | besok 0
Piutang tertunggak (terlambat + hari ini): Rp 3.000.000
- #8 piutang Rp 1.250.000, lewat 20 hari
- #1 piutang Rp 1.750.000, lewat 1 hari
Nama & draf pesan: ketik "rekap pengingat".

PERLU PERHATIAN
1. Selisih kas saat tutup kasir 2026-09-18 22:00: KURANG Rp 11.000 (seharusnya Rp 300.100, dihitung Rp 289.100).
2. Ada 2 void & 1 retur (-Rp 120.400). Cek alasannya di kasir.
3. Stok MINUS 4 barang (RBK, RB, KH, AM600). Lakukan stock opname.
4. 1 kejadian pulang lewat jadwal/masuk hari libur tanpa lembur disetujui. Putuskan: catat lembur atau abaikan.
5. 2 tagihan/follow-up terlambat, piutang Rp 3.000.000.

Sumber: kasir-lokal, buku-stok, absensi-lokal, pengingat-follow-up (hanya dibaca).
```

**Catatan penguji**
- Penjualan: 19 pemeriksaan independen, 0 selisih. Omzet 2.143.600, 2.669.900, dan −19,7% (= −526.300 ÷ 2.669.900 × 100 = −19,71) ✔. Nota 61 (+2 void), per metode, dan top 5 sama dengan `kasir.py rekap --dari 2026-09-14 --sampai 2026-09-20`. Selisih kas 18/9 ✔. Diuji juga minggu berjalan (`--tanggal hari-ini` pada 24/9 → 21–24 vs 14–17, +28,0% ✔) dan hari 15, 18, 21, 23/9 (semua cocok).
- **Kehadiran menyesatkan (cacat SEDANG):** "hadir 30 dari 30 hari terjadwal" terbaca seperti kehadiran 100%, padahal J. sakit 1 hari. Menurut `absensi.py rekap`, hadir terjadwal = 29. Angka 30 muncul karena `laporan.py` baris 510 menjumlahkan `hadir + hadir_di_hari_libur` (S. masuk di hari liburnya, 15/9). Yang benar: "hadir 29 dari 30 (+1 masuk hari libur)".
- Terlambat 2 kali / 34 menit (A.: 25 + 9) ✔. Lembur disetujui 2 jam (S. 15/9) ✔. J. 18/09 pulang 00.30 lewat tengah malam = 4 jam 30 menit setelah jadwal 20.00 ✔.
- `--samarkan` ✔: nama lengkap tidak ada di teks dan JSON. Inisial bisa bentrok (mis. Budi dan Bambang sama-sama "B.").
- Posisi stok = kondisi saat laporan dibuat, tertulis jujur "Posisi per …". Di uji ini stok memuat data setelah 21/9 karena waktu disimulasikan.
