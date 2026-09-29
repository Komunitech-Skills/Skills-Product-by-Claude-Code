# Uji 04 — Input tidak lengkap: HPHT tidak ada, siklus 35 hari

Penguji independen, 2026-09-29, `claude-code (simulasi agent)`. Data fiktif.

## Input pengguna
> "Bidan di sini. Ibu N, hamil anak kedua, siklusnya 35 hari. Hitung HPL dan usia kehamilannya
> sekarang ya."

## Perilaku agent (dengan skill)
Script dijalankan dulu untuk memastikan: `kehamilan --siklus 35 --tanggal-periksa 2026-09-29`
→ keluar 1: `Input tidak valid: isi HPHT atau data USG`. Agent tidak menebak dan bertanya
**sekali**:
```
Untuk menghitung HPL & usia kehamilan Ibu N, saya perlu:
1. HPHT (tanggal hari pertama haid terakhir)? Bila ibu lupa, tulis "lupa".
2. Apakah siklus 35 hari itu teratur?
3. Ada hasil USG? Bila ada: tanggal USG dan usia kehamilan saat USG (minggu + hari).
4. Tanggal periksa (default: hari ini, 29 September 2026)?
Catatan: siklus 35 hari masih dalam rentang 21–45 hari, jadi HPL akan digeser +7 hari
(modifikasi Naegele). Bila HPHT tidak diingat/siklus tidak teratur, penanggalan memakai USG
(idealnya trimester 1).
```

## Lanjutan (pengguna menjawab)
> "HPHT 15 Juni 2026, teratur. USG 10 Agustus 2026: 7 minggu 2 hari."
```
python3 scripts/klinis.py kehamilan --hpht 2026-06-15 --siklus 35 --tanggal-periksa 2026-09-29 --usg-tanggal 2026-08-10 --usg-minggu 7 --usg-hari 2
```
Hasil script: HPL Naegele 29 Mar 2027; HPL +280 (+7) 29 Mar 2027; UK HPHT 14 mg 1 hr;
HPL USG 27 Mar 2027; UK USG 14 mg 3 hr; selisih HPHT vs USG pada tanggal USG 2 hari, ambang
ACOG (USG ≤ 8 mg 6 hr) > 5 hari → **HPHT tetap dipakai**; Trimester 2.

## Verifikasi independen
- 15 Jun + 287 hr = 29 Mar 2027 ✔; (29 Sep − 15 Jun) = 106 hr − 7 = 99 = 14 mg 1 hr ✔.
- UK HPHT pada tanggal USG: 56 − 7 = 49 hr; USG 51 hr → selisih 2 ≤ 5 → HPHT ✔.
- HPL USG: 10 Agu + (280 − 51) = 27 Mar 2027 ✔.
- 20.000 kasus acak HPHT/siklus 21–45/USG + 13 kasus batas ambang ACOG tepat → 0 selisih.
- ACOG CO 700 (dibaca langsung di acog.org, "Reaffirmed 2025"): < 9 0/7: > 5 hr; 9 0/7–13 6/7:
  > 7; 14 0/7–15 6/7: > 7; 16 0/7–21 6/7: > 10; 22 0/7–27 6/7: > 14; ≥ 28 0/7: > 21 ✔ sama.

## Catatan penguji
- ✔ Bertanya sekali, daftar bernomor, tidak menebak HPHT.
- ⚠️ Bila siklus di luar 21–45 (mis. 50 hari) **dan** data USG tersedia, script menolak seluruh
  perhitungan ("pakai penanggalan USG") padahal USG sudah diberikan — agent harus menjalankan
  ulang tanpa HPHT (temuan S6).
- Buku KIA memakai HPHT hanya "pada siklus haid teratur" dan tidak memuat koreksi siklus;
  script menandai koreksi sebagai "modifikasi umum, bukan ACOG" — jujur, tetapi perlu ditinjau
  bidan/SpOG apakah koreksi siklus ingin dipakai di klinik.

Skor skenario: 9/10.
