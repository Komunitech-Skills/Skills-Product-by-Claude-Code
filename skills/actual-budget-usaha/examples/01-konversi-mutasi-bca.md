# Contoh 01 — Mutasi BCA September → CSV impor Actual

Hasil nyata `scripts/actual_budget.py` v1.0.9 (dijalankan ulang 22 Oktober 2026). Data **fiktif**:
mutasi `tests/fixtures/mutasi/bca-sep-2026.csv` dan budget Actual 26.9.0 asli "Studio Rina (fiktif)".

## Permintaan pengguna
> "Ini mutasi BCA September, tolong masukin ke Actual ya. Kategorinya yang biasa aja."

## 1. Percobaan pertama: tahun tidak ada di file
```
$ python3 scripts/actual_budget.py konversi mutasi-bca-sep.csv --db Studio-Rina
GAGAL: Tanggal di mutasi tanpa tahun (mis. '01/09', khas BCA). Sebutkan tahunnya: --tahun 2026.
```
Agent bertanya sekali: "Mutasi BCA tidak mencantumkan tahun. Ini September 2026, kan?" → pengguna: "iya".

## 2. Konversi (dengan aturan kategori milik pengguna, `aturan-kategori.csv`)
```
kata_kunci,kategori,arah
FACEBK,Iklan,keluar
COWORKING,Sewa Coworking,keluar
TRSF E-BANKING CR,Pendapatan Proyek,masuk
```
```
$ python3 scripts/actual_budget.py konversi mutasi-bca-sep.csv --db Studio-Rina --tahun 2026 --peta aturan-kategori.csv
KONVERSI MUTASI -> CSV IMPOR ACTUAL
File mutasi: mutasi-bca-sep.csv
Periode: 1 September 2026 s.d. 30 September 2026
Terbaca: 13 transaksi | Dilewati: 5 | Perlu dicek: 5
Total masuk: Rp 10.262.345,67 | Total keluar: Rp 8.019.969,13
Cek saldo bank: COCOK (saldo awal Rp 5.000.000 -> saldo akhir Rp 7.242.376,54)

RINGKASAN PER KATEGORI USULAN
- Iklan: 1 baris, -Rp 3.200.000
- (menunggu konfirmasi usulan): 5 baris, -Rp 2.487.500
- Sewa Coworking: 1 baris, -Rp 1.500.000
- Transportasi: 1 baris, -Rp 450.000
- Internet & Pulsa: 1 baris, -Rp 380.000
- Pajak: 1 baris, -Rp 2.469,13
- Pendapatan Lain: 1 baris, Rp 12.345,67
- Pendapatan Proyek: 2 baris, Rp 10.250.000

PERLU KONFIRMASI (5 transaksi, daftar teknis juga di mutasi-bca-sep-actual-ragu.csv):
Usulan saya per transaksi (sebut tanggal + keterangan + nominal, jangan nomor baris):
- 2 September 2026 | BIAYA ADM | -Rp 10.000 -> usulan: Biaya Bank (belum ada, buat dulu) - paling cocok menurut keterangan transaksinya
- 3 September 2026 | TRSF E-BANKING DB 0309/FTFVA/WS95051 70001/PLN PRABAYAR | -Rp 502.500 -> usulan: Listrik & Air (belum ada, buat dulu) - paling cocok menurut keterangan transaksinya
- 10 September 2026 | TARIKAN ATM 10/09 ATM BCA | -Rp 1.000.000 -> usulan: pindah dana ke akun sendiri (tanpa kategori) - uang cuma pindah dompet/rekening milik sendiri, bukan pengeluaran usaha
- 18 September 2026 | KARTU DEBIT TOKOPEDIA | -Rp 700.000 -> usulan: Perlengkapan Usaha (belum ada, buat dulu) - belanja online paling sering untuk bahan/peralatan usaha
- 24 September 2026 | QRIS TOKO XYZ 99231 | -Rp 275.000 -> usulan: Biaya Lain-lain (belum ada, buat dulu) - belum ada kata kunci yang cocok, ditaruh sementara di biaya umum

SATU PERTANYAAN UNTUK PENGGUNA: balas 'ya' untuk memakai semua usulan di atas, atau sebut transaksi yang mau diganti (tanggal/keterangan) beserta kategori yang diinginkan.
Kategori yang ada di budget: Arsip Lama, Iklan, Transportasi, Software & Langganan, Internet & Pulsa, Sewa Coworking, Belanja Rumah, Makan, Dana Darurat, Pajak

DILEWATI (5 baris, tidak masuk file hasil):
- PEND | TRSF E-BANKING DB 3009 SHOPEE | 150,000.00 -> transaksi PENDING (belum final) - impor setelah muncul tanggalnya
- Saldo Awal,=,5,000,000.00 -> baris ringkasan (saldo/total), bukan transaksi
- Mutasi Kredit,=,10,262,345.67,3 -> baris ringkasan (saldo/total), bukan transaksi
- Mutasi Debet,=,8,019,969.13,10 -> baris ringkasan (saldo/total), bukan transaksi
- Saldo Akhir,=,7,242,376.54 -> baris ringkasan (saldo/total), bukan transaksi

File hasil: mutasi-bca-sep-actual.csv
Cara impor di Actual: buka akun bank -> Import -> pilih file hasil -> pastikan kolom Date/Payee/Notes/Category/Amount terpasang, format tanggal 'YYYY MM DD', pemisah koma, opsi 'Split amount' (memecah kolom jumlah jadi masuk/keluar) dan 'Flip amount' (membalik tanda plus/minus) dua-duanya MATI -> cek pratinjau -> Import.
```

