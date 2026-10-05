# Uji 03 — Bendahara sekolah: CSV iuran komite (header baris 4, sel kosong, duplikat)

> Uji independen Tahap 6, 2026-09-25. `claude-code (simulasi agent)`.

## Skenario
Bendahara SD mengirim `iuran-komite.csv` (UTF-8 BOM, `;`, 3 baris judul di atas → header baris 4,
kelas ditulis `4A`/`4a`/`4 A`, nominal `50.000,-`/`Rp. 50.000`/`50000`, 2 nominal kosong, 1 kelas kosong,
3 baris dobel persis, 1 baris dobel NIS+bulan dengan keterangan "dobel input?", baris `TOTAL` di kolom E).
Pertanyaan: *"Tolong rapikan data iuran ini dan buatkan ringkasannya per kelas dan per bulan."*

Fixture: `python3 examples/buat_fixture_uji.py <folder>` → `iuran-komite.csv` (91 baris data).

## Langkah agent
```bash
$ python3 scripts/analisis.py profil iuran-komite.csv
```
```markdown
## Profil data

_Sumber: iuran-komite.csv; 91 baris data_

### Kolom

| Kolom | Tipe | Terisi | Kosong | % kosong | Nilai unik | Tidak valid | Contoh |
|---|---|---:|---:|---:|---:|---:|---|
| NIS | kode | 91 | 0 | 0,0% | 32 | 0 | 2023001, 2023002, 2023003 |
| Nama Siswa | teks | 91 | 0 | 0,0% | 32 | 0 | Siswa 4A-01, Siswa 4A-02, Siswa 4A-03 |
| Kelas | teks | 90 | 1 | 1,1% | 8 | 0 | 4A, 4 A, 4B |
| Bulan | teks | 91 | 0 | 0,0% | 3 | 0 | Juli, September, Agustus |
| Tanggal Bayar | tanggal | 91 | 0 | 0,0% | 30 | 0 | 11 Jul 2026, 11 Sep 2026, 12 Jul 2026 |
| Nominal | angka (uang) | 89 | 2 | 2,2% | 2 | 0 | Rp 50.000, Rp 75.000 |
| Keterangan | teks | 2 | 89 | 97,8% | 2 | 0 | belum setor ke bendahara, dobel input? |

### Nilai ekstrem (outlier, metode IQR 1,5×)

| Kolom | Rentang wajar | Jumlah outlier | Contoh (terjauh) |
|---|---|---:|---|
| Nominal | Rp 12.500 s.d. Rp 112.500 | 0 | - |

### Temuan (dihitung script)

- 91 baris data × 7 kolom (judul kolom di baris 4).
- Tipe kolom: 4 teks, 1 kode, 1 tanggal, 1 angka.
- 3 baris persis sama dengan baris lain (mis. baris 93 = baris 7). Periksa apakah data terinput dua kali.
- Kolom dengan ≥ 20% sel kosong: Keterangan.

### Saran grafik

Histogram untuk melihat sebaran kolom angka; box plot untuk menandai outlier. Untuk laporan, lanjutkan dengan 'ringkas', 'pivot', atau 'tren'.

### Perlu diperhatikan

- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 96). Pakai --pertahankan-total bila itu data asli.
- ⚠️ Kolom 'Kelas': penulisan beda huruf besar-kecil/spasi digabung (4A ← '4A' / '4a'; 4B ← '4B' / '4b'; 5A ← '5A' / '5a'; 5B ← '5B' / '5b').

### Catatan

- Judul kolom (header) terdeteksi di baris 4 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.

```

