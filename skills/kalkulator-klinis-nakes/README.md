# Kalkulator Klinis Nakes: Hitung Pasti, Bersumber Jelas

**HPL, usia kehamilan, skrining preeklampsia, IMT, dan skor kognitif — dihitung script, lengkap
dengan kutipan pedoman. Untuk dokter, bidan, dan perawat.**

> ⚠️ **Status: PERLU REVIEW tenaga medis — belum untuk dijual.** Ambang & kalimat tindak lanjut
> wajib ditinjau dokter/bidan sebelum rilis (lihat `references/sumber-pedoman.md`, bagian
> "Status verifikasi"). Alat bantu keputusan untuk tenaga kesehatan, **bukan** pengganti
> penilaian klinis, **bukan** alat diagnosis, dan **tidak memberi dosis obat**.

## Manfaat
- ✅ **HPL & usia kehamilan tanpa salah hitung** — Naegele dan HPHT+280 hari, tahun kabisat,
  siklus ≠ 28 hari, plus cek otomatis "perlu penanggalan ulang dengan USG?" (ACOG 2017).
- ✅ **Skrining preeklampsia sesuai Buku KIA 2023** — isi faktor dengan bahasa biasa, MAP
  dihitung tepat (110/80 = 90,0 → bukan > 90), keluar kategori risiko + sumber.
- ✅ **IMT & kenaikan BB hamil** — kategori Asia-Pasifik **dan** Kemenkes sekaligus, lingkar
  perut, rekomendasi IOM 2009 (termasuk kembar).
- ✅ **Tafsir skor MMSE / MoCA-Ina / AMT** dengan koreksi pendidikan — tanpa melanggar hak cipta
  butir tes.
- ✅ **Catatan sesi stimulasi kognitif** rapi, siap tempel ke rekam medis — tanpa label
  diagnosis.

## Cocok untuk siapa
Dokter umum & dokter praktik mandiri, bidan (praktik mandiri, klinik, puskesmas), perawat klinik
lansia, ahli gizi, dan psikolog klinis/terapis yang menjalankan stimulasi kognitif. **Bukan untuk
pasien/awam** — bila yang bertanya bukan tenaga kesehatan, skill hanya memberi edukasi umum dan
menyarankan konsultasi.

## Contoh sebelum & sesudah
**Sebelum:** bidan menghitung HPL dengan kalender putar; siklus 35 hari tidak disesuaikan; MAP
dihitung kalkulator HP dan dibulatkan sebelum dibandingkan; faktor risiko preeklampsia dicentang
dari ingatan; sumber tidak tercatat.

**Sesudah (cukup ketik):** "Saya bidan. Bu R, G1, 36 th, hamil 14 minggu, TD 120/80, IMT 31,
ibunya dulu preeklampsia. Skrining preeklampsia."
→ MAP 93,3; **5 faktor sedang** (nullipara, usia ≥ 35, riwayat keluarga, IMT > 30, MAP > 90) →
**RISIKO SEDANG, memenuhi kriteria rujukan Buku KIA 2023**; daftar faktor yang belum ditanyakan;
sumber + penafian. Siap disalin ke rekam medis.

## Cara pakai
Setelah terpasang, ketik permintaan biasa, misalnya:
- "HPHT 10 Maret 2026, siklus 30 hari, USG 2 Mei usia 7 minggu 3 hari. HPL dan usia kehamilan
  hari ini?"
- "TB 155, BB sebelum hamil 62, sekarang 68 di usia 24 minggu. Kenaikannya sesuai?"
- "IMT dan lingkar perut: laki-laki, 165 cm, 72 kg, LP 92."
- "Skor MoCA-Ina 24, pendidikan 9 tahun. Interpretasinya?"
- "Buatkan catatan sesi stimulasi kognitif untuk peserta L-07 hari ini: ..."

Butuh Python 3 untuk perhitungan (sudah ada di kebanyakan komputer; Windows: `python`/`py`).
Tanpa Python, agent menghitung manual dengan rumus di `references/` dan memberi tanda
"verifikasi ulang".

## Batasan yang jujur perlu kamu tahu
- **Belum ditinjau dokter/bidan** (PERLU REVIEW). Beberapa ambang dikonfirmasi lewat sumber
  sekunder, bukan naskah asli (Buku KIA 2023, rentang AMT Permenkes 67/2015, tabel IMT
  Kemenkes) — rinciannya di `references/sumber-pedoman.md`.
- **Tanpa dosis obat** apa pun, termasuk aspirin/kalsium pencegahan preeklampsia.
- **Tanpa diagnosis** — hasil berupa kategori risiko/hasil skrining.
- **Butir MMSE & MoCA tidak disertakan** (hak cipta PAR Inc. / MoCA Cognition; MoCA wajib
  sertifikasi pemeriksa). Kamu memasukkan skor total dari formulir resmi milikmu.
- **MoCA-Ina:** studi validasi 2010 belum menetapkan titik potong khusus Indonesia; alat memakai
  batas asli 26 dan menyebutkannya.
- **Skor risiko kardiovaskular tidak disertakan di v1** — agar tidak salah hitung; pakai WHO
  HEARTS risk chart resmi.
- Tidak untuk anak/remaja (< 18 tahun) dan kehamilan bayi tabung (tanggal transfer embrio).
- Data minimal: cukup inisial/ID pasien. Skill tidak menyimpan data apa pun.

## Instalasi singkat
Salin folder `kalkulator-klinis-nakes` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah hasilnya bisa langsung jadi dasar rujukan?**
Hasil adalah alat bantu. Kategori risiko mengikuti pedoman yang dikutip, tetapi keputusan
rujukan dan tata laksana tetap penilaian klinis dokter/bidan yang memeriksa.

**Kenapa HPL Naegele dan HPHT+280 hari bisa beda 1–3 hari?**
Naegele memakai bulan kalender yang panjangnya berbeda-beda; +280 hari menghitung hari persis.
Keduanya ditampilkan agar sesuai kebiasaan praktikmu, dan catatan menjelaskan selisihnya.

**Pasien saya bertanya langsung ke agent, apa yang terjadi?**
Skill memastikan peran penanya. Bila bukan tenaga kesehatan, skill tidak menjalankan skrining
atau menafsirkan angka — hanya edukasi umum, anjuran konsultasi, dan kalimat tanda bahaya
(IGD/119).
