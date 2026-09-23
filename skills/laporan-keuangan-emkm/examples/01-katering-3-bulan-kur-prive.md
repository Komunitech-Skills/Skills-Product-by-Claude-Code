# 01 — Katering 3 bulan (70 transaksi, KUR, beli aset, prive) — diuji ulang dengan v1.2.0

## Skenario
S1, permintaan normal dan lengkap. Pemilik katering rumahan menyerahkan buku kas Januari–Maret 2026 (70 transaksi + baris saldo awal) dan menyebutkan saldo stok, piutang, utang pemasok, serta peralatan lama. Buku kas memuat pencairan KUR, angsuran KUR, pembelian kompor & freezer, beberapa pengambilan pribadi, setoran PPh final, dan 3 transaksi yang tidak jelas.

## Input pengguna
> Mbak, tolong bikinin laporan keuangan katering aku Januari sampai Maret, mau buat arsip sama jaga-jaga kalau bank minta. Filenya kas-dapur-sehati.csv. Stok bahan awal Januari kira-kira 1,2 juta, akhir Maret 1.650.000. PT Maju Fiktif utang 1,5 juta dari Desember (udah lunas Januari), terus pesanan Maret mereka 2 juta belum dibayar. Aku juga masih ngutang toko beras 800rb dari Desember, sekarang sisa utang 600rb. Peralatan dapur lama nilainya 12 juta, kira-kira kepake 4 tahun lagi. Nama usahanya Katering Dapur Sehati.

Isi `kas-dapur-sehati.csv` (fiktif, dibuat penguji):

```csv
Tanggal,Keterangan,Masuk,Keluar,Kategori
01/01/2026,Saldo awal,"Rp 8.500.000",,
02/01/2026,Belanja pasar sayur & bumbu,,"Rp 650.000",
02/01/2026,Beli beras 50 kg,,"Rp 725.000",
03/01/2026,Pesanan nasi box 120 pcs kantor kecamatan,"Rp 3.000.000",,
04/01/2026,Beli daging ayam 25 kg,,"Rp 900.000",
05/01/2026,Gas elpiji 3 tabung 12kg,,"Rp 630.000",
06/01/2026,DP pesanan tumpeng syukuran Pak Harjo,"Rp 500.000",,
07/01/2026,Bayar bon toko beras bulan Desember,,"Rp 800.000",
08/01/2026,Terima pelunasan piutang PT Maju Fiktif (Desember),"Rp 1.500.000",,
09/01/2026,Pelunasan pesanan tumpeng Pak Harjo,"Rp 1.250.000",,
10/01/2026,Ambil untuk belanja rumah tangga,,"Rp 1.000.000",
11/01/2026,Beli box nasi & mika,,"Rp 420.000",
12/01/2026,Katering harian karyawan toko (mingguan),"Rp 2.100.000",,
14/01/2026,Minyak goreng & telur,,"Rp 540.000",
15/01/2026,Token listrik,,"Rp 300.000",
16/01/2026,Bensin antar pesanan,,"Rp 150.000",
18/01/2026,Transfer dari Bu Rina,"Rp 750.000",,
19/01/2026,Pesanan snack box pengajian,"Rp 1.800.000",,
20/01/2026,Beli kompor 2 tungku,,"Rp 1.450.000",
22/01/2026,Belanja pasar sayur & bumbu,,"Rp 580.000",
24/01/2026,Pesanan nasi box 80 pcs arisan RT,"Rp 2.000.000",,
25/01/2026,Beli air mineral gelas 5 dus,,"Rp 125.000",
28/01/2026,Bayar sewa dapur bulan Januari,,"Rp 1.500.000",
30/01/2026,Gaji 2 karyawan Januari,,"Rp 3.600.000",
31/01/2026,Bayar SPP anak,,"Rp 350.000",
02/02/2026,Belanja pasar sayur & bumbu,,"Rp 700.000",
03/02/2026,Beli beras 50 kg,,"Rp 740.000",
04/02/2026,Pesanan nasi box 150 pcs pernikahan,"Rp 3.750.000",,
05/02/2026,Pencairan KUR BRI,"Rp 25.000.000",,
06/02/2026,Beli daging ayam 30 kg,,"Rp 1.080.000",
07/02/2026,Gas elpiji 3 tabung 12kg,,"Rp 630.000",
09/02/2026,Katering harian karyawan toko (mingguan),"Rp 2.100.000",,
10/02/2026,Beli freezer 2 pintu,,"Rp 6.800.000",
11/02/2026,"Setor PPh final 0,5% Januari",,"Rp 61.750",
12/02/2026,Iklan Instagram,,"Rp 250.000",
13/02/2026,Pesanan snack box seminar,"Rp 2.400.000",,
14/02/2026,Minyak goreng & telur,,"Rp 610.000",
15/02/2026,Token listrik,,"Rp 350.000",
16/02/2026,Ambil uang pribadi,,"Rp 1.500.000",
17/02/2026,Kasbon Pak Darto,,"Rp 300.000",
18/02/2026,Beli box nasi & mika,,"Rp 480.000",
20/02/2026,Pesanan tumpeng ulang tahun,"Rp 950.000",,
22/02/2026,Belanja pasar sayur & bumbu,,"Rp 620.000",
23/02/2026,Iuran keamanan & sampah,,"Rp 75.000",
25/02/2026,Bensin antar pesanan,,"Rp 175.000",
27/02/2026,Bayar sewa dapur bulan Februari,,"Rp 1.500.000",
28/02/2026,Gaji 2 karyawan Februari,,"Rp 3.600.000",
02/03/2026,Belanja pasar sayur & bumbu,,"Rp 760.000",
03/03/2026,Beli beras 50 kg,,"Rp 740.000",
04/03/2026,Pesanan nasi box 200 pcs buka bersama,"Rp 5.000.000",,
05/03/2026,Angsuran KUR BRI ke-1,,"Rp 2.291.667",
06/03/2026,Beli daging ayam 40 kg,,"Rp 1.440.000",
07/03/2026,Gas elpiji 4 tabung 12kg,,"Rp 840.000",
08/03/2026,Katering harian karyawan toko (mingguan),"Rp 2.100.000",,
10/03/2026,"Setor PPh final 0,5% Februari",,"Rp 94.750",
11/03/2026,Pesanan takjil 300 pcs masjid,"Rp 2.700.000",,
12/03/2026,Minyak goreng & telur,,"Rp 720.000",
13/03/2026,Beli box nasi & mika,,"Rp 650.000",
15/03/2026,Token listrik,,"Rp 400.000",
16/03/2026,Bayar SPP anak,,"Rp 350.000",
18/03/2026,Pesanan nasi box 150 pcs buka bersama kantor,"Rp 3.750.000",,
19/03/2026,Iklan Instagram,,"Rp 300.000",
20/03/2026,Servis kompor & regulator,,"Rp 185.000",
22/03/2026,Belanja pasar sayur & bumbu,,"Rp 820.000",
24/03/2026,Bensin antar pesanan,,"Rp 210.000",
25/03/2026,Beli sembako & baju lebaran keluarga,,"Rp 2.500.000",
26/03/2026,THR 2 karyawan,,"Rp 3.600.000",
27/03/2026,Bayar sewa dapur bulan Maret,,"Rp 1.500.000",
28/03/2026,Biaya admin bank,,"Rp 15.000",
30/03/2026,Gaji 2 karyawan Maret,,"Rp 3.600.000",
31/03/2026,Zakat,,"Rp 250.000",
```

