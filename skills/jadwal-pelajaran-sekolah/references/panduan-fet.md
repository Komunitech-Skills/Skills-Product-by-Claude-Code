# Panduan opsional — FET (Free Timetabling Software)

**FET** (Free Timetabling Software) adalah program **gratis** lisensi **AGPL-3.0+** dari [lalescu.ro/liviu/fet/](https://lalescu.ro/liviu/fet/). Komunitech **tidak berafiliasi** dan **tidak menyertakan** installer FET di paket skill.

## Kapan memakai FET
- Sekolah besar (banyak guru/ruang/constraint khusus) setelah jadwal awal dari skill sudah bebas bentrok.
- Perlu optimasi global atau cetak otomatis banyak variasi.

## Langkah awam (Windows/Linux/Mac)
1. Unduh versi terbaru dari situs resmi (bukan mirror random).
2. Pasang seperti aplikasi biasa; buka FET.
3. Buat data baru → isi **days**, **hours**, **teachers**, **students (kelas)**, **subjects**, **activities** — bisa copy dari CSV yang skill berikan di chat.
4. Jalankan **Generate multiple timetables** → pilih solusi → export HTML/CSV.

## CLI (lanjutan)
Bila `fet-cl` ada di PATH:
```bash
fet-cl --inputfile=jadwal.fet --outputdir=./hasil-fet
```
Berkas `.fet` penuh biasanya dibuat/diedit di FET GUI; skill ini memberi **CSV penempatan** sebagai jalan cepat.

## Lisensi
Memakai FET berarti mematuhi AGPL (sumber tersedia dari pembuat FET). Skill Komunitech (skrip Python `scripts/`) adalah karya terpisah proprietary pembeli.
