# Uji 02 - Skenario normal (emiten nyata, bank): BBRI

> Uji independen, 2026-09-29, claude-code (simulasi agent). Data nyata dari sumber publik yang diambil penguji.

**Input pengguna:** "Tolong rangkum BBRI: kinerja semester 1, dividen, berita minggu ini. Harga kemarin-kemarin sekitar 3.140."

**Yang dilakukan agent:**
1. idx.co.id -> 403; situs IR BRI dapat dijangkau tapi tidak ada PDF LK yang bisa diekstrak otomatis -> pakai media nasional, ditandai.
2. Menemukan dua angka laba yang tampak bertentangan: Rp31,2 T (6M2026, **konsolidasian**) vs Rp34,77 T (8M2026, laporan
   bulanan **bank saja**). Keduanya ditampilkan dengan periode & basis masing-masing.
3. Laba 6M2025: Rp26,5 T (receh.in, angka tertulis) vs Rp26,6 T (Katadata, turunan dari +17,5%). Dipakai angka tertulis, selisih dicatat.
4. Total ekuitas Rp345,06 T hanya muncul di cuplikan mesin pencari (sumber asli tidak bisa dibuka) -> ditulis "perlu dicek".
5. Saham beredar: tidak ditemukan langsung; dihitung dari total dividen Rp52,10 T / Rp346 = ±150,58 miliar lembar (ditandai turunan).
6. Script: `rasio d2_bbri.json --hari-ini 2026-09-29` (exit 0). Kolom "pendapatan" diisi **pendapatan bunga bersih (NII)** -
   SKILL.md tidak memberi panduan untuk bank (lihat temuan).

---

Asumsi: semua bagian; LK terbaru yang ditemukan 6M2026 (lewat berita, bukan PDF resmi); harga Rp3.140 penutupan 25-09-2026.

# Catatan Riset: BBRI - PT Bank Rakyat Indonesia (Persero) Tbk
Disusun: 2026-09-29 | Data terbaru: LK 6M2026 (per 30-06-2026), laba bank-only 8M2026, harga 25-09-2026

## 1. Ringkasan fakta
- Laba bersih konsolidasian semester I 2026 Rp31,2 T, naik 17,5% yoy (Sumber: Katadata, 31-08-2026; receh.in, 31-08-2026).
- Pendapatan bunga bersih Rp80,5 T dari Rp73,3 T (+9,82%) (Sumber: Katadata, 31-08-2026).
- Total aset Rp2.352 T per Juni 2026; kredit Rp1.646 T; DPK Rp1.581 T (Sumber: Katadata, 31-08-2026).
- ROE yang dilaporkan perusahaan 18,8% (6M2026) vs 16,6% (6M2025) (Sumber: Katadata/Investortrust, 31-08-2026). Hitungan script di bawah 18,08% karena basis berbeda (laba disetahunkan / ekuitas akhir total).
- Laba bank saja 8M2026 Rp34,77 T, +6,63% yoy (Sumber: CNBC Indonesia, 28-09-2026) - basis berbeda dari angka konsolidasian.

## 2. Berita & pengumuman terbaru
| Tanggal | Isi singkat | Sumber |
|---|---|---|
| 28-09-2026 | Keterbukaan informasi: LK per 30-09-2026 akan ditelaah terbatas (limited review) akuntan publik, "dalam rangka rencana aksi korporasi dan/atau pelaksanaan aspirasi pemegang saham"; jenis aksi belum diungkap | cnbcindonesia.com, diakses 2026-09-29 |
| 25-09-2026 | Saham ditutup Rp3.140 (rentang 3.110-3.160) | mediakeuangan.id, diakses 2026-09-29 |
| 23-09-2026 | BRI meraih 4 predikat Fortune Indonesia 100 2026 | liputan6.com, diakses 2026-09-29 |
| 31-08-2026 (berita lama) | Rilis kinerja semester I 2026 | katadata.co.id |

Catatan sumber: artikel harga 25-09-2026 menulis "penutupan sebelumnya 3.300" namun perubahan 0% - **tidak konsisten**; harga perlu dicek ke idx.co.id.

## 3. Aksi korporasi
| Jenis | Tanggal penting | Rincian | Sumber |
|---|---|---|---|
| Dividen interim TB 2025 | dibayar 15-01-2026 | Rp137/saham | cuplikan hasil pencarian (Ajaib/Investortrust) - perlu dicek |
| Dividen final TB 2025 | RUPST 13-04-2026; cum reguler 20-04; ex 21-04; recording 22-04; bayar 08-05-2026 | Rp209/saham; total TB 2025 Rp346/saham = Rp52,10 T | Bareksa, 14-04-2026 (perlu dicocokkan dengan pengumuman resmi) |
| Rencana aksi korporasi (belum diungkap) | limited review LK 30-09-2026 | jenis aksi belum diumumkan | CNBC Indonesia, 28-09-2026 |

## 4. Angka laporan keuangan & rasio (keluaran script apa adanya)
#### Hitungan Rasio: BBRI - PT Bank Rakyat Indonesia (Persero) Tbk

Periode: 6M2026 (6 bulan) | Pembanding: 6M2025 | Tanggal laporan: 2026-06-30
Sumber laporan: Katadata 31-08-2026; receh.in 31-08-2026; ekuitas dari cuplikan hasil pencarian (perlu dicek) | Harga: mediakeuangan.id 25-09-2026, per 2026-09-25 | Dihitung: 2026-09-29

