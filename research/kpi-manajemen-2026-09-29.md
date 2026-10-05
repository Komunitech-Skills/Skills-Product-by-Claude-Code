# Riset KPI & Manajemen Usaha — 2026-09-29

**Kebutuhan pemilik (2026-09-29):** alat/skill/sistem siap pakai untuk mengelola operasional & KPI, untuk usaha pemilik sendiri, member VIP, dan penjualan eceran. Area KPI: (a) kinerja karyawan/tim (target per orang/divisi, OKR, penilaian), (b) keuangan & penjualan, (c) operasional (produksi, stok, pengiriman, SLA, komplain), (d) marketing. Data sekarang di Excel/Google Sheets, kertas, dan grup WA. Bentuk yang diinginkan: lokal, tanpa biaya bulanan, open-source, bisa dioperasikan agent (OpenClaw); alternatif non-AI dicatat juga.

**Metode & batas verifikasi (jujur):**
- Bintang/umur/aktivitas: GitHub search API (via tool sesi) 2026-09-29.
- Lisensi: teks `LICENSE` dibaca langsung dari `raw.githubusercontent.com`. Ada modul di Odoo/Frappe yang dicek lewat ada/tidaknya file di repo.
- Tidak ada kode pihak ketiga yang diinstal atau dijalankan.
- **Belum terverifikasi:** rilis terakhir (API rilis diblokir sesi), dukungan Windows/Mac asli, kelengkapan terjemahan Indonesia (hanya dicek *file terjemahan ada*), dan API Leantime/OrangeHRM/Metabase untuk agent. Ditandai "?" di tabel. Semua "?" wajib dicek sebelum ada produk yang dijual.

---

## 1. Yang SUDAH kita punya per area KPI

Dari `catalog.csv` (semua `lulus`) dan `skills/*`. Tidak ada satu pun skill/riset/panduan yang membahas KPI/OKR/penilaian kinerja (pencarian `kpi|okr` di `research/`, `docs/`, `skills/*/SKILL.md` hanya kena kebetulan di sumber lain; `proposal-kerjasama`, `dolibarr-usaha`, `tulisan-tanpa-kesan-ai` menyebut kata itu sekilas).

| Area KPI | Sudah tercakup | Cakupan |
|---|---|---|
| **Kinerja tim: kehadiran** | `absensi-lokal` (SQLite: hadir/terlambat/lembur/alpa), `gaji-umkm`, `slip-gaji-bpjs` | Hadir & jam kerja saja. Bukan target/hasil kerja |
| **Kinerja tim: tugas** | `vikunja-tugas` (tugas per anggota, terlambat, dari notulen WA), `notulen-rapat`, `ringkas-grup-wa` (daftar tindakan siapa-apa-tenggat) | Tugas selesai/terlambat; tanpa target berangka & bobot |
| **Kinerja tim: penilaian/OKR** | `sop-onboarding`, `surat-peringatan-karyawan`, `lowongan-kerja` (sisi HR lain) | **Kosong**: tidak ada penilaian kinerja, OKR, target per orang |
| **Keuangan** | `laporan-keuangan-emkm`, `arus-kas-13minggu`, `analisis-rasio-keuangan-usaha`, `kas-umkm`, `buku-piutang`, `tagih-piutang`, `hitung-hpp`, `hledger-usaha`, `frappe-books-usaha`, `dolibarr-usaha`, `actual-budget-usaha` | Kuat. Rasio & tren ada; belum ada "target vs realisasi" bulanan |
| **Penjualan** | `rekap-penjualan-csv`, `kasir-lokal`, `crm-wa` (pipeline, konversi), `follow-up-prospek`, `laporan-harian-usaha` | Kuat untuk realisasi. Target per sales/divisi belum ada |
| **Operasional: stok** | `buku-stok`, `resi-picking`, `pantau-website-toko` | Stok menipis/nilai persediaan ada |
| **Operasional: insiden/komplain** | `laporan-insiden-usaha`, `balas-ulasan-pelanggan`, `analisis-ulasan`, `agen-cs-toko` | Insiden per kejadian; **tidak ada log komplain/SLA/produksi/pengiriman berkelanjutan** |
| **Marketing** | `laporan-iklan-mingguan`, `audit-akun-iklan`, `konten-mingguan`, `kalender-konten-30hari`, `promo-kalender` | Kuat untuk iklan (ROAS/CPA). Target konten/lead belum |
| **Pelaporan & dasbor** | `dasbor-lokal` (Datasette + canned query atas SQLite alat kita), `grist-usaha`, `analisis-excel`, `laporan-otomatis-terjadwal`, `laporan-harian-usaha`, `presentasi-data-ke-atasan` | Mesin & pengiriman Telegram sudah ada. Yang kurang: **data dan definisi KPI-nya** |

