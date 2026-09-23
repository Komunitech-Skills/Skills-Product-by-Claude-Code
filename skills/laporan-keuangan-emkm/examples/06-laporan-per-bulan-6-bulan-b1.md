# 06 — Laporan per bulan dari buku kas 6 bulan (uji B1/BB1, diuji ulang dengan v1.2.0)

## Skenario
Uji laporan satu bulan dari buku kas multi-bulan (cacat B1 di v1.0.0 dan BB1 di v1.1.0). Dua data:
1. **Data lama** `kas-dapur-sehati.csv` (Jan–Mar): laporan **Februari** saja. Target: kas akhir Rp 22.408.250.
2. **Data baru** `konveksi-6bln.csv` (Jan–Jun 2026, 63 transaksi, fiktif): KUR cair Februari + 4 angsuran dengan bunga, 2 pembelian mesin, setor/tarik tunai bank, kasbon (Mar, lunas Mei), setoran modal (Apr), prive bulanan, **penjualan tempo Maret Rp 1,2 jt dilunasi April**, dan **bon kain Mei Rp 800 rb dibayar Juni**. Enam laporan bulanan dibuat satu per satu, lalu tiap bulan dicek independen dengan `verif_6bln.py` (ledger akrual bulanan buatan penguji, tanpa kode skill).

## Input pengguna
> Mas, bikinin laporan keuangan per bulan Januari sampai Juni ya, buat tiap bulan satu. Filenya konveksi-6bln.csv, nama usaha Konveksi Rapi Fiktif. Per 1 Januari: stok kain 1,5 juta, piutang CV Contoh 2 juta (lunas Januari), utang ke supplier kain 1,5 juta (lunas Januari), mesin-mesin lama nilainya 10 juta, umurnya 5 tahun. KUR belum ada sebelum Februari. Stok akhir tiap bulan: Jan 1,8jt, Feb 3jt, Mar 2,5jt, Apr 2,2jt, Mei 3,1jt, Jun 2jt. Jaket himpunan bulan Maret masih kurang bayar 1,2 juta (dibayar April). Kain Mei ada yang ngebon 800rb, dibayar Juni. Bunga KUR dari jadwal BRI: angsuran 1 150rb, 2 145rb, 3 140rb, 4 135rb.