```bash
$ python3 scripts/analisis.py bersihkan iuran-komite.csv --buang-duplikat --keluar iuran-bersih.csv
```
```markdown
## Data dibersihkan

_Sumber: iuran-komite.csv; 91 baris data_

### Perubahan

| Kolom | Tipe | Perubahan |
|---|---|---|
| Kelas | teks | 4 kategori diseragamkan huruf besar-kecil: 4A ← 4A/4a; 4B ← 4B/4b; 5A ← 5A/5a |
| Tanggal Bayar | tanggal | 91 tanggal diseragamkan ke YYYY-MM-DD |
| Nominal | angka | 67 teks angka (Rp/titik ribuan/koma desimal) diubah ke angka murni |

### Temuan (dihitung script)

- File bersih ditulis: iuran-bersih.csv (88 baris data, 7 kolom).
- 1 baris Total/Jumlah tidak disalin.
- 3 baris duplikat dibuang (--buang-duplikat).
- File asli TIDAK diubah. Format: UTF-8, pemisah koma, angka tanpa titik ribuan dengan titik desimal.

### Saran grafik

Lanjutkan dengan 'profil' atau 'pivot' pada file bersih ini.

### Perlu diperhatikan

- ⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 96). Pakai --pertahankan-total bila itu data asli.
- ⚠️ Kolom 'Kelas': penulisan beda huruf besar-kecil/spasi digabung (4A ← '4A' / '4a'; 4B ← '4B' / '4b'; 5A ← '5A' / '5a'; 5B ← '5B' / '5b').

### Catatan

- Judul kolom (header) terdeteksi di baris 4 (baris di atasnya dianggap judul/keterangan). Bila salah, pakai --baris-header N.

```

```bash
$ python3 scripts/analisis.py pivot iuran-bersih.csv --grup Kelas --nilai Nominal --kolom-pivot Bulan
```
```markdown
## Jumlah Nominal per Kelas

_Sumber: iuran-bersih.csv; 88 baris data_

### Jumlah Nominal per Kelas × Bulan

| Kelas | Agustus | Juli | September | Total |
|---|---:|---:|---:|---:|
| 4 A | Rp 100.000 | Rp 50.000 | Rp 100.000 | Rp 250.000 |
| 4 B | Rp 50.000 | Rp 50.000 | - | Rp 100.000 |
| 4A | Rp 200.000 | Rp 250.000 | Rp 250.000 | Rp 700.000 |
| 4B | Rp 300.000 | Rp 400.000 | Rp 350.000 | Rp 1.050.000 |
| 5 A | Rp 75.000 | Rp 300.000 | Rp 75.000 | Rp 450.000 |
| 5 B | - | Rp 150.000 | Rp 150.000 | Rp 300.000 |
| 5A | Rp 450.000 | Rp 225.000 | Rp 375.000 | Rp 1.050.000 |
| 5B | Rp 600.000 | Rp 450.000 | Rp 375.000 | Rp 1.425.000 |
| (kosong) | - | - | Rp 50.000 | Rp 50.000 |
| **TOTAL** | **Rp 1.775.000** | **Rp 1.875.000** | **Rp 1.725.000** | **Rp 5.375.000** |

### Saran grafik

Grafik batang berkelompok (clustered bar): sumbu = Kelas, warna = Bulan. Alternatif: tabel dengan pewarnaan bersyarat (heatmap) di Excel.

```

```bash
$ python3 scripts/analisis.py pivot iuran-bersih.csv --grup Bulan --nilai Nominal
```
```markdown
## Jumlah Nominal per Bulan

_Sumber: iuran-bersih.csv; 88 baris data_

| Bulan | Baris | Jumlah Nominal | % dari total |
|---|---:|---:|---:|
| Juli | 31 | Rp 1.875.000 | 34,9% |
| Agustus | 28 | Rp 1.775.000 | 33,0% |
| September | 29 | Rp 1.725.000 | 32,1% |
| **TOTAL** | **88** | **Rp 5.375.000** | **100,0%** |

### Temuan (dihitung script)

- Tertinggi: Juli (Rp 1.875.000, 34,9% dari total).
- Terendah: September (Rp 1.725.000, 32,1% dari total).
- 3 kelompok; jumlah nominal keseluruhan: Rp 5.375.000.

### Saran grafik

Grafik batang horizontal urut terbesar. Pie/donat boleh karena ≤ 5 bagian dari satu total, tapi batang tetap lebih mudah dibandingkan.

```

