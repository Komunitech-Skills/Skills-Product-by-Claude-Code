# Uji 02 — HRD: CSV absensi/lembur (cp1252, pemisah `;`)

> Uji independen Tahap 6, 2026-09-25. `claude-code (simulasi agent)`.

## Skenario
HRD pabrik mengirim `lembur-sep-2026.csv` (ekspor Excel Windows lama: **cp1252**, pemisah `;`,
nama beraksen `Dédé Kurnia`, `André Gunawan`, NIK 16 digit, jam lembur `4,5`, uang `Rp 78.030`,
3 sel Jam Lembur kosong, 40 baris lembur `0`, 1 baris dobel). Pertanyaan:
*"Rata-rata jam lembur per divisi berapa, dan siapa 5 orang yang lemburnya paling banyak?"*

Fixture: `python3 examples/buat_fixture_uji.py <folder>` → `lembur-sep-2026.csv` (383 baris, 38 karyawan, 5 divisi).

## Langkah agent
```bash
$ python3 scripts/analisis.py profil lembur-sep-2026.csv
```
```markdown
## Profil data

_Sumber: lembur-sep-2026.csv; 383 baris data_

### Kolom

| Kolom | Tipe | Terisi | Kosong | % kosong | Nilai unik | Tidak valid | Contoh |
|---|---|---:|---:|---:|---:|---:|---|
| NIK | kode | 383 | 0 | 0,0% | 38 | 0 | (disembunyikan: data pribadi) |
| Nama Karyawan | teks | 383 | 0 | 0,0% | 38 | 0 | Agus Salim, Budi Hartono, Citra Dewi |
| Divisi | teks | 383 | 0 | 0,0% | 5 | 0 | Produksi, Gudang, Admin |
| Tanggal | tanggal | 383 | 0 | 0,0% | 26 | 0 | 3 Sep 2026, 5 Sep 2026, 7 Sep 2026 |
| Jam Lembur | angka | 380 | 3 | 0,8% | 10 | 0 | 4,50, 1, 2 |
| Uang Lembur | angka (uang) | 380 | 3 | 0,8% | 10 | 0 | Rp 78.030, Rp 17.340, Rp 34.680 |
| Keterangan | teks | 156 | 227 | 59,3% | 2 | 0 | Lembur shift malam, Hadir |

### Nilai ekstrem (outlier, metode IQR 1,5×)

| Kolom | Rentang wajar | Jumlah outlier | Contoh (terjauh) |
|---|---|---:|---|
| Jam Lembur | -2 s.d. 6 | 0 | - |
| Uang Lembur | -Rp 34.680 s.d. Rp 104.040 | 0 | - |

### Temuan (dihitung script)

- 383 baris data × 7 kolom (judul kolom di baris 1).
- Tipe kolom: 3 teks, 2 angka, 1 kode, 1 tanggal.
- 1 baris persis sama dengan baris lain (mis. baris 384 = baris 12). Periksa apakah data terinput dua kali.
- Kolom dengan ≥ 20% sel kosong: Keterangan.

### Saran grafik

Histogram untuk melihat sebaran kolom angka; box plot untuk menandai outlier. Untuk laporan, lanjutkan dengan 'ringkas', 'pivot', atau 'tren'.

### Perlu diperhatikan

- ⚠️ File bukan UTF-8; dibaca sebagai cp1252 (ANSI Excel Windows). Bila ada huruf aneh, simpan ulang dari Excel sebagai 'CSV UTF-8'.
- ⚠️ Kolom yang tampak berisi DATA PRIBADI/SENSITIF: NIK. Contoh isinya tidak ditampilkan; jangan bagikan file/hasil mentah ke pihak lain tanpa izin (UU PDP No. 27/2022).

```

