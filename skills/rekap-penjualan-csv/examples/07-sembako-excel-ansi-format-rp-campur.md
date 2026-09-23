# Contoh 07 – CSV dari Excel Windows (ANSI), format rupiah campur `Rp.`/`,-`, tanggal teks

## Skenario
Skenario tambahan uji ulang v1.1.0 untuk memastikan **cacat berat B1 dan cacat sedang S1, S2, S6 dari uji pertama sudah diperbaiki**. Pemilik toko sembako mengetik penjualan seminggu di Excel lalu menyimpannya sebagai CSV (encoding Windows-1252/ANSI, pemisah `;`, ada karakter `½`). Kolom total ditulis campur: `Rp. 29000`, `Rp.87.000`, `29.000,-`, `Rp 12.500,-`. Tanggal ditulis teks: `14 Sept 2026`, `15 September 2026`, `16 Sep 2026`. Data fiktif (dibuat penguji dengan seed tetap, 26 baris).

## Input pengguna
```
ini catatan jualan toko sembako aku minggu kemarin, aku ketik di excel terus save as CSV. rekapin ya
```
Cuplikan file (ditampilkan setelah dikonversi ke UTF-8):
```
Tanggal;Barang;Jumlah;Total
14 Sept 2026;Kopi Sachet (renceng);3;Rp.39.000
14 Sep 2026;Beras Pandan Wangi 5 kg;3;Rp.234.000
14 Sept 2026;Telur Ayam 1 kg;1;Rp. 29000
15 Sept 2026;Telur Ayam 1 kg;1;29.000,-
15 September 2026;Gula Pasir ½ kg;3;Rp.28.500
```

## Proses (dijalankan agent)
```
$ python3 scripts/rekap.py penjualan-sembako.csv --kolom-tanggal "Tanggal" --kolom-produk "Barang" \
    --kolom-qty "Jumlah" --kolom-total "Total"
→ total_omzet 2538500, jumlah_baris_valid 26, baris_dilewati 0,
  peringatan ["File dibaca dengan encoding cp1252 (bukan UTF-8)."]
```

## Output

## Rekap Penjualan 14 – 20 September 2026

**Total omzet:** Rp 2.538.500
**Jumlah transaksi (baris):** 26
**Rata-rata omzet per hari (kalender):** Rp 362.643  _(hari berjualan: Rp 362.643; 7 dari 7 hari ada penjualan)_

ℹ️ File kamu tersimpan dengan format teks bawaan Excel Windows (bukan UTF-8). Semua baris tetap terbaca dengan benar, termasuk tanda "½". Tidak ada baris yang dilewati.

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Beras Pandan Wangi 5 kg | 18 | Rp 1.404.000 | 55,3% |
| 2 | Telur Ayam 1 kg | 17 | Rp 493.000 | 19,4% |
| 3 | Minyak Goreng 2 L | 10 | Rp 380.000 | 15,0% |
| 4 | Kopi Sachet (renceng) | 15 | Rp 195.000 | 7,7% |
| 5 | Gula Pasir ½ kg | 7 | Rp 66.500 | 2,6% |

### Tren harian
Hari terbaik: Rabu, 16 September 2026 (Rp 544.000). Hari terendah: Minggu, 20 September 2026 (Rp 136.000).

### Insight
1. **Beras menyumbang lebih dari separuh omzet (55,3%).** Beras dan telur bersama-sama menyumbang Rp 1.897.000 (74,7%). Stok dua barang ini paling menentukan. Jangan sampai kosong, terutama menjelang hari Rabu–Kamis yang paling ramai minggu ini.
2. **Minggu, 20 September jauh di bawah rata-rata** (Rp 136.000 vs rata-rata Rp 362.643 per hari). Cek apakah toko buka lebih singkat hari itu. Kalau memang sepi setiap Minggu, jam buka bisa disesuaikan.
3. **Rapikan cara menulis total** supaya catatan lebih mudah dibaca orang lain. Pilih satu format saja, misalnya `29000` (angka saja) atau `Rp 29.000`. Saat ini ada 4 gaya berbeda (`Rp.`, `Rp. `, `,-`, dan tanpa Rp). Semuanya terbaca dengan benar, jadi angka di atas tidak terpengaruh.

## Catatan penguji
- **Perbaikan terbukti:** pada v1.0.0, format `Rp. 29000` terbaca **0,29** (cacat berat B1), `29.000,-` dibuang (S1), file ANSI gagal dibaca (S2), dan tanggal teks `14 Sept 2026` dilewati (S6). Di v1.1.0 **semua 26 baris terbaca dengan benar**.
- **Verifikasi independen** (`/tmp/uji-rekap-penjualan-csv/v110/verif7.py`, parser penguji sendiri: decode cp1252, buang `Rp.`/`Rp`/`,-`/titik ribuan secara eksplisit, peta bulan sendiri): total Rp 2.538.500, 26 baris, rata-rata Rp 362.642,86, top-5 (qty, omzet, %), hari terbaik 16/9 Rp 544.000, dan terendah 20/9 Rp 136.000. Semuanya **COCOK 100%**. Nama hari dicek dengan `datetime`: 16/9/2026 Rabu, 20/9/2026 Minggu.
- **Bagus:** peringatan encoding dari script disampaikan dengan bahasa awam, sesuai SKILL.md ("Sampaikan setiap isi `peringatan`"). Insight 3 berbasis data (4 gaya penulisan) dan bisa ditindaklanjuti.
- Angka turunan (74,7%, Rp 1.897.000) dihitung agent dari JSON. Aturan SKILL.md tentang angka turunan belum diperjelas (lihat HASIL-UJI R2).
- **Uji ulang v1.2.0 (2026-09-23):** hasil identik (Rp 2.538.500, 26 baris, peringatan encoding cp1252) dan cocok dengan verifikasi independen.
