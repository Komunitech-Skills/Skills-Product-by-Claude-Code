# 04 — Input tidak lengkap: "bikin neraca dong"

## Skenario
S4, input tidak lengkap. Pengguna tidak melampirkan data apa pun. Sesuai SKILL.md ("Input tidak lengkap"), agent meminta daftar transaksi dan mengajukan pertanyaan saldo awal **sekali** (maks 5 pertanyaan bernomor), sambil menawarkan template buku kas.

## Input pengguna
> bikin neraca dong buat usahaku

## Output

Siap, saya bantu. Neraca (Laporan Posisi Keuangan) paling akurat kalau dibuat dari catatan uang masuk-keluar, jadi sekalian saya buatkan juga Laporan Laba Rugi dan Catatan-nya sesuai SAK EMKM.

**Yang saya perlukan:**
Catatan transaksi selama periode yang mau dilaporkan (mis. Januari–Juni 2026). Boleh file CSV, atau tempel saja tabel dari Excel/Google Sheets/Notes di sini. Minimal ada kolom: **Tanggal, Keterangan, Uang Masuk, Uang Keluar**. Kalau file Excel (.xlsx), simpan dulu sebagai CSV (File › Download › CSV).

Belum punya catatan rapi? Pakai format ini:

```csv
Tanggal,Keterangan,Masuk,Keluar,Kategori
01/01/2026,Saldo awal,"Rp 0",,
02/01/2026,Penjualan harian,"Rp 0",,
03/01/2026,Belanja bahan baku,,"Rp 0",
05/01/2026,Bayar listrik,,"Rp 0",
10/01/2026,Ambil untuk keperluan pribadi,,"Rp 0",prive
```

**Sekalian, jawab singkat 5 hal ini (kira-kira saja tidak apa-apa):**
1. Berapa uang kas + saldo rekening usaha di **awal** periode?
2. Berapa nilai stok barang/bahan di **awal** dan di **akhir** periode?
3. Adakah pelanggan yang belum bayar, atau utang ke pemasok/bank (mis. KUR)? Berapa?
4. Punya peralatan/kendaraan usaha? Nilai kira-kira dan masih dipakai berapa tahun lagi?
5. Nama usaha untuk judul laporan?

Kalau mau cepat, kirim catatannya saja dan bilang "langsung aja". Nanti saya pakai nilai default (misalnya stok dianggap tetap) dan semua asumsinya saya tulis di laporan.

## Catatan penguji
- Sesuai SKILL.md: satu pesan, 5 pertanyaan bernomor, template `templates/buku-kas-template.csv` ditawarkan, ada jalan cepat "langsung aja", tidak mengarang angka.
- Bahasanya awam dan tidak menggurui. Istilah "neraca" dijembatani ke "Laporan Posisi Keuangan".
- Catatan: pertanyaan 3 menggabungkan piutang dan utang dalam satu nomor. Wajar untuk membatasi jumlah pertanyaan, tetapi pengguna awam kadang hanya menjawab separuh. Tidak dihitung sebagai cacat.
