# Uji banding pesaing - Skenario 01

> Penguji independen, 2026-09-28. Skill pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pencarian
- Web search: "competitor price research skill SKILL.md github", "kopi arabika gayo bubuk 250 gr harga" (untuk data nyata).
- GitHub (MCP search): repo `phuryn/pm-skills`, `OneWave-AI/claude-skills`. Kandidat lain yang muncul tetapi bukan riset harga produk fisik: `coreyhaines31/marketingskills` competitor-profiling (tier harga SaaS), `anthropics/knowledge-work-plugins` competitive-brief, `ChenneyZhuang/competitor-recon` (keluhan ulasan), `github/awesome-copilot` competitor-ad-intelligence.
- Tidak ditemukan skill publik berbahasa Indonesia untuk riset harga marketplace (Shopee/Tokopedia) dengan hitung batas untung.

## Pesaing yang dinilai
| Skill | Sumber | Sinyal | Fokus |
|---|---|---|---|
| **pricing-strategy** | github.com/phuryn/pm-skills (pm-product-strategy/skills/pricing-strategy) | ±26,6k bintang, 2,8k fork, aktif (dicek 2026-09-28) | Strategi harga produk digital/SaaS: model harga, tier, Van Westendorp, eksperimen |
| competitor-price-tracker | github.com/OneWave-AI/claude-skills | ±309 bintang, koleksi 200+ skill | Pantau halaman harga pesaing & alert perubahan; tanpa rumus/script |

## Skenario 01 dijalankan dengan pesaing utama (pricing-strategy)
Agent mengikuti alurnya (nilai, model harga, analisis kompetitif, struktur tier, sensitivitas, eksperimen). Ringkasan output:
> Recommended Model: Flat-rate per pack. Value metric: per kemasan.
> | Tier | Price | Target | Positioning | -> 250 g Rp 55.000 (mid-market), 500 g Rp 99.000, 1 kg Rp 185.000.
> Posisi: kamu di premium (Rp 58.000 vs pesaing Rp 42.500-80.000). Asumsi: willingness-to-pay pembeli kopi specialty lebih tinggi -> uji A/B harga di halaman produk. Risiko: perang harga -> tonjolkan kualitas.

## Penilaian berdampingan (skala 1-10)
| Kriteria | pricing-strategy (phuryn) | competitor-price-tracker (OneWave) | riset-harga-kompetitor (kita) |
|---|---|---|---|
| Relevan untuk UMKM marketplace | 3 (SaaS: seat, freemium, annual discount) | 4 | 9 |
| Penyetaraan ukuran 200/500/1000 g | 2 (tidak ada; perbandingan dilakukan agent seadanya) | 1 | 8 (bug `1/2 kg`, `250 g x 2`) |
| Batas untung dari HPP + biaya marketplace | 1 | 1 | 10 |
| Akurasi & auditabilitas angka | 3 | 2 | 10 (0 selisih) |
| Penanganan link diblokir / etika scraping | 3 ("use web search") | 2 (mendorong pemantauan) | 9 |
| Bahasa & konteks Indonesia | 1 | 1 | 9 |
| Ide strategis (eksperimen harga, asumsi yang perlu diuji) | **8** | 5 | 6 |
| **Rata-rata** | **3,0** | **2,3** | **8,7** |

**Kesimpulan:** skill kita **menang telak** untuk tugas ini. Kelebihan pesaing yang layak dipelajari (ditulis ulang dengan cara sendiri, bukan disalin): pricing-strategy selalu menutup dengan "asumsi yang perlu divalidasi + cara mengujinya" (mis. uji harga 2 minggu, pantau konversi). Usul: tambahkan satu baris "Cara menguji harga baru" di bagian Saran (mis. pasang harga X selama 14 hari, bandingkan jumlah pesanan & kunjungan).
