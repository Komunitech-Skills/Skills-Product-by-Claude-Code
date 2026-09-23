# 03 — "Bikinin dong", jualan sambal online, format Jumlah + Jenis, untuk KUR — diuji ulang dengan v1.1.0

## Skenario
S3, permintaan singkat/malas. Pengguna hanya melampirkan file dan minta cepat. Formatnya berbeda: kolom `Uraian, Jenis (Masuk/Keluar), Nominal`. Ada "cicilan motor" (bisa pribadi atau usaha), "transfer ke rekening pribadi", pembelian blender, dan botol kaca yang tidak dikenali.

## Input pengguna
> bikinin laporan keuangan buat ngajuin KUR dong, filenya kas-sambal.csv. langsung aja ya ga usah ribet

Isi `kas-sambal.csv` (fiktif):
```csv
Tanggal,Uraian,Jenis,Nominal
2026-07-01,Modal awal dari tabungan pribadi,Masuk,"Rp 5.000.000"
2026-07-02,Beli cabai rawit 10 kg,Keluar,"Rp 650.000"
2026-07-02,Beli bawang merah & putih,Keluar,"Rp 380.000"
2026-07-03,Beli botol kaca 200 pcs,Keluar,"Rp 700.000"
2026-07-05,Pencairan dana Shopee,Masuk,"Rp 2.340.000"
2026-07-06,Minyak goreng 10 liter,Keluar,"Rp 180.000"
2026-07-08,Iklan Shopee,Keluar,"Rp 150.000"
2026-07-12,Pencairan dana Shopee,Masuk,"Rp 2.880.000"
2026-07-14,Ongkir kirim ke reseller,Keluar,"Rp 95.000"
2026-07-15,Orderan reseller Bandung,Masuk,"Rp 1.500.000"
2026-07-18,Beli cabai rawit 10 kg,Keluar,"Rp 700.000"
2026-07-20,Cicilan motor,Keluar,"Rp 850.000"
2026-07-25,Pencairan dana Shopee,Masuk,"Rp 3.120.000"
2026-07-28,Transfer ke rekening pribadi,Keluar,"Rp 1.000.000"
2026-08-02,Beli cabai & bawang,Keluar,"Rp 1.150.000"
2026-08-04,Beli botol kaca 300 pcs,Keluar,"Rp 1.050.000"
2026-08-06,Pencairan dana Shopee,Masuk,"Rp 3.450.000"
2026-08-10,Beli blender besar,Keluar,"Rp 1.200.000"
2026-08-15,Orderan reseller Bandung,Masuk,"Rp 1.800.000"
2026-08-18,Iklan Shopee,Keluar,"Rp 200.000"
2026-08-20,Cicilan motor,Keluar,"Rp 850.000"
2026-08-24,Pencairan dana Shopee,Masuk,"Rp 3.600.000"
2026-08-30,Paket data HP,Keluar,"Rp 100.000"
```

## Output

### Langkah agent (script v1.1.0)
Pengguna minta "langsung aja", jadi script dijalankan dengan default (`python3 scripts/laporan_emkm.py kas-sambal.csv`) dan asumsinya ditampilkan. Botol kaca kini otomatis dikenali sebagai kemasan. Hasil pertama berstatus **SEMENTARA** dengan tanda ⚠: script menemukan angka mustahil **utang bank akhir −Rp 1.700.000** (karena "Cicilan motor" dianggap angsuran pinjaman padahal tidak ada pinjaman tercatat) dan menanyakan porsi bunga kedua cicilan. Agent mengirim satu pesan:

> Draf laporan sudah jadi (Juli–Agustus 2026), tapi masih SEMENTARA. Dua hal singkat biar angkanya benar:
> 1. **Cicilan motor** Rp 850.000 × 2: motor pribadi (prive) atau motor usaha yang dibeli kredit? Kalau motor usaha, sebutkan sisa utang leasing per 1 Juli dan berapa bunga per cicilan.
> 2. Opsional tapi penting untuk bank: nama usaha, dan kira-kira nilai stok cabai/botol yang tersisa per 31 Agustus. Tanpa stok akhir, laba bisa terlihat terlalu besar.

**Jawaban pengguna:** "motor itu motor pribadi. stok gatau, pake aja yg ada."

