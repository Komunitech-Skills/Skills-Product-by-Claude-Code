# Contoh 06 – Ekspor gaya Shopee dengan kolom status pesanan (uji ulang v1.1.0)

> ⚠️ **Untuk tim Komunitech:** contoh ini sengaja memperlihatkan **cacat B1 hasil uji ulang v1.1.0**. Angka di Output adalah hasil apa adanya bila SKILL.md diikuti persis. Satu pesanan berstatus **"Pengembalian Barang/Dana"** masih ikut dihitung sebagai omzet. Setelah cacat diperbaiki, jalankan ulang dan perbarui angka di contoh ini sebelum dipakai sebagai materi pembeli.

## Skenario
Skenario tambahan uji ulang v1.1.0 (fitur baru `--kolom-status`). Ekspor pesanan toko fashion pria gaya Shopee, Agustus 2026: 89 baris, pemisah koma, harga `Rp129.000`, dan kolom **Status Pesanan** berisi `Selesai` (60), `Batal` (15), `Sedang Dikirim` (13), dan `Pengembalian Barang/Dana` (1). Satu pesanan bisa terdiri dari beberapa baris produk. Data fiktif (dibuat penguji dengan seed tetap).

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
→ total_omzet 9051000, jumlah_baris_valid 74, dibuang_karena_status {"Batal": 15}, peringatan []
```

## Output

## Rekap Penjualan 1 – 31 Agustus 2026

**Total omzet:** Rp 9.051.000
**Jumlah transaksi (baris):** 74
**Rata-rata omzet per hari (kalender):** Rp 291.968  _(hari berjualan: Rp 335.222; 27 dari 31 hari ada penjualan)_

ℹ️ **15 baris berstatus "Batal" tidak dihitung** sebagai omzet, sesuai permintaanmu. Nilainya Rp 1.742.000.
Omzet di atas memakai kolom *Total Harga Produk* (sebelum ongkir, voucher, dan potongan biaya Shopee), jadi bukan uang bersih yang kamu terima.

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Kemeja Flanel Kotak | 26 | Rp 3.354.000 | 37,1% |
| 2 | Celana Chino Slim | 18 | Rp 2.682.000 | 29,6% |
| 3 | Topi Baseball | 26 | Rp 1.170.000 | 12,9% |
| 4 | Kaos Polos Hitam | 12 | Rp 660.000 | 7,3% |
| 5 | Kaos Polos Putih | 12 | Rp 660.000 | 7,3% |

### Tren harian
Hari terbaik: Kamis, 6 Agustus 2026 (Rp 1.054.000). Hari terendah: Jumat, 7 Agustus 2026 (Rp 100.000).
Ada 4 hari tanpa penjualan: 9, 13, 15, dan 21 Agustus.

### Insight
1. **Dua produk menyumbang dua pertiga omzet.** Kemeja Flanel (37,1%) dan Celana Chino (29,6%) bersama-sama menghasilkan Rp 6.036.000 (66,7%). Pastikan stok ukuran terlaris keduanya aman, dan coba paket "Flanel + Chino".
2. **Pembatalan cukup tinggi: 15 dari 89 baris (Rp 1.742.000, setara 19% dari omzet).** Cek alasan batal di Seller Center (stok kosong, pembeli berubah pikiran, atau telat kirim). Jika karena stok, sinkronkan stok lebih sering.
3. **Topi Baseball laku banyak (26 pcs) tapi harganya rendah.** Jadikan add-on di halaman Kemeja/Chino untuk menaikkan nilai per pesanan.

## Catatan penguji
- **Fitur baru bekerja sebagian:** `--kolom-status` membuang 15 baris "Batal" dan melaporkannya di `dibuang_karena_status`.
- **❌ Cacat B1 (baru):** baris **"Pengembalian Barang/Dana"** (Topi Baseball, Rp 45.000, 24 Agustus) **tetap dihitung sebagai omzet tanpa peringatan**. Daftar default `STATUS_BATAL_DEFAULT` hanya berisi `batal, dibatalkan, cancel, retur, return, refund, gagal, failed`. Kata Indonesia "**pengembalian**" dan "**dikembalikan**" tidak ada, padahal SKILL.md berjanji "selalu tambahkan `--kolom-status` agar pesanan batal/retur/refund tidak dihitung". Script juga tidak melaporkan status apa saja yang **ikut dihitung**, sehingga agent tidak bisa menyadarinya.
- **Verifikasi independen** (parser & filter milik penguji, `verif6.py`):
  | | Script (default) | Seharusnya (tanpa pengembalian) |
  |---|---|---|
  | Total omzet | Rp 9.051.000 | **Rp 9.006.000** |
  | Baris valid | 74 | **73** |
  | Topi Baseball | 26 pcs, Rp 1.170.000 (12,9%) | **25 pcs, Rp 1.125.000 (12,5%)** |
  | Hari terendah | Jumat, 7 Agustus (Rp 100.000) | **Senin, 24 Agustus (Rp 55.000)** |
  Perhitungan script dengan filter bawaannya sendiri **cocok 100%** dengan penguji. Masalahnya ada pada daftar kata status, bukan pada aritmetika.
- **Catatan tambahan:** baris "Sedang Dikirim" (13 baris, Rp 1.512.000) ikut dihitung. Ini wajar untuk omzet bruto, tapi sebaiknya disebut ke pengguna. Pada uji tepi terpisah, status **"Belum Bayar"** juga ikut dihitung sebagai omzet.
- **Catatan tambahan:** hari terendah seri (7 dan 24 Agustus sama-sama Rp 100.000 menurut script), tapi hanya satu yang dilaporkan, tanpa keterangan seri.
- Bagus: agent memberi tahu bahwa omzet belum dikurangi ongkir/voucher/biaya marketplace. Ini penting untuk ekspor marketplace, tapi berasal dari inisiatif agent, bukan instruksi SKILL.md.
