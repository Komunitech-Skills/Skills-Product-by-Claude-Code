# 01 — Skrining preeklampsia (bidan, ANC 14 minggu)

> Contoh dari pembuat skill (data fiktif). Belum uji independen — hasil uji ditulis penguji di
> `HASIL-UJI.md`.

**Input pengguna:** "Saya bidan. Bu R, G1P0A0, 36 th, hamil 14 minggu, TD 120/80, IMT sebelum
hamil 31, ibunya dulu preeklampsia. Skrining preeklampsia ya."

**Perintah yang dijalankan agent:**
```
python3 scripts/klinis.py preeklampsia --faktor nullipara,riwayat-keluarga --sistolik 120 --diastolik 80 --usia-ibu 36 --imt 31
```
**Output script:**
```
Pedoman: kia
KATEGORI: RISIKO SEDANG (>= 2 faktor sedang)
Arti: Terdapat >= 2 faktor risiko sedang. Sesuai Buku KIA 2023 memenuhi kriteria rujukan/konsultasi dokter; pertimbangkan tindak lanjut sesuai PNPK/pedoman.
Faktor risiko tinggi: -
Faktor risiko sedang: MAP > 90 mmHg; Nullipara (kehamilan pertama); Obesitas sebelum hamil (IMT > 30 kg/m2); Riwayat preeklampsia pada ibu atau saudara perempuan; Usia ibu >= 35 tahun
Faktor terisi otomatis dari angka: map-90; usia-ibu-35; obesitas
MAP (mmHg): 93.3
Catatan: Buku KIA: skrining dilakukan pada usia kehamilan < 20 minggu.
Catatan: Keputusan terapi/obat pencegahan (termasuk dosis) BUKAN bagian alat ini - ikuti PNPK/pedoman dan resep dokter.
Sumber: Kemenkes RI, Buku Kesehatan Ibu dan Anak (Buku KIA) 2023 - lembar skrining preeklampsia usia kehamilan < 20 minggu
Sumber: Rumus MAP = (sistolik + 2 x diastolik) / 3; ambang MAP > 90 mmHg dari Buku KIA 2023
PENTING: Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap pada dokter/bidan yang memeriksa.
```
**Jawaban agent ke bidan:**
```
🩺 Skrining faktor risiko preeklampsia — Bu R — 29 September 2026

Hasil:
- MAP 93,3 mmHg (> 90)
- Kategori: RISIKO SEDANG (≥ 2 faktor sedang)
  Faktor sedang (5): nullipara; usia ≥ 35 tahun; riwayat preeklampsia pada ibu;
  obesitas pra-hamil (IMT > 30); MAP > 90. Faktor tinggi: tidak ada.
- Belum ditanyakan: diabetes, penyakit ginjal, autoimun/APS, proteinuria — mohon dilengkapi
  bila belum diperiksa.

Arti untuk tindak lanjut:
- Sesuai Buku KIA 2023 memenuhi kriteria rujukan/konsultasi dokter; pertimbangkan tindak
  lanjut sesuai PNPK/pedoman. Keputusan terapi/obat pencegahan (termasuk dosis) bukan bagian
  alat ini.

Sumber: Kemenkes RI, Buku KIA 2023 — lembar skrining preeklampsia < 20 minggu;
rumus MAP = (S + 2D)/3.
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap
pada dokter/bidan yang memeriksa.
```

Verifikasi manual: MAP = (120 + 160)/3 = 93,33 > 90 ✓. Faktor sedang = 5 (≥ 2) ✓, tinggi = 0.
