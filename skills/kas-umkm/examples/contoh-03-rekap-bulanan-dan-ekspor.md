# Contoh 3 — Rekap bulanan, peringatan prive, ekspor ke laporan-keuangan-emkm & arus-kas-13minggu

Dijalankan sungguhan oleh pembuat skill (26/09/2026), melanjutkan buku kas Contoh 1–2 (impor kasir di Contoh 2 tidak
disimpan). **Semua data fiktif.** Skill tujuan dijalankan apa adanya dari repo (tidak diubah).

## 1. Rekap bulanan
Pengguna: *"Rekap kas September dong."*
```
$ kas.py rekap --bulan ini
BUKU KAS Warung Bu Sri (fiktif)
Rekap bulanan September 2026

UANG MASUK: Rp 24.001.235
- Penjualan: Rp 24.000.000
- Pemasukan lain-lain: Rp 1.235
UANG KELUAR: Rp 12.638.500
- Beli stok/bahan: Rp 7.408.000
- Gaji/upah: Rp 1.500.000
- Listrik/air: Rp 385.000
- Sewa tempat: Rp 1.500.000
- Prive (ambil pribadi): Rp 1.800.000
- Pengeluaran lain-lain: Rp 42.500
- Selisih laci kurang: Rp 3.000

HASIL USAHA (masuk usaha - keluar usaha): Rp 13.162.735
  (tidak termasuk modal, pinjaman, prive, dan pindah dana; ini hitungan kas, bukan laba akuntansi)
Prive (ambil pribadi): Rp 1.800.000 = 13,7% dari hasil usaha
Per metode: Tunai masuk Rp 18.070.000 keluar Rp 10.741.000; QRIS masuk Rp 5.180.000 keluar Rp 0; Transfer masuk Rp 751.235 keluar Rp 1.897.500
Pindah dana 15/09/2026: Laci kas -> BRI Rp 5.000.000
Pindah dana 22/09/2026: BRI -> Laci kas Rp 500.000

Per minggu:
01/09-06/09: masuk Rp 5.400.000, keluar Rp 3.620.000, hasil usaha Rp 2.180.000
07/09-13/09: masuk Rp 5.980.000, keluar Rp 3.160.000, hasil usaha Rp 3.220.000
14/09-20/09: masuk Rp 5.860.000, keluar Rp 2.920.000, hasil usaha Rp 3.340.000
21/09-27/09: masuk Rp 6.761.235, keluar Rp 2.938.500, hasil usaha Rp 4.422.735

Pengeluaran terbesar:
1. 01/09 Rp 1.500.000 Sewa tempat - Sewa kios September
2. 10/09 Rp 1.300.000 Beli stok/bahan - Kulakan ke agen
3. 21/09 Rp 1.180.000 Beli stok/bahan - Kulakan ke agen
4. 03/09 Rp 1.020.000 Beli stok/bahan - Kulakan ke agen
5. 17/09 Rp 1.020.000 Beli stok/bahan - Kulakan ke agen

SALDO per akhir 26/09/2026:
- Laci kas: Rp 3.329.000
- BRI: Rp 11.533.735
Total: Rp 14.862.735 (awal periode Rp 3.500.000, naik Rp 11.362.735)
Hitung Laci kas 26/09: buku Rp 2.832.000, fisik Rp 2.829.000 -> SELISIH KURANG Rp 3.000 (disesuaikan)

PERINGATAN PRIVE periode ini: Rp 1.800.000 melewati batas prive bulanan yang Anda tetapkan (Rp 1.500.000).
```
Cek manual: hasil usaha = 24.001.235 − (7.408.000 + 1.500.000 + 385.000 + 1.500.000 + 42.500 + 3.000) = 13.162.735.
Naik saldo 11.362.735 = masuk 24.001.235 − keluar 12.638.500 (pindah dana tidak dihitung).

Agent menambahkan saran singkat (bukan menggurui): *"Ambil pribadi Rp 1,8 juta masih jauh di bawah hasil usaha, tapi
lewat batas yang Ibu tetapkan. Supaya gampang dikontrol, bisa tetapkan 'gaji pemilik' tetap tiap Sabtu, misalnya
Rp 375 ribu, dan catat sebagai prive."*