Isi `konveksi-6bln.csv`:
```csv
Tanggal,Keterangan,Masuk,Keluar
01/01/2026,Saldo awal,"Rp 6.000.000",
03/01/2026,Beli kain katun 3 roll,,"Rp 2.400.000"
05/01/2026,Penjualan kaos seragam SD Fiktif,"Rp 4.500.000",
08/01/2026,Terima pelunasan piutang CV Contoh (Desember),"Rp 2.000.000",
10/01/2026,Bayar tempo supplier kain Desember,,"Rp 1.500.000"
12/01/2026,Beli mesin jahit portable,,"Rp 3.000.000"
15/01/2026,Upah penjahit borongan,,"Rp 1.800.000"
20/01/2026,Penjualan kaos komunitas,"Rp 3.200.000",
25/01/2026,Bayar listrik,,"Rp 350.000"
28/01/2026,Sewa ruko Januari,,"Rp 1.000.000"
30/01/2026,Ambil untuk keperluan rumah,,"Rp 800.000"
02/02/2026,Pencairan KUR BRI,"Rp 20.000.000",
04/02/2026,Beli benang & kancing,,"Rp 600.000"
06/02/2026,Setor tunai ke bank,,"Rp 5.000.000"
10/02/2026,Penjualan seragam kantor,"Rp 6.000.000",
14/02/2026,"Setor PPh final 0,5% Januari",,"Rp 38.500"
15/02/2026,Upah penjahit borongan,,"Rp 2.100.000"
20/02/2026,Beli kain drill 4 roll,,"Rp 3.600.000"
25/02/2026,Bayar listrik,,"Rp 380.000"
27/02/2026,Sewa ruko Februari,,"Rp 1.000.000"
28/02/2026,Ambil uang pribadi,,"Rp 1.000.000"
02/03/2026,Angsuran KUR BRI ke-1,,"Rp 1.850.000"
05/03/2026,Penjualan jaket himpunan (DP & sebagian),"Rp 7.500.000",
08/03/2026,Kasbon Mas Joko,,"Rp 500.000"
10/03/2026,"Setor PPh final 0,5% Februari",,"Rp 30.000"
12/03/2026,Beli kain fleece,,"Rp 4.200.000"
15/03/2026,Upah penjahit borongan,,"Rp 2.400.000"
18/03/2026,Ongkir kirim jaket,,"Rp 250.000"
25/03/2026,Bayar listrik,,"Rp 400.000"
27/03/2026,Sewa ruko Maret,,"Rp 1.000.000"
30/03/2026,Tarik tunai dari bank,"Rp 2.000.000",
02/04/2026,Angsuran KUR BRI ke-2,,"Rp 1.850.000"
04/04/2026,Setoran modal dari tabungan pribadi,"Rp 3.000.000",
06/04/2026,Beli mesin obras,,"Rp 4.500.000"
08/04/2026,Penjualan kaos event lari,"Rp 5.800.000",
09/04/2026,Terima piutang jaket himpunan,"Rp 1.200.000",
10/04/2026,"Setor PPh final 0,5% Maret",,"Rp 43.500"
12/04/2026,Beli kain & rib,,"Rp 3.100.000"
15/04/2026,Upah penjahit borongan,,"Rp 2.000.000"
20/04/2026,Iklan Instagram,,"Rp 300.000"
27/04/2026,Sewa ruko April,,"Rp 1.000.000"
28/04/2026,Bayar listrik,,"Rp 390.000"
30/04/2026,Ambil uang pribadi,,"Rp 1.200.000"
02/05/2026,Angsuran KUR BRI ke-3,,"Rp 1.850.000"
05/05/2026,Penjualan seragam sekolah,"Rp 9.000.000",
07/05/2026,Mas Joko lunasi kasbon,"Rp 500.000",
10/05/2026,"Setor PPh final 0,5% April",,"Rp 29.000"
12/05/2026,Beli kain katun 5 roll,,"Rp 4.000.000"
15/05/2026,Upah penjahit borongan,,"Rp 2.700.000"
20/05/2026,Servis mesin jahit,,"Rp 150.000"
27/05/2026,Sewa ruko Mei,,"Rp 1.000.000"
28/05/2026,Bayar listrik,,"Rp 410.000"
31/05/2026,Biaya admin bank,,"Rp 15.000"
02/06/2026,Angsuran KUR BRI ke-4,,"Rp 1.850.000"
03/06/2026,Bayar bon supplier kain Mei,,"Rp 800.000"
05/06/2026,Penjualan kaos reuni,"Rp 6.500.000",
10/06/2026,"Setor PPh final 0,5% Mei",,"Rp 45.000"
12/06/2026,Beli kain,,"Rp 2.800.000"
15/06/2026,Upah penjahit borongan,,"Rp 2.300.000"
20/06/2026,Ongkir kirim paket,,"Rp 180.000"
25/06/2026,Bayar listrik,,"Rp 400.000"
27/06/2026,Sewa ruko Juni,,"Rp 1.000.000"
30/06/2026,Ambil uang pribadi,,"Rp 1.500.000"
30/06/2026,Biaya admin bank,,"Rp 15.000"
```

## Output

### Langkah agent
Untuk tiap bulan N ≥ 2, script pertama kali dijalankan dengan saldo per 1 Januari. Script lalu **menanyakan sendiri** piutang dan utang pemasok per awal bulan. Contoh untuk April (status SEMENTARA):

> 1. Berapa piutang pelanggan (penjualan tempo yang belum dibayar) per 1 April 2026? Jawab lalu jalankan ulang dengan --piutang-awal-periode <nominal> (0 bila tidak ada).
> 2. Berapa utang ke pemasok (bon/tempo yang belum dibayar) per 1 April 2026? Jawab lalu jalankan ulang dengan --utang-usaha-awal-periode <nominal> (0 bila tidak ada).

Jawabannya sudah ada di pesan pengguna (jaket himpunan Rp 1,2 jt belum dibayar per akhir Maret; tidak ada bon pemasok). Agent tidak perlu bertanya lagi dan langsung menjalankan:
```bash
python3 scripts/laporan_emkm.py konveksi-6bln.csv --nama-usaha "Konveksi Rapi Fiktif" \
  --periode-awal 2026-04-01 --periode-akhir 2026-04-30 --umur-aset-tahun 5 \
  --persediaan-awal 2.500.000 --persediaan-akhir 2.200.000 \
  --piutang-awal 2jt --utang-usaha-awal 1,5jt --aset-tetap-awal 10jt --utang-bank-awal 0 \
  --piutang-awal-periode 1,2jt --utang-usaha-awal-periode 0 --piutang-akhir 0 --utang-usaha-akhir 0 \
  --bunga 23=150.000 --bunga 33=145.000 --bunga 45=140.000 --bunga 55=135.000
```

### Contoh hasil: laporan April 2026 (output script v1.2.0)

# Laporan Keuangan Konveksi Rapi Fiktif
Periode 1 April 2026 s.d. 30 April 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP**

