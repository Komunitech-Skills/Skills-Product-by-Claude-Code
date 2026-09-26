# Uji 01 — Toko bangunan: "Penjualan 2026.xlsx" (3 sheet kuartal + 1 sheet tersembunyi)

> Uji independen Tahap 6 (penguji ≠ pembuat), 2026-09-25. Skill disalin ke scratchpad, script
> dijalankan dari salinan. Simulasi agent: `claude-code (simulasi agent)`.

## Skenario
Pemilik toko bangunan mengirim `Penjualan 2026.xlsx` dan bertanya:
*"Kategori apa paling laku, tren per bulan gimana, dan Q2 vs Q3 naik atau turun?"*

## Fixture (bisa diulang)
`python3 examples/buat_fixture_uji.py <folder>` (deterministik, seed 20260925) → `Penjualan 2026.xlsx`.
XLSX ditulis tangan meniru Excel 365: `sharedStrings.xml`, `styles.xml` dengan numFmt 164
`dd/mm/yyyy;@` + bawaan 14 (tanggal serial) dan numFmt 165 akuntansi `"Rp"* #,##0`,
sheet `Master Barang` **tersembunyi** di urutan pertama, sheet `Q1`/`Q2`/`Q3` (499 transaksi Jan–Sep),
judul 2 baris di-merge (A1:H1, A2:H2), header di baris 3, merge vertikal H4:H6 (Pelanggan),
kolom Total = rumus `=E*F` **dengan nilai tersimpan**, 3 rumus **tanpa** nilai tersimpan (NT-0212, NT-0393,
NT-0412), 4 transaksi Harga/Total diketik sebagai **teks** `Rp 1.250.000`, 1 retur `(185.000)` teks
akuntansi, kategori beda huruf besar-kecil/spasi (`SEMEN`, `semen `, ` cat`), baris `TOTAL` di bawah
tiap sheet (rumus SUM dengan nilai tersimpan). File dibuka tanpa error oleh openpyxl 3.1.5 & pandas 3.0.6
(cek realisme; LibreOffice headless di lingkungan uji gagal memuat file apa pun, termasuk CSV, jadi tidak dipakai).

## Langkah agent (sesuai SKILL.md)
```bash
$ python3 scripts/analisis.py daftar fx/Penjualan 2026.xlsx
```
```markdown
## Isi file Penjualan 2026.xlsx

_Sumber: Penjualan 2026.xlsx_

### Sheet di workbook

| No | Sheet | Status | Baris berisi |
|---:|---|---|---:|
| 1 | Master Barang | tersembunyi | 17 |
| 2 | Q1 | terlihat | 151 |
| 3 | Q2 | terlihat | 175 |
| 4 | Q3 | terlihat | 185 |

### Temuan (dihitung script)

- Workbook berisi 4 sheet. Tanpa --sheet, yang dianalisis: 'Q1'.
- Judul kolom di baris 3: Tanggal, No Nota, Kategori, Barang, Qty, Harga Satuan, Total, Pelanggan.

### Perlu diperhatikan

- ⚠️ Workbook punya 4 sheet (Master Barang, Q1, Q2, Q3); yang dianalisis: 'Q1'. Pakai --sheet untuk sheet lain.
- ⚠️ 1 rentang sel gabungan (merge) ditemukan: H4:H6. Teksnya disalin ke setiap baris di rentang itu agar bisa dikelompokkan — pastikan ini sesuai maksud tabel.

### Catatan

- Judul kolom (header) terdeteksi di baris 3 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.

```

