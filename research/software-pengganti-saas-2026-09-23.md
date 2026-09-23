# Software Pengganti SaaS yang Jalan Lokal & Bisa Dioperasikan AI Agent — Riset 2026-09-23

Untuk: Komunitech. Tujuannya dua:
- **Jalur A:** mengkurasi software open-source terbukti yang bisa menggantikan SaaS berbayar.
- **Jalur B:** menyusun daftar alat kecil yang lebih baik dibuat sendiri.

Syarat semua kandidat: jalan **di komputer pembeli** (data tetap di laptop, tanpa biaya bulanan) dan bisa dioperasikan AI agent. Semua member VIP memakai **OpenClaw**. OpenClaw mengoperasikan software lewat perintah shell/CLI yang dipanggil skill, jadwal (cron), file/SQLite, HTTP API lokal, dan MCP lewat `mcporter`.

Prioritas mengikuti kebutuhan member VIP (`research/kebutuhan-member-vip-2026-09-23.md`):
1. laporan otomatis (±20 member)
2. follow-up/CRM (±6)
3. stok/inventori + cetak resi Shopee (3)
4. absensi & gaji (2)
5. privasi data, yang dikhawatirkan 17 dari 48 member.

**Metode:**
- Bintang, umur repo, dan aktivitas diambil dari GitHub API (data 2026-09-23).
- **Lisensi dibaca langsung dari file LICENSE/COPYING** di repo (raw.githubusercontent.com).
- Harga SaaS diambil dari hasil pencarian (kisaran publik, bisa berubah).
- Tidak ada kode pihak ketiga yang dijalankan. Yang diunduh hanya teks lisensi.

Singkatan: ★ = bintang GitHub; "push" = commit terakhir; SUL = Sustainable Use License; ELv2 = Elastic License 2.0; BSL = Business Source License.

---

## 1. Ringkasan

1. **Hanya kategori "back-office" yang benar-benar cocok untuk lokal:** pembukuan, invoice, stok, kasir satu outlet, PDF/dokumen, catatan/SOP, tugas, dan analitik. Kategori yang melayani **pelanggan dari luar** (booking online, formulir publik, toko online, helpdesk/inbox WA, e-sign untuk pihak lain) butuh server yang bisa diakses internet. Menjalankannya di laptop berarti harus membuka tunnel, dan itu rumit serta berisiko bagi orang awam. Untuk kategori ini, sarannya tetap SaaS gratis/resmi atau VPS kecil, dan tidak dijadikan produk "lokal".
2. **Kandidat jalur A terbaik untuk member VIP:**
   - **Frappe Books**: akuntansi + invoice + stok + POS di desktop, file SQLite, ada terjemahan Indonesia.
   - **Dolibarr** lewat DoliWamp: ERP/CRM/stok/kasir/HR ringan, installer Windows, bahasa Indonesia, **REST API resmi**.
   - **Odoo Community 19**: satu-satunya yang punya modul resmi **e-Faktur Coretax XML dengan DPP 11/12**, cocok untuk usaha mapan.
   - **hledger**: pembukuan teks + CLI + JSON, paling mudah dioperasikan agent.
   - **Stirling-PDF Desktop**: pengganti Acrobat, API, bisa merapikan resi.
   - **Grist Desktop**: pengganti Airtable/Sheets lanjutan, file SQLite.
   - **Vikunja**: tugas/proyek, satu binary + SQLite + API.
   - **SiYuan**: wiki/SOP lokal dengan API + MCP.
   - **Actual Budget**: kas/anggaran, MIT.
   - **Datasette**: mesin laporan SQLite, Apache-2.0.
3. **Payroll Indonesia (PPh 21 TER, BPJS), absensi sederhana, kasir UMKM ber-QRIS, CRM WhatsApp, dan buku stok untuk seller marketplace tidak punya padanan open-source yang cocok.** Pilihan yang ada terlalu berat (Django/Laravel + database server), tidak paham aturan Indonesia, atau butuh server publik. Semua ini masuk **jalur B**: alat kecil Python standar + SQLite + skill OpenClaw. Repo ini sudah punya bahan hitungnya: `pph21-ter-tabel.json`, `hitung-hpp`, `rekap-penjualan-csv`, `tagih-piutang`, `laporan-keuangan-emkm`.
4. **Lisensi.** Kebanyakan software besar berlisensi **GPL/AGPL**. Komunitech **boleh** mendistribusikan installer asli plus skill/panduan berbayar, dengan kewajiban menyertakan lisensi dan menunjuk kode sumber. Semua modifikasi pada software itu sendiri wajib dirilis dengan lisensi yang sama. Skill yang mengoperasikan software lewat API/CLI adalah karya terpisah dan boleh tetap tertutup. **Hindari membundel:**
   - Akaunting (BSL: maks. 2 user / 1 perusahaan / 1.000 invoice)
   - Invoice Ninja (ELv2)
   - n8n & NocoDB (SUL)
   - Planka (Fair Use License)
5. **Perkiraan penghematan** per usaha kecil–menengah dibanding kombinasi SaaS (Jurnal/Accurate + Moka/Majoo + Talenta + Notion/Trello): **±Rp0,6–3 jt per bulan**. Untuk usaha 16–50 karyawan (10 member VIP) penghematan terbesar ada di payroll: Rp25–50 rb × karyawan per bulan.
6. **Nilai tambah Komunitech:**
   - installer/penyiapan sekali klik;
   - skill OpenClaw untuk mengoperasikan tiap software (input transaksi, laporan terjadwal ke WA/Telegram);
   - template Indonesia: bagan akun SAK EMKM, pajak PPN 12% DPP 11/12, format faktur/struk, bahasa Indonesia;
   - panduan backup;
   - jasa setup.

---

## 2. Tabel per kategori (jalur A)

Kolom:
- **Software**
- **Bukti**: ★, tahun dibuat, commit terakhir
- **Lisensi** (dari file LICENSE)
- **Jalan lokal untuk awam**: installer? Docker? berat?
- **Cara agent mengoperasikan**
- **Kecocokan Indonesia**
- **SaaS yang digantikan** + harga/bln
- **Catatan/nilai tambah Komunitech**

