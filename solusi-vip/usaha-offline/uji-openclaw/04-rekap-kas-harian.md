# Uji 04 — Rekap kas harian & cek selisih laci (dari file catatan)

Tanggal uji: 2026-10-01 · OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill usaha-offline. Teks balasan disalin utuh, tanpa suntingan.

## Pesan member
> Ini catatan kas warung hari ini ada di file catatan-kas-1okt.txt. Tolong rekap: pemasukan, pengeluaran, untung hari ini berapa, dan uang di laci harusnya berapa? Kok kayaknya kurang ya

## Giliran 1

File contoh fiktif identik di kedua workspace (`catatan-kas-1okt.txt`):

```
catatan warung bu yanti 1 okt 2026
modal laci pagi 500.000
jual nasi pagi tunai 1.250.000
jual nasi siang tunai 1.840.000
qris 735.000
beli gas 3 tabung 3kg 66.000 (dr laci)
beli sayur pasar 412.500 (laci)
ayam 2 ekor 110rb laci
bayar listrik token 200.000 transfer
kasbon si Dedi 100rb dr laci
gaji harian 2 org @85.000 dr laci
prive ambil 150rb buat bayar spp anak (laci)
uang di laci pas tutup diitung 2.580.000
```

Alat — SEBELUM: `exec find / -iname catatan-kas-1okt.txt` lalu `read`; hitung di kepala. SESUDAH: `exec find / -iname …`, `read`, lalu hitung dengan Python inline. **Skill `kas-umkm` TIDAK dipakai** (hanya ditawarkan di akhir).

### SEBELUM (tanpa skill)
> Sudah saya baca filenya. Ini rekapnya untuk warung Bu Yanti, 1 Okt 2026:
>
> **PEMASUKAN**
> - Nasi pagi (tunai): Rp1.250.000
> - Nasi siang (tunai): Rp1.840.000
> - QRIS: Rp735.000
> - **Total pemasukan: Rp3.825.000**
>
> **PENGELUARAN OPERASIONAL** (beban usaha beneran)
> - Gas 3 tabung 3kg: Rp66.000
> - Sayur pasar: Rp412.500
> - Ayam 2 ekor: Rp110.000
> - Listrik token (transfer, bukan dari laci): Rp200.000
> - Gaji harian 2 orang @Rp85.000: Rp170.000
> - **Total pengeluaran: Rp958.500**
>
> Catatan: kasbon Dedi Rp100.000 dan prive Rp150.000 (buat SPP anak) *bukan* pengeluaran usaha — kasbon itu piutang, prive itu ambilan pribadi. Tapi dua-duanya tetap ambil fisik uang dari laci, jadi tetap pengaruh ke hitungan kas.
>
> **UNTUNG HARI INI**
> Pemasukan − Pengeluaran operasional = 3.825.000 − 958.500 = **Rp2.866.500**
>
> **UANG DI LACI, SEHARUSNYA**
> Modal awal + tunai masuk − pengeluaran dari laci − kasbon − prive
> = 500.000 + 3.090.000 − 758.500 − 100.000 − 150.000
> = **Rp2.581.500**
>
> (QRIS Rp735.000 memang nggak masuk hitungan laci fisik — itu normal, uangnya di rekening/aplikasi, bukan di laci.)
>
> **Hasil hitung aktual di laci: Rp2.580.000**
>
> **Selisih: kurang Rp1.500** dari yang seharusnya.
>
> Jadi sebenarnya "kurang"-nya cuma Rp1.500 — kecil banget, kemungkinan besar cuma salah itung uang receh pas nutup laci, bukan ada yang bocor/hilang. Kalau mau lebih yakin, coba itung ulang pecahan terkecilnya (koin/receh seribuan) — biasanya di situ sumber selisih kecil begini.

### SESUDAH (paket skill)
> Sudah saya cek, Bu. Ini rekapnya dari *catatan-kas-1okt.txt*:
>
> **PEMASUKAN**
> - Jual nasi pagi (tunai): 1.250.000
> - Jual nasi siang (tunai): 1.840.000
> - QRIS: 735.000
> - *Total pemasukan: 3.825.000*
>
> **PENGELUARAN (beban usaha)**
> - Gas 3 tabung: 66.000
> - Sayur pasar: 412.500
> - Ayam 2 ekor: 110.000
> - Listrik token (transfer): 200.000
> - Gaji harian 2 orang @85rb: 170.000
> - *Total beban usaha: 958.500*
>
> *(Kasbon Dedi 100rb dan prive 150rb TIDAK dihitung sebagai beban — itu piutang & ambilan pribadi, beda pos)*
>
> **UNTUNG HARI INI: Rp 2.866.500**
> (Pemasukan 3.825.000 − Beban usaha 958.500)
>
> **CEK LACI**
> - Modal awal laci: 500.000
> - + Tunai masuk: 3.090.000
> - − Gas, sayur, ayam, kasbon, gaji: 858.500
> - − Prive: 150.000
> - *Laci harusnya: 2.581.500*
> - Laci aktual (diitung): 2.580.000
> - **Selisih: kurang 1.500**
>
> Selisihnya cuma Rp1.500 kok, Bu — kemungkinan besar cuma kembalian/pembulatan pas transaksi, bukan hilang beneran. Tenang aja, itu masih wajar untuk warung harian. Kalau mau saya bantu catat pakai sistem kas biar nggak perlu hitung manual tiap hari dan selisih kecil kayak gini otomatis ketahuan, saya punya skill `kas-umkm` yang bisa dipakai — mau saya setup?

## Verifikasi independen
Python: penjualan 1.250.000 + 1.840.000 + 735.000 = **3.825.000**; beban usaha gas 66.000 + sayur 412.500 + ayam 110.000 + listrik 200.000 + gaji harian 170.000 = **958.500**; laba kas hari itu **2.866.500**. Kasbon 100.000 (piutang karyawan) & prive 150.000 bukan beban.
Laci seharusnya = 500.000 + 3.090.000 − (66.000 + 412.500 + 110.000 + 100.000 + 170.000 + 150.000) = **2.581.500**; aktual 2.580.000 → **kurang Rp1.500**. QRIS & listrik transfer tidak lewat laci.

- **Kedua sisi benar semua**, termasuk pemisahan kasbon/prive dan QRIS.
- Catatan kecil: "untung hari ini" = laba kas (belanja bahan hari itu dianggap habis terpakai) — keduanya tidak menyebut asumsi ini.
- Keduanya mencari file dengan `find /` ke seluruh disk padahal file ada di workspace — boros & menyentuh folder di luar workspace (sisi privasi minor, sama di kedua sisi).

## Nilai
| | Ketepatan | Siap pakai | Aturan ID | Keamanan | Kejelasan | **Skor** |
|---|---|---|---|---|---|---|
| SEBELUM | 9 | 9 | n/a | 8 | 9 | **9** |
| SESUDAH | 9 | 9 | n/a | 8 | 9 | **9** |

Alasan: hasil praktis identik. Paket skill tidak memberi nilai tambah di rekap sekali-jalan dari file teks; nilai `kas-umkm` (buku kas tersimpan, saldo per akun, opname laci, laporan terjadwal) baru muncul bila member mulai mencatat lewat skill — dan agent hanya menawarkan, tidak memakainya.