```bash
$ python3 scripts/analisis.py pivot fx/Penjualan 2026.xlsx --sheet Q2 --grup Kategori --nilai Total
```
```markdown
## Jumlah Total per Kategori

_Sumber: Penjualan 2026.xlsx — sheet 'Q2'; 171 baris data_

| Kategori | Baris | Jumlah Total | % dari total |
|---|---:|---:|---:|
| Semen | 55 | Rp 51.802.000 | 53,3% |
| Cat | 24 | Rp 12.417.000 | 12,8% |
| Keramik | 24 | Rp 11.840.000 | 12,2% |
| Besi | 37 | Rp 11.623.000 | 12,0% |
| Pipa & Sanitasi | 13 | Rp 7.386.500 | 7,6% |
| Alat & Perkakas | 18 | Rp 2.044.000 | 2,1% |
| **TOTAL** | **171** | **Rp 97.112.500** | **100,0%** |

### Temuan (dihitung script)

- Tertinggi: Semen (Rp 51.802.000, 53,3% dari total).
- Terendah: Alat & Perkakas (Rp 2.044.000, 2,1% dari total).
- 6 kelompok; jumlah total keseluruhan: Rp 97.112.500.

### Saran grafik

Grafik batang horizontal, urut dari terbesar ke terkecil.

### Perlu diperhatikan

- ⚠️ 1 sel berisi rumus tanpa nilai tersimpan (mis. G68) sehingga dianggap kosong. Biasanya file dibuat aplikasi lain/belum dihitung: buka di Excel/LibreOffice, tekan Simpan sekali, lalu kirim ulang.
- ⚠️ 1 rentang sel gabungan (merge) ditemukan: H4:H6. Teksnya disalin ke setiap baris di rentang itu agar bisa dikelompokkan — pastikan ini sesuai maksud tabel.
- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 175). Pakai --pertahankan-total bila itu data asli.
- ⚠️ Kolom 'Kategori': penulisan beda huruf besar-kecil/spasi digabung (Alat & Perkakas ← 'Alat & Perkakas' / 'alat & perkakas'; Besi ← 'Besi' / 'besi'; Keramik ← 'KERAMIK' / 'Keramik'; Cat ← 'CAT' / 'Cat' / 'cat').

### Catatan

- Judul kolom (header) terdeteksi di baris 3 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.

```

```bash
$ python3 scripts/analisis.py pivot fx/Penjualan 2026.xlsx --sheet Q3 --grup Kategori --nilai Total
```
```markdown
## Jumlah Total per Kategori

_Sumber: Penjualan 2026.xlsx — sheet 'Q3'; 181 baris data_

| Kategori | Baris | Jumlah Total |
|---|---:|---:|
| Semen | 50 | Rp 23.502.000 |
| Cat | 38 | Rp 14.570.000 |
| Pipa & Sanitasi | 21 | Rp 10.433.500 |
| Keramik | 16 | Rp 8.821.000 |
| Besi | 25 | Rp 7.820.000 |
| Alat & Perkakas | 31 | Rp 3.984.000 |
| **TOTAL** | **181** | **Rp 69.130.500** |

### Temuan (dihitung script)

- Tertinggi: Semen (Rp 23.502.000).
- Terendah: Alat & Perkakas (Rp 3.984.000).
- 6 kelompok; jumlah total keseluruhan: Rp 69.130.500.

### Saran grafik

Grafik batang horizontal, urut dari terbesar ke terkecil.

### Perlu diperhatikan

- ⚠️ 2 sel berisi rumus tanpa nilai tersimpan (mis. G79, G98) sehingga dianggap kosong. Biasanya file dibuat aplikasi lain/belum dihitung: buka di Excel/LibreOffice, tekan Simpan sekali, lalu kirim ulang.
- ⚠️ 1 rentang sel gabungan (merge) ditemukan: H4:H6. Teksnya disalin ke setiap baris di rentang itu agar bisa dikelompokkan — pastikan ini sesuai maksud tabel.
- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 185). Pakai --pertahankan-total bila itu data asli.
- ⚠️ Kolom 'Kategori': penulisan beda huruf besar-kecil/spasi digabung (Cat ← 'CAT' / 'Cat'; Besi ← 'Besi' / 'besi'; Pipa & Sanitasi ← 'Pipa & Sanitasi' / 'pipa & sanitasi'; Alat & Perkakas ← 'Alat & Perkakas' / 'alat & perkakas').

### Catatan

- Judul kolom (header) terdeteksi di baris 3 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.

```

