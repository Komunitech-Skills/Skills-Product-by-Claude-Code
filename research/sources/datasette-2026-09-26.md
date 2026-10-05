# Riset sumber — Datasette

**Tanggal riset:** 2026-09-26
**Peneliti:** sesi Komunitech Skills Factory (agent, verifikasi langsung — instal nyata dari PyPI, lihat "Cara verifikasi" di bawah)
**Konteks:** lanjutan `research/software-pengganti-saas-2026-09-23.md` (Datasette disebut di §2 tabel Data/Analitik dan TOP 10 #10) sebagai "dasbor lokal" untuk membuka data alat lokal Komunitech (`buku-stok`, `kasir-lokal`, `crm-wa`, `absensi-lokal`, `buku-piutang`, `kas-umkm`). Lihat juga `docs/panduan-datasette.md` dan `skills/dasbor-lokal/`.

## 1. Identitas & sumber resmi

| Item | Nilai |
|---|---|
| Nama produk | **Datasette** — "multi-tool" open source untuk eksplorasi & publikasi data SQLite |
| Pembuat | **Simon Willison** (pengembang independen, dikenal luas di komunitas Python/data; juga pembuat sqlite-utils, LLM CLI, dsb.) |
| Repo resmi | https://github.com/simonw/datasette |
| Situs produk / dokumentasi | https://datasette.io/ , dokumentasi lengkap https://docs.datasette.io/ |
| Paket resmi | **PyPI**: https://pypi.org/project/datasette/ (`pip install datasette` / `pipx install datasette`) |
| Lisensi | **Apache License 2.0** — dikonfirmasi langsung dari file lisensi di dalam paket terpasang: `datasette-0.65.5.dist-info/licenses/LICENSE` (teks Apache-2.0 standar) dan `pip show datasette` (`License: Apache License, Version 2.0`) |
| Versi yang dicoba | **0.65.5** — versi yang ditarik `pip install datasette` dari PyPI resmi pada tanggal riset (bukan versi lama yang dipin sengaja) |
| Umur & perawatan | Proyek berjalan sejak 2017, aktif dipakai luas di komunitas data (11.000+★ di GitHub per riset 2026-09-23), dipakai sebagai rujukan "mesin laporan SQLite" di berbagai artikel/dokumentasi pihak ketiga; bukan proyek baru/"AI slop" |

## 2. Cara verifikasi (kejujuran metodologi)

Berbeda dari sebagian software di `research/software-pengganti-saas-2026-09-23.md` yang tidak bisa dijalankan langsung di sandbox ini (Docker, aplikasi desktop berlayar), **Datasette adalah paket Python murni** sehingga bisa dicoba langsung:

1. Dipasang ke **virtualenv terpisah** di scratchpad sesi ini (`/tmp/.../scratchpad/datasette/venv`), **bukan** ke sistem: `python3 -m venv venv && ./venv/bin/pip install datasette`. Jaringan proxy sesi mengizinkan PyPI; instalasi berhasil tanpa hambatan.
2. Dikonfirmasi versi & lisensi lewat `pip show datasette` dan membaca langsung file `LICENSE` yang ikut terpasang di `site-packages`.
3. **Enam database SQLite fiktif** dibuat dengan **menjalankan langsung script asli skill Komunitech** (`buku-stok/scripts/stok.py`, `kasir-lokal/scripts/kasir.py`, `crm-wa/scripts/crm.py`, `absensi-lokal/scripts/absensi.py`, `buku-piutang/scripts/piutang.py`, `kas-umkm/scripts/kas.py`) dengan data usaha fiktif (produk, transaksi kasir, kontak CRM, absensi, piutang, saldo kas) — bukan file rekaan manual, jadi skema tabelnya persis skema asli tiap skill.
4. Dijalankan `datasette --immutable <tiap-db> -m metadata.yml --get "/<db>/<query>.json"` untuk tiap canned query yang dirancang `skills/dasbor-lokal/templates/metadata.yml`, hasilnya **dicocokkan manual** dengan isi data fiktif yang dimasukkan (mis. stok menipis = produk dengan `stok <= stok_min`, penjualan per hari dijumlah per tanggal, piutang jatuh tempo = sisa > 0 dan tanggal lewat) — **semua benar**.
5. Dibuktikan bahwa Datasette **tidak mengubah database**: hash SHA-256 tiap file `.db` diambil sebelum dan sesudah seluruh rangkaian query (termasuk percobaan `INSERT` yang sengaja dikirim untuk menguji penolakan) — **hash identik**, dan Datasette sendiri menolak permintaan bukan-`SELECT` (`{"ok": false, "error": "Statement must be a SELECT", "status": 400}`).
6. Script cadangan `skills/dasbor-lokal/scripts/dasbor.py` (Python `sqlite3` biasa, tanpa Datasette) diuji dengan query yang sama lewat URI `?mode=ro`, hasil sama persis, dan hash database tetap tidak berubah.

**Yang TIDAK diuji:** menjalankan Datasette di komputer Windows/Mac awam sungguhan (sandbox ini Linux); memasang lewat `pipx` secara khusus (dipasang lewat `pip` di venv untuk kecepatan riset, tapi `pipx install datasette` adalah cara resmi yang didokumentasikan Datasette sendiri untuk pengguna akhir dan dipakai sebagai anjuran utama di `docs/panduan-datasette.md`); plugin Datasette apa pun (tidak dipakai/disarankan).

## 3. Keputusan kurasi

**Jalur:** kurasi software (jalur A) — **BUKAN** distribusi ulang. Komunitech **tidak pernah menyertakan** file/paket Datasette dalam ZIP produk apa pun. Pengguna memasangnya sendiri dari PyPI resmi mengikuti `docs/panduan-datasette.md`.

**Alasan boleh dikurasi (sesuai aturan lisensi CLAUDE.md §Tahap 2):**
- Apache-2.0 = boleh dimodifikasi & dijual dengan syarat sertakan lisensi + atribusi + `NOTICE` (jika ada) + tandai file yang diubah. Karena Komunitech **tidak mendistribusikan atau memodifikasi kode Datasette sama sekali** (hanya menyiapkan perintah CLI + file `metadata.yml` konfigurasi untuknya), kewajiban distribusi tidak berlaku — tetap dicantumkan di `skills/dasbor-lokal/ATTRIBUTION.md` sebagai etika & kejujuran ke pembeli.
- Bukti pemakaian nyata: >11.000★ GitHub, pembuat individu dengan rekam jejak kuat dan dikenal luas di ekosistem Python/data (bukan akun baru), proyek berjalan 8+ tahun dengan rilis bertahap, dipakai sebagai rujukan di banyak artikel/dokumentasi teknis pihak ketiga sebagai "cara cepat bikin API/dasbor dari SQLite".

**Nilai tambah Komunitech (wajib — skill publik gratis tidak boleh dijual apa adanya):**
1. Panduan instalasi bahasa Indonesia untuk awam, resmi dari PyPI (`pip`/`pipx`), tanpa `curl | sh` — `docs/panduan-datasette.md`.
2. Penekanan keamanan yang tidak otomatis diikuti pengguna awam: **localhost saja** (`--host 127.0.0.1`, bukan `0.0.0.0`), **selalu `--immutable`** supaya data asli tidak bisa berubah — dijelaskan dengan alasan dan cara uji dari HP (pola yang sama dengan `docs/panduan-dolibarr.md` §2.4).
3. `metadata.yml` canned query yang sudah dirancang & **diuji nyata** khusus untuk skema database keenam alat lokal Komunitech (bukan contoh generik Datasette).
4. Script cadangan `scripts/dasbor.py` (Python standar, tanpa Datasette) supaya skill tetap berguna walau pengguna tidak mau/tidak sempat memasang Datasette.
5. Pemisahan tegas dengan `laporan-harian-usaha` (laporan teks terjadwal siap kirim) — `dasbor-lokal` untuk eksplorasi interaktif, dijelaskan di `SKILL.md` §"Kapan TIDAK digunakan".

**Keputusan:** ✅ **Lulus audit lisensi & kurasi.** Masuk katalog dengan `jalur=orisinal` (skill, panduan, dan `metadata.yml` adalah karya Komunitech; Datasette sendiri tetap Apache-2.0 milik pembuatnya, dicatat di `ATTRIBUTION.md`) dan `lisensi=Proprietary Komunitech`. Status awal **draft** — belum melalui Tahap 6 penuh (uji A/B, uji banding pesaing, uji platform asli oleh manusia, beta tester).

**PERLU REVIEW pemilik:** tidak ada isu lisensi abu-abu. Yang perlu perhatian pemilik: instalasi resmi lewat `pipx`/`pip` belum dicoba di Windows/Mac sungguhan oleh Komunitech (hanya Linux sandbox); sebaiknya diuji sungguhan sebelum naik ke status `uji`/`lulus`, mengikuti `docs/uji-platform.md`.
