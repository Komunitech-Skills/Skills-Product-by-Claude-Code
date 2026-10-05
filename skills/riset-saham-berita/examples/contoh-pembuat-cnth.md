# Contoh pembuat skill: catatan riset CNTH (emiten FIKTIF)

> Contoh dari pembuat skill (bukan hasil uji independen). Kode **CNTH**, nama emiten, angka,
> dan berita **fiktif** untuk ilustrasi; tidak merujuk perusahaan tercatat mana pun.

**Input pengguna:**
> Tolong riset CNTH. Ini angka LK semester 1 2026 (dalam jutaan rupiah): pendapatan 4.812.350
> (semester 1 tahun lalu Rp4,5 T), laba bersih 361.200 (tahun lalu 402.900), laba induk 355.480,
> ekuitas 3.950.000, ekuitas induk 3.880.000, liabilitas 2.610.000, utang bank 1.120.000,
> total aset 6.560.000, saham 5,2 miliar lembar. Harga 685 tgl 26/9, dividen tahun buku 2025 Rp24.
> Menurutmu layak beli nggak?

**Yang dilakukan agent:**
1. Menolak bagian "layak beli" dengan templat penolakan, lalu lanjut ke catatan netral.
2. Menulis angka apa adanya ke `contoh-data-emiten.json` (`satuan_laporan: juta`, `periode_bulan: 6`).
3. Menjalankan `python3 <folder-skill>/scripts/rasio_saham.py rasio contoh-data-emiten.json --hari-ini 2026-09-29`.
4. (Dengan akses web) mencari keterbukaan informasi & berita; di contoh fiktif ini diganti tempelan pengguna.

---

Maaf, saya tidak bisa menilai layak beli atau tidak - itu keputusan Anda dan wewenang penasihat
berizin OJK. Berikut catatan riset netral dari angka yang Anda berikan.

# Catatan Riset: CNTH - PT Contoh Pangan Nusantara Tbk (fiktif)
Disusun: 2026-09-29 | Data terbaru yang dipakai: LK 6M2026 (per 2026-06-30), harga per 2026-09-26

## 1. Ringkasan fakta
- Pendapatan semester 1 2026 Rp4,81 T, naik 6,94% dari Rp4,50 T (Sumber: ditempel pengguna, LK 6M2026).
- Laba bersih Rp361,20 M, turun 10,35% dari Rp402,90 M (Sumber: ditempel pengguna, LK 6M2026).
- DER 0,66x; utang berbunga 0,28x ekuitas (Sumber: hitungan script dari angka pengguna).
- Dividen tahun buku 2025 Rp24 per saham (Sumber: ditempel pengguna; tanggal pembayaran perlu dicek).

## 2. Berita & pengumuman terbaru
Tidak dicari di contoh ini (emiten fiktif). Pada pemakaian nyata: maks. 5 berita bertanggal + tautan.

## 3. Aksi korporasi
| Jenis | Tanggal penting | Rincian | Sumber |
|---|---|---|---|
| Dividen tunai TB 2025 | tidak ditemukan / perlu dicek | Rp24/saham | ditempel pengguna |

## 4. Angka laporan keuangan & rasio (keluaran script apa adanya)

Periode: 6M2026 (Jan-Jun) (6 bulan) | Pembanding: 6M2025 | Tanggal laporan: 2026-06-30
Sumber laporan: Tempelan pengguna dari LK interim (fiktif), diakses 2026-09-29 | Harga: Tempelan pengguna (fiktif), per 2026-09-26 | Dihitung: 2026-09-29

#### Angka yang dibaca script (cocokkan dengan sumber)

Satuan laporan: juta

| Pos | Nilai terbaca |
|---|---|
| Pendapatan | Rp4.812.350.000.000 (Rp4,81 T) |
| Pendapatan periode lalu | Rp4.500.000.000.000 (Rp4,50 T) |
| Laba bersih | Rp361.200.000.000 (Rp361,20 M) |
| Laba bersih periode lalu | Rp402.900.000.000 (Rp402,90 M) |
| Laba bersih entitas induk | Rp355.480.000.000 (Rp355,48 M) |
| Total ekuitas | Rp3.950.000.000.000 (Rp3,95 T) |
| Ekuitas entitas induk | Rp3.880.000.000.000 (Rp3,88 T) |
| Total liabilitas | Rp2.610.000.000.000 (Rp2,61 T) |
| Utang berbunga | Rp1.120.000.000.000 (Rp1,12 T) |
| Total aset | Rp6.560.000.000.000 (Rp6,56 T) |
| Saham beredar (lembar) | 5.200.000.000 lembar |
| Harga saham | Rp685 |
| Dividen per saham | Rp24 |

