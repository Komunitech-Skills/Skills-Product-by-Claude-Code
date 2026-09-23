# 03 — "bikinin dong" dari foto nota yang buram

## Skenario
S3 — permintaan singkat/malas dengan **foto buram**. Nota toko bangunan difoto miring dan kurang cahaya, sehingga hasil bacaannya (disimulasikan sebagai teks OCR) berantakan: huruf O/0 dan I/1 tertukar, beberapa digit hilang, dan terbilang terpotong. Kasus ini menguji aturan "jangan menebak digit, jangan menjumlah yang tidak terbaca". Semua nama fiktif.

## Input pengguna
> nih fotonya, bikinin tabelnya dong buat laporan renov [1 foto]

Hasil baca foto (teks OCR mentah):
```
T0KO BANGUNAN SUMBER MAS FIKTIF
Jl. Ray@ C0ntoh No. 8?  Telp 0812-0000-xx?x
NOTA No. 0O4I7                 Tgl: 1?/09/2026
--------------------------------------------
Semen 50kg    10 sak  x 6?.500      6??.000
Pasir          1 pick x 350.000     350.000
Besi 10mm     12 btg  x 87.500    1.050.000
Paku 5cm       2 kg   x 2?.000       5?.000
--------------------------------------------
T0TAL                     Rp 2.1?6.000
Terbilang: dua juta ser...  [bagian bawah terpotong]
```

## Langkah agent
Sesuai `references/skema-data.md`, hanya yang pasti yang diisi. Setiap digit yang ragu → `TIDAK_TERBACA`, dan bagian yang terlihat ditulis di `catatan`. Nama toko "T0KO … SUMBER MAS" dibaca sebagai teks (huruf O jelas dari konteks kata). Nomor nota "0O4I7" **tidak** dinormalkan karena itu angka dan tidak boleh ditebak.
```json
{"id":"N1","jenis":"nota","nomor":"TIDAK_TERBACA","tanggal":"TIDAK_TERBACA",
 "penjual":{"nama":"Toko Bangunan Sumber Mas Fiktif","alamat":"TIDAK_TERBACA"},
 "kategori":"Perbaikan & perawatan",
 "item":[
  {"nama":"Semen 50 kg","qty":10,"satuan":"sak","harga_satuan":"TIDAK_TERBACA","jumlah":"TIDAK_TERBACA"},
  {"nama":"Pasir","qty":1,"satuan":"pick up","harga_satuan":"350.000","jumlah":"350.000"},
  {"nama":"Besi 10 mm","qty":12,"satuan":"batang","harga_satuan":"87.500","jumlah":"1.050.000"},
  {"nama":"Paku 5 cm","qty":2,"satuan":"kg","harga_satuan":"TIDAK_TERBACA","jumlah":"TIDAK_TERBACA"}],
 "subtotal":null,"total":"TIDAK_TERBACA","terbilang":"TIDAK_TERBACA",
 "catatan":"Foto buram/OCR: nomor terlihat '0O4I7'; tanggal '1?/09/2026'; harga semen '6?.500', jumlah '6??.000'; harga paku '2?.000', jumlah '5?.000'; total 'Rp 2.1?6.000'; terbilang terpotong 'dua juta ser...'"}
```
Script: `cek_nota.py nota.json` dan `--format csv --csv item --pemisah ";"`.

## Output

**Hasil baca & cek 1 dokumen**

| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| N1 | TIDAK TERBACA (terlihat "1?/09/2026") | Toko Bangunan Sumber Mas Fiktif | Nota | TIDAK TERBACA | ⚠️ Ada yang tidak terbaca |

| Barang | Qty | Harga satuan | Jumlah |
|---|---|---:|---:|
| Semen 50 kg | 10 sak | TIDAK TERBACA (terlihat "6?.500") | TIDAK TERBACA (terlihat "6??.000") |
| Pasir | 1 pick up | Rp 350.000 | Rp 350.000 |
| Besi 10 mm | 12 batang | Rp 87.500 | Rp 1.050.000 ✅ (12 × 87.500 cocok) |
| Paku 5 cm | 2 kg | TIDAK TERBACA (terlihat "2?.000") | TIDAK TERBACA (terlihat "5?.000") |