Script dijalankan ulang dengan `--tetapkan 13=prive --tetapkan 22=prive`:

---

# Laporan Keuangan [Nama Usaha]
Periode 1 Juli 2026 s.d. 31 Agustus 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP (dengan asumsi)**

## Ringkasan untuk pemilik
Usaha kamu UNTUNG Rp 13.335.000 selama 1 Juli 2026 s.d. 31 Agustus 2026. Dari penjualan bersih Rp 18.690.000, yang tersisa jadi laba sekitar 71,3% (setiap Rp 100.000 penjualan, labanya sekitar Rp 71.348). Pengeluaran terbesar: pembelian bahan/barang dagangan sebesar Rp 3.060.000 (57,1% dari total biaya). Arus kas usaha terbaik di Jul 2026 (Rp 6.985.000), terendah di Agu 2026 (Rp 6.350.000). Kamu mengambil Rp 2.700.000 untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi mengurangi modal usaha. Uang kas di akhir periode: Rp 14.435.000.

## 1. Laporan Laba Rugi
[Nama Usaha] — untuk periode 1 Juli 2026 s.d. 31 Agustus 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan / pendapatan usaha | Rp 18.690.000 |
| **Pendapatan usaha bersih** | **Rp 18.690.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 0 |
| Pembelian bahan/barang dagangan | Rp 3.060.000 |
| Persediaan akhir | Rp 0 |
| Beban pokok penjualan | (Rp 3.060.000) |
| **Laba kotor** | **Rp 15.630.000** |
| **Beban usaha** |  |
| Beban listrik, air, gas & internet | Rp 100.000 |
| Beban transportasi & pengiriman | Rp 95.000 |
| Beban iklan & promosi | Rp 350.000 |
| Beban kemasan & perlengkapan | Rp 1.750.000 |
| Total beban usaha | (Rp 2.295.000) |
| **Laba (rugi) usaha** | **Rp 13.335.000** |
| **Laba (rugi) sebelum pajak** | **Rp 13.335.000** |
| Beban pajak penghasilan | Rp 0 |
| **LABA (RUGI) BERSIH** | **Rp 13.335.000** |

## 2. Laporan Posisi Keuangan (Neraca)
[Nama Usaha] — per 31 Agustus 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas dan setara kas | Rp 14.435.000 |
| Piutang usaha | Rp 0 |
| Persediaan | Rp 0 |
| Aset tetap (awal + pembelian Rp 1.200.000) | Rp 1.200.000 |
| Penyusutan periode ini | Rp 0 |
| Aset tetap (nilai buku) | Rp 1.200.000 |
| **Total aset** | **Rp 15.635.000** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 0 |
| Utang bank / pinjaman | Rp 0 |
| Total liabilitas | Rp 0 |
| **EKUITAS** |  |
| Modal awal | Rp 0 |
| Tambahan modal | Rp 5.000.000 |
| Laba (rugi) bersih periode ini | Rp 13.335.000 |
| Prive (pengambilan pribadi) | (Rp 2.700.000) |
| Modal akhir | Rp 15.635.000 |
| **Total liabilitas + ekuitas** | **Rp 15.635.000** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 15.635.000). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** [Nama Usaha] adalah usaha yang laporan keuangannya disusun untuk periode 1 Juli 2026 s.d. 31 Agustus 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 14.435.000 (saldo awal Rp 0, total uang masuk Rp 23.690.000, total uang keluar Rp 9.255.000).

**4. Piutang usaha** Rp 0 (awal Rp 0). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 0 (awal Rp 0). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 3.060.000.

**6. Aset tetap** nilai buku Rp 1.200.000 (awal Rp 0, pembelian periode ini Rp 1.200.000, penyusutan periode ini Rp 0). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 0 dan utang bank/pinjaman Rp 0 (pinjaman diterima Rp 0, pembayaran pokok Rp 0).

**8. Ekuitas.** Modal awal Rp 0 + tambahan modal Rp 5.000.000 + laba bersih Rp 13.335.000 - prive Rp 2.700.000 = modal akhir Rp 15.635.000.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 18.690.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 2.295.000, beban keuangan Rp 0, beban pajak penghasilan Rp 0. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Tren per periode (arus kas usaha, sebelum penyesuaian stok/piutang/penyusutan)

