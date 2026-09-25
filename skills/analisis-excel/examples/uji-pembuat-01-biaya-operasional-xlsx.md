# Contoh 01 — Biaya operasional kantor (XLSX berantakan): kategori terbesar & Agustus vs September

> Dijalankan sendiri oleh pembuat skill saat pengembangan (bukan uji independen Tahap 6
> `CLAUDE.md` — itu perlu agent/sesi terpisah yang belum dilakukan). Disertakan agar pembeli/
> reviewer bisa melihat contoh nyata input → output. Angka diverifikasi manual di bagian akhir.

## Skenario
Admin CV kecil punya file `biaya-operasional.xlsx` (2 sheet: `Biaya`, `Catatan`). Sheet `Biaya`
khas buatan tangan: baris 1 judul laporan yang di-merge A1:E1, judul kolom di baris 2, penulisan
kategori tidak seragam ("Listrik & Air", "listrik & air ", "LISTRIK & AIR"), satu sel Nominal
berisi rumus tanpa nilai tersimpan (E16, file disimpan aplikasi lain), dan baris `TOTAL` di bawah.

Pertanyaan pengguna: *"Ini file biaya operasional kantor. Pengeluaran paling besar di mana, dan
September naik berapa dibanding Agustus?"*

## Input: sheet `Biaya` (isi sel seperti terlihat di Excel)
| Baris | A Tanggal | B Kategori | C Keterangan | D Divisi | E Nominal |
|---|---|---|---|---|---|
| 1 | Biaya Operasional CV Sinar Jaya — Jul s.d. Sep 2026 (merge A1:E1) | | | | |
| 2 | Tanggal | Kategori | Keterangan | Divisi | Nominal |
| 3 | 03/07/2026 | Sewa | Sewa ruko Juli | Umum | 4500000 |
| 4 | 10/07/2026 | Listrik & Air | PLN + PDAM | Umum | 1250000 |
| 5 | 15/07/2026 | Transport | Bensin kurir | Gudang | 850000 |
| 6 | 28/07/2026 | ATK | Kertas, tinta | Admin | 320000 |
| 7 | 03/08/2026 | Sewa | Sewa ruko Agustus | Umum | 4500000 |
| 8 | 09/08/2026 | `listrik & air ` | ` PLN + PDAM` | Umum | 1310000 |
| 9 | 14/08/2026 | Transport | Bensin kurir | Gudang | 920000 |
| 10 | 20/08/2026 | Transport | Servis motor | Gudang | 675000 |
| 11 | 29/08/2026 | ATK | Kertas | Admin | 150000 |
| 12 | 02/09/2026 | Sewa | Sewa ruko September | Umum | 4500000 |
| 13 | 08/09/2026 | LISTRIK & AIR | PLN + PDAM | Umum | 1580000 |
| 14 | 12/09/2026 | Transport | Bensin kurir | Gudang | 1150000 |
| 15 | 19/09/2026 | Transport | Ganti ban | Gudang | 5400000 |
| 16 | 22/09/2026 | ATK | Tinta printer | Admin | `=150000*1` (tanpa nilai tersimpan) |
| 17 | 26/09/2026 | Konsumsi | Rapat klien | Umum | 480000 |
| 18 | TOTAL | | | | `=SUM(E3:E17)` → 27585000 |

Tanggal tersimpan sebagai serial tanggal Excel (format dd/mm/yyyy). File dibuat programatik
dengan pembuat XLSX di `tests/uji_regresi.py` (fungsi `buat_xlsx`).

