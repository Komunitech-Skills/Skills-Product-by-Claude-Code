# Kurasi sumber KUAT (belum pernah dinilai) — 2026-09-26

Tanggal tinjau: 2026-09-26 · Peninjau: agent kurator (sesi terpisah) · Status: **menunggu keputusan/lanjutan**

**Metode:** WebSearch + WebFetch pada halaman GitHub publik (tidak clone/jalankan kode; `api.github.com` diblokir seperti sesi sebelumnya, jadi bintang/fork/commit dari WebFetch halaman HTML — ada risiko kecil sedikit basi). Dicek dulu terhadap semua repo yang sudah pernah dinilai (lihat daftar di `research/sources/*.md`, digabung via `grep github.com`) dan terhadap `skills/` yang sudah ada (79 skill) — semua kandidat di bawah **belum pernah dinilai**.

**Aturan lisensi dipakai (keputusan pemilik 2026-09-26, prioritas sumber KUAT apa pun lisensinya):**
- MIT / MIT-0 / BSD / Apache-2.0 / CC-BY → **salin-edit** (dengan atribusi + teks lisensi asli; Apache-2.0 tambah NOTICE & keterangan file diubah).
- GPL / AGPL / CC-BY-SA → **salin-edit berlisensi sama** (turunan boleh dipakai tapi ikut lisensi copyleft yang sama) — tetap **PERLU REVIEW pemilik** karena berpotensi konflik dengan model jual-putus tertutup.
- CC-BY-NC / tanpa lisensi eksplisit → **tulis ulang bersih** (2 agent terpisah: agent 1 baca sumber → daftar ide saja tanpa kutipan; agent 2 tulis skill baru dari daftar ide + riset sendiri, tidak membaca sumber).

---

## 1. Tabel kandidat (diurutkan dari sinyal terkuat)