#### Rasio

| Rasio | Nilai | Keterangan |
|---|---|---|
| Pertumbuhan pendapatan | 6,94% | (sekarang - lalu) / abs(lalu) x 100% |
| Pertumbuhan laba bersih | -10,35% | (sekarang - lalu) / abs(lalu) x 100% |
| Margin laba bersih | 7,51% | laba bersih / pendapatan x 100% |
| ROE | 18,32% | entitas induk 6 bulan x 12/6 (disetahunkan sederhana, abaikan musim) / ekuitas entitas induk (akhir periode) x 100% |
| DER (liabilitas/ekuitas) | 0,66x | total liabilitas / total ekuitas |
| DER utang berbunga | 0,28x | utang berbunga / total ekuitas |
| Laba per saham (EPS, setahun) | Rp136,72 | entitas induk 6 bulan x 12/6 (disetahunkan sederhana, abaikan musim) / saham beredar |
| Nilai buku per saham (BVPS) | Rp746,15 | ekuitas entitas induk / saham beredar |
| PER | 5,01x | harga / EPS |
| PBV | 0,92x | harga / BVPS |
| Kapitalisasi pasar | Rp3,56 T | harga x saham beredar |
| Imbal hasil dividen (tahun buku 2025) | 3,50% | DPS / harga x 100% |

#### Fakta yang perlu diketahui
- Laporan interim 6 bulan: ROE, EPS, dan PER memakai laba yang disetahunkan sederhana (x12/6). Hasil bisa meleset bila usaha musiman.
- Imbal hasil dividen memakai dividen yang SUDAH diumumkan/dibayar; dividen tahun berikutnya belum tentu sama.
- Laba bersih turun 10,35% dibanding periode lalu.


## 5. Risiko & hal yang perlu diketahui (fakta)
- Laba bersih turun 10,35% sementara pendapatan naik 6,94% (margin menyempit).
- ROE, EPS, PER memakai laba 6 bulan yang disetahunkan (x2); bila penjualan musiman, angka setahun bisa berbeda.
- Harga per 2026-09-26 (3 hari lalu); PER/PBV/imbal dividen berubah setiap hari bursa.

## 6. Pertanyaan untuk dicari jawabannya sendiri
1. Apa penyebab laba turun saat pendapatan naik? Cek beban pokok penjualan, beban keuangan, dan selisih kurs di catatan LK.
2. Kapan utang bank Rp1,12 T jatuh tempo dan dalam mata uang apa?
3. Apakah arus kas operasi semester 1 sejalan dengan laba bersih?
4. Kapan jadwal cum date & pembayaran dividen TB 2025, dan apakah ada kebijakan dividen tertulis?
5. Apakah ada pengumuman bursa (UMA, suspensi, notasi khusus) dalam 12 bulan terakhir?

## 7. Data yang belum ditemukan / perlu dicek
- Berita & keterbukaan informasi: perlu dicek di idx.co.id dan situs IR emiten.
- Laporan keuangan diaudit / ditelaah terbatas: perlu dicek.
- Laba 12 bulan terakhir (TTM): tidak diisi, sehingga dipakai penyetahunan sederhana.

---
_Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

---

## Verifikasi angka manual (pembuat)
- Laba induk setahun = 355.480 jt x 12/6 = 710.960 jt; EPS = 710,96 M / 5,2 M lembar = Rp136,72
- BVPS = 3.880.000 jt / 5,2 M = Rp746,15; PER = 685/136,7231 = 5,01x; PBV = 685/746,1538 = 0,92x
- ROE = 710.960 / 3.880.000 = 18,32%; DER = 2.610.000 / 3.950.000 = 0,66x
- Imbal dividen = 24/685 = 3,50%; kapitalisasi = 685 x 5,2 M = Rp3,562 T
- Aset 6.560.000 = liabilitas 2.610.000 + ekuitas 3.950.000 (seimbang)
