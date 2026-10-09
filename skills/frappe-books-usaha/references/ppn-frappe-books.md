# PPN 12% dengan DPP nilai lain 11/12 di Frappe Books

**Dasar:** UU HPP & PMK 131/2024 — tarif PPN 12%; untuk barang/jasa **non-mewah** DPP memakai nilai lain
11/12 × harga jual, sehingga PPN efektif = 11% dari harga jual. Dicek 26 September 2026.
Alat bantu hitung, bukan nasihat pajak. Kasus khusus (barang mewah, fasilitas, PPN DTP, e-Faktur) → DJP (Kring Pajak 1500200)
atau konsultan pajak. Frappe Books **tidak** membuat e-Faktur; faktur resmi tetap lewat Coretax DJP.

## Pengaturan di Frappe Books
Buat satu template **Tax** (menu Setup → Tax Templates), mis. nama `PPN 11% (12% x 11/12)`, baris detail: akun `Hutang Pajak`
(atau akun PPN keluaran Anda), **tarif 11**. Pasang template itu di barang (kolom Tax) atau per baris invoice.
Jangan pakai tarif 12 dari harga penuh untuk barang/jasa non-mewah — PPN jadi terlalu besar. Perintah `akun` memberi
peringatan bila menemukan template bertarif 12%.

## Standar pembulatan Komunitech (perintah `ppn` dan pratinjau `csv-transaksi`)
- PPN = DPP × 11/12 × 12% dihitung **persis**, lalu **dibulatkan ke bawah sekali** (tidak pernah memungut melebihi tarif).
- Nominal lain (total baris) dibulatkan ke rupiah terdekat.
- Harga termasuk PPN: DPP = rupiah bulat terbesar dengan DPP + PPN ≤ harga; sisanya ditampilkan.
- **Pembulatan belum dicocokkan dengan Coretax.**

## Kenapa angka Frappe Books bisa beda sedikit
Frappe Books menghitung pajak **per baris** (jumlah baris × 11/100) dan menyimpannya tanpa pembulatan (presisi internal),
lalu menampilkan 2 desimal. Contoh DPP Rp 332.345: Frappe Books menampilkan PPN Rp 36.557,95, standar Komunitech Rp 36.557.
Sampaikan kedua angka apa adanya; jangan mengubah data di Frappe Books. Nilai resmi mengikuti faktur di Coretax.

## PPN per periode (`ppn-periode`)
```
python3 scripts/frappe_books.py ppn-periode --db "<path>" --bulan 2026-09
```
- Hanya invoice **final** (draf & batal tidak dihitung). Retur mengurangi.
- **Baris kena PPN** = baris invoice yang diberi template pajak bertarif > 0. Baris tanpa template (atau tarif 0) dicetak
  terpisah sebagai "TANPA PPN" dan **tidak** masuk DPP PPN.
- PPN dihitung **per faktur**: DPP kena PPN × 11/12 × 12%, dibulatkan ke bawah, lalu dijumlah. Template bertarif selain 11%
  tetap dihitung 11% (standar non-mewah) dan diberi catatan.
- Keluaran − masukan > 0 → **kurang bayar** (disetor); < 0 → **lebih bayar** (tidak ada setoran; kompensasi ke masa berikutnya
  atau restitusi sesuai ketentuan DJP).
- "PPN tercatat di Frappe" dicetak berdampingan. Sama → pengaturan pajak sudah sesuai. Beda < Rp 1 → pecahan pembulatan.
  Beda lebih besar → script menyebut nomor notanya; cek nota itu, jangan langsung menyimpulkan template salah.
- Syarat: usaha **PKP**; PPN masukan hanya bisa dikreditkan dengan faktur pajak masukan yang sah (angka faktur pemasok yang
  dipakai bila berbeda). Pelaporan & setoran lewat Coretax DJP. **Pembulatan belum dicocokkan dengan Coretax.**
- Contoh data uji (fiktif, TB Sumber Rejeki, Sep 2026): DPP kena PPN Rp 4.650.000 → keluaran Rp 511.500; penjualan tanpa PPN
  Rp 160.000; masukan Rp 605.000; selisih −Rp 93.500 (lebih bayar). Salah umum: 12% × 11/12 × total Rp 4.810.000 = Rp 529.100.
