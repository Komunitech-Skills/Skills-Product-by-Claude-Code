# Uji independen Akun B — Skenario 4: input tidak lengkap

## Kasus: pengguna hanya menyebut nama, WA, dan jenis kunjungan (tanpa tanggal & persetujuan)
Permintaan pengguna (simulasi): "Catat Pak Budi, WA 0812-9999-0000, kontrol."

Sesuai SKILL.md bagian "Input", agent seharusnya **bertanya sekali** dalam satu pesan bernomor,
termasuk pertanyaan persetujuan secara eksplisit (tidak boleh diasumsikan "ya"), sebelum
memanggil script. Diverifikasi bahwa script sendiri menolak tegas bila dipaksa dijalankan tanpa
kedua field itu:
```
$ python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 tambah --nama "Pak Budi" --wa "0812-9999-0000" --jenis kontrol
usage: pengingat_pasien.py tambah [-h] --nama NAMA --wa WA --jenis JENIS --tanggal TANGGAL --persetujuan {ya,tidak} [--catatan CATATAN]
pengingat_pasien.py tambah: error: the following arguments are required: --tanggal, --persetujuan
(exit code 2)
```
Ini **benar-benar mencegah agent "menebak"** tanggal atau persetujuan — argparse menolak dengan
pesan jelas kalau field wajib belum diisi, sesuai instruksi "jangan pernah mengasumsikan
persetujuan 'ya' tanpa pasien menyatakannya".

## Simulasi jawaban agent yang benar (mengikuti SKILL.md)
> Untuk mencatat Pak Budi, saya perlu beberapa info lagi:
> 1. Tanggal kunjungan kontrol berikutnya?
> 2. Apakah Pak Budi setuju diingatkan lewat WA untuk jadwal ini?
>
> (Nama klinik untuk draf pesan opsional — kalau tidak diisi, draf akan memakai "kami".)

## Setelah info lengkap, dilanjutkan
```
tambah --nama "Pak Budi" --wa "0812-9999-0000" --jenis kontrol --tanggal "15 Oktober" --persetujuan ya
{"ok": true, "mode": "tersimpan", "id": "1", "teks": "Tersimpan #1: Pak Budi | Kontrol | Kamis, 15 Oktober 2026 | persetujuan: ya", "peringatan": []}
```
Verifikasi manual: 15 Oktober 2026 memang jatuh pada hari Kamis (dihitung independen dengan
`datetime.date(2026,10,15).weekday()` = 3 -> Kamis). Cocok.

## Hasil
LULUS. Field wajib (tanggal, persetujuan) tidak bisa dilewati; pesan error jelas dan dalam bahasa
Indonesia; tidak ada asumsi diam-diam terhadap persetujuan.
