# 09 — Kafe dengan PB1 dipungut terpisah & disetor bulan berikutnya (data baru, v1.2.0)

## Skenario
Skenario normal dengan data baru untuk kategori `titipan_pajak` (baru di v1.2.0). Kafe mencatat PB1 10% yang dipungut dari pembeli sebagai baris terpisah dan menyetornya ke Bapenda tanggal 10 bulan berikutnya, pola yang umum untuk PBJT. Per 1 Juli masih ada PB1 Juni Rp 1.500.000 yang belum disetor.

## Input pengguna
> tolong bikin laporan keuangan kafe aku (Kafe Senja Fiktif) bulan Juli sama Agustus, per bulan. PB1 aku pungut 10% dari pembeli, dicatat terpisah, disetor tiap tgl 10 bulan berikutnya. Per 1 Juli PB1 bulan Juni 1,5 juta belum disetor (disetor 10 Juli). Stok bahan anggap habis tiap akhir bulan. File: kafe-pb1.csv

```csv
Tanggal,Keterangan,Masuk,Keluar
01/07/2026,Saldo awal,"Rp 5.000.000",
05/07/2026,Penjualan minggu 1 (belum termasuk PB1),"Rp 5.000.000",
05/07/2026,PB1 10% dipungut dari pembeli minggu 1,"Rp 500.000",
06/07/2026,Belanja bahan kopi & susu,,"Rp 2.500.000"
10/07/2026,Setor PB1 Juni ke Bapenda,,"Rp 1.500.000"
12/07/2026,Penjualan minggu 2 (belum termasuk PB1),"Rp 6.000.000",
12/07/2026,PB1 10% dipungut dari pembeli minggu 2,"Rp 600.000",
19/07/2026,Penjualan minggu 3 (belum termasuk PB1),"Rp 4.000.000",
19/07/2026,PB1 10% dipungut dari pembeli minggu 3,"Rp 400.000",
25/07/2026,Gaji barista,,"Rp 4.000.000"
28/07/2026,Sewa tempat,,"Rp 3.000.000"
02/08/2026,Penjualan minggu 1 (belum termasuk PB1),"Rp 7.000.000",
02/08/2026,PB1 10% dipungut dari pembeli minggu 1,"Rp 700.000",
05/08/2026,Belanja bahan kopi & susu,,"Rp 3.000.000"
10/08/2026,Setor PB1 Juli ke Bapenda,,"Rp 1.500.000"
16/08/2026,Penjualan minggu 2 (belum termasuk PB1),"Rp 5.000.000",
16/08/2026,PB1 10% dipungut dari pembeli minggu 2,"Rp 500.000",
25/08/2026,Gaji barista,,"Rp 4.000.000"
28/08/2026,Sewa tempat,,"Rp 3.000.000"
```

## Output

### Langkah agent
1. Run pertama: status SEMENTARA dengan **12 pertanyaan PB1**, satu per baris yang memuat kata "PB1", termasuk baris penjualan "(belum termasuk PB1)". Baris "PB1 10% dipungut dari pembeli" otomatis terbaca sebagai **penjualan** (kata `pembeli`) sampai ditetapkan. Agent merangkum semuanya menjadi satu konfirmasi. Karena pengguna sudah menjelaskan polanya, agent langsung menetapkan:
   `--tetapkan 4=titipan_pajak --tetapkan 8=titipan_pajak --tetapkan 10=titipan_pajak --tetapkan 14=titipan_pajak --tetapkan 18=titipan_pajak --tetapkan 6=titipan_pajak --tetapkan 16=titipan_pajak --tetapkan 3=pendapatan_usaha --tetapkan 7=pendapatan_usaha --tetapkan 9=pendapatan_usaha --tetapkan 13=pendapatan_usaha --tetapkan 17=pendapatan_usaha`
2. Laporan Juli:

# Laporan Keuangan Kafe Senja Fiktif
Periode 1 Juli 2026 s.d. 31 Juli 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP (dengan asumsi)**

## Ringkasan untuk pemilik
Usaha kamu UNTUNG Rp 5.500.000 selama 1 Juli 2026 s.d. 31 Juli 2026. Dari penjualan bersih Rp 15.000.000, yang tersisa jadi laba sekitar 36,7% (setiap Rp 100.000 penjualan, labanya sekitar Rp 36.667). Pengeluaran terbesar: beban gaji & upah sebesar Rp 4.000.000 (42,1% dari total biaya). Uang kas di akhir periode: Rp 10.500.000.

## 1. Laporan Laba Rugi
Kafe Senja Fiktif — untuk periode 1 Juli 2026 s.d. 31 Juli 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan / pendapatan usaha | Rp 15.000.000 |
| **Pendapatan usaha bersih** | **Rp 15.000.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 0 |
| Pembelian bahan/barang dagangan | Rp 2.500.000 |
| Persediaan akhir | Rp 0 |
| Beban pokok penjualan | (Rp 2.500.000) |
| **Laba kotor** | **Rp 12.500.000** |
| **Beban usaha** |  |
| Beban gaji & upah | Rp 4.000.000 |
| Beban sewa tempat | Rp 3.000.000 |
| Total beban usaha | (Rp 7.000.000) |
| **Laba (rugi) usaha** | **Rp 5.500.000** |
| **Laba (rugi) sebelum pajak** | **Rp 5.500.000** |
| Beban pajak penghasilan | Rp 0 |
| **LABA (RUGI) BERSIH** | **Rp 5.500.000** |