Kesimpulan: **mesin pelaporan sudah ada, isi "KPI"-nya belum.** Semua yang ada mengukur *realisasi*; belum ada lapisan *target, bobot, skor, dan penilaian*.

---

## 2. Tabel celah (gap)

| # | Celah | Area | Dampak | Butuh alat besar? |
|---|---|---|---|---|
| G1 | Target vs realisasi per orang/divisi + bobot + skor pencapaian (%) | Tim, Sales | Tinggi (tiap usaha punya tim) | **Tidak** — cukup script + SQLite/CSV |
| G2 | OKR (objective, key result, progres, check-in mingguan) | Tim, strategi | Sedang–tinggi (member profesional) | Tidak untuk tim ≤15 |
| G3 | Penilaian kinerja periodik (form, skala, bobot, catatan, 360 ringan) | HR | Sedang (jangan jadi dasar PHK; disclaimer) | Tidak untuk UMKM; ya untuk 50+ karyawan |
| G4 | Log operasional: komplain, SLA (waktu respons/selesai), produksi (jumlah/reject), pengiriman (tepat waktu/retur) | Operasional | Tinggi (manufaktur/distribusi/logistik: 8 member VIP; lihat `kebutuhan-member-vip-2026-09-29.md`) | Tidak — tabel kecil + input dari chat |
| G5 | Katalog KPI siap pakai per jenis usaha (rumus, sumber data, batas hijau/kuning/merah) | Semua | Tinggi untuk awam ("KPI apa yang harus saya pantau?") | Tidak |
| G6 | Input dari kertas/grup WA/Excel/Google Sheets → tabel KPI (impor, validasi, deteksi data ganjil) | Semua | Tinggi (sumber data pemilik memang begitu) | Tidak |
| G7 | Dasbor KPI visual (semaphore, tren, peringkat) | Semua | Sedang | Tidak: Datasette/Grist sudah ada |
| G8 | Laporan KPI terjadwal ke pemilik (Telegram), draf ke manajer | Semua | Sedang | Tidak: pakai `laporan-otomatis-terjadwal` |
| G9 | Sistem multi-pengguna: karyawan mengisi sendiri, atasan menyetujui | Tim 20+ | Sedang (usaha mapan) | **Ya** — perlu server (Frappe HRMS/Leantime/Operately) |
| G10 | Pelacakan waktu/jam proyek (jasa, konsultan, agensi) | Operasional jasa | Rendah–sedang | Ya (Kimai) atau Vikunja |

G1–G8 bisa ditutup **tanpa memasang software baru** (skill + script stdlib + data lokal). Hanya G9–G10 yang butuh server.

---

## 3. Perbandingan kandidat

Data bintang dari GitHub API 2026-09-29. Penilaian "Awam lokal": **M** = mudah (installer/satu file), **S** = sedang, **B** = berat (Docker/server/DB terpisah). Vonis lisensi mengikuti aturan CLAUDE.md §Tahap 2: GPL/AGPL boleh, dengan syarat hasil turunan berlisensi sama; skill yang mengoperasikan lewat API/CLI adalah karya terpisah; lisensi source-available (SUL/ELv2/BSL/Fair Use) **tidak boleh dibundel/dijual**.