```bash
$ python3 scripts/analisis.py banding fx/Penjualan 2026.xlsx --sheet Q2 --file-b fx/Penjualan 2026.xlsx --sheet-b Q3 --nilai Total --grup Kategori --label-a Q2 --label-b Q3
```
```markdown
## Perbandingan Jumlah Total: Q2 vs Q3

_Sumber: Penjualan 2026.xlsx — sheet 'Q2' vs Penjualan 2026.xlsx; 171 baris data_

| Kategori | Q2 | Q3 | Selisih | Perubahan % |
|---|---:|---:|---:|---:|
| Semen | Rp 51.802.000 | Rp 23.502.000 | -Rp 28.300.000 | -54,6% |
| Besi | Rp 11.623.000 | Rp 7.820.000 | -Rp 3.803.000 | -32,7% |
| Pipa & Sanitasi | Rp 7.386.500 | Rp 10.433.500 | Rp 3.047.000 | 41,3% |
| Keramik | Rp 11.840.000 | Rp 8.821.000 | -Rp 3.019.000 | -25,5% |
| Cat | Rp 12.417.000 | Rp 14.570.000 | Rp 2.153.000 | 17,3% |
| Alat & Perkakas | Rp 2.044.000 | Rp 3.984.000 | Rp 1.940.000 | 94,9% |
| **TOTAL** | **Rp 97.112.500** | **Rp 69.130.500** | **-Rp 27.982.000** | **-28,8%** |

### Temuan (dihitung script)

- Jumlah Total: turun 28,8% (Rp 97.112.500 → Rp 69.130.500).
- Jumlah baris: 171 vs 181.
- Naik paling besar: Pipa & Sanitasi — naik 41,3% (Rp 7.386.500 → Rp 10.433.500).
- Turun paling besar: Semen — turun 54,6% (Rp 51.802.000 → Rp 23.502.000).

### Saran grafik

Grafik batang berdampingan (clustered column): Q2 vs Q3 per Kategori.

### Perlu diperhatikan

- ⚠️ 1 sel berisi rumus tanpa nilai tersimpan (mis. G68) sehingga dianggap kosong. Biasanya file dibuat aplikasi lain/belum dihitung: buka di Excel/LibreOffice, tekan Simpan sekali, lalu kirim ulang.
- ⚠️ 1 rentang sel gabungan (merge) ditemukan: H4:H6. Teksnya disalin ke setiap baris di rentang itu agar bisa dikelompokkan — pastikan ini sesuai maksud tabel.
- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 175). Pakai --pertahankan-total bila itu data asli.
- ⚠️ 2 sel berisi rumus tanpa nilai tersimpan (mis. G79, G98) sehingga dianggap kosong. Biasanya file dibuat aplikasi lain/belum dihitung: buka di Excel/LibreOffice, tekan Simpan sekali, lalu kirim ulang.
- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 185). Pakai --pertahankan-total bila itu data asli.
- ⚠️ Kolom 'Kategori': penulisan beda huruf besar-kecil/spasi digabung (Alat & Perkakas ← 'Alat & Perkakas' / 'alat & perkakas'; Besi ← 'Besi' / 'besi'; Keramik ← 'KERAMIK' / 'Keramik'; Cat ← 'CAT' / 'Cat' / 'cat').

### Catatan

- Judul kolom (header) terdeteksi di baris 3 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.

```

### Kendala: pertanyaan Jan–Sep butuh 3 sheet digabung
Script hanya membaca **satu sheet per perintah** (tidak ada `--sheet semua`). Pertanyaan "kategori
paling laku (Jan–Sep)" dan "tren per bulan" tidak bisa dijawab satu perintah. SKILL.md tidak memberi
jalan; agent yang patuh "jangan menghitung sendiri" terpaksa berimprovisasi. Penguji memakai jalan
yang tetap berbasis script: `bersihkan` tiap sheet → gabung CSV (header sekali) → analisis ulang:
```bash
for q in Q1 Q2 Q3; do python3 scripts/analisis.py bersihkan "Penjualan 2026.xlsx" --sheet $q --keluar $q.csv; done
python3 -c "import csv;R=[];[R.extend(r if i==0 else r[1:]) for i,r in enumerate(list(csv.reader(open(q+'.csv',encoding='utf-8-sig'))) for q in ['Q1','Q2','Q3'])];csv.writer(open('gabung-Jan-Sep.csv','w',newline='',encoding='utf-8')).writerows(R)"
```
Peringatan dari `bersihkan` tiap sheet (3 rumus tanpa nilai, 3 baris TOTAL dilewati, kategori digabung)
**hilang** di file gabungan, jadi agent harus membawanya manual.

```bash
$ python3 scripts/analisis.py pivot out/gabung-Jan-Sep.csv --grup Kategori --nilai Total
```
```markdown
## Jumlah Total per Kategori

_Sumber: gabung-Jan-Sep.csv; 499 baris data_

| Kategori | Baris | Jumlah Total |
|---|---:|---:|
| Semen | 149 | Rp 105.444.000 |
| Cat | 88 | Rp 36.252.000 |
| Keramik | 60 | Rp 32.785.000 |
| Pipa & Sanitasi | 50 | Rp 25.453.000 |
| Besi | 85 | Rp 25.428.000 |
| Alat & Perkakas | 67 | Rp 8.194.000 |
| **TOTAL** | **499** | **Rp 233.556.000** |

### Temuan (dihitung script)

- Tertinggi: Semen (Rp 105.444.000).
- Terendah: Alat & Perkakas (Rp 8.194.000).
- 6 kelompok; jumlah total keseluruhan: Rp 233.556.000.

### Saran grafik

Grafik batang horizontal, urut dari terbesar ke terkecil.

```

