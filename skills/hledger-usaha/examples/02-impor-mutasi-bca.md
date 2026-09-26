# 02 — Impor mutasi BCA Agustus lewat aturan hledger (uji pembuat, hledger 1.52.4 asli)

**Pengguna:** "Ini file mutasi BCA Agustus (CSV dari KlikBCA), masukkan ke pembukuan ya."
**Data:** `tests/data/mutasi-bca-agustus.csv` (format mirip ekspor KlikBCA: 5 baris info di atas, tanggal `'01/08` tanpa tahun, kolom CR/DB tanpa judul, baris ringkasan di bawah). Data fiktif.

**Alur agent:** pratinjau → tanyakan 3 baris "belum dikelompokkan" dalam satu pesan → pengguna menjawab: Kantor Maju = pelunasan jualan (dicatat penjualan karena belum ada piutangnya), Roastery Gayo = beli bahan, Ibu Ratna = setoran modal adik pemilik → `--tetapkan` + `--ya` → impor ulang membuktikan tidak dobel → simpan kata kunci untuk bulan depan → cek saldo bank vs saldo akhir di mutasi.

```
$ python3 hledger_usaha.py impor-bank mutasi-bca-agustus.csv --tahun 2026
IMPOR MUTASI BANK (PRATINJAU, belum disimpan)
File: mutasi-bca-agustus.csv -> rekening Aset:Bank:BCA
Kolom terbaca: Tanggal Transaksi, Keterangan, Jumlah, kolom_5, Saldo
Terbaca 12 transaksi (2026-08-01 s.d. 2026-08-31); 0 sudah pernah diimpor (dilewati); 12 baru.
Uang masuk Rp 3.891.734,56 | uang keluar Rp 8.800.500
Uji silang aturan dengan hledger: COCOK (12 baris)
Baris dilewati: baris 19 (tanggal tidak dikenali: Saldo Awal); baris 20 (tanggal tidak dikenali: Mutasi Kredit); baris 21 (tanggal tidak dikenali: Mutasi Debet); baris 22 (tanggal tidak dikenali: Saldo Akhir)

RINGKASAN PER AKUN
- Beban:Gaji: 1 transaksi, keluar Rp 3.000.000
- Beban:Belum Dikelompokkan: 1 transaksi, keluar Rp 2.250.000
- Pendapatan:Penjualan: 2 transaksi, masuk Rp 2.090.500
- Beban:Sewa: 1 transaksi, keluar Rp 2.000.000
- Pendapatan:Belum Dikelompokkan: 2 transaksi, masuk Rp 1.800.000
- Aset:Kas: 1 transaksi, keluar Rp 1.000.000
- Beban:Listrik Air Internet: 1 transaksi, keluar Rp 500.000
- Beban:Transportasi: 1 transaksi, keluar Rp 38.000
- Beban:Admin Bank: 1 transaksi, keluar Rp 12.500
- Pendapatan:Lain-lain: 1 transaksi, masuk Rp 1.234,56

PERLU DITANYAKAN KE PENGGUNA (3 transaksi belum dikelompokkan):
- baris 7: 2026-08-01 TRSF E-BANKING CR 0108/FTSCY/WS95031 1500000.00 KANTOR MAJU JAYA masuk Rp 1.500.000
- baris 10: 2026-08-05 TRSF E-BANKING DB 0508/FTSCY/WS95031 ROASTERY GAYO keluar Rp 2.250.000
- baris 16: 2026-08-28 TRSF E-BANKING CR 2808 IBU RATNA ARISAN masuk Rp 300.000
Tetapkan dengan --tetapkan "BARIS=Akun", atau simpan kata kuncinya untuk bulan depan dengan perintah tambah-aturan.

Cek saldo: saldo bank sebelum transaksi pertama Rp 8.600.000; saldo Aset:Bank:BCA di catatan sebelum tanggal itu Rp 8.600.000.
COCOK. Setelah impor, saldo catatan akan sama dengan saldo akhir bank Rp 3.691.234,56.

Contoh 2 transaksi pertama:
2026-08-01 TRSF E-BANKING CR 0108/FTSCY/WS95031 1500000.00 KANTOR MAJU JAYA  ; ref:d3a08ab1654f, sumber:mutasi-bank
    Aset:Bank:BCA                                   Rp 1.500.000
    Pendapatan:Belum Dikelompokkan                 -Rp 1.500.000
2026-08-02 QRIS MERCHANT KOPI SARI 0208  ; ref:5814b0ee1ffb, sumber:mutasi-bank
    Aset:Bank:BCA                                     Rp 845.500
    Pendapatan:Penjualan                             -Rp 845.500

Simpan 12 transaksi? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode keluar: 0)

$ python3 hledger_usaha.py impor-bank mutasi-bca-agustus.csv --tahun 2026 --tetapkan 7=Pendapatan:Penjualan --tetapkan 10=HPP:Pembelian --tetapkan 16=Modal:Setoran --ya
IMPOR MUTASI BANK: TERSIMPAN
File: mutasi-bca-agustus.csv -> rekening Aset:Bank:BCA
Kolom terbaca: Tanggal Transaksi, Keterangan, Jumlah, kolom_5, Saldo
Terbaca 12 transaksi (2026-08-01 s.d. 2026-08-31); 0 sudah pernah diimpor (dilewati); 12 baru.
Uang masuk Rp 3.891.734,56 | uang keluar Rp 8.800.500
Uji silang aturan dengan hledger: COCOK (12 baris)
Baris dilewati: baris 19 (tanggal tidak dikenali: Saldo Awal); baris 20 (tanggal tidak dikenali: Mutasi Kredit); baris 21 (tanggal tidak dikenali: Mutasi Debet); baris 22 (tanggal tidak dikenali: Saldo Akhir)

RINGKASAN PER AKUN
- Pendapatan:Penjualan: 3 transaksi, masuk Rp 3.590.500
- Beban:Gaji: 1 transaksi, keluar Rp 3.000.000
- HPP:Pembelian: 1 transaksi, keluar Rp 2.250.000
- Beban:Sewa: 1 transaksi, keluar Rp 2.000.000
- Aset:Kas: 1 transaksi, keluar Rp 1.000.000
- Beban:Listrik Air Internet: 1 transaksi, keluar Rp 500.000
- Modal:Setoran: 1 transaksi, masuk Rp 300.000
- Beban:Transportasi: 1 transaksi, keluar Rp 38.000
- Beban:Admin Bank: 1 transaksi, keluar Rp 12.500
- Pendapatan:Lain-lain: 1 transaksi, masuk Rp 1.234,56

Cek saldo: saldo bank sebelum transaksi pertama Rp 8.600.000; saldo Aset:Bank:BCA di catatan sebelum tanggal itu Rp 8.600.000.
COCOK. Setelah impor, saldo catatan akan sama dengan saldo akhir bank Rp 3.691.234,56.
Tersimpan 12 transaksi ke ~/Pembukuan/usaha.journal. Salinan mutasi rapi: ~/Pembukuan/impor/bca-2026-08-01-2026-08-31.csv
(kode keluar: 0)

$ python3 hledger_usaha.py impor-bank mutasi-bca-agustus.csv --tahun 2026
IMPOR MUTASI BANK (PRATINJAU, belum disimpan)
File: mutasi-bca-agustus.csv -> rekening Aset:Bank:BCA
Kolom terbaca: Tanggal Transaksi, Keterangan, Jumlah, kolom_5, Saldo
Terbaca 12 transaksi (2026-08-01 s.d. 2026-08-31); 12 sudah pernah diimpor (dilewati); 0 baru.
Uang masuk Rp 0 | uang keluar Rp 0
Uji silang aturan dengan hledger: COCOK (12 baris)
Baris dilewati: baris 19 (tanggal tidak dikenali: Saldo Awal); baris 20 (tanggal tidak dikenali: Mutasi Kredit); baris 21 (tanggal tidak dikenali: Mutasi Debet); baris 22 (tanggal tidak dikenali: Saldo Akhir)

Cek saldo: saldo bank sebelum transaksi pertama Rp 8.600.000; saldo Aset:Bank:BCA di catatan sebelum tanggal itu Rp 8.600.000.
COCOK. Setelah impor, saldo catatan akan sama dengan saldo akhir bank Rp 3.691.234,56.
Tidak ada transaksi baru untuk disimpan.
(kode keluar: 0)

$ python3 hledger_usaha.py tambah-aturan --kata ROASTERY GAYO --akun HPP:Pembelian --arah keluar --ya
ATURAN BARU untuk ~/Pembukuan/aturan-bank.rules:

# ditambahkan 2026-09-26 lewat tambah-aturan
if %keterangan ROASTERY GAYO
& %keluar [1-9]
 account2 HPP:Pembelian

TERSIMPAN. Aturan paling bawah menang bila beberapa aturan cocok.
(kode keluar: 0)

$ python3 hledger_usaha.py saldo --tanggal 2026-08-31 --nyata Aset:Bank:BCA=3.691.234,56
SALDO AKUN
Kopi Sari
Per 31 Agustus 2026

Aset:Bank:BCA: Rp 3.691.234,56
Dibanding saldo nyata Rp 3.691.234,56: COCOK.

Sumber: usaha.journal | Dihitung dengan: hledger 1.52.4
Uji silang pembaca bawaan: COCOK
(kode keluar: 0)

$ hledger bal Aset:Bank -e 2026-09-01   (hledger 1.52.4 asli)
        Rp 3.691.235  Aset:Bank:BCA
--------------------
        Rp 3.691.235  
```

**Catatan pembuat:** pengelompokan pembaca bawaan diuji silang dengan `hledger print --rules-file` (aturan yang sama) → COCOK 12/12. Saldo akhir catatan = saldo akhir mutasi sampai sen (Rp 3.691.234,56); tampilan `hledger bal` membulatkan ke Rp 3.691.235 karena format tampilan tanpa sen, sudah dijelaskan di panduan.
