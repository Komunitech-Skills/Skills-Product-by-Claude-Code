# Skenario 04 (uji Akun B) — Input tidak lengkap

**Penguji:** Akun B, kernel tiruan `127.0.0.1:16806`.

## Kasus A: `buat` tanpa `--path`
```
$ python3 scripts/siyuan.py ... buat --notebook 20260101000002-konsulbx --md "isi tanpa path"
usage: siyuan.py buat [-h] --notebook NOTEBOOK --path PATH [...]
siyuan.py buat: error: the following arguments are required: --path
```
Kode keluar **2**. Pesan argparse standar (Inggris teknis) — agent yang memanggil harus
menerjemahkan ke bahasa awam sesuai SKILL.md §Batasan ("argumen kurang/salah → tanyakan sekali
semua yang kurang"); skill sendiri tidak menerjemahkan pesan ini, tapi ini konsisten dengan desain
CLI standar dan sudah diantisipasi tabel error di SKILL.md.

## Kasus B: `cari` dengan kata kunci kosong
```
$ python3 scripts/siyuan.py ... cari ""
GAGAL: Kata kunci pencarian tidak boleh kosong.
```
Kode keluar **2**, pesan Bahasa Indonesia jelas — lebih baik dari Kasus A karena ditangani eksplisit
di kode (`p_cari`), bukan hanya lewat argparse.

## Kesimpulan
Kedua kasus ditangani dengan aman (tidak ada permintaan setengah jalan terkirim ke kernel, tidak ada
crash/traceback Python). Temuan minor: pesan error argparse (Kasus A) berbahasa Inggris teknis,
tidak konsisten dengan pesan `Gagal` kustom lain yang berbahasa Indonesia — lihat HASIL-UJI.md.