```bash
$ python3 scripts/analisis.py pivot out/gabung-Jan-Sep.csv --grup Kategori --nilai Qty
```
```markdown
## Jumlah Qty per Kategori

_Sumber: gabung-Jan-Sep.csv; 499 baris data_

| Kategori | Baris | Jumlah Qty |
|---|---:|---:|
| Semen | 149 | 1.683 |
| Besi | 85 | 366 |
| Cat | 88 | 301 |
| Alat & Perkakas | 67 | 220 |
| Keramik | 60 | 219 |
| Pipa & Sanitasi | 50 | 152 |
| **TOTAL** | **499** | **2.941** |

### Temuan (dihitung script)

- Tertinggi: Semen (1.683).
- Terendah: Pipa & Sanitasi (152).
- 6 kelompok; jumlah qty keseluruhan: 2.941.

### Saran grafik

Grafik batang horizontal, urut dari terbesar ke terkecil.

```

```bash
$ python3 scripts/analisis.py tren out/gabung-Jan-Sep.csv --nilai Total
```
```markdown
## Tren Jumlah Total per bulan

_Sumber: gabung-Jan-Sep.csv; 499 baris data_

| Periode | Baris | Jumlah Total | Perubahan vs periode sebelumnya |
|---|---:|---:|---:|
| Jan 2026 | 48 | Rp 23.917.000 | - |
| Feb 2026 | 44 | Rp 17.888.500 | -25,2% |
| Mar 2026 | 55 | Rp 25.507.500 | 42,6% |
| Apr 2026 | 52 | Rp 34.340.000 | 34,6% |
| Mei 2026 | 58 | Rp 30.672.500 | -10,7% |
| Jun 2026 | 61 | Rp 32.100.000 | 4,7% |
| Jul 2026 | 58 | Rp 17.476.000 | -45,6% |
| Agu 2026 | 63 | Rp 26.433.000 | 51,3% |
| Sep 2026 | 60 | Rp 25.221.500 | -4,6% |

### Temuan (dihitung script)

- Tertinggi: Apr 2026 (Rp 34.340.000). Terendah: Jul 2026 (Rp 17.476.000).
- Dari Jan 2026 ke Sep 2026: naik 5,5% (Rp 23.917.000 → Rp 25.221.500).
- Kenaikan terbesar: Agu 2026 (+51,3%).
- Penurunan terbesar: Jul 2026 (-45,6%).
- Rata-rata per bulan: Rp 25.950.667.

### Saran grafik

Grafik garis (line chart): sumbu X = bulan, sumbu Y = Jumlah Total. Di Excel: blok tabel → Insert → Line.

```

```bash
$ python3 scripts/analisis.py banding out/gabung-Jan-Sep.csv --nilai Total --periode-a Q2 2026 --periode-b Q3 2026
```
```markdown
## Perbandingan Jumlah Total: 1 Apr 2026 s.d. 30 Jun 2026 vs 1 Jul 2026 s.d. 30 Sep 2026

_Sumber: gabung-Jan-Sep.csv; 499 baris data_

| Keterangan | 1 Apr 2026 s.d. 30 Jun 2026 | 1 Jul 2026 s.d. 30 Sep 2026 | Selisih | Perubahan % |
|---|---:|---:|---:|---:|
| Jumlah Total | Rp 97.112.500 | Rp 69.130.500 | -Rp 27.982.000 | -28,8% |

### Temuan (dihitung script)

- Jumlah Total: turun 28,8% (Rp 97.112.500 → Rp 69.130.500).
- Jumlah baris: 171 vs 181.
- Panjang periode beda (91 vs 92 hari). Rata-rata per hari: Rp 1.067.170 vs Rp 751.418 — turun 29,6% (Rp 1.067.170 → Rp 751.418).

### Saran grafik

Grafik batang berdampingan (clustered column): 1 Apr 2026 s.d. 30 Jun 2026 vs 1 Jul 2026 s.d. 30 Sep 2026.

```

