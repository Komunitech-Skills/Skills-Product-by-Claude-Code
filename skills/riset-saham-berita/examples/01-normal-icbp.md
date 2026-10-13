# Uji 01 - Skenario normal (emiten nyata, konsumer): ICBP

> Uji independen Tahap 6 (penguji bukan pembuat), 2026-09-29. Penguji berperan sebagai agent
> yang hanya membaca `SKILL.md` + file di folder skill. Data **nyata** dari sumber publik yang
> diambil penguji sendiri (tautan & tanggal di bawah). Model: claude-code (simulasi agent).

**Input pengguna:** "Riset saham ICBP dong, berita & dividen terbaru, sama hitung rasionya."

**Yang dilakukan agent (mengikuti SKILL.md):**
1. Langkah A - urutan sumber `references/sumber-data.md`: idx.co.id dicoba lebih dulu -> **HTTP 403 (blokir bot)**;
   situs IR emiten tidak merespons. Sesuai aturan akses, agent memberi tahu pengguna dan memakai media
   nasional sebagai sumber sekunder, ditandai "bukan dokumen resmi".
2. Berita: semua berita LK semester I terbit 1-14 Agustus 2026 (> 30 hari) -> ditandai "(berita lama)".
3. Sumber bertentangan: total dividen Rp9,22 T (IDX Channel) vs Rp3,09 T (hasil pencarian: Ajaib/PintarSaham/Emitennews).
   Agent menampilkan keduanya (aturan "Sumber saling bertentangan"); cek silang 265 x 11.661.908.000 = Rp3,09 T.
4. Langkah B - angka ditulis apa adanya ke `data/d1_icbp.json`, lalu
   `python3 scripts/rasio_saham.py rasio d1_icbp.json --hari-ini 2026-09-29` (exit 0).
5. Harga terbaru yang bisa diverifikasi hanya Rp7.625 per 18-08-2026 -> script memberi **HARGA LAMA**, ditulis di baris pertama.

---

**HARGA LAMA: harga terakhir yang ditemukan per 18-08-2026 (42 hari lalu); PER/PBV/imbal dividen di bawah memakai harga itu.**
Asumsi: semua bagian, laporan terbaru yang ditemukan (6M2026), berita maks. 5. Situs idx.co.id memblokir akses otomatis;
angka LK diambil dari berita yang mengutip LK, **bukan** dari dokumen resmi. Mohon cocokkan dengan PDF LK di idx.co.id,
atau tempel angkanya ke saya.

# Catatan Riset: ICBP - PT Indofood CBP Sukses Makmur Tbk
Disusun: 2026-09-29 | Data terbaru yang dipakai: LK 6M2026 (per 30-06-2026, lewat berita), harga per 18-08-2026

## 1. Ringkasan fakta
- Penjualan neto semester I 2026 Rp41,86 T, naik 11,33% dari Rp37,60 T (Sumber: Databoks Katadata, 14-08-2026; Kontan via TradingView, Agustus 2026, diakses 2026-09-29).
- Laba bersih yang dapat diatribusikan ke entitas induk Rp3,70 T, turun 33,21% (dihitung ulang dari angka laporan yang dikutip) dari Rp5,54 T (Sumber: Databoks Katadata 14-08-2026; Infobanknews 02-08-2026).
- Laba usaha naik 8% menjadi Rp9,15 T; beban keuangan naik 216% menjadi Rp4,09 T, termasuk rugi selisih kurs Rp2,9 T (Sumber: IDX Channel, 01-08-2026).
- Total aset Rp143,99 T, liabilitas Rp68,71 T, ekuitas Rp75,27 T per 30-06-2026 (Sumber: Databoks Katadata, 14-08-2026).

## 2. Berita & pengumuman terbaru
| Tanggal | Isi singkat | Sumber |
|---|---|---|
| 14-08-2026 (berita lama) | Penjualan semester I tertinggi 2021-2026; laba induk turun 33,21% (dihitung ulang dari angka laporan yang dikutip) | databoks.katadata.co.id, diakses 2026-09-29 |
| 02-08-2026 (berita lama) | Laba bersih Rp3,70 T vs Rp5,54 T; core profit Rp5,40 T | infobanknews.com, diakses 2026-09-29 |
| 01-08-2026 (berita lama) | Laba turun karena rugi kurs belum terealisasi; arus kas disebut menguat | idxchannel.com, diakses 2026-09-29 |
| 26-06-2026 (berita lama) | RUPST menetapkan dividen tunai TB 2025 Rp265/saham (naik 6% dari Rp250) | idxchannel.com, diakses 2026-09-29 |

Tidak ditemukan berita/pengumuman ICBP dalam 30 hari terakhir dari sumber yang bisa diakses.

## 3. Aksi korporasi
| Jenis | Tanggal penting | Rincian | Sumber |
|---|---|---|---|
| Dividen tunai TB 2025 | RUPST 26-06-2026; cum reguler 06-07-2026; recording 08-07-2026; bayar 28-07-2026 | Rp265/saham | IDX Channel 26-06-2026 (DPS, RUPST); tanggal cum/recording/bayar dari cuplikan hasil pencarian (Ajaib/PintarSaham) - **perlu dicek di pengumuman resmi idx.co.id** |
| (catatan sumber bertentangan) | - | Total dividen: Rp9,22 T (IDX Channel) vs Rp3,09 T (Emitennews/PintarSaham). DPS x saham beredar = Rp3,09 T | lihat kolom kiri |

## 4. Angka laporan keuangan & rasio (keluaran script apa adanya)
#### Hitungan Rasio: ICBP - PT Indofood CBP Sukses Makmur Tbk

