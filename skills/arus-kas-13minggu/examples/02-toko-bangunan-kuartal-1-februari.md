# 02 — Toko bangunan: rencana kas kuartal 1 2027 (Februari, akhir bulan, bayar tiap 2 minggu)

## Skenario
S2 — permintaan normal dengan jadwal yang rumit: gaji "tanggal 31 / hari terakhir bulan" (Februari hanya 28 hari), cicilan tanggal 30, pembayaran distributor "tiap 2 minggu mulai minggu ke-3", dan batas aman diisi pengguna. Hasilnya semua minggu aman. Kasus ini menguji aturan "jangan mengarang masalah". Semua nama fiktif.

## Input pengguna
> Saya punya toko bangunan kecil. Mau bikin rencana kas kuartal 1 tahun 2027, mulai Senin 4 Januari 2027. Saldo sekarang 60 juta. Penjualan sekitar 25 juta per minggu. Bayar ke distributor semen & besi 38 juta tiap 2 minggu, mulai minggu ke-3 (minggu 1–2 sudah lunas). Gaji 4 karyawan 16 juta tiap akhir bulan (tanggal 31, kalau bulannya pendek ya hari terakhir). Sewa gudang 8 juta tiap tanggal 1. Setor pajak UMKM sekitar 2,5 juta tiap tanggal 15. Cicilan KUR 6.750.000 tiap tanggal 30. Pelanggan kontraktor CV Bangun Fiktif bayar 45 juta di minggu ke-10. Minggu ke-5 saya mau bayar DP pick-up bekas 30 juta. Saya maunya saldo nggak pernah di bawah 20 juta.

## Langkah yang dijalankan agent
```
minggu;jenis;kategori;nominal;keterangan;kritis
semua;masuk;Penjualan toko;25.000.000;rata-rata per minggu;
10;masuk;Pelunasan piutang;45.000.000;CV Bangun Fiktif (kontraktor);
setiap 2 mulai 3;keluar;Bayar distributor semen & besi (supplier);38.000.000;tiap 2 minggu;ya
tgl:31;keluar;Gaji karyawan;16.000.000;4 orang, akhir bulan;ya
tgl:1;keluar;Sewa gudang;8.000.000;;ya
tgl:15;keluar;Pajak PPh final 0,5%;2.500.000;perkiraan;ya
tgl:30;keluar;Cicilan KUR;6.750.000;;ya
5;keluar;DP pick-up bekas;30.000.000;kendaraan operasional;tidak
```
`python3 scripts/proyeksi_kas.py rencana-kas.csv --saldo-awal "Rp 60.000.000" --mulai 2027-01-04 --batas-aman "20 juta" --output-csv proyeksi-kas-13-minggu.csv`

## Output

## Proyeksi Kas 13 Minggu (4 Jan – 4 Apr 2027)
Saldo awal Rp 60.000.000 · Batas aman Rp 20.000.000 (angka dari Anda)

| Mg | Periode | Masuk | Keluar | Saldo akhir | Status |
|---|---|---:|---:|---:|---|
| 1 | 4 – 10 Jan | Rp 25.000.000 | Rp 0 | Rp 85.000.000 | 🟢 Aman |
| 2 | 11 – 17 Jan | Rp 25.000.000 | Rp 2.500.000 | Rp 107.500.000 | 🟢 Aman |
| 3 | 18 – 24 Jan | Rp 25.000.000 | Rp 38.000.000 | Rp 94.500.000 | 🟢 Aman |
| 4 | 25 – 31 Jan | Rp 25.000.000 | Rp 22.750.000 | Rp 96.750.000 | 🟢 Aman |
| 5 | 1 – 7 Feb | Rp 25.000.000 | Rp 76.000.000 | Rp 45.750.000 | 🟢 Aman |
| 6 | 8 – 14 Feb | Rp 25.000.000 | Rp 0 | Rp 70.750.000 | 🟢 Aman |
| 7 | 15 – 21 Feb | Rp 25.000.000 | Rp 40.500.000 | Rp 55.250.000 | 🟢 Aman |
| 8 | 22 – 28 Feb | Rp 25.000.000 | Rp 22.750.000 | Rp 57.500.000 | 🟢 Aman |
| 9 | 1 – 7 Mar | Rp 25.000.000 | Rp 46.000.000 | Rp 36.500.000 | 🟢 Aman |
| 10 | 8 – 14 Mar | Rp 70.000.000 | Rp 0 | Rp 106.500.000 | 🟢 Aman |
| 11 | 15 – 21 Mar | Rp 25.000.000 | Rp 40.500.000 | Rp 91.000.000 | 🟢 Aman |
| 12 | 22 – 28 Mar | Rp 25.000.000 | Rp 0 | Rp 116.000.000 | 🟢 Aman |
| 13 | 29 Mar – 4 Apr | Rp 25.000.000 | Rp 68.750.000 | Rp 72.250.000 | 🟢 Aman |

