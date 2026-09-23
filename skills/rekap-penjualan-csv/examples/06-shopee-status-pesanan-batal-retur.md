# Contoh 06 – Ekspor gaya Shopee dengan kolom status pesanan (uji ulang v1.2.0)

## Skenario
Ekspor pesanan toko fashion pria gaya Shopee, Agustus 2026: 89 baris, pemisah koma, harga `Rp129.000`. Kolom **Status Pesanan** berisi `Selesai` (60), `Batal` (15), `Sedang Dikirim` (13), dan `Pengembalian Barang/Dana` (1). Satu pesanan bisa terdiri dari beberapa baris produk. Data fiktif (dibuat penguji dengan seed tetap).

Pada v1.1.0, contoh ini memperlihatkan cacat berat: baris "Pengembalian Barang/Dana" ikut dihitung sebagai omzet (Rp 9.051.000). Di v1.2.0 contoh ini dijalankan ulang dan angkanya kini benar.

## Input pengguna
```
tolong rekap penjualan shopee aku bulan agustus ya, file export-pesanan-agustus.csv. pesanan yg batal jangan diitung
```
Cuplikan file:
```
No. Pesanan,Status Pesanan,Waktu Pesanan Dibuat,Nama Produk,Jumlah,Harga Awal,Total Harga Produk
260801SPX0001,Selesai,2026-08-01 21:30,Kaos Kaki (3 pasang),1,Rp25.000,Rp25.000
260801SPX0001,Selesai,2026-08-01 12:42,Kemeja Flanel Kotak,2,Rp129.000,Rp258.000
260802SPX0002,Selesai,2026-08-02 17:06,Kemeja Flanel Kotak,2,Rp129.000,Rp258.000
```

## Proses (dijalankan agent, sesuai SKILL.md langkah 2)
```
$ python3 scripts/rekap.py export-pesanan-agustus.csv --kolom-tanggal "Waktu Pesanan Dibuat" \
    --kolom-produk "Nama Produk" --kolom-qty "Jumlah" --kolom-total "Total Harga Produk" \
    --kolom-status "Status Pesanan"
→ total_omzet 9006000, jumlah_baris_valid 73, baris_dilewati 0,
  dibuang_karena_status {"Batal": 15, "Pengembalian Barang/Dana": 1},
  status_dihitung {"Selesai": 60, "Sedang Dikirim": 13},
  nama_produk_digabung {}, peringatan []
```

## Output

## Rekap Penjualan 1 – 31 Agustus 2026

**Total omzet:** Rp 9.006.000
**Jumlah transaksi (baris):** 73
**Rata-rata omzet per hari (kalender):** Rp 290.516  _(hari berjualan: Rp 333.556; 27 dari 31 hari ada penjualan)_

**Status pesanan yang dipakai:**
- ✅ Dihitung: **Selesai** (60 baris) dan **Sedang Dikirim** (13 baris)
- ❌ Tidak dihitung: **Batal** (15 baris, Rp 1.742.000) dan **Pengembalian Barang/Dana** (1 baris, Rp 45.000)

"Sedang Dikirim" ikut dihitung karena pesanannya sudah dibayar. Kalau kamu mau hanya menghitung yang sudah *Selesai*, bilang saja, nanti aku hitung ulang.
Omzet di atas memakai kolom *Total Harga Produk* (sebelum ongkir, voucher, dan potongan biaya Shopee), jadi bukan uang bersih yang kamu terima.

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Kemeja Flanel Kotak | 26 | Rp 3.354.000 | 37,2% |
| 2 | Celana Chino Slim | 18 | Rp 2.682.000 | 29,8% |
| 3 | Topi Baseball | 25 | Rp 1.125.000 | 12,5% |
| 4 | Kaos Polos Hitam | 12 | Rp 660.000 | 7,3% |
| 5 | Kaos Polos Putih | 12 | Rp 660.000 | 7,3% |

### Tren harian
Hari terbaik: Kamis, 6 Agustus 2026 (Rp 1.054.000). Hari terendah: Senin, 24 Agustus 2026 (Rp 55.000).
Ada 4 hari tanpa penjualan: 9, 13, 15, dan 21 Agustus.

### Insight
1. **Dua produk menyumbang dua pertiga omzet.** Kemeja Flanel (37,2%) dan Celana Chino (29,8%) bersama-sama menghasilkan Rp 6.036.000 (67,0%). Pastikan stok ukuran terlaris keduanya aman, dan coba paket "Flanel + Chino".
2. **Pembatalan cukup tinggi: 15 dari 89 baris, senilai Rp 1.742.000 (setara 19,3% dari omzet).** Cek alasan batal di Seller Center (stok kosong, pembeli berubah pikiran, atau telat kirim). Jika karena stok, sinkronkan stok lebih sering.
3. **Topi Baseball laku banyak (25 pcs) tapi harganya rendah.** Jadikan add-on di halaman Kemeja/Chino untuk menaikkan nilai per pesanan. Ada 1 pengembalian Topi Baseball (24 Agustus). Cek alasannya, misalnya ukuran atau warna tidak sesuai foto.

## Catatan penguji
- **Cacat berat B1 (v1.1.0) sudah beres:** "Pengembalian Barang/Dana" kini dibuang dan dilaporkan di `dibuang_karena_status`. Script juga mengeluarkan `status_dihitung`, sehingga agent bisa menampilkan status yang ikut dan tidak ikut dihitung, sesuai aturan baru di SKILL.md.
- **Verifikasi independen** (parser & filter milik penguji, `verif6.py`, hanya menghitung status Selesai + Sedang Dikirim): total **Rp 9.006.000**, 73 baris, top-5 (qty, omzet, %) sama, hari terbaik 6/8 (Rp 1.054.000), terendah 24/8 (Rp 55.000), rata-rata 9.006.000 / 31 = 290.516,13 dan / 27 = 333.555,56. Nilai per status: Batal Rp 1.742.000, Sedang Dikirim Rp 1.512.000, Pengembalian Rp 45.000. **Cocok 100%.**
- Angka turunan (Rp 6.036.000 = 67,0%, 19,3%) dihitung agent dari JSON. Diizinkan secara wajar, tapi aturan "semua angka dari script" di SKILL.md belum menyebut angka turunan (ringan R2).
- Bagus: agent menyebut bahwa omzet belum dikurangi ongkir/voucher/biaya marketplace. Ini masih inisiatif agent, belum diatur di SKILL.md (ringan R8).
