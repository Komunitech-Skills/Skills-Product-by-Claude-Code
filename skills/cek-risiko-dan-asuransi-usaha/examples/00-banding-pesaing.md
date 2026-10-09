# Uji banding pesaing (skenario normal 1)

- Tanggal: 2026-10-09 · Penguji independen · `claude-code (simulasi agent)`
- Pencarian: web "SKILL.md agent skill risk assessment small business insurance risk register github"; hasil: skills.sh, skills-hub.ai, skillselion. Tidak ditemukan skill publik khusus risiko + asuransi usaha kecil (apalagi konteks Indonesia).
- Pesaing terdekat yang terbukti: **`risk-assessment`** dari `anthropics/knowledge-work-plugins` (folder `operations/skills/risk-assessment/SKILL.md`, ±40 baris; pembuat resmi Anthropic). Hanya dibaca untuk dinilai, tidak disalin.
- Alternatif lain: `headcount-enterprise-risk` (skills-hub.ai, gaya korporat/audit, tidak relevan untuk warung/kafe); skill "risk register" ECNU di skills.sh ditandai gagal audit keamanan oleh Socket, tidak dipakai.

## Pesaing: isi singkat
Matriks kemungkinan × dampak 3×3 (Low/Medium/High → Low…Critical), 6 kategori risiko (operasional, keuangan, kepatuhan, strategis, reputasi, keamanan), format register (deskripsi, kemungkinan, dampak, level, mitigasi, pemilik, status). Tanpa asuransi, tanpa dana darurat, tanpa script, bahasa Inggris.

## Hasil pesaing untuk pesan skenario 1 (simulasi)
> Risk register (bahasa campur): Banjir – High/High – Critical – mitigasi: pindah stok ke tempat tinggi – Owner: pemilik – Open; Kebakaran – Low/High – Medium; Kecelakaan karyawan – Medium/Medium – Medium; Keracunan – Low/High – Medium; Ketergantungan barista – Medium/Medium – Medium; Pencurian – Medium/Low – Low; Kepatuhan BPJS – Medium/Medium – Medium.
> Tidak menjawab "perlu asuransi apa" secara terstruktur (hanya saran umum di mitigasi), dana darurat tidak dihitung, kolom "Owner/Status" tidak berguna untuk kafe 3 karyawan.

## Penilaian berdampingan
| Kriteria | Pesaing `risk-assessment` | Skill ini |
|---|---|---|
| Menjawab pertanyaan pengguna (asuransi? dana darurat?) | Sebagian | Penuh |
| Angka dihitung pasti | Tidak ada angka | Ya (script, cocok verifikasi independen) |
| Keputusan asuransi per risiko | Tidak | Ya (dengan cacat aturan untuk risiko tak-terasuransikan, lihat HASIL-UJI) |
| Konteks Indonesia (BPJS, OJK, banjir/gempa) | Tidak | Ya |
| Tolak merek / klaim pasti cair | Tidak diatur | Diatur jelas |
| Bahasa awam ID | Tidak | Ya |
| **Nilai** | **5/10** | **8/10** |

Kesimpulan: skill ini menang telak. Kelebihan pesaing yang patut dipelajari (ditulis ulang dengan cara sendiri): kolom **status** (sudah dikerjakan/belum) untuk dipantau ulang tiap 3–6 bulan.