## Langkah 1 — `profil`
```bash
python3 scripts/analisis.py profil biaya-operasional.xlsx
```
```markdown
## Profil data

_Sumber: biaya-operasional.xlsx — sheet 'Biaya'; 15 baris data_

### Kolom

| Kolom | Tipe | Terisi | Kosong | % kosong | Nilai unik | Tidak valid | Contoh |
|---|---|---:|---:|---:|---:|---:|---|
| Tanggal | tanggal | 15 | 0 | 0,0% | 15 | 0 | 3 Jul 2026, 10 Jul 2026, 15 Jul 2026 |
| Kategori | teks | 15 | 0 | 0,0% | 5 | 0 | Sewa, Listrik & Air, Transport |
| Keterangan | teks | 15 | 0 | 0,0% | 11 | 0 | Sewa ruko Juli, PLN + PDAM, Bensin kurir |
| Divisi | teks | 15 | 0 | 0,0% | 3 | 0 | Umum, Gudang, Admin |
| Nominal | angka (uang) | 14 | 1 | 6,7% | 12 | 0 | Rp 4.500.000, Rp 1.250.000, Rp 850.000 |

### Nilai ekstrem (outlier, metode IQR 1,5×)

| Kolom | Rentang wajar | Jumlah outlier | Contoh (terjauh) |
|---|---|---:|---|
| Nominal | -Rp 3.858.125 s.d. Rp 8.346.875 | 0 | - |

### Temuan (dihitung script)

- 15 baris data × 5 kolom (judul kolom di baris 2).
- Tipe kolom: 3 teks, 1 tanggal, 1 angka.
- Tidak ada baris yang persis sama (duplikat).

### Saran grafik

Histogram untuk melihat sebaran kolom angka; box plot untuk menandai outlier. Untuk laporan, lanjutkan dengan 'ringkas', 'pivot', atau 'tren'.

### Perlu diperhatikan

- ⚠️ Workbook punya 2 sheet (Biaya, Catatan); yang dianalisis: 'Biaya'. Pakai --sheet untuk sheet lain.
- ⚠️ 1 sel berisi rumus tanpa nilai tersimpan (mis. E16) sehingga dianggap kosong. Biasanya file dibuat aplikasi lain/belum dihitung: buka di Excel/LibreOffice, tekan Simpan sekali, lalu kirim ulang.
- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 18). Pakai --pertahankan-total bila itu data asli.
- ⚠️ Kolom 'Kategori': penulisan beda huruf besar-kecil/spasi digabung (Listrik & Air ← 'LISTRIK & AIR' / 'Listrik & Air' / 'listrik & air').

### Catatan

- Judul kolom (header) terdeteksi di baris 2 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.

```

## Langkah 2 — `pivot` per kategori (+ simpan CSV)
```bash
python3 scripts/analisis.py pivot biaya-operasional.xlsx --grup Kategori --nilai Nominal --keluar per-kategori.csv
```
```markdown
## Jumlah Nominal per Kategori

_Sumber: biaya-operasional.xlsx — sheet 'Biaya'; 15 baris data_

| Kategori | Baris | Jumlah Nominal | % dari total |
|---|---:|---:|---:|
| Sewa | 3 | Rp 13.500.000 | 48,9% |
| Transport | 5 | Rp 8.995.000 | 32,6% |
| Listrik & Air | 3 | Rp 4.140.000 | 15,0% |
| Konsumsi | 1 | Rp 480.000 | 1,7% |
| ATK | 3 | Rp 470.000 | 1,7% |
| **TOTAL** | **15** | **Rp 27.585.000** | **100,0%** |

### Temuan (dihitung script)

- Tertinggi: Sewa (Rp 13.500.000, 48,9% dari total).
- Terendah: ATK (Rp 470.000, 1,7% dari total).
- 5 kelompok; jumlah nominal keseluruhan: Rp 27.585.000.

### Saran grafik

Grafik batang horizontal urut terbesar. Pie/donat boleh karena ≤ 5 bagian dari satu total, tapi batang tetap lebih mudah dibandingkan.

### Perlu diperhatikan

- ⚠️ Workbook punya 2 sheet (Biaya, Catatan); yang dianalisis: 'Biaya'. Pakai --sheet untuk sheet lain.
- ⚠️ 1 sel berisi rumus tanpa nilai tersimpan (mis. E16) sehingga dianggap kosong. Biasanya file dibuat aplikasi lain/belum dihitung: buka di Excel/LibreOffice, tekan Simpan sekali, lalu kirim ulang.
- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 18). Pakai --pertahankan-total bila itu data asli.
- ⚠️ Kolom 'Kategori': penulisan beda huruf besar-kecil/spasi digabung (Listrik & Air ← 'LISTRIK & AIR' / 'Listrik & Air' / 'listrik & air').

### Catatan

- Judul kolom (header) terdeteksi di baris 2 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.
- Tabel hasil disimpan ke per-kategori.csv.

```
Isi `per-kategori.csv` (UTF-8 BOM, bisa langsung dibuka di Excel; tambah `--excel-id` untuk
pemisah `;` dan koma desimal):
```csv
Kategori,Baris,Jumlah Nominal,% dari total
Sewa,3,13500000,48.9
Transport,5,8995000,32.6
Listrik & Air,3,4140000,15.0
Konsumsi,1,480000,1.7
ATK,3,470000,1.7
TOTAL,15,27585000,100.0
```

