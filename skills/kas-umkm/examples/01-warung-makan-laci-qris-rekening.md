# Uji 01 — Warung makan: laci + QRIS + rekening + e-wallet (normal)

Penguji independen Akun B, 2026-09-26. Data rekaan. Dijalankan dari salinan skill di scratchpad (`kas.py` v1.0.0), database terpisah.

## Permintaan pengguna (disimulasikan)
> "Bikinin buku kas buat Warung Makan Bu Tini. Laci 500rb, BRI 3 juta (QRIS masuk ke BRI), GoPay 150rb, mulai 21/09/2026.
> Kamis 24/09: jualan tunai 1,2jt, QRIS 350rb, beli es batu & gas 85rb, jajan anak 100rb, token PLN 200rb dari BRI.
> Jumat 25/09: tunai 1.450.000, QRIS 420rb, GoFood 75rb (GoPay), belanja pasar 650rb, gaji harian 2 orang 300rb, setor laci ke BRI 1jt (biaya 6.500).
> Sabtu 26/09: tunai 980rb, QRIS 260rb, beli ayam 410rb. Terus aku hitung laci: 100rb x10, 50rb x2, 20rb x4, 10rb x3, 5rb x2, 2rb x5, koin 3.500."

## Perintah yang dijalankan (ringkas)
```
kas.py init --nama-usaha "Warung Makan Bu Tini" --kas-awal 500rb --mulai 21/09/2026           (pratinjau -> --ya)
kas.py akun tambah --nama BRI --jenis bank --saldo-awal 3jt --tanggal-awal 21/09/2026 --terima-qris --ya
kas.py akun tambah --nama GoPay --jenis e-wallet --saldo-awal 150rb --tanggal-awal 21/09/2026 --ya
kas.py catat --tanggal 24/09/2026 --baris "masuk;1,2jt;penjualan;tunai;jualan" --baris "masuk;350rb;penjualan;qris" \
   --baris "keluar;85rb;beli-stok;;beli es batu dan gas" --baris "keluar;100rb;;;jajan anak" --baris "keluar;200rb;listrik-air;transfer;token PLN"
kas.py catat --tanggal 25/09/2026 ... ; kas.py pindah --dari laci --ke BRI --jumlah 1jt --biaya 6500 --tanggal 25/09/2026
kas.py catat --tanggal 26/09/2026 ... ; kas.py opname --tanggal 26/09/2026 --pecahan "..." [--sesuaikan]
kas.py rekap --tanggal 26/09/2026 ; kas.py rekap --dari 21/09/2026 --sampai 26/09/2026 ; kas.py saldo
```
Catatan: pada percobaan pertama, "beli es batu dan gas" **tanpa kategori** ditolak script (`perlu_kategori`) — perilaku benar (tidak menebak diam-diam). Dicatat ulang dengan `beli-stok` seolah pengguna menjawab.

## Output script (kutipan asli)
Pratinjau 24/09:
```
1. MASUK  Rp 1.200.000 | 24/09/2026 | Penjualan | Tunai -> Laci kas | jualan
2. MASUK  Rp 350.000 | 24/09/2026 | Penjualan | QRIS -> BRI
3. KELUAR Rp 85.000 | 24/09/2026 | Beli stok/bahan | Tunai -> Laci kas | beli es batu dan gas
4. KELUAR Rp 100.000 | 24/09/2026 | Prive (ambil pribadi) | Tunai -> Laci kas | jajan anak
5. KELUAR Rp 200.000 | 24/09/2026 | Listrik/air | Transfer -> BRI | token PLN
Asumsi: baris 3: dibayar/diterima tunai (metode tidak disebut); baris 4: kategori 'prive' ditebak dari kata 'jajan'; ...
Saldo setelah dicatat: Laci kas Rp 1.515.000, BRI Rp 3.150.000
```
Pindah dana: `Pindah dana Laci kas -> BRI Rp 1.000.000 pada 25/09/2026 (tidak mengubah hasil usaha). Biaya admin Rp 6.500 dicatat sebagai pengeluaran lain-lain dari Laci kas.`

Opname (pratinjau): `Menurut buku : Rp 1.578.500 / Uang dihitung: Rp 1.233.500 / Hasil: SELISIH KURANG Rp 345.000 (ditandai).` + daftar kemungkinan penyebab "jangan menuduh siapa pun".
Setelah `--sesuaikan --ya`: dicatat keluar Rp 345.000 "Selisih laci kurang", rekap harian 26/09 hasil usaha turun dari Rp 830.000 ke Rp 485.000; riwayat `opname --daftar` menyimpan "(disesuaikan)".

Rekap 21–26/09 (sebelum penyesuaian):
```
UANG MASUK: Rp 4.735.000  - Penjualan
UANG KELUAR: Rp 1.751.500 - Beli stok 1.145.000; Gaji 300.000; Listrik/air 200.000; Prive 100.000; Lain-lain 6.500
HASIL USAHA: Rp 3.083.500 ; Prive = 3,2% dari hasil usaha
Per hari: 24/09 1.265.000 | 25/09 988.500 | 26/09 830.000
SALDO: Laci Rp 1.578.500 | BRI Rp 4.830.000 | GoPay Rp 225.000 | Total Rp 6.633.500 (awal Rp 3.650.000, naik Rp 2.983.500)
```
Uji tambahan: bila pindah dana dicatat saat laci belum berisi (urutan salah), pratinjau menandai `saldo Laci kas jadi MINUS -Rp 506.500` sebagai `perlu_izin` dan `--ya` **ditolak** tanpa `--izinkan-minus`. Benar.

## Verifikasi angka independen (Decimal, dihitung dari input, tanpa membaca kode)
| Pos | Hitungan penguji | Script | Cocok |
|---|---|---|---|
| Laci akhir | 500.000 +1.200.000 −85.000 −100.000 +1.450.000 −650.000 −300.000 −1.000.000 −6.500 +980.000 −410.000 = 1.578.500 | 1.578.500 | ya |
| BRI akhir | 3.000.000 +350.000 −200.000 +420.000 +1.000.000 +260.000 = 4.830.000 | 4.830.000 | ya |
| GoPay | 150.000 +75.000 = 225.000 | 225.000 | ya |
| Hasil usaha 25/09 | 1.945.000 − (650.000+300.000+6.500) = 988.500 (pindah dana 1jt tidak ikut) | 988.500 | ya |
| Hasil usaha periode | 4.735.000 − 1.651.500 = 3.083.500; prive 100.000/3.083.500 = 3,24% | 3.083.500 / 3,2% | ya |
| Kenaikan total saldo | 3.083.500 − 100.000 prive = 2.983.500 | 2.983.500 | ya |
| Opname | 1.000.000+100.000+80.000+30.000+10.000+10.000+3.500 = 1.233.500; selisih 345.000 kurang | sama | ya |
| Pindah dana | laci −1.000.000, BRI +1.000.000 → total saldo tetap, hasil usaha tidak berubah (hanya biaya 6.500) | sama | ya |

## Penilaian
- Pratinjau → `--ya` konsisten; asumsi (metode tunai, prive ditebak dari "jajan") disebut.
- QRIS otomatis ke akun penampung, e-wallet ke GoPay; saldo per akun benar.
- Selisih laci disampaikan netral, penyesuaian hanya dengan `--sesuaikan`.
- Kekurangan kecil: rekap harian 26/09 menyarankan "uang laci belum dihitung" karena opname baru pratinjau — benar secara data, tapi agent perlu menjelaskan.

**Hasil: LULUS (9/10).**
