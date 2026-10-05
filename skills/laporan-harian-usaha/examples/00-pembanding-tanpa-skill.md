# 00 — Uji A/B: tanpa skill vs dengan skill (skenario 01)

**Permintaan (sama):** "buat laporan harian usaha saya dari data di folder ini". Folder berisi salinan data 01: `kasir/kasir.db` + 18 file backup kasir, `stok.db` + 17 file backup stok, `absensi/absensi.db`, dan `pengingat/DAFTAR.csv`. Tanggal 24/9/2026.

## A. Tanpa skill (agent umum: jelajahi file, tebak skema, tulis SQL sendiri)
Langkah yang benar-benar dijalankan penguji sebagai agent tanpa skill: `find` → buka `kasir.db` dengan `sqlite3.connect(path)` (mode baca-tulis) → `SELECT sum(total) FROM nota WHERE jenis='jual' AND waktu LIKE '2026-09-24%'` → tabel `produk` stok.db → tabel `tap`/`keterangan`/`lembur` absensi → baca CSV.

```
Laporan Harian - 24 September 2026

Penjualan
- Total penjualan: Rp 371.580 dari 9 transaksi (rata-rata Rp 41.287)
- Kemarin: Rp 272.250 (naik 36,5%)
- Metode: Tunai Rp 318.120, QRIS Rp 53.460
- Terlaris: Kopi Susu Gula Aren (14), Kopi Hitam (4), Roti Bakar Keju (1)

Stok di bawah minimum
- Kopi Hitam -7, Roti Bakar -13, Roti Bakar Keju -21, Air Mineral -5

Karyawan
- Andi masuk 07.18, Budi 12.00-20.40, Joko 12.00-21.40
- Sari izin (anak sakit), Rina alpa. Lembur Budi 1,5 jam (disetujui Bu Maya)

Piutang jatuh tempo
- Bu Tini Fiktif 0812-0000-1111 Rp 1.750.000 (20/9), NIK 3201000000000001
- CV Contoh Maju Rp 3.200.000 (hari ini)
- PT Fiktif Sejahtera (prospek, 23/9)
- Mas Rudi Fiktif Rp 1.250.000 (1/9)
```

## B. Dengan skill `laporan-harian-usaha`
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

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Omzet | **Salah**: Rp 371.580 (termasuk PBJT 10%, void & retur tidak dikurangi) → lebih tinggi **34%** dari yang benar | Rp 276.600 = `penjualan_bersih` resmi kasir, diverifikasi independen |
| % vs kemarin | Salah (36,5%, dari dua angka yang salah) | 16,5% ✔, ditambah pembanding minggu lalu dengan pembagi nol ditangani |
| Void/retur, selisih kas | Tidak terdeteksi | Void, retur, dan **kurang kas Rp 11.000** di "Perlu perhatian" |
| Stok belum diimpor | Tidak terdeteksi | Terdeteksi (24/9 belum diimpor ke buku-stok) |
| Lembur tanpa persetujuan, terlambat (menit) | Hanya jam mentah, pemilik harus menghitung sendiri | Andi 18 menit terlambat, Joko 1 jam 40 menit perlu keputusan |
| Privasi | **Bocor**: nama + nomor HP + NIK pelanggan, alasan izin, nama penyetuju | Hanya nomor item, tanpa nama/HP/NIK |
| Keamanan data | DB dibuka baca-tulis. Risiko file ter-lock/journal saat kasir sedang dipakai | Salinan read-only. Checksum sebelum = sesudah |
| Siap kirim terjadwal | Tidak (tiap kali ditulis ulang, hasil bisa berubah) | Ya: perintah OpenClaw teruji, hasil deterministik |
| Waktu | ±8 langkah eksplorasi + SQL, rawan salah tabel (ada 35 file backup .db) | 1 perintah, <1 detik |

**Kesimpulan:** dengan skill **jelas lebih baik**. Tanpa skill, angka terpenting (omzet) salah 34% karena PBJT, void, dan retur tidak dipahami, data pribadi pelanggan bocor, dan masalah operasional (selisih kas, stok belum diimpor, lembur) tidak muncul. Bahan "sebelum/sesudah" untuk README: "AI biasa: omzet Rp 371.580 (salah). Dengan skill: Rp 276.600 + 7 hal yang perlu dibereskan."
