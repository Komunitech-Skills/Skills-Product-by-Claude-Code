# Contoh 03 – Permintaan singkat, file berisi baris rusak

## Skenario
S3, permintaan singkat/malas. File catatan penjualan kue kering yang diketik manual: nama kolom tidak baku (`tgl, item, jml, total`), tanggal tanpa nol di depan (`15/9/2026`), total berupa angka polos. Ada 3 baris bermasalah: tanggal kosong, tanggal ditulis "kemarin", dan total "-".

## Input pengguna
```
rekapin dong penjualan kue minggu ini, filenya aku lampirin
```
Cuplikan file (`kue-minggu3.csv`):
```
tgl,item,jml,total
15/9/2026,Putri Salju 500gr,2,150000
15/9/2026,Putri Salju 500gr,3,225000
15/9/2026,Kastengel 500gr,1,95000
,Nastar Keju 500gr,1,85000
...
17/9/2026,Kastengel 500gr,2,-
...
kemarin,Putri Salju 500gr,1,75000
```

## Output

## Rekap Penjualan 15 – 21 September 2026

**Total omzet:** Rp 4.220.000
**Jumlah transaksi (baris):** 27
**Rata-rata omzet per hari (kalender):** Rp 602.857  _(hari berjualan: Rp 602.857; 7 dari 7 hari ada penjualan)_

⚠️ **3 baris dilewati** dan tidak ikut dihitung:
- 2 baris karena **tanggal tidak valid**: 1 baris tanggalnya kosong (Nastar Keju 500gr, 1 pcs, Rp 85.000) dan 1 baris tertulis "kemarin" (Putri Salju 500gr, 1 pcs, Rp 75.000).
- 1 baris karena **total tidak valid**: Kastengel 500gr, 2 pcs, tanggal 17/9/2026, kolom total berisi "-".

Kalau ketiga baris ini dilengkapi, omzet minggu ini bertambah Rp 160.000 dari dua baris pertama, ditambah nilai 2 Kastengel yang totalnya belum diisi.

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Nastar Keju 500gr | 17 | Rp 1.445.000 | 34,2% |
| 2 | Putri Salju 500gr | 19 | Rp 1.425.000 | 33,8% |
| 3 | Kastengel 500gr | 9 | Rp 855.000 | 20,3% |
| 4 | Lidah Kucing 250gr | 9 | Rp 495.000 | 11,7% |

(Hanya ada 4 produk di file ini.)

### Tren harian
Hari terbaik: Rabu, 16 September 2026 (Rp 1.045.000). Hari terendah: Minggu, 20 September 2026 (Rp 260.000).

### Insight
1. **Nastar dan Putri Salju bersaing ketat.** Selisih omzetnya hanya Rp 20.000, tapi Putri Salju terjual lebih banyak (19 vs 17 toples). Keduanya menyumbang 68% omzet, jadi prioritaskan bahan dan jadwal produksi untuk dua kue ini.
2. **Kastengel paling mahal tapi paling jarang dibeli** (9 toples, sama dengan Lidah Kucing). Coba tawarkan sebagai tambahan di paket bersama Nastar supaya ikut terangkat.
3. **Rapikan pencatatan.** 3 dari 30 baris (10%) tidak bisa dihitung. Isi tanggal dengan format `tgl/bln/tahun` (bukan "kemarin") dan jangan kosongkan kolom total, supaya rekap berikutnya lengkap.

## Catatan penguji
- Perintah: `python3 <skill>/scripts/rekap.py kue-minggu3.csv --kolom-tanggal "tgl" --kolom-produk "item" --kolom-qty "jml" --kolom-total "total"`. Nama kolom tidak baku berhasil dicocokkan agent dari baris header.
- **Verifikasi independen:** dihitung ulang dengan Python terpisah. Total Rp 4.220.000, 27 baris valid, top-4, dan hari terbaik/terendah **cocok 100%**. Script melaporkan `baris_dilewati: 3` dengan alasan yang benar.
- Bagus: sesuai aturan SKILL.md, jumlah dan alasan baris yang dilewati disebutkan. Agent menambah nilai dengan menunjukkan baris mana yang rusak (dilihat langsung dari file), meskipun script hanya melaporkan jumlahnya.
- Saran: script sebaiknya mengembalikan nomor baris yang dilewati (misalnya `contoh_baris_dilewati: [5, 11, 16]`) supaya agent tidak perlu mencari sendiri.
- Catatan: "68%" adalah angka turunan (34,2% + 33,8%).
- **Uji ulang v1.1.0 (2026-09-23):** hasil identik (Rp 4.220.000, 27 baris valid, 3 dilewati dengan alasan `tanggal tidak terbaca: 2`, `harga/total tidak valid atau meragukan: 1`) dan cocok dengan verifikasi independen. Saran nomor baris yang dilewati (`contoh_baris_dilewati`) **belum** diterapkan.
