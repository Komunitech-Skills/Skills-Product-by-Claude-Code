# Uji 02 — Normal: dokter umum, interpretasi MMSE 22 & AMT 6 (lansia)

Penguji independen, 2026-09-29, `claude-code (simulasi agent)`. Data fiktif.

## Input pengguna
> "Saya dokter umum di klinik lansia. Pasien Tn. H, 74 th, SD 6 tahun. MMSE total 22, AMT 6.
> Interpretasinya bagaimana, sesuai cutoff yang dipakai?"

## Langkah agent
- Peran: dokter → lanjut. Instrumen: MMSE & AMT (skor total, tanpa butir). MoCA tidak diminta.
```
python3 scripts/klinis.py kognitif --instrumen mmse --skor 22
python3 scripts/klinis.py kognitif --instrumen amt --skor 6
```

## Output agent (dengan skill)
```
🩺 Interpretasi skor skrining kognitif — Tn. H — 29 September 2026
Hasil:
- MMSE 22/30 → 18–23: di bawah batas skrining (rentang ringan) — pertimbangkan evaluasi lanjut
- AMT 6/10 → 4–7: gangguan ingatan sedang pada skrining — pertimbangkan evaluasi lanjut
Arti untuk tindak lanjut:
- Kedua skrining di bawah batas. Pertimbangkan evaluasi lanjut/rujukan sesuai penilaian klinis
  (mis. menyingkirkan delirium, depresi, gangguan penglihatan/pendengaran, efek obat).
Catatan: skor dipengaruhi pendidikan (6 tahun), bahasa, dan gangguan sensorik. Hasil skrining
  bukan diagnosis demensia/gangguan kognitif. Butir MMSE berhak cipta (PAR Inc.) — tidak dimuat.
Sumber: Folstein dkk. 1975; rentang Tombaugh & McIntyre 1992 (J Am Geriatr Soc 40:922-935).
  Hodkinson 1972 (Age Ageing 1:233-238); pembagian 8-10 / 4-7 / 0-3 formulir AMT
  Permenkes 67/2015 (PERLU REVIEW tenaga medis).
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis.
```

## Verifikasi
| Klaim | Sumber yang dicek penguji | Hasil |
|---|---|---|
| MMSE 24–30 / 18–23 / 0–17 | Tombaugh & McIntyre 1992 (rentang standar literatur; naskah berbayar, dicek lewat ringkasan sekunder) | ✔ konsisten |
| AMT 8–10 normal / 4–7 sedang / 0–3 berat | Permenkes 67/2015 via JDIH BPK → **HTTP 403** (naskah asli tidak terbaca); dikonfirmasi sekunder: halaman Puskesmas Wirobrajan (jogjakota.go.id), kemendukbangga.go.id | ✔ sekunder, **primer belum** |
| AMT secara internasional | Wikipedia/literatur: ambang bervariasi 6–10, umumnya ≤ 7–8 abnormal | Catatan: rentang Permenkes lebih "longgar" dari literatur Inggris; wajar karena pedoman lokal |
| Semua skor 0–30 MMSE & 0–10 AMT | `verifikasi.py` (tabel penuh) | 0 selisih |

## Catatan penguji
- ✔ Tidak ada label "demensia/pikun"; memakai "di bawah batas skrining".
- ⚠️ Script MMSE/AMT tidak meminta lama pendidikan; MMSE sering memakai ambang terkoreksi
  pendidikan di praktik Indonesia. Output hanya menyebut "dipengaruhi pendidikan" — cukup
  sebagai alat bantu, tetapi perlu ditinjau neurolog/dokter (temuan R-kognitif).
- ⚠️ Catatan delirium/depresi tidak muncul dari script AMT; agent menambahkan dari `references/kognitif.md`.

Skor skenario: 8/10.
