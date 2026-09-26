# Contoh 02 — Daftar biasa → CSV Import Wizard Frappe Books (keluaran NYATA script)

**Konteks:** pemilik mengirim tiga daftar dari Excel (disimpan sebagai CSV bertitik koma) dan berkata:
*"Tolong masukkan pelanggan, barang, dan nota ini ke Frappe Books."* Semua nama **fiktif**.
Database tiruan sama dengan contoh 01 (ditemukan otomatis di `~/Documents/Frappe Books/`).
Dijalankan ulang 26 September 2026, `frappe_books.py` 1.0.1 (database tiruan meniru file asli: akun bernomor, Party tanpa kolom Tax ID).

Yang ditunjukkan: judul kolom bahasa sehari-hari dikenali, `Rp 95.000`/`18rb`/`1,5jt` dibaca benar, nomor HP dirapikan ke +62,
nama yang sudah ada dilewati, satuan yang belum ada ditolak, tanggal mustahil ditolak, huruf besar/kecil nama disamakan
dengan data (`warung bu sari` → `Warung Bu Sari`), akun bernomor dipilih dengan aturan tetap (`Penjualan - 4110.000`, bukan
`Pendapatan Bunga Bank`), kolom Number Series `SINV-` ditulis, NPWP yang tidak bisa diimpor disebutkan, `--keluar` ke file
database ditolak, PPN pratinjau memakai standar Komunitech.

