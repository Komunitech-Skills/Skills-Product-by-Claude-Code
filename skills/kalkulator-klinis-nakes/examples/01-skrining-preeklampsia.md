# 01 — Skrining preeklampsia (bidan, ANC 14 minggu)

> Contoh dari pembuat skill (data fiktif). Belum uji independen — hasil uji ditulis penguji di
> `HASIL-UJI.md`.

**Input pengguna:** "Saya bidan. Bu R, G1P0A0, 36 th, hamil 14 minggu, TD 120/80, IMT sebelum
hamil 31, ibunya dulu preeklampsia. Skrining preeklampsia ya."

**Perintah yang dijalankan agent:**
```
python3 scripts/klinis.py preeklampsia --faktor nullipara,riwayat-keluarga --sistolik 120 --diastolik 80 --usia-ibu 36 --imt 31
```
**Output script (v1.0.x terbaru):**
```
Pedoman: Buku KIA (cetakan 2025)
KATEGORI: BERISIKO PREEKLAMPSIA - perlu rujukan terencana (>= 2 faktor risiko sedang) - Buku KIA (cetakan 2025)
Arti: Memenuhi kriteria ibu berisiko preeklampsia menurut Buku KIA. Buku KIA: pemeriksaan kehamilan, proses melahirkan, dan pemeriksaan nifas dilaksanakan di Rumah Sakit; lakukan rujukan terencana (tidak perlu menunggu inpartu). Pelaksanaan sesuai protokol fasilitas & keputusan dokter.
Faktor risiko tinggi: -
Faktor risiko sedang: MAP >= 90 mmHg; Nullipara (kehamilan pertama); Obesitas sebelum hamil (IMT > 30 kg/m2); Riwayat preeklampsia pada ibu atau saudara perempuan; Usia ibu >= 35 tahun
Faktor terisi otomatis dari angka: map-90; usia-ibu-35; obesitas
MAP (mmHg): 93.3
Catatan: Aturan kategori: Buku KIA (cetakan 2025): >= 2 faktor risiko sedang dan/atau >= 1 faktor risiko tinggi -> ibu berisiko preeklampsia -> rujukan terencana. Hanya faktor dari daftar pedoman ini yang dihitung (tidak dicampur).
Catatan: Buku KIA: skrining dilakukan pada usia kehamilan < 20 minggu.
Catatan: Keputusan terapi/obat pencegahan (termasuk dosis) BUKAN bagian alat ini - ikuti PNPK/pedoman dan resep dokter.
Sumber: Kemenkes RI, Buku Kesehatan Ibu dan Anak (Buku KIA) edisi terbaru - cetakan Ditjen Kesehatan Primer dan Komunitas 2025 (ISBN 978-623-301-149-5) - lembar skrining preeklampsia usia kehamilan < 20 minggu
Sumber: Rumus MAP = (sistolik + 2 x diastolik) / 3; ambang MAP >= 90 mmHg dari Buku KIA (cetakan 2025)
PENTING: Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap pada dokter/bidan yang memeriksa.
```
**Jawaban agent ke bidan:**
```
🩺 Skrining faktor risiko preeklampsia — Bu R — 29 September 2026

Tanda bahaya: tidak ada (TD 120/80 < 140/90; gejala bahaya tidak disebut — mohon konfirmasi
tidak ada nyeri kepala hebat, pandangan kabur, nyeri ulu hati, bengkak mendadak).

Hasil:
- MAP 93,3 mmHg (≥ 90)
- Kategori (Buku KIA cetakan 2025): BERISIKO PREEKLAMPSIA — perlu rujukan terencana
  (≥ 2 faktor risiko sedang)
  Faktor sedang (5): nullipara; usia ≥ 35 tahun; riwayat preeklampsia pada ibu;
  obesitas pra-hamil (IMT > 30); MAP ≥ 90. Faktor tinggi: tidak ada.
- Belum ditanyakan: diabetes, penyakit ginjal, autoimun/APS, proteinuria — mohon dilengkapi
  bila belum diperiksa.

Arti untuk tindak lanjut:
- Memenuhi kriteria ibu berisiko preeklampsia menurut Buku KIA: pemeriksaan kehamilan,
  proses melahirkan, dan pemeriksaan nifas dilaksanakan di Rumah Sakit; lakukan rujukan
  terencana (tidak perlu menunggu inpartu). Pelaksanaan sesuai protokol fasilitas & keputusan
  dokter. Keputusan terapi/obat pencegahan (termasuk dosis) bukan bagian alat ini.

Catatan: aturan kategori dari Buku KIA (≥ 2 sedang dan/atau ≥ 1 tinggi); skrining < 20 minggu.
Sumber: Kemenkes RI, Buku KIA edisi terbaru (cetakan 2025) — lembar skrining preeklampsia
< 20 minggu; rumus MAP = (S + 2D)/3, ambang MAP ≥ 90.
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap
pada dokter/bidan yang memeriksa.
```

Verifikasi manual: MAP = (120 + 160)/3 = 93,33 ≥ 90 ✓. Faktor sedang = 5 (≥ 2) ✓, tinggi = 0.

**Varian tanda bahaya (v1.0.1):** pasien sama dengan TD 170/115 →
`python3 scripts/klinis.py preeklampsia --faktor nullipara,riwayat-keluarga --sistolik 170 --diastolik 115`
→ `!! TANDA BAHAYA: TD 170/115 mmHg dalam rentang BERAT` · `KATEGORI: TANDA BAHAYA - SEGERA
EVALUASI/RUJUK` · arti "SEGERA evaluasi/rujuk sesuai protokol kegawatdaruratan fasilitas Anda"
(sumber NICE NG133 & ACOG PB 222); tidak ada kalimat "ANC rutin".
