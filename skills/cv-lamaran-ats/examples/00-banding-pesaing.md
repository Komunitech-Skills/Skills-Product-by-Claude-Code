# Uji Banding Pesaing — cv-lamaran-ats

## Pencarian yang dilakukan
Kata kunci: `SKILL.md resume ATS claude skill`, `SKILL.md tailor resume job description
skill`, di GitHub, ClawHub, skills.sh, anthropics/skills, dan repo Indonesia
(manairalabs/bicara-skills, alvinindra/bahasa-skills — tidak ditemukan skill CV/resume
di keduanya, keduanya fokus topik lain).

Kandidat yang ditemukan (dibaca lewat raw.githubusercontent.com, **tidak dijalankan,
tidak disalin**):
- `ComposioHQ/awesome-claude-skills` (lead-research-assistant, dll.) — **sengaja
  dikecualikan** sesuai instruksi penguji (lisensi tidak sah untuk dipakai sebagai
  pembanding produk berbayar).
- `unnati06/ats-checker-skill` — MIT, 0 bintang, 2 commit. Terlalu belum terbukti
  untuk jadi pembanding utama (gagal ambang "terbukti" pedoman kurasi Komunitech §Tahap 2), tapi
  fiturnya (skor 0-100 + rating per bagian) relevan untuk dinilai.
- `dabydat/resume-builder-skill` — MIT, 59 bintang, klaim "battle-tested 500K+
  engineers r/EngineeringResumes" (klaim promosi, tidak diverifikasi independen).
  **Dipilih sebagai pembanding utama** karena bintang tertinggi di antara skill
  resume yang ditemukan dan cakupannya paling dekat (penyusunan CV lengkap).

Sumber: https://github.com/dabydat/resume-builder-skill ,
https://raw.githubusercontent.com/dabydat/resume-builder-skill/master/skill/SKILL.md
(dibaca via WebFetch untuk dinilai, isi tidak disalin ke skill kita).

## Simulasi Skenario 1 (Admin Gudang) mengikuti instruksi pesaing (dabydat/resume-builder-skill)

Instruksi pesaing berfokus pada penyusunan resume umum yang rapi & lolos parsing
ATS (Harvard Career Services + gaya r/EngineeringResumes), BUKAN penyesuaian ke
satu lowongan tertentu — tidak ada langkah "tempel teks lowongan" atau skor
kecocokan kata kunci. Mengikuti Step 1-5 pesaing dengan input yang sama:

```
[Step 1: Kumpulkan info] Nama, riwayat kerja (Admin Gudang, CV Berkah Jaya,
2022-2024), pendidikan (SMK Akuntansi), skill (Excel).

[Step 2-3: Susun struktur + XYZ formula]
SITI RAHMA
Bekasi | 0812-0000-1111 | siti.rahma@email.com

TECHNICAL SKILLS
Microsoft Excel, Inventory Tracking, Stock Reconciliation

PROFESSIONAL EXPERIENCE
Admin Gudang — CV Berkah Jaya | 2022–Present
- Recorded incoming/outgoing inventory for retail warehouse using Excel and
  manual stock cards, maintaining accurate monthly stock reports for management
- Supported monthly stock opname process to verify physical inventory against
  records

EDUCATION
SMK, Accounting — SMK Negeri 3 Bekasi (2020)

[Step 4: Format] Calibri 10.5pt, satu kolom, tanpa tabel.
[Step 5: Konversi PDF] "Generate .docx dan .pdf, verifikasi ekstraksi teks dengan
pdftotext" — TIDAK BISA disimulasikan di sini (butuh LibreOffice/pdftotext,
bukan sekadar teks).
```

## Tabel penilaian

| Aspek | cv-lamaran-ats (kita) | dabydat/resume-builder-skill |
|---|---|---|
| Kualitas tulisan | Baik, kalimat aktif + hasil terukur bila ada | Baik, formula XYZ jelas |
| Kesesuaian konteks Indonesia | Bahasa Indonesia natural, format tanggal ID, nomor HP ID | Bahasa Inggris/Spanyol saja, tidak ada Bahasa Indonesia; kalimat CV Siti jadi bahasa Inggris meski pelamar & lowongan berbahasa Indonesia |
| **Penyesuaian ke lowongan spesifik** | Ada — analisis kata kunci lowongan + skor kecocokan by script | **Tidak ada** — tidak meminta teks lowongan sama sekali, resume generik |
| Anti-mengarang pengalaman | Eksplisit dilarang + diuji (lihat skenario 3) | Tidak disebutkan sama sekali di SKILL.md — tidak ada guardrail tertulis |
| Siap pakai langsung | Ya — teks siap tempel ke portal manapun | Perlu tools tambahan (LibreOffice/pdftotext) untuk hasil akhir, tidak instan tanpa setup |
| Surat lamaran/email/pesan WA ke rekruter | Ada, sekali jalan | Tidak ada — hanya resume |
| Skor kecocokan terverifikasi | Ada, via script + fallback manual | Tidak ada skor kecocokan; hanya checklist format |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- Formula "XYZ" (Action + What + Technical Context + Business Impact) untuk
  menulis poin pengalaman bisa jadi acuan tambahan di Langkah 5 SKILL.md kita
  selain "kata kerja aktif + hasil terukur" — bisa dipertegas dengan struktur
  serupa agar lebih konsisten antar sesi.
- Rincian spesifikasi format (font, ukuran, margin) yang eksplisit disebut
  pesaing bisa membantu skill kita menyebutkan rekomendasi format dasar
  (meski kita fokus keluaran teks, bukan file .docx/.pdf), untuk berjaga-jaga
  kalau pengguna menyalin ke Word sendiri.
- Dukungan bilingual (Inggris-Spanyol dengan gaya natural per bahasa, bukan
  terjemahan literal) — prinsip serupa relevan untuk versi Bahasa Indonesia vs
  Inggris di skill kita, sudah disebutkan SKILL.md tapi bisa lebih ditegaskan
  agar tidak jadi terjemahan kaku.

## Kesimpulan
Skill kita **menang telak** untuk kasus penggunaan aslinya (menyesuaikan CV ke
lowongan tertentu, konteks Indonesia, tanpa mengarang): pesaing bahkan tidak
punya fitur penyesuaian ke lowongan spesifik maupun guardrail anti-fabrikasi
tertulis, dan tidak mendukung Bahasa Indonesia. Pesaing unggul tipis di formula
penulisan bullet point (XYZ) dan spesifikasi format file — sudah dicatat sebagai
masukan perbaikan ringan, bukan alasan skor turun.
