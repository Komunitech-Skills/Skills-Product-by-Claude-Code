# 06 — Laporan per bulan dari buku kas 6 bulan (uji B1 v1.1.0)

## Skenario
Uji ulang cacat berat B1 (laporan satu periode dari buku kas multi-bulan). Dua data:
1. **Data lama** `kas-dapur-sehati.csv` (Jan–Mar): laporan **Februari** saja. Target: kas akhir Rp 22.408.250.
2. **Data baru** `konveksi-6bln.csv` (Jan–Jun 2026, 63 transaksi, fiktif): KUR cair Februari + 4 angsuran dengan bunga, 2 pembelian mesin, setor/tarik tunai ke bank, kasbon (Mar, lunas Mei), setoran modal (Apr), prive bulanan, **penjualan tempo Maret Rp 1,2 jt yang dilunasi April**, dan **pembelian tempo Mei Rp 800 rb yang dibayar Juni**. Enam laporan bulanan dibuat satu per satu, lalu setiap bulan dicek independen (kas, piutang, kasbon, utang, aset tetap, modal/laba ditahan, keseimbangan) dengan `verif_6bln.py`, ledger akrual bulanan yang ditulis penguji tanpa memakai kode skill.

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
Untuk setiap bulan, agent menjalankan (contoh Maret):
```bash
python3 scripts/laporan_emkm.py konveksi-6bln.csv --nama-usaha "Konveksi Rapi Fiktif" \
  --periode-awal 2026-03-01 --periode-akhir 2026-03-31 --umur-aset-tahun 5 \
  --persediaan-awal 3.000.000 --persediaan-akhir 2.500.000 \
  --piutang-awal 2jt --utang-usaha-awal 1,5jt --aset-tetap-awal 10jt --utang-bank-awal 0 \
  --piutang-akhir 1,2jt --utang-usaha-akhir 0 --bunga 23=150.000
```
Sesuai SKILL.md langkah 2, saldo awal per 1 Januari diberikan apa adanya dan script menggulirkannya; stok awal bulan diambil dari stok akhir bulan sebelumnya (jawaban pengguna).

### Contoh hasil: laporan Maret 2026 (output script)

# Laporan Keuangan Konveksi Rapi Fiktif
Periode 1 Maret 2026 s.d. 31 Maret 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP**

## Ringkasan untuk pemilik
Usaha kamu RUGI Rp 440.278 selama 1 Maret 2026 s.d. 31 Maret 2026. Dari penjualan bersih Rp 8.700.000, setiap Rp 100.000 penjualan usaha rugi sekitar Rp 5.061. Pengeluaran terbesar: pembelian bahan/barang dagangan sebesar Rp 4.200.000 (48,6% dari total biaya). Uang kas di akhir periode: Rp 19.001.500.

## 1. Laporan Laba Rugi
Konveksi Rapi Fiktif — untuk periode 1 Maret 2026 s.d. 31 Maret 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan tunai/transfer | Rp 7.500.000 |
| Penjualan tempo (piutang) | Rp 1.200.000 |
| Penjualan / pendapatan usaha | Rp 8.700.000 |
| **Pendapatan usaha bersih** | **Rp 8.700.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 3.000.000 |
| Pembelian bahan/barang dagangan | Rp 4.200.000 |
| Persediaan akhir | (Rp 2.500.000) |
| Beban pokok penjualan | (Rp 4.700.000) |
| **Laba kotor** | **Rp 4.000.000** |
| **Beban usaha** |  |
| Beban gaji & upah | Rp 2.400.000 |
| Beban sewa tempat | Rp 1.000.000 |
| Beban listrik, air, gas & internet | Rp 400.000 |
| Beban transportasi & pengiriman | Rp 250.000 |
| Beban penyusutan aset tetap | Rp 210.278 |
| Total beban usaha | (Rp 4.260.278) |
| **Laba (rugi) usaha** | **-Rp 260.278** |
| Beban bunga & biaya bank (beban keuangan) | (Rp 150.000) |
| **Laba (rugi) sebelum pajak** | **-Rp 410.278** |
| Beban pajak penghasilan | (Rp 30.000) |
| **LABA (RUGI) BERSIH** | **-Rp 440.278** |

