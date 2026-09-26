# Skenario 03 — Toko online hanya memakai buku-stok, tanpa kasir (normal)

**Penguji:** agent independen, 2026-09-24. Data fiktif "Toko Kaos Rekaan".

## Permintaan pengguna
> "Gimana usaha kemarin?" (dikirim Kamis 24/9 jam 07.00)

## Data uji (dibuat dengan `stok.py` resmi, folder sementara `<uji>/toko/`)
- 5 SKU: KB-HT-M (stok 20, min 8), KB-HT-L (9, min 8), KB-NV-XL (3, min 5), TOPI-01 (15, min 5), MASKER-3 (2, min 10).
- Penjualan offline (`keluar`): 16/9 KB-HT-M ×2 @79.000 + TOPI-01 ×1 @40.000 (harga nego); 22/9 KB-HT-L ×1 @79.000; 23/9 TOPI-01 ×3 @45.000; 23/9 MASKER-3 ×1 **rusak** (bukan penjualan).
- File pesanan Shopee fiktif 23/9 (`impor-pesanan --platform shopee`): XYZ001 KB-NV-XL 85.000 + MASKER-3 20.000 (Perlu Dikirim), XYZ002 KB-HT-M 2 × 75.000 (Perlu Dikirim), XYZ003 **Batal**.
- Tidak ada kasir-lokal, absensi-lokal, atau pengingat.

## Perintah
```bash
python3 <uji>/skills/laporan-harian-usaha/scripts/laporan.py --tanggal kemarin --sekarang 2026-09-24T07:00+07:00
```

## Output nyata
```
LAPORAN HARIAN USAHA
Rabu, 23 September 2026
Dibuat 2026-09-24 07:00 WIB

PENJUALAN (dari buku-stok)
Omzet tercatat: Rp 390.000 (7 barang)
vs kemarin (Sel 22/9): Rp 79.000 -> naik 393,7%
vs Rabu lalu (16/9): Rp 198.000 -> naik 97,0%

STOK
Posisi per 2026-09-24 07:00 WIB
Minus 0 | habis 1 | menipis 2
- MASKER-3 Masker Kain 3 Lapis - Batik: stok 0 (min 10) HABIS
- KB-NV-XL Kaos Batik Print - Navy XL: stok 2 (min 5) MENIPIS, habis +-60 hari
- KB-HT-L Kaos Batik Print - Hitam L: stok 8 (min 8) MENIPIS, habis +-240 hari
Perlu restock (sampai batas minimum): MASKER-3 10, KB-NV-XL 3
Pesanan belum dikemas: 2

KEHADIRAN
Belum ada data (absensi-lokal belum dipakai di komputer ini).

TAGIHAN & FOLLOW-UP
Belum ada data (pengingat-follow-up belum dipakai di komputer ini).

PERLU PERHATIAN
1. 2 pesanan marketplace belum dikemas.

Sumber: buku-stok (hanya dibaca).
```

## Verifikasi independen
| Angka | Hitung manual | Script | Cocok |
|---|---|---|---|
| Omzet 23/9 | offline 3 × 45.000 = 135.000; Shopee 85.000 + 20.000 + 2 × 75.000 = 255.000; batal & rusak tidak dihitung → **390.000** | 390.000 | ✅ |
| Barang terjual | 3 + 1 + 1 + 2 = **7** | 7 | ✅ |
| 22/9 dan 16/9 | 79.000; 2 × 79.000 + 40.000 = **198.000** | sama | ✅ |
| % | 311.000 ÷ 79.000 = 393,67 → **393,7**; 192.000 ÷ 198.000 = 96,97 → **97,0** | sama | ✅ |
| Stok | MASKER-3 2 − 1 rusak − 1 Shopee = 0 (HABIS, restock 10); KB-NV-XL 3 − 1 = 2 (restock 3); KB-HT-L 9 − 1 = 8 = min → MENIPIS, kurang 0 sehingga tidak masuk daftar restock | sama | ✅ |
| Belum dikemas | XYZ001, XYZ002 = **2** | 2 | ✅ |

- Mingguan (`--periode mingguan --tanggal 2026-09-23`) pada data yang sama: minggu berjalan 21–24/9 = 79.000 + 390.000 = **469.000 (8 barang)** vs 14–17/9 **198.000** → 136,9% ✅. Waktu 0,7 detik (14 panggilan `laporan ringkas`).
- sha256 `stok.db` + 2 backup sebelum = sesudah ✅.
- Bagian yang alatnya tidak dipakai ditulis "Belum ada data", tidak diisi perkiraan ✅. Judul "PENJUALAN (dari buku-stok)" dan kata "Omzet tercatat" jujur bahwa sumbernya bukan kasir.

**Hasil: LULUS.**
