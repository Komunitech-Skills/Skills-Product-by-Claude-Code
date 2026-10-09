# Uji ulang v1.0.2 — Skenario normal 3: gudang & kurir campuran (Blibli/Lazada-style) + kolom SKU ambigu

File fiktif dengan header ala Blibli/Lazada (`Order ID, AWB, Substatus, Shipping Provider, Item Name,
SKU Induk, Nomor SKU, Variation, Qty, Buyer Remark`) — sengaja punya **dua** kolom yang sama-sama
cocok sinonim SKU ("SKU Induk" dan "Nomor SKU"), 2 kurir berbeda (Anteraja, ID Express), 1 pesanan
dibatalkan.

## Tanpa override
```
python3 scripts/resi.py pesanan-blibli-lazada.csv --json
```
- `pemetaan_kolom.SKU` = "Nomor SKU" (dipilih otomatis karena "sku" ada di daftar sinonim lebih dulu
  dari "sku induk" untuk pencocokan persis vs sebagian — cek urutan `SINONIM_PESANAN["sku"]`).
- `kolom_ambigu` = `{"SKU": ["SKU Induk", "Nomor SKU"]}` — **peringatan baru v1.0.2 bekerja seperti
  dijanjikan**: field yang punya >1 kandidat cocok diberi tahu eksplisit ke pengguna, bukan diam-diam
  ditebak.
- Pesan peringatan: `"Kolom untuk SKU ambigu: ada 2 kolom mirip di file ('SKU Induk', 'Nomor SKU'),
  yang dipakai: 'Nomor SKU'. Kalau salah, jalankan ulang dengan --kolom-sku "Nama Kolom Persis".`" —
  jelas, menyebut kandidat lengkap, dan memberi perintah override siap pakai.

## Dengan override (`--kolom-sku "SKU Induk"`)
`kolom_ambigu` menjadi `{}` (field yang dioverride manual tidak lagi ditandai ambigu, sesuai
dokumentasi Langkah kerja SKILL.md), dan `pemetaan_kolom.SKU` berubah jadi "SKU Induk" sesuai
override. Tidak ada traceback pada kedua kasus.

## Verifikasi independen
BLI-001 (BTL-500-BRN x4, aktif), BLI-002 (BTL-500-BRN x2, aktif), BLI-003 (TMB-1L-SILVR x1,
aktif), BLI-004 (dibatalkan → dilewati). BTL-500-BRN total = 4+2 = 6, TMB-1L-SILVR = 1, grand
total = **7 pcs**, 3 pesanan aktif, 2 jenis barang — cocok dengan urutan-resi (3 pesanan, 2 kurir:
Anteraja 2 pesanan, ID Express 1 pesanan).

**Hasil: BENAR.** Fitur `kolom_ambigu` baru v1.0.2 lolos uji dengan kasus yang sengaja dirancang
untuk memicunya.