Kesulitan instal untuk awam: **M** = mudah (installer biasa), **S** = sedang, **B** = berat (Docker/server).

### 2.1 Akuntansi / pembukuan

| Software | Bukti | Lisensi | Lokal awam | Agent | Indonesia | Menggantikan | Catatan |
|---|---|---|---|---|---|---|---|
| **Frappe Books** | 4.981★, 2018, push 20 Sep 2026. **Rilis terakhir v0.36.0 (Nov 2024)** | AGPL-3.0 | **M**: installer Win/Mac/Linux, offline, **SQLite** | Baca SQLite untuk laporan; input via **Import Wizard CSV** (template resmi) | Terjemahan `translations/id.csv` (±1.240 baris); IDR; pajak bisa diatur (PPN 11% efektif = 12% × DPP 11/12); **tanpa e-Faktur** | Jurnal Rp399–499 rb, Kledo Rp140–350 rb, Paper.id | Rilis lama: pantau risiko proyek melambat. Komunitech: COA SAK EMKM, template faktur, skill "catat penjualan → CSV import" |
| **Dolibarr** (DoliWamp) | 7.650★, 2011, push 23 Sep 2026; v22–24 rilis 2025–2026 | GPL-3.0 | **M–S**: DoliWamp = Apache+MySQL+PHP sekali instal (Windows). Mac: MAMP/Docker | **REST API resmi** (`/api/index.php`, header `DOLAPIKEY`, Swagger explorer) | Bahasa `id_ID` ada; IDR; modul invoice, stok, kasir TakePOS, CRM, proyek, cuti/HR ringan | Jurnal/Accurate + Moka + Qontak CRM ringan | **Kandidat "ERP lokal" terbaik untuk awam.** Komunitech: skill API (buat invoice, cek stok, laporan harian) |
| **Odoo Community 19** | 54.538★, 2014, aktif | LGPL-3.0 | **S–B**: installer Windows (bundel PostgreSQL), berat. Mac perlu Docker | XML-RPC/JSON-RPC API resmi | **`l10n_id` + `l10n_id_efaktur_coretax` di Community**: XML e-Faktur Coretax, DPP × 11/12 | Accurate Rp333 rb+, Jurnal, sebagian Klikpajak | Akuntansi penuh (laporan lengkap) ada di Enterprise; di Community pakai modul OCA. Untuk usaha mapan + jasa setup. Merek "Odoo" tidak boleh dipakai untuk nama produk |
| **hledger** (+ hledger-web) | ±4,7 rb★, stabil 1.52.4 (10 Sep 2026) | GPL-3.0 | **M**: binary Win/Mac (zip/tar), tanpa database | **CLI + output JSON/CSV/SQL + HTTP API**; jurnal = file teks yang bisa ditulis agent | Mata uang bebas (Rp); akun berbahasa Indonesia bebas | Pembukuan SaaS mikro/profesional | **Paling "agent-native".** Awam tidak perlu melihat file; agent mencatat dan membuat laporan. Komunitech: template jurnal Indonesia + skill |
| **GnuCash** | 4.354★, 2013 di GitHub (proyek sejak 1998), 5.16 (Jun 2026) | GPL-2/3 | **M**: installer Win/Mac; opsi penyimpanan **SQLite** | Baca SQLite / import CSV (tanpa API resmi) | Terjemahan `po/id.po` | Sama | UI kaku untuk awam. Alternatif dari Frappe Books |
| Beancount + **Fava** | Beancount 6.028★ (GPL-2.0); Fava 2.579★ (MIT) | GPL-2 / MIT | S (butuh Python/pip) | CLI + teks | – | – | Mirip hledger. Pilih salah satu; hledger lebih mudah dipasang |
| Akaunting | 10.133★ | **BSL 1.1**: maks. 2 user / 1 perusahaan / 1.000 invoice; tidak boleh rebrand/jasa akuntansi | B (PHP server) | REST API | – | – | **Jangan dibundel/dijual** |
| BigCapital | 3.906★ | AGPL-3.0 | B (Docker) | API | – | – | Berat untuk lokal |
| ERPNext | 39.496★ | GPL-3.0 | B (bench/Docker) | REST API | Lokalisasi ID lemah | – | Terlalu berat untuk laptop awam |

### 2.2 Invoice & penagihan

| Software | Bukti | Lisensi | Lokal | Agent | Menggantikan | Catatan |
|---|---|---|---|---|---|---|
| Frappe Books / Dolibarr / Odoo | lihat 2.1 | – | – | – | Paper.id, Jurnal | Invoice sudah ada di software akuntansi di atas |
| InvoiceShelf (fork Crater) | 1.834★, 2024 | AGPL-3.0 | B (PHP/Docker) | REST API | Paper.id | Butuh server |
| SolidInvoice | 972★ | MIT | B (PHP) | API | – | Kecil |
| Invoice Ninja | 10.105★ | **ELv2** (source-available) | B | API | – | **PERLU REVIEW**: tidak boleh jadi layanan terkelola / mengakali kunci lisensi |

→ Untuk UMKM: **jalur B `buku-piutang`** (lihat §5) lebih cocok daripada server invoice.

### 2.3 Kasir / POS

| Software | Bukti | Lisensi | Lokal | Agent | Menggantikan | Catatan |
|---|---|---|---|---|---|---|
| **Frappe Books (POS)** | lihat 2.1 | AGPL-3.0 | M | SQLite/CSV | Moka Rp299–799 rb/outlet, Majoo Rp249–999 rb, Olsera ±Rp107–224 rb (tahunan/12) | POS dasar, satu komputer. Belum ada QRIS/struk thermal khas Indonesia |
| **Dolibarr TakePOS** | lihat 2.1 | GPL-3.0 | M–S | REST API | Sama | Terhubung stok & invoice |
| Open Source POS (OSPOS) | 4.402★, 2013 | MIT | B (PHP+MySQL, Docker) | API terbatas | Sama | Web; butuh server lokal |
| NexoPOS | 1.263★ | GPL-3.0 | B (Laravel) | – | Sama | Berat |

→ Kasir UMKM ringan (satu laptop, struk 58/80 mm, rekap PPN/PPh final) → **jalur B `kasir-lokal`**.

