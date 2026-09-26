# 04 — Input tidak lengkap, data rusak, dan tanpa hledger (uji pembuat)

Skenario: nominal ambigu, cara bayar tidak disebut, salah ketik akun, transaksi kembar, mutasi tanpa tahun / tanpa penanda CR/DB / file Excel / baris rusak, file jurnal yang diedit manual sampai tidak seimbang, file tidak ada, selisih kas, dan komputer tanpa hledger.

Yang diharapkan dari agent: menanyakan sekali apa yang kurang, tidak menebak, tidak menulis apa pun saat ada galat (file jurnal tetap utuh), dan tetap bisa bekerja tanpa hledger.

```
$ python3 hledger_usaha.py catat --jenis jual --nominal 62,500 --via kas
GAGAL: --nominal '62,500' ambigu: maksudnya 62,500 (desimal) atau 62.500? Tulis ulang tanpa koma atau dengan titik ribuan.
(kode keluar: 2)

$ python3 hledger_usaha.py catat --jenis jual --nominal 150rb
GAGAL: --via belum diisi: dibayar pakai kas (tunai), bank (transfer/QRIS), atau tempo (belum dibayar)?
(kode keluar: 2)

$ python3 hledger_usaha.py catat --jenis beban --nominal 20rb --via kas --akun Beban:Listrik Air Internt
GAGAL: Akun 'Beban:Listrik Air Internt' belum ada di jurnal. Mungkin maksudnya: Beban:Listrik Air Internet. Bila memang akun baru, ulangi dengan --akun-baru.
(kode keluar: 2)

$ python3 hledger_usaha.py catat --jenis jual --nominal 1.250.000 --via kas --tanggal 2026-07-01 --ket Penjualan harian kopi --ya
PRATINJAU CATATAN
File: ~/Pembukuan/usaha.journal

2026-07-01 Penjualan harian kopi
    Aset:Kas                                        Rp 1.250.000
    Pendapatan:Penjualan                           -Rp 1.250.000
Artinya: Penjualan Rp 1.250.000, uang masuk ke Aset:Kas.

KEMUNGKINAN DOBEL: transaksi ke-1 sama persis dengan catatan 2026-07-01 'Penjualan harian kopi'.
TIDAK DISIMPAN. Bila memang transaksi berbeda (mis. dua kali beli barang yang sama), ulangi dengan --tetap-catat.
(kode keluar: 7)

$ python3 hledger_usaha.py impor-bank mutasi-bca-agustus.csv
GAGAL: Tanggal di mutasi tanpa tahun (mis. '01/08'). Sebutkan --tahun 2026.
(kode keluar: 2)

$ python3 hledger_usaha.py impor-bank mutasi-tanpa-dk.csv
GAGAL: Kolom nominal tanpa penanda masuk/keluar (CR/DB) di baris 2. Sebutkan --kolom-dk atau --kolom-masuk/--kolom-keluar.
(kode keluar: 2)

$ python3 hledger_usaha.py impor-bank mutasi-excel.xlsx
GAGAL: File mutasi-excel.xlsx adalah Excel (.xlsx). Simpan sebagai CSV dulu.
(kode keluar: 2)

$ python3 hledger_usaha.py impor-bank mutasi-mandiri-rusak.csv --bank BCA
IMPOR MUTASI BANK (PRATINJAU, belum disimpan)
File: mutasi-mandiri-rusak.csv -> rekening Aset:Bank:BCA
Kolom terbaca: Tanggal, Keterangan, Debet, Kredit, Saldo
Terbaca 3 transaksi (2026-08-01 s.d. 2026-08-04); 0 sudah pernah diimpor (dilewati); 3 baru.
Uang masuk Rp 750.000 | uang keluar Rp 1.500.000
Uji silang aturan dengan hledger: COCOK (3 baris)
Baris dilewati: baris 4 (tanggal tidak dikenali: tanggal-rusak); baris 5 (nominal 0/kosong); baris 7 (masuk dan keluar sekaligus terisi)

RINGKASAN PER AKUN
- Beban:Belum Dikelompokkan: 1 transaksi, keluar Rp 1.500.000
- Aset:Kas: 1 transaksi, masuk Rp 500.000
- Pendapatan:Penjualan: 1 transaksi, masuk Rp 250.000

PERLU DITANYAKAN KE PENGGUNA (1 transaksi belum dikelompokkan):
- baris 3: 2026-08-02 TRF KE CV SUSU SEGAR keluar Rp 1.500.000
Tetapkan dengan --tetapkan "BARIS=Akun", atau simpan kata kuncinya untuk bulan depan dengan perintah tambah-aturan.
PERINGATAN: kolom saldo di file tidak konsisten dengan mutasinya (ada baris hilang/terpotong?).

Contoh 2 transaksi pertama:
2026-08-01 SETOR TUNAI KOPI SARI  ; ref:20fa906c461b, sumber:mutasi-bank
    Aset:Bank:BCA                                     Rp 500.000
    Aset:Kas                                         -Rp 500.000
2026-08-02 TRF KE CV SUSU SEGAR  ; ref:da1cec91a677, sumber:mutasi-bank
    Aset:Bank:BCA                                  -Rp 1.500.000
    Beban:Belum Dikelompokkan                       Rp 1.500.000

Simpan 3 transaksi? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode keluar: 0)

$ python3 hledger_usaha.py catat --jurnal rusak.journal --jenis jual --nominal 10rb --via kas --ya
GAGAL: hledger menolak file jurnal:
hledger: Error: ~/rusak.journal:172-174:
172 | 2026-08-15 Diedit manual, salah ketik
    |     Aset:Kas                 Rp 100.000,
    |     Pendapatan:Penjualan     Rp -10.000,
This transaction is unbalanced.
The real postings' sum should be 0 but is: Rp 90.000
(kode keluar: 4)

$ python3 hledger_usaha.py laba-rugi --jurnal rusak.journal --bulan 2026-08 --mesin bawaan
GAGAL: baris 172: transaksi 'Diedit manual, salah ketik' tidak seimbang (selisih Rp 90.000).
(kode keluar: 4)

$ python3 hledger_usaha.py laba-rugi --jurnal tidak-ada.journal
GAGAL: File jurnal tidak ditemukan: ~/tidak-ada.journal
Buat dulu dengan perintah `init`, atau sebutkan --jurnal <path>.
(kode keluar: 3)

$ python3 hledger_usaha.py saldo Aset:Kas --tanggal 2026-08-31 --nyata Aset:Kas=2.300.000
SALDO AKUN
Kopi Sari
Per 31 Agustus 2026

Aset:Kas: Rp 2.400.000
Dibanding saldo nyata Rp 2.300.000: SELISIH Rp 100.000 (catatan lebih besar dari kenyataan).

Sumber: usaha.journal | Dihitung dengan: hledger 1.52.4
Uji silang pembaca bawaan: COCOK
(kode keluar: 1)

# Tanpa hledger terpasang (PATH tanpa hledger):
$ python3 hledger_usaha.py cek --jurnal Pembukuan/usaha.journal
CEK HLEDGER-USAHA (skill v1.0.0)
hledger: TIDAK ditemukan. Skill tetap bisa mencatat & membuat laporan dengan pembaca bawaan. Pasang hledger (gratis) lewat docs/panduan-hledger.md untuk pemeriksaan lengkap & hledger-web.
File jurnal: ~/Pembukuan/usaha.journal (26 transaksi, 2026-06-30 s.d. 2026-08-31)
Pemeriksaan bawaan: seimbang & saldo LULUS; semua akun terdaftar
(kode keluar: 0)

$ python3 hledger_usaha.py laba-rugi --bulan 2026-08
LAPORAN LABA RUGI
Kopi Sari
Periode: 1 Agustus 2026 s.d. 31 Agustus 2026

PENDAPATAN
- Penjualan: Rp 3.590.500
- Lain-lain: Rp 1.234,56
Total pendapatan: Rp 3.591.734,56

HARGA POKOK PENJUALAN (HPP)
- Pembelian: Rp 2.250.000
Total HPP: Rp 2.250.000

LABA KOTOR: Rp 1.341.734,56 (37,4% dari pendapatan)

BEBAN USAHA
- Gaji: Rp 3.000.000
- Sewa: Rp 2.000.000
- Listrik Air Internet: Rp 500.000
- Transportasi: Rp 38.000
- Admin Bank: Rp 12.500
Total beban: Rp 5.550.500

RUGI BERSIH: Rp 4.208.765,44 (-117,2% dari pendapatan)

Sumber: usaha.journal | Dihitung dengan: pembaca bawaan skill (hledger belum terpasang)
Laporan manajemen dari catatan Anda sendiri, bukan laporan audit/pajak. Untuk bank/KUR format SAK EMKM, pakai perintah ekspor-emkm.
(kode keluar: 0)

```

**Catatan pembuat:** tidak ada satu pun perintah galat di atas yang mengubah `usaha.journal` (diperiksa byte demi byte di `tests/uji_regresi.py`). Baris mutasi rusak dilewati dengan alasan, dan kolom saldo yang tidak konsisten (karena satu baris rusak dilewati) dilaporkan sebagai PERINGATAN. Tanpa hledger, laporan tetap keluar dengan label mesin "pembaca bawaan".
