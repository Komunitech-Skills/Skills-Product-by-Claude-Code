# 07 — Warung makan: kulakan gas, air mineral, iuran pasar, PB1, dan "(200.000)" di kolom Keluar (uji S2 & S5, diuji ulang dengan v1.2.0)

## Skenario
Uji ulang klasifikasi yang dulu salah (S2) dan nominal dalam kurung/minus di kolom Keluar (S5), dengan buku kas warung makan fiktif. Isinya kulakan gas untuk dijual, air mineral untuk dijual, gas untuk masak, air PDAM, iuran kebersihan pasar, setoran PB1, `(200.000)` dan `-150.000` di kolom Keluar, serta `(50.000)` di kolom Masuk.

## Input pengguna
> tolong itungin untung warung makanku bulan juli ya, sisa bahan di kulkas akhir bulan kira2 300rb. file: warung-makan.csv

```csv
Tanggal,Keterangan,Masuk,Keluar
01/07/2026,Saldo awal,"Rp 3.000.000",
02/07/2026,Belanja bahan masak,,"Rp 1.200.000"
02/07/2026,Beli air mineral gelas 5 dus untuk dijual,,"Rp 120.000"
03/07/2026,Kulakan gas melon 10 tabung,,"Rp 200.000"
05/07/2026,Penjualan makan siang minggu 1,"Rp 4.200.000",
08/07/2026,Iuran kebersihan pasar,,"Rp 25.000"
10/07/2026,Bayar pajak restoran PB1 Juni,,"Rp 350.000"
12/07/2026,Penjualan makan siang minggu 2,"Rp 3.900.000",
15/07/2026,Gas elpiji untuk masak,,"Rp 90.000"
20/07/2026,Bayar air PDAM,,"Rp 80.000"
25/07/2026,Beli tepung,,(200.000)
28/07/2026,Beli minyak,,-150.000
30/07/2026,Retur salah input,(50.000),
```

## Output

### Langkah agent
1. `python3 scripts/laporan_emkm.py warung-makan.csv --nama-usaha "Warung Makan Mbak Yuni" --persediaan-awal 0 --persediaan-akhir 300rb`
2. Klasifikasi otomatis: "Beli air mineral gelas ... untuk dijual" dan "Kulakan gas melon" → **pembelian barang dagangan**; "Gas elpiji untuk masak" dan "Bayar air PDAM" → beban utilitas; "Iuran kebersihan pasar" → **beban lain-lain**; "Bayar pajak restoran PB1 Juni" → **beban pajak daerah** (bukan PPh) + pertanyaan otomatis. `(200.000)` dan `-150.000` di kolom Keluar dibaca sebagai **uang keluar** (disebut di Peringatan). `(50.000)` di kolom Masuk tidak dihitung dan ditanyakan. Agent bertanya sekali:

> Dua hal sebelum saya finalkan:
> 1. **PB1 Rp 350.000 (10 Jul):** apakah pajak restoran ini Mbak pungut dari pembeli (harga + 10%)? Kalau ya, uang itu titipan, bukan biaya warung. Kalau tidak dipungut (Mbak tanggung sendiri), saya catat sebagai biaya.
> 2. **Baris 30 Jul "Retur salah input" (50.000) di kolom Masuk:** ini koreksi salah ketik yang bisa dihapus, atau memang ada uang dikembalikan ke pembeli?

**Jawaban pengguna:** "PB1 aku tanggung sendiri, ga dipungut. yang retur itu salah ketik, hapus aja."

3. Baris 30 Juli dihapus dari file (atas persetujuan pengguna), lalu script dijalankan ulang dengan `--tetapkan 8=beban_pajak_lain` (PB1 ditanggung sendiri, jadi beban):

---

# Laporan Keuangan Warung Makan Mbak Yuni
Periode 1 Juli 2026 s.d. 31 Juli 2026 · disusun mengacu pada SAK EMKM · status: **LENGKAP (dengan asumsi)**

