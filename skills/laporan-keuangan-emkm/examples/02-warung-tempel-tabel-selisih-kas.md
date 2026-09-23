# 02 — Warung sembako, tabel ditempel di chat, uang laci kurang Rp 150.000

## Skenario
S2, permintaan normal dari pengguna awam. Tabel ditempel langsung di chat (format Markdown, tanggal "1 Agt 2026"). Pengguna memberi kas awal, stok awal/akhir, dan uang nyata di laci. Uang nyata di laci ternyata kurang dari hitungan buku.

## Input pengguna
> tolong dong hitungin aku untung berapa bulan agustus kemarin. awal bulan uang di laci 2 juta, stok barang awal bulan kira2 3,5jt, sisa stok akhir bulan 3jt. uang di laci skrg 7.650.000. ini catetanku:
>
> | Tgl | Keterangan | Masuk | Keluar |
> |---|---|---|---|
> | 1 Agt 2026 | Kulakan sembako di agen | | Rp 2.450.000 |
> | 3 Agt 2026 | Hasil jualan minggu 1 | Rp 3.200.000 | |
> | 5 Agt 2026 | Bayar listrik | | Rp 185.000 |
> | 7 Agt 2026 | Ambil buat jajan anak | | Rp 150.000 |
> | 10 Agt 2026 | Hasil jualan minggu 2 | Rp 2.950.000 | |
> | 11 Agt 2026 | Kulakan rokok & minuman | | Rp 1.800.000 |
> | 14 Agt 2026 | Beli plastik kresek | | Rp 45.000 |
> | 17 Agt 2026 | Hasil jualan minggu 3 | Rp 3.400.000 | |
> | 18 Agt 2026 | Kulakan gas melon 20 tabung | | Rp 400.000 |
> | 20 Agt 2026 | Iuran kebersihan pasar | | Rp 20.000 |
> | 22 Agt 2026 | Bayar arisan | | Rp 200.000 |
> | 24 Agt 2026 | Hasil jualan minggu 4 | Rp 3.050.000 | |
> | 25 Agt 2026 | Kulakan sembako di agen | | Rp 2.300.000 |
> | 28 Agt 2026 | Bayar sewa kios | | Rp 750.000 |
> | 30 Agt 2026 | Belanja dapur rumah | | Rp 600.000 |
> | 31 Agt 2026 | Hasil jualan 25-31 | Rp 2.100.000 | |

## Output

### Langkah agent
1. Tabel disimpan apa adanya ke `s2-tempel.md`, lalu:
   `python3 scripts/laporan_emkm.py s2-tempel.md --nama-usaha "Warung Bu Tini" --kas-awal "2 juta" --persediaan-awal "3,5jt" --persediaan-akhir "3 juta" --kas-akhir-aktual "Rp 7.650.000"`
2. Ada 2 transaksi belum jelas. Agent bertanya sekali:

> Sebelum saya finalkan, 2 catatan ini untuk usaha atau keperluan pribadi?
> 1. 22 Agt, **Bayar arisan** Rp 200.000: a) arisan pribadi/keluarga (prive) · b) arisan pedagang pasar untuk modal usaha
> 2. 30 Agt, **Belanja dapur rumah** Rp 600.000: a) kebutuhan rumah (prive) · b) barang untuk dijual di warung
>
> Satu lagi: uang di laci Rp 7.650.000, tapi menurut catatan seharusnya Rp 7.800.000 (kurang Rp 150.000). Apakah ada pengeluaran/pengambilan yang belum dicatat?

**Jawaban pengguna:** "dua2nya pribadi. yg kurang 150rb aku gatau, mungkin kembalian salah."

3. Script dijalankan ulang dengan `--tetapkan 13=prive --tetapkan 17=prive`. Hasil:

---

# Laporan Keuangan Warung Bu Tini
Periode 1 Agustus 2026 s.d. 31 Agustus 2026 · disusun mengacu pada SAK EMKM · status: **SEMENTARA**

