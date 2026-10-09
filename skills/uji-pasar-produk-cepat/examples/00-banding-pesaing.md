# Uji banding pesaing (skenario normal 1)

> Dibuat oleh penguji independen (2026-09-29). Skill pesaing hanya **dibaca untuk dinilai** dari clone sementara di scratchpad penguji, tidak disalin ke folder ini.

## Pesaing yang dicari
Kata kunci: "experiment design", "A/B test analysis", "pretotype", "validation experiment", "pm-skills" di GitHub (pencarian repo diurutkan bintang).

| Kandidat | Bukti | Skill yang dinilai |
|---|---|---|
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) (MIT, commit `8607e3b`) | ±26.600 bintang, ±2.800 fork, aktif | `brainstorm-experiments-new` (desain pretotype) + `pm-data-analytics/ab-test-analysis` (analisis hasil) |
| [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) (Apache-2.0, commit `1cef1a9`) | ±700 bintang, ±90 fork | `measure-experiment-design`, `measure-experiment-results` |

Keduanya juga sumber ATM skill ini. Pesaing terkuat untuk skenario "sudah ada data, lanjut atau tidak" = phuryn `ab-test-analysis` + `brainstorm-experiments-new` (satu-satunya dengan ambang X% dan analisis signifikansi). skills.sh/ClawHub tidak diperiksa langsung (tidak ada akses API dari lingkungan uji); dicatat sebagai keterbatasan.

## Input (sama dengan 00-pembanding-tanpa-skill.md)
Nastar Rp95.000, HPP Rp58.000, pre-order WA ke 120 kontak (sebagian keluarga), 21 DP, target 15%, "lanjut produksi 300 toples?"

## Ringkasan keluaran pesaing (dijalankan penguji mengikuti instruksi pesaing)
- **phuryn `brainstorm-experiments-new`:** menyusun hipotesis XYZ ("At least 15% of existing WA customers will pay a deposit"), menyarankan 2-3 pretotype (landing page, email, pre-order), prinsip skin-in-the-game. Hasil 17,5% > 15% → hipotesis "validated". Tidak ada rentang ketidakpastian, tidak ada aturan jumlah sampel, tidak ada perlakuan bias keluarga.
- **phuryn `ab-test-analysis`:** dirancang untuk dua varian (control vs variant); untuk satu proporsi tanpa pembanding, instruksinya meminta hipotesis, durasi, SRM, guardrail metric, lift relatif. Tidak ada varian kontrol, jadi hampir seluruh tabel kosong/tidak relevan. Rumus sample size yang disebut `n = (Z² × 2 × p(1-p)) / MDE²` tidak memasukkan power padahal teks meminta cek power 80%. Rekomendasi "Ship/Extend/Stop" berbahasa korporat software (roll out 100%).
- **product-on-purpose `measure-experiment-results`:** dokumen laporan panjang (segment analysis, guardrail, appendix) bergantung template; cocok tim produk, terlalu berat untuk pemilik UMKM.

## Penilaian berdampingan (1-5)
| Kriteria | phuryn (gabungan) | product-on-purpose | **uji-pasar-produk-cepat** |
|---|---|---|---|
| Angka dihitung, bukan dikira (script teruji) | 2 (hanya "generate script bila perlu") | 1 | **5** (script + tes, terverifikasi) |
| Rentang ketidakpastian satu proporsi | 1 | 3 (minta CI, tanpa cara) | **5** (Wilson) |
| Keputusan jelas untuk UMKM | 3 | 2 | **5** (LANJUT/UBAH/STOP + batas stop) |
| Konteks Indonesia (WA, PO, bazar, marketplace, PIRT/BPOM, Rupiah) | 1 | 1 | **5** |
| Kejujuran pre-order / etika | 2 (skin-in-the-game saja) | 1 | **5** (refund, tanpa testimoni palsu) |
| Rigor perbandingan dua varian (power) | 3 (menyebut power 80%) | 4 (MDE + power disebut) | **2** (panduan sampel dua varian terlalu optimis, tanpa power) |
| Bahasa awam | 2 | 1 | **5** |
| **Total** | 14 | 13 | **32** |

## Kesimpulan
Skill kita **menang jelas** untuk skenario normal 1 dan untuk audiens UMKM. Satu kelebihan pesaing yang perlu dipelajari (tanpa menyalin): pesaing menyebut **power/MDE** untuk desain uji dua varian. Skill kita belum punya itu, dan angka "150-300 per varian" / "100-150 per varian untuk selisih 10 poin" terlalu optimis (lihat HASIL-UJI.md, bug B2). Perbaiki dengan cara sendiri.