### 2.4 Stok / inventori

| Software | Bukti | Lisensi | Lokal | Agent | Menggantikan | Catatan |
|---|---|---|---|---|---|---|
| Dolibarr (modul Stok) | – | GPL-3.0 | M–S | REST API | Jubelio Rp799 rb–2,49 jt/bln (min. 6 bln), fitur stok di Majoo/Moka | Multi-gudang, mutasi |
| Frappe Books (inventori, batch) | – | AGPL-3.0 | M | SQLite/CSV | – | Sederhana |
| InvenTree | 7.619★, 2017 | MIT | **B**: Docker disarankan; Windows via WSL | REST API + `inventree-python` | – | Fokus komponen/manufaktur, bukan toko online |
| Grist Desktop (sebagai buku stok) | lihat 2.12 | Apache-2.0 | M | SQLite + REST API | Airtable | Fleksibel, tapi tanpa logika stok bawaan |

→ Seller marketplace (stok ter-update dari file pesanan Shopee/TikTok, stock opname, *picking list*) → **jalur B `buku-stok`**.

### 2.5 CRM & pipeline sales

| Software | Bukti | Lisensi | Lokal | Agent | Menggantikan | Catatan |
|---|---|---|---|---|---|---|
| Dolibarr (CRM/prospek/penawaran) | – | GPL-3.0 | M–S | REST API | Qontak CRM (paket mulai ±Rp400–750 rb/bln) | Cukup untuk UMKM |
| Krayin CRM | 23.936★, 2021 | **MIT** | B (Laravel+MySQL) | REST API | HubSpot Starter, Qontak | Lisensi paling bebas |
| Twenty | 57.358★, 2022 | AGPL-3.0 + file Enterprise komersial | B (Docker, Postgres, Redis) | GraphQL/REST; MCP bawaan di versi Cloud | Salesforce/HubSpot | Terlalu berat untuk laptop |
| EspoCRM | 3.383★, 2014 | AGPL-3.0 | B (PHP) | REST API | – | – |
| Frappe CRM | 3.581★ | AGPL-3.0 | B | REST API | – | – |

→ CRM + follow-up WA untuk member (±6 kebutuhan) → **jalur B `crm-wa`** (kontak + tahap + pengingat; pesan dikirim lewat kanal OpenClaw/manual, bukan blast).

### 2.6 Helpdesk / inbox pelanggan

| Software | Bukti | Lisensi | Lokal | Agent | Menggantikan | Catatan |
|---|---|---|---|---|---|---|
| Chatwoot | 37.109★, 2019 | MIT (kecuali folder `enterprise/`) | **B** + butuh URL publik untuk webhook WhatsApp Cloud API | REST API; MCP komunitas | Qontak Rp400–750 rb+, Wati | **Bukan kandidat lokal.** Butuh VPS |
| FreeScout | 4.554★ | AGPL-3.0 | B (PHP) | API (modul) | Help Scout/Zendesk | Email saja |
| Zammad | 5.946★ | AGPL-3.0 | B | API | Zendesk | Berat |

→ Auto-reply WA member (±12) sebaiknya memakai **kanal WhatsApp OpenClaw** (sudah dipakai member) + skill `balas-chat-cs`. Tidak perlu helpdesk server. Catatan risiko kanal WA non-resmi ada di lampiran.

### 2.7 HR, absensi & payroll

| Software | Bukti | Lisensi | Lokal | Agent | Indonesia | Menggantikan | Catatan |
|---|---|---|---|---|---|---|---|
| Frappe HRMS | 8.819★, 2022 | GPL-3.0 | B (bench/Docker) | REST API | **Tidak paham PPh 21 TER/BPJS** | Talenta Rp25–50 rb/karyawan/bln, Gadjian ±Rp12,5 rb | Terlalu berat + tidak lokal Indonesia |
| OrangeHRM | 1.142★ | GPL-3.0 | B (PHP) | REST API | Tanpa payroll ID | Sama | – |
| Horilla | (repo aktif) | LGPL-2.1 | B (Django) | API | Tanpa payroll ID | Sama | – |
| Dolibarr (cuti, pengeluaran, gaji manual) | – | GPL-3.0 | M–S | API | Tanpa PPh 21 | – | Hanya pencatatan |

→ **Jalur B `absensi-lokal` + `gaji-umkm`** (PPh 21 TER dari `research/sources/pph21-ter-tabel.json`, BPJS, slip gaji).

### 2.8 Proyek / tugas / SOP / catatan

| Software | Bukti | Lisensi | Lokal | Agent | Menggantikan | Catatan |
|---|---|---|---|---|---|---|
| **Vikunja** | 5.491★, 2018 | AGPL-3.0 | **M–S**: satu binary Go + SQLite (ada aplikasi desktop) | **REST API** | Trello Standard ±USD5/user, ClickUp, Asana | Ringan, cocok untuk tim kecil di jaringan kantor |
| **SiYuan** | 46.478★, 2020, topik `local-first`, `mcp` | AGPL-3.0 | **M**: installer desktop | **API kernel lokal** (127.0.0.1:6806 + token); MCP komunitas | Notion Plus ±USD10/user | SOP, wiki, notulen. Pengembang dari Tiongkok: audit data/telemetri sebelum direkomendasikan |
| Logseq | 45.033★ | AGPL-3.0 | M (desktop) | File Markdown lokal (agent bisa menyunting langsung) | Notion | Alternatif paling sederhana untuk agent |
| AFFiNE | 72.894★ | MIT (klien); backend lisensi lain | M (desktop) | Terbatas | Notion/Miro | Lisensi klien ramah; API untuk agent kurang jelas |
| AppFlowy | 76.901★ | AGPL-3.0 | M (desktop) | Terbatas | Notion | – |
| Plane | 59.789★ | AGPL-3.0 | B (Docker) | API | Jira/Linear/ClickUp | Server |
| Kanboard | 9.881★ | MIT | S (PHP) | JSON-RPC API | Trello | Mode perawatan; lisensi bebas |
| Planka | 12.576★ | **Fair Use License** (komersial terbatas) | B | API | Trello | Hindari bundel |

