# 00 — Uji A/B skenario 01 (toko kue): TANPA skill vs DENGAN skill

> Penguji independen (Akun B), 2026-09-26. Permintaan pengguna sama persis dengan `01-uji-independen-toko-kue.md`. Jawaban "tanpa skill" ditulis penguji sebagai agent umum yang tahu hledger tetapi tanpa skill ini (pola yang lazim di dokumentasi/tutorial hledger), lalu dijalankan dengan hledger 1.52.4 asli. Ini simulasi satu agent, bukan rata-rata banyak model; agent umum yang sangat teliti bisa menghindari sebagian kesalahan di bawah.

## TANPA skill — jurnal yang ditulis agent umum
```
; ditulis agent TANPA skill (gaya umum dokumentasi hledger)
2026-08-31 Opening balances
    assets:cash              IDR 1500000
    assets:bank:mandiri      IDR 8250000
    assets:inventory         IDR 2400000
    assets:equipment         IDR 6000000
    liabilities:payable      IDR -1200000
    equity:opening

2026-09-01 Penjualan kue harian
    assets:cash      IDR 2350000
    income:sales
... (15 transaksi, lihat pola di atas; 'Ambil pribadi' → expenses:personal)
```
Hasil `hledger is -p 2026-09` & `hledger bs` (dipotong):
```
----------------------++-----------------
                      || IDR 11600750.50 
======================++=================
 Net:                 ||   IDR 414749.50 
                     ||  IDR 1625750.50 
=====================++=================
 Net:                || IDR 17364749.50 
```
Jawaban agent tanpa skill ke pengguna: tabel hledger berbahasa Inggris, "laba September IDR 414749.50".

## DENGAN skill (ringkas; lengkap di 01)
```
- Pendapatan: Rp 12.015.500
- Laba bersih: Rp 914.749,50
- Kas & bank akhir: Rp 10.590.500 (+Rp 840.500 dari awal bulan)
- Piutang: Rp 0 | Utang: Rp 1.625.750,50 | Neraca: seimbang
LABA KOTOR: Rp 6.989.749,50 (58,2% dari pendapatan)
Cek: Aset = Utang + Modal (Rp 18.740.500). SEIMBANG.
Arus kas: operasi +1.590.500, pendanaan (prive) −750.000 → +840.500. COCOK.
Uji silang pembaca bawaan: COCOK
```

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Laba bersih | **Rp 414.749,50 (salah)**: prive dianggap beban (−750.000), stok akhir tidak disesuaikan (+250.000) | **Rp 914.749,50 (benar**, diverifikasi Decimal & hledger) |
| Persediaan di neraca | 2.400.000 (stok awal, tidak diperbarui) | 2.150.000 (hitung fisik) |
| Piutang/utang per pihak | Satu akun `assets:receivable`/`liabilities:payable` gabungan | Per pelanggan/pemasok otomatis (`PT Arunika`, `CV Gula Manis`) |
| Persetujuan sebelum menulis | Tidak ada; file langsung ditulis | Pratinjau + "Artinya:" + "ya" + cadangan `.sebelum-ubah` + pemeriksaan ulang |
| Deteksi dobel | Tidak ada | Batch diulang ditolak (kode 7) |
| Bahasa & format | Tabel hledger Inggris, `IDR 414749.50` | Bahasa Indonesia, `Rp 914.749,50`, siap tempel WA/Telegram |
| Neraca dengan modal & laba | `hledger bs` hanya "Net" (tanpa baris modal/laba) | Modal awal, prive, laba berjalan, cek seimbang |
| Arus kas per sumber | `hledger cf` hanya per akun kas | Operasi/investasi/pendanaan per sumber |
| Tanpa hledger terpasang | Tidak bisa membuat laporan | Pembaca bawaan, angka identik |
| Jembatan ke SAK EMKM/KUR | Tidak ada | `ekspor-emkm` → laporan_emkm.py, angka konsisten |

**Kesimpulan A/B:** dengan skill **jelas lebih baik** — dua kesalahan akuntansi material (prive sebagai beban, stok tidak disesuaikan) yang membuat laba meleset 55% hilang, ditambah pengaman tulis dan format lokal. Bahan "sebelum/sesudah" README valid.
