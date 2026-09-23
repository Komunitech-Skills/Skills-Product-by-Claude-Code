# Hitung Manual (fallback jika Python tidak bisa dijalankan)

Beri tahu pengguna: "Script tidak bisa dijalankan, jadi angka ini dihitung manual dan belum diverifikasi script. Mohon dicek ulang."

## Langkah
1. **Bulatkan** setiap nominal ke rupiah terdekat (0,5 ke atas). Semua penjumlahan memakai angka bulat.
2. **Klasifikasikan** tiap baris memakai tabel di `pemetaan-kategori.md`. Baris yang tidak jelas → tanyakan; sementara catat sebagai "lain-lain (perlu dicek)".
3. **Jumlahkan per kategori** dalam tabel kerja (kategori | jumlah transaksi | total).
4. **Hitung:**
   - Penjualan tempo = piutang akhir − piutang awal + penerimaan piutang (jika hasil negatif → 0, dan selisihnya menjadi beban piutang tak tertagih)
   - Pendapatan usaha bersih = penjualan tunai + penjualan tempo − retur
   - Pembelian tempo = utang pemasok akhir − utang pemasok awal + pembayaran utang pemasok (negatif → 0)
   - HPP = persediaan awal + (pembelian tunai + pembelian tempo) − persediaan akhir
   - Laba kotor = pendapatan usaha bersih − HPP
   - Penyusutan (garis lurus) per bulan = nilai aset ÷ (umur tahun × 12); aset baru mulai bulan berikutnya
   - Laba usaha = laba kotor − semua beban usaha (termasuk penyusutan)
   - Laba sebelum pajak = laba usaha + pendapatan lain − beban keuangan
   - Laba bersih = laba sebelum pajak − beban PPh
5. **Neraca akhir:**
   - Kas = kas awal + total masuk − total keluar (transfer ke rekening sendiri tetap dihitung sebagai kas/setara kas)
   - Aset tetap = awal + pembelian − penyusutan
   - Utang bank = awal + pinjaman diterima − cicilan pokok
   - Modal awal = aset awal − utang awal (jika tidak diberikan)
   - Modal akhir = modal awal + setoran modal + laba bersih − prive
   - **Cek:** total aset − (total liabilitas + modal akhir) harus 0. Jika tidak, tampilkan selisihnya.
6. Sajikan dengan format output di SKILL.md dan cantumkan asumsi + disclaimer.

## Contoh angka kecil
Kas awal Rp 1.000.000; jual Rp 5.000.000; beli bahan Rp 2.000.000; gaji Rp 1.000.000; prive Rp 500.000; stok awal 0, stok akhir Rp 300.000.
- HPP = 0 + 2.000.000 − 300.000 = Rp 1.700.000
- Laba bersih = 5.000.000 − 1.700.000 − 1.000.000 = Rp 2.300.000
- Kas akhir = 1.000.000 + 5.000.000 − 3.500.000 = Rp 2.500.000
- Modal akhir = 1.000.000 + 2.300.000 − 500.000 = Rp 2.800.000
- Aset = 2.500.000 + 300.000 = Rp 2.800.000 = liabilitas 0 + modal 2.800.000 ✔
