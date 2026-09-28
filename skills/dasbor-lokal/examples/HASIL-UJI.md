# Uji independen Akun B — `dasbor-lokal` v1.0.0

Penguji: Akun B (sesi terpisah dari pembuat), 2026-09-26. Hanya membaca folder
`skills/dasbor-lokal/` + `docs/panduan-datasette.md` (commit d93bb98). Kerja di scratchpad
terisolasi, Datasette dipasang di venv terpisah (bukan Python sistem). Enam database contoh
dibuat dengan menjalankan script asli tiap alat Komunitech (data fiktif), bukan disuntik
manual.

## Ringkasan
- 5 skenario (`01`–`05`) + A/B (`00-pembanding-tanpa-skill`) + banding pesaing
  (`00-banding-pesaing`) — semua lulus, tidak ada penyimpangan dari `SKILL.md`.
- 18/18 unit test bawaan (`tests/uji_regresi.py`) lulus.
- `python3 scripts/validate.py --skill dasbor-lokal` → lulus.
- 6/6 canned query diverifikasi manual (dihitung ulang dari data mentah, bukan hanya
  dibandingkan dengan JSON) — semua angka cocok persis. Rincian di `01-...md`.
- **Immutable & localhost dibuktikan, bukan diasumsikan:**
  - Hash SHA-256 `kas.db`/`stok.db` identik sebelum dan sesudah menjalankan Datasette dan
    mencoba `INSERT`/`DELETE` langsung lewat koneksi `?mode=ro` skill.
  - `INSERT`/`DELETE` lewat koneksi `?mode=ro` skill → `attempt to write a readonly
    database`.
  - `INSERT` lewat endpoint SQL Datasette → ditolak Datasette sendiri (`Statement must be a
    SELECT`, HTTP 400).
  - Datasette yang dijalankan dengan `--host 127.0.0.1` **tidak bisa** dihubungi dari IP
    LAN kontainer (`192.0.2.2:8123` → connection refused), hanya dari `127.0.0.1`.
  - `cetak_perintah_datasette()` di `scripts/dasbor.py` hardcode `--host 127.0.0.1`; tidak
    ada flag/jalur untuk menghasilkan `0.0.0.0`.
- Database tidak ada / 0 byte / rusak (garbage bytes) → pesan galat jelas bahasa awam,
  menyebut path & solusi, kode keluar 1, tidak ada traceback. Detail di `04-...md`.
- Permintaan di luar cakupan (buka ke internet, ubah data lewat dasbor) → ditolak dengan
  alasan sesuai `SKILL.md`, dan pagar teknisnya nyata (bukan cuma janji dokumentasi).
  Detail di `05-...md`.
- A/B (`00-pembanding-tanpa-skill`): skill memberi nilai tambah jelas (lokasi & skema 6 db
  otomatis diketahui, format Rupiah konsisten, pagar read-only/localhost yang tidak bisa
  diandalkan dari agent umum yang menulis SQL bebas).
- Banding pesaing (`00-banding-pesaing`): kandidat generik (`0xterrybit/database`,
  `gitgoodordietrying/sql-toolkit`, dll di openclaw/skills) lebih luas cakupan DB-nya tapi
  tidak tahu skema 6 alat Komunitech, dan beberapa justru menonjolkan kemampuan tulis
  (migrasi/backup) — tidak ada jaminan read-only/localhost bawaan seperti `dasbor-lokal`.

## Skor kualitas: 9/10
**Alasan:** semua canned query benar (diverifikasi manual independen), pagar keamanan
(immutable + localhost) terbukti nyata lewat pengujian teknis (bukan hanya baca dokumentasi),
penanganan error jelas dan ramah pengguna awam, dan skill unggul jelas baik vs "tanpa skill"
maupun vs kandidat pesaing generik. Tidak diberi 10 karena: (1) belum ada uji skenario
"database is locked" (proses lain menulis bersamaan) — disebut di `SKILL.md` tapi tidak
sempat diuji nyata oleh Akun B; (2) instalasi Datasette Windows/Mac di `docs/
panduan-datasette.md` sendiri sudah mengaku "belum dicoba langsung" — bukan salah skill ini,
tapi membatasi cakupan bukti lintas-OS.

