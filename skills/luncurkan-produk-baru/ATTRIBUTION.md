# Atribusi

Skill **luncurkan-produk-baru** adalah karya turunan (jalur kurasi, ATM: Amati-Tiru-Modifikasi) oleh Komunitech (komunitech.com) dari tiga sumber terbuka. Bagian yang berasal dari sumber hanyalah **kerangka**: fase peluncuran bertahap, kerangka saluran milik/sewa/pinjam (ORB), gerbang kesiapan, gerbang go/no-go + rencana mundur, dan pemilihan 2-4 gerakan pemasaran. Seluruh isi lokal Indonesia (jadwal T-30..T+30, kanal WA/marketplace/TikTok/bazar, aturan promo, stok, label halal/BPOM/PIRT, script jadwal, contoh sambal) adalah tambahan Komunitech.

## Sumber

| # | Sumber | Pembuat | Berkas yang dibaca | Lisensi | Teks lisensi |
|---|--------|---------|--------------------|---------|--------------|
| 1 | https://github.com/coreyhaines31/marketingskills (skill `launch`, `skills/launch/SKILL.md`, versi 2.0.2) | Corey Haines | SKILL.md | MIT, Copyright (c) 2025 Corey Haines | `licenses/LICENSE-MIT-marketingskills.txt` |
| 2 | https://github.com/phuryn/pm-skills (skill `gtm-motions`, `pm-go-to-market/skills/gtm-motions/SKILL.md`) | Pawel Huryn | SKILL.md | MIT, Copyright (c) 2026 Pawel Huryn | `licenses/LICENSE-MIT-pm-skills-phuryn.txt` |
| 3 | https://github.com/product-on-purpose/pm-skills (skill `deliver-launch-checklist`, versi 2.2.0) | product-on-purpose | SKILL.md (juga templat `references/TEMPLATE.md`, hanya dibaca untuk struktur) | Apache-2.0 | `licenses/LICENSE-Apache-2.0-pm-skills-product-on-purpose.txt` |

Ketiga sumber dibaca penuh dan diaudit pada 2026-09-29: hanya berisi teks instruksi (tanpa script, tanpa tautan unduhan, tanpa perintah destruktif, tanpa instruksi tersembunyi/prompt injection, tanpa kunci atau data pribadi).

## Yang diambil dan diubah

- Dari #1: fase bertahap (internal, alfa, beta, akses awal, penuh), kerangka ORB, gerbang "Simple-Lovable-Complete", daftar periksa pra/hari-H/pasca. Diubah total: ditulis ulang dalam Bahasa Indonesia untuk produk fisik/jasa UMKM; Product Hunt, Hacker News, email, blog, dan konteks SaaS dibuang; diganti WA, marketplace, IG/TikTok, bazar, KOL mikro.
- Dari #2: gagasan memilih 2-4 gerakan pemasaran dan menskor kecocokannya. Diubah menjadi tabel saluran UMKM Indonesia (`references/kanal-checklist.md`); alat SaaS dibuang.
- Dari #3: gagasan daftar kesiapan lintas fungsi dengan pemilik, tanggal, kriteria go/no-go, dan rencana mundur. Diubah menjadi kesiapan stok/operasional/legal untuk usaha kecil (`references/runbook-hari-h.md`).

**Keterangan Apache-2.0 (bagian 4 lisensi): file telah diubah.** Semua file dalam folder ini yang memuat gagasan dari sumber #3 adalah **versi yang telah diubah** oleh Komunitech dari aslinya dan bukan produk pembuat asli. Sumber #3 tidak memiliki berkas `NOTICE` (dicek: `NOTICE` tidak ada di repo per 2026-09-29), sehingga tidak ada teks NOTICE yang diteruskan. Pemberitahuan hak cipta, paten, merek, dan atribusi dari sumber asli dipertahankan lewat berkas ini dan folder `licenses/`.

Komunitech **tidak berafiliasi** dengan, dan tidak didukung oleh, Corey Haines, Pawel Huryn, product-on-purpose, maupun pihak mana pun yang disebut di sini. Nama proyek dipakai hanya untuk atribusi.

## Materi tambahan Komunitech (orisinal)

`scripts/jadwal_peluncuran.py` dan `tests/`, daftar libur nasional (disalin dari skill kalender-pajak Komunitech; sumber SKB 3 Menteri di dalam script), seluruh folder `references/`, `templates/`, `examples/`, dan README. Lisensi materi tambahan: proprietary Komunitech; penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian. Bagian turunan tetap tunduk pada lisensi MIT/Apache-2.0 sumbernya (lihat `licenses/`).