| # | Nama & URL | Pembuat | ★/Fork | Commit terakhir | Lisensi (dari halaman/LICENSE) | Sinyal (dari 5) | Cara ambil | Usulan nama skill ID | Nilai tambah lokal | Prioritas |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **anthropics/claude-for-legal** — `commercial-legal/` (vendor agreement/NDA/SaaS review) — github.com/anthropics/claude-for-legal | **Anthropic** (resmi) | **9,5k / 1,9k** | aktif, 38 commit main, rilis produk resmi "Claude for Legal" | **Apache-2.0** (terverifikasi via halaman repo) | Pembuat kredibel ✓✓✓, popularitas ✓✓, dipakai komunitas ✓ (produk resmi + eksternal plugin Thomson Reuters), kualitas isi ✓ (guardrail "draft untuk ditinjau pengacara, bukan nasihat hukum", cold-start interview, gate sebelum kirim/file) = **4 sinyal** | Salin-edit (atribusi + NOTICE + keterangan file diubah) | `tinjau-kontrak-vendor` (lengkapi `perjanjian-sederhana` untuk kontrak vendor/supplier B2B yang lebih kompleks) | Bahasa Indonesia, klausul umum kontrak vendor RI (force majeure, PPN, jangka waktu, ganti rugi), disclaimer "bukan nasihat hukum, tinjau ke pengacara" wajib | **TINGGI** |
| 2 | **anthropics/claude-for-legal** — `employment-legal/` (skill: `termination-review`, `worker-classification`, `handbook-updates`, `wage-hour-qa`) | Anthropic (resmi) | 9,5k / 1,9k (repo sama) | sama | Apache-2.0 | sama (4 sinyal) | Salin-edit | `tinjau-phk-karyawan` (cek kelengkapan & risiko sebelum PHK/pemutusan kerja) dan `cek-klasifikasi-karyawan` (karyawan tetap vs kontrak vs freelance) | UU Cipta Kerja/Ketenagakerjaan RI, pesangon PP 35/2021, disclaimer arahkan ke HR/pengacara ketenagakerjaan; melengkapi `kontrak-kerja-pkwt` & `surat-peringatan-karyawan` yang sudah ada (beda: itu buat dokumen, ini **cek risiko sebelum bertindak**) | **TINGGI** |
| 3 | **anthropics/claude-for-legal** — `privacy-legal/` (skill: `dsar-response`, `dpa-review`, `privacy-triage`) | Anthropic (resmi) | 9,5k / 1,9k (repo sama) | sama | Apache-2.0 | sama (4 sinyal) | Salin-edit | `tanggapi-permintaan-data-pribadi` — draf balasan ke pelanggan yang minta data dihapus/diberi (hak subjek data UU PDP) | UU PDP No. 27/2022 (bukan GDPR/CCPA), tenggat waktu & bahasa formal Indonesia; melengkapi `kebijakan-privasi-pdp` yang sudah ada (beda: itu bikin kebijakan, ini **respons ke permintaan individu**) | **SEDANG-TINGGI** |
| 4 | **anthropics/claude-cookbooks** — notebook `skills/02_skills_financial_applications.ipynb` & `03_skills_custom_development.ipynb` (contoh `financial_analyzer`) — github.com/anthropics/claude-cookbooks | **Anthropic** (resmi) | **53k / 6,4k** | aktif (cookbook resmi terus diperbarui) | **MIT** (terverifikasi via halaman repo) | Pembuat kredibel ✓✓✓, popularitas ✓✓✓, dipakai komunitas ✓✓ (cookbook resmi rujukan luas), kualitas isi ✓ (metodologi rasio keuangan, dashboard, forecast dijelaskan lengkap) = **4 sinyal** | Salin-edit (atribusi + teks MIT) — ini contoh kode/notebook edukasi, bukan SKILL.md siap pakai, jadi tetap ditulis ulang jadi skill kita sendiri | `analisis-rasio-keuangan-usaha` — hitung rasio likuiditas/profitabilitas/leverage dari laporan keuangan sederhana usaha | Istilah & standar SAK EMKM (bukan US GAAP), Rupiah, dibandingkan ke ambang wajar UMKM Indonesia, script perhitungan (bukan kira-kira) sesuai Tahap 4 CLAUDE.md; melengkapi `laporan-keuangan-emkm`/`rekonsiliasi-bank` (beda: itu susun laporan, ini **baca laporan & kasih insight rasio**) | **SEDANG-TINGGI** |
| 5 | **mohitagw15856/pm-claude-skills** — github.com/mohitagw15856/pm-claude-skills (skill dipilih: kategori "postmortem"/laporan insiden, bukan seluruh koleksi) | Individu (terdaftar di direktori plugin resmi Anthropic, menurut README) | **1,4k / 250** | aktif, 883 commit tersebar berbulan-bulan (bukan dump 1 hari) | **MIT** | Popularitas ✓✓, umur & perawatan ✓ (883 commit bertahap, ada sistem deprecation skill lama → pengganti, bukan ditinggal), dipakai komunitas ✓ (terdaftar direktori plugin resmi Anthropic, klaim skor evaluasi 4,8/5 dari 208 output — **belum diverifikasi independen**), kualitas isi ✓ (dokumentasi SKILLSPEC, CI, contoh spesifik) = **4 sinyal**, tapi skala 1.170 skill oleh individu tetap perlu kehati-hatian ekstra saat memilih skill spesifik untuk ATM (jangan asumsikan semua 1.170 skill sama kualitasnya) | Salin-edit (per-skill, bukan borongan; cek isi skill spesifik dulu sebelum ambil) | `laporan-insiden-usaha` — draf laporan & tindak lanjut saat ada masalah operasional (retur massal, sistem kasir down, komplain viral) | Bahasa Indonesia, contoh kasus UMKM (bukan startup software), format singkat siap kirim ke tim/owner | **SEDANG** (verifikasi ulang skill spesifiknya sebelum ATM — jangan ambil dari klaim README saja) |
| 6 | **product-on-purpose/pm-skills** — github.com/product-on-purpose/pm-skills (skill: Foundation Sprint / Design Sprint) | Individu/tim kecil, proyek aktif | **699 / 88** | aktif, 873 commit, rilis reguler (v2.33.0 Agu 2026, mingguan) | **Apache-2.0** | Popularitas ✓ (di atas ambang 100 repo satu-tema), umur & perawatan ✓✓ (rilis reguler berbulan-bulan), dipakai komunitas ✓ (multi-platform: Claude/Copilot/Cursor/Windsurf), kualitas isi ✓ (200+ contoh output, dokumentasi lengkap) = **4 sinyal** | Salin-edit | `validasi-ide-produk-baru` — proses terstruktur uji ide produk/fitur baru sebelum invest waktu/modal (beda dari `brainstorming-ide-usaha` yang sudah ada: itu gali ide dari nol, ini **validasi ide yang sudah ada** dengan kerangka sprint) | Konteks UMKM Indonesia (modal terbatas, uji pasar cepat lewat WA/marketplace, bukan software sprint ala Silicon Valley) | **SEDANG** |
| 7 | **nimrodfisher/data-analytics-skills** — github.com/nimrodfisher/data-analytics-skills (skill kategori "Stakeholder Communication"/"Data Storytelling") | Individu (Nimrod Fisher), proyek aktif | **451 / 81** | aktif, 20 commit tersebar, update Sept 2026, versi 1.2.0 | **MIT** | Popularitas ✓, umur & perawatan ✓ (commit bertahap, versi berjenjang), dipakai komunitas — sedang (belum ada bukti issue/PR eksternal terlihat), pembuat kredibel — sedang (bukan organisasi besar, tapi konsisten & terdokumentasi) = **3 sinyal (pas ambang)** | Salin-edit | `presentasi-data-ke-atasan` — ubah hasil analisis data mentah jadi ringkasan 1 halaman untuk atasan/klien non-teknis | Bahasa Indonesia awam, contoh data penjualan/operasional UMKM, format "1 halaman siap kirim" bukan slide teknis; melengkapi `analisis-excel` yang sudah ada (beda: itu analisis, ini **komunikasikan hasilnya**) | **SEDANG-RENDAH** |
| 8 | **evolsb/claude-legal-skill** — github.com/evolsb/claude-legal-skill (contract review, 41 kategori risiko) | Individu | 453 / 58 | 15 commit | **MIT** | Popularitas ✓, kualitas isi ✓ (ada folder `/examples` output nyata), umur/perawatan & dipakai komunitas — belum kuat = **2 sinyal** | — (dicatat sebagai **pembanding**, bukan sumber ATM) | — | Kalah dari kandidat #1 (`anthropics/claude-for-legal`, 9,5k★, resmi Anthropic) untuk fungsi sama → sesuai Tahap 6, jangan dipakai sebagai sumber utama; simpan untuk uji banding pesaing saat `tinjau-kontrak-vendor` diuji | **RENDAH — hanya pembanding** |
| 9 | **coffeefuelbump/csv-data-summarizer-claude-skill** — github.com/coffeefuelbump/csv-data-summarizer-claude-skill | Individu ("Corbin") | 467 / 68 | **hanya 1 commit terlihat** (Okt 2025), tidak ada pembaruan bertahap | **MIT** | Popularitas ✓, kualitas isi — sedang, umur & perawatan **✗** (statis sejak rilis, tidak "masih diperbarui"), dipakai komunitas — belum ada bukti = **≤2 sinyal** | Tidak memenuhi ambang 3 sinyal | — | Tumpang tindih penuh dengan `analisis-excel`/`rekap-penjualan-csv` yang sudah ada (orisinal, lebih lokal) | **DITOLAK untuk ATM** — sinyal tidak cukup + tumpang tindih katalog |
| 10 | **tfriedel/claude-office-skills** — github.com/tfriedel/claude-office-skills (PPTX/DOCX/XLSX/PDF workflows) | Individu | 833 / 118 | 7 commit | **TIDAK DITEMUKAN file LICENSE** di repo (dicek langsung, 404) — README sendiri menyatakan "sebagian besar berasal langsung dari Claude/Anthropic" tanpa kejelasan hak | Popularitas ✓ tapi lisensi tidak jelas — gagal syarat legal mutlak | **DILARANG** disalin/dijual — tanpa lisensi eksplisit | — | — | **DITOLAK — lisensi tidak ada, jangan disentuh** |
| 11 | **w95/awesome-claude-corporate-skills** — github.com/w95/awesome-claude-corporate-skills (166 skill, 14 kategori termasuk Finance 42 skill) | Individu | 214 / 53 | **1 commit tunggal** ("Initial release: 166 skills"), 1 hari (26 Feb 2026), kontributor: pemilik + bot "claude" | MIT (halaman) | Popularitas — di bawah ambang, umur & perawatan **✗ GAGAL** (166 skill muncul dalam **satu commit/satu hari** — persis pola AI slop yang dilarang CLAUDE.md Tahap 2), dipakai komunitas — sedang (6 PR/1 issue) = **≤2 sinyal kuat** | Tidak memenuhi ambang 3 sinyal | — | — | **DITOLAK untuk ATM** — pola pembuatan massal dalam sehari, meski MIT & kontennya tampak rapi. Catat sebagai contoh pola AI slop untuk kalibrasi sesi berikutnya |