| Produk | ★ / umur | Aktivitas | Lisensi (dibaca dari LICENSE) | Vonis komersial | Fitur KPI relevan | Pasang lokal | UI Indonesia | API untuk agent |
|---|---|---|---|---|---|---|---|---|
| **Frappe HRMS** | 8.836★, 2022 (dari ERPNext) | Aktif (push 28 Sep 2026) | GPL-3.0 | Boleh (skill/panduan terpisah, tanpa mendistribusikan modifikasi) | **Ada** doctype `Appraisal Cycle`, `Appraisal`, `KRA`, `Goal` (hierarki induk-anak, progres), `Employee Performance Feedback` (dicek di repo) | **B**: bench/Docker (Linux); Windows lewat Docker Desktop/WSL | File `id.po` ada; kelengkapan ? | REST API Frappe (dikenal luas) |
| **Leantime** | 11.675★, 2015 | Aktif (29 Sep 2026) | AGPL-3.0 (LICENSE dibaca; versi lama sempat kurang jelas) | Boleh, ketentuan sama | Goal & metrics tracking, tugas, timesheet, papan ide, retrospektif (README) | **S–B**: PHP 8.2+ + MySQL 8/MariaDB, atau Docker resmi | `id-ID.ini` ada | "Extendable via plugins and API" (README); detail ? |
| **Operately** | 562★, 2023 | Aktif (28 Sep 2026) | Apache-2.0 + folder `ee` berlisensi komersial (README/LICENSE) | Inti boleh; **jangan pakai/bundel `ee`** | **Goals/OKR**, check-in, ruang tim, proyek. **CLI + API + skill untuk OpenClaw sudah ada di ClawHub** (README) | **B**: Docker Compose (`install.sh`, Elixir + Postgres) | ? (kemungkinan hanya Inggris) | **CLI npm + API** (paling agent-native) |
| **OrangeHRM (OS)** | 1.144★, 2017 | Push 25 Sep 2026; rilis 5.9 (Jun 2024) di halaman rilis ? | GPL-3.0 | Boleh | Plugin Performance ada di kode (`orangehrmPerformancePlugin`); cakupan di edisi OS ? | **B**: PHP 7.4–8.5 + MySQL/MariaDB | ? | REST (README menyebut `restful-api`); ? |
| **Odoo Community 20** | 54.737★, 2014 | Sangat aktif | LGPL-3.0 | Boleh untuk Community | Modul `hr_appraisal` **tidak ada** di repo Community (404); penilaian/OKR = **Enterprise** (berbayar). Hanya `hr_skills`, `hr_holidays`, `hr_recruitment` yang ada | **S–B** (lihat riset 2026-09-23) | Ya (`l10n_id`) | XML/JSON-RPC |
| **Metabase OSS** | 49.451★, 2015 | Sangat aktif | AGPL-3.0 di luar `enterprise/`; folder itu Metabase Commercial License | Boleh (jangan pakai binari/kode `enterprise`) | Dasbor KPI, kartu angka, sasaran/alert. **Bukan** sistem target/penilaian | **S**: JAR + Java 25 (Temurin). H2 bawaan "bukan untuk produksi" (dok. resmi) | `id.po` ada | REST API; autentikasi & API key di OSS ? |
| **Apache Superset** | 74.961★, 2015 | Sangat aktif | Apache-2.0 | Bebas | Dasbor & SQL; tanpa modul target | **B** (Python + DB + Redis) | ? | API |
| **Grafana** | 76.981★, 2013 | Sangat aktif | AGPL-3.0 | Boleh, ketentuan sama | Dasbor metrik/alert; orientasi observabilitas | **S** (binari/installer) | Sebagian ? | HTTP API |
| **Evidence.dev** | 6.965★, 2021 | Aktif | MIT (2026) | Bebas | Laporan = SQL + Markdown → situs statis. Cocok ditulis agent | **S** (Node.js) | Bebas (teks kita) | File teks — agent tulis langsung |
| **NocoDB** | 65.106★, 2017 | Aktif | **Sustainable Use License** (LICENSE.md, 29 Jan 2026): hanya untuk keperluan bisnis internal atau non-komersial; distribusi hanya gratis & non-komersial | **DILARANG dibundel/dijual**. Pemakai boleh memakai sendiri (internal) | Tabel + tampilan; tanpa modul KPI | B (Node + DB) | ? | REST otomatis |
| **Baserow** | 6.020★, 2020 | Aktif | MIT ("OSE"), kecuali folder `premium/` & `enterprise/` (berlisensi lain) | Boleh untuk OSE saja | Tabel + dasbor; fitur dasbor/aplikasi ada yang premium ? | **B** (Docker/Postgres) | ? | REST API |
| **Kimai** | 5.048★, 2016 | Aktif (28 Sep 2026) | AGPL-3.0 | Boleh | Pelacak jam kerja, laporan, faktur. Bukan KPI | **S–B**: PHP 8.2+, MySQL; Docker | `messages.id.xlf` ada; kelengkapan ? | JSON API (README) |
| **OpenProject** | 16.251★, 2012 | Aktif | GPL-3.0 | Boleh | Proyek/Gantt/waktu; tidak ada OKR di edisi Community ? | **B** (Ruby + Postgres) | Ya (umum dikenal) ? | API v3 |
| **Plane** | 60.044★, 2022 | Aktif | AGPL-3.0 | Boleh | Tugas/siklus; tanpa OKR di CE ? | **B** (Docker) | ? | API |
| **Twenty CRM** | 57.690★, 2022 | Aktif | AGPL-3.0 + file berlisensi komersial | Boleh (file bertanda komersial dilarang) | CRM/pipeline; bukan KPI tim | **B** (Docker/Postgres/Redis) | ? | GraphQL/REST |
| **InvenTree** | 7.654★, 2017 | Aktif | MIT | Bebas | Stok/komponen/produksi (perakitan, BOM) untuk manufaktur; bukan KPI | **B**: Docker | ? | REST |
| **Grist** (sudah ada) | grist-core Apache-2.0 | – | Apache-2.0 | Bebas | Tabel + rumus Python + grafik: **KPI scorecard bisa dibangun di sini** | **M** (Desktop) | Sebagian | SQLite + REST |
| **Datasette** (sudah ada) | 11.479★ | – | Apache-2.0 | Bebas | Dasbor/query di atas SQLite | S | – | JSON API |
| Open OKR (`open-okr/open-okr`) | **3★**, 2026-07 | – | AGPL-3.0 | – | OKR | – | – | – |
| Okra, Zaplyng | 9★ / 2★ | mati/kecil | ? | – | OKR | – | – | – |