## Ringkasan untuk pemilik
Usaha kamu UNTUNG Rp 6.250.000 selama 1 Agustus 2026 s.d. 31 Agustus 2026. Dari penjualan bersih Rp 14.700.000, yang tersisa jadi laba sekitar 42,5% (setiap Rp 100.000 penjualan, labanya sekitar Rp 42.517). Pengeluaran terbesar: pembelian bahan/barang dagangan sebesar Rp 6.570.000 (82,6% dari total biaya). Kamu mengambil Rp 950.000 untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi mengurangi modal usaha. Uang kas di akhir periode: Rp 7.650.000.

## 1. Laporan Laba Rugi
Warung Bu Tini — untuk periode 1 Agustus 2026 s.d. 31 Agustus 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan / pendapatan usaha | Rp 14.700.000 |
| **Pendapatan usaha bersih** | **Rp 14.700.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 3.500.000 |
| Pembelian bahan/barang dagangan | Rp 6.570.000 |
| Persediaan akhir | (Rp 3.000.000) |
| Beban pokok penjualan | (Rp 7.070.000) |
| **Laba kotor** | **Rp 7.630.000** |
| **Beban usaha** |  |
| Beban sewa tempat | Rp 750.000 |
| Beban listrik, air, gas & internet | Rp 585.000 |
| Beban kemasan & perlengkapan | Rp 45.000 |
| Total beban usaha | (Rp 1.380.000) |
| **Laba (rugi) usaha** | **Rp 6.250.000** |
| **Laba (rugi) sebelum pajak** | **Rp 6.250.000** |
| Beban pajak penghasilan | Rp 0 |
| **LABA (RUGI) BERSIH** | **Rp 6.250.000** |

## 2. Laporan Posisi Keuangan (Neraca)
Warung Bu Tini — per 31 Agustus 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas dan setara kas | Rp 7.650.000 |
| Piutang usaha | Rp 0 |
| Persediaan | Rp 3.000.000 |
| Aset tetap (nilai buku) | Rp 0 |
| **Total aset** | **Rp 10.650.000** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 0 |
| Utang bank / pinjaman | Rp 0 |
| Total liabilitas | Rp 0 |
| **EKUITAS** |  |
| Modal awal | Rp 5.500.000 |
| Laba (rugi) bersih periode ini | Rp 6.250.000 |
| Prive (pengambilan pribadi) | (Rp 950.000) |
| Modal akhir | Rp 10.800.000 |
| **Total liabilitas + ekuitas** | **Rp 10.800.000** |

✘ **Cek keseimbangan: TIDAK SEIMBANG.** Selisih -Rp 150.000 (aset Rp 10.650.000 vs liabilitas + ekuitas Rp 10.800.000).
- Saldo kas nyata (Rp 7.650.000) berbeda -Rp 150.000 dari hasil hitung buku kas (Rp 7.800.000). Kemungkinan ada transaksi yang belum dicatat, salah ketik nominal, atau kas awal kurang tepat.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Warung Bu Tini adalah usaha yang laporan keuangannya disusun untuk periode 1 Agustus 2026 s.d. 31 Agustus 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 7.650.000 (saldo awal Rp 2.000.000, total uang masuk Rp 14.700.000, total uang keluar Rp 8.900.000).

**4. Piutang usaha** Rp 0 (awal Rp 0). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 3.000.000 (awal Rp 3.500.000). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 7.070.000.

**6. Aset tetap** nilai buku Rp 0 (awal Rp 0, pembelian periode ini Rp 0, penyusutan periode ini Rp 0). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 0 dan utang bank/pinjaman Rp 0 (pinjaman diterima Rp 0, pembayaran pokok Rp 0).

**8. Ekuitas.** Modal awal Rp 5.500.000 + tambahan modal Rp 0 + laba bersih Rp 6.250.000 - prive Rp 950.000 = modal akhir Rp 10.800.000.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 14.700.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 1.380.000, beban keuangan Rp 0, beban pajak penghasilan Rp 0. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Tren per periode (arus kas usaha, sebelum penyesuaian stok/piutang/penyusutan)

| Periode | Uang masuk usaha | Uang keluar usaha | Selisih | Prive |
|---|---:|---:|---:|---:|
| Agu 2026 | Rp 14.700.000 | Rp 7.950.000 | Rp 6.750.000 | Rp 950.000 |