### 2.9 Dokumen, PDF & e-signature

| Software | Bukti | Lisensi | Lokal | Agent | Menggantikan | Catatan |
|---|---|---|---|---|---|---|
| **Stirling-PDF (Desktop)** | 92.890★, 2023, v2.14.3 (Agu 2026) | MIT (inti) + folder `app/proprietary/` (fitur tim/SSO/audit berbayar) | **M**: `.msi`/`.exe` Windows, `.dmg` Mac, offline | **REST API + pipeline + MCP** (klaim vendor) | Adobe Acrobat Pro (±USD20/bln), situs PDF online | Gabung/potong/crop **resi**, OCR, kompres, tanda tangan gambar. Fitur inti gratis untuk bisnis |
| Paperless-ngx | 45.940★, 2022 | GPL-3.0 | **B** (Docker) | REST API; MCP komunitas | Arsip dokumen berbayar | Arsip nota + OCR. Berat → jalur B `arsip-nota` |
| DocuSeal | 18.605★ | AGPL-3.0 | B (server) | API | Mekari Sign/Privy (harga tidak publik) | **TTE tidak tersertifikasi**: sah menurut UU ITE Ps. 11, tapi pembuktiannya lebih lemah daripada PSrE (Privy/Mekari Sign/Peruri) |
| Documenso / OpenSign | 15.161★ / 7.023★ | AGPL-3.0 | B | API | Sama | Sama |
| LibreOffice | proyek besar | MPL-2.0 | M | CLI `soffice --headless --convert-to pdf` | Microsoft 365 (sebagian) | Konversi dokumen oleh agent |

### 2.10 Formulir/survei & 2.11 Penjadwalan/booking

| Software | Bukti | Lisensi | Lokal | Catatan |
|---|---|---|---|---|
| Formbricks | 13.006★ | AGPL-3.0 (+ folder `ee`) | B | Formulir untuk publik butuh server |
| HeyForm | 8.986★ | AGPL-3.0 | B | Sama |
| LimeSurvey | 3.732★ | GPL-2.0+ | B (PHP) | Sama |
| Cal.com | – | MIT (file LICENSE saat ini) | B (Postgres, berat) | Pengganti Calendly (±USD10–12/user). Butuh server publik |
| Easy!Appointments | 4.394★, 2014 | GPL-3.0 | B (PHP) | Booking salon/klinik. Butuh server publik |
| Rallly | 5.269★ | AGPL-3.0 | B | Polling jadwal |

→ Untuk pelanggan dari luar, **Google Forms/Calendar gratis sudah memadai**. Tidak ada nilai tambah dari versi lokal. Untuk internal (antrian klinik/salon di satu komputer) → jalur B `jadwal-janji` (prioritas rendah).

### 2.12 Toko online & 2.13 Analitik/laporan

| Software | Bukti | Lisensi | Lokal | Agent | Menggantikan | Catatan |
|---|---|---|---|---|---|---|
| WooCommerce | 10.527★ | GPL-3.0 | B (WordPress + hosting) | REST API | Shopify (±USD29+) | Toko online wajib online (hosting). Bukan produk lokal |
| Bagisto / Medusa / Saleor | 28.160★ MIT / 36.435★ MIT(+EE) / 23.369★ BSD-3 | – | B | API | – | Untuk developer |
| **Grist Desktop** | grist-core 11.851★ (Apache-2.0); desktop 518★, v0.3.15 (Sep 2026) | Apache-2.0 | **M**: installer Win/Mac/Linux, **offline, file `.grist` = SQLite** | SQLite + REST API lokal; formula Python (sandbox pyodide) | Airtable (USD20+/user), Sheets berbayar | Buku stok/CRM/rekap versi "spreadsheet pintar". Catatan: impor di Windows butuh izin symlink |
| **Datasette** | 11.479★, 2017 | Apache-2.0 | S (Python/pip; installer dari Komunitech) | **JSON API di atas SQLite** | Dashboard SaaS | Mesin "laporan otomatis" untuk semua alat jalur B |
| Metabase OSS | 49.394★ | AGPL-3.0 (+ folder `enterprise` komersial) | S (JAR, butuh Java) | REST API | Metabase Cloud, Looker | Dashboard untuk usaha mapan |
| Apache Superset | 74.897★ | Apache-2.0 | B | API | – | Terlalu berat |
| Evidence | 6.957★ | MIT | S (Node) | Laporan = SQL + Markdown | – | Cocok untuk laporan yang ditulis agent |
| **Actual Budget** | 29.104★, 2022, v26.9.0 (1 Sep 2026) | MIT | **M**: installer Win/Mac, local-first | `@actual-app/api` (Node) | YNAB (±USD15), aplikasi anggaran | Untuk profesional/freelancer & kas usaha kecil |
| Umami / Plausible | 38.972★ MIT / 29.195★ AGPL | – | B | API | Analitik web | Butuh server (website) |

### Otomasi (catatan lisensi)
- **n8n** (205.770★): **Sustainable Use License**. Hanya untuk keperluan bisnis internal. Komunitech **tidak boleh** menjualnya sebagai bagian produk; pembeli boleh memasang sendiri.
- **NocoDB** (65.050★): kini juga **SUL** (LICENSE diperbarui 29 Jan 2026).
- **Activepieces** (24.694★): MIT (kecuali folder `ee`), jadi pengganti yang aman lisensinya.
- **Teable** (21.815★): inti AGPL-3.0, paket MIT.

OpenClaw sendiri sudah punya cron + skill, sehingga otomasi server terpisah umumnya tidak diperlukan.

---

## 3. TOP 10 kurasi (jalur A) + penghematan per bulan

Penghematan = biaya SaaS yang tidak perlu dibayar lagi, sesuai kisaran harga di §2. Biaya jasa setup & listrik tidak dihitung.

