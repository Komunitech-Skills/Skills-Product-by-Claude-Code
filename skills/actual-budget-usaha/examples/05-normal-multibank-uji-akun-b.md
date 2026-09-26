# Skenario 5 (normal) — BRI, Mandiri, BNI sekaligus (uji Akun B)

**Pengguna (pemilik warung kopi + freelancer):** "Ini mutasi BRI warung, Mandiri pribadi, sama BNI. Jadikan file
impor Actual."

File fiktif buatan penguji:
- BRI: UTF-8 **dengan BOM**, `TGL_TRAN` berjam, angka `"2.900.000,00"`, baris SALDO AWAL bernilai 0, saldo minus.
- Mandiri: pemisah `;`, **cp1252** (tanda pisah `–`), `01 Agu 2026`, baris Saldo Awal/Akhir tanpa nominal,
  bayar kartu kredit, refund, dan nominal kecil `12,5`.
- BNI: `Tipe` = `Cr.`/`Db.`, angka bulat `"7.500.000"`, pencairan pinjaman KUR.

| File | Terbaca/Dilewati/Ragu | Cek saldo | Impor via API Actual 26.9.0 (akun kosong) |
|---|---|---|---|
| BRI | 6 / 1 (saldo awal 0) / 6 | COCOK 5.000.000 → 16.845.000,75 | 6 baris, 0 galat, jumlah persis, saldo +11.845.000,75 ✔ |
| Mandiri | 5 / 2 / 3 | COCOK 1.000.000 → 4.324.987,75 | 5 baris, 0 galat, `-12.50` persis, 2/2 kategori ✔ |
| BNI (tanpa `--db`) | 4 / 1 / 1 | COCOK 2.000.000 → 34.075.000 | 4 baris, 0 galat, jumlah persis; **0/3 kategori terpasang** (nama bawaan tidak ada di budget) |

Baris ragu yang ditandai benar: SETORAN TUNAI LACI (pindah dana), TRF KE KARTU KREDIT (pindah dana), REFUND SHOPEE
("masukkan ke kategori asal, bukan pendapatan"), PENCAIRAN PINJAMAN KUR Rp 25 jt ("BUKAN pendapatan"), PLN/PAYROLL
(kategori usulan belum ada di budget warung).

Temuan:
1. **SETORAN PENJUALAN QRIS Rp 18.250.000,75 ditandai "PINDAH DANA"** karena pola `SETORAN` saja. Tidak salah
   kategori (baris dikosongkan dan ditanyakan), tetapi pesannya menyesatkan untuk warung — ini pendapatan
   penjualan. Disarankan pola hanya `SETOR(AN)? TUNAI`, atau pengecualian `SETORAN PENJUALAN`.
2. BNI tanpa `--db`: script sudah memberi catatan "nama kategori BELUM dicocokkan ... jalankan ulang dengan --db".
   Terbukti penting: tanpa itu 3 kategori hilang diam-diam saat impor.
3. `12,5` dibaca Rp 12,50 karena gaya angka file = koma; konsisten dengan kolom saldo. Namun
   `references/format-bank.md` menulis angka seperti `12,5` "tanpa petunjuk lain → dilewati"; pada file berisi hanya
   `"12,5"` dan `"1.500"` script **tidak** melewatinya (12,50 dan 1.500). Perilaku wajar, dokumentasi perlu diselaraskan.

**Hasil: LULUS** dengan catatan temuan 1 & 3.