```bash
$ python3 scripts/analisis.py pivot lembur-sep-2026.csv --grup Divisi --nilai Jam Lembur --fungsi rata
```
```markdown
## Rata-rata Jam Lembur per Divisi

_Sumber: lembur-sep-2026.csv; 383 baris data_

| Divisi | Baris | Rata-rata Jam Lembur |
|---|---:|---:|
| Produksi | 135 | 2,27 |
| Gudang | 79 | 1,84 |
| QC | 46 | 1,82 |
| Sales | 79 | 1,76 |
| Admin | 44 | 1,75 |
| **TOTAL** | **383** | **1,96** |

### Temuan (dihitung script)

- Tertinggi: Produksi (2,27).
- Terendah: Admin (1,75).
- 5 kelompok; rata-rata jam lembur keseluruhan: 1,96.

### Saran grafik

Grafik batang horizontal, urut dari terbesar ke terkecil.

### Perlu diperhatikan

- ⚠️ File bukan UTF-8; dibaca sebagai cp1252 (ANSI Excel Windows). Bila ada huruf aneh, simpan ulang dari Excel sebagai 'CSV UTF-8'.
- ⚠️ Kolom yang tampak berisi DATA PRIBADI/SENSITIF: NIK. Contoh isinya tidak ditampilkan; jangan bagikan file/hasil mentah ke pihak lain tanpa izin (UU PDP No. 27/2022).

```

```bash
$ python3 scripts/analisis.py pivot lembur-sep-2026.csv --grup Divisi --nilai Jam Lembur
```
```markdown
## Jumlah Jam Lembur per Divisi

_Sumber: lembur-sep-2026.csv; 383 baris data_

| Divisi | Baris | Jumlah Jam Lembur | % dari total |
|---|---:|---:|---:|
| Produksi | 135 | 302,50 | 40,6% |
| Gudang | 79 | 145 | 19,5% |
| Sales | 79 | 137,50 | 18,4% |
| QC | 46 | 83,50 | 11,2% |
| Admin | 44 | 77 | 10,3% |
| **TOTAL** | **383** | **745,50** | **100,0%** |

### Temuan (dihitung script)

- Tertinggi: Produksi (302,50, 40,6% dari total).
- Terendah: Admin (77, 10,3% dari total).
- 5 kelompok; jumlah jam lembur keseluruhan: 745,50.

### Saran grafik

Grafik batang horizontal urut terbesar. Pie/donat boleh karena ≤ 5 bagian dari satu total, tapi batang tetap lebih mudah dibandingkan.

### Perlu diperhatikan

- ⚠️ File bukan UTF-8; dibaca sebagai cp1252 (ANSI Excel Windows). Bila ada huruf aneh, simpan ulang dari Excel sebagai 'CSV UTF-8'.
- ⚠️ Kolom yang tampak berisi DATA PRIBADI/SENSITIF: NIK. Contoh isinya tidak ditampilkan; jangan bagikan file/hasil mentah ke pihak lain tanpa izin (UU PDP No. 27/2022).

```

```bash
$ python3 scripts/analisis.py top lembur-sep-2026.csv --grup Nama --nilai Jam Lembur --n 5
```
```markdown
## 5 teratas Nama Karyawan menurut Jumlah Jam Lembur

_Sumber: lembur-sep-2026.csv; 383 baris data_

| # | Nama Karyawan | Baris | Jumlah Jam Lembur | % dari total | % kumulatif |
|---:|---|---:|---:|---:|---:|
| 1 | Eko Prasetyo | 16 | 41 | 5,5% | 5,5% |
| 2 | Ferry Irawan | 16 | 35 | 4,7% | 10,2% |
| 3 | Agus Salim | 14 | 32 | 4,3% | 14,5% |
| 4 | Rizky Ramadhan | 14 | 30,50 | 4,1% | 18,6% |
| 5 | Gita Anggraini | 10 | 28,50 | 3,8% | 22,4% |
| - | Lainnya (33 Nama Karyawan) | 313 | 578,50 | 77,6% | - |

### Temuan (dihitung script)

- 5 teratas (Eko Prasetyo, Ferry Irawan, Agus Salim...) menyumbang 22,4% dari total 745,50.

### Saran grafik

Grafik batang horizontal urut nilai + garis % kumulatif (diagram Pareto).

### Perlu diperhatikan

- ⚠️ File bukan UTF-8; dibaca sebagai cp1252 (ANSI Excel Windows). Bila ada huruf aneh, simpan ulang dari Excel sebagai 'CSV UTF-8'.
- ⚠️ Kolom yang tampak berisi DATA PRIBADI/SENSITIF: NIK. Contoh isinya tidak ditampilkan; jangan bagikan file/hasil mentah ke pihak lain tanpa izin (UU PDP No. 27/2022).

```

