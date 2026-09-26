# Contoh 2 — Impor mutasi bank & rekap kasir-lokal (dengan penjagaan dobel)

Dijalankan sungguhan dengan `scripts/kas.py` oleh pembuat skill (26/09/2026), melanjutkan buku kas Contoh 1.
**Semua data fiktif** (nomor rekening dan nama pelanggan karangan). Output dipotong seperlunya; angka tidak diubah.

## File mutasi dari internet banking (CSV, format angka Inggris, tanggal tanpa tahun)
```
Mutasi Rekening BRI (fiktif) periode 21/09 - 25/09
No. rekening : 0000-00-000000-00-0
Tanggal Transaksi,Keterangan,Cabang,Jumlah,Saldo
21/09,TRSF CR KATERING ARISAN BU RINA,0998,"750,000.00 CR","10,990,000.00"
22/09,TARIKAN ATM 22/09,0998,"500,000.00 DB","10,490,000.00"
23/09,BIAYA ADM,0000,"12,500.00 DB","10,477,500.00"
24/09,TRSF DB PLN PASCABAYAR,0998,"185,000.00 DB","10,292,500.00"
25/09,BUNGA,0000,"1,234.56 CR","10,293,734.56"
PEND,TRSF MASUK,0000,"100,000.00 CR",
```
Pengguna: *"Masukin mutasi BRI minggu ini ke buku kas."*

## 1. Pratinjau pertama: tanggal tanpa tahun ditolak
```
$ kas.py impor mutasi-bri-sep.csv --akun BRI
PRATINJAU (belum disimpan):
Impor mutasi-bri-sep.csv: 0 baris akan dicatat (masuk Rp 0, keluar Rp 0).
Baris dilewati: 9 (tanggal kosong/PEND (transaksi belum dibukukan bank)).
Baris BERMASALAH (tidak diimpor): 4: tanggal tanpa tahun ('21/09'); ulangi dengan --tahun YYYY; 5: ... 8: tanggal tanpa tahun ('25/09'); ulangi dengan --tahun YYYY.
```
Agent memastikan ke pengguna bahwa mutasinya tahun 2026, lalu:
```
$ kas.py impor mutasi-bri-sep.csv --akun BRI --tahun 2026
PRATINJAU (belum disimpan):
Impor mutasi-bri-sep.csv: 5 baris akan dicatat (masuk Rp 751.235, keluar Rp 697.500).
Tanggal 21/09/2026 - 25/09/2026. Per kategori: Pemasukan lain-lain Rp 751.235, Pengeluaran lain-lain Rp 512.500, Listrik/air Rp 185.000.
- baris 4: 21/09/2026 masuk Rp 750.000 | Pemasukan lain-lain | TRSF CR KATERING ARISAN BU RINA (belum jelas)
- baris 5: 22/09/2026 keluar Rp 500.000 | Pengeluaran lain-lain | TARIKAN ATM 22/09 (belum jelas)
- baris 6: 23/09/2026 keluar Rp 12.500 | Pengeluaran lain-lain | BIAYA ADM (ditebak dari keterangan)
- baris 7: 24/09/2026 keluar Rp 185.000 | Listrik/air | TRSF DB PLN PASCABAYAR (ditebak dari keterangan)
- baris 8: 25/09/2026 masuk Rp 1.235 | Pemasukan lain-lain | BUNGA (ditebak dari keterangan)
PERLU DICEK KE PENGGUNA (2 baris, sementara dicatat lain-lain):
- baris 4: masuk Rp 750.000 'TRSF CR KATERING ARISAN BU RINA' -> kategori belum jelas. Saran: --tetapkan 4=<kategori>
- baris 5: keluar Rp 500.000 'TARIKAN ATM 22/09' -> mungkin pindah dana (tarik/setor tunai/top up). Saran: --tetapkan 5=pindah:<akun pasangan> atau 5=prive / 5=modal
Baris dilewati: 9 (tanggal kosong/PEND (transaksi belum dibukukan bank)).
Catatan: 1 nominal bersen dibulatkan ke rupiah terdekat (0,5 ke atas).
```
Agent menggabungkan dua pertanyaan dalam **satu pesan**:
1. *"Transfer Rp 750.000 dari Bu Rina (katering arisan): ini penjualan?"*
2. *"Tarik ATM Rp 500.000 tanggal 22/09: uangnya dimasukkan ke laci warung, atau dipakai pribadi?"*

