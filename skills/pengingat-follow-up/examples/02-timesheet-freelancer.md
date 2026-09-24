# 02 — Freelancer desain: timesheet 2 klien, format jam campur, rekap Jumat + draf ke klien

**Skenario:** Desainer lepas mencatat jam kerja sepanjang minggu lewat chat, dua klien dengan tarif berbeda,
lalu Jumat sore minta rekap dan draf pesan ke klien. Hari acuan: **Jumat, 2 Oktober 2026**. Klien fiktif.

## Input pengguna (persis, dikirim bertahap selama minggu itu, di sini diringkas dalam satu sesi Jumat)
> catat jam ya:
> Kopi Senja (tarif 175rb/jam): 28/9 1:45 revisi logo v2, 29/9 2,5 jam desain menu A3, 30/9 40m meeting online, kemarin 1j15m feed IG 6 slide
> Batik Laras (225rb/jam): Senin 3 jam foto katalog seleksi, 30/9 1,33 jam layout katalog, hari ini 50 menit kirim file final. Oh sama tgl 25/9 0:20 brief awal (itu minggu lalu)
> terus rekap minggu ini per klien, bikinin pesan buat masing2 klien

## Proses
```bash
S="python3 <folder-skill>/scripts/cek_jatuh_tempo.py --hari-ini 2026-10-02"
$S --teks catat-jam --klien "Kopi Senja"  --jam "1:45"     --tanggal "28/9"     --tarif "175rb"     --keterangan "Revisi logo v2"
$S --teks catat-jam --klien "Kopi Senja"  --jam "2,5"      --tanggal "29/9"     --tarif "175rb"     --keterangan "Desain menu A3"
$S --teks catat-jam --klien "Kopi Senja"  --jam "40m"      --tanggal "30/9"     --tarif "175rb"     --keterangan "Meeting online"
$S --teks catat-jam --klien "Kopi Senja"  --jam "1j15m"    --tanggal "kemarin"  --tarif "175rb"     --keterangan "Feed IG 6 slide"
$S --teks catat-jam --klien "Batik Laras" --jam "3 jam"    --tanggal "Senin"    --tarif "Rp225.000" --keterangan "Foto katalog - seleksi"
$S --teks catat-jam --klien "Batik Laras" --jam "1,33"     --tanggal "30/9"     --tarif "Rp225.000" --keterangan "Layout katalog"
$S --teks catat-jam --klien "Batik Laras" --jam "50 menit" --tanggal "hari ini" --tarif "Rp225.000" --keterangan "Kirim file final"
$S --teks catat-jam --klien "Batik Laras" --jam "0:20"     --tanggal "25/9"     --tarif "Rp225.000" --keterangan "Brief awal (minggu lalu)"
$S --teks timesheet --periode minggu-ini
$S --teks timesheet --periode minggu-ini --klien "Kopi Senja"
$S --teks timesheet --periode minggu-ini --klien "Batik Laras"
```