## Langkah 3 — `banding` Agustus vs September per kategori
```bash
python3 scripts/analisis.py banding biaya-operasional.xlsx --nilai Nominal --periode-a 2026-08 --periode-b 2026-09 --grup Kategori
```
```markdown
## Perbandingan Jumlah Nominal: Agu 2026 vs Sep 2026

_Sumber: biaya-operasional.xlsx — sheet 'Biaya'; 15 baris data_

| Kategori | Agu 2026 | Sep 2026 | Selisih | Perubahan % |
|---|---:|---:|---:|---:|
| Transport | Rp 1.595.000 | Rp 6.550.000 | Rp 4.955.000 | 310,7% |
| Konsumsi | Rp 0 | Rp 480.000 | Rp 480.000 | - |
| Listrik & Air | Rp 1.310.000 | Rp 1.580.000 | Rp 270.000 | 20,6% |
| Sewa | Rp 4.500.000 | Rp 4.500.000 | Rp 0 | 0,0% |
| ATK | Rp 150.000 | - | - | - |
| **TOTAL** | **Rp 7.555.000** | **Rp 13.110.000** | **Rp 5.555.000** | **73,5%** |

### Temuan (dihitung script)

- Jumlah Nominal: naik 73,5% (Rp 7.555.000 → Rp 13.110.000).
- Jumlah baris: 5 vs 6.
- Naik paling besar: Transport — naik 310,7% (Rp 1.595.000 → Rp 6.550.000).
- Hanya ada di Sep 2026: Konsumsi.
- Panjang periode beda (31 vs 30 hari). Rata-rata per hari: Rp 243.710 vs Rp 437.000 — naik 79,3% (Rp 243.710 → Rp 437.000).

### Saran grafik

Grafik batang berdampingan (clustered column): Agu 2026 vs Sep 2026 per Kategori.

### Perlu diperhatikan

- ⚠️ Workbook punya 2 sheet (Biaya, Catatan); yang dianalisis: 'Biaya'. Pakai --sheet untuk sheet lain.
- ⚠️ 1 sel berisi rumus tanpa nilai tersimpan (mis. E16) sehingga dianggap kosong. Biasanya file dibuat aplikasi lain/belum dihitung: buka di Excel/LibreOffice, tekan Simpan sekali, lalu kirim ulang.
- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 18). Pakai --pertahankan-total bila itu data asli.
- ⚠️ Periode Sep 2026 tidak sepenuhnya tercakup data (data 3 Jul 2026 s.d. 26 Sep 2026); angkanya bisa belum lengkap.
- ⚠️ 'ATK' ada di Sep 2026 tetapi semua nilainya kosong/tidak terbaca (ditulis '-').
- ⚠️ Kolom 'Kategori': penulisan beda huruf besar-kecil/spasi digabung (Listrik & Air ← 'LISTRIK & AIR' / 'Listrik & Air' / 'listrik & air').

### Catatan

- Judul kolom (header) terdeteksi di baris 2 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.

```

(`tren --nilai Nominal` juga dijalankan: Jul Rp 6.920.000 → Agu Rp 7.555.000 (+9,2%) → Sep
Rp 13.110.000 (+73,5%), dengan peringatan Jul & Sep tidak penuh.)

