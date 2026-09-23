# 00 — Uji A/B: S1 dengan skill vs tanpa skill

**Permintaan (sama persis dengan S1, `01-katering-3-bulan-kur-prive.md`):** laporan keuangan Katering Dapur Sehati Jan–Mar 2026 dari `kas-dapur-sehati.csv` (70 transaksi), stok awal 1,2 jt / akhir 1,65 jt, piutang awal 1,5 jt / akhir 2 jt, utang toko beras 800 rb → 600 rb, peralatan lama 12 jt umur 4 tahun.

**Metode tanpa skill:** penguji menjawab sebagai AI agent biasa tanpa membaca skill apa pun. Agent membaca CSV, mengelompokkan transaksi sendiri (dibantu python ad-hoc), lalu menulis laporan. Transaksi yang tidak jelas **ditebak** dan asumsinya ditulis, sesuai perilaku umum agent tanpa panduan.

## Ringkasan berdampingan

| Aspek | Dengan skill | Tanpa skill |
|---|---|---|
| Laba (rugi) bersih | −Rp 2.118.583 (setelah 3 transaksi ditanyakan) | −Rp 2.382.125 |
| Total aset = L + E | Rp 37.639.750 ✔ (dicek script) | Rp 37.626.208 (seimbang, tidak ada baris cek eksplisit) |
| Transaksi ambigu (Bu Rina, kasbon, zakat) | **Ditanyakan** dalam satu pesan, lalu dihitung ulang | Ditebak: Bu Rina = penjualan, kasbon = piutang karyawan, zakat = beban usaha (salah bila zakat pribadi) |
| Penyusutan | Rp 952.083, aset baru disusutkan mulai bulan berikutnya | Rp 1.265.625: freezer yang dibeli 10 Feb disusutkan penuh 3 bulan (terlalu besar) |
| Prive | Rp 5.950.000, tidak masuk beban ✔ | Rp 5.700.000 ✔ (zakat masuk beban) |
| Angsuran KUR | Seluruhnya dianggap pokok (bunga tidak dipisah) | Sama, seluruhnya pokok |
| Struktur SAK EMKM | Laba Rugi + Posisi Keuangan + CaLK 10 butir + tren bulanan + asumsi + "Perlu dicek" | Laba Rugi + Neraca + catatan singkat. CaLK tidak lengkap (tanpa kebijakan akuntansi) |
| Disclaimer "bukan laporan audit" | Ada | Tidak ada |
| Reproduksibilitas | Script deterministik, bisa diulang dengan `--tetapkan` | Hitungan ad-hoc. Bila diulang di sesi lain, angka bisa berbeda |
| Baris rusak (koma di keterangan tanpa kutip) | Dilaporkan nomor barisnya | Tergantung cara agent membaca. Mudah terlewat |

## Output DENGAN skill
(lengkap; sama dengan 01 setelah jawaban pengguna)

# Laporan Keuangan Katering Dapur Sehati
Periode 1 Januari 2026 s.d. 31 Maret 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP**

## Ringkasan untuk pemilik
Usaha kamu RUGI Rp 2.118.583 selama 1 Januari 2026 s.d. 31 Maret 2026. Dari penjualan bersih Rp 36.150.000, yang tersisa jadi laba sekitar -5,9% (setiap Rp 100.000 penjualan, labanya sekitar -Rp 5.861). Pengeluaran terbesar: beban gaji & upah sebesar Rp 14.700.000 (38,0% dari total biaya). Arus kas usaha terbaik di Jan 2026 (Rp 1.280.000), terendah di Mar 2026 (-Rp 2.324.750). Kamu mengambil Rp 5.950.000 untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi mengurangi modal usaha. Uang kas di akhir periode: Rp 14.691.833.