## Output

### Langkah agent (mengikuti SKILL.md, script v1.2.0)
1. File CSV disimpan apa adanya, lalu script dijalankan:
   ```bash
   python3 scripts/laporan_emkm.py kas-dapur-sehati.csv --nama-usaha "Katering Dapur Sehati" \
     --persediaan-awal "1,2jt" --persediaan-akhir "Rp 1.650.000" --piutang-awal "1.500.000" --piutang-akhir "2 juta" \
     --utang-usaha-awal 800rb --utang-usaha-akhir 600rb --aset-tetap-awal "Rp 12.000.000" --umur-aset-tahun 4
   ```
2. Status SEMENTARA. Bagian "Perlu dicek" berisi 1 pertanyaan otomatis (porsi bunga angsuran KUR baris 52) dan 2 transaksi belum terklasifikasi. "Kasbon Pak Darto" sekarang otomatis dicatat sebagai kasbon/piutang karyawan (aset), dan "Beli air mineral gelas" sebagai pembelian bahan. Agent menggabungkan semuanya menjadi **satu** pesan:

> Laporannya hampir jadi. Ada 3 hal yang perlu Ibu jawab dulu:
>
> 1. **Angsuran KUR BRI ke-1 (5 Mar, Rp 2.291.667):** berapa bagian **bunga**nya? Lihat di jadwal angsuran/buku tabungan BRI. Bunga dicatat sebagai beban, pokok mengurangi utang KUR. Kalau tidak tahu, saya bisa anggap pokok saja, tapi laba akan terlihat sedikit lebih tinggi.
> 2. **Transfer dari Bu Rina (18 Jan, masuk Rp 750.000):** a) bayar pesanan · b) setoran modal · c) pinjaman · d) lainnya
> 3. **Zakat (31 Mar, keluar Rp 250.000):** a) zakat pribadi (prive) · b) sumbangan atas nama usaha (beban lain-lain)
>
> Catatan: kasbon Pak Darto Rp 300.000 saya catat sebagai piutang karyawan (bukan biaya), karena nanti dipotong dari gaji.

