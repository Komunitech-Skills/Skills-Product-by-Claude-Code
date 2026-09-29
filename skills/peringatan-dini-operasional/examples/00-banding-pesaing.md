# Uji banding pesaing (penguji independen, 2026-09-29)

## Pencarian
Kata kunci: "SKILL.md anomaly detection agent skill KPI early warning control chart",
"clawhub skill anomaly detection metrics alert", "clawhub data-analyst skill outlier", GitHub code
search `filename:SKILL.md "anomaly" "z-score"` (1.924 hasil).
Sumber yang dicek:
- ClawHub: menurut ulasan fast.io, dari ribuan skill "fewer than a dozen address anomaly detection
  directly"; yang paling dekat `data-analyst` (oyi77) — isi SKILL.md tidak bisa diambil (raw GitHub 404,
  LobeHub 403), jadi tidak dinilai.
  https://fast.io/resources/best-openclaw-tools-ai-anomaly-detection-data-monitoring/ ·
  https://clawhub.ai/oyi77/data-analyst
- agent-skills.md tag anomaly-detection: hanya 2 skill tak relevan (riset akademik, debug Jira).
  https://agent-skills.md/tags/anomaly-detection
- anthropics/skills: tidak ada skill anomali/peringatan dini operasional.
- **Pesaing terdekat yang dinilai:** `detect-metric-anomaly` (v1.0.0) di registry agregator
  majiayu000/claude-skill-registry —
  https://github.com/majiayu000/claude-skill-registry/blob/main/skills/analysis/detect-metric-anomaly/SKILL.md
  (133 baris: z-score |z|≥2 warning, ≥3 critical; ambang absolut contoh CPU/memori; tren = 80% dari
  10 nilai terakhir di satu sisi rata-rata; output JSON alert). Pembanding kedua (lebih umum):
  `anomaly-detection-aj-geddes-useful-ai-prompts` (kode sklearn IsolationForest/LOF/IQR, butuh
  numpy/scikit-learn) — tidak cocok untuk log harian UMKM tanpa instalasi.
Pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Skenario normal 01 (garmen 45 hari) dijalankan dengan prosedur pesaing
Mengikuti langkahnya secara harfiah (garis dasar = seluruh riwayat sebelum hari ini, tanpa buang
pencilan; z; tren 80%/10):
| Metrik | Pesaing | Skill kita |
|---|---|---|
| Reject 52 | z 5,08 critical, trend increasing | 🔴 6,4σ + target + hari sama + beruntun |
| **Downtime 95 menit** | **z 1,76 → normal** (hari listrik padam 240 menit melebarkan sd jadi 36,7) | 🔴 7,0σ (pencilan 4 Sep dibuang dari garis dasar), +255% vs Selasa |
| Stok kain 2,8 hari | tidak ada konsep sisa hari / lead time (z −1,46 "normal") | 🔴 pesan HARI INI |
| Output (3/7 hari di bawah target) | tidak ada aturan target per hari | 🟡 |
| % reject | tidak ada | 🔴 4,6σ |
| Angka `1.271`, `5.430` | tidak ada panduan parsing (agent harus menebak) | dibaca otomatis |
| Format | JSON alert teknis (bahasa Inggris, contoh CPU server) | pesan Indonesia siap Telegram + pertanyaan cek |

## Skor
| Kriteria (1–5) | Pesaing `detect-metric-anomaly` | Skill kita |
|---|---|---|
| Ketepatan deteksi | 2 (downtime & stok terlewat) | 5 |
| Angka dihitung script/teruji | 1 (hanya rumus, tanpa script/tes) | 5 (script + 31 tes regresi + verifikasi independen 0 beda) |
| Konteks Indonesia/UMKM | 1 | 5 |
| Tindak lanjut & kejujuran | 2 | 4 |
| Tanpa instalasi | 4 | 5 |
| **Total** | **10/25** | **24/25** |

**Kesimpulan:** skill kita menang telak. Satu hal yang layak dipelajari dari pesaing (ditulis ulang
dengan cara sendiri bila diadopsi): ambang **absolut** per metrik (warning/critical) sebagai pengaman
untuk metrik yang garis dasarnya nol/konstan — lihat temuan MAYOR di `HASIL-UJI.md`.