## 1. Laporan Laba Rugi
Katering Dapur Sehati — untuk periode 1 Januari 2026 s.d. 31 Maret 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan tunai/transfer | Rp 34.150.000 |
| Penjualan tempo (piutang) | Rp 2.000.000 |
| Penjualan / pendapatan usaha | Rp 36.150.000 |
| **Pendapatan usaha bersih** | **Rp 36.150.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 1.200.000 |
| Pembelian bahan/barang dagangan | Rp 12.225.000 |
| Persediaan akhir | (Rp 1.650.000) |
| Beban pokok penjualan | (Rp 11.775.000) |
| **Laba kotor** | **Rp 24.375.000** |
| **Beban usaha** |  |
| Beban gaji & upah | Rp 14.700.000 |
| Beban sewa tempat | Rp 4.500.000 |
| Beban listrik, air, gas & internet | Rp 3.275.000 |
| Beban transportasi & pengiriman | Rp 535.000 |
| Beban iklan & promosi | Rp 550.000 |
| Beban kemasan & perlengkapan | Rp 1.550.000 |
| Beban perawatan & perbaikan | Rp 185.000 |
| Beban lain-lain | Rp 75.000 |
| Beban penyusutan aset tetap | Rp 952.083 |
| Total beban usaha | (Rp 26.322.083) |
| **Laba (rugi) usaha** | **-Rp 1.947.083** |
| Beban bunga & biaya bank (beban keuangan) | (Rp 15.000) |
| **Laba (rugi) sebelum pajak** | **-Rp 1.962.083** |
| Beban pajak penghasilan | (Rp 156.500) |
| **LABA (RUGI) BERSIH** | **-Rp 2.118.583** |

## 2. Laporan Posisi Keuangan (Neraca)
Katering Dapur Sehati — per 31 Maret 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas dan setara kas | Rp 14.691.833 |
| Piutang usaha | Rp 2.000.000 |
| Persediaan | Rp 1.650.000 |
| Aset tetap (awal + pembelian Rp 8.250.000) | Rp 20.250.000 |
| Penyusutan periode ini | (Rp 952.083) |
| Aset tetap (nilai buku) | Rp 19.297.917 |
| **Total aset** | **Rp 37.639.750** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 600.000 |
| Utang bank / pinjaman | Rp 22.708.333 |
| Total liabilitas | Rp 23.308.333 |
| **EKUITAS** |  |
| Modal awal | Rp 22.400.000 |
| Laba (rugi) bersih periode ini | -Rp 2.118.583 |
| Prive (pengambilan pribadi) | (Rp 5.950.000) |
| Modal akhir | Rp 14.331.417 |
| **Total liabilitas + ekuitas** | **Rp 37.639.750** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 37.639.750). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Katering Dapur Sehati adalah usaha yang laporan keuangannya disusun untuk periode 1 Januari 2026 s.d. 31 Maret 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 14.691.833 (saldo awal Rp 8.500.000, total uang masuk Rp 60.650.000, total uang keluar Rp 54.458.167).

**4. Piutang usaha** Rp 2.000.000 (awal Rp 1.500.000). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 1.650.000 (awal Rp 1.200.000). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 11.775.000.

**6. Aset tetap** nilai buku Rp 19.297.917 (awal Rp 12.000.000, pembelian periode ini Rp 8.250.000, penyusutan periode ini Rp 952.083). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 600.000 dan utang bank/pinjaman Rp 22.708.333 (pinjaman diterima Rp 25.000.000, pembayaran pokok Rp 2.291.667).

**8. Ekuitas.** Modal awal Rp 22.400.000 + tambahan modal Rp 0 + laba bersih -Rp 2.118.583 - prive Rp 5.950.000 = modal akhir Rp 14.331.417.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 36.150.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 26.322.083, beban keuangan Rp 15.000, beban pajak penghasilan Rp 156.500. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Tren per periode (arus kas usaha, sebelum penyesuaian stok/piutang/penyusutan)

| Periode | Uang masuk usaha | Uang keluar usaha | Selisih | Prive |
|---|---:|---:|---:|---:|
| Jan 2026 | Rp 11.400.000 | Rp 10.120.000 | Rp 1.280.000 | Rp 1.350.000 |
| Feb 2026 | Rp 9.200.000 | Rp 11.171.750 | -Rp 1.971.750 | Rp 1.500.000 |
| Mar 2026 | Rp 13.550.000 | Rp 15.874.750 | -Rp 2.324.750 | Rp 3.100.000 |

## Perlu dicek
**Baris yang sengaja dilewati:** baris saldo awal (dipakai sebagai kas awal bila --kas-awal tidak diisi) (1 baris)

## Asumsi yang dipakai
- Periode laporan dianggap 1 Januari 2026 s.d. 31 Maret 2026 (bulan penuh dari transaksi pertama sampai terakhir).
- Kas awal diambil dari baris 'saldo awal' di file: Rp 8.500.000.
- Saldo awal utang bank/pinjaman tidak diberikan, dianggap Rp 0.
- Penyusutan garis lurus, umur manfaat 4 tahun, tanpa nilai sisa; aset yang dibeli dalam periode mulai disusutkan bulan berikutnya. Aset awal disusutkan dari nilai bukunya (pendekatan).
- Modal awal dihitung dari (aset awal - utang awal) = Rp 22.400.000.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