**Catatan:**
- **Alat OKR mandiri open-source yang kuat ternyata tidak ada.** Pencarian GitHub "OKR tracker open source" hanya menemukan proyek ≤ 9★ (Okra, Zaplyng, Open OKR: tanda "AI slop"/tanpa pemakai → ditolak sesuai kriteria kurasi). Yang punya OKR sungguhan hanya **Operately** (562★, muda), **Leantime** (goals) dan **Frappe HRMS** (KRA/Goal/Appraisal). Sumber kuat = Leantime (11k★, sejak 2015) dan Frappe HRMS (8,8k★).
- **Odoo:** modul penilaian/OKR adalah Enterprise. Jangan diklaim "Odoo gratis untuk KPI".
- **NocoDB, dan folder `enterprise/`/`premium/`/`ee` di Metabase, Baserow, Operately, Twenty**: tidak boleh dibundel/dijual. Tidak masuk paket.
- Twenty/OpenProject/Plane/Superset/Baserow: tidak bermasalah lisensi, tetapi berat dan bukan alat KPI; tidak diusulkan.
- Metabase/Grafana/Evidence: bagus untuk *melihat* KPI; tidak memberi target, bobot, skor. Grist + Datasette sudah menutup fungsi itu dengan pemasangan jauh lebih mudah.

### Pendekatan tanpa instalasi: "KPI lewat Excel/Google Sheets + AI agent"

Layak dan **paling cocok untuk mayoritas pembeli awam**, dengan batasan:
- **Google Sheets:** agent OpenClaw tidak bisa membaca Sheet pribadi tanpa akun/API/OAuth, yang bertentangan dengan prinsip "tanpa API key/akun". Jalur aman: pengguna **unduh sebagai `.xlsx`/`.csv`** (File → Unduh) atau tempel isi → agent memproses lokal. Sebaliknya, agent **membuat file `.xlsx`/`.csv` template** yang bisa diunggah ke Google Drive (Impor). Tidak butuh akun untuk agent.
- **Excel:** `.xlsx` bisa ditulis dan dibaca dengan Python standar (`zipfile` + XML) tanpa `openpyxl`, seperti yang sudah dilakukan `analisis-excel` (dicek bahwa skill itu jalan tanpa paket tambahan; mekanisme persis perlu dirujuk saat implementasi).
- **Alur:** (1) agent buat template KPI dari pertanyaan singkat (jenis usaha, divisi, orang); (2) tim mengisi di Excel/Sheets atau lewat catatan grup WA (`ringkas-grup-wa` mengekstrak angka); (3) script menghitung **skor per KPI, bobot, skor total, status hijau/kuning/merah** (bukan dikira model; aturan pembulatan sama seperti standar library); (4) laporan draf dikirim ke Telegram lewat `laporan-otomatis-terjadwal`; (5) hasil disimpan di SQLite agar `dasbor-lokal` bisa membacanya.
- **Risiko:** data karyawan bersifat pribadi/sensitif. Pakai `cek-privasi-openclaw`; simpan lokal; hasil penilaian = bahan diskusi, **bukan** dasar keputusan PHK/sanksi tanpa proses hukum (ada `surat-peringatan-karyawan`). Skill hukum baru tidak dikerjakan (keputusan pemilik 2026-09-26): cukup disclaimer dan rujukan ke skill yang sudah ada.