#### Angka yang dibaca script (cocokkan dengan sumber)

Satuan laporan: satuan (rupiah penuh)

| Pos | Nilai terbaca |
|---|---|
| Pendapatan | Rp80.500.000.000.000 (Rp80,50 T) |
| Pendapatan periode lalu | Rp73.300.000.000.000 (Rp73,30 T) |
| Laba bersih | Rp31.200.000.000.000 (Rp31,20 T) |
| Laba bersih periode lalu | Rp26.500.000.000.000 (Rp26,50 T) |
| Total ekuitas | Rp345.060.000.000.000 (Rp345,06 T) |
| Total aset | Rp2.352.000.000.000.000 (Rp2.352,00 T) |
| Saham beredar (lembar) | 150.580.000.000 lembar |
| Harga saham | Rp3.140 |
| Dividen per saham | Rp346 |

#### Rasio

| Rasio | Nilai | Keterangan |
|---|---|---|
| Pertumbuhan pendapatan | 9,82% | (sekarang - lalu) / abs(lalu) x 100% |
| Pertumbuhan laba bersih | 17,74% | (sekarang - lalu) / abs(lalu) x 100% |
| Margin laba bersih | 38,76% | laba bersih / pendapatan x 100% |
| ROE | 18,08% | laba bersih total 6 bulan x 12/6 (disetahunkan sederhana, abaikan musim) / total ekuitas (akhir periode) x 100% |
| DER (liabilitas/ekuitas) | - | tidak dihitung, butuh: Total liabilitas |
| Laba per saham (EPS, setahun) | Rp414,40 | laba bersih total 6 bulan x 12/6 (disetahunkan sederhana, abaikan musim) / saham beredar |
| Nilai buku per saham (BVPS) | Rp2.291,54 | total ekuitas / saham beredar |
| PER | 7,58x | harga / EPS |
| PBV | 1,37x | harga / BVPS |
| Kapitalisasi pasar | Rp472,82 T | harga x saham beredar |
| Imbal hasil dividen (tahun buku 2025) | 11,02% | DPS / harga x 100% |

#### Fakta yang perlu diketahui
- Laporan interim 6 bulan: ROE, EPS, dan PER memakai laba yang disetahunkan sederhana (x12/6). Hasil bisa meleset bila usaha musiman.
- Imbal hasil dividen memakai dividen yang SUDAH diumumkan/dibayar; dividen tahun berikutnya belum tentu sama.
- Laba entitas induk tidak diisi: ROE/EPS memakai laba bersih total (termasuk kepentingan nonpengendali bila ada).
- Sektor keuangan: DER lazim tinggi karena dana nasabah tercatat sebagai liabilitas; jangan dibandingkan dengan DER perusahaan non-keuangan.

Rasio hanyalah hasil hitung dari angka di atas, bukan penilaian murah/mahal atau layak/tidak.

Catatan agent: baris "Pendapatan" = pendapatan bunga bersih (NII), sehingga "margin laba bersih" = laba / NII, tidak sebanding dengan margin emiten non-bank. Saham beredar adalah angka turunan (total dividen / DPS). Imbal dividen memakai total DPS TB 2025 (interim + final) Rp346.

## 5. Risiko & hal yang perlu diketahui (fakta)
- Sektor bank: DER tidak dihitung (liabilitas tidak ditemukan) dan memang tidak sebanding dengan sektor non-keuangan.
- Rencana aksi korporasi belum diungkap jenisnya (CNBC Indonesia, 28-09-2026).
- Total ekuitas belum terverifikasi dari dokumen yang bisa dibuka.

## 6. Pertanyaan untuk dicari jawabannya sendiri
1. Aksi korporasi apa yang direncanakan (pantau keterbukaan informasi setelah 30-09-2026)?
2. Apa pendorong utama kenaikan laba: pendapatan bunga, penurunan biaya kredit, atau pos satu kali?
3. Bagaimana tren kualitas kredit (NPL, biaya kredit) di catatan LK?
4. Berapa rasio pembayaran dividen historis & apakah kebijakan dividen tertulis?

## 7. Data yang belum ditemukan / perlu dicek
- Total ekuitas & total liabilitas dari LK resmi 6M2026.
- Jumlah saham beredar resmi (dikurangi saham treasuri) di idx.co.id.
- Harga penutupan 28-09-2026 (sumber harga 25-09 memuat angka tidak konsisten).

---
_Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

---
### Penilaian penguji (skenario 02)
- Rasio cocok 11/11 dengan verifikasi independen. Fakta "sektor keuangan: DER tidak sebanding" muncul otomatis. Bagus.
- **Temuan SEDANG:** SKILL.md/script tidak punya panduan "pendapatan" untuk bank (NII? pendapatan bunga bruto? total pendapatan operasional?). Margin 38,76% bisa menyesatkan tanpa catatan; catatan di atas ditulis penguji atas inisiatif sendiri, bukan instruksi skill.
- **Temuan RENDAH:** ROE script (18,08%) berbeda dengan ROE yang dilaporkan bank (18,8%); skill tidak menyuruh menjelaskan perbedaan basis. Agent penguji menjelaskannya sendiri.
- Kepatuhan: artikel yang dipakai tidak memuat target harga; tidak ada kata rekomendasi. Lolos.