## Jawaban akhir agent
**Jawaban singkat:** Rata-rata lembur per catatan harian tertinggi di **Produksi (2,27 jam)**, lalu
Gudang 1,84, QC 1,82, Sales 1,76, Admin 1,75 (keseluruhan 1,96 jam). Lima orang dengan total lembur
terbanyak September: Eko Prasetyo (41 jam), Ferry Irawan (35), Agus Salim (32), Rizky Ramadhan (30,50),
Gita Anggraini (28,50) — bersama 22,4% dari total 745,50 jam.

**Perlu dicek:** file dibaca sebagai cp1252 (nama beraksen tampil benar: Dédé, André); ada 1 baris
persis dobel (baris 384 = baris 12, Agus Salim 25/09) yang ikut terhitung — bila memang salah input,
total Agus Salim jadi 30 jam dan urutan tetap; 3 sel Jam Lembur kosong tidak dihitung (bukan dianggap 0);
kolom NIK = data pribadi (UU PDP) — hanya ringkasan yang ditampilkan.
(Asumsi: "rata-rata" = per catatan harian yang terisi, termasuk catatan lembur 0. Bila maksudnya rata-rata
per karyawan per bulan, skill tidak punya perintah langsung — lihat catatan.)

## Verifikasi angka independen (parser sendiri: csv + Decimal, tanpa script skill)
| Divisi | n terisi | Jumlah | Rata (kunci) | Median (kunci) | Script |
|---|---:|---:|---:|---:|:--:|
| Produksi | 133 | 302,5 | 2,2744 | 2 | 2,27 / 302,50 / med 2 ✔ |
| Gudang | 79 | 145 | 1,8354 | 1,5 | ✔ |
| QC | 46 | 83,5 | 1,8152 | 1,5 | ✔ |
| Sales | 78 | 137,5 | 1,7628 | 1,5 | ✔ |
| Admin | 44 | 77 | 1,75 | 1,5 | ✔ |
| Semua | 380 | 745,5 | 1,9618 | 2 | ✔ |
Top-5 kunci: Eko 41, Ferry 35, Agus 32, Rizky 30,5, Gita 28,5 (ke-6 Gilang 28) ✔. 40 baris bernilai 0 ✔ (`--filter "Jam Lembur=0"`).

## Catatan penguji
- ✔ cp1252 + `;` + koma desimal terdeteksi otomatis; NIK sebagai `kode` dan disembunyikan di profil.
- ✘ Kolom "Baris" di pivot rata-rata = 135 untuk Produksi padahal pembaginya 133 (2 sel kosong). Pengguna
  yang mengecek 302,5 ÷ 135 = 2,24 akan mengira salah. Pivot tidak memberi peringatan sel kosong.
- ✘ Duplikat hanya diperingatkan di `profil`, tidak di `pivot`/`top` yang angkanya terpengaruh.
- ✘ Tidak ada cara menghitung "rata-rata per karyawan" (butuh hitung-unik / group 2 tingkat).
  Kunci: Produksi 21,61 · QC 20,88 · Sales 19,64 · Gudang 18,13 · Admin 15,4 jam/orang — urutannya
  **berbeda** dari rata per catatan; agent wajib menanyakan maksud "rata-rata".
- ✘ `top --grup NIK` menampilkan NIK lengkap sebagai label (bertentangan dengan `references/format-didukung.md`
  "tidak ditampilkan sebagai label di top").
- Kolom "Uang Lembur" tidak ditandai sensitif (gaji ditandai, uang lembur tidak) — minor.