## Jawaban agent ke pengguna (disusun dari keluaran di atas, angka tidak diubah)
**Jawaban singkat:** Pengeluaran terbesar adalah **Sewa, Rp 13.500.000 (48,9% dari total
Rp 27.585.000)** selama Juli–September. September **naik 73,5%** dibanding Agustus
(Rp 7.555.000 → Rp 13.110.000).

| Kategori | Agu 2026 | Sep 2026 | Selisih | Perubahan % |
|---|---:|---:|---:|---:|
| Transport | Rp 1.595.000 | Rp 6.550.000 | Rp 4.955.000 | 310,7% |
| Konsumsi | Rp 0 | Rp 480.000 | Rp 480.000 | - |
| Listrik & Air | Rp 1.310.000 | Rp 1.580.000 | Rp 270.000 | 20,6% |
| Sewa | Rp 4.500.000 | Rp 4.500.000 | Rp 0 | 0,0% |
| ATK | Rp 150.000 | - | - | - |
| **TOTAL** | **Rp 7.555.000** | **Rp 13.110.000** | **Rp 5.555.000** | **73,5%** |

**Temuan:**
1. Sewa hampir separuh biaya (48,9%) dan tetap Rp 4.500.000/bulan — biaya tetap terbesar.
2. Kenaikan September hampir seluruhnya dari **Transport** (naik Rp 4.955.000), terutama ada
   pengeluaran "Ganti ban" Rp 5.400.000 pada 19 Sep. Ini tampak sebagai pengeluaran sekali, bukan
   kenaikan rutin — layak dicek apakah wajar.
3. Listrik & Air naik 20,6% (Rp 1.310.000 → Rp 1.580.000). Konsumsi Rp 480.000 baru muncul di
   September.

**Saran grafik:** batang berdampingan Agustus vs September per kategori (Excel: blok tabel →
*Insert → Clustered Column*). Untuk porsi per kategori: batang horizontal urut terbesar.

**Perlu dicek:**
- Sel **E16** (ATK, Tinta printer, 22 Sep) berisi rumus tanpa nilai tersimpan → tidak ikut
  dihitung. Buka file di Excel, tekan *Simpan* sekali, lalu kirim ulang agar ATK September terhitung.
- Baris 18 (TOTAL) tidak ikut dijumlah agar tidak dobel.
- "Listrik & Air", "listrik & air ", dan "LISTRIK & AIR" dihitung sebagai satu kategori.
- Data September baru sampai 26 Sep, jadi angka September bisa masih bertambah.

_Asumsi: sheet Biaya, kolom nilai Nominal, kolom kategori Kategori. File hasil: per-kategori.csv._

## Verifikasi manual (independen dari script)
- Sewa: 4.500.000 × 3 = **13.500.000** ✓; Transport: 850.000 + 920.000 + 675.000 + 1.150.000 +
  5.400.000 = **8.995.000** ✓; Listrik & Air: 1.250.000 + 1.310.000 + 1.580.000 = **4.140.000** ✓;
  ATK: 320.000 + 150.000 = **470.000** (E16 tidak terhitung) ✓; Konsumsi **480.000** ✓.
- Total: 13.500.000 + 8.995.000 + 4.140.000 + 470.000 + 480.000 = **27.585.000** ✓
  (kebetulan sama dengan nilai tersimpan sel TOTAL, karena nilai TOTAL itu juga tidak memuat E16).
- % Sewa: 13.500.000 ÷ 27.585.000 = 48,94% → **48,9%** ✓.
- Agustus: 4.500.000 + 1.310.000 + 920.000 + 675.000 + 150.000 = **7.555.000** ✓; September:
  4.500.000 + 1.580.000 + 1.150.000 + 5.400.000 + 480.000 = **13.110.000** ✓;
  (13.110.000 − 7.555.000) ÷ 7.555.000 = 73,53% → **73,5%** ✓.
- Transport: (6.550.000 − 1.595.000) ÷ 1.595.000 = 310,66% → **310,7%** ✓.
- Rata-rata per hari: 7.555.000 ÷ 31 = 243.709,7 → **Rp 243.710** ✓; 13.110.000 ÷ 30 = **Rp 437.000** ✓.
