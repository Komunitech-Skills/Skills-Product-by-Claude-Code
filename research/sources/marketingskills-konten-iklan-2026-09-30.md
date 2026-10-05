# Sumber ATM: marketingskills `content-strategy` + `ads` (untuk skill `strategi-konten-iklan`) - 2026-09-30

| Hal | Catatan |
|---|---|
| Sumber | skill `content-strategy` (SKILL.md v2.1.1, `references/headless-cms.md`, `content-distribution.md`) dan skill `ads` (judul "Paid Ads", SKILL.md v2.3.2, 14 file `references/`). Catatan: tidak ada folder bernama `paid-ads`; skill iklan berbayar berada di folder `skills/ads/`. |
| URL | https://github.com/coreyhaines31/marketingskills (folder `skills/content-strategy/` dan `skills/ads/`) |
| Pembuat | Corey Haines (perorangan; repo koleksi yang sama sudah dipakai untuk skill kita `program-referral-loyalitas` dan lainnya) |
| Verifikasi web | Halaman repo dibuka 2026-09-30: MIT License, sekitar 52 rb bintang, sekitar 7,8 rb fork, 473 commit di main, 60+ skill. |
| Snapshot | `git clone --depth 1` 2026-09-30, commit `5b2c0007766c6a1cf1d53fd8fc73e979e0821022` (commit tanggal 2026-09-04) |
| Lisensi | MIT, Copyright (c) 2025 Corey Haines (file `LICENSE` root dibaca; disalin ke skill sebagai `LICENSE-MIT-marketingskills`) |
| Sinyal bukti | Popularitas (bintang/fork sangat tinggi), perawatan (ratusan commit, aktif September 2026), komunitas (fork ribuan), isi berstruktur (ada `evals/evals.json` per skill). Lolos >= 3 sinyal. |
| Audit keamanan | Isi kedua folder: file `.md` + `evals/evals.json`. Tidak ada script; tidak ada yang dijalankan. SKILL.md dan referensi dibaca (pencarian pola `curl`/`wget`/`base64`/`eval`/"ignore previous" hanya menemukan satu kalimat pembela di `ads/references/audit-guardrails.md` yang justru memperingatkan agar tidak mengikuti instruksi tersembunyi di halaman/ekspor). Tidak ada kunci/token tertanam. Bagian "Tool Integrations" (akses akun iklan lewat alat pihak ketiga) tidak dipakai. |
| Keputusan | **DIPAKAI (ATM, MIT, atribusi).** Nilai tambah: konteks UMKM Indonesia (Meta/IG, TikTok, Shopee Ads, TikTok Shop Ads, Google Ads), momen belanja lokal (gajian, tanggal kembar, Ramadan, Harbolnas), script `alokasi_anggaran.py` (angka format Indonesia, ambigu ditolak, titik impas ROAS dari margin, batas uji, pembulatan dengan total tetap), uji regresi 30 kasus, catatan kategori terbatas (kesehatan/keuangan/kripto), tanpa janji hasil. |

## Yang diadaptasi (ide/struktur, ditulis ulang)
- Pilar konten 3-5 dan klaster; pemetaan topik ke tahap corong (awareness/pertimbangan/beli).
- Anggaran fase uji ~70/30, kenaikan bertahap ~20% dan jeda 3-5 hari, hierarki uji kreatif, titik impas sebagai patokan target.

## Yang TIDAK dipakai
SEO/CMS headless, backlink/format link-earning untuk situs SaaS, LinkedIn/ABM/B2B, payback period SaaS, otomasi akses langsung ke akun iklan, contoh & harga dolar.