## Output TANPA skill (simulasi agent biasa)

> Berikut laporan keuangan Katering Dapur Sehati untuk Januari–Maret 2026. Saya mengelompokkan 70 transaksi di file. Beberapa transaksi kurang jelas, jadi saya pakai asumsi berikut:
> - "Transfer dari Bu Rina" Rp 750.000 saya anggap pembayaran pesanan.
> - "Kasbon Pak Darto" Rp 300.000 saya anggap piutang karyawan (akan dipotong gaji).
> - "Zakat" Rp 250.000 saya masukkan ke beban lain-lain.
> - Pencairan KUR Rp 25 juta dicatat sebagai utang, bukan pendapatan. Angsuran Rp 2.291.667 mengurangi utang.
> - Penyusutan peralatan: garis lurus 4 tahun untuk semua aset selama 3 bulan.
>
> **LAPORAN LABA RUGI (1 Jan – 31 Mar 2026)**
>
> | Keterangan | Jumlah (Rp) |
> |---|---:|
> | Pendapatan penjualan (tunai 34.150.000 + piutang baru 2.000.000) | 36.150.000 |
> | HPP (stok awal 1.200.000 + pembelian 12.350.000 − stok akhir 1.650.000) | (11.900.000) |
> | **Laba kotor** | **24.250.000** |
> | Gaji & THR | (14.400.000) |
> | Sewa dapur | (4.500.000) |
> | Gas & listrik | (3.150.000) |
> | Kemasan (box, mika) | (1.550.000) |
> | Iklan | (550.000) |
> | Bensin | (535.000) |
> | Servis | (185.000) |
> | Iuran & zakat | (325.000) |
> | Biaya bank | (15.000) |
> | Penyusutan | (1.265.625) |
> | **Laba sebelum pajak** | **(2.225.625)** |
> | PPh final | (156.500) |
> | **Rugi bersih** | **(2.382.125)** |
>
> **NERACA per 31 Maret 2026**
>
> | Aset | Rp | Kewajiban & Modal | Rp |
> |---|---:|---|---:|
> | Kas | 14.691.833 | Utang dagang | 600.000 |
> | Piutang usaha | 2.000.000 | Utang KUR | 22.708.333 |
> | Piutang karyawan | 300.000 | Modal awal | 22.400.000 |
> | Persediaan | 1.650.000 | Rugi periode | (2.382.125) |
> | Peralatan (20.250.000 − 1.265.625) | 18.984.375 | Prive | (5.700.000) |
> | **Total** | **37.626.208** | **Total** | **37.626.208** |
>
> **Catatan:** Usaha rugi sekitar Rp 2,4 juta dalam 3 bulan, terutama karena biaya gaji dan sewa yang tinggi dibanding penjualan. Pengambilan pribadi Rp 5,7 juta juga mengurangi modal. Sebaiknya kurangi biaya tetap atau naikkan harga.

## Penilaian penguji
**Skill jelas lebih baik**, terutama untuk keandalan (janji "reliable"):
1. **Tidak menebak diam-diam.** Tanpa skill, zakat pribadi masuk beban usaha. Laba jadi lebih kecil Rp 250.000 dan pemilik tidak tahu bahwa itu tebakan, kecuali membaca daftar asumsi. Skill menanyakan tiga transaksi itu lebih dulu.
2. **Hitungan tepat & bisa diulang.** Penyusutan skill mengikuti tanggal beli. Versi tanpa skill membebankan freezer 3 bulan penuh (lebih besar Rp 313.542). Script membuat hasil sama setiap kali dijalankan, dan baris rusak dilaporkan.
3. **Format SAK EMKM lengkap** dengan CaLK (dasar penyusunan, kebijakan, rincian pos), tren bulanan, asumsi, dan disclaimer "bukan laporan audit". Versi tanpa skill tidak punya disclaimer, padahal pengguna menyebut "kalau bank minta".
4. **Ringkasan awam** (untung/rugi, pengeluaran terbesar, prive, kas akhir) lebih jelas.

**Di mana versi tanpa skill lebih baik:** kasbon karyawan dicatat sebagai **piutang karyawan** (aset). Itu perlakuan yang lebih tepat daripada `beban_gaji`, yang terpaksa dipakai skill karena tidak punya kategori piutang lain-lain. Keduanya **sama-sama gagal** memisahkan bunga dari angsuran KUR.

Kesimpulan: nilai tambah skill nyata (akurasi, konsistensi, kepatuhan format, penanganan ambigu). Uji A/B **lulus**.
