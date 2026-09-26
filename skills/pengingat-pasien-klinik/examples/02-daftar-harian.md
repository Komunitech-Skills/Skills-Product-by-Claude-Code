# Contoh 2 — Daftar harian + draf pesan (data fiktif)

Melanjutkan dari `01-tambah-pasien.md`, dengan tambahan pasien:
```bash
tambah --nama "Pak Budi" --wa "0813-2222-3333" --jenis vaksin --tanggal "besok" --persetujuan ya
```

## Input pengguna
> "Siapa yang harus diingatkan hari ini?"

## Perintah
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 daftar
```

## Output
```
HARI INI (1)
  #3 Kucing Mimi | Vaksin hewan | 26 Sep 2026 | 0812-9999-8888
BESOK (H-1) (1)
  #2 Pak Budi | Vaksin | 27 Sep 2026 | 0813-2222-3333

DRAF PESAN (salin & kirim sendiri, JANGAN dikirim otomatis):

#3 Kucing Mimi (0812-9999-8888):
Halo Kucing Mimi, ini pengingat dari kami untuk jadwal vaksin hewan Anda pada 26 Sep 2026. Mohon
konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.

#2 Pak Budi (0813-2222-3333):
Halo Pak Budi, ini pengingat dari kami untuk jadwal vaksin Anda pada 27 Sep 2026. Mohon
konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.
```

Agent menyampaikan hasil ini apa adanya, ditambah pengingat: **"Ini draf untuk disalin dan
dikirim sendiri oleh staf, bukan kiriman otomatis."** Pasien #4 (Bu Wati, persetujuan "tidak")
sengaja tidak muncul di daftar ini.

## Input pengguna — hanya satu kategori
> "Ada yang H-3?"

```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 daftar --kapan h-3
```
```
Tidak ada jadwal pada kategori ini.
```

## Input pengguna — draf satu pasien saja, dengan nama klinik
> "Bikinin draf buat Pak Budi, atas nama Klinik Sehat Bahagia."

```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv draf --id 2 --klinik "Klinik Sehat Bahagia"
```
```
Halo Pak Budi, ini pengingat dari Klinik Sehat Bahagia untuk jadwal vaksin Anda pada 27 Sep 2026.
Mohon konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.
```
