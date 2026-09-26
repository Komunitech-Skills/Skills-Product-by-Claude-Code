# Contoh 02 — Ringkasan anggaran bulanan (read-only)

Hasil nyata `scripts/actual_budget.py` v1.0.0 (26 September 2026) pada budget Actual 26.9.0 **asli** berisi data
fiktif. Angka sisa per kategori dan "To Budget" dicocokkan dengan `getBudgetMonth` milik Actual sendiri: **sama persis**.

## Permintaan pengguna
> "Anggaran saya bulan September gimana? Ada yang jebol?"

## Mode amplop (envelope)
```
$ python3 scripts/actual_budget.py ringkasan --db Studio-Rina --bulan "September 2026"
RINGKASAN ANGGARAN SEPTEMBER 2026
Budget: Studio Rina (fiktif) (dibaca read-only)
Jenis anggaran: amplop (envelope)

- Pemasukan bulan ini: Rp 8.400.000
- Total dianggarkan: Rp 9.850.000
- Total terpakai: Rp 10.960.000,50
- Siap dianggarkan (To Budget): Rp 1.010.000
- Kelebihan belanja bulan lalu yang memotong bulan ini: Rp 40.000

KATEGORI JEBOL (2):
- Iklan: minus Rp 1.100.000 (anggaran Rp 1.000.000, terpakai Rp 3.200.000, bawaan bulan lalu Rp 1.100.000)
- Pajak: minus Rp 200.000 (anggaran Rp 1.000.000, terpakai Rp 600.000, bawaan bulan lalu minus Rp 600.000)
  Saran: tutup dari kategori yang masih bersisa, atau kurangi anggaran bulan depan.

SISA ANGGARAN PER KATEGORI:
[Biaya Usaha]
- Iklan: sisa minus Rp 1.100.000 (JEBOL) | anggaran Rp 1.000.000, terpakai Rp 3.200.000
- Transportasi: sisa Rp 560.000 | anggaran Rp 1.100.000, terpakai Rp 540.000
- Software & Langganan: sisa Rp 10.000 | anggaran Rp 600.000, terpakai Rp 1.290.000
- Internet & Pulsa: sisa Rp 270.000 | anggaran Rp 450.000, terpakai Rp 380.000
- Sewa Coworking: sisa Rp 0 | anggaran Rp 1.500.000, terpakai Rp 1.500.000
[Kebutuhan Pribadi]
- Belanja Rumah: sisa Rp 149.999,50 | anggaran Rp 1.200.000, terpakai Rp 1.650.000,50
- Makan: sisa Rp 1.300.000 | anggaran Rp 2.500.000, terpakai Rp 1.800.000
[Dana Cadangan]
- Dana Darurat: sisa Rp 1.500.000 | anggaran Rp 500.000, terpakai Rp 0
- Pajak: sisa minus Rp 200.000 (JEBOL) | anggaran Rp 1.000.000, terpakai Rp 600.000

PENGELUARAN TERBESAR:
1. 13 Sep - Meta Ads - Rp 3.200.000 (Iklan)
2. 16 Sep - Warung & Resto - Rp 1.800.000 (Makan)
3. 5 Sep - Coworking Hub - Rp 1.500.000 (Sewa Coworking)
4. 20 Sep - Superindo - Rp 1.350.000,50 (Belanja Rumah)
5. 10 Sep - Figma & Adobe - Rp 890.000 (Software & Langganan)

PERLU DICEK: 1 transaksi belum berkategori (bersih Rp 275.000 keluar). Beri kategori di Actual agar sisa anggaran akurat.

Sumber: db.sqlite | Dihitung ulang dari db.sqlite dengan rumus Actual 26.9.0; bila beda dengan layar Actual, yang benar adalah layar Actual.
```
Saran agent (tambahan, angka tidak diubah):
> 1. Iklan jebol Rp 1.100.000 — bisa ditutup dari **Makan** (sisa Rp 1.300.000) atau **Dana Darurat** (Rp 1.500.000).
> 2. Pajak minus Rp 200.000 terbawa karena "Rollover overspending" aktif; tambah anggaran Pajak Oktober minimal Rp 200.000.
> 3. Ada 1 transaksi Rp 275.000 belum berkategori (QRIS Toko XYZ) — beri kategori agar sisa akurat.

Yang diuji di contoh ini: transfer BCA → Kas tidak dihitung pengeluaran, transfer ke rekening "di luar anggaran"
yang berkategori Pajak dihitung, transaksi split dihitung per bagian, transaksi terhapus ("Salah Input" Rp 5 jt)
diabaikan, kategori "Ojek Online" yang dihapus dialihkan ke Transportasi, sen (Rp 1.350.000,50) tidak dibulatkan.

## Mode pelacakan (tracking)
```
$ python3 scripts/actual_budget.py ringkasan --db actual-26.9.0-toko-kue-tracking --bulan 2026-09
RINGKASAN ANGGARAN SEPTEMBER 2026
Budget: Toko Kue Sari (fiktif, tracking) (dibaca read-only)
Jenis anggaran: pelacakan (tracking)

- Pemasukan bulan ini: Rp 5.000.000
- Total dianggarkan: Rp 3.500.000
- Total terpakai: Rp 3.450.000

KATEGORI JEBOL: tidak ada.

SISA ANGGARAN PER KATEGORI:
[Operasional]
- Kemasan: sisa Rp 50.000 | anggaran Rp 500.000, terpakai Rp 650.000
- Bahan Kue: sisa Rp 200.000 | anggaran Rp 3.000.000, terpakai Rp 2.800.000

PENGELUARAN TERBESAR:
1. 5 Sep - Toko Bahan - Rp 2.800.000 (Bahan Kue)
2. 7 Sep - Plastik - Rp 650.000 (Kemasan)

Sumber: db.sqlite | Dihitung ulang dari db.sqlite dengan rumus Actual 26.9.0; bila beda dengan layar Actual, yang benar adalah layar Actual.
Catatan: mode pelacakan (tracking) - sisa tidak dibawa ke bulan berikutnya kecuali opsi 'rollover' kategori itu dinyalakan di Actual.
```
Kemasan: anggaran Rp 500.000 − terpakai Rp 650.000 + sisa Agustus Rp 200.000 (rollover aktif) = Rp 50.000. Bahan Kue
tanpa rollover: minus Agustus tidak dibawa. Sama dengan hitungan Actual.

## File sedang dikunci Actual
```
$ python3 scripts/actual_budget.py ringkasan --db Studio-Rina-kunci
exit 4
GAGAL: File budget sedang dipakai/ditulis Actual. Tunggu sebentar (atau tutup Actual) lalu coba lagi.

```
(Diuji dengan kunci tulis eksklusif di file. Script berhenti setelah 5 detik; file tidak diubah.)
