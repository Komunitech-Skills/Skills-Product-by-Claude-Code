# Uji A/B — skenario normal pertama, tanpa skill vs dengan skill (penguji independen Akun B)

Tanggal uji: 26 September 2026. Penguji hanya membaca folder skill; data dan budget Actual dibuat sendiri
(bukan fixture pembuat): budget **"Desainer Dimas (uji B)"** dibuat dengan `@actual-app/api` 26.9.0 (npm, folder
sementara), mutasi **BCA Agustus 2026 fiktif** berpenyandian cp1252 (ada `CAFÉ`), tanggal `'01/08` tanpa tahun,
kolom CR/DB tanpa judul, 1 baris `PEND`, 4 baris ringkasan, 2 baris kembar, angka gaya Inggris dengan sen.

## Permintaan
> "Ini mutasi BCA Agustus, masukin ke Actual ya."

## A. Tanpa skill (baseline wajar yang ditulis agent umum)
Agent umum menulis script `csv` sederhana:
1. Percobaan pertama **gagal**: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc9` (file cp1252). Setelah
   dibuka latin-1, 11 baris terbaca, total bersih Rp 1.915.987,16 (benar).
2. Hasil CSV: **tanpa kolom Category** sama sekali; Payee = potongan 30 karakter (`TRSF E-BANKING CR 0108/FTSCY/W`);
   angka float (`9800000.0`); tahun 2026 **diasumsikan diam-diam**; tarik ATM Rp 1 jt dan top up GoPay Rp 500 rb
   tidak ditandai sebagai pindah dana (akan terhitung pengeluaran bila pengguna memberi kategori); baris kembar
   `CAFÉ BENGAWAN` tidak diperingatkan; tidak ada cek saldo; tidak ada panduan layar Import.
3. Ringkasan anggaran tanpa skill (agent menebak skema `db.sqlite`: `SUM(amount)` per kategori − `zero_budgets`):

| Kategori (Agu 2026) | Tebakan tanpa skill | Actual `getBudgetMonth` |
|---|---|---|
| Makan | sisa **-Rp 8.619.999** (transaksi terhapus Rp 9.999.999 ikut dihitung) | Rp 1.380.000 |
| Alat Kerja | sisa -Rp 1.280.000 (rollover minus Juli diabaikan) | -Rp 1.780.000 |
| Tabungan Pajak | sisa -Rp 500.000 (sisa bulan lalu diabaikan) | Rp 1.500.000 |
| To Budget | tidak dihitung | Rp 2.281.997,77 |
3 dari 6 kategori salah, satu salah besar dan menyesatkan ("Makan jebol 8,6 juta").

## B. Dengan skill (`scripts/actual_budget.py` v1.0.0, dijalankan penguji)
```
$ python3 scripts/actual_budget.py konversi bca-agu.csv --db <Desainer> --tahun 2026 --peta aturan.csv
Terbaca: 11 transaksi | Dilewati: 5 | Perlu dicek: 8
Total masuk: Rp 9.801.234,56 | Total keluar: Rp 7.885.247,40
Cek saldo bank: COCOK (saldo awal Rp 3.000.000 -> saldo akhir Rp 4.915.987,16)
- Kos: 1 baris, -Rp 2.250.000 | Software: -Rp 850.000,49 | Makan: 2 baris, -Rp 175.000 | Honor Klien: Rp 9.800.000
PERLU DICEK: BIAYA ADM (kategori 'Biaya Bank' belum ada), TOP UP GOPAY & TARIKAN ATM (PINDAH DANA -> transfer),
  2x CAFÉ BENGAWAN (baris sama persis 2x, pastikan bukan dobel), TOKOPEDIA (marketplace), BUNGA/PAJAK BUNGA
DILEWATI: 1 PENDING + 4 baris ringkasan (dengan alasan)
```
- Tanpa `--tahun` script berhenti dan meminta tahun (tidak menebak).
- File hasil diurai parser CSV **server Actual 26.9.0** dan `looselyParseAmount` **asli dari paket** (bukan port),
  lalu diimpor lewat `importTransactions`: 11 baris, 0 galat, 11 jumlah persis sampai sen, 5/5 kategori terpasang,
  saldo akun bertambah persis Rp 1.915.987,16.
- Ringkasan `ringkasan --bulan "Agustus 2026"` = `getBudgetMonth` untuk semua kategori & To Budget (lihat HASIL-UJI).

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Membaca file cp1252 | gagal di percobaan pertama | otomatis |
| Tahun tanpa tahun | ditebak diam-diam | ditanyakan |
| Kategori sesuai nama di budget | tidak ada | ada, dicocokkan ke budget, sisanya ditanyakan |
| Pindah dana / dobel / pending / ringkasan | tidak dikenali | ditandai atau dilewati dengan alasan |
| Cek saldo | tidak ada | COCOK/TIDAK COCOK |
| Ringkasan anggaran | 3/6 kategori salah | 100% sama dengan Actual |

**Kesimpulan:** dengan skill **jelas lebih baik** — lebih aman (tidak salah kategori pindah dana) dan angkanya benar.