| # | Software | Kebutuhan VIP yang dijawab | Setup awam | Agent (OpenClaw) | Menggantikan | Hemat/bln (perkiraan) | Nilai tambah Komunitech |
|---|---|---|---|---|---|---|---|
| 1 | **Dolibarr** (DoliWamp) — GPL-3.0 | Laporan, stok, kasir, CRM/follow-up, invoice | M–S (Windows mudah; Mac lebih sulit) | **REST API resmi** → skill `dolibarr-*` (buat invoice, cek stok, penawaran, laporan harian terjadwal) | Jurnal/Accurate Rp333–499 rb + Moka/Majoo Rp249–799 rb + Qontak CRM ±Rp400 rb+ | **±Rp0,6–1,7 jt** | Installer + konfigurasi bahasa ID, PPN 12%/DPP 11/12, template faktur, akun API baca-dulu |
| 2 | **Frappe Books** — AGPL-3.0 | Pembukuan, invoice, stok & POS kecil (solo/2–5 orang) | **M** | SQLite (baca laporan) + CSV Import Wizard (input) | Jurnal Rp399–499 rb / Kledo Rp140–350 rb / Paper.id | **±Rp140–500 rb** | COA SAK EMKM, template cetak, skill "catat → import", laporan ke WA. **Rilis terakhir Nov 2024: pantau** |
| 3 | **hledger** — GPL-3.0 | Laporan keuangan otomatis (agent mencatat dan melapor) | **M** (binary) | **CLI + JSON**; paling andal untuk agent | Pembukuan SaaS mikro | **±Rp140–500 rb** | Mesin untuk skill `laporan-keuangan-emkm`, `arus-kas-13minggu`, `rekonsiliasi-bank`; template akun Indonesia |
| 4 | **Odoo Community 19** + `l10n_id_efaktur_coretax` — LGPL-3.0 | Usaha mapan (50+ orang = 14 member): akuntansi, stok, penjualan, e-Faktur | S–B | XML-RPC/JSON API | Accurate/Jurnal + fitur e-Faktur (Klikpajak/OnlinePajak) | **±Rp0,5–1,5 jt+** | Jasa implementasi (bukan instan). Skill laporan via API. Pantau modul OCA |
| 5 | **Stirling-PDF Desktop** — MIT (inti) | **Cetak resi Shopee** (crop/gabung PDF resi ke 100×150), arsip, OCR | **M** | REST API/pipeline/MCP | Acrobat Pro ±USD20, alat PDF online | **±Rp150–330 rb** | Pipeline "rapikan resi" + skill; privasi (file tidak diunggah) |
| 6 | **Grist Desktop** — Apache-2.0 | Stok opname, CRM sederhana, rekap operasional | **M** | SQLite + REST API | Airtable/Sheets berbayar | **±Rp300 rb** (per tim kecil) | Template Indonesia: buku stok, daftar pelanggan, jadwal follow-up |
| 7 | **Vikunja** — AGPL-3.0 | Asisten admin / tugas tim / follow-up internal | M–S | **REST API** (satu binary + SQLite) | Trello/ClickUp/Asana | **±Rp100–500 rb** (tim 5–10) | Skill "ringkas grup WA → tugas di Vikunja" |
| 8 | **SiYuan** (alt: Logseq) — AGPL-3.0 | SOP, notulen, basis pengetahuan untuk agen CS | **M** | API lokal + token; MCP (komunitas, audit dulu) | Notion Plus ±USD10/user | **±Rp165 rb/user** | Template SOP (`sop-writer`), basis pengetahuan toko untuk `balas-chat-cs` |
| 9 | **Actual Budget** — MIT | Kas & anggaran (profesional/freelancer, usaha kecil) | **M** | `@actual-app/api` | YNAB/aplikasi anggaran | **±Rp150–250 rb** | Lisensi bebas → boleh dibundel penuh; kategori berbahasa Indonesia |
| 10 | **Datasette** — Apache-2.0 | **Laporan otomatis** di atas SQLite (semua alat jalur B) | S (dipasang lewat installer Komunitech) | JSON API + SQL | Dashboard/BI SaaS | (pendukung) | Lapisan laporan bersama untuk `kasir-lokal`, `buku-stok`, `gaji-umkm` |

Catatan pemilihan:
- CRM server (Twenty/Krayin), helpdesk (Chatwoot), HR (Frappe HRMS), booking, formulir, dan toko online **tidak masuk TOP 10**. Alasannya: butuh server/Docker atau internet publik, atau (khusus HR) tidak paham aturan Indonesia.
- **Kombinasi paket yang disarankan:**
  - **Solo/kecil:** Frappe Books atau hledger + Stirling-PDF + Actual + alat jalur B.
  - **Menengah:** Dolibarr + Grist + Vikunja + jalur B gaji/absensi.
  - **Mapan:** Odoo + jasa setup.

---

## 4. Implikasi lisensi untuk paket berbayar Komunitech

| Jenis | Contoh | Boleh dibundel dalam paket berbayar? | Kewajiban |
|---|---|---|---|
| MIT / Apache-2.0 / BSD | Actual, Stirling-PDF (inti), Grist, Datasette, InvenTree, Krayin, Kanboard, Activepieces (non-ee) | **Ya** | Sertakan teks lisensi & atribusi (Apache: + NOTICE, tandai file yang diubah). Folder `proprietary/`/`ee/` tidak termasuk |
| GPL-2/3, LGPL-3 | Dolibarr, GnuCash, hledger, Odoo CE, ERPNext | **Ya, versi asli tanpa modifikasi** | Sertakan lisensi + tawaran/tautan kode sumber versi persis. Modifikasi yang didistribusikan wajib GPL. Skill/template terpisah yang memakai API/CLI = karya terpisah (boleh tertutup). **PERLU REVIEW pemilik** untuk template yang dimasukkan ke dalam aplikasi |
| AGPL-3.0 | Frappe Books, Vikunja, SiYuan, Logseq, DocuSeal, Metabase | Ya (sama seperti GPL) | Jika Komunitech **memodifikasi dan menyediakannya lewat jaringan** (mis. VPS terkelola), kode modifikasi wajib dibuka untuk pengguna. Untuk instal lokal tanpa modifikasi: kewajiban sama seperti GPL |
| **BSL 1.1** | Akaunting | **Tidak** | Maks. 2 user / 1 perusahaan / 1.000 invoice; tidak boleh rebrand atau jasa akuntansi |
| **ELv2** | Invoice Ninja | **Tidak (PERLU REVIEW)** | Tidak boleh jadi layanan terkelola / mengakali lisensi |
| **Sustainable Use / Fair Use** | n8n, NocoDB, Planka | **Tidak** | Hanya untuk penggunaan internal; pembeli boleh memasang sendiri, Komunitech hanya boleh menjual panduan/jasa (tanpa menyertakan software) |
| Merek dagang | Odoo, Dolibarr, dll. | – | Jangan pakai merek mereka di nama produk ("Paket X untuk Dolibarr" boleh sebagai deskripsi) |

