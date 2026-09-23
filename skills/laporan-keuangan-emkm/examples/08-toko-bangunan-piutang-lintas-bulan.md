# 08 — Toko bangunan, piutang & bon pemasok besar lintas bulan (data baru, v1.2.0)

## Skenario
Skenario normal dengan data baru. Toko bangunan menjual banyak secara tempo ke proyek. Piutang dan bon pemasok tidak tercatat di buku kas saat terjadi, hanya saat dibayar. Pemilik minta laporan per bulan Juli–September. Ini kasus terberat untuk laporan bulanan dari buku kas: tanpa saldo piutang/utang per awal bulan, pendapatan dan HPP pasti salah.

## Input pengguna
> Mas tolong bikinin laporan keuangan per bulan Juli, Agustus, September buat toko bangunanku (Toko Bangunan Fiktif Jaya), file toko-bangunan-q3.csv. Catatan tagihan: piutang pelanggan per 1 Juli 8 juta, akhir Juli 9 juta, akhir Agustus 12 juta, akhir September 2 juta. Bon ke supplier per 1 Juli 5 juta, akhir Juli 8 juta, akhir Agustus 7 juta, akhir September lunas. Stok gudang 1 Juli 20 juta, akhir Juli 22 juta, akhir Agustus 19 juta, akhir September 21 juta.

```csv
Tanggal,Keterangan,Masuk,Keluar
01/07/2026,Saldo awal,"Rp 10.000.000",
02/07/2026,Terima piutang Proyek Ruko A (tagihan Juni),"Rp 6.000.000",
03/07/2026,Penjualan tunai semen & cat,"Rp 4.500.000",
05/07/2026,Bayar supplier semen tagihan Juni,,"Rp 5.000.000"
08/07/2026,Bayar supplier besi,,"Rp 7.000.000"
12/07/2026,Gaji karyawan toko,,"Rp 3.000.000"
15/07/2026,Terima piutang Pak Budi,"Rp 5.000.000",
20/07/2026,Penjualan tunai,"Rp 3.800.000",
25/07/2026,Bayar listrik,,"Rp 600.000"
28/07/2026,Sewa gudang,,"Rp 2.000.000"
30/07/2026,Ambil uang pribadi,,"Rp 1.500.000"
03/08/2026,Terima piutang Proyek Ruko A,"Rp 7.000.000",
05/08/2026,Penjualan tunai,"Rp 5.200.000",
07/08/2026,Bayar supplier besi,,"Rp 10.000.000"
12/08/2026,Gaji karyawan toko,,"Rp 3.000.000"
20/08/2026,Penjualan tunai,"Rp 4.100.000",
25/08/2026,Bayar listrik,,"Rp 650.000"
28/08/2026,Sewa gudang,,"Rp 2.000.000"
30/08/2026,Ambil uang pribadi,,"Rp 1.500.000"
02/09/2026,Terima piutang Proyek Ruko A,"Rp 10.000.000",
05/09/2026,Penjualan tunai,"Rp 4.000.000",
08/09/2026,Bayar supplier semen,,"Rp 13.000.000"
10/09/2026,Terima piutang Pak Budi,"Rp 5.000.000",
12/09/2026,Gaji karyawan toko,,"Rp 3.000.000"
25/09/2026,Bayar listrik,,"Rp 620.000"
28/09/2026,Sewa gudang,,"Rp 2.000.000"
30/09/2026,Ambil uang pribadi,,"Rp 1.500.000"
```

## Output

### Langkah agent
Semua saldo per awal & akhir bulan sudah diberikan, jadi tidak perlu bertanya. Untuk Agustus:
```bash
python3 scripts/laporan_emkm.py toko-bangunan-q3.csv --nama-usaha "Toko Bangunan Fiktif Jaya" \
  --periode-awal 2026-08-01 --periode-akhir 2026-08-31 --persediaan-awal 22jt --persediaan-akhir 19jt \
  --piutang-awal 8jt --utang-usaha-awal 5jt --piutang-awal-periode 9jt --utang-usaha-awal-periode 8jt \
  --piutang-akhir 12jt --utang-usaha-akhir 7jt
```

### Contoh hasil: laporan Agustus 2026

# Laporan Keuangan Toko Bangunan Fiktif Jaya
Periode 1 Agustus 2026 s.d. 31 Agustus 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP (dengan asumsi)**

## Ringkasan untuk pemilik
Usaha kamu UNTUNG Rp 1.650.000 selama 1 Agustus 2026 s.d. 31 Agustus 2026. Dari penjualan bersih Rp 19.300.000, yang tersisa jadi laba sekitar 8,5% (setiap Rp 100.000 penjualan, labanya sekitar Rp 8.549). Pengeluaran terbesar: pembelian bahan/barang dagangan sebesar Rp 9.000.000 (61,4% dari total biaya). Kamu mengambil Rp 1.500.000 untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi mengurangi modal usaha. Uang kas di akhir periode: Rp 9.350.000.

## 1. Laporan Laba Rugi
Toko Bangunan Fiktif Jaya — untuk periode 1 Agustus 2026 s.d. 31 Agustus 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan tunai/transfer | Rp 9.300.000 |
| Penjualan tempo (piutang) | Rp 10.000.000 |
| Penjualan / pendapatan usaha | Rp 19.300.000 |
| **Pendapatan usaha bersih** | **Rp 19.300.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 22.000.000 |
| Pembelian bahan/barang dagangan | Rp 9.000.000 |
| Persediaan akhir | (Rp 19.000.000) |
| Beban pokok penjualan | (Rp 12.000.000) |
| **Laba kotor** | **Rp 7.300.000** |
| **Beban usaha** |  |
| Beban gaji & upah | Rp 3.000.000 |
| Beban sewa tempat | Rp 2.000.000 |
| Beban listrik, air, gas & internet | Rp 650.000 |
| Total beban usaha | (Rp 5.650.000) |
| **Laba (rugi) usaha** | **Rp 1.650.000** |
| **Laba (rugi) sebelum pajak** | **Rp 1.650.000** |
| Beban pajak penghasilan | Rp 0 |
| **LABA (RUGI) BERSIH** | **Rp 1.650.000** |

