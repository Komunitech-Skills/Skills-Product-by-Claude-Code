# 05 — Input buruk, galat, dan permintaan di luar cakupan

> **Sumber keluaran:** dijalankan pembuat skill pada 30 Sep 2026 dengan `scripts/odoo.py` v1.0.0 terhadap **server Odoo TIRUAN** (`tests/server_tiruan.py`, data fiktif), BUKAN Odoo asli. Path HOME diganti `/home/pemilik`; alamat tiruan ditulis `http://localhost:8069`. Ini contoh input-output, bukan hasil uji independen.

Skenario: nama produk ambigu, angka ambigu, item kosong, singkatan flag konfirmasi, host yang belum diizinkan, Odoo mati, kunci dicabut, dan permintaan **menghapus faktur**.

```
$ python3 scripts/odoo.py quotation buat --pelanggan 3 --item "kopi|1"
GAGAL: Item 1: 'kopi' cocok ke beberapa produk: #21 [KP-250] Kopi Robusta Bubuk 250g; #25 [KP-1KG] Kopi Arabika Gayo 1kg; #28 [KP-250-D] Kopi Robusta Bubuk 250g (Decaf). Tanyakan yang mana, lalu pakai #id.
(kode keluar: 7)
```
```
$ python3 scripts/odoo.py quotation buat --pelanggan 3 --item "KP-250|62,500"
GAGAL: Item 1: jumlah '62,500' ambigu (62,500 bisa berarti 62.500 atau 62,5). Tulis 62500 atau 62.500.
(kode keluar: 2)
```
```
$ python3 scripts/odoo.py quotation buat --pelanggan 3
GAGAL: Belum ada item. Contoh: --item "KP-250|3" --item "Gula Aren 1kg|2|32500".
(kode keluar: 2)
```
```
$ python3 scripts/odoo.py quotation buat --pelanggan 3 --item "KP-250|1" --y
usage: odoo.py [-h]
               {atur,simpan-kunci,cek,penjualan,piutang,stok-menipis,pelanggan,produk,quotation,laporan-harian}
               ...
odoo.py: error: unrecognized arguments: --y
(kode keluar: 2)
```
```
$ python3 scripts/odoo.py cek --url https://erp.tokomaju.id
GAGAL: Host erp.tokomaju.id belum ada di daftar host yang diizinkan. Demi keamanan, skill ini hanya bicara dengan Odoo di komputer ini, *.odoo.com, atau server yang Anda daftarkan sendiri.
Saran: Jika server itu memang milik Anda, pemilik menjalankan: python3 scripts/odoo.py atur --url https://erp.tokomaju.id --izinkan-host  (pastikan https:// untuk server di internet).
(kode keluar: 2)
```
```
$ python3 scripts/odoo.py cek --url http://localhost:8099
GAGAL: Odoo di http://localhost:8099 tidak bisa dihubungi ([Errno 111] Connection refused).
Saran: Pastikan Odoo menyala dan alamatnya benar (buka di browser). Odoo lokal biasanya http://localhost:8069.
(kode keluar: 3)
```
```
$ python3 scripts/odoo.py cek --kunci-file ~/.komunitech/odoo-kunci-lama.txt
GAGAL: Kunci API ditolak Odoo (401: Invalid apikey).
Saran: Kunci mungkin salah, dicabut, atau kedaluwarsa. Buat kunci baru, lalu `simpan-kunci --ya`.
(kode keluar: 5)
```
```
$ python3 scripts/odoo.py hapus INV/2026/00190
usage: odoo.py [-h]
               {atur,simpan-kunci,cek,penjualan,piutang,stok-menipis,pelanggan,produk,quotation,laporan-harian}
               ...
odoo.py: error: argument perintah: invalid choice: 'hapus' (choose from 'atur', 'simpan-kunci', 'cek', 'penjualan', 'piutang', 'stok-menipis', 'pelanggan', 'produk', 'quotation', 'laporan-harian')
(kode keluar: 2)
```

## Perilaku agent yang diwajibkan SKILL.md
- `kopi` ambigu → tanyakan sekali: "Kopi yang mana: Robusta 250g, Arabika Gayo 1kg, atau Robusta Decaf?" lalu pakai `#id`.
- `62,500` → tanyakan: "Maksudnya 62.500 (enam puluh dua ribu lima ratus) atau 62,5?"
- Host belum diizinkan → jangan menambah izin sendiri; tanya pemilik apakah server itu miliknya, baru pemilik menjalankan `atur --izinkan-host`.
- "Hapus faktur INV/2026/00190" / "konfirmasi pesanan S00108" / "posting faktur" → **tolak dengan sopan**: skill ini hanya membaca dan membuat draf penawaran; hapus/konfirmasi/posting/pembayaran dilakukan manusia di layar Odoo (Faktur > pilih faktur > Reset ke Draf/Batalkan). Script memang tidak punya perintah itu (lihat galat `invalid choice`), dan agent tidak boleh memanggil API Odoo lewat cara lain.
