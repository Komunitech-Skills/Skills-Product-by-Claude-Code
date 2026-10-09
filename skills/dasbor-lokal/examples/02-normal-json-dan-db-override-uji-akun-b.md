# 02 — Normal: mode `--json` dan `--db PATH` (uji independen Akun B)

## Perintah
```
python3 scripts/dasbor.py query kas-umkm saldo-per-akun --json
python3 scripts/dasbor.py query buku-stok stok-menipis --db "<path-scratchpad>/stok.db"
```

## Hasil
- `--json` menghasilkan objek `{"ok": true, "alat", "query", "judul", "db", "parameter",
  "jumlah_baris", "baris": [...]}` persis sesuai `SKILL.md`. Kolom uang (`saldo`) tetap
  angka mentah (`1700000`), bukan string "Rp 1.700.000" — sesuai janji "pembulatan tampilan
  hanya di mode teks".
- `--db PATH` menimpa lokasi default/ENV dengan sukses: query `stok-menipis` menunjuk
  langsung ke file di scratchpad (bukan `~/KomunitechData/stok.db`) dan hasilnya identik
  dengan menjalankan lewat ENV `KOMUNITECH_STOK_DB`.

## Verifikasi
`jumlah_baris` pada JSON (3 untuk saldo-per-akun) cocok dengan jumlah objek di `baris`, dan
angka saldo cocok dengan perhitungan manual di skenario 01.

## Kesimpulan
Kedua fitur bekerja sesuai dokumentasi. Tidak ada perbedaan hasil antara mode teks dan JSON
selain format tampilan angka uang, seperti yang dijanjikan.
