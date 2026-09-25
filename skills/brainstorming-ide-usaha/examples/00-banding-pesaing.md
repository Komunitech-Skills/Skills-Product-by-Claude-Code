# Uji Banding Pesaing — Skenario 01 (warung makan sepi siang, modal ≤ Rp5 juta)

Penguji independen (Tahap 6), 2026-09-25. Skill pesaing hanya **dibaca untuk dinilai** (script pesaing tidak dijalankan, tidak disalin).

## Pencarian pesaing

| Kata kunci | Sumber | Hasil relevan |
|---|---|---|
| `business idea brainstorming agent skill SKILL.md github` | Web search | obra/superpowers `brainstorming`; phuryn/pm-skills; borghei/Claude-Skills `brainstorm-ideas`; Cygnusfear/claude-stuff `brainstorming`; VoltAgent/awesome-agent-skills |
| `clawhub skill brainstorm business ideas small business` | Web search | lobehub.com/skills/openclaw-skills-idea (umum, bukan khusus usaha); artikel ide bisnis generik — tidak ada skill ClawHub populer khusus brainstorming usaha UMKM |

URL yang dipakai:
- https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md — MIT, commit `5bf4e78` (2026-09-18), sumber ATM skill ini.
- https://github.com/phuryn/pm-skills — MIT, ±26,6 ribu bintang, 2,8 ribu fork, commit `8607e3b` (2026-09-14). Skill dibaca: `pm-product-discovery/skills/brainstorm-ideas-existing/SKILL.md` dan `pm-marketing-growth/skills/marketing-ideas/SKILL.md`.
- https://github.com/borghei/Claude-Skills/blob/main/project-management/discovery/brainstorm-ideas/SKILL.md — dilihat dari hasil pencarian; turunan pola Product Trio yang sama dengan pm-skills, tidak diuji terpisah.

## P1. Mengikuti instruksi obra/superpowers `brainstorming`

Agent mengikuti apa adanya:
> "This looks **architectural** (new product line, no existing flow in a repo) — I'll ask questions one at a time, propose 2–3 approaches, present the design in sections, then write a spec to `docs/superpowers/specs/2026-09-25-warung-siang-design.md` and invoke writing-plans."
> Q1: "What is the intended outcome — more revenue, or using idle staff time?" … (satu per pesan) …
> Pendekatan: (1) delivery lunch pre-order, (2) afternoon drinks & snacks, (3) catering boxes — dengan trade-off kualitatif, rekomendasi (1).
> Lalu: "Design section 1: components, data flow, error handling, testing — does this look right?" → menulis file spec & commit git → memanggil skill `writing-plans`.

Hasil: alur tanya-pahami-setujui bagus, tetapi keluaran berbahasa Inggris, istilah software (spec, data flow, testing, git commit) tidak nyambung untuk pemilik warung, tidak ada angka modal/impas, tidak ada uji pasar/MVP, dan ujungnya rencana implementasi kode.

## P2. Mengikuti instruksi phuryn/pm-skills `brainstorm-ideas-existing`

> **Understand the opportunity:** Product: warung makan; objective: raise 13–16 revenue; segment: nearby shops & residents; outcome: more afternoon orders.
> **PM perspective (5):** lunch subscription for nearby offices; catering boxes; afternoon snack menu; delivery-app listing; loyalty stamp card.
> **Designer perspective (5):** WhatsApp pre-order menu; "ngopi sore" corner; visible afternoon signage; combo board; order-ahead pickup.
> **Engineer perspective (5):** simple order form/Google Sheet; WhatsApp catalog; delivery radius map; POS data to find slow items; SMS reminders.
> **Top 5 prioritized:** (1) lunch subscription for offices, (2) WhatsApp pre-order, (3) afternoon snack combo, (4) catering boxes, (5) delivery-app listing — each with one-sentence reason and "key assumptions to validate" (e.g., offices will commit to daily orders).

Hasil: variasi ide lebih banyak (15) dan ada "asumsi yang harus divalidasi" — kelebihan nyata. Tetapi: tidak menggali kendala (modal, tenaga, yang sudah dicoba) sebelum ide, perspektif "Engineer" dipaksakan untuk warung, tidak ada angka, tidak ada rencana uji/target/aksi harian, bahasa Inggris; `marketing-ideas` (5 ide kanal promosi) juga generik tanpa kendala lokal.

## P3. Skill kita

Lihat `01-warung-makan-sepi-siang.md`.

## Penilaian berdampingan (1–5)

| Kriteria | superpowers `brainstorming` | pm-skills `brainstorm-ideas-existing` | **brainstorming-ide-usaha** |
|---|---|---|---|
| Cocok domain (usaha UMKM, bukan software/PM) | 1 | 3 | 5 |
| Menggali kendala nyata sebelum ide | 5 | 2 | 5 |
| Variasi/kekayaan ide | 2 | 5 | 3 |
| Penyaringan terukur & angka dihitung | 1 | 2 | 4 |
| Siap eksekusi (MVP, target, aksi harian) | 1 | 2 | 5 |
| Konteks & bahasa Indonesia (WA, Rupiah, momen lokal) | 1 | 1 | 5 |
| Kecepatan / beban pengguna | 2 | 5 | 3 |
| **Total (maks 35)** | **13** | **20** | **30** |

## Kesimpulan

Skill kita **menang jelas** melawan kedua pesaing untuk skenario ini. Kelebihan pesaing yang layak dipelajari (ditulis ulang dengan cara sendiri, bukan disalin):
1. pm-skills: **jumlah & sudut pandang ide lebih kaya** sebelum disaring (15 ide dari 3 sudut pandang). Skill kita hanya memunculkan 3–6 ide; bisa ditambah langkah "curah 10–15 ide mentah dari 2–3 sudut pandang (pemilik, pelanggan, pesaing/pemasok)" sebelum disaring — `references/teknik-ide-terstruktur.md` sudah menyebut 10–20 ide mentah, tapi SKILL.md B.3 tidak menyebut jumlah.
2. pm-skills: setiap ide terpilih disertai **"asumsi kunci yang harus dibuktikan"** — bisa ditambahkan ke kerangka uji murah (bagian "pertanyaan yang dijawab uji ini").
3. pm-skills: **cepat** (satu kali jawab) — mendukung usulan menggabungkan pertanyaan penggalian jadi satu pesan.
