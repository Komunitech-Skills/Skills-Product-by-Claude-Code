# Laporan Harian Otomatis Tanpa Dashboard Berbayar

**Setiap malam satu pesan Telegram berisi omzet, stok, karyawan, dan tagihan usaha Anda. Tanpa aplikasi dashboard berlangganan, data tetap di komputer sendiri.**

## Manfaat
- ✅ **Satu pesan, seluruh usaha.** Penjualan, stok menipis, siapa yang terlambat/alpa, lembur yang perlu diputuskan, dan tagihan jatuh tempo, digabung dari alat Komunitech yang sudah Anda pakai (Kasir Lokal, Buku Stok, Absensi Lokal, Pengingat Follow-up).
- ✅ **Langsung kelihatan naik atau turun.** Omzet dibandingkan dengan kemarin dan hari yang sama minggu lalu dalam persen. Tiap Senin pagi ada laporan mingguan dibanding minggu sebelumnya.
- ✅ **Masalah muncul sendiri.** Selisih uang laci, stok minus, penjualan kasir yang belum masuk buku stok, absen yang belum diimpor, dan piutang terlambat dikumpulkan di bagian "Perlu Perhatian".
- ✅ **Angka apa adanya.** Semua angka diambil dari alat Anda. Bagian yang datanya belum ada ditulis "belum ada data", tidak diisi perkiraan. Rumus persen dan pembulatan tertulis jelas.
- ✅ **Aman.** Hanya membaca data (tidak pernah mengubah kasir/stok/absen Anda), tanpa nama pelanggan di laporan, nama karyawan bisa disamarkan, dan hanya dikirim ke Anda sendiri.

## Cocok untuk siapa
- Pemilik toko, warung, kafe, atau usaha jasa yang sudah memakai minimal satu alat lokal Komunitech: **Kasir Lokal**, **Buku Stok**, **Absensi Lokal**, atau **Pengingat Follow-up**. Makin banyak alat yang dipakai, makin lengkap laporannya.
- Pemilik yang jarang di toko dan ingin tahu kondisi usaha dari HP tanpa membuka banyak aplikasi.
- Anggota VIP yang memakai OpenClaw dan ingin laporan terjadwal ke Telegram.

**Kurang cocok:** usaha yang datanya ada di aplikasi lain (Moka, Majoo, Excel dari marketplace). Untuk itu pakai skill **Laporan Otomatis Terjadwal** atau **Rekap Penjualan CSV**.

## Contoh sebelum & sesudah
**Sebelum:** tiap malam membuka rekap kasir, lalu cek stok, lalu tanya admin siapa yang tidak masuk, lalu ingat-ingat siapa yang belum bayar. Atau berlangganan aplikasi dashboard bulanan.

**Sesudah (otomatis jam 21.00 di Telegram):**
```
LAPORAN HARIAN USAHA
Kamis, 24 September 2026

PENJUALAN
Omzet bersih: Rp 69.000
Nota: 2 (+1 dibatalkan) | rata-rata Rp 34.500
vs kemarin (Rab 23/9): Rp 36.000 -> naik 91,7%
Per metode bayar: Tunai Rp 51.000, QRIS Rp 18.000

STOK
- RB Roti Bakar - Coklat: stok -5 (min 5) MINUS
- KH Kopi Hitam: stok 4 (min 10) MENIPIS

KEHADIRAN
Hadir 2 dari 5 terjadwal | Terlambat: Andi 08.12 | Alpa: Rina

TAGIHAN & FOLLOW-UP
- #2 piutang Rp 12.500.000, lewat 3 hari

PERLU PERHATIAN
1. Selisih kas saat tutup kasir: KURANG Rp 11.000
2. Penjualan kasir hari ini belum diimpor ke buku stok
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Laporan usaha hari ini"
- "Gimana usaha kemarin?"
- "Laporan minggu lalu, bandingkan dengan minggu sebelumnya"
- "Kirim laporan harian ke Telegram saya tiap jam 9 malam, dan laporan mingguan tiap Senin pagi" (OpenClaw)
- "Samarkan nama karyawan di laporan"

## Instalasi singkat
Salin folder `laporan-harian-usaha` ke folder skills AI agent kamu, **di folder yang sama** dengan alat Komunitech yang kamu pakai (mis. `kasir-lokal`, `buku-stok`):

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

Butuh **Python 3.8+** (gratis di python.org; Mac/Linux biasanya sudah ada). Tidak butuh internet, akun, atau API key. Laporan terjadwal ke Telegram butuh OpenClaw yang menyala di komputer yang sama dengan data toko (panduan langkah demi langkah ada di `references/openclaw-jadwal.md`; Komunitech juga menyediakan jasa setup).

## FAQ
**Apakah skill ini bisa mengubah atau merusak data kasir/stok/absen saya?**
Tidak. Data dibuka dalam mode baca saja dan disalin sementara untuk dihitung. File asli tidak pernah ditulis (sudah diuji otomatis).

**Saya baru memakai Kasir Lokal saja. Apakah tetap berguna?**
Ya. Bagian penjualan langsung terisi; bagian lain menulis "belum ada data" sampai alatnya dipakai. Tidak ada angka karangan.

**Kenapa nama pelanggan yang belum bayar tidak muncul?**
Sengaja, supaya laporan aman walau terbaca orang lain di HP Anda. Ketik "rekap pengingat" untuk melihat nama dan draf pesan penagihan dari skill Pengingat Follow-up.