```text
=== isi pelanggan.csv (dari pengguna)
Nama Pelanggan;No HP;Email;NPWP
Kedai Kopi Senja;0812-3456-7890;senja@contoh.id;01.234.567.8-901.000
Toko Sinar Abadi;081234567001;;
CV Berkah, Solo;62811222333;;
Bu Rina (catering);+62 857 1111 2222;rina@contoh;

=== isi barang.csv (dari pengguna)
nama barang;sku;satuan;harga jual;jenis;stok
Kopi Liberika 200g;KPL-200;Unit;Rp 95.000;barang;ya
Susu UHT 1L;SUS-1;Liter;18rb;barang;ya
Kelas Barista;;;1,5jt;jasa;

=== isi nota.csv (dari pengguna)
No Nota;Tanggal;Pelanggan;Barang;Jumlah;Harga;Pajak
N-01;27/09/2026;Toko Sinar Abadi;Kopi Arabika 250g;3;85.000;PPN 11% (12% x 11/12)
N-01;27/09/2026;Toko Sinar Abadi;Gula Aren 1kg;2;32.500;PPN 11% (12% x 11/12)
N-01;27/09/2026;Toko Sinar Abadi;Jasa Seduh Event;1;12345;PPN 11% (12% x 11/12)
N-02;28 Sep 2026;warung bu sari;kopi robusta 1kg;1;150rb;
N-03;31/09/2026;Kedai Kopi Senja;Kopi Arabika 250g;2;85000;

$ python3 scripts/frappe_books.py akun
AKUN (bukan grup) - pakai nama PERSIS seperti di bawah untuk CSV:
- Kas Besar - 1111.001 (Aset) [Cash]
- Persediaan Barang - 1141.000 (Aset) [Stock]
- Piutang Dagang - 1131.0010 (Aset) [Receivable]
- HUtang Dagang Biaya Kirim Luar Negeri - 2111.004 (Kewajiban) [Payable]
- Hutang Dagang Dalam Negeri - 2111.001 (Kewajiban) [Payable]
- Hutang Dagang Luar Negeri - 2111.002 (Kewajiban) [Payable]
- Hutang Pajak - 2141.000 (Kewajiban) [Payable]
- Stock Diterima Tapi Tidak Ditagih - 2115.000 (Kewajiban) [Stock Received But Not Billed]
- HPP Pembelian - 4210.000 (Pendapatan) [Cost of Goods Sold]
- Pendapatan Bunga Bank - 4410.000 (Pendapatan)
- Pendapatan Service - 4310.000 (Pendapatan)
- Penjualan - 4110.000 (Pendapatan)
- Retur Penjualan - 4120.000 (Pendapatan)
- Biaya PLN Gudang & Kantor - 5130.001 (Beban)
- Biaya Sewa Kantor - 5130.013 (Beban)
SATUAN (UOM): Day, Gram, Hour, Kg, Meter, Unit
LOKASI GUDANG: Gudang, Stores
PAJAK (template Tax):
- PPN 11% (12% x 11/12): 11% ke akun Hutang Pajak - 2141.000
(kode keluar 0)

$ python3 scripts/frappe_books.py csv-pelanggan --masuk pelanggan.csv --keluar impor-pelanggan.csv
(Memakai database Frappe Books: ~/Documents/Frappe Books/Toko Kopi Nusantara.books.db)
VALIDASI CSV PELANGGAN/PEMASOK (Frappe Books: Party)
Perlu dicek (tidak menghalangi):
  - baris 3: 'Toko Sinar Abadi' sudah ada di Frappe Books -> dilewati
  - baris 5: email 'rina@contoh' tampak salah, dikosongkan
  - NPWP '01.234.567.8-901.000' milik 'Kedai Kopi Senja' TIDAK ikut diimpor: file Frappe Books ini tidak punya kolom Tax ID. Catat manual setelah impor (mis. di data pelanggan atau alamat).
LOLOS: 3 pihak siap diimpor -> impor-pelanggan.csv
Langkah di Frappe Books: menu Import Wizard (Setup/Pengaturan) > pilih jenis 'Party' > Select File > pilih file ini >
periksa pratinjau (kolom merah = salah) > Import Data. Saat ditanya 'submit after syncing', jawab TIDAK untuk transaksi
agar masuk sebagai draf dan bisa dicek dulu. Backup file .books.db sebelum impor pertama.
(kode keluar 0)

$ python3 scripts/frappe_books.py csv-barang --masuk barang.csv --keluar impor-barang.csv
(Memakai database Frappe Books: ~/Documents/Frappe Books/Toko Kopi Nusantara.books.db)
VALIDASI CSV BARANG (Frappe Books: Item)
TIDAK LOLOS: 1 masalah harus diperbaiki dulu (file CSV TIDAK dibuat):
  - baris 3: satuan 'Liter' belum ada di Frappe Books (yang ada: Day, Gram, Hour, Kg, Meter, Unit). Tambahkan dulu satuan itu atau ganti.
(kode keluar 5)

=== pengguna mengganti satuan 'Liter' menjadi 'Unit' pada baris Susu UHT, lalu menjalankan ulang
$ python3 scripts/frappe_books.py csv-barang --masuk barang.csv --keluar impor-barang.csv
(Memakai database Frappe Books: ~/Documents/Frappe Books/Toko Kopi Nusantara.books.db)
VALIDASI CSV BARANG (Frappe Books: Item)
LOLOS: 3 barang/jasa siap diimpor -> impor-barang.csv
Akun penjualan: Penjualan - 4110.000 (jasa: Pendapatan Service - 4310.000) | akun pembelian: HPP Pembelian - 4210.000
Langkah di Frappe Books: menu Import Wizard (Setup/Pengaturan) > pilih jenis 'Item' > Select File > pilih file ini >
periksa pratinjau (kolom merah = salah) > Import Data. Saat ditanya 'submit after syncing', jawab TIDAK untuk transaksi
agar masuk sebagai draf dan bisa dicek dulu. Backup file .books.db sebelum impor pertama.
(kode keluar 0)

=== impor-pelanggan.csv (hasil)
Party,Party,Party,Party
Name,Role,Email,Phone
Party.name,Party.role,Party.email,Party.phone
Kedai Kopi Senja,Customer,senja@contoh.id,+6281234567890
"CV Berkah, Solo",Customer,,+62811222333
Bu Rina (catering),Customer,,+6285711112222

=== impor-barang.csv (hasil)
Item,Item,Item,Item,Item,Item,Item,Item,Item,Item,Item
Item Name,Item Code,Purpose,Type,Unit Type,Rate,Description,Sales Acc.,Purchase Acc.,Barcode,Track Inventory
Item.name,Item.itemCode,Item.for,Item.itemType,Item.unit,Item.rate,Item.description,Item.incomeAccount,Item.expenseAccount,Item.barcode,Item.trackItem
Kopi Liberika 200g,KPL-200,Both,Product,Unit,95000,,Penjualan - 4110.000,HPP Pembelian - 4210.000,,1
Susu UHT 1L,SUS-1,Both,Product,Unit,18000,,Penjualan - 4110.000,HPP Pembelian - 4210.000,,1
Kelas Barista,,Both,Service,Hour,1500000,,Pendapatan Service - 4310.000,HPP Pembelian - 4210.000,,0

$ python3 scripts/frappe_books.py csv-transaksi --masuk nota.csv --keluar impor-nota.csv
(Memakai database Frappe Books: ~/Documents/Frappe Books/Toko Kopi Nusantara.books.db)
VALIDASI CSV PENJUALAN (Frappe Books: SalesInvoice)
TIDAK LOLOS: 1 masalah harus diperbaiki dulu (file CSV TIDAK dibuat):
  - baris 6: tanggal '31/09/2026' tidak ada di kalender
(kode keluar 5)

=== pengguna menunda nota N-03 (tanggal salah & pelanggan belum diimpor), menghapus barisnya, lalu menjalankan ulang
$ python3 scripts/frappe_books.py csv-transaksi --masuk nota.csv --keluar impor-nota.csv
(Memakai database Frappe Books: ~/Documents/Frappe Books/Toko Kopi Nusantara.books.db)
VALIDASI CSV PENJUALAN (Frappe Books: SalesInvoice)
LOLOS: 2 nota (4 baris barang) siap diimpor -> impor-nota.csv
Pratinjau per nota (hitungan Komunitech):
  - N-01 | 27 Sep 2026 | Toko Sinar Abadi | DPP Rp 332.345 | PPN (standar Komunitech) Rp 36.557 | total Rp 368.902
  - N-02 | 28 Sep 2026 | Warung Bu Sari | DPP Rp 150.000
Total DPP semua nota: Rp 482.345
Akun piutang: Piutang Dagang - 1131.0010 | Number Series: SINV-
Kolom 'Invoice No' (IMPOR-...) hanya pengelompok baris; nomor final diberi otomatis oleh Number Series SINV-.
Langkah di Frappe Books: menu Import Wizard (Setup/Pengaturan) > pilih jenis 'Sales Invoice' > Select File > pilih file ini >
periksa pratinjau (kolom merah = salah) > Import Data. Saat ditanya 'submit after syncing', jawab TIDAK untuk transaksi
agar masuk sebagai draf dan bisa dicek dulu. Backup file .books.db sebelum impor pertama.
Setelah impor, cocokkan total tiap invoice di Frappe Books dengan pratinjau di atas. Pajak di Frappe Books dihitung per baris tanpa pembulatan ke bawah, jadi bisa beda pecahan rupiah.
(kode keluar 0)

=== impor-nota.csv (hasil)
Sales Invoice,Sales Invoice,Sales Invoice,Sales Invoice,Sales Invoice,Sales Invoice,Sales Invoice Item,Sales Invoice Item,Sales Invoice Item,Sales Invoice Item,Sales Invoice Item
Invoice No,Number Series,Customer,Account,Date,Notes,Item,Rate,Quantity,Account,Tax
SalesInvoice.name,SalesInvoice.numberSeries,SalesInvoice.party,SalesInvoice.account,SalesInvoice.date,SalesInvoice.terms,SalesInvoiceItem.item,SalesInvoiceItem.rate,SalesInvoiceItem.quantity,SalesInvoiceItem.account,SalesInvoiceItem.tax
IMPOR-N-01,SINV-,Toko Sinar Abadi,Piutang Dagang - 1131.0010,2026-09-27,,Kopi Arabika 250g,85000,3,Penjualan - 4110.000,PPN 11% (12% x 11/12)
IMPOR-N-01,SINV-,Toko Sinar Abadi,Piutang Dagang - 1131.0010,2026-09-27,,Gula Aren 1kg,32500,2,Penjualan - 4110.000,PPN 11% (12% x 11/12)
IMPOR-N-01,SINV-,Toko Sinar Abadi,Piutang Dagang - 1131.0010,2026-09-27,,Jasa Seduh Event,12345,1,Pendapatan Service - 4310.000,PPN 11% (12% x 11/12)
IMPOR-N-02,SINV-,Warung Bu Sari,Piutang Dagang - 1131.0010,2026-09-28,,Kopi Robusta 1kg,150000,1,Penjualan - 4110.000,

=== pengaman: pengguna tidak sengaja menulis nama file database sebagai tujuan
$ python3 scripts/frappe_books.py csv-transaksi --masuk nota.csv --keluar ~/Documents/Frappe Books/Toko Kopi Nusantara.books.db
GAGAL: --keluar 'Toko Kopi Nusantara.books.db' harus berakhiran .csv (file ini TIDAK ditulis).
Saran: Pakai nama file baru berakhiran .csv, mis. impor-pelanggan.csv, di folder lain dari file .books.db.
(kode keluar 2)
```

