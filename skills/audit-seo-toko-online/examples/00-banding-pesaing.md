# Uji Banding Pesaing

> Dibuat oleh **penguji independen**, Tahap 6 butir 5 pedoman kurasi Komunitech. Skill pesaing dibaca langsung dari repo publik (clone lokal sementara di scratchpad penguji) untuk dinilai, **tidak disalin isinya**.

## Kata kunci pencarian & sumber yang dicek
Dicari lewat web search: "SEO audit skill for Claude Code/OpenClaw", "ClawHub skills.sh seo audit agent skill". Kandidat yang muncul: `JeffLi1993/seo-audit-skill`, `dtsola/xiaoyaoclaw-seo-skill`, `RankSpotAI/awesome-seo-agent-skills` (daftar kurasi, bukan skill tunggal), `ryudi84/sovereign-seo-audit` (ClawHub), `mattvalenta/pls-seo-audit` (ClawHub), `coreyhaines31/marketingskills` (sumber ATM kita sendiri, dibandingkan juga di bawah).

## 1. Skill sumber ATM kita: `coreyhaines31/marketingskills` → `skills/seo-audit`
Dibaca langsung dari `SKILL.md` (499 baris, clone lokal, tidak disalin isinya).

| Aspek | `seo-audit` (sumber) | `audit-seo-toko-online` (kita) |
|---|---|---|
| Bahasa & audiens | Inggris, ditulis untuk konsultan/agency SEO profesional yang mengaudit situs SaaS/e-commerce besar | 100% Bahasa Indonesia awam, tiap istilah dijelaskan satu kalimat (`references/istilah-seo.md`) |
| Script/alat | **Tidak ada script sama sekali** — hanya instruksi + daftar tools eksternal berbayar (Screaming Frog, Ahrefs, Semrush) atau Search Console | `scripts/cek_halaman.py` teruji (41 tes unit) yang benar-benar menghitung panjang title/meta, validasi JSON-LD, dll., tanpa akun/API apa pun |
| Ambang title/meta | 50-60 / 150-160 karakter (disebut sebagai rekomendasi umum, tanpa disclaimer piksel vs karakter) | 30-60 / 70-155, eksplisit disclaimer "Google memotong berdasarkan piksel, ini perkiraan" di tiap laporan |
| Cakupan lokal Indonesia | Hanya "Local Business" generik (NAP, GBP, local schema) tanpa detail | NAP + Google Bisnisku + `LocalBusiness` format alamat Indonesia lengkap, kata kunci lokal Indonesia (`references/lokal-dan-gmb.md`) |
| Larangan teknik terlarang | Disebut implisit lewat E-E-A-T/thin content, tidak melarang eksplisit beli backlink/ulasan palsu/jaminan ranking | Larangan eksplisit + tegas untuk ketiganya, dengan alasan risiko konkret (lihat skenario 05) |
| Cakupan | Full-site audit (robots.txt, sitemap, hreflang internasional, crawl budget) — jauh lebih luas dari 1 halaman | Sengaja dibatasi ke 1 halaman + GBP untuk UMKM (skala & kebutuhan berbeda, disebutkan di ATTRIBUTION.md) |

**Kesimpulan vs sumber ATM:** Skill kita **menang telak untuk target audiens UMKM Indonesia awam** (bahasa, angka yang benar-benar dihitung lewat script gratis, konteks lokal), sementara sumber lebih cocok untuk audit teknis skala penuh oleh profesional berbahasa Inggris dengan akses tools berbayar. Ini konsisten dengan kesimpulan ATTRIBUTION.md — bukan klaim baru penguji.

## 2. Pesaing independen: `JeffLi1993/seo-audit-skill` (varian `seo-audit`, bukan `seo-audit-full`)
Dibaca langsung dari clone lokal (`SKILL.md` 383 baris, `scripts/fetch-page.py`, `scripts/check-page.py`, `references/REFERENCE.md`) — **tidak disalin**.

