# Contoh 3 — Ubah status, jadwal ulang, dan batal (data fiktif)

Melanjutkan dari contoh sebelumnya.

## Sudah diingatkan
> "Sudah aku kirim pesannya ke Pak Budi."
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 \
  ubah-status --id 2 --status sudah-diingatkan
```
```
#2 Pak Budi: status -> sudah-diingatkan
```

## Pasien datang, dijadwalkan ulang untuk vaksin berikutnya
> "Kucing Mimi sudah datang vaksin. Jadwalkan lagi 1 bulan lagi."
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 \
  ubah-status --id 3 --status datang --berikutnya "1 bulan lagi"
```
```
#3 Kucing Mimi: status -> dijadwalkan | jadwal berikutnya 26 Okt 2026
```
Baris di CSV otomatis diperbarui: tanggal menjadi 2026-10-26, status kembali `dijadwalkan`, dan
catatan mencantumkan "kunjungan sebelumnya 26 Sep 2026 selesai" (tanpa detail medis apa pun).

## Pasien batal
> "Bu Sari batal, katanya pindah kota."
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 \
  ubah-status --id 1 --status batal --alasan "pindah kota"
```
```
#1 Bu Sari: status -> batal
```
Bu Sari tidak lagi muncul di `daftar` setelah ini.

## Salah ketik nomor WA, dikoreksi
> "Nomor WA Pak Budi salah, yang benar 0813-2222-4444."
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 \
  ubah --id 2 --wa "0813-2222-4444"
```
```
Diubah #2: Pak Budi | Vaksin | 27 Sep 2026
```