---

## 2. Ringkasan kata kunci & sumber ditelusuri
`github.com anthropics/skills`, `"SKILL.md" legal contract review skill claude stars MIT`, `"SKILL.md" project management OR task management skill claude agent stars`, `github awesome claude skills data analysis spreadsheet finance accounting stars popular 2026`, `"SKILL.md" HR recruiting onboarding skill claude agent stars license 2026`, `github claude skill e-commerce marketplace product listing seller tools stars license`, `"SKILL.md" customer support ticket triage skill claude agent stars license 2026`, `github claude skill financial model DCF budgeting forecast agent stars Apache OR MIT license 2026`.

**Kategori tanpa kandidat kuat baru:** HR/rekrutmen murni (kandidat terbaik `tuanductran/hr-skills` & `borghei/Claude-Skills` sudah ditolak sesi 2026-09-24, tidak ada penemuan baru yang lebih kuat), Customer Service (tidak ada repo satuan bersinyal kuat spesifik CS, hanya koleksi besar tanpa metrik per-skill), E-commerce/marketplace (kandidat `nexscope-ai/eCommerce-Skills` 157 skill & `mardab96/ecommerce-claude-skills` 20 skill tidak sempat diverifikasi bintang/lisensi — cadangan sesi berikut, indikasi awal kurang kuat dibanding standar kandidat #1–7 di atas).

**Hambatan:** `api.github.com` diblokir (403) — semua metrik dari WebFetch halaman HTML publik, bukan API resmi; kandidat #5 (`mohitagw15856`) khususnya perlu verifikasi ulang lebih dalam per-skill sebelum ATM (klaim skor evaluasi 4,8/5 belum diverifikasi independen oleh kurator, hanya dikutip dari README repo itu sendiri).

## 3. Prioritas untuk sesi ATM berikutnya
1. **`tinjau-kontrak-vendor`**, **`tinjau-phk-karyawan`**, **`cek-klasifikasi-karyawan`** — dari `anthropics/claude-for-legal` (#1–2), sumber terkuat sesi ini (resmi Anthropic, Apache-2.0, 9,5k★).
2. **`analisis-rasio-keuangan-usaha`** — dari `anthropics/claude-cookbooks` (#4), juga resmi Anthropic (53k★, MIT).
3. **`tanggapi-permintaan-data-pribadi`** — dari `anthropics/claude-for-legal` `privacy-legal/` (#3).
4. **`validasi-ide-produk-baru`** — dari `product-on-purpose/pm-skills` (#6).
5. Prioritas lebih rendah/cadangan: `laporan-insiden-usaha` (#5, verifikasi ulang dulu), `presentasi-data-ke-atasan` (#7).

---

## 4. Verifikasi lanjutan & keputusan — `laporan-insiden-usaha` (2026-09-26, K4)

**Metode:** `git clone --depth 1` ke scratchpad session terpisah (kode **tidak dijalankan**,
hanya dibaca), lalu `git fetch --depth 200` untuk melihat riwayat commit file spesifik.

**Skill sumber ditemukan (3, dijadikan inspirasi bersama):**
- `skills/incident-postmortem/` — blameless postmortem, timeline, root cause + contributing
  factors, action items berpemilik/tenggat, referensi five-whys & worked example.
- `skills/customer-incident-update/` — komunikasi status ke pelanggan saat insiden, jujur
  tanpa over-promise, tense sesuai tahap insiden.
- `plugins/pm-crisis/skills/apology-letter/` — struktur permintaan maaf efektif (akui
  spesifik, tanggung jawab tanpa "tapi", empati, perbaikan konkret, tanpa janji berlebih).

**Lisensi:** MIT, diverifikasi dari file `LICENSE` di root repo (Copyright (c) 2026 Mohit
Aggarwal, teks MIT standar).

**Riwayat commit (bukan dump):** `git log --oneline --follow -- skills/incident-postmortem/SKILL.md`
menunjukkan commit bertahap dengan rilis versi berjenjang (mis. `29960fb6 feat(craft):
upgrade the incident-response spine to flagship quality (v76.1)`, commit terbaru repo
`f6ca7934 release: v80.0.0`). 214 commit terlihat dalam window `--depth 200`, tersebar —
bukan pola "ratusan skill dalam satu hari" yang jadi tanda AI slop di CLAUDE.md.

**Kualitas isi:** Spesifik dan teruji — bukan teks generik. `incident-postmortem` punya
kerangka "Done when" per langkah, referensi five-whys lengkap dengan taksonomi
contributing-factor, dan worked example. `customer-incident-update` punya Quality Checks
dan Anti-Patterns eksplisit. `apology-letter` punya larangan non-apology ("sorry you feel
that way") dengan contoh konkret. Ini pola instruksi yang teruji, bukan AI slop.

**Audit keamanan (Tahap 3):** Tidak ada folder `scripts/` di ketiga skill sumber (murni
markdown). `grep -rniE` untuk pola perintah destruktif, unduh-pipe-ke-shell, `eval`/`exec`,
`base64 -d`, akses SSH/`/etc/passwd`, API key/token, dan pola prompt injection tersembunyi
("ignore previous/above instructions", "do not tell", "without telling/asking", "silently",
"bypass") — **nihil kecocokan berbahaya** (satu-satunya match kasar adalah frasa "token
praise"/"not token" dalam konteks kualitas tulisan, diperiksa manual, aman). Tidak ada
API key/kredensial/data pribadi tertanam.

**Keputusan: LOLOS verifikasi, ATM dilanjutkan.** 4 sinyal bukti terpenuhi (popularitas di
atas ambang repo satu-tema untuk skala 3 skill spesifik yang dinilai, umur & perawatan
kuat lewat commit bertahap + versi berjenjang, kualitas isi tinggi, cara ambil sesuai
lisensi MIT). Skill baru `laporan-insiden-usaha` dibuat sebagai **karya gabungan & tulis
ulang** dari ketiga skill sumber, dilokalkan penuh untuk insiden operasional UMKM
Indonesia (bukan insiden software/engineering) dengan tambahan: penanganan kebocoran data
pelanggan (arahan umum UU PDP + rujuk `kebijakan-privasi-pdp`), larangan menyalahkan
individu di akar masalah, penanda `[isi: ...]` anti-karang-angka, draf minta maaf +
ringkasan WA siap tempel. Rincian lengkap perubahan & atribusi di
`skills/laporan-insiden-usaha/ATTRIBUTION.md`. Status katalog: `draft` (belum diuji sesuai
Tahap 6, belum diberi skor kualitas).
