# Uji banding pesaing — KPI/OKR tim

> Penguji independen, 2026-09-29. Pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pencarian
Kata kunci: "SKILL.md agent skill KPI OKR scorecard team performance", "clawhub skill OKR KPI tracker",
direktori skills (agent-skills.md, LobeHub, mcpmarket, skills.lc), GitHub.

| Kandidat | Sumber | Isi (ringkas) |
|---|---|---|
| `okr-design` (rampstackco/claude-skills) | https://github.com/rampstackco/claude-skills/blob/main/skills/okr-design/SKILL.md | Metodologi OKR untuk product leader: desain objective/KR, skor 0,0–1,0 manual, target rata-rata 0,6–0,7, anti-pattern, cadence. **Tanpa script**, tanpa bobot KPI per orang, tanpa arah turun, tanpa privasi. |
| `okr-design` / OKR-KPI patterns (yonatangross/orchestkit) | https://agent-skills.md/skills/yonatangross/orchestkit/okr-design ; https://mcpmarket.com/tools/skills/okr-kpi-performance-patterns | Kerangka OKR, KPI tree, North Star, leading/lagging untuk tim produk. Tidak terdokumentasi menghitung skor per orang. |
| OKR skill (alirezarezvani/claude-skills, repo ±26,8k bintang, MIT) | https://lobehub.com/skills/alirezarezvani-claude-skills-okr | Halaman detail tidak bisa diakses (403); dari repo, fokus perencanaan/cascade OKR, bukan skor KPI tim. |
| ClawHub | https://clawhub.ai | Tidak ditemukan skill KPI/OKR tim yang relevan (hasil pencarian hanya "skill usage tracker"). |

Tidak ada pesaing publik yang menghitung **skor KPI tertimbang per orang/divisi** dari Excel/WA untuk UMKM.
Pesaing terdekat untuk bagian OKR: `rampstackco okr-design`.

## Banding berdampingan (skenario 01 bagian KPI + skenario 03 bagian OKR)
| Aspek | okr-design (rampstackco) | kpi-tim |
|---|---|---|
| KPI tertimbang per orang/divisi/perusahaan | ✗ | ✓ script, Decimal, 0 selisih |
| KPI makin rendah makin baik, target 0 | ✗ | ✓ (2−r/t), nol kejadian |
| Batas capaian, ambang warna | ✗ | ✓ 120% default, per KPI |
| Data kosong eksplisit | "sebutkan celahnya" (umum) | ✓ 3 mode, default tidak merugikan |
| OKR progres & status tengah periode | manual | ✓ `okr --jalan`, KR menurun benar |
| Kedalaman metodologi OKR (anti-pattern, cadence) | **lebih kaya** | ringkas |
| Excel/Sheets, rekap grup WA, Telegram/OpenClaw | ✗ | ✓ |
| Bahasa & konteks Indonesia, UU PDP, UU Ketenagakerjaan | ✗ | ✓ |
| Etika (bukan PHK otomatis, bukan pengawasan) | ✗ | ✓ |

**Nilai (skala 10, untuk pembeli UMKM Indonesia):** okr-design 4 · kpi-tim 8.
Kelebihan pesaing yang layak dipelajari (tulis ulang sendiri, bukan salin): panduan anti-pattern OKR
(sandbagging vs target fantasi) dan ritme review kuartalan bisa diperkaya di `references/`.

**Kesimpulan: kpi-tim menang** untuk tugas yang sama; tidak ada pesaing yang mengungguli.
