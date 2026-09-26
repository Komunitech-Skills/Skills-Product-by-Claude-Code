# Contoh 5 — Impor daftar pasien dari CSV (data fiktif)

File `templates/impor-contoh.csv`:
```
nama,wa,jenis,tanggal,persetujuan
Bu Wati,0812-1111-0001,kontrol,10/10/2026,ya
Pak Joko,0812-1111-0002,vaksin,15/10/2026,ya
Kucing Oyen,0812-1111-0003,vaksin hewan,20/10/2026,tidak
```

## Input pengguna
> "Impor daftar pasien ini." (mengunggah/menempel file di atas)

## Perintah (pratinjau dulu, tanpa `--ya`)
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 \
  impor templates/impor-contoh.csv
```
```
Pratinjau impor templates/impor-contoh.csv: 3 pasien akan ditambahkan, 0 baris ditolak.
Bu Wati | Kontrol | 2026-10-10 | setuju:ya
Pak Joko | Vaksin | 2026-10-15 | setuju:ya
Kucing Oyen | Vaksin hewan | 2026-10-20 | setuju:tidak
Ulangi perintah yang sama + --ya untuk menyimpan.
```
Agent menunjukkan pratinjau ini ke pengguna dan menunggu persetujuan sebelum melanjutkan.

## Setelah pengguna setuju
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 \
  impor templates/impor-contoh.csv --ya
```
```
Impor selesai: 3 pasien ditambahkan, 0 baris ditolak.
```
Kucing Oyen (persetujuan "tidak") tersimpan tapi tidak akan muncul di `daftar`/`draf`/`ringkasan`.

## File tanpa kolom persetujuan (ditolak sampai ditegaskan)
Jika file impor tidak punya kolom persetujuan sama sekali, script menolak dan meminta
`--persetujuan-default` supaya persetujuan tidak pernah diasumsikan begitu saja:
```
ERROR: file tidak punya kolom persetujuan, dan --persetujuan-default belum diisi. Wajib
menegaskan persetujuan pasien dihubungi (ya/tidak) sebelum impor.
```
Agent harus bertanya ke pengguna: "Apakah semua pasien di file ini sudah pernah menyatakan
setuju dihubungi lewat WA?" sebelum menambahkan `--persetujuan-default ya` (atau `tidak`).