Periode: 6M2026 (6 bulan) | Pembanding: 6M2025 | Tanggal laporan: 2026-06-30
Sumber laporan: Databoks Katadata 14-08-2026; Infobanknews 02-08-2026; IDX Channel 01-08-2026 (berita, bukan LK resmi) | Harga: cuplikan hasil pencarian (Investing/TradingView), 18-08-2026, per 2026-08-18 | Dihitung: 2026-09-29

#### Angka yang dibaca script (cocokkan dengan sumber)

Satuan laporan: satuan (rupiah penuh)

| Pos | Nilai terbaca |
|---|---|
| Pendapatan | Rp41.860.000.000.000 (Rp41,86 T) |
| Pendapatan periode lalu | Rp37.600.000.000.000 (Rp37,60 T) |
| Laba bersih | Rp3.700.000.000.000 (Rp3,70 T) |
| Laba bersih periode lalu | Rp5.540.000.000.000 (Rp5,54 T) |
| Laba bersih entitas induk | Rp3.700.000.000.000 (Rp3,70 T) |
| Total ekuitas | Rp75.270.000.000.000 (Rp75,27 T) |
| Total liabilitas | Rp68.710.000.000.000 (Rp68,71 T) |
| Total aset | Rp143.990.000.000.000 (Rp143,99 T) |
| Saham beredar (lembar) | 11.661.908.000 lembar |
| Harga saham | Rp7.625 |
| Dividen per saham | Rp265 |

#### Rasio

| Rasio | Nilai | Keterangan |
|---|---|---|
| Pertumbuhan pendapatan | 11,33% | (sekarang - lalu) / abs(lalu) x 100% |
| Pertumbuhan laba bersih | -33,21% | (sekarang - lalu) / abs(lalu) x 100% |
| Margin laba bersih | 8,84% | laba bersih / pendapatan x 100% |
| ROE | 9,83% | entitas induk 6 bulan x 12/6 (disetahunkan sederhana, abaikan musim) / total ekuitas (akhir periode) x 100% |
| DER (liabilitas/ekuitas) | 0,91x | total liabilitas / total ekuitas |
| Laba per saham (EPS, setahun) | Rp634,54 | entitas induk 6 bulan x 12/6 (disetahunkan sederhana, abaikan musim) / saham beredar |
| Nilai buku per saham (BVPS) | Rp6.454,35 | total ekuitas / saham beredar |
| PER | 12,02x | harga / EPS |
| PBV | 1,18x | harga / BVPS |
| Kapitalisasi pasar | Rp88,92 T | harga x saham beredar |
| Imbal hasil dividen (tahun buku 2025) | 3,48% | DPS / harga x 100% |

#### Kesegaran data
- HARGA LAMA: harga per 2026-08-18 (42 hari lalu). PER/PBV/imbal dividen berubah setiap hari bursa.

#### Fakta yang perlu diketahui
- Laporan interim 6 bulan: ROE, EPS, dan PER memakai laba yang disetahunkan sederhana (x12/6). Hasil bisa meleset bila usaha musiman.
- Imbal hasil dividen memakai dividen yang SUDAH diumumkan/dibayar; dividen tahun berikutnya belum tentu sama.
- Laba bersih turun 33,21% dibanding periode lalu.

Rasio hanyalah hasil hitung dari angka di atas, bukan penilaian murah/mahal atau layak/tidak.

## 5. Risiko & hal yang perlu diketahui (fakta)
- Rugi selisih kurs Rp2,9 T dari kegiatan pembiayaan disebut sebagai penyebab utama turunnya laba (IDX Channel, 01-08-2026).
- Laba interim disetahunkan sederhana (x2); semester I memuat rugi kurs belum terealisasi yang bisa berubah arah bila kurs berubah.
- Angka berasal dari berita, bukan PDF LK; saham beredar 11.661.908.000 lembar dari profil umum emiten (**perlu dicek** di idx.co.id).

## 6. Pertanyaan untuk dicari jawabannya sendiri
1. Kenapa laba bergerak berbeda arah dengan pendapatan? Cek pos selisih kurs & beban keuangan di catatan LK.
2. Kapan utang berbunga besar jatuh tempo, dan dalam mata uang apa?
3. Apakah arus kas operasi sejalan dengan laba bersih?
4. Berapa porsi laba dari pos satu kali / belum terealisasi?
5. Siapa pemegang saham pengendali dan berapa porsi publik (free float)?

## 7. Data yang belum ditemukan / perlu dicek
- Harga saham terbaru (setelah 18-08-2026): tidak ditemukan dari sumber yang bisa diakses; mohon tempel harga + tanggal.
- Utang berbunga & rincian mata uang pinjaman: perlu dicek di catatan LK.
- Tanggal cum/ex/recording dari pengumuman resmi: perlu dicek di idx.co.id.

---
_Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

---
### Penilaian penguji (skenario 01)
- Alur SKILL.md bisa diikuti tanpa menebak; blokir idx.co.id ditangani sesuai aturan (jujur, pakai sumber sekunder bertanda).
- Script: 11 rasio cocok 11/11 dengan hitungan independen Decimal (lihat HASIL-UJI.md).
- HARGA LAMA terdeteksi otomatis; berita > 30 hari ditandai. Konflik sumber (Rp9,22 T vs Rp3,09 T) tertangani.
- Kekurangan: SKILL.md tidak mengatur bila **laba total & laba induk** tidak dipisah di berita (agent mengisi keduanya sama; margin pakai laba induk). Minor.
- Kepatuhan: tidak ada label murah/mahal, tidak ada rekomendasi. Lolos.