## Perlu dicek
**Peringatan:**
- Saldo kas sempat minus (-Rp 450.000 pada 1 Agustus 2026). Biasanya karena kas awal belum diisi atau ada pemasukan yang belum dicatat.

## Asumsi yang dipakai
- Periode laporan dianggap 1 Agustus 2026 s.d. 31 Agustus 2026 (bulan penuh dari transaksi pertama sampai terakhir).
- Saldo awal piutang tidak diberikan, dianggap Rp 0.
- Saldo awal aset tetap tidak diberikan, dianggap Rp 0.
- Saldo awal utang ke pemasok tidak diberikan, dianggap Rp 0.
- Saldo awal utang bank/pinjaman tidak diberikan, dianggap Rp 0.
- Modal awal dihitung dari (aset awal - utang awal) = Rp 5.500.000.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

---

### Penjelasan neraca belum seimbang
Neraca selisih **Rp 150.000** karena uang di laci (Rp 7.650.000) lebih kecil dari hitungan buku kas (Rp 7.800.000). Saya tidak memaksa angkanya seimbang. Kalau memang tidak ketemu, selisih ini bisa dicatat sebagai "selisih kas (kurang)" di beban lain-lain dengan menambah satu baris di catatan, lalu laporan saya hitung ulang. Mau saya tambahkan?

### Saran tindakan
1. Laba bersih **Rp 6.250.000** (42,5% dari penjualan). Kamu mengambil Rp 950.000 untuk pribadi, jadi sebagian besar laba masih ada di usaha (stok + kas).
2. Pembelian barang Rp 6.570.000 = 82,6% dari semua pengeluaran usaha. Stok turun Rp 500.000 dari awal bulan. Kalau mau stok tetap, kulakan bulan depan perlu sedikit lebih besar.
3. Pisahkan uang laci untuk pribadi (arisan, belanja dapur) supaya selisih kas lebih mudah dilacak. Catat setiap pengambilan walau kecil.

Mau dibuatkan versi PDF, atau saya catat selisih Rp 150.000 sebagai beban supaya neraca seimbang?

## Catatan penguji
- Verifikasi independen (hitung manual, klasifikasi penguji): penjualan 3,2+2,95+3,4+3,05+2,1 = Rp 14.700.000; HPP = 3.500.000 + 6.950.000 (kulakan sembako, rokok, gas) − 3.000.000 = Rp 7.450.000; beban = sewa 750.000 + listrik 185.000 + kresek 45.000 + iuran 20.000 = Rp 1.000.000; laba = **Rp 6.250.000 ✔** (total sama dengan script, tetapi pos HPP/beban berbeda, lihat di bawah). Aset Rp 10.650.000 vs L+E Rp 10.800.000 → selisih −Rp 150.000 ✔.
- Bagus: tabel tempel Markdown & tanggal "1 Agt 2026" terbaca; "Ambil buat jajan anak" otomatis prive; kas nyata dipakai di neraca dan selisihnya **dijelaskan, tidak dipaksa seimbang**; peringatan "saldo kas sempat minus" (kulakan Rp 2,45 jt saat kas Rp 2 jt) relevan.
- **Salah klasifikasi (sedang):** "Kulakan gas melon 20 tabung" (barang dagangan warung) masuk **Beban listrik, air, gas** karena aturan `gas` (utilitas) dicek sebelum `kulakan` (pembelian). "Iuran kebersihan pasar" Rp 20.000 masuk **Pembelian bahan** karena kata `pasar`. Laba bersih tetap benar, tetapi HPP, laba kotor, dan rincian beban salah. Pembeli warung sangat sering kulakan gas/air galon.
- **Kurang (sedang):** tidak ada cara resmi mencatat selisih kas. Laporan tertahan di status SEMENTARA/TIDAK SEIMBANG, padahal selisih kas kecil sangat umum di warung. Agent harus mengarang langkah sendiri (menambah baris).
- Ringan: "Belanja dapur rumah" tidak dikenali sebagai prive (kata kunci hanya "belanja rumah"). Tetap ditanyakan, jadi aman.
- Ringan: bagian "Tren per periode" tetap muncul walau hanya 1 bulan (SKILL.md: "jika > 1 bulan").
