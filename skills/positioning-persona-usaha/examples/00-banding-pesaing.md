# Uji banding pesaing (skenario normal 1)

> Uji independen, 2026-09-29. Skill pesaing hanya dibaca untuk dinilai, tidak disalin. Klon dangkal ke folder scratchpad penguji (bukan repo).

## Pencarian
- Kata kunci: "agent skill customer persona positioning STP", "SKILL.md persona positioning", "clawhub persona", "skills.sh positioning".
- Sumber: WebSearch (ClawHub, skills.sh, awesome-openclaw-skills, docs OpenClaw), GitHub `coreyhaines31/marketingskills`, `phuryn/pm-skills`, anthropics/skills (tidak ada skill positioning/persona pemasaran).
- Hasil ClawHub teratas untuk "persona" (mis. "open-persona") adalah **persona untuk agent AI**, bukan persona pelanggan → tidak relevan.
- Pesaing terbaik yang relevan (pembuat kredibel, dirawat, MIT):
  1. `coreyhaines31/marketingskills` → `skills/product-marketing` (v2.1.0, commit 5b2c000, 2026-09-04)
  2. `phuryn/pm-skills` → `pm-market-research/skills/user-personas` + `pm-marketing-growth/skills/positioning-ideas` (commit 8607e3b, 2026-09-14)
- Catatan: keduanya adalah sumber ATM skill ini (lihat `ATTRIBUTION.md`); uji ini memeriksa apakah skill turunan "menang telak".

## Cara kerja pesaing pada permintaan katering Semarang (disimulasikan mengikuti instruksi mereka)
**product-marketing:** menawarkan "auto-draft dari codebase" (tidak relevan bagi UMKM) atau wawancara **satu bagian per giliran** untuk 12 bagian (Product Overview, Target Audience, Personas *B2B only*, Pain Points, Competitive Landscape, Differentiation, Objections & Anti-persona, Switching Dynamics, Customer Language, Brand Voice, Proof Points, Goals). Hasil akhir: file `.agents/product-marketing.md` berbahasa Inggris sebagai konteks untuk skill lain. Tidak memilih segmen, tidak membuat tagline/bio/caption, tidak ada ceklis klaim. Pengguna awam perlu ±12 putaran tanya-jawab sebelum mendapat apa pun.

**user-personas + positioning-ideas:** membuat **3 persona** (JTBD, 3 pain, 3 gain, 1 wawasan tak terduga, product fit) lalu **mengidentifikasi 5 pesaing teratas** dan 5 ide positioning dengan statement "the only [category] designed for ...". Untuk usaha lokal kecil, langkah "identifikasi 5 pesaing" mendorong agent mengarang nama pesaing; "the only ..." mendorong klaim superlatif yang tak terbukti. Tidak ada skor segmen, tagline siap pakai, teks tempel, atau konteks Indonesia.

## Penilaian berdampingan (1-5)
| Kriteria | product-marketing | user-personas + positioning-ideas | **positioning-persona-usaha** |
|---|---|---|---|
| Instan untuk awam (1 kalimat → hasil) | 1 (12 putaran) | 4 | **4** (tanya sekali atau asumsi) |
| Memilih target dengan alasan terukur | 1 | 2 | **5** (script berbobot, teruji) |
| Kedalaman persona/JTBD | 4 (Four Forces, bahasa pelanggan) | 4 (3 persona, wawasan) | **5** (JTBD 3 jenis + Empat Gaya + anti-persona) |
| Kejujuran klaim / tidak mengarang | 3 | 2 ("the only", 5 pesaing) | **5** (FAKTA/HIPOTESIS, `[isi:]`, ceklis) |
| Siap tempel (bio, listing, caption, WA) | 1 | 1 | **5** |
| Konteks Indonesia (Rupiah, WA, marketplace, BPOM/halal/DJKI) | 1 | 1 | **5** |
| Ringkas dibaca | 3 | 3 | **3** (panjang) |
| Nilai jangka panjang (dokumen konteks untuk skill lain) | **5** (versi & changelog) | 2 | 3 (disebut terhubung dengan skill lain, tapi tidak menyimpan dokumen) |
| **Total (maks 40)** | 19 | 19 | **35** |

## Kelebihan pesaing yang patut dipelajari (tulis ulang dengan cara sendiri, jangan salin)
- product-marketing menyimpan hasil sebagai **dokumen konteks berversi** yang dibaca skill lain (caption, landing page). Skill ini bisa menawarkan "simpan ringkasan positioning sebagai file untuk dipakai skill Komunitech lain" (opsional).
- pm-skills memberi **3 persona berbeda** untuk melihat keragaman; skill ini hanya 1 (+1 pendamping) — sudah sesuai fokus UMKM, tidak perlu diubah.

**Kesimpulan:** untuk pasar sasaran (UMKM Indonesia awam), **skill ini menang telak** (35 vs 19). Pesaing unggul hanya pada dokumen konteks berversi.