## Temuan berprioritas

**Sedang**
1. **Belum diuji: `database is locked`.** `SKILL.md` menjanjikan pesan "data aman, coba
   lagi sebentar" saat DB dipakai program lain, tapi Akun B tidak sempat mensimulasikan
   koneksi penulis bersamaan untuk memicu `sqlite3.OperationalError: database is locked`
   secara nyata. Rekomendasi: uji ini di sesi berikutnya (buka koneksi tulis dari script
   lain, tahan transaksi, lalu jalankan `dasbor.py query`).

**Rendah**
2. **`stok` dan `stok_min` tampil sebagai `3.0`/`20.0` (float) di mode teks**, bukan `3`/`20`
   — data aslinya integer di skema `buku-stok`. Tidak salah (SQLite bertipe dinamis, dan
   ini bukan kolom uang jadi tidak masuk `KOLOM_UANG`), tapi kurang rapi untuk pembeli awam
   yang mengharapkan angka bulat untuk stok barang. Rekomendasi kosmetik: bulatkan tampilan
   kolom non-uang yang bernilai integer utuh.
3. Panduan `docs/panduan-datasette.md` sendiri mencatat langkah Windows/Mac "belum dicoba
   langsung" — konsisten dengan `platform_teruji` yang seharusnya hanya mencantumkan
   platform yang benar-benar diuji manusia (di luar cakupan pengujian agent ini).

## Berkas pendukung
`00-pembanding-tanpa-skill-uji-akun-b.md`, `00-banding-pesaing-uji-akun-b.md`,
`01-normal-cari-dan-enam-query-uji-akun-b.md`, `02-normal-json-dan-db-override-uji-akun-b.md`,
`03-normal-datasette-browser-uji-akun-b.md`, `04-input-tidak-lengkap-uji-akun-b.md`,
`05-luar-cakupan-keamanan-uji-akun-b.md` (semua di folder ini).

---

## Uji ulang v1.0.1 (2026-09-28)

Penguji independen, scratchpad terpisah, tidak mengubah `scripts/`/`SKILL.md`. DB SQLite tiruan
dibuat manual (tabel `produk` gaya `buku-stok`) untuk menguji `fmt_nilai` secara terisolasi.

- **Stok integer tampil tanpa `.0`**: kolom `stok` bernilai `25.0` (float REAL SQLite) tampil sebagai
  `25` di mode teks (`query buku-stok stok-menipis`), dan kolom `stok` bernilai `5.5` tetap tampil
  `5.5` apa adanya — dikonfirmasi lewat query nyata terhadap DB tiruan (tabel berisi 1 baris integer,
  1 baris pecahan) dan lewat pemanggilan langsung `fmt_nilai("stok", 25.0)` → `"25"`,
  `fmt_nilai("stok", 5.5)` → `"5.5"`. Menutup temuan RENDAH dari uji U18.
- **Kolom Rupiah tidak terpengaruh**: `fmt_nilai("total_penjualan", 150000.0)` → `"Rp 150.000"` —
  pengecekan `kolom in KOLOM_UANG` terjadi **sebelum** logika pembulatan tampilan integer, jadi
  kolom uang bulat tidak pernah lolos ke jalur `str(int(nilai))` tanpa prefiks "Rp" dan pemisah ribuan.
  Tidak ada regresi pada format Rupiah.
- `tests/uji_regresi.py`: **22/22 lulus**, tanpa regresi.

**Skor: 9/10.** Perbaikan tampilan stok integer di v1.0.1 terverifikasi benar, dan kolom Rupiah
terbukti tidak terpengaruh (jalur kode terpisah). Tidak ada temuan baru. Skor dipertahankan sama
seperti uji U18 sebelumnya (9/10) — satu-satunya temuan RENDAH dari sesi itu kini tertutup.
