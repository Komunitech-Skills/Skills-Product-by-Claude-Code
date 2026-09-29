# 00 — Banding pesaing (uji independen Akun B)

## Pencarian
Kata kunci: "sqlite dashboard skill claude agent read-only", "ClawHub skills.sh local data
explorer sqlite dashboard skill", via web search 2026-09-26.

## Kandidat yang ditemukan (dibaca untuk dinilai, tidak disalin)
- **`0xterrybit/database`** (openclaw/skills) — "database explorer" generik: konek ke
  PostgreSQL/MySQL/SQLite/MongoDB/Redis, jalankan query bebas, inspeksi skema, ekspor data.
- **`gitgoodordietrying/sql-toolkit`** (openclaw/skills) — desain skema, migrasi, indexing,
  backup/restore, debug query lambat, lintas SQLite/PostgreSQL/MySQL.
- **`ivangdavila/sqlite`** (openclaw/skills) — dasar-dasar SQLite umum.
- Skill Datasette generik disebut di hasil pencarian umum, tapi hanya membungkus perintah
  `datasette` biasa tanpa pengetahuan skema alat tertentu.

## Penilaian berdampingan (skenario: "lihat semua data usaha dari satu tempat")
| Aspek | Pesaing (db-explorer generik) | `dasbor-lokal` (Komunitech) |
|---|---|---|
| Tahu lokasi 6 database Komunitech | Tidak — harus ditanyakan/ditebak | Ya, otomatis (`cari`), prioritas `--db`>ENV alat>ENV bersama>default |
| Tahu skema & pertanyaan bisnis relevan (stok menipis, piutang lewat tempo, dst.) | Tidak — user/agent harus menulis SQL sendiri | Ya, 6 canned query siap pakai, sudah teruji |
| Default read-only dipaksa di level driver | Bergantung skill; banyak db-explorer generik justru menonjolkan kemampuan tulis (migrasi, backup/restore) | Ya, `?mode=ro` selalu, tidak bisa dimatikan |
| Localhost-only saat dibuka di browser | Tidak dibahas / tidak dijamin | Ya, `--host 127.0.0.1` wajib, dilarang `0.0.0.0`/tunnel |
| Fallback tanpa instalasi tambahan | Umumnya butuh driver DB / instalasi | Ya, `scripts/dasbor.py` Python standar saja |
| Bahasa & format Rupiah Indonesia | Tidak | Ya |

## Kesimpulan
Kandidat generik lebih luas cakupannya (banyak jenis DB) tapi **lebih berisiko** (mengajak
tulis/migrasi) dan tidak tahu apa-apa soal skema 6 alat Komunitech — user/agent tetap harus
menulis SQL sendiri, dan tidak ada jaminan read-only/localhost bawaan. `dasbor-lokal` unggul
untuk kasus penggunanya (pemilik UMKM awam yang sudah pakai alat Komunitech): instan, aman
by design, dan hasilnya sudah diverifikasi benar. Tidak ada kandidat yang secara khusus untuk
mengintegrasikan enam alat Komunitech ini, jadi perbandingan bersifat kapabilitas umum, bukan
tiru langsung.