Pengguna: *"1 penjualan, 2 masuk laci buat kembalian."*
```
$ kas.py impor mutasi-bri-sep.csv --akun BRI --tahun 2026 --tetapkan 5=pindah:laci --tetapkan 4=penjualan --ya
TERSIMPAN.
Impor mutasi-bri-sep.csv: 5 baris dicatat (masuk Rp 751.235, keluar Rp 197.500).
Tanggal 21/09/2026 - 25/09/2026. Per kategori: Penjualan Rp 750.000, Pindah dana Rp 500.000, Pengeluaran lain-lain Rp 12.500, Listrik/air Rp 185.000, Pemasukan lain-lain Rp 1.235.
- baris 4: 21/09/2026 masuk Rp 750.000 | Penjualan | TRSF CR KATERING ARISAN BU RINA (ditetapkan pengguna)
- baris 5: 22/09/2026 keluar Rp 500.000 | Pindah ke/dari Laci kas | TARIKAN ATM 22/09 (ditetapkan pengguna)
- baris 6: 23/09/2026 keluar Rp 12.500 | Pengeluaran lain-lain | BIAYA ADM (ditebak dari keterangan)
- baris 7: 24/09/2026 keluar Rp 185.000 | Listrik/air | TRSF DB PLN PASCABAYAR (ditebak dari keterangan)
- baris 8: 25/09/2026 masuk Rp 1.235 | Pemasukan lain-lain | BUNGA (ditebak dari keterangan)
Baris dilewati: 9 (tanggal kosong/PEND (transaksi belum dibukukan bank)).
Catatan: 1 nominal bersen dibulatkan ke rupiah terdekat (0,5 ke atas).
```
(Cadangan otomatis `kas-...-sebelum-impor.db` dibuat sebelum menyimpan.)

## 2. File yang sama tidak sengaja diimpor lagi
```
$ kas.py impor mutasi-bri-sep.csv --akun BRI --tahun 2026
PRATINJAU (belum disimpan):
Impor mutasi-bri-sep.csv: 0 baris akan dicatat (masuk Rp 0, keluar Rp 0).
Dilewati karena sudah pernah diimpor: 5 baris.
Baris dilewati: 9 (tanggal kosong/PEND (transaksi belum dibukukan bank)).

$ kas.py saldo
Saldo per akhir Sabtu, 26/09/2026:
- Laci kas: Rp 3.329.000
- BRI: Rp 11.533.735
Total: Rp 14.862.735
```
Cek manual: BRI 11.480.000 + 750.000 − 500.000 − 12.500 − 185.000 + 1.235 = 11.533.735.
Laci 2.829.000 + 500.000 (tarik ATM masuk laci) = 3.329.000. Hasil usaha tidak berubah karena tarik tunai = pindah dana.

## 3. Rekap kasir-lokal untuk tanggal yang penjualannya sudah dicatat manual
Pengguna baru mulai memakai kasir-lokal dan ingin memasukkan rekap kasir 25/09 (isi file JSON fiktif, format sama
persis dengan `kasir.py rekap --tanggal 25/09/2026 --json`: `per_metode` Tunai 905.000, QRIS 360.000).
```
$ kas.py impor-kasir rekap-kasir-25-09.json
PRATINJAU (belum disimpan):
Impor rekap kasir-lokal Jumat, 25/09/2026 (uang diterima Rp 1.265.000):
- MASUK  Rp 905.000 | 25/09/2026 | Penjualan | Tunai -> Laci kas | Penjualan kasir 25/09/2026 (Tunai)
- MASUK  Rp 360.000 | 25/09/2026 | Penjualan | QRIS -> BRI | Penjualan kasir 25/09/2026 (QRIS)
Pengeluaran laci (kasir.py kas --keluar) TIDAK ikut; catat pengeluaran usaha di buku kas ini.

PERLU KEPUTUSAN PENGGUNA sebelum disimpan:
- Sudah ada catatan penjualan 25/09/2026 dari sumber lain (#58, #59, total Rp 840.000). Jika itu penjualan yang sama dengan rekap kasir, impor ini membuat penjualan DOBEL: batalkan catatan lama dulu (kas.py batal) atau jangan impor. Jika memang penjualan berbeda (mis. pesanan di luar kasir), ulangi dengan --izinkan-duplikat.
```
Agent bertanya: *"Tanggal 25/09 sudah ada catatan jualan Rp 840.000 (dari buku kas lama). Rekap kasir Rp 1.265.000
itu penjualan yang sama atau berbeda?"* Jika sama → batalkan #58 dan #59 (`batal --id 58 --alasan "diganti rekap
kasir"`, dst.) lalu impor. Menjalankan `--ya` tanpa keputusan ini ditolak script ("BELUM DISIMPAN").