```bash
$ python3 scripts/analisis.py ringkas iuran-bersih.csv --kolom Nominal
```
```markdown
## Ringkasan statistik

_Sumber: iuran-bersih.csv; 88 baris data_

### Kolom angka

| Kolom | Terisi | Jumlah | Rata-rata | Median | Min | Max |
|---|---:|---:|---:|---:|---:|---:|
| Nominal | 86 | Rp 5.375.000 | Rp 62.500 | Rp 62.500 | Rp 50.000 | Rp 75.000 |

### Temuan (dihitung script)

- 'Nominal': total Rp 5.375.000 dari 86 baris, rata-rata Rp 62.500 per baris (terkecil Rp 50.000, terbesar Rp 75.000).

### Saran grafik

Kartu angka (KPI) untuk total & rata-rata; bila ingin melihat pembagian per kategori, lanjutkan dengan 'pivot'.

```

## Jawaban akhir agent
**Jawaban singkat:** Setelah 3 baris dobel dibuang, iuran masuk **Rp 5.375.000** dari 86 pembayaran
(Juli Rp 1.875.000, Agustus Rp 1.775.000, September Rp 1.725.000). File rapi: `iuran-bersih.csv`.

**Perlu dicek:** kelas "4 A" dan "4A" (juga 4 B/5 A/5 B) masih terpisah — gabungkan dulu (lihat catatan);
1 baris kelas kosong (Rp 50.000); 2 nominal kosong (1 berketerangan "belum setor ke bendahara");
1 baris berketerangan "dobel input?" (NIS 2023012, Juli) tidak persis sama sehingga **tidak** dibuang
— bila memang dobel, total menjadi Rp 5.325.000.

## Verifikasi angka independen
| Angka | Kunci | Script | Cocok |
|---|---:|---:|:--:|
| Mentah (91 baris, 89 nominal) | 5.525.000 | — (profil) | — |
| Tanpa duplikat persis (88 baris, 86 nominal) | 5.375.000 | 5.375.000 | ✔ |
| Juli / Agustus / September | 1.875.000 / 1.775.000 / 1.725.000 | sama | ✔ |
| Per kelas sebenarnya 4A/4B/5A/5B | 950.000 / 1.200.000 / 1.500.000 / 1.725.000 | 4A 700.000 + "4 A" 250.000; 4B 1.050.000 + "4 B" 100.000 + (kosong) 50.000; 5A 1.050.000 + "5 A" 450.000; 5B 1.425.000 + "5 B" 300.000 | ✔ setelah dijumlah manual, ✘ sebagai tabel |
| Rata/median/min/max | 62.500 / 62.500 / 50.000 / 75.000 | sama | ✔ |
| Bila dobel NIS+bulan dibuang | 5.325.000 | tidak terdeteksi | ✘ |

## Catatan penguji
- ✔ Header baris 4 & baris TOTAL (di kolom E, bukan kolom A) terdeteksi; 4 gaya nominal terbaca semua.
- ✘ **"4 A" vs "4A" tidak diseragamkan** (hanya huruf besar-kecil & spasi tepi) → pivot per kelas terpecah
  jadi 9 baris. Untuk data sekolah/cabang ("Cab. Bogor"/"Cabang Bogor") ini sering terjadi.
- ✘ Duplikat hanya "persis sama"; tidak ada opsi kunci (mis. NIS+Bulan).
- Kolom pivot `Bulan` (teks nama bulan) diurutkan abjad (Agustus, Juli, September), bukan kronologis.
- Tidak bisa langsung menjawab "siapa yang belum bayar" (kunci: 11 kombinasi siswa×bulan) — wajar di luar
  cakupan, tapi bisa jadi saran fitur.