**Jawaban pengguna:** "Di jadwal BRI bunganya 208.334. Bu Rina itu pelunasan pesanan nasi box. Zakat itu zakat pribadi aku."

3. Script dijalankan ulang dengan `--bunga 52=208.334 --tetapkan 18=pendapatan_usaha --tetapkan 72=prive`. Hasil akhir:

---

# Laporan Keuangan Katering Dapur Sehati
Periode 1 Januari 2026 s.d. 31 Maret 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP (dengan asumsi)**

## Ringkasan untuk pemilik
Usaha kamu RUGI Rp 2.026.917 selama 1 Januari 2026 s.d. 31 Maret 2026. Dari penjualan bersih Rp 36.150.000, setiap Rp 100.000 penjualan usaha rugi sekitar Rp 5.607. Pengeluaran terbesar: beban gaji & upah sebesar Rp 14.400.000 (37,3% dari total biaya). Arus kas usaha terbaik di Jan 2026 (Rp 1.280.000), terendah di Mar 2026 (-Rp 2.533.084). Kamu mengambil Rp 5.950.000 untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi mengurangi modal usaha. Uang kas di akhir periode: Rp 14.691.833.

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
| Pembelian bahan/barang dagangan | Rp 12.350.000 |
| Persediaan akhir | (Rp 1.650.000) |
| Beban pokok penjualan | (Rp 11.900.000) |
| **Laba kotor** | **Rp 24.250.000** |
| **Beban usaha** |  |
| Beban gaji & upah | Rp 14.400.000 |
| Beban sewa tempat | Rp 4.500.000 |
| Beban listrik, air, gas & internet | Rp 3.150.000 |
| Beban transportasi & pengiriman | Rp 535.000 |
| Beban iklan & promosi | Rp 550.000 |
| Beban kemasan & perlengkapan | Rp 1.550.000 |
| Beban perawatan & perbaikan | Rp 185.000 |
| Beban lain-lain | Rp 75.000 |
| Beban penyusutan aset tetap | Rp 952.083 |
| Total beban usaha | (Rp 25.897.083) |
| **Laba (rugi) usaha** | **-Rp 1.647.083** |
| Beban bunga & biaya bank (beban keuangan) | (Rp 223.334) |
| **Laba (rugi) sebelum pajak** | **-Rp 1.870.417** |
| Beban pajak penghasilan | (Rp 156.500) |
| **LABA (RUGI) BERSIH** | **-Rp 2.026.917** |

## 2. Laporan Posisi Keuangan (Neraca)
Katering Dapur Sehati — per 31 Maret 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas dan setara kas | Rp 14.691.833 |
| Piutang usaha | Rp 2.000.000 |
| Kasbon karyawan & piutang lain-lain | Rp 300.000 |
| Persediaan | Rp 1.650.000 |
| Aset tetap (awal + pembelian Rp 8.250.000) | Rp 20.250.000 |
| Penyusutan periode ini | (Rp 952.083) |
| Aset tetap (nilai buku) | Rp 19.297.917 |
| **Total aset** | **Rp 37.939.750** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 600.000 |
| Utang bank / pinjaman | Rp 22.916.667 |
| Total liabilitas | Rp 23.516.667 |
| **EKUITAS** |  |
| Modal awal | Rp 22.400.000 |
| Laba (rugi) bersih periode ini | -Rp 2.026.917 |
| Prive (pengambilan pribadi) | (Rp 5.950.000) |
| Modal akhir | Rp 14.423.083 |
| **Total liabilitas + ekuitas** | **Rp 37.939.750** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 37.939.750). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Katering Dapur Sehati adalah usaha yang laporan keuangannya disusun untuk periode 1 Januari 2026 s.d. 31 Maret 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 14.691.833 (saldo awal Rp 8.500.000, total uang masuk Rp 60.650.000, total uang keluar Rp 54.458.167).

**4. Piutang usaha** Rp 2.000.000 (awal Rp 1.500.000). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 1.650.000 (awal Rp 1.200.000). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 11.900.000.

**6. Aset tetap** nilai buku Rp 19.297.917 (awal Rp 12.000.000, pembelian periode ini Rp 8.250.000, penyusutan periode ini Rp 952.083). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 600.000 dan utang bank/pinjaman Rp 22.916.667 (pinjaman diterima Rp 25.000.000, pembayaran pokok Rp 2.083.333).

