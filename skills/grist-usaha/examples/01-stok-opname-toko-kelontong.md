# Skenario 1 (normal) — Ringkasan stok opname toko kelontong

**Penguji:** Akun B (independen dari pembuat), 2026-09-26. Data & file `.grist` **dibuat sendiri
oleh penguji** (`ujiku/fixture_independen.py`), berbeda dari fixture pembuat
(`tests/fixtures/buat_fixture.py`) — supaya benar-benar independen.

## Permintaan pengguna
> "Grist saya file-nya di `toko-berkah-jaya.grist`, ringkas stok yang menipis/habis dong."

## Perintah yang dijalankan agent
```bash
python3 scripts/grist.py daftar-tabel toko-berkah-jaya.grist
python3 scripts/grist.py ringkasan toko-berkah-jaya.grist StokOpname --n 8
```

## Keluaran nyata
```
TABEL DI 'toko-berkah-jaya.grist' (2):
  - StokOpname  (7 kolom)
  - RekapHarian  (4 kolom)

RINGKASAN TABEL 'StokOpname'
Jumlah baris: 8
Kolom (7): Nama, Satuan, StokMasuk, StokKeluar, BatasMinimum, StokSaatIni (rumus), Status (rumus)

Contoh 8 baris pertama:
  Minyak Goreng 1L   masuk 120 keluar 95  batas 20 -> sisa 25  AMAN
  Beras Premium 5kg  masuk 40  keluar 39  batas 5  -> sisa 1   MENIPIS
  Telur Ayam         masuk 80  keluar 80  batas 10 -> sisa 0   HABIS
  Gula Pasir 1kg     masuk 60  keluar 12  batas 15 -> sisa 48  AMAN
  Mie Instan Dus     masuk 30  keluar 28  batas 3  -> sisa 2   MENIPIS
  Sabun Cuci Piring  masuk 25  keluar 25  batas 5  -> sisa 0   HABIS
  Kecap Manis        masuk 50  keluar 10  batas 0  -> sisa 40  AMAN
  Tepung Terigu 1kg  masuk 70  keluar 55  batas 20 -> sisa 15  MENIPIS
```

## Verifikasi independen (dihitung ulang manual, bukan dipercaya begitu saja)
Sisa = Masuk − Keluar; Status: HABIS bila sisa ≤ 0, MENIPIS bila batas > 0 dan sisa < batas,
selain itu AMAN. Dihitung ulang untuk semua 8 baris **sebelum** menulis fixture — hasil **cocok
100%** dengan yang dibaca `grist.py`, termasuk kasus batas 0 (Kecap Manis → AMAN, bukan MENIPIS,
karena aturan "batas > 0" ditegakkan dengan benar) dan kasus sisa pas di bawah batas (Mie Instan
Dus: sisa 2 < batas 3 → MENIPIS).

## Hasil
Sesuai harapan. Perintah baca `.grist` (read-only) jalan tanpa Grist perlu menyala, tanpa kunci
API, sesuai klaim di SKILL.md.