Model paling aman: **Komunitech menjual skill + template + panduan + jasa**, sedangkan software diunduh dari sumber resmi oleh installer/skrip Komunitech dengan checksum. Dengan begitu Komunitech bukan pihak yang mendistribusikan ulang software.

---

## 5. Jalur B — alat kecil buatan Komunitech

Prinsip teknis bersama (sesuai CLAUDE.md):
- **Python standar saja** (`sqlite3`, `csv`, `json`, `http.server`, `argparse`).
- **Satu file SQLite** per usaha di folder dokumen pengguna.
- **CLI dengan output JSON** agar mudah dipanggil skill OpenClaw.
- Tampilan web lokal opsional (`127.0.0.1`).
- Backup = salin satu file.
- Lintas OS.
- Perhitungan uang/pajak lewat script, dengan pembulatan sesuai standar library.
- Laporan terjadwal via **cron OpenClaw**, dikirim ke WA/Telegram pemilik.
- Tidak mengirim data ke luar.

| # | Alat | Menjawab kebutuhan VIP | Spesifikasi singkat | Kenapa open-source yang ada tidak cocok | Skill pasangan |
|---|---|---|---|---|---|
| 1 | **`buku-stok`** | Stok/inventori, stock opname (3) + laporan | Tabel barang, lokasi, mutasi masuk/keluar, stok minimum, HPP rata-rata. Impor file pesanan/produk Shopee/TikTok (CSV/XLSX→CSV). Mode opname (hitung fisik → selisih). Laporan stok menipis harian | InvenTree butuh Docker dan fokus komponen; Dolibarr/Odoo terlalu besar untuk seller solo; tidak ada yang paham format ekspor marketplace ID | `rekap-penjualan-csv`, `hitung-hpp`, `harga-jual-marketplace`, `listing-marketplace` |
| 2 | **`resi-picking`** | **Cetak resi Shopee** (3) | Dari file pesanan: buat **daftar ambil barang (picking list)** + urutan resi, tandai pesanan "sudah dikemas", kurangi stok di `buku-stok`. Crop/gabung PDF resi didelegasikan ke Stirling-PDF (API lokal) atau `pypdf` (BSD) sebagai dependensi opsional | Shopee sudah punya cetak massal & mode thermal di Seller Centre; yang belum ada adalah alur picking + stok lokal. Open API resi butuh registrasi partner | `rekap-penjualan-csv` |
| 3 | **`kasir-lokal`** | Operasional toko offline, laporan harian | Transaksi, item, diskon, metode bayar (tunai/QRIS statis/transfer, dicatat saja), struk 58/80 mm (HTML → print), tutup kasir, rekap harian. Opsi PPN 12% DPP 11/12 atau PPh final 0,5% | OSPOS/NexoPOS butuh PHP+MySQL; POS Frappe Books minim fitur struk/rekap Indonesia; SaaS Rp249–799 rb/outlet | `hitung-ppn`, `pph-final-umkm`, `rekap-penjualan-csv` |
| 4 | **`absensi-lokal`** | Absensi (2) | Karyawan kirim "masuk/pulang" ke bot OpenClaw (WA/Telegram) atau admin mencatat. Tersimpan di SQLite (waktu, catatan, opsional lokasi yang diketik). Rekap bulanan: hadir, telat, lembur, cuti → input gaji | Frappe HRMS/OrangeHRM/Horilla berat dan butuh server; absensi via chat sesuai kebiasaan UMKM | `surat-peringatan-karyawan` |
| 5 | **`gaji-umkm`** | Gaji (2) + usaha 16–50+ orang (24 member) | Komponen gaji, **PPh 21 TER** (tabel `research/sources/pph21-ter-tabel.json`), BPJS Kesehatan & Ketenagakerjaan, THR, slip gaji HTML/PDF, rekap bank transfer (CSV) | Tidak ada payroll open-source yang mengerti TER/BPJS; Talenta/Gadjian Rp12,5–50 rb/karyawan/bln | skill pph21-ter, slip-gaji-bpjs, hitung-thr (sedang dibuat) |
| 6 | **`crm-wa`** | Follow-up & sales (±6), pengingat | Kontak, sumber lead, tahap (baru → ditawar → deal → selesai), catatan, tanggal follow-up berikutnya. Pengingat harian ke pemilik. Draf pesan + tautan `wa.me` (dikirim manusia/kanal OpenClaw). **Tanpa blast otomatis** | Twenty/Krayin/Chatwoot butuh server; Qontak CRM Rp400 rb+; CRM umum tidak paham alur "chat WA → deal" | `follow-up-prospek`, `surat-penawaran-harga`, `balas-chat-cs` |
| 7 | **`buku-piutang`** | Follow-up tagihan, laporan | Invoice bernomor, jatuh tempo, pembayaran sebagian, aging (0–30/31–60/>60 hari), pengingat terjadwal, draf pesan penagihan | InvoiceShelf/SolidInvoice butuh server; Invoice Ninja ELv2 | `buat-invoice`, `tagih-piutang` |
| 8 | **`kas-umkm`** | Laporan keuangan otomatis (±20) | Kas masuk/keluar sederhana (bukan double-entry) → laporan SAK EMKM & arus kas. Opsi ekspor ke hledger/Frappe Books untuk yang naik kelas | GnuCash/hledger terlalu teknis bagi pencatat mikro | `laporan-keuangan-emkm`, `arus-kas-13minggu`, `rekonsiliasi-bank` |
| 9 | **`laporan-harian`** (orkestrator) | Laporan otomatis terjadwal (±20) | Membaca SQLite dari alat 1–8, menyusun ringkasan harian/mingguan (angka dihitung script), mengirim via cron OpenClaw. Datasette opsional untuk tampilan | Tidak ada alat yang menyatukan data UMKM lokal + kirim ringkasan ke WA | semua skill laporan |
| 10 | **`arsip-nota`** (prioritas rendah) | Privasi, rapi dokumen | Folder pantau + indeks SQLite (tanggal, vendor, nominal hasil `ekstrak-nota-faktur`), pencarian | Paperless-ngx butuh Docker | `ekstrak-nota-faktur` |

