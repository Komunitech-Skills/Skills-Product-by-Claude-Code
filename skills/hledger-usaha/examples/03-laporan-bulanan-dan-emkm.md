# 03 — Laporan bulanan + rekap untuk laporan-keuangan-emkm (uji pembuat, hledger 1.52.4 asli)

**Pengguna:** "Laporan keuangan Juli dong, sekalian yang format SAK EMKM buat pengajuan KUR."

```
$ python3 hledger_usaha.py bulanan --bulan 2026-07
RINGKASAN 1 JULI 2026 S.D. 31 JULI 2026
Kopi Sari
- Pendapatan: Rp 8.800.000
- Laba bersih: Rp 1.600.000
- Kas & bank akhir: Rp 10.000.000 (-Rp 2.000.000 dari awal bulan)
- Piutang (belum dibayar pelanggan): Rp 0
- Utang: Rp 6.100.000
- Neraca: seimbang

--------------------------------

LAPORAN LABA RUGI
Kopi Sari
Periode: 1 Juli 2026 s.d. 31 Juli 2026

PENDAPATAN
- Penjualan: Rp 8.800.000
Total pendapatan: Rp 8.800.000

HARGA POKOK PENJUALAN (HPP)
- Pembelian: Rp 3.500.000
- Penyesuaian Persediaan: Rp 300.000
Total HPP: Rp 3.800.000

LABA KOTOR: Rp 5.000.000 (56,8% dari pendapatan)

BEBAN USAHA
- Gaji: Rp 3.000.000
- Listrik Air Internet: Rp 350.000
- Bunga: Rp 50.000
Total beban: Rp 3.400.000

LABA BERSIH: Rp 1.600.000 (18,2% dari pendapatan)

--------------------------------

NERACA (POSISI KEUANGAN)
Kopi Sari
Per 31 Juli 2026

ASET (yang dimiliki)
- Bank: Rp 8.600.000
- Peralatan: Rp 4.500.000
- Persediaan: Rp 2.700.000
- Kas: Rp 1.400.000
Total aset: Rp 17.200.000

UTANG (kewajiban)
- Utang Bank: Rp 4.600.000
- Utang Usaha: Rp 1.500.000
Total utang: Rp 6.100.000

MODAL
- Saldo Awal: Rp 10.000.000
- Prive: -Rp 500.000
- Laba (rugi) tahun 2026 s.d. tanggal ini: Rp 1.600.000
Total modal: Rp 11.100.000

Cek: Aset = Utang + Modal (Rp 17.200.000). SEIMBANG.

--------------------------------

LAPORAN ARUS KAS
Kopi Sari
Periode: 1 Juli 2026 s.d. 31 Juli 2026

Kas & bank awal: Rp 12.000.000

ARUS KAS DARI OPERASI (jualan & biaya sehari-hari)
- Pendapatan:Penjualan: masuk Rp 8.050.000
- Beban:Gaji: keluar Rp 3.000.000
- HPP:Pembelian: keluar Rp 2.000.000
- Aset:Piutang Usaha: masuk Rp 750.000
- Beban:Listrik Air Internet: keluar Rp 350.000
- Beban:Bunga: keluar Rp 50.000
Bersih: +Rp 3.400.000

ARUS KAS DARI INVESTASI (beli/jual peralatan)
- Aset:Peralatan: keluar Rp 4.500.000
Bersih: -Rp 4.500.000

ARUS KAS DARI PENDANAAN (modal, prive, pinjaman)
- Modal:Prive: keluar Rp 500.000
- Utang:Bank: keluar Rp 400.000
Bersih: -Rp 900.000

Kenaikan (penurunan) kas: -Rp 2.000.000
Kas & bank akhir: Rp 10.000.000
- Aset:Bank:BCA: Rp 8.600.000
- Aset:Kas: Rp 1.400.000
Cek: kas akhir = saldo akun kas & bank. COCOK.
Pindah uang antar kas/bank sendiri tidak dihitung sebagai masuk/keluar.

Sumber: usaha.journal | Dihitung dengan: hledger 1.52.4
Uji silang pembaca bawaan: COCOK
Laporan manajemen dari catatan Anda sendiri, bukan laporan audit/pajak. Untuk bank/KUR format SAK EMKM, pakai perintah ekspor-emkm.
(kode keluar: 0)

$ python3 hledger_usaha.py ekspor-emkm --bulan 2026-07
EKSPOR BUKU KAS UNTUK LAPORAN SAK EMKM
Periode: 1 Juli 2026 s.d. 31 Juli 2026
File: ~/Pembukuan/ekspor/buku-kas-2026-07-01-2026-07-31.csv
10 baris (uang masuk/keluar kas & bank; pindah dana sendiri tidak ikut).

Saldo dari jurnal untuk dipakai laporan-keuangan-emkm:
- kas-awal: Rp 12.000.000
- piutang-awal: Rp 0
- piutang-akhir: Rp 0
- persediaan-awal: Rp 3.000.000
- persediaan-akhir: Rp 2.700.000
- aset-tetap-awal: Rp 0
- utang-usaha-awal: Rp 0
- utang-usaha-akhir: Rp 1.500.000
- utang-bank-awal: Rp 5.000.000

Perintah (satu baris; jalankan dengan skill laporan-keuangan-emkm):
python3 <folder laporan-keuangan-emkm>/scripts/laporan_emkm.py "~/Pembukuan/ekspor/buku-kas-2026-07-01-2026-07-31.csv" --nama-usaha "Kopi Sari" --periode-awal 2026-07-01 --periode-akhir 2026-07-31 --kas-awal 12000000 --piutang-awal 0 --piutang-akhir 0 --persediaan-awal 3000000 --persediaan-akhir 2700000 --aset-tetap-awal 0 --utang-usaha-awal 0 --utang-usaha-akhir 1500000 --utang-bank-awal 5000000

Catatan: penjualan/pembelian tempo tercermin lewat saldo piutang/utang awal-akhir; aset tetap butuh --umur-aset-tahun bila ingin penyusutan.

Sumber: usaha.journal | Dihitung dengan: hledger 1.52.4
Uji silang pembaca bawaan: COCOK
(kode keluar: 0)

$ hledger is -p 2026-07   (pembanding, hledger 1.52.4 asli)
Income Statement 2026-07

                            ||          Jul 
============================++==============
 Revenues                   ||              
----------------------------++--------------
 Pendapatan:Penjualan       || Rp 8.800.000 
----------------------------++--------------
                            || Rp 8.800.000 
============================++==============
 Expenses                   ||              
----------------------------++--------------
 HPP:Pembelian              || Rp 3.500.000 
 HPP:Penyesuaian Persediaan ||   Rp 300.000 
 Beban:Gaji                 || Rp 3.000.000 
 Beban:Listrik Air Internet ||   Rp 350.000 
 Beban:Bunga                ||    Rp 50.000 
----------------------------++--------------
                            || Rp 7.200.000 
============================++==============
 Net:                       || Rp 1.600.000 
```

## Hasil skill laporan-keuangan-emkm dari file ekspor (perintah di atas dijalankan apa adanya)
```
Periode 1 Juli 2026 s.d. 31 Juli 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP (dengan asumsi)**
| **LABA (RUGI) BERSIH** | **Rp 1.600.000** |
| **Total aset** | **Rp 17.200.000** |
✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 17.200.000). Neraca seimbang.
```

**Verifikasi independen:** laba bersih Juli Rp 1.600.000 sama di (1) skill ini, (2) `hledger is` asli, dan (3) skill `laporan-keuangan-emkm` yang membaca ekspor buku kas + saldo dari jurnal. Total aset Rp 17.200.000 sama di neraca skill ini, `hledger bs`, dan laporan SAK EMKM. Arus kas: kas akhir Rp 10.000.000 = saldo Aset:Kas + Aset:Bank:BCA.
