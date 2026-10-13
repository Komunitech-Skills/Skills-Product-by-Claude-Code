# Contoh 1 — Baca ringkasan stok langsung dari file `.grist` (read-only, tanpa Grist perlu menyala)

**Konteks uji:** file `.grist` TIRUAN dibuat dengan `tests/fixtures/buat_fixture.py`
(`buat_dokumen_contoh`), skemanya disusun sama persis dengan kode sumber resmi `grist-core`
v1.7.19 (lihat (riset internal kurator, tidak disertakan dalam paket)). **Bukan** ekspor Grist sungguhan.

## Percakapan

> **Pengguna:** "Grist saya ada di `Data Usaha Saya.grist` di folder Dokumen. Stok yang mau
> habis apa aja?"

Agent menjalankan (path disesuaikan komputer pengguna):

```
$ python3 grist.py daftar-tabel "Data Usaha Saya.grist"
TABEL DI 'Data Usaha Saya.grist' (2):
  - Pelanggan  (5 kolom)
  - Stok  (6 kolom)

$ python3 grist.py ringkasan "Data Usaha Saya.grist" Stok
RINGKASAN TABEL 'Stok'
Jumlah baris: 3
Kolom (6):
  - Nama                 [Text      ]          label: Nama Barang
  - StokMasuk            [Int       ]          label: Masuk
  - StokKeluar           [Int       ]          label: Keluar
  - BatasMinimum         [Int       ]          label: Batas Minimum
  - StokSaatIni          [Int       ] (rumus)  label: Sisa Stok
  - Status               [Text      ] (rumus)  label: Status

Contoh 3 baris pertama:
  {'Nama': 'Kopi Robusta 1kg', 'StokMasuk': 100, 'StokKeluar': 40, 'BatasMinimum': 20, 'StokSaatIni': 60, 'Status': 'AMAN'}
  {'Nama': 'Gula Aren 1kg', 'StokMasuk': 50, 'StokKeluar': 48, 'BatasMinimum': 10, 'StokSaatIni': 2, 'Status': 'MENIPIS'}
  {'Nama': 'Cup Kertas 12oz', 'StokMasuk': 200, 'StokKeluar': 200, 'BatasMinimum': 50, 'StokSaatIni': 0, 'Status': 'HABIS'}
```

**Balasan agent ke pengguna:**

> Dari tabel Stok (3 barang tercatat):
> - **HABIS**: Cup Kertas 12oz (sisa 0)
> - **MENIPIS**: Gula Aren 1kg (sisa 2, batas minimum 10)
> - Aman: Kopi Robusta 1kg (sisa 60)
>
> Angka ini langsung dari kolom rumus `StokSaatIni`/`Status` di file Grist Anda (dihitung Grist
> sendiri, saya hanya membacanya). Mau saya buatkan daftar belanja untuk yang menipis/habis?

## Catatan uji
- Perintah dijalankan **read-only** (`PRAGMA query_only`) — dicek otomatis di
  `tests/uji_regresi.py` (`test_benar_benar_read_only_tidak_menulis`): ukuran file tidak berubah,
  dan percobaan `INSERT` langsung ditolak SQLite.
- Tidak butuh Grist/Docker menyala sama sekali untuk skenario ini.