**Cara jadwal Anda ditempatkan (mohon dicek):**
- Gaji "tanggal 31": 31 Jan → minggu 4, **28 Feb (hari terakhir Februari 2027)** → minggu 8, 31 Mar → minggu 13.
- Cicilan KUR tanggal 30: 30 Jan → minggu 4, **Februari tidak punya tanggal 30, jadi ditempatkan di 28 Feb** → minggu 8, 30 Mar → minggu 13. Kalau bank menagih 1 Maret, beri tahu saya.
- Distributor tiap 2 minggu mulai minggu 3 → minggu 3, 5, 7, 9, 11, 13.
- Sewa gudang tanggal 1: 1 Jan sudah lewat (sebelum minggu 1), jadi tidak dihitung. 1 Feb → minggu 5, 1 Mar → minggu 9, dan **1 Apr (sewa April) sudah masuk minggu 13**.
- Pajak tanggal 15 → minggu 2, 7, 11.

### Kesimpulan
- **Semua 13 minggu aman.** Tidak ada minggu negatif atau di bawah Rp 20.000.000.
- Saldo terendah **Rp 36.500.000 di minggu 9 (1–7 Mar)**, saat distributor Rp 38.000.000 dan sewa Rp 8.000.000 jatuh bersamaan. Minggu 5 (bayar DP pick-up Rp 30.000.000 + distributor + sewa) juga turun tajam ke Rp 45.750.000, tapi masih aman.
- Tambahan dana dibutuhkan: Rp 0.
- Total 13 minggu: masuk Rp 370.000.000, keluar Rp 357.750.000, kas naik Rp 12.250.000. Kenaikan ini **sangat bergantung pada CV Bangun Fiktif** (Rp 45.000.000). Tanpa pembayaran itu, kas justru turun Rp 32.750.000 dan saldo akhir Rp 27.250.000.

### Saran menjaga kas (karena tidak ada minggu bermasalah)
1. **Kunci pembayaran CV Bangun Fiktif.** Kalau pembayaran mundur ke setelah minggu 13, saldo terendah tetap Rp 36.500.000 (minggu 9) karena uangnya baru masuk di minggu 10. Namun saldo akhir turun ke Rp 27.250.000, tinggal Rp 7.250.000 di atas batas aman. Minta konfirmasi tertulis tanggal bayarnya.
2. **DP pick-up di minggu 5 aman**, jadi tidak perlu ditunda. Kalau ada pilihan, geser ke minggu 6 (8–14 Feb) yang tidak ada pembayaran distributor/sewa, supaya saldo tidak turun ke titik yang sama dengan pembayaran rutin.
3. **Sisihkan dana cadangan** untuk THR Lebaran 2027 (perkiraan pertengahan Maret; tanggal resmi menunggu pengumuman pemerintah). THR 4 karyawan ≈ 1 bulan gaji = Rp 16.000.000 belum masuk tabel ini. Kalau THR dibayar di minggu 10, saldo minggu 10 menjadi Rp 90.500.000, jadi masih aman. Mau saya tambahkan ke rencana?

### File Excel
`proyeksi-kas-13-minggu.csv` (pemisah `;`, untuk Excel berbahasa Indonesia).

Asumsi: penjualan rata Rp 25.000.000/minggu · batas aman Rp 20.000.000 dari Anda · pos "tanggal 30/31" di bulan pendek ditempatkan di hari terakhir bulan · Pembulatan ke rupiah penuh.
Catatan: proyeksi berdasarkan perkiraan Anda. Perbarui tiap minggu dengan angka aktual.

## Catatan penguji
- **Diverifikasi independen**: 13/13 minggu cocok. Penempatan `tgl:31` dan `tgl:30` → 28 Feb 2027 (minggu 8), `setiap 2 mulai 3` → 3, 5, 7, 9, 11, 13, serta sewa 1 Jan yang dikecualikan dan sewa 1 Apr di minggu 13 semuanya benar. Tahun kabisat juga diuji terpisah: 2028, `tgl:29/30/31` → 29 Feb (minggu yang benar).
- Angka "tanpa CV Bangun" dan "THR di minggu 10" dihitung ulang dengan CSV yang diubah: saldo akhir 72.250.000 − 45.000.000 = 27.250.000. Saldo minggu 10 tanpa piutang = 61.500.000; dengan THR = 106.500.000 − 16.000.000 = 90.500.000.
- Bagus: SKILL.md punya aturan "jika semua minggu aman … jangan mengarang masalah", dan output mengikutinya.
- Kurang (ringan): SKILL.md tidak meminta agent menjelaskan penempatan tanggal kepada pengguna (terutama bulan pendek dan pos yang jatuh sebelum minggu 1), padahal itu sumber salah paham paling umum. Penjelasan di sini ditambahkan oleh agent.