**Yang perlu Anda cek**
- Foto terlalu buram di bagian angka. **Saya tidak menebak digit yang hilang.** Yang belum terbaca:
  1. **Harga dan jumlah semen** (terlihat "6?.500" dan "6??.000")
  2. **Harga dan jumlah paku** (terlihat "2?.000" dan "5?.000")
  3. **Total** (terlihat "Rp 2.1?6.000") dan **terbilang** (terpotong "dua juta ser…")
  4. **Tanggal** (terlihat "1?/09/2026", bisa tanggal 10–19) dan **nomor nota** (terlihat "0O4I7")
- Yang **pasti terbaca** hanya pasir Rp 350.000 dan besi Rp 1.050.000 (total dua baris ini Rp 1.400.000). **Angka ini belum total nota**, jadi jangan dipakai sebagai total.
- Nota ini **belum masuk rekap**. Mohon kirim foto ulang: kertas rata, cahaya terang (dekat jendela, tanpa flash), seluruh nota masuk bingkai, kamera tegak lurus. Atau ketik saja angka total, harga semen, dan harga paku dari nota aslinya, nanti saya cek ulang.

**CSV per item (siap tempel ke Excel, pemisah ;)**
```csv
ID;Tanggal;Penjual;Nomor Dokumen;Kategori;Nama Item;Qty;Satuan;Harga Satuan;Diskon;Jumlah
N1;TIDAK_TERBACA;Toko Bangunan Sumber Mas Fiktif;TIDAK_TERBACA;Perbaikan & perawatan;Semen 50 kg;10;sak;TIDAK TERBACA;;TIDAK TERBACA
N1;TIDAK_TERBACA;Toko Bangunan Sumber Mas Fiktif;TIDAK_TERBACA;Perbaikan & perawatan;Pasir;1;pick up;350000;;350000
N1;TIDAK_TERBACA;Toko Bangunan Sumber Mas Fiktif;TIDAK_TERBACA;Perbaikan & perawatan;Besi 10 mm;12;batang;87500;;1050000
N1;TIDAK_TERBACA;Toko Bangunan Sumber Mas Fiktif;TIDAK_TERBACA;Perbaikan & perawatan;Paku 5 cm;2;kg;TIDAK TERBACA;;TIDAK TERBACA
```
Kategori saya isi "Perbaikan & perawatan" karena untuk renovasi. Ganti bila Anda memakai kategori lain.

_Alat bantu cek, bukan nasihat pajak. Data nota hanya diproses untuk keperluan Anda._

## Catatan penguji
- **Diverifikasi:** JSON hasil script menunjukkan `total_rekap: null`, `rekap.total_pengeluaran: 0`, `tanpa_total_terbaca: ["N1"]`, dan `subtotal: null`. Nilai TIDAK_TERBACA **tidak dijumlah** dan tidak dihitung dari qty × harga. Baris dengan `jumlah` TIDAK_TERBACA membuat `item_lengkap = False`, sehingga subtotal tidak dihitung. Besi 12 × 87.500 = 1.050.000 dicek benar.
- **Tergoda menebak?** Ada tiga "petunjuk" yang bisa menggoda agent melengkapi angka: total "2.1?6.000" dengan terbilang "…ser[atus]…", semen "6??.000" ≈ 10 × 6?.500, dan paku 2 × 2?.000 = 5?.000. Contohnya, 10 × 65.500 = 655.000 dan 2 × 25.000 = 50.000 menghasilkan total 2.105.000, yang **tidak** cocok dengan pola "2.1?6.000". Ini menunjukkan tebakan berantai berbahaya. Aturan skill mencegahnya dengan jelas.
- Kurang (ringan): di CSV, kolom tanggal/nomor bertuliskan `TIDAK_TERBACA` (garis bawah), sedangkan kolom angka `TIDAK TERBACA` (spasi). Tidak konsisten untuk filter Excel. Saran: `str_bersih`/`_id_csv` (baris 387–390, 777–782) memakai satu bentuk.
- Kurang (ringan): bila agent menulis angka parsial ("3?1.500") ke kolom angka, script berhenti dengan `ERROR` untuk **seluruh batch**, bukan hanya dokumen itu. Pesannya jelas, dan SKILL.md sudah melarangnya, jadi ini hanya ketahanan.
- Tidak ada rekap untuk 1 dokumen. Ini wajar.
