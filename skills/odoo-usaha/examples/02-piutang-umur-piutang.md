# 02 — Piutang & umur piutang (Odoo 17, XML-RPC)

> **Sumber keluaran:** dijalankan pembuat skill pada 30 Sep 2026 dengan `scripts/odoo.py` v1.0.0 terhadap **server Odoo TIRUAN** (`tests/server_tiruan.py`, data fiktif), BUKAN Odoo asli. Path HOME diganti `/home/pemilik`; alamat tiruan ditulis `http://localhost:8069`. Ini contoh input-output, bukan hasil uji independen.

**Permintaan pengguna:** "Siapa saja yang belum bayar? Yang paling telat siapa?"

Odoo 17 memakai XML-RPC, jadi nama database & login pengguna API wajib diisi sekali lewat `atur` (non-rahasia). Kunci tetap di file kunci terpisah.

```
$ python3 scripts/odoo.py atur --url http://localhost:8069 --db tokomaju --login bot-laporan@tokomaju.test
KONFIGURASI ODOO (disimpan)
File: /home/pemilik/.komunitech/odoo.json
- url: http://localhost:8069
- db: tokomaju
- login: bot-laporan@tokomaju.test
- protokol: (belum diisi)
- tz: (belum diisi)
- host_diizinkan: (hanya lokal & *.odoo.com)
Kunci API TIDAK disimpan di sini. Simpan terpisah dengan `simpan-kunci` di terminal Anda sendiri.
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py piutang --per-tanggal 2026-09-30
PIUTANG PELANGGAN ODOO (per Rabu, 30 September 2026)
Belum lunas: 7 faktur, Rp 11.424.502,95
Lewat jatuh tempo: 4 faktur, Rp 8.658.000

UMUR PIUTANG (dari tanggal jatuh tempo)
- belum jatuh tempo: 3 faktur, Rp 2.766.502,95
- 1-30 hari: 1 faktur, Rp 499.500
- 31-60 hari: 1 faktur, Rp 1.110.000
- 61-90 hari: 1 faktur, Rp 1.387.500
- >90 hari: 1 faktur, Rp 5.661.000

PELANGGAN TERBESAR
- Hotel Melati Indah: Rp 7.059.600 (2 faktur, terlama lewat 103 hari)
- Toko Bangunan Sinar Abadi: Rp 1.387.500 (1 faktur, terlama lewat 86 hari)
- CV Maju Jaya: Rp 1.367.902,95 (2 faktur)
- PT Kopi Nusantara Sejahtera: Rp 1.110.000 (1 faktur, terlama lewat 37 hari)
- Budi Santoso: Rp 499.500 (1 faktur, terlama lewat 13 hari)

RINCIAN (terlama dulu, maks. 30)
- INV/2026/00170 Hotel Melati Indah: sisa Rp 5.661.000 | tempo 2026-06-19 | lewat 103 hari
- INV/2026/00180 Toko Bangunan Sinar Abadi: sisa Rp 1.387.500 | tempo 2026-07-06 | lewat 86 hari
- INV/2026/00185 PT Kopi Nusantara Sejahtera: sisa Rp 1.110.000 (dibayar sebagian) | tempo 2026-08-24 | lewat 37 hari
- INV/2026/00190 Budi Santoso: sisa Rp 499.500 | tempo 2026-09-17 | lewat 13 hari
- INV/2026/00192 CV Maju Jaya: sisa Rp 999.000 | tempo 2026-10-04 | jatuh tempo 4 hari lagi
- INV/2026/00201 CV Maju Jaya: sisa Rp 368.902,95 | tempo 2026-10-14 | jatuh tempo 14 hari lagi
- INV/2026/00202 Hotel Melati Indah: sisa Rp 1.398.600 | tempo 2026-10-30 | jatuh tempo 30 hari lagi
CATATAN: ada 1 nota kredit belum dipakai, Rp 49.950; piutang bersih bisa lebih kecil.
Status bayar = kondisi SAAT INI di Odoo. Faktur draf tidak dihitung.
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py piutang --per-tanggal 2026-09-30 --samarkan --maks 3
PIUTANG PELANGGAN ODOO (per Rabu, 30 September 2026)
Belum lunas: 7 faktur, Rp 11.424.502,95
Lewat jatuh tempo: 4 faktur, Rp 8.658.000

UMUR PIUTANG (dari tanggal jatuh tempo)
- belum jatuh tempo: 3 faktur, Rp 2.766.502,95
- 1-30 hari: 1 faktur, Rp 499.500
- 31-60 hari: 1 faktur, Rp 1.110.000
- 61-90 hari: 1 faktur, Rp 1.387.500
- >90 hari: 1 faktur, Rp 5.661.000

PELANGGAN TERBESAR
- H.M.I.: Rp 7.059.600 (2 faktur, terlama lewat 103 hari)
- T.B.S.: Rp 1.387.500 (1 faktur, terlama lewat 86 hari)
- C.M.J.: Rp 1.367.902,95 (2 faktur)
- P.K.N.: Rp 1.110.000 (1 faktur, terlama lewat 37 hari)
- B.S.: Rp 499.500 (1 faktur, terlama lewat 13 hari)

RINCIAN (terlama dulu, maks. 3)
- INV/2026/00170 H.M.I.: sisa Rp 5.661.000 | tempo 2026-06-19 | lewat 103 hari
- INV/2026/00180 T.B.S.: sisa Rp 1.387.500 | tempo 2026-07-06 | lewat 86 hari
- INV/2026/00185 P.K.N.: sisa Rp 1.110.000 (dibayar sebagian) | tempo 2026-08-24 | lewat 37 hari
... dan 4 faktur lain (pakai --maks untuk melihat semua).
CATATAN: ada 1 nota kredit belum dipakai, Rp 49.950; piutang bersih bisa lebih kecil.
Status bayar = kondisi SAAT INI di Odoo. Faktur draf tidak dihitung.
(kode keluar: 0)
```

## Pemeriksaan angka (manual)
- Dihitung: faktur pelanggan **terposting** dengan status bayar belum/sebagian dan sisa > 0. Tidak dihitung: INV/2026/00193 (in_payment, sisa 0), INV/2026/00194 (lunas), INV/2026/00195 (draf).
- Total sisa = 368.902,95 + 1.398.600 + 1.387.500 + 1.110.000 + 499.500 + 999.000 + 5.661.000 = **11.424.502,95**.
- Umur INV/2026/00170: 19 Jun → 30 Sep = 11 + 31 + 31 + 30 = **103 hari** (>90).
- Nota kredit RINV/2026/00007 (Rp 49.950) belum dipakai → dicatat terpisah, tidak dikurangkan otomatis.

**Catatan:** versi `--samarkan` dipakai bila hasil akan diteruskan ke orang lain/Telegram; versi lengkap hanya untuk pemilik di percakapan langsung.