**Pilihan non-AI (catatan untuk panduan pembeli):**
- Template Excel/LibreOffice/Google Sheets dan cetak untuk papan target di kantor.
- Looker Studio (gratis, tetapi cloud Google, bukan lokal).
- Leantime/Kimai bila tim ingin sistem tanpa agent, dengan server sendiri.
- Papan tulis/kertas + rapat mingguan 15 menit: sering cukup untuk ≤ 10 orang.

---

## 4. Rekomendasi (urut prioritas)

### #1 — Skill orisinal `kpi-tim` (jalur 1/KREASI + alat kecil)  — **prioritas utama**
- **Isi:** target per orang/divisi, bobot, skor pencapaian (script Python stdlib, SQLite + CSV/`.xlsx`), OKR ringan (objective, key result, progres, check-in mingguan), penilaian periodik (skala 1–5, bobot, catatan, opsi 360 ringan), **katalog KPI per jenis usaha** (toko online, manufaktur/distribusi, jasa/klinik/konsultan; area keuangan, sales, operasional, marketing), impor dari CSV/Excel/ringkasan grup WA (`ringkas-grup-wa`), template `.xlsx` siap isi, draf laporan Telegram & draf ke atasan (`presentasi-data-ke-atasan`).
- **Menutup:** G1, G2, G3, G4 (log komplain/SLA/produksi/pengiriman sebagai tabel kecil), G5, G6, G8.
- **Alasan:** kebutuhan langsung dari pemilik + 8 member VIP paket "Kantor & Manajemen"; nol instalasi; tidak ada pesaing kuat yang lokal & berbahasa Indonesia (pesaing: prompt/templat generik; wajib dicari di ClawHub/skills.sh saat uji banding); angka dihitung script; jalan di semua platform target.
- **Usaha:** sedang–besar (±1 iterasi pembuatan Opus karena ada perhitungan skor/bobot + verifikasi angka independen + uji A/B/banding pesaing; 1 iterasi paket template). Skrip serupa `absensi-lokal`/`gaji-umkm`.
- **Perlu persetujuan pemilik:** tier & harga (usulan: `ecer` Rp199.000, masuk paket VIP `kantor-manajemen`); apakah ada penilaian karyawan (sensitif) atau hanya target/hasil; nama.

### #2 — `dasbor-kpi` = perluasan `dasbor-lokal` + laporan terjadwal (tanpa produk baru)
- `kpi-tim` menulis `kpi.db` (SQLite). Tambahkan canned query & metadata Datasette KPI ke `dasbor-lokal` (semaphore, tren, peringkat, target vs realisasi) + resep jadwal `laporan-otomatis-terjadwal` (Senin pagi ke Telegram).
- Alternatif tampilan visual awam: templat **Grist** (`grist-usaha`) berisi tabel KPI + widget kartu/grafik.
- **Menutup:** G7, G8. **Usaha kecil** (update skill yang sudah `lulus`: revisi versi + uji ulang independen; bukan skill baru).
- **Perlu persetujuan:** tidak ada (perubahan versi patch/minor). Bila dijual terpisah: harga.
- Jangan pasang Metabase/Superset/Grafana sebagai paket: berat (Java 25 / DB terpisah / Docker) dan tidak menambah fungsi yang tidak sudah dimiliki Datasette + Grist.

### #3 — Panduan jalur-2 (produk siap pakai) untuk usaha 20+ orang: **Leantime** (goal & metrik + tugas + timesheet) — *kondisional*, bukan langsung dikerjakan
- **Alasan Leantime dibanding lainnya:** sumber terkuat (11,7k★, sejak 2015, aktif harian), AGPL-3.0 (boleh), bahasa Indonesia ada, goal tracking bawaan, gratis, bisa pakai PHP+MySQL atau Docker; menutup G9/G10 untuk tim yang ingin sistem bersama.
- **Sebelum jadi produk (wajib):** (a) uji nyata di sandbox terpisah dengan izin pemilik: pemasangan di Windows/Mac/mini-PC, kelengkapan terjemahan ID, API untuk agent (JSON-RPC? belum diverifikasi), (b) audit keamanan Tahap 3, (c) putuskan bentuk: hanya panduan + skill `leantime-tujuan`, atau jasa setup.
- **Usaha:** besar (pemasangan awam lebih sulit daripada Vikunja/Grist: butuh MySQL). Lebih realistis dijual sebagai **jasa setup berbayar** + panduan, bukan produk unduh-langsung.
- **Alternatif yang disimpan (belum dipilih):**
  - **Operately** — paling agent-native (CLI + API + skill OpenClaw sudah ada di ClawHub) dan OKR sungguhan, tetapi muda (562★, 2023), Docker/Elixir/Postgres, terjemahan ID belum jelas, ada folder `ee` komersial. Pantau 3–6 bulan; jika menguat dan ada opsi pemasangan lebih ringan → naikkan.
  - **Frappe HRMS** — paling lengkap (KRA + Appraisal Cycle + Goal + Feedback), GPL-3.0; berat (bench/Docker), tanpa payroll Indonesia (sudah diketahui). Cocok hanya untuk usaha mapan lewat **jasa setup VIP** — bukan produk unduh.
  - **Kimai** — hanya jika ada permintaan pelacakan jam (konsultan/agensi).