## 2. Laporan Posisi Keuangan (Neraca)
Konveksi Rapi Fiktif — per 31 Maret 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas menurut buku | Rp 21.001.500 |
| Dana dipindah ke kas/rekening lain | -Rp 2.000.000 |
| Kas dan setara kas | Rp 19.001.500 |
| Piutang usaha | Rp 1.200.000 |
| Kasbon karyawan & piutang lain-lain | Rp 500.000 |
| Persediaan | Rp 2.500.000 |
| Aset tetap (awal + pembelian Rp 0) | Rp 12.616.667 |
| Penyusutan periode ini | (Rp 210.278) |
| Aset tetap (nilai buku) | Rp 12.406.389 |
| **Total aset** | **Rp 35.607.889** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 0 |
| Utang bank / pinjaman | Rp 18.300.000 |
| Total liabilitas | Rp 18.300.000 |
| **EKUITAS** |  |
| Modal awal | Rp 17.748.167 |
| Laba (rugi) bersih periode ini | -Rp 440.278 |
| Prive (pengambilan pribadi) | Rp 0 |
| Modal akhir | Rp 17.307.889 |
| **Total liabilitas + ekuitas** | **Rp 35.607.889** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 35.607.889). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Konveksi Rapi Fiktif adalah usaha yang laporan keuangannya disusun untuk periode 1 Maret 2026 s.d. 31 Maret 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 19.001.500 (saldo awal Rp 22.131.500, total uang masuk Rp 9.500.000, total uang keluar Rp 10.630.000).

**4. Piutang usaha** Rp 1.200.000 (awal Rp 0). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 2.500.000 (awal Rp 3.000.000). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 4.700.000.

**6. Aset tetap** nilai buku Rp 12.406.389 (awal Rp 12.616.667, pembelian periode ini Rp 0, penyusutan periode ini Rp 210.278). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 0 dan utang bank/pinjaman Rp 18.300.000 (pinjaman diterima Rp 0, pembayaran pokok Rp 1.700.000).

**8. Ekuitas.** Modal awal Rp 17.748.167 + tambahan modal Rp 0 + laba bersih -Rp 440.278 - prive Rp 0 = modal akhir Rp 17.307.889.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 8.700.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 4.260.278, beban keuangan Rp 150.000, beban pajak penghasilan Rp 30.000. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Perlu dicek
**Baris yang sengaja dilewati:** baris saldo awal (dipakai sebagai kas awal bila --kas-awal tidak diisi) (1 baris)

**Peringatan:**
- 33 transaksi setelah 31 Maret 2026 tidak dihitung.
- Stok (persediaan) awal periode dianggap Rp 3.000.000 karena stok per 1 Maret 2026 tidak diketahui. Saldo awal stok, piutang, dan utang sebaiknya per 1 Maret 2026 (hasil hitung stok / catatan tagihan).

## Asumsi yang dipakai
- Kas awal diambil dari baris 'saldo awal' di file: Rp 6.000.000.
- Saldo awal yang Anda berikan/dibaca dari file dianggap per awal data (3 Januari 2026), lalu digulirkan dengan 20 transaksi sebelum 1 Maret 2026. Kas awal periode = Rp 22.131.500; modal awal periode sudah termasuk laba/prive sebelum periode. Jika angka yang Anda berikan sudah per 1 Maret 2026, jalankan dengan --saldo-awal-per awal-periode.
- Penyusutan sebelum periode (Rp 383.333) sudah dikurangkan dari aset tetap awal.
- Penyusutan garis lurus, umur manfaat 5 tahun, tanpa nilai sisa; aset yang dibeli dalam periode mulai disusutkan bulan berikutnya. Aset awal disusutkan dari nilai bukunya (pendekatan).
- Modal awal dihitung dari (aset awal - utang awal) = Rp 17.748.167.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

### Rekap uji 6 laporan bulanan vs verifikasi independen
| Bulan | Kas & setara kas (script, dicek penguji) | Utang KUR | Laba script | Laba penguji | Modal awal script | Modal akhir bulan lalu (laporan script) | Status script |
|---|---:|---:|---:|---:|---:|---:|---|
| Jan | 4.850.000 ✔ | 0 ✔ | 2.283.333 | 2.283.333 ✔ | 18.000.000 | – | LENGKAP, ✔ seimbang |
| Feb | 22.131.500 ✔ | 20.000.000 ✔ | −732.389 | −735.167 | 19.483.333 | 19.483.333 ✔ | LENGKAP, ✔ seimbang |
| Mar | 19.001.500 ✔ | 18.300.000 ✔ | −440.278 | −446.667 | 17.748.167 | 17.750.944 (beda 2.777) | LENGKAP, ✔ seimbang |
| **Apr** | 14.618.000 ✔ | 16.595.000 ✔ | **−485.167** | **−1.695.167** | 16.101.500 | 17.307.889 (**beda 1.206.389**) | LENGKAP, ✔ seimbang |
| Mei | 13.964.000 ✔ | 14.885.000 ✔ | 377.944 | 364.333 | 17.406.333 | 17.416.333 (beda 10.000) | LENGKAP, ✔ seimbang |
| **Jun** | 9.574.000 ✔ | 13.170.000 ✔ | **−2.548.194** | **−1.766.667** | 18.570.667 | 17.784.277 (**beda 786.390**) | LENGKAP, ✔ seimbang |
| Jan–Jun (satu laporan) | 9.574.000 ✔ | 13.170.000 ✔ | −1.996.000 | −1.996.000 ✔ | 18.000.000 | – | LENGKAP, ✔ seimbang |

