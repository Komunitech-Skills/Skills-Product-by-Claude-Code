# Uji banding pesaing — kalkulator klinis (skenario normal pertama)

Penguji independen, 2026-09-29. Pesaing hanya **dibaca & dijalankan untuk dinilai** (kode
diaudit dulu: fungsi tanggal/aritmetika murni, tanpa jaringan/berkas), tidak disalin.

## Pencarian (kata kunci & sumber)
- Web: "SKILL.md clinical calculator skill github agent skills medical calculator MDCalc claude".
- GitHub (clone dangkal, 2026-09-29):
  - **vitaldb/medcalc** — MCP server 59 kalkulator klinis, lisensi MIT, commit terakhir 2 Mei
    2026. Punya `pregnancy_calculator`, `map_calculator`, `bmi_bsa_calculator`. **Pesaing terdekat.**
  - FreedomIntelligence/OpenClaw-Medical-Skills (869 skill, commit 21 Jul 2026) — tidak ada
    kalkulator obstetri/IMT/kognitif (hanya biomedis/riset).
  - dromlakhani/MD2SKILL (888 skill pedoman, commit 28 Agu 2026) — ada skill diabetes dalam
    kehamilan, **tidak ada** skrining preeklampsia/penanggalan/IMT.
- ClawHub/skills.sh: tidak ditemukan skill kalkulator obstetri/skrining PE berbahasa Indonesia.
- Web MDCalc (situs, bukan skill): punya kalkulator due date & BMI, tetapi tidak bisa dipasang
  sebagai skill agent; tidak dinilai sebagai skill.
- Jumlah bintang GitHub tidak bisa diambil (API GitHub tidak aktif di sesi ini).

## Hasil menjalankan pesaing (vitaldb/medcalc) pada data skenario 1 & 4
```
pregnancy_calculator('lmp','2026-07-02')        -> due 2027-04-08, GA 12w5d, First trimester
pregnancy_calculator('lmp','2026-06-15', 35)    -> due 2027-03-29, GA 15w1d   (GA TIDAK dikoreksi siklus;
                                                   tidak konsisten dengan HPL yang dikoreksi)
pregnancy_calculator('lmp','2026-06-15', 24)    -> due 2027-03-22 (siklus < 28 diabaikan: koreksi hanya bila > 28)
map_calculator(118, 78)                         -> 91.3333 (tanpa ambang/interpretasi)
```
Kode `get_trimester`: `< 13` minggu = T1, `< 27` = T2 → 13 0/7–13 6/7 dilabeli T2 dan 27 mg
dilabeli T3 (tidak sesuai batas ACOG 13 6/7 / 27 6/7). Usia kehamilan memakai `datetime.now()`
(tidak bisa diisi tanggal periksa).

## Penilaian berdampingan (skenario 1)
| Kriteria (bobot) | vitaldb/medcalc | kalkulator-klinis-nakes |
|---|---|---|
| Ketepatan HPL/UK (3) | 2 — HPL benar; koreksi siklus hanya > 28; UK tak dikoreksi; batas trimester salah | 3 — 0 selisih dari 40.000+ kasus acak & kasus kabisat |
| Skrining preeklampsia (3) | 0 — tidak ada | 2,5 — Buku KIA + NICE; ada selisih ambang MAP/proteinuria (lihat HASIL-UJI) |
| Kenaikan BB hamil IOM (2) | 0 — tidak ada | 2 — tabel IOM 2009 cocok penuh |
| Penanggalan ulang USG (2) | 0 — tidak ada | 2 — ambang ACOG CO 700 cocok |
| Sumber + tahun, penafian, tanpa dosis (2) | 0 | 2 |
| Konteks Indonesia (bahasa, Buku KIA, Kemenkes) (2) | 0 | 2 |
| Mudah dipakai tanpa setup (1) | 0,5 — perlu server MCP + uv | 1 — Python standar |
| **Total (15)** | **2,5** | **14,5** |

**Kesimpulan:** skill kita menang telak. Kelebihan pesaing yang layak dipelajari (ditulis ulang
dengan cara sendiri, bukan disalin): cakupan kalkulator luas (eGFR, CHA2DS2-VASc, dll.) dan
antarmuka alat terstruktur — kandidat v2 bila pemilik ingin memperluas.
