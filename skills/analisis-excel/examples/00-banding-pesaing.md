# Banding Pesaing — Skenario 01

> Penguji independen, 2026-09-25. Skill pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pencarian
Kata kunci: `clawhub excel analysis skill SKILL.md spreadsheet data analysis`, `anthropics skills xlsx`.
Kandidat ditemukan:
| Kandidat | URL | Status akses |
|---|---|---|
| anthropics/skills — `xlsx` | https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md | ✔ dibaca (raw.githubusercontent.com) |
| ClawHub ivangdavila/data-analysis | https://clawhub.ai/ivangdavila/skills/data-analysis | ✘ diblokir proxy lingkungan uji |
| ClawHub ivangdavila/excel-xlsx | https://clawhub.ai/ivangdavila/skills/excel-xlsx | ✘ diblokir |
| openclaw/skills oyi77/data-analyst | https://github.com/openclaw/skills/blob/main/skills/oyi77/data-analyst/SKILL.md | ✘ 404 via raw / repo tidak dapat diakses sesi |
| skills.sh claude-office-skills/data-analysis | https://www.skills.sh/claude-office-skills/skills/data-analysis | ✘ diblokir |
| LobeHub openclaw-skills-excel / data-analyst | https://lobehub.com/skills/openclaw-skills-data-analyst | ✘ diblokir |

Hanya `anthropics/skills xlsx` yang bisa dibaca penuh → dipakai sebagai pesaing. **Saran:** pemilik/sesi
lain dengan akses ClawHub perlu mengulang banding terhadap `ivangdavila/data-analysis` (paling mirip cakupannya).

## Profil pesaing: anthropics/skills `xlsx`
- Lisensi: **proprietary** (LICENSE.txt) — tidak boleh diambil apa pun, hanya pembanding.
- Fokus: **membuat/mengedit** workbook (rumus, format, recalc LibreOffice). Deskripsinya: "The deliverable
  must be a spreadsheet file". Analisis data = "Bulk data → pandas read_excel".
- Butuh `openpyxl`, `pandas`, `markitdown`, LibreOffice ("preinstalled" di sandbox Anthropic; di laptop pembeli
  awam tidak ada → melanggar prinsip "tanpa setup").
- Tidak ada panduan baris TOTAL, angka teks Rupiah, huruf besar-kecil kategori, format jawaban awam.

## Menjalankan skenario 01 mengikuti pesaing
Untuk adil, pandas 3.0.6 + openpyxl 3.1.5 dipasang di venv scratchpad (PyPI). Agent mengikuti arahan
"pandas read_excel", membaca 3 sheet dengan `header=2`, membuang baris TOTAL (agent teliti), merapikan
kategori `.str.strip().str.title()`, `pd.to_numeric(errors='coerce')`:
```
non-numeric Total: 8
Semen 104.270.000 · Cat 36.437.000 · Keramik 32.785.000 · Pipa & Sanitasi 25.453.000 · Besi 25.428.000 · Alat & Perkakas 8.159.000
Feb 17.208.500 · Jul 17.661.000 · Agu 26.143.000 · Sep 24.982.500 (bulan lain sama dengan kunci)
Q2 97.112.500 · Q3 68.786.500 → -29,2% ;  grand 232.532.000
```
(Percobaan pertama script agent juga sempat gagal `KeyError` karena kolom tanggal berisi campuran datetime & teks "TOTAL".)

## Penilaian berdampingan (skala 1–5)
| Kriteria | Pesaing (xlsx + pandas) | analisis-excel | Catatan |
|---|:--:|:--:|---|
| Ketepatan angka | 3 | 5 | pesaing: 8 nilai teks/rumus dibuang diam-diam → total −1.024.000, Q3/Q2 −29,2% (kunci −28,8%) |
| Tanpa instal | 1 | 5 | pesaing perlu pandas/openpyxl |
| Transparansi peringatan | 2 | 5 | skill menyebut sel G68/G79/G98, baris TOTAL, penggabungan kategori |
| Multi-sheet | 5 | 2 | pandas `sheet_name=None` + concat mudah; skill 1 sheet/perintah |
| Jawaban siap pakai bahasa awam | 2 | 5 | pesaing tanpa format jawaban |
| Konteks Indonesia (Rp, koma desimal, bulan ID, cp1252) | 1 | 5 | |
| **Rata-rata** | **2,3** | **4,5** | |

**Kesimpulan:** skill kita **unggul** terhadap pesaing yang bisa diakses. Kelebihan pesaing yang perlu
dipelajari (ditulis ulang dengan cara sendiri): membaca/menggabung **semua sheet** sekaligus.
