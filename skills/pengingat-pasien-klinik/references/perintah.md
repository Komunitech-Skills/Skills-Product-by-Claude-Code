# Rincian perintah `scripts/pengingat_pasien.py`

Semua perintah menerima `--json` untuk keluaran JSON, dan `--file PATH` untuk lokasi CSV lain
(default `pasien/DAFTAR.csv`). Opsi umum ini (juga `--hari-ini`, `--tz`) boleh ditulis sebelum
atau sesudah nama perintah: `pengingat_pasien.py --json daftar` = `pengingat_pasien.py daftar --json`. `--hari-ini` (format bebas) dan `--tz`
(default `Asia/Jakarta`) berguna untuk pengujian.

## tambah
```
tambah --nama "Bu Sari" --wa "0812-0000-1111" --jenis kontrol --tanggal "10 Okt" \
       --persetujuan ya [--catatan "..."]
```
Semua opsi wajib kecuali `--catatan`. Ditolak (kode 1) bila `jenis`/`catatan` menyerupai
diagnosis, atau (kode 2) bila `nama`/`catatan` berisi nomor HP/email/NIK pihak lain.

## ubah
```
ubah --id 3 [--nama ..] [--wa ..] [--jenis ..] [--tanggal ..] [--catatan ..] [--persetujuan ya|tidak]
```
Hanya kolom yang disebut yang diubah.

## ubah-status
```
ubah-status --id 3 --status dijadwalkan|sudah-diingatkan|datang|batal [--berikutnya ..] [--alasan ..]
```
- `sudah-diingatkan`: mencatat tanggal staf sudah mengirim draf hari itu.
- `datang` + `--berikutnya "3 bulan lagi"`: jadwal baru dibuat, status kembali `dijadwalkan`.
  `datang` tanpa `--berikutnya`: kunjungan dianggap selesai, berhenti muncul di `daftar`.
- `batal` [+ `--alasan`]: berhenti muncul di `daftar`; alasan (bila ada, non-diagnosis) dicatat.

## hapus
```
hapus --id 3            # atau
hapus --wa 0812-0000-1111
```
Tanpa `--ya`: pratinjau (daftar yang akan terhapus). Dengan `--ya`: hapus permanen. Pakai ini
segera saat pasien meminta datanya dihapus (UU PDP 27/2022).

## impor
```
impor daftar.csv [--jenis-default kontrol] [--tanggal-default "10 Okt"] [--persetujuan-default ya|tidak] [--ya]
```
Kolom yang dikenali: `nama`/`nama_panggilan`/`pasien`, `wa`/`no wa`/`nomor`/`hp`/`whatsapp`,
`jenis`/`jenis_kunjungan`/`keperluan`, `tanggal`/`tgl`/`jadwal`/`tanggal_berikutnya`,
`persetujuan`/`setuju`/`consent`. Tanpa `--ya`: pratinjau saja, file tidak diubah. File tanpa
kolom persetujuan **wajib** disertai `--persetujuan-default` — tanyakan dulu ke pengguna.

## daftar
```
daftar [--kapan terlambat|hari-ini|besok|h-1|h-3|minggu-ini|semua] [--tanpa-draf] [--klinik "Nama Klinik"]
```
Tanpa `--kapan`: TERLAMBAT + HARI INI + BESOK (H-1) + H-3 sekaligus, plus draf pesan (maks. 15,
sisanya lewat `draf --id`). Hanya menampilkan pasien berstatus aktif (`dijadwalkan` /
`sudah-diingatkan`) **dan** `persetujuan: ya`.

## draf
```
draf --id 3 [--klinik "Nama Klinik"]
```
Draf untuk satu pasien. Ditolak (kode 1) bila persetujuan pasien itu bukan `ya`.

## ringkasan
```
ringkasan [--samarkan] [--tanpa-nama]
```
Jumlah per kategori (TERLAMBAT/HARI INI/BESOK/H-3) + total aktif. `--samarkan` mengubah nama jadi
inisial (mis. "Bu Sari" -> "Bu S."). `--tanpa-nama` menyembunyikan daftar nama sama sekali, hanya
angka. **Tidak pernah** memuat nomor WA, dengan atau tanpa opsi ini.

## info
```
info
```
Path file dan jumlah baris per status. Berguna untuk memeriksa lokasi database yang sedang dipakai.

## Kode keluar
0 = berhasil. 1 = input/perintah salah, pesan di `error`/stderr diawali `ERROR:`. 2 = ditolak
karena berisi data pribadi pihak lain (nomor HP/email/NIK) di kolom yang bukan untuk itu.
