# Skenario 03 — Dolibarr 22.0.4 (versi DoliWamp terbaru): cek, stok, tambah pelanggan (normal)

**Penguji:** pembuat skill (BUKAN penguji independen), 2026-09-24. Dolibarr **asli** 22.0.4 di container Linux (PHP 8.4, MariaDB 10.11), zona PHP Asia/Jakarta. Data fiktif.

## `cek` (kunci user khusus API, bukan admin)
```
CEK DOLIBARR
Alamat: http://127.0.0.1:8089/dolibarr
Versi Dolibarr: 22.0.4
Kunci API: ****cdef (dari ENV DOLIBARR_API_KEY)
User API: api_tulis

MODUL
- Pihak Ketiga (pelanggan): aktif, bisa dibaca
- Nota/Invoice pelanggan: aktif, bisa dibaca
- Produk: aktif, bisa dibaca
- Stok (gudang): aktif, bisa dibaca

HAK AKSES KUNCI
- [x] baca pelanggan (Pihak Ketiga)
- [x] lihat SEMUA pelanggan (bukan hanya yang ditautkan)
- [x] baca invoice/nota pelanggan
- [x] baca produk
- [x] baca stok
- [x] tambah/ubah pelanggan (menulis)
- [x] buat/ubah draf invoice (menulis)
```
## "Stok apa yang mau habis?" → `stok`
```
STOK PRODUK
Minus 0 | habis 1 | menipis 1 | dari 2 produk barang
- CUP-12 Gelas Kertas: stok 0 (min 20) HABIS -> beli 20
- KPI-250 Kopi Bubuk Arabika 250g: stok 7 (min 10) MENIPIS -> beli 23
```
Verifikasi: KPI-250 stok 7 < batas 10 → MENIPIS, saran = stok ideal 30 − 7 = **23** ✓; CUP-12 stok 0 → HABIS, tanpa stok ideal → batas 20 − 0 = **20** ✓.

## "Tambah pelanggan Kedai Kopi Senja, 0857 1111 2222, senja@contoh.id, Yogyakarta"
Pratinjau (tanpa `--ya`, tidak ada yang ditulis):
```
PRATINJAU PELANGGAN BARU
Nama: Kedai Kopi Senja
Telepon: 085711112222
Email: senja@contoh.id
Alamat: -
Kota: Yogyakarta
Kode pelanggan: dibuat otomatis oleh Dolibarr
Negara: Indonesia

Belum disimpan. Jika sudah benar, ulangi perintah yang sama dengan --ya.
```
Setelah "ya" (`--ya`):
```
TAMBAH PELANGGAN
Nama: Kedai Kopi Senja
Telepon: 085711112222
Email: senja@contoh.id
Alamat: -
Kota: Yogyakarta
Kode pelanggan: dibuat otomatis oleh Dolibarr
Negara: Indonesia

TERSIMPAN: ID 3 kode CU2609-00003
```
Kode pelanggan dibuat otomatis oleh Dolibarr (`code_client: auto`) ✓.
