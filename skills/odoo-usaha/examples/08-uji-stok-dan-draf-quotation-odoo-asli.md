# 08 — Uji independen: stok menipis + draf quotation (skenario normal 3)

> **Sumber keluaran:** penguji independen, 30 Sep 2026, Odoo Community ASLI 18.0 & 19.0 lokal (Docker resmi), data fiktif penguji.

**Permintaan pengguna:** "Stok apa yang mau habis?" lalu "Buatkan penawaran untuk CV Maju Jaya: kopi 3, gula aren 2 harga 32.500 diskon 10%, sirup 1,5."

## A. Stok menipis
Data (dicek penguji lewat admin): Kopi stok 40, min 25/maks 100, perkiraan 100 (ada penerimaan terjadwal); Gula stok 5, min 10/maks 10, perkiraan 3; Sirup stok −2, min 5/maks 20, perkiraan −5; Teh stok 0 tanpa aturan; Ongkos Kirim = jasa (tidak boleh muncul).

Hitungan penguji: Sirup MINUS, saran 20 − (−5) = **25**; Gula MENIPIS, saran 10 − 3 = **7**; Kopi aman (40 ≥ 25, perkiraan 100 ≥ 25); Teh HABIS tanpa aturan.
```
$ python3 scripts/odoo.py stok-menipis
STOK PERLU PERHATIAN (ODOO)
Aturan stok minimum (Reordering Rules) terbaca: 3

DENGAN ATURAN MINIMUM
- [SRP-VNL] Sirup Vanila 750ml: stok -2 (MINUS), perkiraan -5, min 5, maks 20 -> saran pesan 25
- [GA-1] Gula Aren 1kg: stok 5 (MENIPIS), perkiraan 3, min 10 -> saran pesan 7

HABIS/MINUS TANPA ATURAN MINIMUM
- [TH-100] Teh Melati 100g: stok 0 (HABIS)
Rumus: saran pesan = (maksimum bila diisi, selain itu minimum) - stok perkiraan (forecast), minimal 0.
(kode keluar: 0)
```
Cocok. Field `stock.warehouse.orderpoint.qty_on_hand/qty_forecast`, `product.product.is_storable` (18/19) dan `qty_available/virtual_available` benar di Odoo asli.

Catatan perilaku nyata: saat aturan ber-*trigger* otomatis, penjadwal Odoo langsung membuat penerimaan (perkiraan naik ke maks). Skill lalu menulis "Sirup ... stok -2 (MINUS), perkiraan 20 ... saran pesan 0". Angkanya benar, tetapi pembeli awam tidak diberi tahu bahwa "saran 0 karena sudah ada barang masuk terjadwal" (temuan rendah).

## B. Draf quotation
```
$ python3 scripts/odoo.py quotation buat --pelanggan 6 --item "KP-250|3" --item "Gula Aren 1kg|2|32.500|10" --item "SRP-VNL|1,5"
PRATINJAU DRAF QUOTATION ODOO
Pelanggan: CV Maju Jaya Abadi (ID 6)
Berlaku sampai: 2026-10-14
1. [KP-250] Kopi Robusta 250g: 3 x Rp 85.000 (harga jual Odoo) = Rp 255.000
2. [GA-1] Gula Aren 1kg: 2 x Rp 32.500 diskon 10% = Rp 58.500
3. [SRP-VNL] Sirup Vanila 750ml: 1,5 x Rp 12.345,67 (harga jual Odoo) = Rp 18.519
Subtotal sebelum pajak (DPP): Rp 332.019
Perkiraan pajak standar Komunitech (PPN 12% x DPP nilai lain 11/12 (efektif 11%)): Rp 36.522
Perkiraan total: Rp 368.541
...
Belum disimpan. Jika sudah benar dan pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
```
Hitungan penguji: 255.000 + 58.500 + 18.518,505 (→ 18.519) = 332.019; PPN 332.019 × 11% = 36.522,09 → dibulatkan ke bawah **36.522**. Cocok.

Setelah "ya" (`--ya`):
```
TERSIMPAN: S00008 (ID 8), status DRAF/Penawaran
Menurut Odoo: sebelum pajak Rp 332.018,51 | pajak Rp 36.522,04 | total Rp 368.540,55
Sebelum pajak: COCOK
Pajak: COCOK
Draf belum dikirim ke pelanggan. Periksa di Odoo (Penjualan > Penawaran), lalu klik Kirim/Konfirmasi sendiri bila sudah benar.
```
Dicek penguji lewat admin: `state = draft`, `origin = "Draf AI Komunitech <kode>"`, `validity_date = 2026-10-14`, 3 baris dengan harga/diskon/qty sesuai. Selisih sen (18.519 vs 18.518,51) wajar dan dilaporkan COCOK (< Rp 1).

Ulang perintah yang sama dengan `--ya` (dua kali):
```
DRAF TIDAK DIBUAT: sudah ada draf quotation serupa untuk pelanggan ini:
- S00008 (sebelum pajak Rp 332.018,51)
Periksa draf itu di Odoo. Bila memang perlu draf baru, ulangi dengan --tetap-buat.
(kode keluar: 7)
```
Draf dobel **diblokir** di 18 & 19.

## Temuan dari skenario ini
- **TEMUAN SEDANG:** draf S00008 di atas dibuat memakai kunci **bot-laporan** (hak yang disarankan panduan §5 untuk "Bot Laporan": *Sales User: All Documents*, Accounting Read-only). Odoo asli mengizinkannya (`create_uid = bot-laporan`). Klaim SKILL "kunci baca dipakai membuat draf → Hak akses kurang" tidak terjadi dengan hak yang disarankan; Odoo tidak punya grup standar "Penjualan hanya-baca". Pengaman nyata = daftar izin metode di script (terbukti bekerja, lihat 10).
