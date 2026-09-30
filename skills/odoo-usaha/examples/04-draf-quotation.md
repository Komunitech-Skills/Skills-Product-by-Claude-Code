# 04 — Draf quotation dengan konfirmasi (Odoo 19)

> **Sumber keluaran:** dijalankan pembuat skill pada 30 Sep 2026 dengan `scripts/odoo.py` v1.0.0 terhadap **server Odoo TIRUAN** (`tests/server_tiruan.py`, data fiktif), BUKAN Odoo asli. Path HOME diganti `/home/pemilik`; alamat tiruan ditulis `http://localhost:8069`. Ini contoh input-output, bukan hasil uji independen.

**Permintaan pengguna:** "Buatkan penawaran untuk CV Maju Jaya (0812 3456 7890): kopi robusta 250g 3, gula aren 2 harga 32.500, kopi gayo 1kg 1 harga 132.345."

Alur: cari pelanggan → cari produk yang namanya kurang jelas → **pratinjau** → pengguna menjawab "ya" → simpan dengan `--ya`. Percobaan pertama memakai kunci baca-saja (ditolak Odoo, benar); lalu kunci kedua khusus pembuat draf (`~/.komunitech/odoo-kunci-draf.txt`, disimpan pemilik sendiri dengan `simpan-kunci --kunci-file ...`). Perintah yang sama diulang → ditahan (kode 7) agar tidak dobel.

```
$ python3 scripts/odoo.py pelanggan cari "0812 3456 7890"
PELANGGAN ODOO cocok '0812 3456 7890': 1
- ID 3: CV Maju Jaya | 0812****890 | a***@majujaya.test | Solo
(Nomor HP & email disamarkan.)
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py produk cari "gula aren"
PRODUK ODOO cocok 'gula aren': 1
- #22 [GA-1KG] Gula Aren Cair 1kg: harga jual Rp 32.500, stok 8
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py quotation buat --pelanggan 3 --item "KP-250|3" --item "Gula Aren|2|32.500" --item "KP-1KG|1|132.345"
PRATINJAU DRAF QUOTATION ODOO
Pelanggan: CV Maju Jaya (ID 3)
Berlaku sampai: 2026-10-14
1. [KP-250] Kopi Robusta Bubuk 250g: 3 x Rp 45.000 (harga jual Odoo) = Rp 135.000
2. [GA-1KG] Gula Aren Cair 1kg: 2 x Rp 32.500 = Rp 65.000
3. [KP-1KG] Kopi Arabika Gayo 1kg: 1 x Rp 132.345 = Rp 132.345
Subtotal sebelum pajak (DPP): Rp 332.345
Perkiraan pajak standar Komunitech (PPN 12% x DPP nilai lain 11/12 (efektif 11%)): Rp 36.557
Perkiraan total: Rp 368.902
Pajak final dihitung Odoo dari pengaturan pajak produk/pelanggan (bisa berbeda; akan dicocokkan).

Belum disimpan. Jika sudah benar dan pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py quotation buat --pelanggan 3 --item "KP-250|3" --item "Gula Aren|2|32.500" --item "KP-1KG|1|132.345" --ya
GAGAL: Hak akses pengguna API kurang: You are not allowed to create 'Sales Order' (sale.order) records.
Saran: Beri pengguna API hak yang diperlukan (docs/panduan-odoo.md §5).
(kode keluar: 5)
```
```
$ python3 scripts/odoo.py quotation buat --pelanggan 3 --item "KP-250|3" --item "Gula Aren|2|32.500" --item "KP-1KG|1|132.345" --ya --kunci-file ~/.komunitech/odoo-kunci-draf.txt
MEMBUAT DRAF QUOTATION ODOO
Pelanggan: CV Maju Jaya (ID 3)
Berlaku sampai: 2026-10-14
1. [KP-250] Kopi Robusta Bubuk 250g: 3 x Rp 45.000 (harga jual Odoo) = Rp 135.000
2. [GA-1KG] Gula Aren Cair 1kg: 2 x Rp 32.500 = Rp 65.000
3. [KP-1KG] Kopi Arabika Gayo 1kg: 1 x Rp 132.345 = Rp 132.345
Subtotal sebelum pajak (DPP): Rp 332.345
Perkiraan pajak standar Komunitech (PPN 12% x DPP nilai lain 11/12 (efektif 11%)): Rp 36.557
Perkiraan total: Rp 368.902
Pajak final dihitung Odoo dari pengaturan pajak produk/pelanggan (bisa berbeda; akan dicocokkan).

TERSIMPAN: S00108 (ID 108), status DRAF/Penawaran
Menurut Odoo: sebelum pajak Rp 332.345 | pajak Rp 36.557,95 | total Rp 368.902,95
Sebelum pajak: COCOK
Pajak: COCOK
Draf belum dikirim ke pelanggan. Periksa di Odoo (Penjualan > Penawaran), lalu klik Kirim/Konfirmasi sendiri bila sudah benar.
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py quotation buat --pelanggan 3 --item "KP-250|3" --item "Gula Aren|2|32.500" --item "KP-1KG|1|132.345" --ya --kunci-file ~/.komunitech/odoo-kunci-draf.txt
MEMBUAT DRAF QUOTATION ODOO
Pelanggan: CV Maju Jaya (ID 3)
Berlaku sampai: 2026-10-14
1. [KP-250] Kopi Robusta Bubuk 250g: 3 x Rp 45.000 (harga jual Odoo) = Rp 135.000
2. [GA-1KG] Gula Aren Cair 1kg: 2 x Rp 32.500 = Rp 65.000
3. [KP-1KG] Kopi Arabika Gayo 1kg: 1 x Rp 132.345 = Rp 132.345
Subtotal sebelum pajak (DPP): Rp 332.345
Perkiraan pajak standar Komunitech (PPN 12% x DPP nilai lain 11/12 (efektif 11%)): Rp 36.557
Perkiraan total: Rp 368.902
Pajak final dihitung Odoo dari pengaturan pajak produk/pelanggan (bisa berbeda; akan dicocokkan).

DRAF TIDAK DIBUAT: sudah ada draf quotation serupa untuk pelanggan ini:
- S00108 (sebelum pajak Rp 332.345)
Periksa draf itu di Odoo. Bila memang perlu draf baru, ulangi dengan --tetap-buat.
(kode keluar: 7)
```

## Pemeriksaan angka (manual)
- DPP = 3 × 45.000 + 2 × 32.500 + 1 × 132.345 = **332.345**. PPN standar Komunitech = 332.345 × 11% = 36.557,95 → dibulatkan ke bawah **36.557**.
- Server tiruan menghitung pajak per baris (2 desimal) = 36.557,95; selisih < Rp 1 → COCOK. Di Odoo asli, pajak mengikuti pengaturan pajak produk/posisi fiskal; bila BEDA, skill melaporkan apa adanya.
- Status draf = `draft` (Penawaran). Skill tidak punya perintah kirim/konfirmasi.
