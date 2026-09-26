# Uji A/B — Skenario 01 tanpa skill vs dengan skill

Penguji independen Akun B, 2026-09-26. Permintaan sama dengan `01-warung-makan-laci-qris-rekening.md` (warung makan, 3 hari, laci + QRIS ke BRI + GoPay, pindah dana, hitung laci).

Metode: output "tanpa skill" adalah jawaban agent umum (tanpa folder skill, tanpa script) yang disusun penguji dengan pola jawaban khas asisten umum; keterbatasan: disusun oleh penguji yang sama, bukan sesi terpisah. Angka di dalamnya sengaja dihitung apa adanya oleh penguji (tanpa kesalahan buatan) agar perbandingan adil.

## A. Tanpa skill (jawaban agent umum, dipotong)
```
Baik Bu Tini, ini catatan kas Anda:

| Tanggal | Keterangan         | Masuk     | Keluar  |
|---------|--------------------|-----------|---------|
| 24/09   | Jualan tunai       | 1.200.000 |         |
| 24/09   | QRIS               |   350.000 |         |
| 24/09   | Es batu & gas      |           |  85.000 |
| 24/09   | Jajan anak         |           | 100.000 |
| 24/09   | Token PLN          |           | 200.000 |
| 25/09   | ... (dst.)         |           |         |
| 25/09   | Setor ke BRI       |           |1.000.000|
| 25/09   | Biaya transfer     |           |   6.500 |
...
Total masuk Rp 4.735.000, total keluar Rp 2.751.500, SALDO Rp 1.983.500 (+ modal awal).
Uang laci Anda Rp 1.233.500, sepertinya ada selisih. Coba cek lagi.
Tips: pisahkan uang pribadi dan usaha, gunakan aplikasi seperti BukuWarung.
```
Masalah khas yang terlihat:
- **Setoran ke BRI 1 jt dicatat sebagai pengeluaran** → keluar membengkak, "saldo" menyesatkan (tidak ada saldo per akun: laci vs BRI vs GoPay).
- "Jajan anak" dicampur dengan beban usaha; tidak ada konsep hasil usaha vs prive.
- Selisih laci tidak dihitung dari saldo buku laci (butuh saldo laci terpisah yang tidak dimiliki), hanya "sepertinya ada selisih".
- **Tidak tersimpan**: besok pengguna harus mengirim ulang semua data; tidak ada rekap mingguan/bulanan otomatis, backup, impor mutasi/kasir, ekspor ke laporan keuangan.
- Tidak ada pratinjau/konfirmasi, tidak ada penanganan tanggal/nominal ambigu.

## B. Dengan skill (output asli script, dipotong)
```
SALDO per akhir 26/09/2026:
- Laci kas: Rp 1.578.500
- BRI: Rp 4.830.000
- GoPay: Rp 225.000
Total: Rp 6.633.500 (awal periode Rp 3.650.000, naik Rp 2.983.500)
HASIL USAHA (masuk usaha - keluar usaha): Rp 3.083.500   (bukan laba akuntansi)
Prive (ambil pribadi): Rp 100.000 = 3,2% dari hasil usaha
Pindah dana 25/09/2026: Laci kas -> BRI Rp 1.000.000

Hitung uang Laci kas, Sabtu, 26/09/2026
Menurut buku : Rp 1.578.500
Uang dihitung: Rp 1.233.500
Hasil: SELISIH KURANG Rp 345.000 (ditandai).
Kemungkinan penyebab (cek dulu, jangan menuduh siapa pun): kembalian terlalu banyak; pengeluaran kecil dari laci belum dicatat ...
```

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Saldo per akun (laci/BRI/GoPay/QRIS) | tidak ada | ada, benar ke rupiah |
| Pindah dana | dicatat sebagai pengeluaran (salah) | netral, biaya admin saja yang jadi beban |
| Prive | tercampur beban | terpisah + peringatan berangka |
| Opname laci | "sepertinya selisih" | selisih pasti Rp 345.000 + penyebab + opsi sesuaikan |
| Persistensi & riwayat | tidak ada | SQLite lokal, backup harian, batal beralasan |
| Keamanan tulis | tidak ada | pratinjau → `--ya`, `perlu_izin` minus/duplikat |
| Integrasi | tidak ada | impor kasir-lokal/mutasi bank, ekspor emkm & arus kas |

**Kesimpulan: dengan skill jelas lebih baik** — terutama pada pemisahan akun & pindah dana (sumber kesalahan paling umum di buku kas manual) dan penyimpanan permanen.
