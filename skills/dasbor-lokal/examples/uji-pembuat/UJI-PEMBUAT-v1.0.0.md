# UJI PEMBUAT — dasbor-lokal v1.0.0 (status: draft)

- **Tanggal:** 2026-09-26
- **Penguji:** **pembuat skill** (belum ada penguji independen, belum ada uji A/B & banding pesaing, belum uji platform asli oleh manusia). Karena itu **belum diberi skor kualitas** dan status tetap `draft`.
- **Lingkungan:** Linux (sandbox sesi), Python 3.11 (skill) + Python 3.11 venv terpisah untuk Datasette. Datasette **0.65.5** dipasang dari **PyPI resmi** ke virtualenv di scratchpad (`/tmp/.../scratchpad/datasette/venv`), **bukan** ke sistem.
- **Tidak diuji:** Windows/Mac sungguhan, `pipx install datasette` secara khusus (dipasang lewat `pip` di venv untuk kecepatan; `pipx` adalah anjuran resmi di dokumentasi Datasette dan disebut sebagai cara utama di `docs/panduan-datasette.md`), OpenClaw sungguhan, perilaku agent (skill dipanggil model).

## Ringkasan

| Uji | Hasil |
|---|---|
| Instal Datasette dari PyPI resmi ke virtualenv terpisah | **Lulus** — `datasette, version 0.65.5`, lisensi Apache-2.0 dikonfirmasi dari `pip show` + file `LICENSE` terpasang |
| Buat 6 database contoh dengan **menjalankan langsung script asli tiap skill** (`stok.py`, `kasir.py`, `crm.py`, `absensi.py`, `piutang.py`, `kas.py`) dengan data fiktif | **Lulus** — semua `init` + transaksi berhasil, dikonfirmasi lewat `--json` masing-masing skill |
| 6 canned query di `templates/metadata.yml` dijalankan lewat `datasette --immutable ... --get` | **Lulus**, hasil dicocokkan manual dengan data fiktif yang dimasukkan — lihat tabel di bawah |
| 6 canned query yang sama dijalankan lewat `scripts/dasbor.py query` (tanpa Datasette) | **Lulus**, hasil **identik** dengan Datasette |
| Database tidak berubah setelah dipakai Datasette maupun `dasbor.py` | **Lulus** — hash SHA-256 tiap file `.db` sama persis sebelum & sesudah |
| Datasette menolak SQL selain SELECT (`INSERT`) | **Lulus** — `{"ok": false, "error": "Statement must be a SELECT", "status": 400}` |
| `tests/uji_regresi.py` (18 skenario, database sintetis skema asli) | **18/18 OK** |
| `python3 scripts/validate.py --skill dasbor-lokal` | **Lulus** |
| `bash scripts/uji_openclaw.sh` | Lihat `examples/UJI-PLATFORM.md`/laporan sesi untuk hasil (dijalankan sekali dari root repo, hasil sama untuk semua skill termasuk `dasbor-lokal`) |
| Penanganan error: database tidak ada / 0 byte / rusak bukan-SQLite / alat & query tidak dikenal / tabel tidak ada (salah pasang alat) / database locked | **Lulus** — pesan Indonesia jelas, kode keluar 1, tidak ada traceback ke pengguna |

## Pencocokan hasil canned query dengan data fiktif (dihitung manual)

