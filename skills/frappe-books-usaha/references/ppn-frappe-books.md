# PPN 12% dengan DPP nilai lain 11/12 di Frappe Books

**Dasar:** UU HPP & PMK 131/2024 — tarif PPN 12%; untuk barang/jasa **non-mewah** DPP memakai nilai lain
11/12 × harga jual, sehingga PPN efektif = 11% dari harga jual. Dicek 26 September 2026.
Alat bantu hitung, bukan nasihat pajak. Kasus khusus (barang mewah, fasilitas, PPN DTP, e-Faktur) → DJP (Kring Pajak 1500200)
atau konsultan pajak. Frappe Books **tidak** membuat e-Faktur; faktur resmi tetap lewat Coretax DJP.

## Pengaturan di Frappe Books
Buat satu template **Tax** (menu Setup → Taxes), mis. nama `PPN 11% (12% x 11/12)`, baris detail: akun `Hutang Pajak`
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