| Aspek | `seo-audit-skill` (JeffLi1993) | `audit-seo-toko-online` (kita) |
|---|---|---|
| Cara ambil halaman | **Mengambil URL langsung via internet** (`scripts/fetch-page.py` pakai library `requests`, spoof User-Agent Chrome) | Tidak pernah mengakses internet; bekerja dari HTML yang ditempel/diambil agent — sesuai target "tanpa setup" untuk agent tanpa akses web |
| Dependensi | **Butuh `pip install requests`** (library luar) — kalau belum terpasang, skrip langsung `sys.exit(1)` dengan pesan minta instal | Hanya pustaka standar Python (`argparse`, `json`, `re`, `html.parser`, `pathlib`) — sesuai aturan "tanpa instalasi paket" pedoman kurasi Komunitech §1 |
| Bahasa & lokalisasi | Bahasa Inggris, ambang title/meta 50-60/120-160, tidak ada contoh Indonesia, NAP, atau Rupiah sama sekali (dicek dengan `grep -i "NAP\|indonesia\|rupiah"` — nihil) | Bahasa Indonesia penuh + lokalisasi lengkap (NAP, GBP, kata kunci lokal, schema alamat Indonesia) |
| Larangan teknik terlarang / jaminan ranking | Dicek dengan `grep -i "guarantee\|fake review\|buy backlink\|search volume"` di seluruh isi skill → **nihil**, tidak ada larangan eksplisit maupun disclaimer soal ini | Larangan eksplisit + tegas (beli backlink, ulasan palsu, jaminan ranking) di `SKILL.md` & `references/lokal-dan-gmb.md` |
| Output | Laporan HTML lewat template (`assets/report-template.html`), disimpan ke file `reports/<hostname>-audit.html` | Laporan Markdown terstruktur (`templates/laporan-audit.md`) langsung di chat, plus teks siap tempel |
| Skala target | Audiens teknis (developer/marketer yang nyaman `npx skills add`, jalankan Python dgn dependensi, baca laporan HTML) | Pemilik UMKM awam teknologi — instalasi cukup salin folder, tanpa command line/paket tambahan untuk memakainya |
| Lisensi | MIT (dicek langsung, `Copyright (c) 2026 Jeff`) — tidak relevan karena tidak ada materinya yang disalin, hanya dibaca untuk pembanding |

**Kesimpulan vs pesaing independen:** Untuk **audiens target kita** (UMKM Indonesia awam, tanpa akses agent yang bisa browsing internet, tanpa mau install paket Python), skill kita **unggul** karena tidak butuh koneksi internet dari skrip, tidak butuh dependensi luar, dan berbahasa Indonesia dengan konteks lokal penuh. Untuk **audiens developer teknis berbahasa Inggris yang agennya sudah bisa browsing web**, pesaing ini punya kelebihan sah: bisa audit langsung dari URL tanpa perlu pengguna menempel HTML manual, dan punya deteksi SPA/prerender (bandingkan response Googlebot UA vs browser UA) yang tidak ada di skill kita. Ini kelebihan nyata, dicatat jujur — tapi tidak relevan untuk target pembeli komunitech.com yang mayoritas awam teknologi dan skillnya harus "tanpa setup" (pedoman kurasi Komunitech §1).

## Ide yang layak dipertimbangkan untuk versi berikutnya (bukan disalin, hanya diamati)
- Deteksi SPA/JS-rendering via perbandingan ukuran respons Googlebot-UA vs browser-UA (dari `seo-audit-skill`) — tidak relevan langsung karena skill kita offline, tapi prinsipnya bisa diadaptasi jadi pertanyaan manual ke pengguna ("apakah situsmu dibuat pakai React/Vue single-page app tanpa SSR?").
- Format laporan HTML siap unduh (dari `seo-audit-skill`) sebagai opsi tambahan di versi mendatang, di luar cakupan revisi wajib saat ini.

## Kesimpulan akhir
Skill kita **tidak kalah** dari kedua pembanding untuk target pasarnya (UMKM Indonesia awam teknologi, tanpa akses internet/paket tambahan di skrip) — memenuhi syarat Tahap 6 butir 5 pedoman kurasi Komunitech untuk tidak otomatis dibatasi skor maksimal 6.