## Output script apa adanya (menunjukkan CACAT)
```
Tercatat: Kopi Senja, Senin, 28 September 2026, 1 jam 45 menit, tarif Rp 175.000/jam.
Catatan: Tahun tidak disebut; dipakai 28 Sep 2026 (tanggal terdekat dari hari ini). Ubah bila maksudnya lain.
Tercatat: Kopi Senja, Selasa, 29 September 2026, 2 jam 30 menit, tarif Rp 175.000/jam.
Catatan: Tahun tidak disebut; ...
Tercatat: Kopi Senja, Rabu, 30 September 2026, 40 menit, tarif Rp 175.000/jam.
Catatan: Tahun tidak disebut; ...
Tercatat: Kopi Senja, Kamis, 1 Oktober 2026, 1 jam 15 menit, tarif Rp 175.000/jam.
Tercatat: Batik Laras, Senin, 5 Oktober 2026, 3 jam, tarif Rp 225.000/jam.      <-- SALAH: "Senin" = 28 Sep (sudah lewat), bukan 5 Okt
Tercatat: Batik Laras, Rabu, 30 September 2026, 1 jam 20 menit, tarif Rp 225.000/jam.
Catatan: Durasi 1,33 dibulatkan ke 80 menit.
Catatan: Tahun tidak disebut; ...
Tercatat: Batik Laras, Jumat, 2 Oktober 2026, 50 menit, tarif Rp 225.000/jam.
Tercatat: Batik Laras, Jumat, 25 September 2026, 20 menit, tarif Rp 225.000/jam.
Catatan: Tahun tidak disebut; ...
```
```
REKAP TIMESHEET 28 Sep 2026 - 4 Okt 2026

- Batik Laras: 2 jam 10 menit (≈ 2,17 jam) | 2 jam 10 menit x Rp 225.000/jam = Rp 487.500
- Kopi Senja: 6 jam 10 menit (≈ 6,17 jam) | 6 jam 10 menit x Rp 175.000/jam = Rp 1.079.167

Total semua klien: 8 jam 20 menit | Rp 1.566.667

Nilai dihitung per menit (menit x tarif / 60), dibulatkan ke rupiah terdekat per klien.
```
3 jam hari Senin untuk Batik Laras (Rp 675.000) **hilang** dari rekap minggu ini tanpa peringatan apa pun,
karena script menyimpannya di Senin **depan** (5 Okt). Nama hari di `catat-jam` selalu dibaca ke depan,
walaupun jam kerja hampir selalu dicatat untuk hari yang sudah lewat.

## Output yang seharusnya diberikan agent (setelah penguji mengoreksi baris Senin menjadi `--tanggal "28/9"`)
Agent yang teliti bisa menangkap "Senin, 5 Oktober 2026" di konfirmasi dan menanyakannya; SKILL.md tidak
memperingatkan hal ini. Dengan tanggal yang benar, rekap menjadi:

```
REKAP TIMESHEET 28 Sep 2026 - 4 Okt 2026

- Batik Laras: 5 jam 10 menit (≈ 5,17 jam) | 5 jam 10 menit x Rp 225.000/jam = Rp 1.162.500
- Kopi Senja: 6 jam 10 menit (≈ 6,17 jam) | 6 jam 10 menit x Rp 175.000/jam = Rp 1.079.167

Total semua klien: 11 jam 20 menit | Rp 2.241.667
```

**Draf ke Kopi Senja** (output `timesheet --klien "Kopi Senja"`, apa adanya):
```
DRAF PESAN KE KLIEN (cek dulu, lalu kirim sendiri):
Selamat sore Kopi Senja, berikut rekap jam kerja periode 28 Sep 2026 - 4 Okt 2026: total 6 jam 10 menit (6,17 jam), nilai Rp 1.079.167. Rincian:
- 28 Sep 2026: 1 jam 45 menit - Revisi logo v2
- 29 Sep 2026: 2 jam 30 menit - Desain menu A3
- 30 Sep 2026: 40 menit - Meeting online
- 1 Okt 2026: 1 jam 15 menit - Feed IG 6 slide
Mohon konfirmasinya sebelum kami terbitkan invoice. Terima kasih.
```

**Draf ke Batik Laras** (setelah koreksi tanggal Senin):
```
DRAF PESAN KE KLIEN (cek dulu, lalu kirim sendiri):
Selamat sore Batik Laras, berikut rekap jam kerja periode 28 Sep 2026 - 4 Okt 2026: total 5 jam 10 menit (5,17 jam), nilai Rp 1.162.500. Rincian:
- 28 Sep 2026: 3 jam - Foto katalog - seleksi
- 30 Sep 2026: 1 jam 20 menit - Layout katalog
- 2 Okt 2026: 50 menit - Kirim file final
Mohon konfirmasinya sebelum kami terbitkan invoice. Terima kasih.
```
Catatan untuk pemilik: "1,33 jam" dibulatkan ke 80 menit. Brief 25 Sep (20 menit) masuk minggu lalu, jadi tidak
ikut rekap ini. Mau dibuatkan invoice? Pakai skill `buat-invoice` dengan angka di atas.