## 2. Ke laporan-keuangan-emkm (laba rugi & neraca)
Pengguna: *"Bikinin laporan keuangan September buat pengajuan KUR."*
```
$ kas.py ekspor --format emkm --bulan ini --csv kas-emkm-2026-09.csv
Ekspor untuk skill laporan-keuangan-emkm: 73 baris 01/09/2026 - 26/09/2026 ke kas-emkm-2026-09.csv
Kolom: Tanggal;Keterangan;Masuk;Keluar;Kategori (kode kategori emkm; pajak & lain-lain dikosongkan agar emkm mengklasifikasi dari keterangan). Pindah dana antar akun (4 baris) tidak ditulis karena kas + rekening dihitung sebagai satu. Saldo awal gabungan semua akun Rp 3.500.000, saldo akhir Rp 14.862.735.
Jalankan (tanyakan dulu stok awal/akhir, piutang, utang, aset):
python3 <folder-laporan-keuangan-emkm>/scripts/laporan_emkm.py "kas-emkm-2026-09.csv" --nama-usaha "Warung Bu Sri (fiktif)" --periode-awal 2026-09-01 --periode-akhir 2026-09-26 --kas-akhir-aktual 14862735

$ head -5 kas-emkm-2026-09.csv
Tanggal;Keterangan;Masuk;Keluar;Kategori
01/09/2026;Saldo awal;3500000;;
01/09/2026;Jualan tunai;830000;;pendapatan_usaha
01/09/2026;Jualan QRIS;270000;;pendapatan_usaha
01/09/2026;Sewa kios September;;1500000;beban_sewa
```
Dijalankan di skill laporan-keuangan-emkm (tanpa data stok, hanya untuk membuktikan file terbaca; dipotong):
```
Usaha kamu UNTUNG Rp 13.162.735 selama 1 September 2026 s.d. 26 September 2026. ... Kamu mengambil Rp 1.800.000
untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi mengurangi modal usaha. Uang kas di akhir periode:
Rp 14.862.735. Ada 2 hal yang perlu kamu jawab dulu (lihat 'Perlu dicek'), jadi angka ini masih SEMENTARA.
| **LABA (RUGI) BERSIH** | **Rp 13.162.735** |
✔ Cek keseimbangan: Aset = Liabilitas + Ekuitas (Rp 14.862.735). Neraca seimbang.
```
Laba emkm = hasil usaha kas-umkm (tanpa stok/piutang/aset), dan kas akhir emkm = saldo gabungan kas-umkm. Untuk laporan
KUR yang sebenarnya, agent menanyakan stok awal/akhir, piutang, utang, dan aset sesuai SKILL.md emkm.

## 3. Ke arus-kas-13minggu (proyeksi)
Pengguna: *"Kalau begini terus, kas saya aman sampai akhir tahun?"*
```
$ kas.py ekspor --format arus-kas --csv rencana-kas.csv
Draf rencana arus kas dari riwayat 2 minggu (07/09/2026 - 20/09/2026): rencana-kas.csv
- semua masuk Penjualan (rata-rata riwayat): Rp 5.920.000
- semua keluar Beli stok (bahan/supplier): Rp 2.140.000
- semua keluar Gaji karyawan: Rp 500.000
- tgl:24 keluar Listrik/air: Rp 385.000
- tgl:1 keluar Sewa tempat: Rp 1.500.000
- semua keluar Prive (ambil pribadi): Rp 400.000
Saldo semua akun hari ini: Rp 14.862.735. Proyeksi mulai Senin 28/09/2026.
SEBELUM menjalankan proyeksi, tanyakan ke pengguna dan tambahkan baris rencana yang tidak terlihat di riwayat: THR, piutang yang akan dibayar, pembelian besar, kenaikan/penurunan penjualan musiman. Baris 'tgl:' = pos bulanan (tanggal bayar terakhir).
Jalankan:
python3 <folder-arus-kas-13minggu>/scripts/proyeksi_kas.py "rencana-kas.csv" --saldo-awal 14862735 --mulai 2026-09-28 --output-csv proyeksi-kas-13-minggu.csv
Catatan: Riwayat hanya 2 minggu penuh (diminta 8); rata-rata memakai 2 minggu.
```
Cek manual: penjualan minggu 07–13/09 Rp 5.980.000 + 14–20/09 Rp 5.860.000 = 11.840.000 / 2 = 5.920.000.
Listrik/air = token 5/09 Rp 200.000 + PLN 24/09 Rp 185.000 dalam bulan yang sama (agent mengonfirmasi ke pengguna
apakah keduanya memang rutin tiap bulan).

Dijalankan di skill arus-kas-13minggu (dipotong):
```
Saldo awal: Rp 14.862.735 | Batas aman: Rp 3.475.000 (ASUMSI: rata-rata pengeluaran 1 minggu (belum dikonfirmasi pengguna))
| Mg | Periode | Masuk | Keluar | Bersih | Saldo akhir | Status |
| 1 | 28 Sep – 4 Okt | Rp 5.920.000 | Rp 4.540.000 | Rp 1.380.000 | Rp 16.242.735 | 🟢 Aman |
| 2 | 5 Okt – 11 Okt | Rp 5.920.000 | Rp 3.040.000 | Rp 2.880.000 | Rp 19.122.735 | 🟢 Aman |
```
