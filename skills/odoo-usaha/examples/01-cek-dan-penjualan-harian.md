# 01 — Cek koneksi & ringkasan penjualan harian (Odoo 19, JSON-2)

> **Sumber keluaran:** dijalankan pembuat skill pada 30 Sep 2026 dengan `scripts/odoo.py` v1.0.0 terhadap **server Odoo TIRUAN** (`tests/server_tiruan.py`, data fiktif), BUKAN Odoo asli. Path HOME diganti `/home/pemilik`; alamat tiruan ditulis `http://localhost:8069`. Ini contoh input-output, bukan hasil uji independen.

**Permintaan pengguna:** "Odoo saya sudah nyambung? Terus penjualan hari ini berapa?"

Persiapan (dilakukan pemilik sendiri di terminal, kunci tidak tampil): `python3 scripts/odoo.py simpan-kunci` → kunci **baca-saja** (pengguna "Bot Laporan") tersimpan di `~/.komunitech/odoo-kunci.txt` berizin 600. Alamat default `http://localhost:8069`, jadi `atur` tidak diperlukan. Odoo 19 → protokol otomatis JSON-2 (tanpa nama database/login).

```
$ python3 scripts/odoo.py cek
CEK KONEKSI ODOO
Alamat: http://localhost:8069
Versi Odoo: 19.0
Protokol: JSON-2 (/json/2)
Database: (tidak dipakai/otomatis)
Kunci API: ****5e3f (file /home/pemilik/.komunitech/odoo-kunci.txt)
Pengguna API: Bot Laporan (bot-laporan@tokomaju.test) id 6
Mata uang perusahaan: IDR
Akses baca:
- Kontak/pelanggan: bisa dibaca (7 data)
- Penjualan (Sales): bisa dibaca (9 data)
- Faktur (Invoicing): bisa dibaca (11 data)
- Produk: bisa dibaca (9 data)
- Aturan stok minimum (Inventory): bisa dibaca (5 data)
CATATAN:
- Skill ini belum diuji ke server Odoo asli (hanya server tiruan). Cocokkan angka pertama kali dengan layar Odoo.
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py penjualan --tanggal 2026-09-30
RINGKASAN PENJUALAN ODOO
Rabu, 30 September 2026

PESANAN PENJUALAN TERKONFIRMASI (Sales)
Jumlah pesanan: 3
Total (termasuk pajak): Rp 1.917.352,95
Sebelum pajak Rp 1.727.345 | Pajak Rp 190.007,95
Kemarin: Rp 1.498.500 (+28,0%)
Rata-rata per pesanan: Rp 639.118
Produk terlaris (nilai sebelum pajak):
1. [KP-1KG] Kopi Arabika Gayo 1kg: 7 unit, Rp 1.392.345
2. [KP-250] Kopi Robusta Bubuk 250g: 6 unit, Rp 270.000
3. [GA-1KG] Gula Aren Cair 1kg: 2 unit, Rp 65.000
CATATAN: S00106 memakai USD (1.000) - tidak dijumlahkan.

FAKTUR PELANGGAN DIPOSTING (Invoicing)
Faktur: 2, nota kredit: 1
Total (termasuk pajak, dikurangi nota kredit): Rp 1.717.552,95
Sebelum pajak Rp 1.547.345 | Pajak Rp 170.207,95

Pesanan dan faktur adalah dua sudut pandang yang sama; JANGAN dijumlahkan (bisa dobel).
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py penjualan --tanggal 2026-09-30 --rinci --samarkan
RINGKASAN PENJUALAN ODOO
Rabu, 30 September 2026

PESANAN PENJUALAN TERKONFIRMASI (Sales)
Jumlah pesanan: 3
Total (termasuk pajak): Rp 1.917.352,95
Sebelum pajak Rp 1.727.345 | Pajak Rp 190.007,95
Kemarin: Rp 1.498.500 (+28,0%)
Rata-rata per pesanan: Rp 639.118
Produk terlaris (nilai sebelum pajak):
1. [KP-1KG] Kopi Arabika Gayo 1kg: 7 unit, Rp 1.392.345
2. [KP-250] Kopi Robusta Bubuk 250g: 6 unit, Rp 270.000
3. [GA-1KG] Gula Aren Cair 1kg: 2 unit, Rp 65.000
Rincian:
- S00101 C.M.J.: Rp 368.902,95
- S00102 W.B.S.: Rp 149.850
- S00103 H.M.I.: Rp 1.398.600
CATATAN: S00106 memakai USD (1.000) - tidak dijumlahkan.

FAKTUR PELANGGAN DIPOSTING (Invoicing)
Faktur: 2, nota kredit: 1
Total (termasuk pajak, dikurangi nota kredit): Rp 1.717.552,95
Sebelum pajak Rp 1.547.345 | Pajak Rp 170.207,95

Pesanan dan faktur adalah dua sudut pandang yang sama; JANGAN dijumlahkan (bisa dobel).
(kode keluar: 0)
```

## Pemeriksaan angka (manual, dari data tiruan)
- Rentang 30 Sep WIB = 29 Sep 17.00 s.d. 30 Sep 17.00 UTC (Odoo menyimpan jam dalam UTC). S00101 (29 Sep 18.30 UTC = 30 Sep 01.30 WIB) **ikut**; S00107 (30 Sep 17.30 UTC = 1 Okt 00.30 WIB) **tidak**; S00104 draf & S00105 batal tidak dihitung; S00106 berkurs USD dipisah.
- Total = 368.902,95 + 149.850 + 1.398.600 = **1.917.352,95**. Kemarin = 999.000 + 499.500 = 1.498.500. Kenaikan = 418.852,95 ÷ 1.498.500 = 27,95% → **+28,0%**.
- Faktur 30 Sep = 368.902,95 + 1.398.600 − 49.950 (nota kredit) = **1.717.552,95**.

**Jawaban agent (ringkas):** menyampaikan angka apa adanya, menegaskan pesanan dan faktur tidak dijumlahkan, dan menyebut 1 pesanan USD dipisah.
