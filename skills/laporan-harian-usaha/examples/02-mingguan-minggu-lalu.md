# Skenario 02 — Laporan mingguan: minggu lalu vs minggu sebelumnya (normal)

**Penguji:** agent independen, 2026-09-24. Data sama dengan skenario 01 ("Kedai Kopi Senja", fiktif).

## Permintaan pengguna
> "Laporan minggu lalu, bandingkan dengan minggu sebelumnya."

## Perintah
```bash
python3 <uji>/skills/laporan-harian-usaha/scripts/laporan.py --periode mingguan --sekarang 2026-09-24T21:30+07:00
```
Hari ini Kamis 24/9 → minggu lalu = Senin 14/9 – Minggu 20/9, pembanding 7/9 – 13/9.

## Output nyata
```
LAPORAN MINGGUAN USAHA
14 September 2026 - 20 September 2026
Dibuat 2026-09-24 21:30 WIB

PENJUALAN
Omzet bersih: Rp 372.500
Uang diterima: Rp 409.750 (selisih Rp 37.250 = pajak/service yang dicatat kasir)
Nota: 6 | rata-rata Rp 62.083
vs 7/9-13/9: Rp 189.000 -> naik 97,1%
Per metode bayar:
- QRIS Rp 170.500
- Transfer Rp 143.550
- Tunai Rp 95.700
Terlaris:
1. Kopi Susu Aren: 10 terjual, Rp 190.000
2. Matcha Latte: 3 terjual, Rp 75.000
3. Pisang Goreng Keju: 3 terjual, Rp 40.500
4. Americano: 2 terjual, Rp 36.000
5. Roti Bakar Srikaya: 1 terjual, Rp 16.000

STOK
Posisi per 2026-09-24 21:30 WIB
Minus 1 | habis 1 | menipis 1
- RTB Roti Bakar Srikaya: stok -5 (min 8) MINUS
- TEH Es Teh Lemon: stok 0 (min 10) HABIS
- MCH Matcha Latte: stok 4 (min 6) MENIPIS
Perlu restock (sampai batas minimum): RTB 13, TEH 10, MCH 2
Pesanan belum dikemas: 0

KEHADIRAN
6 karyawan | hadir 35 dari 36 hari terjadwal
Terlambat 3 kali (72 menit) | izin 1, sakit 0, cuti 0, dinas 0
Alpa 0 | tanpa keterangan 0 hari | lembur disetujui 2 jam
Paling sering terlambat: Lala 2x, Yoga 1x

TAGIHAN & FOLLOW-UP
Terlambat 1 | hari ini 2 | besok 1
Piutang tertunggak (terlambat + hari ini): Rp 4.950.000
- #1 piutang Rp 1.750.000, lewat 6 hari
- #2 piutang Rp 3.200.000, hari ini
- #5 janji, hari ini
- #3 prospek, besok
Nama & draf pesan: ketik "rekap pengingat".

PERLU PERHATIAN
1. Penjualan kasir tanggal 2026-09-14, 2026-09-15, 2026-09-17, 2026-09-19, 2026-09-20 belum diimpor ke buku-stok (stok belum terpotong).
2. Stok MINUS 1 barang (RTB). Lakukan stock opname.
3. 1 data absen ganjil perlu dicek (mis. tap tidak lengkap).
4. 1 tagihan/follow-up terlambat, piutang Rp 1.750.000.

Sumber: kasir-lokal, buku-stok, absensi-lokal, pengingat-follow-up (hanya dibaca).
```

## Verifikasi independen
| Angka | Hitung manual dari nota / tap | Script | Cocok |
|---|---|---|---|
| Omzet 14–20/9 | 14/9 80.000 + 15/9 35.000 + 17/9 52.000 + 25.000 + 19/9 (145.000 − 10% = 130.500) + 20/9 50.000 = **372.500** | 372.500 | ✅ |
| Rata-rata | 372.500 ÷ 6 = 62.083,3 → **62.083** | 62.083 | ✅ |
| Omzet 7–13/9 | 55.000 + 54.000 + 80.000 = **189.000** | 189.000 | ✅ |
| % | 183.500 ÷ 189.000 × 100 = 97,089… → **97,1** | 97,1% | ✅ |
| Kopi Susu Aren | 4 + 1 + 5 = 10; 80.000 + 20.000 + 90.000 (setelah diskon) = **190.000** | sama | ✅ |
| Hari terjadwal | 6 hari (Minggu 20/9 libur, pola 6 hari) × 6 orang = **36**; hadir 35 (Fajar izin 16/9) | 35/36 | ✅ |
| Terlambat | Lala 15/9 25 mnt + 16/9 7 mnt, Yoga 18/9 40 mnt = **3 kali, 72 menit** | sama | ✅ |
| Data ganjil | Dimas 19/9: lembur disetujui 2 jam, tap pulang 17.02 (±2 menit) → 1 kasus | 1 | ✅ |
| Belum diimpor | hanya nota 23/9 yang ada di tabel `pesanan` buku-stok; 5 hari berpenjualan di minggu itu | 5 tanggal | ✅ |

## Variasi yang juga diuji
- **Jadwal Senin 07.00** (`--sekarang 2026-09-21T07:00+07:00`): periode tetap 14–20/9, angka identik. ✅
- **Minggu berjalan** (`--tanggal hari-ini`): "21 September 2026 - 24 September 2026 (minggu berjalan, s.d. hari ini)", omzet 96.000 + 346.400 = **442.400**, nota 9 − 1 void = 8, rata-rata **55.300**, dibanding 14–17/9 = 80.000 + 35.000 + 52.000 + 25.000 = **192.000** → (250.400 ÷ 192.000) = 130,42 → **130,4%**. Semua cocok ✅ (perbandingan adil: hari yang sama).
- **`--samarkan` mingguan**: "Paling sering terlambat: L. 2x, Y. 1x"; `perlu_dicek` di JSON bernama `D.`; grep 6 nama karyawan di JSON → 0 ✅.
- Rincian kasus "data absen ganjil" hanya berupa jumlah (pemilik perlu membuka `absensi-lokal`). Wajar untuk ringkasan.

**Hasil: LULUS.**
