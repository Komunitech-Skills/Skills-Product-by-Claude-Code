# Contoh 2 - Rekap bulanan dan cek nota dobel

Lanjutan dari Contoh 1 (dua nota sudah diarsipkan: Rp 150.000 & Rp 50.000, bulan September 2026).

## Rekap

**Pengguna:** "Rekap pengeluaran nota bulan September dong."

```bash
python3 scripts/arsip.py rekap --bulan 09/2026 --json
```
```json
{
  "ok": true, "mode": "baca", "periode": "bulan", "dari": "2026-09-01", "sampai": "2026-09-30",
  "jumlah_nota": 2, "total_nominal": 200000,
  "per_kategori": [
    {"kategori": "bahan-baku", "jumlah": 1, "total": 150000},
    {"kategori": "peralatan", "jumlah": 1, "total": 50000}
  ],
  "per_vendor_teratas": [
    {"vendor": "Toko Sembako Bu Yati", "jumlah": 1, "total": 150000},
    {"vendor": "Toko C Elektronik", "jumlah": 1, "total": 50000}
  ]
}
```

**Agent:**
> REKAP NOTA (01/09/2026 - 30/09/2026)
> Jumlah nota: 2 | Total: Rp 200.000
>
> Per kategori:
> - Bahan baku: 1 nota, Rp 150.000
> - Peralatan: 1 nota, Rp 50.000
>
> Vendor teratas:
> - Toko Sembako Bu Yati: 1 nota, Rp 150.000
> - Toko C Elektronik: 1 nota, Rp 50.000

## Cek nota dobel (mengarsipkan foto yang sama persis dua kali)

**Pengguna:** "Saya foto ulang nota Toko Sembako Bu Yati karena buram, tolong arsipkan lagi ya, sama filenya."

```bash
python3 scripts/arsip.py tambah --file "in/IMG_20260920_1.jpg" --tanggal 20/09/2026 \
  --vendor "Toko Sembako Bu Yati" --nominal 150000 --json
```
```json
{
  "ok": true, "mode": "pratinjau",
  "perlu_izin": ["izinkan_duplikat"],
  "duplikat": {"id": 1, "tanggal": "2026-09-20", "vendor": "Toko Sembako Bu Yati", "nominal": 150000,
               "path_file": "data/arsip/2026/09/2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg"},
  "hash_sha256": "08bed2ae3b52fc9fa213bfb69c23751941bb298a2e886057f9215aaba44f70f3"
}
```

**Agent:**
> File ini isinya SAMA PERSIS dengan nota yang sudah diarsipkan (ID 1, 20/09/2026, Toko Sembako Bu Yati,
> Rp 150.000). Ini file foto yang sama dengan yang lama (bukan foto baru yang berbeda), jadi tidak perlu
> diarsipkan lagi — nota yang sudah ada sudah cukup. Kalau Anda memang punya foto ulang dengan file **berbeda**
> (bukan file yang persis sama), kirim file itu dan saya arsipkan sebagai nota baru.

## Perintah `duplikat` (pengecekan menyeluruh)

```bash
python3 scripts/arsip.py duplikat --json
```
```json
{"ok": true, "mode": "baca", "file_sama_persis": [], "kemungkinan_dobel": []}
```
(Belum ada duplikat karena percobaan di atas dihentikan sebelum `--ya`.) Bila pengguna tetap memaksa dengan
`--izinkan-duplikat --ya`, ID nota baru akan muncul di `file_sama_persis` pada pemanggilan `duplikat` berikutnya.

## Ekspor ke kas-umkm

**Pengguna:** "Masukin nota-nota September ini ke buku kas saya."

```bash
python3 scripts/arsip.py ekspor --bulan 09/2026 --csv nota-09-2026.csv --json
```
```json
{"ok": true, "mode": "baca", "jumlah": 2, "total_nominal": 200000, "file_csv": "nota-09-2026.csv",
 "dari": "2026-09-01", "sampai": "2026-09-30"}
```
Isi `nota-09-2026.csv`:
```csv
Tanggal;Keterangan;Masuk;Keluar;Kategori
20/09/2026;Toko Sembako Bu Yati;;150000;beli-stok
22/09/2026;Toko C Elektronik - beli kabel;;50000;beli-stok
```

**Agent:** "File `nota-09-2026.csv` sudah dibuat. Untuk memasukkannya ke buku kas, jalankan (dari folder skill
kas-umkm): `python3 scripts/kas.py impor "nota-09-2026.csv" --jenis-file buku-kas` — nanti akan ada pratinjau lagi
sebelum tersimpan di sana."