## 2. Laporan Posisi Keuangan (Neraca)
Toko Bangunan Fiktif Jaya — per 31 Agustus 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas dan setara kas | Rp 9.350.000 |
| Piutang usaha | Rp 12.000.000 |
| Persediaan | Rp 19.000.000 |
| Aset tetap (nilai buku) | Rp 0 |
| **Total aset** | **Rp 40.350.000** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 7.000.000 |
| Utang bank / pinjaman | Rp 0 |
| Total liabilitas | Rp 7.000.000 |
| **EKUITAS** |  |
| Modal awal | Rp 33.200.000 |
| Laba (rugi) bersih periode ini | Rp 1.650.000 |
| Prive (pengambilan pribadi) | (Rp 1.500.000) |
| Modal akhir | Rp 33.350.000 |
| **Total liabilitas + ekuitas** | **Rp 40.350.000** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 40.350.000). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Toko Bangunan Fiktif Jaya adalah usaha yang laporan keuangannya disusun untuk periode 1 Agustus 2026 s.d. 31 Agustus 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 9.350.000 (saldo awal Rp 10.200.000, total uang masuk Rp 16.300.000, total uang keluar Rp 17.150.000).

**4. Piutang usaha** Rp 12.000.000 (awal Rp 9.000.000). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 19.000.000 (awal Rp 22.000.000). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 12.000.000.

**6. Aset tetap** nilai buku Rp 0 (awal Rp 0, pembelian periode ini Rp 0, penyusutan periode ini Rp 0). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 7.000.000 dan utang bank/pinjaman Rp 0 (pinjaman diterima Rp 0, pembayaran pokok Rp 0).

**8. Ekuitas.** Modal awal Rp 33.200.000 + tambahan modal Rp 0 + laba bersih Rp 1.650.000 - prive Rp 1.500.000 = modal akhir Rp 33.350.000.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 19.300.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 5.650.000, beban keuangan Rp 0, beban pajak penghasilan Rp 0. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Perlu dicek
**Baris yang sengaja dilewati:** baris saldo awal (dipakai sebagai kas awal bila --kas-awal tidak diisi) (1 baris)

**Peringatan:**
- 8 transaksi setelah 31 Agustus 2026 tidak dihitung.

## Asumsi yang dipakai
- Kas awal diambil dari baris 'saldo awal' di file: Rp 10.000.000.
- Saldo awal aset tetap tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal utang bank/pinjaman tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal yang Anda berikan/dibaca dari file dianggap per awal data (1 Juli 2026), lalu digulirkan dengan 10 transaksi sebelum 1 Agustus 2026. Kas awal periode = Rp 10.200.000; modal awal periode sudah termasuk laba/prive sebelum periode. Stok awal (--persediaan-awal) dipakai sebagai stok per 1 Agustus 2026.
- Modal awal dihitung dari (aset awal - utang awal) = Rp 33.200.000.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

### Rekap tiga bulan vs verifikasi independen (`verif_toko.py`)
| Bulan | Pendapatan (tunai + tempo) | HPP | Laba | Kas | Piutang | Bon pemasok | Modal awal → akhir | Hasil |
|---|---:|---:|---:|---:|---:|---:|---|---|
| Juli | 20.300.000 | 13.000.000 | 1.700.000 | 10.200.000 | 9.000.000 | 8.000.000 | 33.000.000 → 33.200.000 | 9 pos cocok ✔, seimbang |
| Agustus | 19.300.000 | 12.000.000 | 1.650.000 | 9.350.000 | 12.000.000 | 7.000.000 | 33.200.000 → 33.350.000 | 9 pos cocok ✔, modal bersambung |
| September | 9.000.000 | 4.000.000 | −620.000 | 8.230.000 | 2.000.000 | 0 | 33.350.000 → 31.230.000 | 9 pos cocok ✔, modal bersambung |
| Jul–Sep (1 laporan) | | | **2.730.000** = Σ bulanan ✔ | | | | 33.000.000 → 31.230.000 | cocok ✔ |

### Saran tindakan
1. Piutang naik dari Rp 8 juta ke Rp 12 juta di akhir Agustus, lebih besar dari penjualan tunai sebulan (Rp 9,3 juta). Tagih proyek sebelum memberi tempo baru.
2. September rugi Rp 620.000 karena penjualan tempo baru sedikit, sementara gaji & sewa tetap. Kas masih aman berkat pelunasan piutang Rp 15 juta.

## Catatan penguji
- Verifikasi independen per bulan: pendapatan = tunai + (piutang akhir − piutang awal + pelunasan); pembelian = bon akhir − bon awal + pembayaran; HPP = stok awal + pembelian − stok akhir. Semua pos cocok di tiga bulan, dan laporan triwulan = Σ laporan bulanan.
- Diuji juga dengan `--saldo-awal-per awal-periode --piutang-awal <per awal bulan> --utang-usaha-awal <per awal bulan>`: hasil identik (pos yang diisi dipakai, kas tetap digulir dari baris saldo awal).
- Bila agent lupa `--piutang-awal-periode`, Agustus menjadi laba 2.650.000 (salah) tetapi **SEMENTARA** dengan 2 pertanyaan eksplisit (piutang & bon per 1 Agustus). Aman.