### Ditolak / tidak dikerjakan
- **NocoDB** (SUL: tidak boleh dibundel/dijual) — pemakaian internal pengguna boleh, tidak masuk paket.
- **Odoo untuk KPI/appraisal** (Enterprise-only), **Okra/Zaplyng/Open OKR** (bukti pemakaian nihil).
- Superset/Metabase/Grafana/Plane/OpenProject/Twenty/InvenTree/Baserow sebagai produk KPI: lisensi boleh (kecuali folder komersial), tetapi berat dan tidak lebih baik dari #1–#2 untuk pembeli awam.
- Skill hukum ketenagakerjaan baru untuk penilaian/PHK: tidak dikerjakan (keputusan pemilik 2026-09-26).

---

## 5. Perlu persetujuan / PERLU REVIEW pemilik

1. Tier & harga `kpi-tim` (usulan `ecer` Rp199.000) dan apakah masuk paket VIP `kantor-manajemen`.
2. Menjalankan uji pemasangan Leantime (dan opsional Operately) di sandbox: perlu izin memasang paket dari sumber luar (sesuai CLAUDE.md §5).
3. Jasa setup berbayar untuk Leantime/Frappe HRMS (mesin 24 jam, DB MySQL/Postgres): bagian dari keputusan "jasa setup" pemilik 2026-09-23; perlu SOP jasa.
4. Kebijakan data: data penilaian karyawan (sensitif), disimpan lokal saja + disclaimer; **jangan pernah menyimpan nama/kontak member di repo**.
5. Item "?" di tabel §3 (rilis terakhir, Windows/Mac, terjemahan ID, API) harus diverifikasi sebelum ada klaim jual.

## 6. Sumber (semua dibaca 2026-09-29)

- Statistik repo: GitHub search API (metabase/metabase, apache/superset, grafana/grafana, evidence-dev/evidence, nocodb/nocodb, baserow/baserow, orangehrm/orangehrm, frappe/hrms, odoo/odoo, kimai/kimai, Leantime/leantime, opf/openproject, makeplane/plane, twentyhq/twenty, inventree/InvenTree, operately/operately).
- Lisensi (raw): https://raw.githubusercontent.com/{metabase/metabase/master/LICENSE.txt, nocodb/nocodb/develop/LICENSE.md, baserow/baserow/develop/LICENSE, Leantime/leantime/master/LICENSE, orangehrm/orangehrm/main/LICENSE, frappe/hrms/develop/license.txt, kimai/kimai/main/LICENSE, opf/openproject/dev/LICENSE, evidence-dev/evidence/main/LICENSE, operately/operately/main/LICENSE, apache/superset/master/LICENSE, grafana/grafana/main/LICENSE, inventree/InvenTree/master/LICENSE, makeplane/plane/preview/LICENSE, twentyhq/twenty/main/LICENSE, odoo/odoo/20.0/LICENSE}
- Fitur Frappe HRMS: `hrms/hr/doctype/{appraisal_cycle,appraisal,kra,goal,employee_performance_feedback}` di https://github.com/frappe/hrms
- Leantime README (fitur, PHP 8.2+, MySQL 8/MariaDB 10.6+, Docker): https://github.com/Leantime/leantime
- Operately README & CLI: https://github.com/operately/operately , https://operately.com/help/cli
- Metabase JAR (Java 25, H2 bukan produksi, port 3000): https://www.metabase.com/docs/latest/installation-and-operation/running-the-metabase-jar-file
- OrangeHRM rilis/prasyarat: https://github.com/orangehrm/orangehrm/releases
- Kimai README: https://github.com/kimai/kimai
- Riset sebelumnya: `research/software-pengganti-saas-2026-09-23.md`, `research/kebutuhan-member-vip-2026-09-29.md`
