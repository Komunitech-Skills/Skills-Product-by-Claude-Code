# 00 — Uji banding pesaing (pengajuan-kur)

## Pencarian (2026-09-23)
- GitHub code search: `"Kredit Usaha Rakyat" filename:SKILL.md` (0 hasil), `KUR bank filename:SKILL.md cicilan` (3 hasil, tidak relevan: indonesia-vat, skill "finance" Ozolab yang hanya kalkulasi akuntansi umum), `loan amortization filename:SKILL.md` (±1.384), `"small business loan" application filename:SKILL.md`.
- VoltAgent/awesome-openclaw-skills README: tidak ada skill KUR/pinjaman usaha Indonesia. manairalabs/bicara-skills & alvinindra/bahasa-skills: tidak ada. anthropics/skills: tidak ada.
- **Tidak ada pesaing khusus KUR.** Pesaing terdekat untuk bagian simulasi pinjaman:

| Skill | URL | Lisensi | Catatan |
|---|---|---|---|
| FerroxLabs/wayland `loan-comparison` (foundry-skills) | https://github.com/FerroxLabs/wayland/blob/HEAD/src/process/resources/skills-library/bodies/skills/personal-finance/loan-comparison/SKILL.md | Apache-2.0 (frontmatter) | Instruksi rinci: amortisasi, APR/IRR, biaya, perbandingan 2–4 penawaran → **dipakai untuk banding** |
| AgentPMT `financial-loan-calculator` | https://github.com/AgentPMT/agent-skills | tidak tercantum | Memanggil API eksternal berbayar (tidak dijalankan) |
| Ozolab Indonesia `finance` | https://github.com/edorabma9304/Claude-Skill-by-Ozolab-Indonesia | tidak tercantum | Akuntansi umum UMKM, tidak ada simulasi kredit/KUR |

## S1 dengan instruksi pesaing (loan-comparison)
Skill pesaing mensyaratkan 2–4 penawaran; ia sendiri menyebut kasus "memilih antara tenor" sebagai pemakaian sah, jadi agent membandingkan 36 vs 60 bulan (bunga 6% yang disebut pengguna diasumsikan sebagai *stated rate*, tanpa biaya):

> | | Opsi A: 36 bulan | Opsi B: 60 bulan |
> |---|---:|---:|
> | Monthly payment | Rp 3.042.194 | Rp 1.933.280 |
> | Total interest | Rp 9.518.984 | Rp 15.996.800 |
> | Total repaid | Rp 109.518.984 | Rp 115.996.800 |
> | Effective APR | 6,00% (tanpa biaya) | 6,00% |
>
> **Bottom line:** Opsi A hemat Rp 6,48 jt bunga, tetapi cicilan Rp 3,04 jt adalah 51% dari laba bulanan Anda; Opsi B lebih aman untuk arus kas. Tanyakan biaya provisi/asuransi untuk menghitung APR sebenarnya. *(Disclaimer edukasi, konsultasikan ke penasihat keuangan.)*

(Tidak ada: aturan KUR, bunga acuan, NPWP/agunan, checklist dokumen, profil usaha, rencana dana, bahasa Indonesia.)

## Penilaian
| Kriteria | Pesaing (loan-comparison) | Skill kita |
|---|---|---|
| Kualitas output | Baik untuk perbandingan tenor/biaya | Lengkap: simulasi + rasio + rencana dana + profil + checklist |
| Kesesuaian konteks Indonesia | Rendah (APR/AS, tak kenal KUR, flat vs efektif) | Tinggi (Permenko 1/2026, bunga flat vs efektif, SLIK, NIB) |
| Akurasi | Rumus benar | Rumus benar + fakta regulasi terverifikasi |
| Siap pakai | Sedang (perlu diterjemahkan) | Tinggi |
| **Skor** | 5/10 | 8/10 |

**Skill kita menang** jelas.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- **Perbandingan tenor berdampingan** (mis. 36 vs 60 bulan: cicilan vs total bunga) sebagai bagian standar output — membantu keputusan awam.
- **Biaya di luar bunga** (asuransi, provisi bila ada, materai) masuk ke total biaya/"bunga efektif sebenarnya" bila pengguna punya rinciannya.
- Membandingkan **2–3 penawaran bank** sekaligus (mis. KUR bank A vs kredit komersial bank B).
- Contoh patokan cepat ("100 jt, 6%, 60 bulan ≈ Rp 1,93 jt") untuk menjawab pertanyaan singkat tanpa bertanya.
