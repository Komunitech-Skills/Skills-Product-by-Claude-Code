---
name: dasbor-lokal
description: Dasbor lokal read-only di atas SQLite untuk alat Komunitech (buku-stok, kasir-lokal, crm-wa, absensi-lokal, buku-piutang, kas-umkm, kpi-tim) - temukan file database, jalankan canned query siap pakai (penjualan per hari, stok menipis, piutang jatuh tempo, kehadiran, prospek per tahap, saldo kas, skor KPI tim & KPI merah), dan siapkan perintah Datasette read-only/immutable untuk eksplorasi interaktif di browser localhost. Tanpa Datasette pun tetap jalan lewat script sqlite3 standar. Gunakan saat pengguna minta "buka dasbor toko saya", "lihat semua data di satu tempat", "explore database", local dashboard, data explorer, SQL browser. Berbeda dari laporan-harian-usaha (teks harian siap kirim); dasbor-lokal untuk eksplorasi interaktif, bukan laporan terjadwal.
---

# Dasbor Lokal (jembatan baca-saja ke database alat Komunitech)

## Tujuan
Pemilik usaha yang memakai beberapa alat lokal Komunitech (kasir, stok, CRM, absensi, piutang, kas — semua SQLite di komputernya sendiri) ingin **melihat semuanya dari satu tempat**, seperti dasbor BI berbayar, tanpa mengirim data ke mana pun. Skill ini **tidak** membuat data baru: ia membaca (baca-saja, tidak pernah menulis) database yang sudah ada dan menyiapkan:
1. Query SQL siap pakai ("canned query") untuk pertanyaan yang paling sering ditanyakan.
2. Perintah **Datasette** (perangkat lunak terpisah, Apache-2.0, https://datasette.io/) untuk membukanya di browser bila pengguna mau eksplorasi interaktif.
3. Jalur cadangan Python murni (`scripts/dasbor.py query ...`) yang mencetak tabel ringkas walau Datasette tidak terpasang.

**Versi 1.0.2** (revisi rendah): alat ke-7 `kpi-tim` (database `kpi.db` hasil `skor_kpi.py ekspor-db`,
5 query: `perusahaan-tren`, `divisi-terbaru`, `orang-terbaru`, `tren-orang`, `kpi-merah`; blok `kpi` di
`templates/metadata.yml`). Skor per orang = data pribadi karyawan: tetap `127.0.0.1` saja; sarankan
`--anonim` di `ekspor-db` bila layar dilihat orang lain. Uji regresi 25/25.

**Versi 1.0.1** (revisi rendah): mode teks (`query ... ` tanpa `--json`) sekarang menampilkan angka
bulat dari kolom REAL SQLite (mis. `stok`) sebagai `25`, bukan `25.0` — nilai pecahan asli (`25.5`)
tetap tampil apa adanya, kolom Rupiah tidak berubah. Uji regresi 22/22.

## Kapan digunakan
- "Buka dasbor toko saya", "lihat semua data di satu tempat", "saya mau eksplorasi data sendiri" → `datasette` (siapkan perintah) atau `query` (jawab langsung).
- "Stok apa yang menipis?", "penjualan per hari bulan ini?", "siapa yang piutangnya lewat jatuh tempo?", "siapa yang belum absen?", "prospek per tahap berapa?", "saldo kas berapa?" → `query <alat> <nama-query>` langsung, tanpa perlu Datasette.
- "Saya mau lihat tabel mentahnya / mau tanya SQL bebas" → arahkan ke Datasette (browser localhost) via perintah dari `datasette`.

## Kapan TIDAK digunakan
- **Laporan teks harian siap kirim ke Telegram/WA** (ringkasan naratif terjadwal) → pakai `laporan-harian-usaha`, bukan skill ini.
- Alat lokalnya belum pernah dipakai (belum ada database) → arahkan ke skill alat itu dulu (mis. `kasir-lokal`, `buku-stok`) supaya ada data.
- Meminta skill ini **mengubah** data (tambah transaksi, hapus baris, dsb.) → tolak; semua koneksi di sini baca-saja by design. Arahkan ke skill alat yang bersangkutan.
- Meminta membuka dasbor ke jaringan/internet (supaya bisa diakses dari HP lain, cabang lain, dsb.) → tolak dan jelaskan risikonya (lihat Keamanan). Datasette di sini hanya untuk `127.0.0.1` (komputer sendiri).
- Data pelanggan/karyawan yang sensitif → tampilkan seperlunya; jangan sarankan expose ke internet atau membagikan link dasbor ke orang lain.

## Persiapan (opsional, hanya bila mau pakai Datasette)
Datasette **tidak wajib**. Untuk canned query, `scripts/dasbor.py query ...` sudah cukup dan tidak butuh instalasi apa pun.

Bila pengguna mau tampilan browser: pasang Datasette sekali mengikuti `docs/panduan-datasette.md` (pip/pipx dari PyPI resmi, **bukan** curl-pipe-sh). Skill akan cek dulu apakah `datasette` sudah ada di PATH (`dasbor.py datasette`); kalau belum, tunjukkan perintah instalasi dari panduan itu, jangan memasangkan sendiri tanpa persetujuan pengguna.

## Langkah kerja
Semua perintah lintas OS (Windows: `python`/`py`). Tambahkan `--json` untuk hasil terstruktur.

### A. Temukan database yang ada
```bash
python3 scripts/dasbor.py cari
```
Tunjukkan mana yang ADA/TIDAK ADA dan lokasinya. Yang TIDAK ADA berarti alat itu belum pernah dipakai — bukan galat.

### B. Jalankan canned query
```bash
python3 scripts/dasbor.py query buku-stok stok-menipis
python3 scripts/dasbor.py query kasir-lokal penjualan-per-hari
python3 scripts/dasbor.py query buku-piutang piutang-jatuh-tempo
python3 scripts/dasbor.py query absensi-lokal kehadiran-harian --tanggal 2026-09-25
python3 scripts/dasbor.py query crm-wa prospek-per-tahap
python3 scripts/dasbor.py query kas-umkm saldo-per-akun
python3 scripts/dasbor.py query kpi-tim kpi-merah        # butuh kpi.db dari kpi-tim ekspor-db
```
- Lihat daftar lengkap: `python3 scripts/dasbor.py daftar-query`.
- `--db PATH` mengganti lokasi database default (berguna bila pengguna menyimpan di tempat lain).
- `kehadiran-harian` tanpa `--tanggal` memakai tanggal hari ini; kosong bukan berarti galat, bisa jadi memang belum ada yang tap hari itu.
- Sampaikan hasil apa adanya. Uang ditampilkan format "Rp 1.200.000"; jangan membulatkan atau menghitung ulang — angka sudah dari database asli.

### C. Buka dasbor interaktif di browser (opsional, pakai Datasette)
```bash
python3 scripts/dasbor.py datasette
```
Mencetak perintah siap tempel yang mencakup **semua database yang ditemukan** + `templates/metadata.yml` (berisi canned query yang sama seperti bagian B, tapi bisa diklik di browser) + `--host 127.0.0.1` (wajib; jangan pernah pakai `0.0.0.0` atau menambahkan tunnel/ngrok). Jika `datasette` belum terpasang, keluaran juga berisi perintah instalasi resmi (rujuk `docs/panduan-datasette.md`); tunjukkan itu ke pengguna, jangan langsung menjalankan instalasi tanpa izin.

Setelah pengguna menjalankan perintah itu sendiri di terminalnya, arahkan ke `http://127.0.0.1:8001` (port default Datasette) untuk melihat tabel, menjalankan SQL bebas, dan mengklik canned query yang tersedia.

## Format Output
- Mode teks (default): tabel rata kolom + judul query + "Sumber: <path db>" + jumlah baris.
- Mode `--json`: `{"ok": true, "alat", "query", "judul", "db", "parameter", "jumlah_baris", "baris": [...]}`. Kolom uang tetap angka mentah di JSON (pembulatan tampilan hanya di mode teks).

## Batasan & Penanganan Error
- **Database tidak ditemukan** → pesan menyebut path yang dicek dan menyarankan `--db PATH` atau memakai alat itu dulu. Bukan galat fatal.
- **File 0 byte / bukan file SQLite / rusak** → pesan jelas "bukan database yang bisa dibaca/rusak"; sarankan cadangan (`backup`) milik skill alat itu, jangan mencoba memperbaiki file dari sini.
- **Tabel/kolom tidak ada** (mis. salah pasang query alat ke database alat lain, atau versi skill sumber sudah berubah skema) → pesan menyebut kemungkinan penyebab dan menyarankan perbarui skill alat itu; tidak menebak-nebak isi data.
- **Database sedang dipakai program lain** (`database is locked`) → sampaikan bahwa data aman, coba lagi sebentar; jangan mengulang otomatis bertubi-tubi.
- **Semua koneksi baca-saja** lewat URI SQLite `?mode=ro`: bahkan bila SQL yang dijalankan bukan `SELECT` (mis. salah ketik), SQLite akan menolaknya di level driver, dan Datasette (di luar skill ini) juga menolak apa pun selain `SELECT`.
- Skill ini tidak pernah mengirim data ke internet; semua berjalan di komputer pengguna.

## Keamanan
- Datasette hanya dijalankan di `127.0.0.1` (localhost). **Tidak pernah** disarankan `--host 0.0.0.0`, port-forward router, atau tunnel (ngrok, Cloudflare Tunnel, dsb.) — itu membuka data usaha (transaksi, pelanggan, karyawan) ke internet.
- Semua database dibuka **immutable/read-only** (`-i`/`--immutable` di Datasette; `?mode=ro` di script Python) — data asli tidak bisa berubah lewat skill ini apa pun query yang dijalankan.
- Skill ini tidak menyimpan salinan data di tempat lain; ia hanya membaca file yang sudah ada di komputer pengguna saat diminta.
