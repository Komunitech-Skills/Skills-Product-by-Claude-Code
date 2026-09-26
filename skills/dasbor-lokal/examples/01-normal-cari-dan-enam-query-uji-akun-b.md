# 01 — Normal: temukan database & jalankan 6 canned query (uji independen Akun B)

## Data uji
Enam database dibuat dengan menjalankan **script asli tiap alat** (bukan disuntik manual),
data fiktif, di scratchpad Akun B (bukan `~/KomunitechData` sungguhan):
- `buku-stok`: 4 produk (Beras, Minyak Goreng, Gula Pasir, Kopi Sachet); 2 di bawah stok
  minimum.
- `kasir-lokal`: toko "Warung Sari", 3 produk, 6 nota tanggal 21–25 Sep 2026.
- `crm-wa`: 6 kontak di 5 tahap pipeline (baru/dihubungi/ditawar/deal x2/batal).
- `absensi-lokal`: 3 karyawan, tap masuk/pulang untuk 2 karyawan tgl 25 Sep, 1 karyawan
  tgl 24 Sep.
- `buku-piutang`: 2 pelanggan, 3 nota, 1 pembayaran sebagian.
- `kas-umkm`: 3 akun (Laci, Bank BCA, QRIS), 3 transaksi kas.

## Perintah & hasil
```
python3 scripts/dasbor.py cari
```
→ Semua 6 alat "ADA" dengan path & ukuran yang benar.

```
python3 scripts/dasbor.py query buku-stok stok-menipis
python3 scripts/dasbor.py query kasir-lokal penjualan-per-hari
python3 scripts/dasbor.py query buku-piutang piutang-jatuh-tempo
python3 scripts/dasbor.py query absensi-lokal kehadiran-harian --tanggal 2026-09-25
python3 scripts/dasbor.py query crm-wa prospek-per-tahap
python3 scripts/dasbor.py query kas-umkm saldo-per-akun
```

| Query | Hasil skill | Hitung manual independen | Cocok? |
|---|---|---|---|
| stok-menipis | BRG003 (3<20), BRG002 (5<15) | Sama, benar diurutkan paling parah dulu | ✅ |
| penjualan-per-hari | 21–23 Sep: 1 nota Rp66.000/hari; 24 Sep: Rp30.000; 25 Sep: 2 nota Rp36.000 | Jumlah item x harga per nota dihitung ulang manual: cocok persis | ✅ |
| piutang-jatuh-tempo | Hanya PB-0001 (Warung Makmur), sisa Rp1.000.000 | PB-0001: 1.500.000 - 500.000 bayar = 1.000.000, jatuh tempo 31 Agu (lewat); PB-0002/PB-0003 belum jatuh tempo → benar dikeluarkan | ✅ |
| kehadiran-harian (25 Sep) | A01 & A02 tampil, A03 tidak (tidak tap) | Sama | ✅ |
| prospek-per-tahap | deal 2/Rp1.500.000, ditawar 1/1.200.000, dihubungi 1/750.000, batal 1/300.000, baru 1/500.000 | Dijumlah manual per tahap dari 6 kontak: cocok | ✅ |
| saldo-per-akun | Laci Rp1.700.000, Bank BCA Rp1.700.000, QRIS Rp800.000 | 500rb+1,2jt=1,7jt; 2jt-300rb=1,7jt; 0+800rb=800rb | ✅ |

Format uang konsisten "Rp x.xxx.xxx" di semua baris; sumber (path db) dan jumlah baris
tercetak di tiap hasil. Skema output teks sesuai `SKILL.md` (Format Output).

## Kesimpulan
6/6 database ditemukan otomatis, 6/6 canned query benar dan diverifikasi manual independen
(lihat juga penghitungan lengkap di `HASIL-UJI.md`). Tidak ada penyimpangan.