## Ringkasan untuk pemilik
Usaha kamu UNTUNG Rp 5.985.000 selama 1 Juli 2026 s.d. 31 Juli 2026. Dari penjualan bersih Rp 8.100.000, yang tersisa jadi laba sekitar 73,9% (setiap Rp 100.000 penjualan, labanya sekitar Rp 73.889). Pengeluaran terbesar: pembelian bahan/barang dagangan sebesar Rp 1.870.000 (77,4% dari total biaya). Uang kas di akhir periode: Rp 8.685.000.

## 1. Laporan Laba Rugi
Warung Makan Mbak Yuni — untuk periode 1 Juli 2026 s.d. 31 Juli 2026

| Pos | Jumlah |
|---|---:|
| **Pendapatan usaha** |  |
| Penjualan / pendapatan usaha | Rp 8.100.000 |
| **Pendapatan usaha bersih** | **Rp 8.100.000** |
| **Beban pokok penjualan** |  |
| Persediaan awal | Rp 0 |
| Pembelian bahan/barang dagangan | Rp 1.870.000 |
| Persediaan akhir | (Rp 300.000) |
| Beban pokok penjualan | (Rp 1.570.000) |
| **Laba kotor** | **Rp 6.530.000** |
| **Beban usaha** |  |
| Beban listrik, air, gas & internet | Rp 170.000 |
| Beban pajak daerah, retribusi & meterai | Rp 350.000 |
| Beban lain-lain | Rp 25.000 |
| Total beban usaha | (Rp 545.000) |
| **Laba (rugi) usaha** | **Rp 5.985.000** |
| **Laba (rugi) sebelum pajak** | **Rp 5.985.000** |
| Beban pajak penghasilan | Rp 0 |
| **LABA (RUGI) BERSIH** | **Rp 5.985.000** |

## 2. Laporan Posisi Keuangan (Neraca)
Warung Makan Mbak Yuni — per 31 Juli 2026

| Pos | Jumlah |
|---|---:|
| **ASET** |  |
| Kas dan setara kas | Rp 8.685.000 |
| Piutang usaha | Rp 0 |
| Persediaan | Rp 300.000 |
| Aset tetap (nilai buku) | Rp 0 |
| **Total aset** | **Rp 8.985.000** |
| **LIABILITAS** |  |
| Utang usaha (ke pemasok) | Rp 0 |
| Utang bank / pinjaman | Rp 0 |
| Total liabilitas | Rp 0 |
| **EKUITAS** |  |
| Modal awal | Rp 3.000.000 |
| Laba (rugi) bersih periode ini | Rp 5.985.000 |
| Prive (pengambilan pribadi) | Rp 0 |
| Modal akhir | Rp 8.985.000 |
| **Total liabilitas + ekuitas** | **Rp 8.985.000** |

✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 8.985.000). Neraca seimbang.

## 3. Catatan atas Laporan Keuangan (ringkas)
**1. Umum.** Warung Makan Mbak Yuni adalah usaha yang laporan keuangannya disusun untuk periode 1 Juli 2026 s.d. 31 Juli 2026. [Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]

**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).

**3. Kas dan setara kas** per akhir periode Rp 8.685.000 (saldo awal Rp 3.000.000, total uang masuk Rp 8.100.000, total uang keluar Rp 2.415.000).

**4. Piutang usaha** Rp 0 (awal Rp 0). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.

**5. Persediaan** Rp 300.000 (awal Rp 0). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan = persediaan awal + pembelian - persediaan akhir = Rp 1.570.000.

**6. Aset tetap** nilai buku Rp 0 (awal Rp 0, pembelian periode ini Rp 0, penyusutan periode ini Rp 0). Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.

**7. Liabilitas.** Utang usaha Rp 0 dan utang bank/pinjaman Rp 0 (pinjaman diterima Rp 0, pembayaran pokok Rp 0).

**8. Ekuitas.** Modal awal Rp 3.000.000 + tambahan modal Rp 0 + laba bersih Rp 5.985.000 - prive Rp 0 = modal akhir Rp 8.985.000.

**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini Rp 8.100.000.

**10. Beban** diakui saat terjadi. Total beban usaha Rp 545.000, beban keuangan Rp 0, beban pajak penghasilan Rp 0. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]


