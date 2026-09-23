---
name: rekap-penjualan-csv
description: Menganalisis file penjualan CSV (ekspor kasir, Shopee, Tokopedia, atau spreadsheet) lalu membuat rekap omzet, produk terlaris, dan tren harian dalam bahasa Indonesia. Gunakan saat pengguna mengirim data penjualan atau minta laporan/rekap penjualan (sales report, sales summary, analisis omzet).
---

# Rekap Penjualan dari CSV

Mengubah data penjualan mentah menjadi ringkasan yang mudah dipahami pemilik usaha.

## Kapan TIDAK digunakan
- Laporan laba rugi / neraca dari buku kas → pakai skill `laporan-keuangan-emkm`.
- Menghitung pajak (PPh Final 0,5%) → pakai skill `pph-final-umkm`.
- Prediksi/forecast penjualan masa depan → jelaskan bahwa skill ini hanya merekap data yang sudah terjadi.
- File Excel `.xlsx` → minta pengguna menyimpannya sebagai CSV dulu (Excel: *File → Save As → CSV*).

## Alur kerja

1. **Cek kolom file.** Lihat beberapa baris pertama CSV. Tentukan kolom untuk:
   - tanggal (wajib)
   - nama produk (wajib)
   - jumlah/qty (opsional, default 1)
   - total harga baris (wajib; jika tidak ada, gunakan harga satuan × qty)
2. **Jalankan script analisis** `scripts/rekap.py`. Path ini relatif terhadap folder yang berisi
   SKILL.md ini; gunakan path lengkapnya. Di Windows, ganti `python3` dengan `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/rekap.py <file.csv> \
     --kolom-tanggal "Tanggal" --kolom-produk "Produk" \
     --kolom-qty "Qty" --kolom-total "Total"
   ```
   - Jika tidak ada kolom total tapi ada harga satuan, pakai `--kolom-harga "Harga"` sebagai ganti `--kolom-total`.
   - Jika ada kolom status pesanan (ekspor Shopee/Tokopedia), **selalu** tambahkan `--kolom-status "Status Pesanan"`
     agar pesanan batal/retur/refund tidak dihitung sebagai omzet.
   - Delimiter (`,` `;` tab), encoding Excel Windows, format angka (`Rp 15.000`, `Rp. 25000`, `15.000,-`, `15.000,50`),
     dan tanggal (`01/09/2026`, `2026-09-01 10:00`, `1 Sep 2026`, `1 Agustus 2026`) dideteksi otomatis.
   - Jika output berisi `peringatan` tentang urutan tanggal ambigu, tanyakan ke pengguna apakah formatnya
     hari/bulan (Indonesia) atau bulan/hari (AS); jika AS, jalankan ulang dengan `--urutan-tanggal mdy`.
   - Jika Python tidak tersedia, hitung manual langkah demi langkah dan beri tahu pengguna bahwa hasil belum diverifikasi script.
3. **Tulis rekap** berdasarkan output JSON script, dengan format di bawah.
4. **Beri 2–3 insight** yang bisa langsung ditindaklanjuti, berdasarkan angka.

## Format output

```
## Rekap Penjualan <tanggal awal> – <tanggal akhir>

**Total omzet:** Rp X
**Jumlah transaksi (baris):** N
**Rata-rata omzet per hari (kalender):** Rp Y  _(hari berjualan: Rp Z)_

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
- Jika script melaporkan baris yang dilewati (`baris_dilewati` > 0) atau `dibuang_karena_status`, sebutkan jumlah dan alasannya.
- Sampaikan setiap isi `peringatan` dari script kepada pengguna.
- Jika memakai `--kolom-status`, tampilkan ke pengguna status yang **dihitung** (`status_dihitung`) dan yang **dibuang**
  (`dibuang_karena_status`), agar pengguna bisa mengoreksi bila ada status yang salah golongan
  (mis. jalankan ulang dengan `--abaikan-status` berisi daftar sendiri).
- Jika `nama_produk_digabung` tidak kosong, sebutkan penggabungannya (mis. "Kopi" dan "kopi " dihitung sebagai satu produk).
- Angka dengan format meragukan (mis. `15.000.00`, `15000.500`, notasi ilmiah `1.5E+06` dari Excel) sengaja **dilewati**,
  bukan ditebak; sebutkan jumlahnya dan sarankan pengguna memperbaiki format kolom di Excel.
- Insight harus berdasarkan data; hindari saran generik seperti "tingkatkan pemasaran".
- Jangan mengirim isi file pengguna ke layanan eksternal.
