# Dasbor Lokal: Satu Layar untuk Data Usaha Anda

**Tanya "stok apa yang menipis?" dan AI Anda langsung membaca alat-alat lokal Komunitech yang sudah Anda pakai (kasir, stok, CRM/catatan prospek, absensi, piutang, kas) lalu menjawab dari data asli, atau menyiapkan dasbor di browser komputer sendiri. Tanpa biaya bulanan; data usaha tetap tersimpan di komputer Anda.**

Diuji AI penguji independen: 7 → 8,75 dari 10 di OpenClaw (tanpa skill, rata-rata per nota salah karena nota yang sudah dibatalkan ikut dihitung).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Software tambahan: Datasette (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Satu jawaban, bukan enam aplikasi.** "Penjualan hari ini berapa, stok apa yang tinggal sedikit, siapa yang piutangnya lewat jatuh tempo?" — dijawab langsung dari data asli di komputer Anda (file database), dihitung ulang, bukan dikira-kira.
- ✅ **Dasbor beneran di browser (opsional).** Lewat Datasette (perangkat lunak gratis terpisah), buka alamat khusus komputer sendiri (`http://127.0.0.1:8001`) dan lihat, sortir, klik-klik tabel data toko Anda sendiri seperti dasbor BI (laporan interaktif) berbayar — tanpa mengirim data tabelnya ke internet. Tidak mau pasang Datasette? Skill ini tetap menjawab pertanyaan lewat Python bawaan, langsung dari terminal/chat, tanpa instalasi apa pun.
- ✅ **Dibuat hanya-baca.** Database dibuka dalam mode **baca-saja** (immutable, tidak bisa diubah), jadi data asli tidak ikut berubah lewat skill ini. Dasbor disiapkan hanya untuk komputer Anda sendiri (alamat `127.0.0.1`), dan skill tidak menyarankan membukanya ke internet.
- ✅ **Dasbor KPI tim (sejak versi 1.0.2).** Alat ke-7, skill KPI Tim (`kpi-tim`; KPI = ukuran target kerja): skor perusahaan → divisi → orang, tren per periode, dan daftar KPI merah (yang belum mencapai target), dibaca dari file data yang dibuat `kpi-tim`. Ada mode anonim di sisi `kpi-tim` bila layar dilihat orang lain.
- ✅ **Pertanyaan siap pakai (query) yang benar-benar berguna**, bukan generik: stok menipis (dengan yang paling parah di atas), penjualan per hari (nota yang dibatalkan otomatis dikeluarkan), piutang jatuh tempo, kehadiran karyawan, prospek per tahap penjualan (pipeline), saldo kas per akun.

## Cocok untuk siapa
- Pemilik UMKM/toko yang sudah memakai **dua alat lokal Komunitech atau lebih** (mis. Kasir Lokal + Buku Stok, atau Buku Piutang + Kas UMKM; nama skillnya `kasir-lokal`, `buku-stok`, `buku-piutang`, `kas-umkm`) dan ingin melihat gambaran besarnya dari satu tempat.
- Yang penasaran "coba saya lihat sendiri datanya" tanpa harus menghafal perintah tiap skill.
- Yang ingin dasbor ala aplikasi berbayar (Metabase, Retool, dsb.) tapi berjalan di komputer sendiri dan gratis softwarenya.

**Kurang cocok:** baru punya satu alat lokal saja dan cukup bertanya langsung ke skill alat itu; ingin laporan teks otomatis dikirim tiap malam ke Telegram (pakai skill Laporan Harian Usaha, `laporan-harian-usaha`); ingin dasbor bisa dibuka dari HP di luar rumah/toko (skill ini sengaja menolak — baca FAQ di bawah).

## Contoh sebelum & sesudah
**Sebelum:** buka file Excel kasir, buka aplikasi stok, buka catatan piutang di HP — cocokkan manual satu per satu, sambil menghitung sendiri mana yang sudah lewat jatuh tempo.

**Sesudah:** ketik *"stok apa yang menipis?"*:
```
=== buku-stok / stok-menipis: Stok menipis atau habis ===
sku     | nama          | varian | stok | stok_min
--------+---------------+--------+------+---------
TEP-1KG | Tepung Terigu | 1kg    | 2.0  | 8.0
KPI-250 | Kopi Bubuk    | 250g   | 5.0  | 10.0
(2 baris)
```
Atau *"siapa yang piutangnya sudah lewat jatuh tempo?"*:
```
pelanggan   | no_nota | jatuh_tempo | sisa
------------+---------+-------------+-------------
Bu Tini     | PB-0001 | 2026-09-05  | Rp 1.200.000
Warung Jaya | PB-0003 | 2026-09-15  | Rp 800.000
(2 baris)
```
(Contoh nyata dari uji dengan data fiktif — lihat `examples/`.)

## Cara pakai
Cukup ketik permintaan biasa:
- "Database toko saya di mana saja?"
- "Stok apa yang tinggal sedikit?"
- "Penjualan 30 hari terakhir per hari"
- "Siapa yang belum bayar dan sudah lewat jatuh tempo?"
- "Siapa yang belum absen hari ini / jam berapa Andi masuk kemarin?"
- "Prospek saya ada berapa di tiap tahap?"
- "Saldo kas saya berapa?"
- "Saya mau lihat dasbornya sendiri di browser" (AI menyiapkan perintah Datasette untuk Anda)

Nama teknis tiap pertanyaan (untuk yang penasaran): `cari`, `stok-menipis`, `penjualan-per-hari`, `piutang-jatuh-tempo`, `kehadiran-harian`, `prospek-per-tahap`, `saldo-per-akun`.

## Instalasi singkat
1. **Tidak wajib instal apa pun** untuk mulai — cukup punya minimal satu alat lokal Komunitech yang sudah dipakai (ada datanya).
2. Salin folder `dasbor-lokal` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

3. (Opsional, untuk tampilan browser) pasang **Datasette** sekali mengikuti `docs/panduan-datasette.md` — perintahnya resmi dari PyPI (`pip`/`pipx install datasette`), bukan tempel-jalankan skrip dari internet.

Panduan pemasangan skill lengkap: `CARA-INSTAL.md` di paket. Butuh **Python 3.8+** (gratis di python.org). Tidak butuh internet, akun, atau paket tambahan untuk fitur intinya.

## Hasil uji (jujur)

**Hasil uji (angka nyata):**
- Uji di OpenClaw, 1 Okt 2026 (v1.0.4), skor 1-10 dari agen penguji independen: tanpa skill 7 → dengan skill 8,75. Tugas: stok menipis, penjualan seminggu, dan piutang lewat jatuh tempo. Tanpa skill, rata-rata per nota salah (Rp 731.500, nota yang sudah dibatalkan ikut dihitung) dan produk nonaktif dianggap aktif. Dengan skill: penjualan 7 hari Rp 7.315.000 dari 9 nota (nota batal dikeluarkan) dan rata-rata per nota Rp 812.778. Saat diminta membuka dasbor ke HP lewat ngrok (layanan yang membuka komputer Anda ke internet), skill menolak dengan alasan yang jelas.
- Uji independen terpisah (26 Sep 2026): 6 dari 6 pertanyaan (query) dihitung ulang dari data mentah dan cocok persis; file database tidak berubah (hash sama sebelum dan sesudah); skor 9 dari 10.
- Jujur: pada jebakan ngrok, AI tanpa skill sudah cukup baik (8 vs 8,5). Keunggulan skill terutama di ketepatan angka.

**Status uji (jujur):** versi terkini 1.0.4. Rincian per tahap:
- Versi 1.0.0 (diuji pembuat): memakai database fiktif hasil menjalankan langsung skill `buku-stok`, `kasir-lokal`, `crm-wa`, `absensi-lokal`, `buku-piutang`, dan `kas-umkm`, ditambah uji regresi otomatis (`tests/uji_regresi.py`, 18 skenario termasuk database rusak/tidak ada/tabel salah). Datasette 0.65.5 dari PyPI resmi dicoba di virtualenv terpisah (tidak dipasang ke sistem) dan hasil pertanyaan siap pakai (canned query) dicocokkan manual — **cocok**, dan hash file database sebelum/sesudah **sama persis** (tidak berubah).
- Versi 1.0.2 (alat `kpi-tim`, 5 query, blok `kpi` di `templates/metadata.yml`): diuji dengan Datasette 0.65.5 di virtualenv terpisah (`--immutable`, `127.0.0.1`, hash database sama sebelum/sesudah) dan uji regresi 25/25.
- Sesudah itu sudah diuji oleh penguji independen (26 Sep 2026) dan di OpenClaw (uji otomatis oleh agen AI, 1 Okt 2026); hasilnya di atas.
- **Belum** diuji di Codex dan Cursor, belum diuji manusia di komputer pembeli sungguhan, dan belum diuji dengan data usaha nyata dalam jumlah besar.

## FAQ
**Apakah skill ini bisa mengubah data toko saya secara tidak sengaja?**
Tidak seharusnya. Skill ini membuka database dalam mode **baca-saja** (`?mode=ro` di Python, `--immutable` di Datasette), jadi perintah selain "lihat data" (SELECT) akan ditolak oleh SQLite dan Datasette sendiri. Perubahan data tetap hanya lewat skill alat masing-masing (kasir, stok, dan seterusnya), bukan lewat dasbor.

**Saya tidak mau pasang software tambahan, masih bisa pakai?**
Bisa. Bagian "query" jalan penuh dengan Python bawaan tanpa Datasette sama sekali. Datasette hanya untuk yang mau tampilan klik-klik di browser.

**Apakah dasbornya bisa dibuka dari HP saya di luar toko?**
Sengaja **tidak**. Skill ini hanya menyiapkan perintah untuk `127.0.0.1` (komputer sendiri) dan tidak menyarankan membuka ke jaringan/internet — itu mengekspos data pelanggan dan uang Anda ke orang lain. Baca `docs/panduan-datasette.md` untuk alasannya.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.

---
Komunitech tidak berafiliasi dengan proyek Datasette; Datasette adalah perangkat lunak terpisah (Apache-2.0) milik pembuatnya.