## Jawaban akhir agent (format SKILL.md)
**Jawaban singkat:** Kategori paling laku Jan–Sep 2026 adalah **Semen**: Rp 105.444.000 dari total
Rp 233.556.000 (149 transaksi, 1.683 sak). Omzet tertinggi di **Apr 2026** (Rp 34.340.000), terendah
**Jul 2026** (Rp 17.476.000). **Q3 turun 28,8% dibanding Q2** (Rp 97.112.500 → Rp 69.130.500),
terutama karena Semen turun 54,6% (Rp 51.802.000 → Rp 23.502.000).

(tabel pivot kategori, tren 9 bulan, dan banding per kategori di atas ditempel apa adanya)

**Temuan:**
1. Semen menyumbang porsi terbesar di setiap kuartal (Q1 44,8%, Q2 53,3%).
2. Q3 turun 28,8%; per hari Rp 1.067.170 → Rp 751.418 (turun 29,6%). Yang naik: Alat & Perkakas
   (+94,9%), Pipa & Sanitasi (+41,3%), Cat (+17,3%).
3. Juli anjlok 45,6% dari Juni lalu pulih di Agustus (+51,3%).

**Saran grafik:** garis/kolom per bulan untuk tren; batang berdampingan Q2 vs Q3 per kategori.

**Perlu dicek:** 3 sel Total berupa rumus tanpa nilai tersimpan (Q2!G68, Q3!G79, Q3!G98) tidak
terhitung — buka di Excel, Simpan, kirim ulang; baris TOTAL tiap sheet dilewati; penulisan kategori
digabung (SEMEN/semen → Semen, dst.); sel gabungan H4:H6; ada retur -Rp 185.000 di Juli.
(Asumsi: "paling laku" = rupiah terbesar, juga terbesar menurut qty; sheet Q1–Q3; sheet tersembunyi
"Master Barang" diabaikan.)

## Verifikasi angka independen
Kunci dihitung dari data sumber generator (`kunci-jawaban.json`, bukan dari script skill):
| Angka | Kunci | Script | Cocok |
|---|---:|---:|:--:|
| Total Jan–Sep (496 nilai terisi dari 499 baris) | 233.556.000 | 233.556.000 | ✔ |
| Semen / Cat / Keramik / Pipa / Besi / Alat | 105.444.000 / 36.252.000 / 32.785.000 / 25.453.000 / 25.428.000 / 8.194.000 | sama | ✔ |
| Qty Semen | 1.683 | 1.683 | ✔ |
| Jan…Sep | 23.917.000 · 17.888.500 · 25.507.500 · 34.340.000 · 30.672.500 · 32.100.000 · 17.476.000 · 26.433.000 · 25.221.500 | sama | ✔ |
| Q2 / Q3 / % | 97.112.500 / 69.130.500 / (69.130.500−97.112.500)/97.112.500 = −28,81% | −28,8% | ✔ |
| Rata / median / min / max Total | 470.879,03 / 215.000 / −185.000 / 3.400.000 | Rp 470.879 / Rp 215.000 / −Rp 185.000 / Rp 3.400.000 | ✔ |
| Per kuartal (Q1 67.313.000, 6 kategori tiap Q) | sesuai kunci | sama | ✔ |
| Nomor baris outlier (Q1 baris 11 & 40 qty 50) & sel rumus kosong G68 | dicek dengan openpyxl | benar | ✔ |
| File sistem 1904 (`Penjualan 2026 (1904).xlsx`) tren Q3 | sama dengan 1900 | sama | ✔ |

## Catatan penguji
- ✔ Teks `Rp 1.250.000` & `(185.000)` terbaca sebagai angka; rumus tanpa nilai dilaporkan per sel;
  sheet tersembunyi dilewati & ditandai; TOTAL dilewati; merge vertikal dilaporkan.
- ✘ Tidak ada analisis lintas sheet (lihat HASIL-UJI #1).
- ✘ `banding` dua sheet dari file yang sama memberi label "A: Penjualan 2026.xlsx vs B: Penjualan 2026.xlsx"
  (tidak menyebut sheet) bila tanpa `--label-a/--label-b`.
- ✘ `banding --periode-a "Q2 2026"` pada sheet Q3 saja memberi "naik dari 0" — benar secara data, tetapi
  tidak ada petunjuk bahwa Q2 ada di sheet lain.
- Kolom "Baris" pada pivot menghitung baris termasuk yang nilainya kosong (Q2: 171 baris, 170 nilai).
- Pivot Q3 menghilangkan kolom "% dari total" (karena ada nilai negatif) tanpa penjelasan.