## 2. Laporan Posisi Keuangan (Neraca)
Kafe Senja Fiktif — per 31 Juli 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas dan setara kas | Rp 10.500.000 |
| Piutang usaha | Rp 0 |
| Persediaan | Rp 0 |
| Aset tetap (nilai buku) | Rp 0 |
| **Total aset** | **Rp 10.500.000** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 0 |
| Utang bank / pinjaman | Rp 0 |
| Total liabilitas | Rp 0 |
| **EKUITAS** |  |
| Modal awal | Rp 5.000.000 |
| Laba (rugi) bersih periode ini | Rp 5.500.000 |
| Prive (pengambilan pribadi) | Rp 0 |
| Modal akhir | Rp 10.500.000 |
| **Total liabilitas + ekuitas** | **Rp 10.500.000** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 10.500.000). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Kafe Senja Fiktif adalah usaha yang laporan keuangannya disusun untuk periode 1 Juli 2026 s.d. 31 Juli 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 10.500.000 (saldo awal Rp 5.000.000, total uang masuk Rp 16.500.000, total uang keluar Rp 11.000.000).

**4. Piutang usaha** Rp 0 (awal Rp 0). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 0 (awal Rp 0). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 2.500.000.

**6. Aset tetap** nilai buku Rp 0 (awal Rp 0, pembelian periode ini Rp 0, penyusutan periode ini Rp 0). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 0 dan utang bank/pinjaman Rp 0 (pinjaman diterima Rp 0, pembayaran pokok Rp 0).

**8. Ekuitas.** Modal awal Rp 5.000.000 + tambahan modal Rp 0 + laba bersih Rp 5.500.000 - prive Rp 0 = modal akhir Rp 10.500.000.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 15.000.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 7.000.000, beban keuangan Rp 0, beban pajak penghasilan Rp 0. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Perlu dicek
**Baris yang sengaja dilewati:** baris saldo awal (dipakai sebagai kas awal bila --kas-awal tidak diisi) (1 baris)

**Peringatan:**
- 8 transaksi setelah 31 Juli 2026 tidak dihitung.

## Asumsi yang dipakai
- Kas awal diambil dari baris 'saldo awal' di file: Rp 5.000.000.
- Saldo awal piutang tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal aset tetap tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal utang ke pemasok tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal utang bank/pinjaman tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal (kas, piutang, stok, utang, aset) harus per 1 Juli 2026.
- Modal awal dihitung dari (aset awal - utang awal) = Rp 5.000.000.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

### Catatan agent untuk pemilik (wajib ditambahkan)
> ⚠ Utang PB1 di neraca tertulis Rp 0, padahal per 31 Juli masih ada PB1 Juli Rp 1.500.000 yang baru disetor 10 Agustus. Script belum punya isian untuk PB1 Juni yang belum disetor per 1 Juli (Rp 1.500.000), sehingga setoran 10 Juli dianggap melunasi PB1 Juli. Laba Rp 5.500.000 sudah benar, tetapi di neraca utang kurang Rp 1.500.000 dan modal lebih Rp 1.500.000.

Laporan Agustus: status **SEMENTARA** dan ⚠, karena "utang pajak daerah (titipan) −Rp 300.000" dan saran script "catat penyetorannya sebagai beban_pajak_lain". Saran itu **salah** untuk kasus ini. Kalau diikuti, laba Agustus turun Rp 1.500.000 padahal PB1 dipungut dari pembeli.

## Catatan penguji
- **Verifikasi independen:** Juli pendapatan 15.000.000 (tanpa PB1), bahan 2.500.000, gaji 4.000.000, sewa 3.000.000 → laba **5.500.000 ✔**; kas 5.000.000 + 16.500.000 − 11.000.000 = **10.500.000 ✔**. Agustus laba 12.000.000 − 3.000.000 − 7.000.000 = **2.000.000 ✔**. PB1 tidak masuk pendapatan maupun beban ✔ (inti `titipan_pajak` bekerja).
- **Utang PB1 yang benar:** 31 Juli = 1.500.000 + 1.500.000 − 1.500.000 = **Rp 1.500.000** (script: Rp 0, berlabel LENGKAP). 31 Agustus = 1.500.000 + 1.200.000 − 1.500.000 = **Rp 1.200.000** (script: −Rp 300.000, SEMENTARA). Modal awal Juli yang benar Rp 3.500.000 (script Rp 5.000.000).
- **Cacat sedang:** tidak ada opsi saldo awal titipan (mis. `--titipan-pajak-awal`), dan SKILL.md tidak menanyakannya. Padahal PB1 hampir selalu disetor bulan berikutnya, jadi setiap kafe/rumah makan yang memakai `titipan_pajak` terkena di laporan pertamanya. Laba tetap benar, tetapi pembagian utang/modal di neraca salah tanpa peringatan (Juli). Saran perbaikan otomatis untuk titipan negatif juga menyesatkan. *Saran:* tambah `--titipan-pajak-awal` (digulir seperti kasbon) + masukkan ke daftar pertanyaan bila ada baris `titipan_pajak` keluar di bulan pertama. Ubah teks saran anomali menjadi "Apakah ada PB1 bulan lalu yang belum disetor per <awal periode>? Isi --titipan-pajak-awal".
- **Ringan:** pertanyaan PB1 muncul per baris (12 pertanyaan untuk 18 transaksi), termasuk baris penjualan yang hanya menyebut "belum termasuk PB1". Kelompokkan menjadi satu pertanyaan dengan daftar nomor baris, dan jangan memicu pertanyaan pada baris masuk yang sudah terbaca sebagai penjualan dengan frasa "belum/tidak termasuk PB1".