**8. Ekuitas.** Modal awal Rp 22.400.000 + tambahan modal Rp 0 + laba bersih -Rp 2.026.917 - prive Rp 5.950.000 = modal akhir Rp 14.423.083.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 36.150.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 25.897.083, beban keuangan Rp 223.334, beban pajak penghasilan Rp 156.500. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Tren per periode (arus kas usaha, sebelum penyesuaian stok/piutang/penyusutan)

| Periode | Uang masuk usaha | Uang keluar usaha | Selisih | Prive |
|---|---:|---:|---:|---:|
| Jan 2026 | Rp 11.400.000 | Rp 10.120.000 | Rp 1.280.000 | Rp 1.350.000 |
| Feb 2026 | Rp 9.200.000 | Rp 10.871.750 | -Rp 1.671.750 | Rp 1.500.000 |
| Mar 2026 | Rp 13.550.000 | Rp 16.083.084 | -Rp 2.533.084 | Rp 3.100.000 |

## Perlu dicek
**Baris yang sengaja dilewati:** baris saldo awal (dipakai sebagai kas awal bila --kas-awal tidak diisi) (1 baris)

## Asumsi yang dipakai
- Periode laporan dianggap 1 Januari 2026 s.d. 31 Maret 2026 (bulan penuh dari transaksi pertama sampai terakhir).
- Kas awal diambil dari baris 'saldo awal' di file: Rp 8.500.000.
- Saldo awal utang bank/pinjaman tidak diberikan, dianggap Rp 0 (per awal data).
- Penyusutan garis lurus, umur manfaat 4 tahun, tanpa nilai sisa; aset yang dibeli mulai disusutkan bulan berikutnya; dihitung per bulan dari harga perolehan (dibulatkan ke rupiah per bulan). Nilai aset tetap awal yang Anda berikan diperlakukan sebagai harga perolehan per awal data.
- Modal awal dihitung dari (aset awal - utang awal) = Rp 22.400.000.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

---

### Saran tindakan (berdasarkan angka di atas)
1. **Biaya gaji Rp 14.400.000 = 39,8% dari penjualan** (termasuk THR Maret Rp 3.600.000). Gaji + sewa sudah 52% dari penjualan. Rugi Rp 2.026.917 terutama karena biaya tetap lebih besar dari laba kotor. Pertimbangkan menaikkan minimal pesanan atau harga nasi box, atau menambah pesanan rutin (katering harian karyawan paling stabil: Rp 2.100.000 per minggu).
2. **Kas Rp 14,7 juta sebagian besar masih uang KUR** (sisa pokok Rp 22,9 juta). Jangan anggap saldo ini sebagai laba. Sisihkan dana angsuran KUR (± Rp 2,3 juta) tiap bulan.
3. **Prive Rp 5.950.000 dalam 3 bulan** saat usaha rugi. Coba tetapkan "gaji pemilik" tetap per bulan agar modal tidak terus turun.

Mau saya buatkan versi PDF/Word atau laporan per bulan?

## Catatan penguji (uji ulang v1.2.0)
- **Angka diverifikasi independen** (`verif_s1_v110.py`, klasifikasi manual per baris oleh penguji, tanpa kode skill): pendapatan Rp 36.150.000; HPP Rp 11.900.000 (air mineral kini ikut pembelian); penyusutan Rp 952.083; beban keuangan Rp 223.334 (bunga KUR 208.334 + admin bank 15.000); laba **−Rp 2.026.917**; kas Rp 14.691.833; utang KUR Rp 22.916.667 (25 jt − pokok 2.083.333); kasbon Rp 300.000 di aset; total aset = liabilitas + ekuitas = **Rp 37.939.750**. **Semua cocok.**
- Hasil v1.2.0 identik dengan v1.1.0 (penyusutan kini dihitung per bulan dari harga beli: 250.000 + 280.208 + 421.875 = Rp 952.083, sama). Perbaikan v1.1.0 tetap terbukti di data yang sama: angsuran KUR **ditanyakan otomatis** dan `--bunga` memecahnya dengan benar (cacat S1 lama tuntas); kasbon menjadi piutang karyawan; air mineral menjadi pembelian bahan; ringkasan rugi tidak lagi berbunyi "laba −5,9%".
- Status akhir "LENGKAP (dengan asumsi)" karena saldo awal utang bank tidak disebut (asumsi Rp 0, memang benar untuk kasus ini). Label ini lebih jujur daripada "LENGKAP" di v1.0.0.
- Ringan: kalimat "Arus kas usaha ... terendah di Mar 2026 (−Rp 2.533.084)" ikut menghitung bunga KUR sebagai arus kas usaha; wajar, tetapi pokok angsuran tidak ikut. Pengguna awam bisa bingung mengapa angka ini tidak sama dengan penurunan kas. Tidak dihitung cacat.