| Periode | Uang masuk usaha | Uang keluar usaha | Selisih | Prive |
|---|---:|---:|---:|---:|
| Jul 2026 | Rp 9.840.000 | Rp 2.855.000 | Rp 6.985.000 | Rp 1.850.000 |
| Agu 2026 | Rp 8.850.000 | Rp 2.500.000 | Rp 6.350.000 | Rp 850.000 |

## Asumsi yang dipakai
- Periode laporan dianggap 1 Juli 2026 s.d. 31 Agustus 2026 (bulan penuh dari transaksi pertama sampai terakhir).
- Kas awal tidak diberikan, dianggap Rp 0.
- Saldo awal piutang tidak diberikan, dianggap Rp 0.
- Saldo awal persediaan (stok) tidak diberikan, dianggap Rp 0.
- Saldo awal aset tetap tidak diberikan, dianggap Rp 0.
- Saldo awal utang ke pemasok tidak diberikan, dianggap Rp 0.
- Saldo awal utang bank/pinjaman tidak diberikan, dianggap Rp 0.
- Stok akhir tidak diberikan: dianggap sama dengan stok awal (Rp 0), sehingga beban pokok penjualan = total pembelian bahan/barang. Isi --persediaan-akhir dari hasil hitung stok agar laba lebih akurat.
- Penyusutan aset tetap BELUM dihitung (tidak ada --penyusutan / --umur-aset-tahun). Laba bisa sedikit lebih tinggi dari seharusnya.
- Modal awal dihitung dari (aset awal - utang awal) = Rp 0.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

---

### Catatan untuk pengajuan KUR
- Nama usaha masih `[Nama Usaha]` dan stok akhir dianggap Rp 0. Bank biasanya menanyakan omzet rata-rata per bulan (di sini ±Rp 9,3 juta) dan bukti mutasi rekening. Isi nama usaha dan perkiraan stok supaya laporan lebih meyakinkan.
- Laporan ini bukan laporan audit. Untuk syarat dan dokumen KUR, tanyakan ke bank penyalur.

### Saran tindakan
1. Margin laba **71,3%** tampak sangat tinggi karena stok akhir dianggap nol dan penyusutan blender belum dihitung. Hitung sisa stok (cabai, bawang, botol) di akhir bulan agar angka lebih realistis.
2. Cicilan motor pribadi Rp 850.000/bulan dibayar dari uang usaha. Sebaiknya dibayar dari "gaji pemilik" tetap supaya uang usaha tidak tercampur.
3. Pencairan Shopee dicatat bersih (setelah potongan admin). Kalau ingin omzet kotor dan biaya admin terlihat, catat keduanya terpisah.

Mau saya buatkan versi PDF, atau jalankan ulang setelah nama usaha & stok akhir diisi?

## Catatan penguji (uji ulang v1.1.0)
- Verifikasi independen: penjualan Rp 18.690.000; bahan Rp 3.060.000; kemasan (botol) Rp 1.750.000; iklan 350.000; ongkir 95.000; paket data 100.000 → laba **Rp 13.335.000 ✔**; kas = 5.000.000 + 18.690.000 − 9.255.000 = **Rp 14.435.000 ✔**; aset Rp 15.635.000 = modal akhir Rp 15.635.000 ✔. Angka identik dengan v1.0.0 (tidak ada regresi).
- **Cacat S3 lama tuntas:** utang bank negatif sekarang membuat status SEMENTARA, cek keseimbangan memakai ⚠ (bukan ✔), dan menjadi pertanyaan wajib. Laporan dengan liabilitas negatif tidak bisa lagi terkirim sebagai "LENGKAP".
- Bagus: "botol" kini dikenali sebagai kemasan; label akhir "LENGKAP (dengan asumsi)" jujur karena stok akhir & penyusutan memakai default.
- Ringan: pertanyaan otomatis "berapa bagian bunga" untuk cicilan motor muncul bersamaan dengan pertanyaan "utang negatif". Agent perlu merangkum keduanya menjadi satu pertanyaan (pribadi atau usaha) agar tidak membingungkan pengguna awam.
