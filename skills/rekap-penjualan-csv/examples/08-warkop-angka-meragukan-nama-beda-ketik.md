# Contoh 08 – Catatan warkop: angka meragukan dan nama menu beda ketik (uji ulang v1.2.0)

## Skenario
Skenario tambahan uji ulang v1.2.0 untuk dua perbaikan: (1) angka berformat meragukan harus **dilewati, bukan ditebak**, dan (2) nama produk yang sama tapi beda huruf besar/spasi harus **digabung dan dilaporkan**. Pemilik warung kopi mencatat penjualan 3 hari secara manual di spreadsheet, 16 baris. Ada salah ketik `15.000.00`, sel yang berubah jadi notasi ilmiah `1.5E+06`, dan `16000.500`. Nama menu ditulis tidak seragam: `Kopi Hitam` / `kopi hitam `, `Kopi Susu` / `KOPI SUSU`, `Indomie Telur` / `indomie telur`, `Es Teh` / `Es  Teh`. Data fiktif.

## Input pengguna
```
rekapin catetan warkop aku 3 hari ini dong, filenya catatan-warkop.csv. menu apa yg paling laku?
```
Cuplikan file:
```
Tanggal,Menu,Qty,Total
21/09/2026,Kopi Hitam,3,15.000
21/09/2026,kopi hitam ,2,10.000
22/09/2026,Indomie Telur,3,15.000.00
23/09/2026,Indomie Telur,2,1.5E+06
23/09/2026,Kopi Susu,2,16000.500
```

## Proses (dijalankan agent)
```
$ python3 scripts/rekap.py catatan-warkop.csv --kolom-tanggal "Tanggal" --kolom-produk "Menu" \
    --kolom-qty "Qty" --kolom-total "Total"
→ total_omzet 202000, jumlah_baris_valid 13, baris_dilewati 3,
  alasan_dilewati {"harga/total tidak valid atau meragukan": 3},
  nama_produk_digabung {"Kopi Hitam": ["Kopi Hitam", "kopi hitam"],
                        "Indomie Telur": ["Indomie Telur", "indomie telur"],
                        "Kopi Susu": ["KOPI SUSU", "Kopi Susu"]},
  peringatan []
```

## Output

## Rekap Penjualan 21 – 23 September 2026

**Total omzet:** Rp 202.000
**Jumlah transaksi (baris):** 13 (dari 16 baris di file)
**Rata-rata omzet per hari (kalender):** Rp 67.333  _(hari berjualan: Rp 67.333; 3 dari 3 hari ada penjualan)_

⚠️ **3 baris tidak dihitung karena angka Total-nya meragukan.** Aku tidak menebak angkanya supaya omzet tidak salah:
- 22/09 Indomie Telur, Total `15.000.00`. Mungkin maksudnya Rp 15.000 (salah ketik titik).
- 23/09 Indomie Telur, Total `1.5E+06`. Excel mengubah angkanya ke format ilmiah, jadi nilai aslinya tidak bisa dipastikan.
- 23/09 Kopi Susu, Total `16000.500`. Tidak jelas apakah Rp 16.000 atau Rp 16.000.500.

Cara memperbaiki: di Excel, blok kolom Total → klik kanan → *Format Cells* → *Number* (0 desimal), ketik ulang ketiga angka itu, lalu simpan lagi sebagai CSV. Kirim ulang filenya, nanti aku rekap lagi.

ℹ️ **Nama menu yang beda ketik sudah aku gabung:** "Kopi Hitam" = "kopi hitam", "Kopi Susu" = "KOPI SUSU", "Indomie Telur" = "indomie telur".

### 5 Menu Terlaris (omzet)
| # | Menu | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Kopi Hitam | 14 | Rp 70.000 | 34,7% |
| 2 | Kopi Susu | 5 | Rp 40.000 | 19,8% |
| 3 | Es Teh | 12 | Rp 36.000 | 17,8% |
| 4 | Indomie Telur | 3 | Rp 36.000 | 17,8% |
| 5 | Pisang Goreng | 10 | Rp 20.000 | 9,9% |

### Tren harian
Hari terbaik: Senin, 21 September 2026 (Rp 77.000). Hari terendah: Rabu, 23 September 2026 (Rp 55.000).
Catatan: 2 dari 3 baris yang dilewati ada di tanggal 23. Omzet Rabu kemungkinan sebenarnya lebih tinggi.

### Insight
1. **Kopi Hitam paling laku: 14 gelas, sepertiga omzet (34,7%).** Pastikan stok kopi bubuk dan gula tidak pernah habis, terutama di jam ramai.
2. **Es Teh laku banyak (12 gelas) tapi omzetnya kecil (Rp 3.000/gelas).** Coba paket "Pisang Goreng + Es Teh" untuk menaikkan nilai per pembeli.
3. **Angka Indomie Telur belum lengkap:** 2 dari 5 baris Indomie dilewati. Setelah angkanya diperbaiki, peringkat Indomie kemungkinan naik. Perbaiki dulu sebelum memutuskan stok mi dan telur.

## Catatan penguji
- **Cacat sedang S1 (v1.1.0) beres:** `15.000.00`, `1.5E+06`, dan `16000.500` kini **dilewati** dengan alasan "harga/total tidak valid atau meragukan". Pada v1.1.0 angka ini terbaca 1.500.000, 1.506, dan 16.000.500, sehingga omzet membengkak diam-diam.
- **Cacat sedang S2 (v1.1.0) beres:** nama beda huruf/spasi digabung dan dilaporkan di `nama_produk_digabung`. Varian yang hanya beda spasi (`Es  Teh`) digabung tanpa dilaporkan. Ini tidak masalah, karena tampilannya sama.
- **Verifikasi independen** (python terpisah, nilai rupiah dipetakan manual, nama dinormalisasi sendiri): total Rp 202.000, 13 baris, 3 dilewati, top-5 (qty/omzet/%) sama, harian 77.000 / 70.000 / 55.000, rata-rata 67.333,33. **Cocok 100%.**
- Kurang (ringan R3, masih terbuka): script tidak mengeluarkan nomor/isi baris yang dilewati. Daftar 3 baris di atas ditemukan agent dengan membuka file sendiri. `contoh_baris_dilewati` akan membuat langkah ini andal.
- Es Teh dan Indomie Telur seri (Rp 36.000). Urutan di tabel mengikuti script. Tidak salah, tapi seri tidak ditandai.
