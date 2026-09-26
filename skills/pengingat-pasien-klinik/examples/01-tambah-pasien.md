# Contoh 1 — Mencatat pasien baru (data fiktif)

Hari ini: Sabtu, 26 September 2026.

## Input pengguna
> "Catat Bu Sari, kontrol gigi lagi 10 hari lagi, WA 0812-0000-1111. Dia bilang boleh diingatkan."

## Perintah
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv \
  tambah --nama "Bu Sari" --wa "0812-0000-1111" --jenis "kontrol gigi" \
  --tanggal "10 hari lagi" --persetujuan ya
```

## Output
```
Tersimpan #1: Bu Sari | Kontrol gigi | 6 Okt 2026 | persetujuan: ya
```

## Input pengguna (klinik hewan)
> "Ada pasien vaksin, kucing Mimi punya Bu Wati, WA 0812-9999-8888, vaksin hari ini, setuju diingatkan."

## Perintah
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv \
  tambah --nama "Kucing Mimi" --wa "0812-9999-8888" --jenis "vaksin hewan" \
  --tanggal "hari ini" --persetujuan ya
```

## Output
```
Tersimpan #3: Kucing Mimi | Vaksin hewan | 26 Sep 2026 | persetujuan: ya
```

## Input pengguna (pasien belum setuju dihubungi)
> "Catat Bu Wati juga, kontrol besok, WA 0812-4444-5555, tapi dia belum bilang setuju diingatkan atau tidak."

Agent seharusnya **bertanya dulu** ke pengguna: "Apakah Bu Wati sudah menyatakan setuju
dihubungi lewat WA untuk pengingat ini?" Jika pengguna menjawab "belum, catat saja dulu tapi
jangan diingatkan":
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv \
  tambah --nama "Bu Wati" --wa "0812-4444-5555" --jenis kontrol --tanggal besok --persetujuan tidak
```
```
Tersimpan #4: Bu Wati | Kontrol | 27 Sep 2026 | persetujuan: tidak
Catatan: Persetujuan 'tidak': pasien ini TIDAK akan muncul di daftar pengingat/draf/ringkasan
sampai persetujuannya diubah menjadi 'ya' ...
```

## Input pengguna (ditolak — menyebut diagnosis)
> "Catat Pak Anto, kontrol kanker, WA 0812-7777-6666, besok, setuju diingatkan."

Script menolak karena `jenis` menyerupai diagnosis (kode keluar 1):
```
ERROR: 'jenis kunjungan' berisi kata yang menyerupai diagnosis/nama penyakit ('kanker'). Skill
ini HANYA menyimpan jenis kunjungan umum (kontrol, vaksin, cabut jahitan, cek gigi, vaksin hewan,
groom, sunat, medical check up, dll), TANPA diagnosis atau rekam medis. Tulis ulang tanpa nama
penyakit.
```
Agent seharusnya meminta pengguna menyebut jenis kunjungan saja, mis. "kontrol" atau "kontrol
rutin", tanpa nama penyakit.