Urutan pembangunan yang disarankan:
1. `buku-stok` + `resi-picking`
2. `laporan-harian`
3. `crm-wa`
4. `gaji-umkm` + `absensi-lokal`
5. `kasir-lokal`
6. `buku-piutang`
7. `kas-umkm`

Alasannya: urutan ini mengikuti jumlah member yang butuh dan bahan yang sudah ada di repo.

---

## 6. Risiko lisensi & keamanan

1. **Lisensi berubah.** Sudah terjadi pada Akaunting (→ BSL), NocoDB (→ SUL, Jan 2026), Planka (→ Fair Use), dan Stirling-PDF (open-core). Cek ulang LICENSE setiap rilis paket; kunci versi yang sudah diaudit.
2. **Proyek melambat.** Frappe Books belum merilis versi baru sejak Nov 2024, walaupun commit tetap berjalan. Siapkan jalur migrasi: ekspor CSV → Dolibarr/hledger.
3. **Keamanan instal lokal.**
   - Server lokal (Dolibarr/DoliWamp, Vikunja, Grist, SiYuan, Stirling) harus **hanya mendengar di 127.0.0.1**. Jangan dibuka ke internet atau di-port-forward.
   - Pakai kata sandi admin kuat dan token API terpisah dengan hak minimal. Untuk agent, mulai dari akses baca.
4. **Agent menulis data keuangan.** Wajibkan konfirmasi di skill sebelum membuat, mengubah, atau menghapus transaksi. Simpan log perubahan dan backup otomatis sebelum operasi tulis massal.
5. **Unduhan installer.** Hanya dari rilis resmi (GitHub/SourceForge resmi proyek) dengan verifikasi checksum. Jangan pernah dari mirror tidak resmi.
6. **MCP komunitas** (SiYuan, Chatwoot, Twenty, Paperless). Audit dulu sesuai CLAUDE.md Tahap 3 sebelum direkomendasikan. Lebih baik skill memanggil API resmi software secara langsung.
7. **Pajak.**
   - e-Faktur/Coretax: hanya Odoo yang punya modul resmi; format bisa berubah. Alat jalur B tidak mengirim ke DJP, hanya menghitung dan menyiapkan data.
   - Cantumkan disclaimer bahwa pembulatan belum dicocokkan dengan Coretax.
8. **Data pribadi (UU PDP).** Data karyawan (gaji, NIK, BPJS) dan pelanggan tersimpan lokal. Berikan panduan enkripsi disk/backup terenkripsi, dan jangan kirim isi mentah ke kanal chat. Ringkasan cukup berisi angka agregat.
9. **TTE tidak tersertifikasi** (DocuSeal/Documenso) tetap sah, tapi pembuktiannya lemah. Untuk kontrak penting, arahkan ke PSrE (Privy/Mekari Sign/Peruri).
10. **Kanal WhatsApp OpenClaw** memakai Baileys (WhatsApp Web, tidak resmi), sehingga ada risiko nomor diblokir. Sarankan nomor terpisah atau Telegram untuk laporan internal. Lihat lampiran.

---

## 7. Sumber

Lisensi (file LICENSE/COPYING, diakses 2026-09-23 via raw.githubusercontent.com)
- https://github.com/frappe/books · https://github.com/Dolibarr/dolibarr · https://github.com/odoo/odoo · https://github.com/simonmichael/hledger · https://github.com/Gnucash/gnucash · https://github.com/beancount/beancount · https://github.com/beancount/fava
- https://github.com/akaunting/akaunting (LICENSE.txt, BSL 1.1) · https://github.com/invoiceninja/invoiceninja (ELv2) · https://github.com/InvoiceShelf/InvoiceShelf · https://github.com/SolidInvoice/SolidInvoice · https://github.com/bigcapitalhq/bigcapital · https://github.com/frappe/erpnext
- https://github.com/opensourcepos/opensourcepos · https://github.com/Blair2004/NexoPOS · https://github.com/inventree/InvenTree
- https://github.com/twentyhq/twenty · https://github.com/krayin/laravel-crm · https://github.com/espocrm/espocrm · https://github.com/frappe/crm · https://github.com/chatwoot/chatwoot · https://github.com/zammad/zammad · https://github.com/freescout-help-desk/freescout · https://github.com/frappe/helpdesk
- https://github.com/frappe/hrms · https://github.com/orangehrm/orangehrm · https://github.com/horilla-opensource/horilla
- https://github.com/go-vikunja/vikunja · https://github.com/siyuan-note/siyuan · https://github.com/logseq/logseq · https://github.com/toeverything/AFFiNE · https://github.com/AppFlowy-IO/AppFlowy · https://github.com/makeplane/plane · https://github.com/kanboard/kanboard · https://github.com/plankanban/planka
- https://github.com/Stirling-Tools/Stirling-PDF · https://github.com/paperless-ngx/paperless-ngx · https://github.com/docusealco/docuseal · https://github.com/documenso/documenso · https://github.com/OpenSignLabs/OpenSign
- https://github.com/formbricks/formbricks · https://github.com/heyform/heyform · https://github.com/LimeSurvey/LimeSurvey · https://github.com/calcom/cal.com · https://github.com/alextselegidis/easyappointments · https://github.com/lukevella/rallly
- https://github.com/woocommerce/woocommerce · https://github.com/bagisto/bagisto · https://github.com/medusajs/medusa · https://github.com/saleor/saleor · https://github.com/PrestaShop/PrestaShop · https://github.com/opencart/opencart · https://github.com/evershopcommerce/evershop
- https://github.com/gristlabs/grist-core · https://github.com/gristlabs/grist-desktop · https://github.com/simonw/datasette · https://github.com/metabase/metabase · https://github.com/apache/superset · https://github.com/evidence-dev/evidence · https://github.com/actualbudget/actual · https://github.com/umami-software/umami · https://github.com/plausible/analytics
- https://github.com/n8n-io/n8n · https://github.com/nocodb/nocodb · https://github.com/activepieces/activepieces · https://github.com/teableio/teable