## Verifikasi angka (independen)
| Angka | Script | Hitung ulang | Status |
|---|---|---|---|
| Kopi Senja menit 105+150+40+75 | 370 (6 j 10 m) | 370 | cocok |
| Kopi Senja 370 × 175.000 / 60 = 1.079.166,67 | Rp 1.079.167 | 1.079.167 | cocok (0,5 ke atas) |
| Batik Laras versi script 80+50 = 130 × 225.000/60 | Rp 487.500 | 487.500 | cocok secara aritmetika |
| Batik Laras bila Senin = 28 Sep: 310 × 225.000/60 | — | Rp 1.162.500 | script **kurang Rp 675.000** |
| 6,17 jam (370/60 = 6,1667) | 6,17 | 6,17 | cocok |
| "1,33" jam = 79,8 menit | 80 menit + catatan | 79,8 → 80 | cocok |

## Catatan penguji
- Bagus: aritmetika persis (pecahan, bulat sekali per klien), tarif berbeda per klien, format jam campur
  ("1:45", "2,5", "40m", "1j15m", "3 jam", "50 menit") terbaca. Draf ke klien rapi & siap kirim, dengan rincian
  per tanggal. Entri minggu lalu tidak bocor ke minggu ini.
- **Cacat BERAT:** nama hari di `catat-jam` ("Senin", "Kamis") dibaca ke **depan** → jam kerja tercatat di masa
  depan, hilang dari rekap minggu ini, draf ke klien kurang tagih. Tidak ada peringatan "tanggal di masa depan".
  "Jumat" diucapkan hari Jumat juga dipindah ke Jumat depan.
- Ringan: catatan "Tahun tidak disebut" muncul di hampir setiap entri (bising). "1.30" (gaya titik untuk jam)
  dibaca 1,3 jam = 78 menit tanpa catatan (lihat HASIL-UJI).

---
## Uji ulang v1.0.1 (2026-09-24): input yang sama, output script apa adanya
Cacat nama hari sudah diperbaiki. "Senin" diucapkan Jumat 2 Okt kini tercatat **Senin, 28 September 2026**.
Catatan "Tahun tidak disebut" untuk tanggal kerja yang sudah lewat tidak muncul lagi.
```
Tercatat: Batik Laras, Senin, 28 September 2026, 3 jam, tarif Rp 225.000/jam.
Tercatat: Batik Laras, Rabu, 30 September 2026, 1 jam 20 menit, tarif Rp 225.000/jam.
Catatan: 1,33 dibaca 1,33 jam (desimal). Kalau maksudnya 1 jam 33 menit, tulis 1:33. Durasi 1,33 dibulatkan ke 80 menit.
...
REKAP TIMESHEET 28 Sep 2026 - 4 Okt 2026

- Batik Laras: 5 jam 10 menit (≈ 5,17 jam) | 5 jam 10 menit x Rp 225.000/jam = Rp 1.162.500
- Kopi Senja: 6 jam 10 menit (≈ 6,17 jam) | 6 jam 10 menit x Rp 175.000/jam = Rp 1.079.167

Total semua klien: 11 jam 20 menit | Rp 2.241.667
```
Draf ke Batik Laras sama persis dengan draf "seharusnya" di atas (total 5 jam 10 menit, Rp 1.162.500).
Tanggal kerja di masa depan kini ditolak: `--tanggal "besok"` / `"3 Okt"` saat Jumat 2 Okt menghasilkan
`ERROR: tanggal kerja Sabtu, 3 Oktober 2026 ada di masa depan ...`, dan `"Senin depan"` juga ditolak.
`"1.30"` ditolak sebagai ambigu dan ditanyakan ("1 jam 30 menit, atau 1,30 jam?").

Selisih Rp 675.000 vs Rp 1.162.500: **Rp 1.162.500 benar** untuk data skenario ini (310 menit × 225.000 / 60).
Rp 675.000 adalah angka dari tes regresi pembuat yang datanya berbeda (4:30 × Rp 150.000 = 270 menit → Rp 675.000).
Kebetulan angkanya sama dengan porsi hari Senin yang dulu hilang (3 jam × Rp 225.000).
