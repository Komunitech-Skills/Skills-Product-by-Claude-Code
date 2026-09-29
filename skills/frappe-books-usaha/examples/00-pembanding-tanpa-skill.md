# Uji A/B — skenario normal pertama (toko kopi), tanpa skill vs dengan skill

Penguji: Akun B (penguji independen, bukan pembuat), 26 Sep 2026.
Data: **file `.books.db` asli** buatan aplikasi Frappe Books v0.36.0 (AppImage Linux resmi, SHA-512 cocok dengan
`latest-linux.yml` rilis v0.36.0), perusahaan fiktif "Kopi Senja (fiktif)", negara Indonesia, IDR; aplikasi dijalankan
dengan zona waktu Asia/Jakarta. Transaksi dibuat lewat mesin aplikasi itu sendiri (bukan fixture pembuat skill). Semua nama fiktif.

Permintaan pengguna: *"Penjualan September berapa, dan berapa yang belum dibayar?"*

## Isi data (dicatat penguji saat membuat)
| Invoice | Waktu WIB | Status | Total |
|---|---|---|---|
| SINV-1004 | 31 Agu 23:50 | final | 85.000 |
| SINV-1001 | 1 Sep 00:30 | final, lunas | 76.000 |
| SINV-1008 | 2 Sep | retur dari SINV-1001 (1 croissant) | -22.000 |
| SINV-1007 | 10 Sep | di-Submit lalu **dibatalkan** | 40.000 |
| SINV-1005 | 15 Sep | final, dibayar 100.000 | 255.000 |
| SINV-1006 | 20 Sep | **draf** | 50.000 |
| SINV-1002 | 30 Sep 23:45 | final, belum dibayar | 255.000 |
| SINV-1003 | 1 Okt 00:10 | final | 30.000 |

Jawaban benar (dihitung penguji dengan Decimal dari data mentah, zona WIB): **4 invoice final, total Rp 564.000,
belum dibayar Rp 410.000** (sisa invoice retur tidak dihitung sebagai piutang).

## A. Tanpa skill (simulasi pendekatan agen umum)
Catatan kejujuran: penguji sudah membaca skill, jadi ini **bukan** agen buta; ini simulasi pola yang lazim dipakai agen umum
(SQL langsung ke file, filter tanggal teks). Query dijalankan sungguhan pada file yang sama:

| Pendekatan umum | Hasil | Selisih vs benar |
|---|---|---|
| `SUM(grandTotal) WHERE date LIKE '2026-09%'` | Rp 608.000 (6 invoice) | +44.000: ikut draf & batal |
| + `submitted=1` | Rp 558.000 | ikut invoice batal |
| + `submitted=1 AND cancelled=0` | Rp 518.000, sisa Rp 418.000 | -46.000: tanggal disimpan UTC → SINV-1001 (1 Sep WIB) hilang, SINV-1003 (1 Okt WIB) ikut |

Risiko tambahan tanpa skill: file dibuka read-write (bisa bentrok saat Frappe Books terbuka), tidak ada penjelasan
draf/batal/retur, format rupiah tidak konsisten, tidak tahu Frappe Books tidak menyimpan tanggal jatuh tempo.

## B. Dengan skill (`penjualan --bulan 2026-09`, keluaran nyata)
```
PENJUALAN - Kopi Senja (fiktif)
Periode: Sep 2026 (1 Sep 2026 s.d. 30 Sep 2026), zona WIB
Invoice final: 4 (termasuk 1 retur) | draf belum final: 1 (tidak dihitung) | dibatalkan: 1 (tidak dihitung)
DPP / sebelum pajak : Rp 564.000
Pajak               : Rp 0
TOTAL               : Rp 564.000
Sudah dibayar       : Rp 154.000 | Belum dibayar: Rp 410.000
Per pelanggan (terbesar dulu):
  1. Kantor Maju (fiktif) - 1 invoice - Rp 255.000
  2. Bu Rina (fiktif) - 1 invoice - Rp 255.000
  3. Pelanggan Umum - 2 invoice - Rp 54.000
```
Cocok 100% dengan hitungan independen; file tidak berubah (SHA-256 sama sebelum/sesudah).
Catatan kecil: "Sudah dibayar Rp 154.000" = total bersih − sisa; uang yang benar-benar diterima Rp 176.000 dan ada
Rp 22.000 retur yang belum dikembalikan ke pelanggan. Tidak salah hitung, tapi bisa membingungkan (lihat HASIL-UJI).

## Kesimpulan A/B
Untuk laporan baca, skill **jelas lebih baik**: angka benar di batas hari WIB, draf/batal/retur ditangani, read-only terjamin.
(Temuan tinggi skill ada di jalur impor CSV, bukan di laporan ini — lihat `HASIL-UJI.md`.)