Fitur, instalasi, rilis
- Frappe Books: https://github.com/frappe/books/releases · https://sourceforge.net/projects/frappe-books.mirror/ · https://docs.frappebooks.com/miscellaneous/import-wizard.html · `translations/id.csv` di repo
- Dolibarr: https://sourceforge.net/projects/dolibarr/files/Dolibarr%20installer%20for%20Windows%20(DoliWamp)/ · https://wiki.dolibarr.org/index.php/Dolibarr_for_Windows_(DoliWamp) · https://wiki.dolibarr.org/index.php?title=Module_Web_Services_API_REST_%28developer%29 · https://www.dolibarr.org/dolibarr-erp-crm-v22-has-been-released.php
- Odoo Indonesia: https://www.odoo.com/documentation/19.0/applications/finance/fiscal_localizations/indonesia.html · `addons/l10n_id_efaktur_coretax/__manifest__.py` (branch 19.0)
- hledger: https://github.com/simonmichael/hledger/releases
- GnuCash: https://github.com/Gnucash/gnucash/releases/tag/5.16 · https://www.gnucash.org/news.phtml
- Grist Desktop: https://github.com/gristlabs/grist-desktop (README: offline, SQLite, symlink Windows)
- Stirling-PDF: https://github.com/Stirling-Tools/Stirling-PDF/releases · https://docs.stirlingpdf.com/Paid-Offerings/ · https://www.xda-developers.com/stopped-uploading-pdfs-to-random-websites-after-finding-this-free-desktop-app/
- InvenTree: https://docs.inventree.org/en/latest/start/install/ · https://github.com/inventree/inventree-python
- Actual: https://github.com/actualbudget/actual/releases
- SiYuan MCP (komunitas): https://github.com/PurpleLiu/siyuan-mcp · https://github.com/unclemicdo/siyuan-mcp-server
- Twenty MCP: https://www.folk.app/articles/twenty-crm-mcp · Chatwoot MCP komunitas: https://github.com/hugoblanc/chatwoot-mcp
- Resi Shopee: https://desty.mekari.com/blog/cara-cetak-resi-shopee · https://www.hitoko.co.id/blog/cara-cetak-resi-shopee-dengan-printer-biasa-dan-mode-thermal/

Harga SaaS (kisaran publik)
- Jurnal: https://www.jurnal.id/en/pricing-plans/ · Accurate: https://softwareonline.id/harga-accurate-online/ · Kledo: https://kledo.com/perbandingan/
- Moka/Majoo: https://www.hashmicro.com/id/blog/review-aplikasi-moka-pos/ · https://majoo.id/harga/detail · Olsera: https://www.olsera.com/en/pricing
- Qontak: https://qontak.com/en/pricing/ · Jubelio: https://jubelio.com/tag/harga-jubelio/ · Paper.id: https://www.paper.id/pricing
- Talenta/Gadjian: https://www.talenta.co/en/pricing-subscription/ · https://www.gadjian.com/price · https://albatech.id/blog/berapa-biaya-hris-indonesia-2026-panduan-harga
- TTE: https://www.hukumonline.com/berita/a/cepat-belum-tentu-aman--pentingnya-tanda-tangan-elektronik-tersertifikasi-lt68f4e9ec7ba3f/ · https://prolegal.id/tanda-tangan-elektronik-tidak-tersertifikasi-pada-kontrak-bisnis-apakah-sah/

---

## Lampiran — ringkasan temuan konektor/MCP layanan online (riset sebelumnya, dihentikan atas arahan pemilik)

- **Konektor resmi yang siap pakai:** Google (Gmail/Drive/Calendar), Microsoft 365, Notion, Canva, HubSpot, Zoom, ClickUp, Trello, Meta Ads MCP (open beta), TikTok Ads MCP, Google Ads MCP (read-only).
- **WhatsApp resmi:** Wati MCP (hosted), Meta WhatsApp Business Tools MCP (±15 Sep 2026, untuk setup/tes, bukan broadcast). Qontak hanya Open API. **Kanal WhatsApp OpenClaw memakai Baileys (tidak resmi) → risiko nomor diblokir** (openclaw/openclaw#4376). Fonnte/Wablas juga tidak resmi.
- **Pembayaran lokal dengan MCP resmi:** Mayar, DOKU. Xendit & Midtrans hanya punya MCP komunitas (0–4★), jadi hindari untuk akses tulis.
- **Akuntansi lokal SaaS:** Jurnal (API HMAC; MCP komunitas read-only 2★), Accurate (OAuth, tanpa MCP), Kledo (MCP komunitas 0★). Tidak ada MCP resmi.
- **Marketplace:** Shopee (54% GMV 2025) & TikTok Shop+Tokopedia (38%) belum punya MCP resmi untuk seller. MCP komunitas berbasis scraping berisiko melanggar ToS.
- **Coretax:** tidak ada API publik untuk wajib pajak; integrasi hanya lewat PJAP.
- **Afiliasi:** Notion 50% selama 12 bln, HubSpot 30% berulang selama 12 bln, Mekari hingga 30% cashback berulang, Kledo Rp150 rb, Xendit Rp20 rb.
- Sumber utama: https://techcrunch.com/2026/09/15/meta-now-lets-ai-agents-handle-the-boring-parts-of-whatsapp-business-setup/ · https://github.com/openclaw/openclaw/issues/4376 · https://mayar.id/mcp · https://developers.doku.com/accept-payments/doku-mcp-server · https://github.com/mrslbt/xendit-mcp · https://github.com/Teguhcanggu/jurnal-mcp · https://teknologi.bisnis.com/read/20260516/84/1974139/pangsa-pasar-e-commerce-2025-shopee-tiktok-gerus-bukalapak-blibli-dan-lazada
