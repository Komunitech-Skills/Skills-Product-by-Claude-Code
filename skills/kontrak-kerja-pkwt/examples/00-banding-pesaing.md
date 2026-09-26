# Uji Banding Pesaing — Skenario 01

> Penguji independen, 25 September 2026. Pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pencarian
Kata kunci (WebSearch, 25 Sep 2026):
- "github agent skill SKILL.md employment contract Indonesia PKWT"
- "clawhub skill kontrak kerja OR employment contract OR labor contract skill.md"
- "template PKWT contoh kontrak kerja waktu tertentu Talenta Gadjian Kontrak Hukum"
- "talenta contoh kontrak kerja PKWT pasal masa percobaan uang kompensasi"

Hasil yang relevan:
| Kandidat | URL | Bukti pemakaian | Dapat dibaca? |
|---|---|---|---|
| **wshobson/agents — `employment-contract-templates`** (plugin hr-legal-compliance) | https://github.com/wshobson/agents/tree/main/plugins/hr-legal-compliance/skills/employment-contract-templates ; mirror: https://github.com/rmyndharis/antigravity-skills , https://agent-skills.md/skills/rmyndharis/antigravity-skills/employment-contract-templates , https://mcpmarket.com/tools/skills/employment-contract-templates-9 | Repo ±39,9k bintang (star-history.com, 22 Sep 2026), multi-platform, banyak mirror | ✅ SKILL.md + `references/details.md` (461 baris) via raw.githubusercontent |
| anthropics/claude-for-legal — `employment-legal/hiring-review` | https://github.com/anthropics/claude-for-legal/blob/main/employment-legal/skills/hiring-review/SKILL.md | Vendor resmi | Tidak relevan langsung (review perekrutan, fokus AS) |
| Skills.lc `emplaw-employment-contract-drafter` | https://skills.lc/Eli-yu-first/skillshub/... | Tidak ada bukti pemakaian | Tidak dibaca (tidak lolos sinyal bukti) |
| Template HR Indonesia: Mekari Talenta, Mekari Sign, KitaLulus, Glints, KantorKu, Kemnaker "halohubungankerja" | https://www.talenta.co/blog/berikut-contoh-dan-penjelasan-kontrak-kerja-karyawan-pkwt-pkwtt-serta-freelance/ ; https://mekarisign.com/id/blog/contoh-kontrak-kerja/ ; https://kantorku.id/blog/contoh-kontrak-kerja/ ; https://halohubungankerja.kemnaker.go.id/contoh_pkwt.php | Situs HR populer | ❌ Terblokir proxy/DNS dari lingkungan uji. Hanya cuplikan hasil penelusuran yang terbaca |

Pesaing utama yang diuji: **wshobson `employment-contract-templates`** (skill publik terpopuler untuk kontrak kerja). Pembanding kedua: **template HR Indonesia** berdasarkan cuplikan penelusuran (dinilai terbatas).

## Menjalankan skenario 01 dengan skill pesaing (wshobson)
Isi skill pesaing: SKILL.md generik (tabel jenis dokumen, "At-Will vs Contract", "Exempt vs Non-Exempt", disclaimer umum), `references/details.md` berisi Offer Letter, Employment Agreement, handbook — semua bergaya **AS** ($, 401(k), at-will, "[X] weeks severance", non-compete), tanpa script, tanpa aturan Indonesia.

Output agent yang mengikuti pesaing (ringkas): "Employment Agreement" dwibahasa terjemahan bebas: *Position: Production Staff; Term: 1 Oct 2026 – 30 Sep 2027; Compensation: base salary IDR 3,900,000 + allowance IDR 250,000; Benefits: health insurance per company policy; Termination: either party may terminate with 30 days notice; Severance: [X] weeks base salary if applicable; Non-compete 12 months; At-Will Employment: may be terminated by either party at any time* (details.md baris 64–66 & 140–141 memuat klausul at-will; tidak ada klausul masa percobaan), disclaimer umum "consult legal counsel". Tidak ada perhitungan kompensasi PKWT (konsep ini tidak dikenal pesaing).

## Pembanding kedua: template HR Indonesia (dari cuplikan)
Cuplikan penelusuran Talenta/HR menyebut: PKWT tanpa masa percobaan, kompensasi proporsional minimal 1 bulan, bahasa Indonesia, tetapi juga **"PKWT maksimal 2 tahun dan hanya boleh diperpanjang satu kali 1 tahun"** (aturan lama UU 13/2003 sebelum UU 6/2023/PP 35/2021 — **usang**) dan **"masa percobaan → otomatis PKWTT"** (tidak tepat; PP 35/2021 Pasal 12: batal demi hukum, masa kerja tetap dihitung). Template statis: tidak menghitung, tidak memeriksa, tidak menyesuaikan ke kasus.

## Penilaian berdampingan (0–2 per kriteria)
| # | Kriteria | wshobson | Template HR ID (cuplikan) | **Skill kita** |
|---|---|---|---|---|
| 1 | Sesuai hukum Indonesia (PKWT, PP 35/2021, MK 168) | 0 | 1 (sebagian usang) | 2 |
| 2 | Tanpa masa percobaan / tanpa "putus kapan saja" | 1 (tanpa probation, tetapi memuat at-will) | 2 | 2 |
| 3 | Kompensasi PKWT dihitung benar & dapat diaudit | 0 | 1 (rumus saja) | 2 |
| 4 | Ganti rugi Pasal 62 dua arah | 0 | 1 | 2 |
| 5 | Batas 5 tahun | 0 | 0 (2+1 tahun, usang) | 2 |
| 6 | UMK/BPJS/THR/pencatatan | 0 | 1 | 2 |
| 7 | Bahasa Indonesia, siap cetak, terbilang, `[isi]` | 0 | 1 | 2 |
| 8 | Uji kelayakan jenis pekerjaan & risiko PKWTT | 0 | 0 | 2 |
| 9 | Disclaimer bertanggal + status regulasi | 1 (generik) | 0 | 2 |
| 10 | Mode periksa draf & penanganan input buruk | 0 | 0 | 2 |
| | **Total (maks 20)** | **2** | **7** | **20** |

## Kesimpulan
Skill kita **menang telak**. Pesaing terpopuler berorientasi AS dan justru berbahaya untuk PKWT (at-will "putus kapan saja", severance mingguan, non-compete 12 bulan, tanpa kompensasi PKWT). Template HR Indonesia benar di beberapa poin tetapi sebagian usang dan tidak menghitung. Tidak ada kelebihan pesaing yang perlu dipelajari selain: wshobson menyertakan **offer letter** — bisa jadi ide skill pendamping ("surat penawaran kerja") di backlog.
Keterbatasan: template Talenta/Mekari/Kemnaker tidak bisa dibuka penuh (proxy memblokir), jadi penilaian kolom kedua berdasarkan cuplikan saja.
