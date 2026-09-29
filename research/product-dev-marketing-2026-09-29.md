# Riset: Pengembangan Produk (A) & Strategi Marketing (B) — 2026-09-29

Metode: WebFetch halaman GitHub publik (tanpa clone/jalankan kode; angka bisa sedikit basi). Belum dibaca isi SKILL.md per skill, jadi audit keamanan (Tahap 3) dan cek isi dilakukan saat ATM. Belum ditelusuri: awesome-list, anthropics/skills (tidak ada skill marketing/PM bersinyal di sana berdasarkan sesi sebelumnya; cek ulang bila sempat).

## 1. Sumber kuat (diurutkan)

| # | Repo | Bintang/Fork | Lisensi | Update | Isi relevan | Jalur ambil |
|---|------|-------------|---------|--------|-------------|-------------|
| 1 | github.com/coreyhaines31/marketingskills | 51,9k / 7,8k, 473 commit | MIT | aktif | 60 skill: marketing-plan, launch, pricing, product-marketing, competitors, competitor-profiling, ads, ad-creative, content-strategy, offers, lead-magnets, referrals, marketing-loops, marketing-psychology, customer-research, analytics, attribution, community-marketing, influencer-marketing, public-relations, dll. | Salin-edit (MIT, atribusi + teks lisensi). Sudah diadaptasi: copywriting/landing, seo-audit, prospecting |
| 2 | github.com/phuryn/pm-skills | 26,7k / 2,8k, 69 skill + 42 workflow, 9 plugin | MIT | commit terakhir 14 Sep 2026; sejak Mar 2026; rilis v2.0 (5 Jun), v2.1 (3 Jul); ada kontributor luar (PR #6) | pm-go-to-market (gtm-strategy, beachhead-segment, ideal-customer-profile, growth-loops, gtm-motions, competitive-battlecard), pm-marketing-growth (positioning-ideas, value-prop-statements, product-name, north-star-metric), pm-product-strategy (value-proposition, lean-canvas, business-model, monetization/pricing-strategy, SWOT, PESTLE, Porter, Ansoff), pm-market-research (user-personas, market-segments, journey-map, market-sizing, competitor-analysis), pm-execution (create-prd, outcome-roadmap, user-stories, pre-mortem, release-notes), pm-product-discovery (interview-script, summarize-interview, assumptions, experiments, prioritize-features) | Salin-edit (MIT). Catatan sinyal: umur ±6 bulan, 67 commit; bintang sangat tinggi, tapi pembuat individu. Lolos ≥3 sinyal (populer, dirawat, ada PR luar, kualitas). Tetap cek per skill |
| 3 | github.com/product-on-purpose/pm-skills | 700 / 90, 68 skill, v2.33.0 (29 Agu 2026), 873 commit | Apache-2.0 | aktif mingguan | deliver-prd, deliver-launch-checklist, deliver-user-stories, define-jtbd-canvas, foundation-persona, foundation-lean-canvas, discover-competitive-analysis, discover-market-sizing, measure-experiment-design, measure-survey-analysis, iterate-lessons-log, iterate-pivot-decision, tool-design-sprint-* (7), 200+ contoh output | Salin-edit (Apache: NOTICE + keterangan diubah). Sudah dipakai: validasi-ide-produk-baru |
| 4 | github.com/deanpeters/Product-Manager-Skills | 7,1k / 848, 77 skill, v0.84 | **CC BY-NC-SA 4.0** | aktif | positioning, PRD, discovery, RICE/ICE, TAM/SAM/SOM, 14 skill intelijen pasar, lifecycle/EOL | **DILARANG salin-edit untuk dijual** (NC). Hanya tulis ulang bersih (2 agent) bila perlu. Karena #2 dan #3 (MIT/Apache) sudah menutup topik yang sama, **tidak perlu dipakai**. Catat "PERLU REVIEW" bila pemilik ingin. |

## 2. Peta celah (A dan B vs katalog)

Sudah ada: validasi-ide-produk-baru, brainstorming-ide-usaha, riset-calon-pelanggan, riset-harga-kompetitor, hitung-hpp, harga-jual-marketplace, analisis-ulasan, copy-landing-page, audit-seo-toko-online, pesan-prospek-wa, kalender-konten-30hari, konten-mingguan, promo-kalender, audit-akun-iklan, laporan-iklan-mingguan, studio-video-pendek-ai, kpi-tim.

| Kebutuhan | Status | Sumber terbaik |
|-----------|--------|----------------|
| Spesifikasi produk / PRD ringan (UMKM: produk fisik, F&B, fashion, jasa) | KOSONG | phuryn create-prd + pop deliver-prd |
| Roadmap & prioritas fitur/produk | KOSONG | phuryn outcome-roadmap, prioritize-features; pop define-prioritization |
| Persona + segmentasi + STP | KOSONG (riset-calon-pelanggan hanya riset) | phuryn user-personas, market-segments, ideal-customer-profile |
| Positioning + value proposition | KOSONG | phuryn value-proposition, positioning-ideas; marketingskills product-marketing |
| Strategi harga (bukan hitung HPP) | SEBAGIAN (hitung-hpp, harga-jual-marketplace) | marketingskills pricing; phuryn pricing-strategy |
| Rencana marketing tahunan/kuartalan + anggaran + funnel/KPI | KOSONG | marketingskills marketing-plan; phuryn north-star-metric |
| Go-to-market + rencana peluncuran + kampanye launch | KOSONG | marketingskills launch; phuryn gtm-strategy; pop deliver-launch-checklist |
| Analisis kompetitor & battlecard (strategis) | SEBAGIAN (harga saja) | marketingskills competitors/competitor-profiling; phuryn competitive-battlecard |
| Prototipe & uji pasar (pre-order, MVP via WA/marketplace, uji coba) | KOSONG | phuryn experiments/assumptions; pop measure-experiment-design; tulis sendiri konteks lokal |
| Iterasi dari feedback (pivot, lessons, survei) | SEBAGIAN (analisis-ulasan) | pop iterate-pivot-decision, measure-survey-analysis |
| Strategi konten & iklan (strategi, bukan kalender/audit) | SEBAGIAN | marketingskills content-strategy, ads, ad-creative |
| Brand strategy / naming | KOSONG | phuryn product-name; marketingskills offers |
| Referral / program loyalitas | KOSONG | marketingskills referrals |
| Bisnis model / lean canvas | KOSONG | phuryn lean-canvas; pop foundation-lean-canvas |

## 3. Rekomendasi daftar bangun (skill), sumber terkuat dulu

Semua nama baru; harga usulan mengikuti pola tier lama (ecer 49-99 rb, bundle "Paket Produk & Marketing"). Nilai tambah wajib: Rupiah, marketplace/WA/IG/TikTok, konteks UMKM, script hitung (anggaran, titik impas, skor prioritas).

| Prio | Skill | Sumber | Jalur lisensi | Nilai tambah Indonesia | Usaha |
|------|-------|--------|---------------|------------------------|-------|
| 1 | `rencana-marketing-usaha` (tahunan/kuartalan: tujuan, STP ringkas, saluran, anggaran, kalender, KPI) | marketingskills marketing-plan + phuryn gtm-strategy | Salin-edit MIT (dua sumber, atribusi keduanya) | Alokasi anggaran per kanal (script), CAC/ROAS/BEP dalam Rupiah, musim Ramadan/Harbolnas/gajian, kanal WA/marketplace/IG/TikTok Shop | Sedang-Besar |
| 2 | `positioning-persona-usaha` (persona, segmen, STP, value proposition, positioning) | phuryn user-personas, market-segments, value-proposition; marketingskills product-marketing | Salin-edit MIT | Contoh persona lokal (ibu rumah tangga, mahasiswa, pemilik warung), bahasa awam, keluaran siap tempel ke listing/caption | Sedang |
| 3 | `luncurkan-produk-baru` (GTM + checklist + kampanye peluncuran + pre-order/soft launch) | marketingskills launch; pop deliver-launch-checklist (Apache); phuryn gtm-motions | Salin-edit MIT + Apache (NOTICE) | Jadwal H-30..H+14, soft launch di grup WA/komunitas, pre-order, tautan ke skill konten/iklan yang sudah ada | Sedang |
| 4 | `spesifikasi-produk-usaha` (PRD ringan + prioritas + roadmap; produk fisik, F&B, fashion, jasa) | phuryn create-prd, outcome-roadmap, prioritize-features; pop deliver-prd | Salin-edit MIT + Apache | Templat per jenis usaha (resep/BOM, ukuran/bahan, paket jasa), skor prioritas dihitung script, tautan ke hitung-hpp | Sedang-Besar |
| 5 | `strategi-harga-produk` (nilai vs biaya vs pesaing, paket/tier, uji harga) | marketingskills pricing; phuryn pricing-strategy | Salin-edit MIT | Pakai hitung-hpp, margin setelah fee marketplace/ongkir, psikologi harga lokal (Rp 99.000, paket hemat), script sensitivitas | Sedang |
| 6 | `analisis-pesaing-strategis` (peta pesaing, SWOT, battlecard, celah) | marketingskills competitors/competitor-profiling; phuryn competitive-battlecard | Salin-edit MIT | Pesaing di marketplace/IG/GMaps lokal, input manual (tanpa scraping login, sesuai keputusan pemilik), keluaran tabel + tindakan | Sedang |
| 7 | `uji-pasar-produk-cepat` (asumsi, MVP, pre-order, survei, kriteria lanjut/berhenti/pivot) | phuryn identify-assumptions, brainstorm-experiments; pop measure-experiment-design, iterate-pivot-decision | Salin-edit MIT + Apache | Uji lewat status WA, marketplace, pre-order, sampel F&B; ambang keputusan dihitung script; melengkapi validasi-ide-produk-baru | Sedang |
| 8 | `iterasi-dari-masukan-pelanggan` (kumpul, kelompokkan, prioritas, rencana perbaikan) | pop measure-survey-analysis, iterate-lessons-log; phuryn prioritize-features | Salin-edit MIT + Apache | Masukan dari WA/ulasan/DM, ekstensi dari analisis-ulasan; format perubahan + pengumuman ke pelanggan | Kecil-Sedang |

Cadangan: `strategi-konten-iklan` (marketingskills content-strategy, ads), `program-referral-loyalitas` (referrals), `strategi-merek-usaha` (product-name, offers). Bundle usulan: "Paket Produk & Marketing" = 1-8.

Catatan: skill hukum tidak diusulkan (keputusan pemilik). Deanpeters tidak dipakai (NC-SA). Tumpang tindih 1-3 sengaja dirujuk-silang, bukan diduplikasi.

## 4. Produk jalur 2 (jalan lokal, tanpa biaya bulanan)

| Produk | Bintang | Lisensi | Berat pasang | Verdict |
|--------|---------|---------|-------------|---------|
| **Umami** (analitik web, pengganti GA) github.com/umami-software/umami | 39,1k | MIT | Node 18.18+ dan PostgreSQL, atau docker-compose | **PRIORITAS 1**: MIT, ringan, cocok untuk toko/landing page; skill orisinal `analitik-web-umami` + panduan. Catatan: perlu server publik bila situs publik (sama seperti pantau-website-toko), atau uji lokal |
| **Fider** (papan masukan/voting fitur) github.com/getfider/fider | 4,5k | AGPL-3.0 | Go + PostgreSQL | **PRIORITAS 2** untuk jalur iterasi (skill 8): AGPL tidak didistribusikan (pola siyuan/vikunja), skill orisinal. Bintang rendah (4,5k) tapi aktif |
| **listmonk** (email newsletter) github.com/knadh/listmonk | 23,6k / 2,6k | AGPL-3.0 | Satu binary Go + PostgreSQL | **PRIORITAS 3**: ringan, berguna untuk retensi; butuh SMTP (Brevo/SES) dan daftar opt-in, jangan blast tanpa izin (selaras larangan blast). Skill orisinal + panduan |
| Plane (roadmap/sprint) github.com/makeplane/plane | 60,1k | AGPL-3.0 | Docker Compose, Postgres+Redis (berat) | Tunda: sudah ada vikunja-tugas; berat untuk awam |
| Formbricks (survei) github.com/formbricks/formbricks | 13k | AGPL-3.0 + folder `ee` berlisensi terpisah | Docker, Postgres, banyak layanan (berat) | Tunda: berat; pakai formulir sederhana dulu |
| Mautic (automation) github.com/mautic/mautic | 10,6k | GPL-3.0 (halaman hanya menulis "LICENSE.txt"; verifikasi) | PHP + MySQL + cron (berat) | Tunda/tolak: terlalu rumit untuk awam |
| Penpot (desain) github.com/penpot/penpot | 60,5k | MPL-2.0 | Docker/K8s (berat) | Tunda: fokus desain, bukan produk-marketing; pengguna sudah pakai Canva |
| Plausible, PostHog OSS | tidak dicek | Plausible AGPL, PostHog MIT (ee terpisah), dari pengetahuan umum | Berat (ClickHouse) | Tidak diprioritaskan; Umami lebih ringan |

Jalur 2 kecil buatan Komunitech (alternatif): "Pelacak eksperimen produk" berbasis CSV + Python standar (skor prioritas, hasil uji pasar), tanpa server, cocok untuk paket skill 4/7/8.

## 5. PERLU REVIEW
- Pemilik: apakah Deanpeters (CC BY-NC-SA) dilewati sepenuhnya (rekomendasi: ya).
- phuryn/pm-skills berumur ±6 bulan dengan 67 commit; verifikasi ulang isi skill (bukan klaim README) sebelum ATM.
- Lisensi Mautic dan status Plausible/PostHog perlu dicek langsung bila dipilih.
- Belum dilakukan: audit isi/keamanan per SKILL.md, awesome-list, uji pesaing.