## Ringkasan untuk pemilik
Usaha kamu RUGI Rp 1.695.167 selama 1 April 2026 s.d. 30 April 2026. Dari penjualan bersih Rp 5.800.000, setiap Rp 100.000 penjualan usaha rugi sekitar Rp 29.227. Pengeluaran terbesar: pembelian bahan/barang dagangan sebesar Rp 3.100.000 (43,1% dari total biaya). Kamu mengambil Rp 1.200.000 untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi mengurangi modal usaha. Uang kas di akhir periode: Rp 14.618.000.

## 1. Laporan Laba Rugi
Konveksi Rapi Fiktif — untuk periode 1 April 2026 s.d. 30 April 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan / pendapatan usaha | Rp 5.800.000 |
| **Pendapatan usaha bersih** | **Rp 5.800.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 2.500.000 |
| Pembelian bahan/barang dagangan | Rp 3.100.000 |
| Persediaan akhir | (Rp 2.200.000) |
| Beban pokok penjualan | (Rp 3.400.000) |
| **Laba kotor** | **Rp 2.400.000** |
| **Beban usaha** |  |
| Beban gaji & upah | Rp 2.000.000 |
| Beban sewa tempat | Rp 1.000.000 |
| Beban listrik, air, gas & internet | Rp 390.000 |
| Beban iklan & promosi | Rp 300.000 |
| Beban penyusutan aset tetap | Rp 216.667 |
| Total beban usaha | (Rp 3.906.667) |
| **Laba (rugi) usaha** | **-Rp 1.506.667** |
| Beban bunga & biaya bank (beban keuangan) | (Rp 145.000) |
| **Laba (rugi) sebelum pajak** | **-Rp 1.651.667** |
| Beban pajak penghasilan | (Rp 43.500) |
| **LABA (RUGI) BERSIH** | **-Rp 1.695.167** |

## 2. Laporan Posisi Keuangan (Neraca)
Konveksi Rapi Fiktif — per 30 April 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas menurut buku | Rp 11.618.000 |
| Dana dipindah ke kas/rekening lain | Rp 3.000.000 |
| Kas dan setara kas | Rp 14.618.000 |
| Piutang usaha | Rp 0 |
| Kasbon karyawan & piutang lain-lain | Rp 500.000 |
| Persediaan | Rp 2.200.000 |
| Aset tetap (awal + pembelian Rp 4.500.000) | Rp 16.899.999 |
| Penyusutan periode ini | (Rp 216.667) |
| Aset tetap (nilai buku) | Rp 16.683.332 |
| **Total aset** | **Rp 34.001.332** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 0 |
| Utang bank / pinjaman | Rp 16.595.000 |
| Total liabilitas | Rp 16.595.000 |
| **EKUITAS** |  |
| Modal awal | Rp 17.301.499 |
| Tambahan modal | Rp 3.000.000 |
| Laba (rugi) bersih periode ini | -Rp 1.695.167 |
| Prive (pengambilan pribadi) | (Rp 1.200.000) |
| Modal akhir | Rp 17.406.332 |
| **Total liabilitas + ekuitas** | **Rp 34.001.332** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 34.001.332). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Konveksi Rapi Fiktif adalah usaha yang laporan keuangannya disusun untuk periode 1 April 2026 s.d. 30 April 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 14.618.000 (saldo awal Rp 19.001.500, total uang masuk Rp 10.000.000, total uang keluar Rp 14.383.500).

**4. Piutang usaha** Rp 0 (awal Rp 1.200.000). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 2.200.000 (awal Rp 2.500.000). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 3.400.000.

**6. Aset tetap** nilai buku Rp 16.683.332 (awal Rp 12.399.999, pembelian periode ini Rp 4.500.000, penyusutan periode ini Rp 216.667). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 0 dan utang bank/pinjaman Rp 16.595.000 (pinjaman diterima Rp 0, pembayaran pokok Rp 1.705.000).

**8. Ekuitas.** Modal awal Rp 17.301.499 + tambahan modal Rp 3.000.000 + laba bersih -Rp 1.695.167 - prive Rp 1.200.000 = modal akhir Rp 17.406.332.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 5.800.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 3.906.667, beban keuangan Rp 145.000, beban pajak penghasilan Rp 43.500. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Perlu dicek
**Baris yang sengaja dilewati:** baris saldo awal (dipakai sebagai kas awal bila --kas-awal tidak diisi) (1 baris)

**Peringatan:**
- 23 transaksi setelah 30 April 2026 tidak dihitung.

