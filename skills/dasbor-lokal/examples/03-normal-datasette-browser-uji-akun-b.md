# 03 — Normal: buka dasbor interaktif via Datasette (uji independen Akun B)

## Persiapan
Datasette 0.65.5 dipasang **di virtualenv scratchpad terpisah** (`venv/bin/pip install
datasette`), bukan ke Python sistem — sesuai instruksi `docs/panduan-datasette.md` §2.1/2.2
(walau di sini pakai `pip` langsung di venv, bukan `pipx`, karena venv sudah mengisolasi).

## Perintah
```
python3 scripts/dasbor.py datasette
```
→ Karena `datasette` belum ada di PATH shell uji (hanya ada di `venv/bin`), skill dengan
benar mendeteksi belum terpasang dan mencetak instruksi pasang (`pipx install datasette`)
**plus** tetap mencetak perintah lengkap yang disarankan (6x `-i PATH`, `-m
templates/metadata.yml`, `--host 127.0.0.1`) — sesuai `SKILL.md` §C.

Perintah itu lalu dijalankan manual dengan `venv/bin/datasette` (mensimulasikan pengguna
yang sudah memasang):
```
venv/bin/datasette -i stok.db -i kasir.db -i crm.db -i absensi.db -i piutang.db -i kas.db \
  -m templates/metadata.yml --host 127.0.0.1 -p 8123
```

## Hasil
- Server menyala di `http://127.0.0.1:8123` saja (log Uvicorn mengonfirmasi host).
- Canned query `kas/saldo_per_akun.json` di Datasette browser mengembalikan Bank BCA
  Rp1.700.000, Laci kas Rp1.700.000, QRIS Rp800.000 — **identik** dengan hasil
  `scripts/dasbor.py query kas-umkm saldo-per-akun` di skenario 01.
- `templates/metadata.yml` termuat dengan benar (canned query tampil & bisa dijalankan).

## Kesimpulan
Alur Datasette bekerja end-to-end dan hasilnya konsisten dengan jalur `dasbor.py query`
tanpa Datasette, seperti dijanjikan skill. Detail keamanan (localhost-only, immutable)
diuji terpisah di skenario 05.
