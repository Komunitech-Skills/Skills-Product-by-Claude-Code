---
name: rekap-penjualan-csv
description: Menganalisis file penjualan CSV (ekspor kasir, Shopee, Tokopedia, atau spreadsheet) lalu membuat rekap omzet, produk terlaris, dan tren harian dalam bahasa Indonesia. Gunakan saat pengguna mengirim data penjualan atau minta laporan/rekap penjualan (sales report, sales summary, analisis omzet).
---

# Rekap Penjualan dari CSV

Mengubah data penjualan mentah menjadi ringkasan yang mudah dipahami pemilik usaha.

## Alur kerja

1. **Cek kolom file.** Lihat beberapa baris pertama CSV. Tentukan kolom untuk:
   - tanggal (wajib)
   - nama produk (wajib)
   - jumlah/qty (opsional, default 1)
   - total harga baris (wajib; jika tidak ada, gunakan harga satuan × qty)
2. **Jalankan script analisis** `scripts/rekap.py` yang ada di folder skill ini
   (pakai path lengkap ke folder skill; di Windows ganti `python3` dengan `python` atau `py`):
   ```bash
   python3 <folder-skill>/scripts/rekap.py <file.csv> \
     --kolom-tanggal "Tanggal" --kolom-produk "Produk" \
     --kolom-qty "Qty" --kolom-total "Total"
   ```
   - Jika tidak ada kolom total tapi ada harga satuan, pakai `--kolom-harga "Harga"` sebagai ganti `--kolom-total`.
   - Delimiter (`,` atau `;`) dan format angka Indonesia (`Rp 15.000`, `15.000,50`) dideteksi otomatis.
   - Jika Python tidak tersedia, hitung manual langkah demi langkah dan beri tahu pengguna bahwa hasil belum diverifikasi script.
3. **Tulis rekap** berdasarkan output JSON script, dengan format di bawah.
4. **Beri 2–3 insight** yang bisa langsung ditindaklanjuti, berdasarkan angka.

## Format output

```
## Rekap Penjualan <tanggal awal> – <tanggal akhir>

**Total omzet:** Rp X
**Jumlah transaksi (baris):** N
**Rata-rata omzet per hari:** Rp Y

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|

### Tren harian
Hari terbaik: <tanggal> (Rp ...). Hari terendah: <tanggal> (Rp ...).

### Insight
1. ...
2. ...
```

## Aturan & batasan

- Semua angka rupiah ditulis dengan pemisah ribuan titik: `Rp 1.250.000`.
- Jangan mengarang angka: semua angka harus berasal dari output script.
- Jika script melaporkan baris yang dilewati (`baris_dilewati` > 0), sebutkan jumlahnya dan alasannya.
- Insight harus berdasarkan data; hindari saran generik seperti "tingkatkan pemasaran".
- Jangan mengirim isi file pengguna ke layanan eksternal.
