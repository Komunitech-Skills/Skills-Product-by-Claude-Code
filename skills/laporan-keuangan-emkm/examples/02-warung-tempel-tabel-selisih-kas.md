# 02 — Warung sembako, tabel ditempel di chat, uang laci kurang Rp 150.000 — diuji ulang dengan v1.2.0

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

### Langkah agent (script v1.2.0)
1. Tabel disimpan apa adanya ke `s2-tempel.md`, lalu:
   `python3 scripts/laporan_emkm.py s2-tempel.md --nama-usaha "Warung Bu Tini" --kas-awal "2 juta" --persediaan-awal "3,5jt" --persediaan-akhir "3 juta" --kas-akhir-aktual "Rp 7.650.000"`
2. "Kulakan gas melon" kini otomatis masuk pembelian barang dagangan dan "Iuran kebersihan pasar" masuk beban lain-lain. Status SEMENTARA karena 2 transaksi belum jelas, 1 pertanyaan "angka mustahil" (kas sempat minus di 1 Agustus), dan selisih kas laci. Agent bertanya sekali:

> Sebelum saya finalkan, 4 hal singkat:
> 1. 22 Agt, **Bayar arisan** Rp 200.000: a) arisan pribadi/keluarga (prive) · b) arisan pedagang untuk modal usaha
> 2. 30 Agt, **Belanja dapur rumah** Rp 600.000: a) kebutuhan rumah (prive) · b) barang untuk dijual
> 3. Tanggal 1 Agustus kulakan Rp 2.450.000 padahal uang laci awal bulan Rp 2.000.000. Apakah ada uang lain yang dipakai (mis. hasil jualan tanggal 1–2 yang baru dicatat tanggal 3)?
> 4. Uang di laci Rp 7.650.000, tapi menurut catatan seharusnya Rp 7.800.000 (kurang Rp 150.000). Kalau memang tidak ketemu, boleh saya catat sebagai "selisih kas (kurang)"?

**Jawaban pengguna:** "dua2nya pribadi. tgl 1 itu pake uang jualan hari itu, jualan emang aku catet mingguan. yg kurang 150rb gatau, catet aja."

3. Script dijalankan ulang dengan `--tetapkan 13=prive --tetapkan 17=prive --catat-selisih-kas --abaikan-kas-minus`. Hasil:

---

# Laporan Keuangan Warung Bu Tini
Periode 1 Agustus 2026 s.d. 31 Agustus 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP (dengan asumsi)**

## Ringkasan untuk pemilik
Usaha kamu UNTUNG Rp 6.100.000 selama 1 Agustus 2026 s.d. 31 Agustus 2026. Dari penjualan bersih Rp 14.700.000, yang tersisa jadi laba sekitar 41,5% (setiap Rp 100.000 penjualan, labanya sekitar Rp 41.497). Pengeluaran terbesar: pembelian bahan/barang dagangan sebesar Rp 6.950.000 (85,8% dari total biaya). Kamu mengambil Rp 950.000 untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi mengurangi modal usaha. Uang kas di akhir periode: Rp 7.650.000.

## 1. Laporan Laba Rugi
Warung Bu Tini — untuk periode 1 Agustus 2026 s.d. 31 Agustus 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan / pendapatan usaha | Rp 14.700.000 |
| **Pendapatan usaha bersih** | **Rp 14.700.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 3.500.000 |
| Pembelian bahan/barang dagangan | Rp 6.950.000 |
| Persediaan akhir | (Rp 3.000.000) |
| Beban pokok penjualan | (Rp 7.450.000) |
| **Laba kotor** | **Rp 7.250.000** |
| **Beban usaha** |  |
| Beban sewa tempat | Rp 750.000 |
| Beban listrik, air, gas & internet | Rp 185.000 |
| Beban kemasan & perlengkapan | Rp 45.000 |
| Beban lain-lain | Rp 20.000 |
| Selisih kas (kurang), dikonfirmasi pemilik | Rp 150.000 |
| Total beban usaha | (Rp 1.150.000) |
| **Laba (rugi) usaha** | **Rp 6.100.000** |
| **Laba (rugi) sebelum pajak** | **Rp 6.100.000** |
| Beban pajak penghasilan | Rp 0 |
| **LABA (RUGI) BERSIH** | **Rp 6.100.000** |

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
| Laba (rugi) bersih periode ini | Rp 6.100.000 |
| Prive (pengambilan pribadi) | (Rp 950.000) |
| Modal akhir | Rp 10.650.000 |
| **Total liabilitas + ekuitas** | **Rp 10.650.000** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 10.650.000). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Warung Bu Tini adalah usaha yang laporan keuangannya disusun untuk periode 1 Agustus 2026 s.d. 31 Agustus 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 7.650.000 (saldo awal Rp 2.000.000, total uang masuk Rp 14.700.000, total uang keluar Rp 8.900.000).

