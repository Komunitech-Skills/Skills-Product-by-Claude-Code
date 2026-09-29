# 04 — Input tidak lengkap: database tidak ada / 0 byte / rusak (uji independen Akun B)

## Skenario A — Database belum pernah dibuat (alat belum pernah dipakai)
```
KOMUNITECH_KAS_DB=/tmp/tidak-ada-di-manapun/kas.db python3 scripts/dasbor.py query kas-umkm saldo-per-akun
```
→ `GAGAL: Database tidak ditemukan di /tmp/tidak-ada-di-manapun/kas.db. Pastikan alat itu
sudah pernah dipakai (ada datanya), atau tunjukkan lokasinya dengan --db PATH. Lihat
docs/panduan-datasette.md.` Kode keluar 1. Pesan sesuai `SKILL.md` (bukan galat fatal,
menyebut path & solusi).

## Skenario B — File 0 byte
```
touch kosong.db
python3 scripts/dasbor.py query buku-stok stok-menipis --db kosong.db
```
→ `GAGAL: File .../kosong.db kosong (0 byte), bukan database yang bisa dibaca.` Kode 1.

## Skenario C — File rusak (bukan SQLite)
```
head -c 200 /dev/urandom > rusak.db
python3 scripts/dasbor.py query buku-stok stok-menipis --db rusak.db
```
→ `GAGAL: File .../rusak.db bukan database SQLite yang valid atau rusak (file is not a
database).` Kode 1.

## Kesimpulan
Ketiga bentuk "input tidak lengkap/rusak" ditangani dengan pesan jelas dalam bahasa awam,
menyebut penyebab dan solusi (pakai `--db PATH` lain, atau pakai alat itu dulu), tidak ada
traceback Python yang membingungkan pengguna awam, dan kode keluar konsisten (1). Sesuai
`SKILL.md` bagian "Batasan & Penanganan Error".