## Catatan
- Nota N-03 hanya menampilkan galat tanggal; setelah tanggal dibetulkan, script akan menolak "Kedai Kopi Senja" sampai
  `impor-pelanggan.csv` benar-benar sudah diimpor di Frappe Books (urutan: pelanggan & barang dulu, baru nota).
- PPN N-01 di Frappe Books akan tampil Rp 36.557,95 (pajak per baris tanpa pembulatan); standar Komunitech Rp 36.557
  (dibulatkan ke bawah). Pembulatan belum dicocokkan dengan Coretax.
- File CSV hasil memakai 3 baris judul seperti template resmi Import Wizard (`references/import-wizard.md`).
  v1.0.0 (tanpa Number Series) ditolak Import Wizard asli; penguji menambah kolom `SINV-` dan impor berhasil. CSV v1.0.1 di atas
  sudah berisi kolom itu tetapi **belum diuji ulang** di Import Wizard asli.

## Jawaban agent ke pemilik (ringkas)
> Sudah saya siapkan 3 file. **Sebelum impor, salin dulu file `Toko Kopi Nusantara.books.db` ke folder lain (backup).**
> Urutannya: 1) Import Wizard → Party → `impor-pelanggan.csv` (3 pelanggan baru; Toko Sinar Abadi sudah ada; email Bu Rina
> kosong karena tampak salah; NPWP Kedai Kopi Senja 01.234.567.8-901.000 harus dicatat manual karena Frappe Books Anda tidak punya kolom NPWP); 2) Item → `impor-barang.csv` (3 barang); 3) Sales Invoice → `impor-nota.csv` (2 nota), pilih
> **tidak submit** supaya masuk draf, lalu cocokkan: N-01 total Rp 368.902, N-02 Rp 150.000. Nota N-03 tanggalnya 31/09
> (tidak ada) — tanggal benarnya berapa?
