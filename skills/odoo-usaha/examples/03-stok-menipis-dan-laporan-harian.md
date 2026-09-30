# 03 — Stok menipis & laporan harian siap kirim Telegram (Odoo 19)

> **Sumber keluaran:** dijalankan pembuat skill pada 30 Sep 2026 dengan `scripts/odoo.py` v1.0.0 terhadap **server Odoo TIRUAN** (`tests/server_tiruan.py`, data fiktif), BUKAN Odoo asli. Path HOME diganti `/home/pemilik`; alamat tiruan ditulis `http://localhost:8069`. Ini contoh input-output, bukan hasil uji independen.

**Permintaan pengguna:** "Barang apa yang mau habis? Terus buatkan laporan harian buat dikirim ke Telegram saya tiap malam."

```
$ python3 scripts/odoo.py stok-menipis
STOK PERLU PERHATIAN (ODOO)
Aturan stok minimum (Reordering Rules) terbaca: 5

DENGAN ATURAN MINIMUM
- [SRP-VNL] Sirup Vanila 750ml: stok -2 (MINUS), perkiraan -2, min 6, maks 24 -> saran pesan 26
- [CUP-12] Gelas Kertas 12oz (isi 50): stok 0 (HABIS), perkiraan 50, min 20, maks 100 -> saran pesan 50
- [GA-1KG] Gula Aren Cair 1kg: stok 8 (MENIPIS), perkiraan 8, min 10 -> saran pesan 2
- [KP-250] Kopi Robusta Bubuk 250g: stok 120 (PERKIRAAN DI BAWAH MINIMUM), perkiraan 96, min 100, maks 200 -> saran pesan 104

HABIS/MINUS TANPA ATURAN MINIMUM
- [SDT-KYU] Sendok Kayu (isi 100): stok 0 (HABIS)
Rumus: saran pesan = (maksimum bila diisi, selain itu minimum) - stok perkiraan (forecast), minimal 0.
(kode keluar: 0)
```
```
$ python3 scripts/odoo.py laporan-harian --tanggal 2026-09-30
LAPORAN HARIAN ODOO
Rabu, 30 September 2026

PENJUALAN
Pesanan terkonfirmasi: 3, total Rp 1.917.352,95 (+28,0% vs kemarin)
Sebelum pajak Rp 1.727.345 | Pajak Rp 190.007,95
Terlaris: [KP-1KG] Kopi Arabika Gayo 1kg (7); [KP-250] Kopi Robusta Bubuk 2… (6); [GA-1KG] Gula Aren Cair 1kg (2)
Faktur diposting: 2 (+1 nota kredit), total Rp 1.717.552,95

PIUTANG (per 2026-09-30)
Belum lunas: 7 faktur, Rp 11.424.502,95
Lewat jatuh tempo: 4 faktur, Rp 8.658.000
- INV/2026/00170 (H.M.I.) sisa Rp 5.661.000, lewat 103 hari
- INV/2026/00180 (T.B.S.) sisa Rp 1.387.500, lewat 86 hari
- INV/2026/00185 (P.K.N.) sisa Rp 1.110.000, lewat 37 hari
- ... 1 faktur telat lainnya

STOK
- [SRP-VNL] Sirup Vanila 750ml: -2 (MINUS)
- [CUP-12] Gelas Kertas 12oz (isi 50): 0 (HABIS)
- [GA-1KG] Gula Aren Cair 1kg: 8 (MENIPIS)
- [KP-250] Kopi Robusta Bubuk 250g: 120 (PERKIRAAN DI BAWAH MINIMUM)
- [SDT-KYU] Sendok Kayu (isi 100): 0 (HABIS)

PERLU PERHATIAN
1. Ada faktur lewat 60+ hari. Rincian & nama pelanggan: perintah `piutang`.
2. 3 barang habis/minus. Cek pembelian.
(Nama pelanggan disamarkan. Angka dihitung script dari Odoo.)
(kode keluar: 0)
```

## Pemeriksaan (manual)
- Sirup Vanila: stok −2, minimum 6, maksimum 24 → saran pesan = 24 − (−2) = **26**.
- Kopi Robusta 250g: stok 120 (di atas minimum 100) tetapi perkiraan 96 (ada pesanan keluar) → "PERKIRAAN DI BAWAH MINIMUM", saran = 200 − 96 = **104**. Aturan ini sama dengan pemicu pemesanan ulang Odoo (perkiraan < minimum).
- Ongkos Antar (jasa) tidak ikut; Sendok Kayu tidak punya aturan minimum tetapi stok 0 → daftar terpisah.
- Laporan harian: **tanpa nama pelanggan** (hanya nomor faktur + inisial), < 3.500 karakter (batas aman satu pesan Telegram). Jadwal pengiriman: `references/openclaw-jadwal.md` (tunjukkan perintah + minta "ya" dulu).