## Perlu dicek
**Baris yang sengaja dilewati:** baris saldo awal (dipakai sebagai kas awal bila --kas-awal tidak diisi) (1 baris)

**Peringatan:**
- 2 nominal minus/dalam kurung di kolom Keluar dibaca sebagai uang keluar.

## Asumsi yang dipakai
- Periode laporan dianggap 1 Juli 2026 s.d. 31 Juli 2026 (bulan penuh dari transaksi pertama sampai terakhir).
- Kas awal diambil dari baris 'saldo awal' di file: Rp 3.000.000.
- Saldo awal piutang tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal aset tetap tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal utang ke pemasok tidak diberikan, dianggap Rp 0 (per awal data).
- Saldo awal utang bank/pinjaman tidak diberikan, dianggap Rp 0 (per awal data).
- Modal awal dihitung dari (aset awal - utang awal) = Rp 3.000.000.

---
_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah terdekat._

---

### Saran tindakan
1. Laba bersih **Rp 5.985.000** dari penjualan Rp 8.100.000 (73,9%). Angka ini tinggi karena gaji/tenaga sendiri dan sewa tempat tidak tercatat. Kalau Mbak menggaji diri sendiri, catat sebagai prive agar laba usaha tetap terlihat jujur.
2. PB1 Rp 350.000 yang Mbak tanggung sendiri memotong laba. Kalau aturan daerah membolehkan, pertimbangkan memungut PB1 dari pembeli.

## Catatan penguji
- **Verifikasi independen:** pembelian 1.200.000 + 120.000 + 200.000 + 200.000 + 150.000 = Rp 1.870.000; HPP = 0 + 1.870.000 − 300.000 = Rp 1.570.000; beban usaha = iuran 25.000 + PB1 350.000 + gas masak 90.000 + PDAM 80.000 = Rp 545.000; laba = 8.100.000 − 1.570.000 − 545.000 = **Rp 5.985.000 ✔**; kas = 3.000.000 + 8.100.000 − 2.415.000 = **Rp 8.685.000 ✔**; aset Rp 8.985.000 = modal 3.000.000 + 5.985.000 ✔.
- **Cacat S2 lama tuntas:** kulakan gas & air mineral = pembelian dagangan; gas masak/PDAM tetap utilitas; iuran kebersihan pasar = beban lain; PB1 = pajak daerah (bukan PPh) dan ditanyakan.
- **Cacat S5 lama tuntas:** `(200.000)` dan `-150.000` di kolom Keluar menjadi uang keluar (v1.0.0 membaliknya menjadi uang masuk). Nilai kurung di kolom Masuk tidak ditebak, tetapi ditanyakan.
- **BS3 (v1.1.0) tuntas di v1.2.0:** `--tetapkan 8=beban_pajak_lain` menutup pertanyaan dan status menjadi **LENGKAP (dengan asumsi)**. Pertanyaan PB1 kini memberi dua pilihan jelas: (a) `titipan_pajak` bila PB1 dicatat terpisah saat dipungut, (b) `beban_pajak_lain` bila sudah ikut penjualan/ditanggung sendiri. Perlakuan titipan diuji di `09-kafe-pb1-titipan-lintas-bulan.md`.
- *(Catatan v1.1.0, kini sudah diperbaiki:)* pertanyaan PB1 dipicu oleh teks keterangan dan **tidak bisa ditutup**. Bahkan `--tetapkan 8=beban_pajak_lain` tetap membuat status SEMENTARA. Untuk rumah makan yang menyetor PB1 setiap bulan, laporan tidak pernah bisa final. Jika PB1 memang dipungut dari pembeli, tidak ada kategori/opsi "titipan pajak" untuk mengoreksinya (penjualan termasuk PB1 → pendapatan terlalu tinggi). *Saran:* lewati pertanyaan bila baris ditetapkan pengguna (`t["sumber"] == "ditetapkan pengguna"`), dan tambahkan kategori dua arah `titipan_pajak` (masuk = PB1 dipungut, keluar = penyetoran) yang hanya mengubah utang pajak di neraca.
