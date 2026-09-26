# Uji Banding Pesaing — Skenario 01 (Kafe Yogyakarta, 2 Barista PKWTT)

Penguji independen (Tahap 6), 25 September 2026. Skill/template pesaing hanya **dibaca untuk dinilai**,
tidak disalin.

## Pencarian
Kata kunci: `"employee onboarding" SKILL.md claude skill github`, `team onboarding playbook skill`,
`template checklist onboarding karyawan baru Talenta Gadjian Mekari`, `hr onboarding agent skill`.

| Sumber | URL | Status baca |
|---|---|---|
| rampstackco/claude-skills — `team-onboarding-playbook` | https://github.com/rampstackco/claude-skills/blob/main/skills/team-onboarding-playbook/SKILL.md | ✅ dibaca penuh (189 baris). Jumlah bintang/lisensi tidak bisa dicek (API GitHub repo ini tidak diizinkan di sesi) |
| nexu-io "HR Onboarding" | https://www.getclaudeskills.com/skills/hr-onboarding-nexu-io | ❌ terblokir proxy; hanya ringkasan hasil cari (rencana 1 halaman HTML minggu pertama, default 30/60/90) |
| jeffreytse grimoire-hub `design-employee-onboarding` | https://skills.lc/jeffreytse/grimoire-hub/jeffreytse-grimoire-hub-skills-business-hr-skills-design-employee-onboarding-skill-md | tidak dibaca (repo koleksi besar, indikasi volume tinggi) |
| alirezarezvani/claude-skills (380+ skill) | https://github.com/alirezarezvani/claude-skills | tidak dibaca rinci (koleksi massal) |
| Mekari Talenta — On-Boarding Checklist Template | https://www.talenta.co/en/free-tools/hr-document/on-boarding-checklist/ | ❌ terblokir proxy |
| Gadjian — 5 Jenis Form Onboarding Karyawan Baru | https://www.gadjian.com/blog/2026/03/26/form-onboarding-karyawan-baru/ | ❌ terblokir proxy |
| GajiHub — Template Checklist Onboarding | https://gajihub.com/blog/template-checklist-onboarding-karyawan-baru/ | ❌ terblokir proxy |
| LinovHR — HR Checklist Onboarding | https://www.linovhr.com/hr-checklist-onboarding-karyawan-baru/ | ❌ terblokir proxy |

Pesaing terbaik yang bisa dibaca penuh: **`team-onboarding-playbook` (rampstackco)**. Template HR Indonesia
(Talenta/Gadjian/GajiHub) hanya dinilai dari cuplikan hasil pencarian: checklist dokumen/form
(Word/PDF/Excel) — statis, tanpa perhitungan tanggal; perlu dicek ulang oleh pemilik bila akses terbuka.

## Hasil pesaing pada skenario 01 (ringkas, dijalankan penguji mengikuti instruksinya)
- Kerangka 4 lapis: Belonging (minggu 1) → Context (minggu 1–4) → Contribution (minggu 2–6) → Mastery (bulan 2–3).
- Deliverables: checklist pra-H1, jadwal H1, reading list 5–10 item, milestone 30/60/90, **panduan buddy**,
  **ritme check-in manajer** (harian minggu 1, mingguan bulan 1), **template retrospektif 90 hari**.
- Daftar "failure patterns" (buddy tanpa waktu, 8 jam rapat di H1, tidak ada pekerjaan nyata terlalu lama).
- Overlay peran hanya engineering/design/product/marketing — barista harus diadaptasi sendiri.
- Tidak ada tanggal (hanya "30 days"), tidak ada hukum Indonesia (masa percobaan, PKWT, BPJS, PDP), tidak ada
  pesan WA, tidak ada buku saku/aturan kerja, berbahasa Inggris dan berorientasi tim kantor/teknologi.

## Penilaian berdampingan (0–2 per kriteria)
| # | Kriteria | Pesaing (rampstack) | sop-onboarding | Catatan |
|---|---|---|---|---|
| 1 | Tanggal konkret & benar | 0 | 2 | Pesaing tidak menghitung tanggal |
| 2 | Kepatuhan hukum Indonesia (percobaan, PKWT, BPJS, PDP) | 0 | 2 | |
| 3 | Cocok untuk UMKM/kafe/shift | 0 | 2 | Pesaing untuk tim kantor/teknologi |
| 4 | Pesan siap kirim (WA) & pengumuman tim | 1 | 2 | Pesaing hanya menyebut "welcome message" |
| 5 | Buku saku/aturan kerja tanpa karangan | 0 | 2 | |
| 6 | Formulir evaluasi siap cetak | 1 | 2 | Pesaing: 30/60/90 review template di references |
| 7 | Metodologi onboarding (belonging, first task, failure patterns) | 2 | 1 | Pesaing unggul: prinsip kenapa & jebakan umum |
| 8 | Panduan buddy & ritme check-in | 2 | 0 | **Kekurangan skill kita**: buddy hanya disebut, tidak ada panduan tugas buddy maupun jadwal check-in harian/mingguan |
| 9 | Target per peran | 1 | 0 | Pesaing punya overlay 4 peran; skill kita tidak punya target 30/60/90 per jabatan (kasir/barista/mekanik/admin) |
| 10 | Retrospektif untuk perbaikan proses | 2 | 0 | |
| | **Total** | **9/20** | **15/20** | |

## Kesimpulan
`sop-onboarding` **menang** untuk pasar sasaran (UMKM Indonesia): tanggal terhitung, aman hukum, bahasa
awam, siap kirim/cetak. Pesaing unggul di sisi **metodologi**: panduan buddy, ritme check-in, target per peran,
retrospektif, dan daftar jebakan. Usulan (tulis ulang dengan cara sendiri, bukan salin):
1. Tambah `templates/panduan-buddy.md` (tugas buddy per minggu, waktu yang dilindungi).
2. Tambah ritme check-in (harian minggu 1, mingguan bulan 1) sebagai baris jadwal atau catatan.
3. Tambah target 30/60/90 contoh per jabatan umum UMKM di `references/varian-jenis-usaha.md`.
4. Tambah jadwal H1 per jam (singkat) di template.
