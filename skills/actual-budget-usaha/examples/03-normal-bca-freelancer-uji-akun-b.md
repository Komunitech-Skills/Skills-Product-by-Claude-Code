# Skenario 3 (normal) — Freelancer desainer: mutasi BCA Agustus → CSV impor Actual (uji Akun B)

Data fiktif buatan penguji: budget Actual 26.9.0 "Desainer Dimas (uji B)" (kategori: Honor Klien, Software, Alat
Kerja, Internet, Makan, Kos, Tabungan Pajak) dan `bca-agu.csv` (cp1252, 11 transaksi + PEND + 4 baris ringkasan).

**Pengguna:** "Ini mutasi BCA Agustus, masukin ke Actual ya."

## Jalannya (mengikuti SKILL.md langkah A)
1. `konversi bca-agu.csv --db <budget>` → `GAGAL: Tanggal di mutasi tanpa tahun ... --tahun 2026` (kode 2). Agent
   bertanya sekali soal tahun. ✔
2. Tanpa `--peta`: 11 baris terbaca, **semua 11 masuk "perlu dicek"** karena nama usulan bawaan (Pendapatan Usaha,
   Sewa, Software & Langganan, Biaya Bank, dst.) tidak ada di budget ini; script memberi tahu dengan jelas dan
   mengosongkan kategori (tidak memaksa nama yang tidak ada). ✔
3. Dengan aturan pengguna (`KLIEN→Honor Klien`, `ADOBE→Software`, `IBU KOS→Kos`, `CAFÉ→Makan`):
```
Terbaca: 11 transaksi | Dilewati: 5 | Perlu dicek: 8
Total masuk: Rp 9.801.234,56 | Total keluar: Rp 7.885.247,40
Cek saldo bank: COCOK (saldo awal Rp 3.000.000 -> saldo akhir Rp 4.915.987,16)
- (menunggu konfirmasi usulan): 6 baris, -Rp 4.609.012,35
- Kos: 1 baris, -Rp 2.250.000 | Software: 1 baris, -Rp 850.000,49 | Makan: 2 baris, -Rp 175.000 | Honor Klien: Rp 9.800.000
PERLU DICEK: TOP UP GOPAY & TARIKAN ATM (PINDAH DANA → transfer), 2x CAFÉ BENGAWAN (baris sama persis 2x),
  TOKOPEDIA TABLET (marketplace), BIAYA ADM / BUNGA / PAJAK BUNGA (kategori usulan belum ada)
DILEWATI: PENDING SHOPEE, Saldo Awal, Mutasi Kredit, Mutasi Debet, Saldo Akhir
```
4. Verifikasi independen: total masuk/keluar dan saldo akhir dihitung ulang penguji dengan Decimal → sama.
   CSV hasil (UTF-8, `Date,Payee,Notes,Category,Amount`, `-850000.49`, `1234.56`) diimpor ke akun kosong lewat
   parser server Actual + `looselyParseAmount` asli paket 26.9.0: 11/11 baris, 0 galat, jumlah persis, saldo akun
   +Rp 1.915.987,16 = hitungan penguji. File mutasi asli tidak berubah (hash sama).

## Draf balasan agent (satu pesan)
> Mutasi BCA Agustus sudah jadi file impor `bca-agu-actual.csv` (11 transaksi, saldo cocok: akhir Rp 4.915.987,16).
> Tolong pilihkan 8 baris ini sekaligus:
> 1. 9 Agu TOP UP GOPAY Rp 500.000 dan 10 Agu TARIKAN ATM Rp 1.000.000 → pindah uang sendiri; di Actual pilih Payee =
>    akun "GoPay"/"Kas" (transfer), tanpa kategori. Setuju?
> 2. 12 Agu CAFÉ BENGAWAN Rp 87.500 muncul 2x — memang dua kali beli, atau dobel?
> 3. 14 Agu TOKOPEDIA TABLET Rp 3.100.000 → Alat Kerja?
> 4. BIAYA ADM Rp 10.000, BUNGA Rp 1.234,56, PAJAK BUNGA Rp 246,91 → kategori belum ada; buat "Biaya Bank" dll. atau
>    pakai kategori yang ada?
> Setelah itu: akun Mandiri/BCA di Actual → Import → pilih file → tanggal "YYYY MM DD", Split/Flip amount mati → Import.

**Hasil: LULUS.** Catatan kecil: bila budget hanya punya satu kategori pemasukan (Honor Klien), usulan bawaan
"Pendapatan Usaha" sebenarnya bisa dipetakan otomatis ke kategori itu.
