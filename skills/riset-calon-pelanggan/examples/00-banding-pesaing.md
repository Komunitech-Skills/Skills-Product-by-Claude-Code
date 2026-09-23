# Uji Banding Pesaing — riset-calon-pelanggan

## Pencarian yang dilakukan
Kata kunci: `SKILL.md lead generation ideal customer profile prospecting skill`,
`SKILL.md prospecting B2B lead scoring`, di GitHub, ClawHub, skills.sh,
anthropics/skills, dan repo Indonesia (manairalabs/bicara-skills,
alvinindra/bahasa-skills — tidak ditemukan skill prospecting/ICP di keduanya).

Kandidat yang ditemukan (dibaca lewat raw.githubusercontent.com/WebFetch,
**tidak dijalankan, tidak disalin**):
- `ComposioHQ/awesome-claude-skills` (lead-research-assistant) — **sengaja
  dikecualikan** sesuai instruksi penguji.
- `apify/agent-skills` (apify-lead-generation) — berbasis scraping otomatis
  (Google Maps, Instagram, TikTok, LinkedIn) lewat Apify actors → melanggar
  aturan sumber sah skill kita (tidak dinilai lebih lanjut sebagai pembanding
  langsung karena filosofinya bertentangan: scraping berbayar vs sumber
  publik manual).
- `coreyhaines31/marketingskills` (skills/prospecting) — MIT, **51.300 bintang**,
  473 commit, dibuat Corey Haines (marketer dikenal luas) — repo paling
  terbukti dari semua kandidat. **Dipilih sebagai pembanding utama.**

Sumber: https://github.com/coreyhaines31/marketingskills ,
https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/prospecting/SKILL.md
(dibaca untuk dinilai, isi tidak disalin ke skill kita).

## Simulasi Skenario 1 (Cleaning Service Surabaya) mengikuti instruksi pesaing

Skill pesaing meminta memilih 1 dari 4 "motion": SaaS / B2B umum / Local SMB /
Demand-signal. Untuk kasus ini paling cocok "Local SMB". Mengikuti Phase 1-5:

```
[Phase 1: ICP] Kantor kecil-menengah Surabaya, belum ada vendor cleaning tetap.

[Phase 2: Build candidate list, 2-3x target, "2-3 cross-verified sources per
prospect"] → Sumber yang diminta pesaing: Google Maps, Yelp, direktori lokal,
Facebook — TAPI juga menyebut tools berbayar/API (Apollo, Clay, BuiltWith,
ZoomInfo, Truelist untuk verifikasi email) yang TIDAK tersedia untuk UMKM tanpa
langganan/API key. Tanpa akses tools tersebut, langkah ini tidak bisa
dijalankan penuh — instruksi pesaing berasumsi penggunanya (agency/SaaS B2B)
punya akses tools tersebut.

[Phase 3-4: Qualify & score] Meminta level keyakinan (High/Medium/Low)
berdasarkan jumlah sumber independen yang memverifikasi tiap kontak — konsep
bagus tapi berat untuk UMKM yang hanya punya 1 sumber (Google Maps) per
prospek lokal kecil.

[Phase 5: Output] Tabel markdown/CSV dengan kolom score, company, industry,
size, signal, contact, email status (Truelist), source, confidence — kolom
"email status (verified via Truelist)" tidak relevan untuk cleaning service
lokal yang biasanya kontak lewat WA, bukan email dingin B2B SaaS.
```

Hasil: skill pesaing **tidak bisa dijalankan sepenuhnya tanpa tools
berbayar/API** (Apollo, Clay, BuiltWith, Truelist) untuk kasus UMKM lokal
sederhana ini — jauh dari prinsip "instan, tanpa setup" yang jadi target
produk kita.

## Tabel penilaian

| Aspek | riset-calon-pelanggan (kita) | coreyhaines31/marketingskills (prospecting) |
|---|---|---|
| Kualitas kerangka kerja | Baik, 5 langkah jelas | Sangat matang, 5 fase + 4 motion + confidence level — lebih canggih secara metodologi |
| Kesesuaian konteks Indonesia/UMKM | Bahasa Indonesia, WA sebagai default, tanpa tools berbayar | Bahasa Inggris, berasumsi tools SaaS B2B Barat (Apollo/Clay/ZoomInfo/Truelist), tidak menyebut WA sama sekali |
| **Instan/tanpa setup** | Ya — hanya perlu Python standar utk skor CSV, sisanya manual | **Tidak** — banyak langkah bergantung API berbayar (Apollo, Clay, BuiltWith, Truelist) yang tidak dimiliki UMKM |
| Kepatuhan hukum lokal | Ada bagian khusus UU PDP + dasar hukum | Ada bagian compliance (GDPR/CAN-SPAM/CASL) — relevan untuk pasar Barat, **tidak menyebut UU PDP Indonesia** |
| Larangan scraping/beli data | Eksplisit, diuji (skenario 5) | Eksplisit juga ("no bulk scraping", "no reselling data") — sama-sama kuat |
| Siap pakai untuk UMKM kecil | Ya | Lebih cocok untuk tim sales B2B/SaaS dengan budget tools, kurang pas untuk UMKM kecil |
| Skor kualifikasi terverifikasi | Ada, via script + fallback manual, kategori Panas/Hangat/Dingin | Ada kategori Hot/Warm/Cold, tapi skor bergantung "confidence level" dari banyak sumber berbayar — tidak ada rumus angka eksplisit/script |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- Konsep **confidence level** (High = 2+ sumber independen, Medium = 1 sumber +
  bukti pencarian konsisten, Low = data tidak lengkap) adalah ide bagus yang
  bisa diadaptasi ringan: skill kita bisa menambah catatan "tandai keyakinan
  data kontak (pasti/perlu dicek ulang)" di Langkah 3 SKILL.md, tanpa perlu
  tools berbayar — cukup dari jumlah sumber publik yang cocok.
- Pembagian "motion" (SaaS/B2B/Local SMB/Demand-signal) membantu mempersempit
  arahan sumber; skill kita sudah cukup fokus ke UMKM/B2B Indonesia tapi bisa
  eksplisit membedakan gaya arahan untuk B2B korporat vs UMKM lokal di
  `references/sumber-pencarian.md`.
- Checklist "quality checks" pesaing (no duplicate, source URL + tanggal
  dicatat per kontak) relevan diadaptasi: skill kita bisa menambah saran
  mencatat tanggal & sumber tiap kontak di kolom tabel Daftar Calon Pelanggan
  untuk transparansi (mendukung poin "identitas pengirim jelas" UU PDP kita).

## Kesimpulan
Metodologi pesaing lebih matang secara struktur (4 motion, confidence level),
tapi **tidak cocok untuk target pembeli kita** (UMKM/profesional Indonesia awam
tanpa tools berbayar) karena bergantung pada API/tools SaaS Barat berbayar dan
tidak menyebut UU PDP maupun WhatsApp sama sekali. Untuk kasus penggunaan nyata
target pasar kita, skill kita **menang** dari sisi "instan tanpa setup" dan
kepatuhan hukum lokal; pesaing unggul dari sisi kedalaman metodologi untuk
tim sales B2B/SaaS berbudget besar — beberapa idenya (confidence level, catat
sumber+tanggal) sudah dicatat sebagai masukan perbaikan ringan.
