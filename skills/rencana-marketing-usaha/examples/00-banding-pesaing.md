# Uji banding pesaing / sumber asli — skenario normal 1 (warung bakso)

> Penguji independen, 2026-09-29. Skill sumber **hanya dibaca untuk dinilai** (tidak disalin): 
> - `marketing-plan` — https://github.com/coreyhaines31/marketingskills/blob/main/skills/marketing-plan/SKILL.md (v1.1.1, MIT, Corey Haines). Diambil 2026-09-29; folder `references/` sumber tidak dimuat (hanya SKILL.md), jadi keluarannya dinilai dari SKILL.md saja.
> - `gtm-strategy` — https://github.com/phuryn/pm-skills/blob/main/pm-go-to-market/skills/gtm-strategy/SKILL.md (MIT, Pawel Huryn).
> Permintaan = `01-uji-warung-bakso.md`. Agent penguji menjalankan tiap skill sesuai instruksinya.

## Keluaran dengan `marketing-plan` (ringkasan)
- Agent memulai fase **INIT** dan mengajukan intake 10 pertanyaan: *funding state (round, runway, burn)*, tim, budget per lini, tooling stack (Customer.io, Stripe, GA4, Mixpanel), *beta or GA?*, dll. Sebagian besar tidak relevan untuk warung bakso.
- Mencoba menyimpan ke `~/marketing-plans/{client}/progress.md` dan menjalankan fase **REVIEW** 13 bagian satu per satu (interaktif, beberapa putaran).
- Struktur AARRR (Acquisition/Activation/Retention/Referral/Revenue); bagian *Activation* (onboarding, paywall, signup) dan *Marketing operations stack* (MCP/API) dipaksakan untuk warung.
- Anggaran: patokan *funding-stage* dalam **USD** ($0-2K/mo bootstrapped = organik saja) dan rumus *goal-based* berbasis **ARR/ARPC/retention** — tidak ada cara menghitung margin per mangkuk atau CAC impas.
- Target panjang 8.000-12.000 kata; merujuk 139 ide `marketing-ideas` yang tidak terpasang.
- Kekuatan: kerangka 70/20/10, "hope is not a strategy" (setiap langkah punya indikator & kill criterion), open decisions eksplisit, north-star metric.

## Keluaran dengan `gtm-strategy` (ringkasan)
- 5 langkah generik (riset -> kanal -> pesan -> metrik -> jadwal peluncuran). Keluaran: daftar kanal (paid search, social, display, content, SEO, outbound, community, PLG) dengan justifikasi umum, *value proposition*, KPI (impressions, CTR, MRR, CAC, LTV, market share), timeline pre-launch/launch/post-launch, 90-day roadmap.
- Tidak ada angka anggaran, tidak ada hitungan, tidak ada konteks Indonesia; orientasi *product launch* SaaS (MRR, market share) — canggung untuk warung yang sudah jalan.

## Keluaran dengan skill kita
`01-uji-warung-bakso.md`.

## Penilaian berdampingan (1-5)
| Kriteria (untuk UMKM Indonesia awam) | marketing-plan | gtm-strategy | **rencana-marketing-usaha** |
|---|---|---|---|
| Relevansi konteks (Rupiah, WA, GoFood, Maps, gajian, musim hujan) | 1 | 1 | **5** |
| Angka dihitung & dapat diverifikasi (margin, CAC/ROAS impas, alokasi, corong) | 2 (rumus ARR, tanpa script) | 1 | **5** (script Decimal, 0 selisih) |
| Cek kelayakan sebelum iklan (margin, potongan platform) | 1 | 1 | **5** |
| Kecepatan / "instan" (satu pesan pertanyaan, 1 dokumen) | 1 (intake + 13 putaran review) | 3 | **5** |
| Bahasa awam | 2 (fCMO, AARRR, ARR, π-shaped) | 2 | **5** |
| Keamanan saran (WA spam, klaim, data pribadi) | 3 | 2 | **5** |
| Kedalaman strategi (portofolio, open decisions, kill criteria) | **5** | 2 | 4 |
| Siap pakai (langkah minggu ini, KPI+pemilik, aturan hentikan) | 4 | 3 | **5** |
| **Total (maks 40)** | **15** | **15** | **39** |

## Kesimpulan
Skill kita **menang telak** untuk UMKM Indonesia: sumber asli dirancang untuk SaaS/startup ber-funding (USD, ARR, MCP stack, 8-12 ribu kata) dan tidak menghitung apa pun yang dibutuhkan warung. Yang diambil dari sumber (70/20/10, corong AARRR -> Kenal/Tertarik/Beli/Beli lagi/Rekomendasi, kill criterion, open decisions, roadmap 90 hari) sudah diadaptasi dan ditulis ulang, bukan terjemahan. Satu keunggulan sumber yang masih bisa dipelajari: **gerbang kualitas pasar (ukuran x frekuensi masalah)** dan penegasan "setiap langkah punya indikator" — skill kita sudah punya aturan hentikan per KPI; gerbang ukuran x frekuensi bisa ditambahkan sebagai 2 baris di langkah 1 (opsional, bukan syarat lulus).

Cakupan banding: hanya dua skill sumber ATM di atas (keduanya dari repo kuat: koleksi populer & dirawat). Pencarian pesaing tambahan di skills.sh/ClawHub **tidak dilakukan** penguji pada sesi ini — bila ingin lengkap, cari kata kunci "marketing plan", "rencana marketing UMKM", "go-to-market" sebelum rilis.
