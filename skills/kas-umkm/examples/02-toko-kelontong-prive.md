# Uji 02 — Toko kelontong dengan prive pemilik (normal)

Penguji independen Akun B, 2026-09-26. Data rekaan, database terpisah.

## Permintaan pengguna (disimulasikan)
> "Toko Kelontong Pak Darto, laci 2 juta, BCA 5 juta, mulai 1 September. Batas ambil pribadi 2 juta sebulan.
> 1/9 kulakan agen sembako 3,5jt transfer BCA, jualan 1,1jt. 5/9 jualan 1,3jt, sewa kios 750rb BCA. 10/9 jualan 1,2jt, bayar SPP anak 1jt dari laci.
> 15/9 ambil 1,5jt buat belanja bulanan rumah. 18/9 masukin uang pribadi 1jt ke laci (eh salah, harusnya 800rb). 22/9 jualan 2,4jt tunai + pesanan hajatan 600rb transfer BCA."

## Jalannya uji & output asli
1. `init ... --batas-prive 2jt`, `akun tambah --nama BCA ...` → tersimpan.
2. 10/09 "bayar SPP anak" tanpa kategori → **ditebak prive** (disebut di `Asumsi`) dan langsung muncul:
   `PERINGATAN PRIVE bulan ini (s.d. 10/09/2026): hasil usaha -Rp 650.000, tetapi uang usaha diambil pribadi Rp 1.000.000. Uang ini memakan modal/uang belanja stok. (Hasil usaha bisa rendah karena belanja stok besar di awal; lihat rekap bulanan sebelum menyimpulkan.)` — sopan dan memberi konteks kulakan awal bulan.
3. 15/09 "belanja bulanan rumah" tanpa kategori → **ditolak** (`perlu_kategori`, agent harus bertanya). Aman, tetapi tidak konsisten dengan "SPP" yang ditebak prive (lihat temuan). Dengan `--kategori prive`:
   ```
   KELUAR Rp 1.500.000 | 15/09/2026 | Prive (ambil pribadi) | Tunai -> Laci kas | belanja bulanan rumah
   Catatan: PERINGATAN PRIVE ... hasil usaha -Rp 650.000, tetapi uang usaha diambil pribadi Rp 2.500.000 ...
   Catatan: PERINGATAN PRIVE bulan ini (s.d. 15/09/2026): Rp 2.500.000 melewati batas prive bulanan yang Anda tetapkan (Rp 2.000.000).
   ```
4. Modal 1jt tersimpan; mencatat ulang yang sama → `perlu_izin`: "Kemungkinan tercatat DOBEL ... sama dengan catatan #7". Benar.
5. `batal --id #7 --alasan "salah nominal, harusnya 800rb" --ya` lalu catat 800rb. Catatan batal tidak dihapus (terlihat di `daftar --semua`/ekspor lengkap).
6. Rekap bulan 09/2026 (akhir):
   ```
   UANG MASUK: Rp 7.400.000 (Penjualan 6.600.000; Modal pemilik 800.000)
   UANG KELUAR: Rp 6.750.000 (Beli stok 3.500.000; Sewa 750.000; Prive 2.500.000)
   HASIL USAHA: Rp 2.350.000
   Prive (ambil pribadi): Rp 2.500.000 = 106,4% dari hasil usaha
   PERINGATAN PRIVE periode ini: diambil pribadi Rp 2.500.000, lebih besar dari hasil usaha Rp 2.350.000 (106,4%). Kelebihan Rp 150.000 diambil dari modal usaha.
   PERINGATAN PRIVE periode ini: Rp 2.500.000 melewati batas prive bulanan yang Anda tetapkan (Rp 2.000.000).
   SALDO: Laci Rp 6.300.000, BCA Rp 1.350.000
   ```
7. `atur --batas-prive hapus --ya` → peringatan batas hilang, peringatan "prive > hasil usaha" tetap. Benar.

## Verifikasi angka independen (Decimal)
| Pos | Hitungan penguji | Script | Cocok |
|---|---|---|---|
| Penjualan | 1,1+1,3+1,2+2,4+0,6 jt = 6.600.000 | 6.600.000 | ya |
| Hasil usaha | 6.600.000 − 3.500.000 − 750.000 = 2.350.000 (modal & prive tidak ikut) | 2.350.000 | ya |
| Prive % | 2.500.000 / 2.350.000 = 106,38% | 106,4% | ya |
| Kelebihan prive | 2.500.000 − 2.350.000 = 150.000 | 150.000 | ya |
| Laci | 2.000.000+1.100.000+1.300.000+1.200.000−1.000.000−1.500.000+800.000+2.400.000 = 6.300.000 (modal 1jt dibatalkan) | 6.300.000 | ya |
| BCA | 5.000.000−3.500.000−750.000+600.000 = 1.350.000 | 1.350.000 | ya |
| Hasil usaha s.d. 10/09 | 3.600.000 − 4.250.000 = −650.000 | −650.000 | ya |

## Penilaian
Prive dibedakan dari beban, modal tidak dihitung sebagai hasil usaha, batal tercatat dengan alasan, duplikat ditanyakan. Peringatan berangka jelas dan tidak menggurui.
Kekurangan kecil: tebakan kategori tidak konsisten ("SPP" → prive, "belanja bulanan rumah" → tanya); aman karena gagal ke arah bertanya.

**Hasil: LULUS (9/10).**