| Query | Data fiktif yang dimasukkan | Hasil query | Cocok? |
|---|---|---|---|
| `buku-stok / stok-menipis` | KPI-250 (stok 5, min 10), TEP-1KG (stok 2, min 8), GUL-1KG (stok 30, min 5, aman) | KPI-250 & TEP-1KG muncul, GUL-1KG tidak, TEP-1KG di atas (selisih paling besar: -6 vs -5) | ✅ |
| `kasir-lokal / penjualan-per-hari` | 24/09: 2 nota (36rb+15rb); 25/09: 1 nota (24rb); 26/09: 1 nota (18rb) | `2026-09-24: Rp 51.000 (2 nota)`, `2026-09-25: Rp 24.000 (1 nota)`, `2026-09-26: Rp 18.000 (1 nota)` | ✅ |
| `buku-piutang / piutang-jatuh-tempo` | Bu Tini (Rp1,2jt, jatuh tempo 05/09, belum bayar), Kafe Senja (Rp2,5jt, jatuh tempo 10/10, belum lewat), Warung Jaya (Rp800rb, jatuh tempo 15/09, belum bayar) | Bu Tini & Warung Jaya muncul (sisa sesuai nominal), Kafe Senja tidak (belum jatuh tempo) | ✅ |
| `absensi-lokal / kehadiran-harian` | Andi masuk 08.05/pulang 17.10, Sari masuk 08.20/pulang 17.00, tanggal 2026-09-25 | Jam masuk/pulang persis sama untuk tanggal itu | ✅ |
| `crm-wa / prospek-per-tahap` | baru(300rb), dihubungi(500rb), ditawar(1,2jt), deal(4,5jt) — 1 kontak/tahap | 4 baris, jumlah=1 tiap tahap, nilai sesuai | ✅ |
| `kas-umkm / saldo-per-akun` | Laci: +500rb -150rb; BCA (QRIS): +300rb | Laci Rp350.000, BCA Rp300.000 | ✅ |

## Bukti database tidak berubah (hash SHA-256)
```
$ find data -name "*.db" -exec sha256sum {} \; | sort -k2 > hash-sebelum.txt
... (jalankan Datasette --immutable untuk 6 canned query + 1 percobaan INSERT yang ditolak,
     lalu scripts/dasbor.py query untuk 6 alat) ...
$ find data -name "*.db" -exec sha256sum {} \; | sort -k2 > hash-sesudah.txt
$ diff hash-sebelum.txt hash-sesudah.txt && echo "TIDAK ADA PERUBAHAN"
TIDAK ADA PERUBAHAN
```
(File `.db` di sini adalah data fiktif hasil menjalankan skill asli — bukan disertakan di repo, hanya prosedurnya yang didokumentasikan di sini dan di `research/sources/datasette-2026-09-26.md`.)

## Audit keamanan (oleh pembuat)
- Hanya pustaka standar (`argparse`, `json`, `sqlite3`, `shutil`, `datetime`, `pathlib`). Tidak ada `subprocess`, `eval`, `exec`, akses jaringan, atau penulisan file apa pun.
- Semua koneksi database dibuka lewat URI `?mode=ro` (`sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True)`) — level driver menolak tulisan.
- Perintah Datasette yang disiapkan skill selalu memakai `-i`/`--immutable` per database dan `--host 127.0.0.1`; tidak pernah menyarankan `0.0.0.0`, port-forward, atau tunnel.
- Tidak ada API key/token/kredensial apa pun yang dipakai atau disimpan skill ini.
- SKILL.md diperiksa: tidak ada instruksi tersembunyi ke agent untuk mengabaikan pengguna, mengirim file, atau menonaktifkan konfirmasi.

## Yang belum diuji / catatan jujur untuk pemilik
- Belum ada penguji independen (Tahap 6.2 CLAUDE.md), uji A/B "tanpa skill vs dengan skill", dan uji banding pesaing — dilewati sesuai cakupan tugas sesi ini (fokus: kurasi Datasette + skill + uji instalasi nyata). Perlu dikerjakan sebelum naik ke status `uji`/`lulus`.
- Instalasi `pipx` (bukan `pip` biasa) belum dicoba langsung; kedua cara didokumentasikan resmi di `docs.datasette.io`.
- Belum diuji dengan Datasette versi lain, database besar (>~10rb baris), atau `KOMUNITECH_DATA` yang menunjuk folder jaringan (SMB/NFS) — mode `?mode=ro` seharusnya tetap aman tapi belum dicoba.