Jumlah laba enam laporan bulanan script = −1.544.751, sedangkan laporan Jan–Jun script sendiri = −1.996.000 (selisih Rp 451.249).

## Catatan penguji
- **Data lama, Februari:** kas awal digulirkan ke Rp 7.680.000 dan **kas akhir Rp 22.408.250 ✔** (v1.0.0: Rp 23.228.250). Kasbon Rp 300.000 tercatat di aset, neraca seimbang, asumsi penggulungan disebut. **Cacat B1 lama (kas) tuntas.**
- **Data baru, yang benar setiap bulan:** kas & setara kas (termasuk dana yang disetor ke bank), utang KUR setelah pemecahan bunga, kasbon (Mar–Apr Rp 500.000, Mei nol), dan keseimbangan neraca. Laporan Jan–Jun sekaligus cocok persis dengan penguji (laba −Rp 1.996.000; aset = L + E = Rp 27.674.000).
- **CACAT BERAT BARU — piutang/utang pemasok tidak ikut bergulir antarbulan.** Penggulungan hanya mengurangi piutang/utang awal file dengan pembayaran sebelum periode. Script tidak tahu penjualan/pembelian tempo di bulan sebelumnya. Akibatnya:
  - **April:** piutang awal dianggap Rp 0 (seharusnya Rp 1.200.000). Pelunasan jaket Rp 1,2 jt dihitung lagi sebagai "penjualan tempo". Pendapatan **dihitung dua kali** (Maret dan April), jadi laba April −Rp 485.167, padahal seharusnya −Rp 1.695.167.
  - **Juni:** utang pemasok awal dianggap Rp 0 (seharusnya Rp 800.000). Pembayaran bon Rp 800 rb menjadi "pembelian tempo" baru, jadi HPP dihitung dua kali dan laba −Rp 2.548.194, padahal seharusnya −Rp 1.766.667.
  - Keduanya berlabel **LENGKAP** dan **✔ seimbang**, tanpa peringatan khusus selain kalimat umum "saldo awal stok, piutang, dan utang sebaiknya per 1 April". Modal awal April tidak sama dengan modal akhir Maret (beda Rp 1,2 jt), tetapi tidak ada yang memeriksanya.
  - Tidak ada jalan benar lewat CLI. `--piutang-awal 1,2jt` dianggap per awal file lalu dipotong pelunasan Januari menjadi 0. Kalau memakai `--saldo-awal-per awal-periode`, aset tetap, utang bank, dan kasbon tidak digulirkan lagi. Kasbon juga tidak punya opsi saldo awal, sehingga pada uji "rantai" (saldo per awal bulan diambil dari neraca bulan lalu) kasbon Rp 500.000 hilang dari neraca April (tetap LENGKAP, ✔), dan Mei menjadi SEMENTARA karena kasbon negatif.
  - *Saran:* (1) di mode `awal-file`, bila ada transaksi sebelum periode, masukkan ke "Pertanyaan untuk pemilik": "Berapa piutang pelanggan dan utang pemasok per <tanggal awal periode>?" (status SEMENTARA sampai dijawab); (2) tambahkan opsi per pos yang berlaku per awal periode (mis. `--piutang-awal-periode`, `--utang-usaha-awal-periode`) atau ubah `--saldo-awal-per awal-periode` agar hanya pos yang diisi pengguna yang tidak digulir; (3) tambahkan `--piutang-lain-awal`; (4) tambahkan uji regresi "penjualan tempo bulan lalu dilunasi bulan ini".
- **Sedang baru — penyusutan bulanan dari nilai buku, bukan biaya perolehan** (`hitung()`, blok penyusutan: `Decimal(aset_tetap_awal) / bulan_umur`). Setelah digulirkan, aset awal periode adalah nilai buku, sehingga penyusutan per bulan makin kecil (Feb 213.889; Mar 210.278; Jun 273.194 vs 216.667/216.667/291.667). Laba bulanan tidak menjumlah ke laba semester, dan modal akhir bulan ≠ modal awal bulan berikutnya (selisih kecil). *Saran:* simpan biaya perolehan + bulan mulai per aset (awal file & pembelian), lalu hitung penyusutan periode dari biaya perolehan, sama seperti `dep_sebelum`.
- Ringan: peringatan "Stok awal periode dianggap Rp 3.000.000 karena stok per 1 Maret tidak diketahui" tetap muncul walau pengguna memberi stok per 1 Maret. Asumsi menulis "awal data (3 Januari 2026)" padahal baris saldo awal bertanggal 1 Januari.
- Ringan: di neraca Maret, baris "Kas menurut buku Rp 21.001.500 / Dana dipindah −Rp 2.000.000" hanya memakai transfer bulan berjalan, sehingga tidak menunjukkan uang laci (Rp 16.001.500) maupun saldo bank (Rp 3.000.000). Total kas & setara kas tetap benar.