## 3. File hasil `mutasi-bca-sep-actual.csv`
```
Date,Payee,Notes,Category,Amount
2026-09-01,PT MAJU KREATIF,TRSF E-BANKING CR 0109/FTSCY/WS95031 8250000.00 PT MAJU KREATIF,Pendapatan Proyek,8250000
2026-09-02,BIAYA ADM,BIAYA ADM,,-10000
2026-09-03,PLN PRABAYAR,TRSF E-BANKING DB 0309/FTFVA/WS95051 70001/PLN PRABAYAR,,-502500
2026-09-05,COWORKING HUB SENOPATI,TRSF E-BANKING DB 0509/FTSCY/WS95031 1500000.00 COWORKING HUB SENOPATI,Sewa Coworking,-1500000
2026-09-08,TELKOMSEL,KARTU DEBIT TELKOMSEL 8801,Internet & Pulsa,-380000
2026-09-10,TARIKAN ATM 10/09 ATM BCA,TARIKAN ATM 10/09 ATM BCA,,-1000000
2026-09-12,PERTAMINA,KARTU DEBIT PERTAMINA 34.123,Transportasi,-450000
2026-09-13,FACEBK ADS META,TRSF E-BANKING DB 1309/FTSCY/WS95031 3200000.00 FACEBK ADS META,Iklan,-3200000
2026-09-18,TOKOPEDIA,KARTU DEBIT TOKOPEDIA,,-700000
2026-09-20,BUDI SANTOSO,TRSF E-BANKING CR 2009/FTSCY/WS95031 2000000.00 BUDI SANTOSO,Pendapatan Proyek,2000000
2026-09-24,TOKO XYZ,QRIS TOKO XYZ 99231,,-275000
2026-09-30,BUNGA,BUNGA,Pendapatan Lain,12345.67
2026-09-30,PAJAK BUNGA,PAJAK BUNGA,Pajak,-2469.13
```

## 4. Balasan agent (usulan + satu konfirmasi, satu pesan)
> Sudah saya konversi: 13 transaksi terbaca, saldo cocok (Rp 7.242.376,54). 5 transaksi belum pasti, ini usulan saya:
> 1. 2 Sep, BIAYA ADM Rp 10.000 → "Biaya Bank" (kategori ini belum ada di Actual, buat dulu).
> 2. 3 Sep, PLN PRABAYAR Rp 502.500 → "Listrik & Air" (belum ada, buat dulu).
> 3. 10 Sep, TARIKAN ATM Rp 1.000.000 → pindah uang ke dompet sendiri, dicatat sebagai transfer tanpa kategori.
> 4. 18 Sep, TOKOPEDIA Rp 700.000 → "Perlengkapan Usaha" (belum ada, buat dulu).
> 5. 24 Sep, QRIS TOKO XYZ Rp 275.000 → "Biaya Lain-lain" (belum ada, buat dulu).
>
> Balas "ya" kalau usulan ini cocok, atau sebut yang mau diganti. Lima baris dilewati (satu transaksi PENDING dan empat baris saldo/total), tidak ikut diimpor.
>
> Impor: buka akun **BCA Usaha** → Import → pilih file hasil → tanggal "YYYY MM DD" → Import. Saldo akhir di Actual harus **Rp 7.242.376,54**.

## Catatan verifikasi
File hasil ini sudah diurai dengan parser CSV server Actual 26.9.0 dan diimpor ke salinan budget lewat API resmi:
13 baris terbaca, 0 galat, jumlah tepat hingga sen; 8 baris yang mirip transaksi lama digabung otomatis oleh fitur
anti-dobel Actual (lihat `references/sumber-resmi.md` §4). Layar Import aplikasi desktop belum diklik manual.
