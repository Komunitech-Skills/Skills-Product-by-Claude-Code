# Kategori usulan & kata kunci bawaan

Nama kategori di bawah hanyalah **usulan**. Actual hanya mengisi kategori bila namanya **sama persis** dengan kategori
di budget pengguna. Jalankan `konversi ... --db <budget>` supaya nama dicocokkan (beda huruf besar/kecil dibetulkan
otomatis; nama yang tidak ada dikosongkan dan masuk daftar "perlu dicek").

## Susunan awal yang disarankan (buat di Actual sekali, boleh diubah)
Tanyakan dulu apakah pengguna memisahkan rekening usaha & pribadi. Bila satu rekening dipakai bersama, tambahkan grup
"Kebutuhan Pribadi" supaya belanja pribadi tidak tercampur biaya usaha.

| Grup | Kategori | Kata kunci bawaan (tidak peka huruf besar/kecil) |
|---|---|---|
| Pemasukan (grup income) | Pendapatan Usaha | SETORAN PENJUALAN/HASIL/OMZET, QRIS, SETTLEMENT, MERCHANT, EDC, dan semua uang masuk yang tidak cocok aturan lain |
| | Pendapatan Lain | BUNGA, INTEREST, JASA GIRO |
| Biaya Usaha | Sewa | SEWA, KONTRAKAN, KOS, COWORKING, RUKO |
| | Listrik & Air | PLN, LISTRIK, TOKEN, PDAM, AIR |
| | Internet & Pulsa | TELKOMSEL, INDOSAT, XL, SMARTFREN, PULSA, INDIHOME, BIZNET, WIFI, ... |
| | Software & Langganan | ADOBE, CANVA, FIGMA, MICROSOFT, GOOGLE WORKSPACE, ZOOM, HOSTING, DOMAIN, ... |
| | Iklan & Promosi | FACEBOOK, META, GOOGLE ADS, TIKTOK ADS, IKLAN |
| | Transportasi | PERTAMINA, SPBU, TOL, GOJEK, GRAB, PARKIR, KAI, TIKET |
| | Ongkir & Kurir | JNE, J&T, SICEPAT, ANTERAJA, POS INDONESIA, ONGKIR |
| | Gaji & Honor | GAJI, PAYROLL, HONOR, UPAH, THR |
| | BPJS | BPJS |
| | Biaya Bank | BIAYA ADM, BIAYA ADMIN, BIAYA TRANSFER, FEE, MATERAI |
| | Cicilan & Pinjaman | ANGSURAN, CICILAN, KUR, LEASING, PINJAMAN |
| Dana Cadangan | Pajak | PAJAK, DJP, MPN, BILLING PAJAK, PBB, SAMSAT |
| | Dana Darurat | (diisi anggaran, bukan dari mutasi) |

## Selalu masuk daftar "perlu dicek" (kategori dikosongkan)
- **Setor tunai** (SETOR TUNAI, CASH DEPOSIT): diberi usulan (mis. hasil jualan tunai) dalam satu konfirmasi. Hasil jualan tunai yang belum tercatat → kategori
  pemasukan; uang dari laci/dompet yang sudah tercatat di akun Actual lain → transfer. Setoran yang jelas hasil
  usaha (SETORAN PENJUALAN/HASIL/OMZET, QRIS, SETTLEMENT/MERCHANT, EDC) langsung diusulkan "Pendapatan Usaha".
- **Pindah dana milik sendiri**: TARIK TUNAI/TARIKAN ATM, TOP UP/GOPAY/OVO/DANA/SHOPEEPAY/FLAZZ,
  pembayaran KARTU KREDIT. Di Actual ini harus **transfer** (Payee = akun tujuan, misalnya akun "Kas Tunai" atau
  "GoPay"), bukan pengeluaran; kalau diberi kategori, pengeluaran terhitung dua kali.
- **Marketplace** (Tokopedia, Shopee, Lazada, ...) dan **minimarket/supermarket**: bisa usaha atau pribadi.
- **Refund/retur/koreksi**: masukkan ke kategori pengeluaran asalnya, bukan pendapatan.
- **Pencairan pinjaman**: bukan pendapatan.
- Uang keluar yang tidak cocok kata kunci mana pun.
- Baris yang persis sama muncul lebih dari sekali di satu file (mungkin dobel, mungkin memang dua transaksi).

## Aturan sendiri (`--peta`)
File CSV `kata_kunci,kategori,arah` (arah `masuk`/`keluar`/kosong). Kata kunci = teks biasa, dicari di keterangan
mutasi. Aturan pengguna dicek **sebelum** aturan bawaan. Contoh:
```
kata_kunci,kategori,arah
ROASTERY GAYO,Bahan Baku,keluar
PT MAJU KREATIF,Pendapatan Proyek,masuk
```
Simpan file ini di samping budget pengguna (mis. `Documents/Actual/aturan-kategori.csv`) agar dipakai tiap bulan.