**4. Piutang usaha** Rp 0 (awal Rp 0). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 3.000.000 (awal Rp 3.500.000). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 7.450.000.

**6. Aset tetap** nilai buku Rp 0 (awal Rp 0, pembelian periode ini Rp 0, penyusutan periode ini Rp 0). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 0 dan utang bank/pinjaman Rp 0 (pinjaman diterima Rp 0, pembayaran pokok Rp 0).

**8. Ekuitas.** Modal awal Rp 5.500.000 + tambahan modal Rp 0 + laba bersih Rp 6.100.000 - prive Rp 950.000 = modal akhir Rp 10.650.000.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 14.700.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 1.150.000, beban keuangan Rp 0, beban pajak penghasilan Rp 0. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Asumsi yang dipakai
- Periode laporan dianggap 1 Agustus 2026 s.d. 31 Agustus 2026 (bulan penuh dari transaksi pertama sampai terakhir).
- Saldo awal piutang tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal aset tetap tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal utang ke pemasok tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal utang bank/pinjaman tidak diberikan, dianggap Rp 0 (per awal data).
- Selisih kas Rp 150.000 dicatat sebagai beban selisih kas (kas kurang) atas konfirmasi pemilik.
- Modal awal dihitung dari (aset awal - utang awal) = Rp 5.500.000.
- Saldo kas sempat minus (-Rp 450.000 pada 1 Agustus 2026) dan pemilik mengonfirmasi ini karena urutan pencatatan (mis. penjualan dicatat mingguan), bukan transaksi yang terlewat.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

---

### Catatan untuk pemilik
Kas sempat tercatat minus Rp 450.000 pada 1 Agustus hanya karena jualan dicatat mingguan (sudah Ibu konfirmasi), jadi ini tidak dianggap kesalahan dan sudah ditulis di bagian Asumsi. Kalau laporan ini mau dipakai untuk bank/koperasi, sebaiknya mulai bulan depan jualan dicatat harian.

### Saran tindakan
1. Laba bersih **Rp 6.100.000** (41,5% dari penjualan). Prive Rp 950.000, jadi sebagian besar laba masih ada di usaha (stok + kas).
2. Pembelian barang Rp 6.950.000, stok turun Rp 500.000. Kalau mau stok tetap, kulakan bulan depan perlu sedikit lebih besar.
3. Pisahkan uang laci untuk pribadi (arisan, belanja dapur) supaya selisih kas lebih mudah dilacak.

Mau dibuatkan versi PDF?

## Catatan penguji (uji ulang v1.2.0)
- Verifikasi independen (hitung manual): penjualan Rp 14.700.000; HPP = 3.500.000 + 6.950.000 (sembako, rokok, **gas melon**) − 3.000.000 = Rp 7.450.000; beban = sewa 750.000 + listrik 185.000 + kresek 45.000 + iuran 20.000 + selisih kas 150.000 = Rp 1.150.000; laba **Rp 6.100.000 ✔**; aset 7.650.000 + 3.000.000 = Rp 10.650.000 = modal 5.500.000 + 6.100.000 − 950.000 ✔.
- Kulakan gas → pembelian barang, iuran kebersihan pasar → beban lain (sejak v1.1.0). `--catat-selisih-kas` membukukan selisih Rp 150.000 sebagai beban; neraca seimbang.
- **BS2 (v1.1.0) tuntas:** `--abaikan-kas-minus` menutup pertanyaan "kas sempat minus" setelah pemilik mengonfirmasi. Konfirmasinya dicatat di Asumsi, dan status menjadi **LENGKAP (dengan asumsi)**. Tanpa opsi ini, laporan tetap SEMENTARA dan ditanyakan (aman).
