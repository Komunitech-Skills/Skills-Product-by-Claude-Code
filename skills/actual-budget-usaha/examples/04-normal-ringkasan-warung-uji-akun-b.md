# Skenario 4 (normal) — Warung kopi: "Anggaran warung bulan Agustus gimana? Yang jebol apa?" (uji Akun B)

Budget Actual 26.9.0 asli buatan penguji "Warung Kopi Pak Joko (uji B)", mode amplop, Juni–Agustus 2026: 2 akun
on-budget (BRI Usaha, Laci Kasir), 5 kategori biaya, 2 kategori pemasukan, kategori jebol berturut-turut, sen
(Rp 18.250.000,75; Rp 1.100.000,10), dan **dana ditahan untuk bulan depan Rp 1.000.000** (`holdBudgetForNextMonth`).

```
$ python3 scripts/actual_budget.py ringkasan --db <Warung> --bulan 08/2026 --top 3
- Pemasukan bulan ini: Rp 18.250.000,75
- Total dianggarkan: Rp 12.200.000
- Total terpakai: Rp 12.855.000
- Siap dianggarkan (To Budget): Rp 9.500.000,65
- Kelebihan belanja bulan lalu yang memotong bulan ini: Rp 550.000
KATEGORI JEBOL (2):
- Susu & Gula: minus Rp 750.000 (anggaran Rp 1.000.000, terpakai Rp 1.750.000)
- Gaji Barista: minus Rp 500.000 (anggaran Rp 4.000.000, terpakai Rp 4.500.000)
SISA: Sewa Kios Rp 0 | Listrik Rp 25.000 | Biji Kopi Rp 600.000
PENGELUARAN TERBESAR: Gaji Barista Rp 4.500.000; Pemilik Kios Rp 3.000.000; Roastery Gayo Rp 2.900.000
```

## Verifikasi tiga arah
| Pos (Agu 2026) | `getBudgetMonth` resmi | Hitung sendiri (Decimal) | Script |
|---|---|---|---|
| Susu & Gula | -750.000 | -750.000 | -750.000 |
| Gaji Barista | -500.000 | -500.000 | -500.000 |
| Listrik / Biji Kopi / Sewa | 25.000 / 600.000 / 0 | sama | sama |
| To Budget | 9.500.000,65 | 9.500.000,65 | 9.500.000,65 |
Juni, Juli, September juga sama (September: To Budget Rp 9.250.000,65, kelebihan belanja Agustus Rp 1.250.000
memotong bulan ini). Transaksi dari akun "Laci Kasir" (Rp 450.000) ikut terhitung di Susu & Gula dengan benar.

## Draf balasan agent
> (teks script di atas apa adanya) + saran berbasis angka:
> 1. Susu & Gula jebol Rp 750.000 → tutup dari Biji Kopi (sisa Rp 600.000) + To Budget.
> 2. Gaji Barista jebol Rp 500.000 → naikkan anggaran September ke Rp 4.500.000 bila memang tetap.

**Hasil: LULUS (angka).** Temuan: teks ringkasan **tidak menyebut dana ditahan Rp 1.000.000** (`ditahan` hanya ada
di `--json`). To Budget tetap benar, tetapi pemilik tidak tahu kenapa To Budget lebih kecil Rp 1 jt dari hitungan
kasarnya. Disarankan baris "Ditahan untuk bulan depan: Rp 1.000.000".