## Asumsi yang dipakai
- Kas awal diambil dari baris 'saldo awal' di file: Rp 6.000.000.
- Saldo awal yang Anda berikan/dibaca dari file dianggap per awal data (1 Januari 2026), lalu digulirkan dengan 31 transaksi sebelum 1 April 2026. Kas awal periode = Rp 19.001.500; modal awal periode sudah termasuk laba/prive sebelum periode. Stok awal (--persediaan-awal) dipakai sebagai stok per 1 April 2026.
- Penyusutan sebelum periode (Rp 600.001) sudah dikurangkan dari aset tetap awal.
- Penyusutan garis lurus, umur manfaat 5 tahun, tanpa nilai sisa; aset yang dibeli mulai disusutkan bulan berikutnya; dihitung per bulan dari harga perolehan (dibulatkan ke rupiah per bulan). Nilai aset tetap awal yang Anda berikan diperlakukan sebagai harga perolehan per awal data.
- Modal awal dihitung dari (aset awal - utang awal) = Rp 17.301.499.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

### Rekap uji 6 laporan bulanan vs verifikasi independen
| Bulan | Kas & setara kas | Piutang | Kasbon | Aset tetap | Utang pemasok | Utang KUR | Modal awal | Laba | Modal akhir | 11 pos vs penguji | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Jan | 4.850.000 | 0 | 0 | 12.833.333 | 0 | 0 | 18.000.000 | **2.283.333** | 19.483.333 | semua cocok ✔ | LENGKAP, ✔ seimbang |
| Feb | 22.131.500 | 0 | 0 | 12.616.666 | 0 | 20.000.000 | 19.483.333 (= modal akhir bln lalu ✔) | **−735.167** | 17.748.166 | semua cocok ✔ | LENGKAP, ✔ seimbang |
| Mar | 19.001.500 | 1.200.000 | 500.000 | 12.399.999 | 0 | 18.300.000 | 17.748.166 (= modal akhir bln lalu ✔) | **−446.667** | 17.301.499 | semua cocok ✔ | LENGKAP, ✔ seimbang |
| Apr | 14.618.000 | 0 | 500.000 | 16.683.332 | 0 | 16.595.000 | 17.301.499 (= modal akhir bln lalu ✔) | **−1.695.167** | 17.406.332 | semua cocok ✔ | LENGKAP, ✔ seimbang |
| Mei | 13.964.000 | 0 | 0 | 16.391.665 | 800.000 | 14.885.000 | 17.406.332 (= modal akhir bln lalu ✔) | **364.333** | 17.770.665 | semua cocok ✔ | LENGKAP, ✔ seimbang |
| Jun | 9.574.000 | 0 | 0 | 16.099.998 | 0 | 13.170.000 | 17.770.665 (= modal akhir bln lalu ✔) | **−1.766.667** | 14.503.998 | semua cocok ✔ | LENGKAP, ✔ seimbang |

Σ laba 6 laporan bulanan = **−1.996.002** = laba laporan Jan–Jun sekaligus (**−1.996.002**) ✔. 11 pos per bulan: kas, piutang, kasbon, stok, aset tetap, utang pemasok, utang KUR, modal awal, laba, modal akhir, penyusutan.

## Catatan penguji (uji ulang v1.2.0)
- **Data lama, Februari:** kas akhir **Rp 22.408.250 ✔**. Karena file berisi pelunasan piutang/bon, script kini menanyakan piutang & utang pemasok per 1 Februari (SEMENTARA sampai dijawab).
- **BB1 (v1.1.0) tuntas.** April kini **−Rp 1.695.167** (v1.1.0: −485.167, pendapatan terhitung dua kali) dan Juni **−Rp 1.766.667** (v1.1.0: −2.548.194). Semua 11 pos cocok dengan penguji di **setiap** bulan. Modal akhir bulan N = modal awal bulan N+1 di kelima sambungan. Σ laba bulanan = laba 6 bulan (−1.996.002).
- **Aman bila agent lupa:** tanpa `--piutang-awal-periode` / `--utang-usaha-awal-periode`, April & Juni tetap salah (−495.167 / −2.566.667), **tetapi berstatus SEMENTARA** dengan pertanyaan eksplisit. Tidak ada lagi angka salah berlabel LENGKAP.
- **BS1 (v1.1.0) tuntas:** penyusutan per bulan kini dari harga beli (Feb 216.667, Mei–Jun 291.667). Pembulatan per bulan membuat total 6 bulan 1.400.002 (bukan 1.400.000). Selisih Rp 2 itu konsisten antara laporan bulanan dan laporan 6 bulan, dan disebut di asumsi.
- Ringan v1.1.0 tuntas: tanggal awal data kini 1 Januari (dari baris saldo awal); neraca menampilkan "Kas menurut buku Rp 11.618.000 + dana di rekening lain Rp 3.000.000" (uang laci + saldo bank sebenarnya); peringatan stok hanya muncul bila stok awal tidak diisi.
- Uji mode `--saldo-awal-per awal-periode` pada data toko (08): pos yang diisi dipakai apa adanya, pos lain tetap digulir. Hasilnya sama persis dengan mode awal-file.
