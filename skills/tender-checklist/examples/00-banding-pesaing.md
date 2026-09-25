# Uji banding pesaing — Skenario 01

> Penguji independen, 2026-09-25. Skill pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pencarian
Kata kunci: "SKILL.md agent skill tender procurement RFP bid checklist github"; "clawhub skill tender OR procurement OR RFP response"; "checklist dokumen penawaran tender LPSE agar tidak gugur UMKM 2025".
Hasil yang dinilai / dicatat:
| Sumber | URL | Catatan |
|---|---|---|
| **rfp-responder** (alirezarezvani/claude-skills, MIT, repo koleksi populer) | https://github.com/alirezarezvani/claude-skills/blob/main/commercial/skills/rfp-responder/SKILL.md | Pesaing terdekat (sisi penyedia). Dibaca via raw GitHub |
| rfp-builder (w95/awesome-claude-corporate-skills) | https://github.com/w95/awesome-claude-corporate-skills/blob/main/12-procurement-supply-chain/rfp-builder/SKILL.md | Sisi **pembeli** (menyusun RFP) — tidak sebanding |
| rfp-response (skills.rest) | https://skills.rest/skill/rfp-response | Drafting proposal generik — tidak sebanding untuk tender pemerintah RI |
| Ethiopian public procurement explainer (mirror skills.lc) | https://skills.lc/gabrielmoreira/agent-skills-mirror/... | Negara lain |
| Blog Indonesia: tenderkita.com, pengadaanpro.com, menulis.vendor-indonesia.id | https://tenderkita.com/cara-ikut-tender-lpse-panduan-lengkap/ ; https://www.pengadaanpro.com/blogs/Cara-Ikut-Tender-LPSE-Panduan-Lengkap-untuk-Pelaku-Usaha | **Tidak bisa dibuka** (egress proxy memblokir); dinilai hanya dari cuplikan hasil pencarian: panduan langkah umum (registrasi LPSE, dokumen OSS/SBU), tanpa perhitungan |
Tidak ditemukan skill ClawHub/skills.sh khusus tender pemerintah Indonesia (SPSE/LPSE).

## Penerapan pada skenario 01
**rfp-responder:** memecah dokumen menjadi syarat MANDATORY/WEIGHTED/NICE-TO-HAVE, matriks bukti (STRONG/PARTIAL/GAP), 3–5 win-theme gaya Shipley, estimasi winrate & keputusan bid/no-bid (script stdlib). Secara eksplisit **tidak** menangani aritmetika harga, pajak, maupun detail jadwal. Pada skenario 01 ia akan menghasilkan matriks kepatuhan dari LDK (jika ditempel) + rekomendasi bid — tanpa PPN 11/12, tanpa %HPS/batas 80%, tanpa terbilang, tanpa aturan Perpres/UMK/KBLI, tanpa jadwal hari kerja.

| Kriteria (0–2) | rfp-responder | tender-checklist |
|---|---|---|
| Angka penawaran benar (PPN, total, %HPS, terbilang) | 0 | 2 |
| Kelayakan & keputusan ikut | 1 (bid/no-bid generik, winrate) | 2 (UMK, KBLI, PKP, SKP) |
| Checklist dokumen sesuai SPSE | 0 | 2 |
| Jadwal mundur | 0 | 2 |
| Regulasi Indonesia + disclaimer bertanggal | 0 | 2 |
| Strategi menang / win-theme | 2 | 0 |
| **Total** | **3** | **10** |

**Kesimpulan:** skill kita unggul telak untuk tugas ini. Kelebihan pesaing yang layak dipelajari (ditulis ulang dengan cara sendiri, bukan disalin): **matriks "syarat LDK → bukti yang dimiliki → status"** dari dokumen pemilihan yang ditempel — memperkuat langkah 2–3 bila pengguna menempel LDK/LDP.
