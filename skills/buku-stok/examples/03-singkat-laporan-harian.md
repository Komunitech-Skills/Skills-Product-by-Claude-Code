# 03 — Permintaan singkat: laporan stok hari ini (uji ulang v1.1.0)

**Skenario:** S3 (normal, singkat/malas). Hari ini ada restock kaos (contoh 02), impor pesanan Shopee (contoh 01), dan penjualan offline 6 mug @ Rp 45.000.

**Input pengguna (persis):**
> bikinin dong laporan stok hari ini, yg mau abis apa aja

**Perintah yang dijalankan agent (hanya baca, tanpa konfirmasi):**
```bash
python3 scripts/stok.py laporan ringkas --json
python3 scripts/stok.py laporan menipis --json
```

## Output
Teks script dikirim apa adanya (v1.1.0), ditambah dua kalimat penutup dari agent:
```
Laporan Stok Harian - 23/09/2026
Terjual: 12 barang (marketplace 6 dari 2 pesanan, toko/offline 6)
Omzet tercatat: Rp 594.000 | HPP: Rp 321.824 | Laba kotor (perkiraan): Rp 272.176
Terlaris: MUG-KRM (6), KAOS-PT-M (3), KAOS-HT-M (2), TOTE-NAT (1)
Pesanan belum dikemas: 2
Restock hari ini: 50 barang (Rp 1.725.000, termasuk ongkir/biaya tambahan)
Stok menipis/habis: 1 produk
  - MUG-KRM Mug Keramik 350ml - Putih: sisa 5 (min 6), habis +-21 hari lagi
Barang tidak laku >= 30 hari: 0 produk (modal tertahan Rp 0)
Nilai persediaan: Rp 4.805.176

Yang perlu dipesan ulang: Mug Keramik Putih (sisa 5, minimum 6; rata-rata laku ±0,23/hari).
Laba kotor di atas belum dikurangi biaya admin marketplace, ongkir, dan iklan.
```

## Catatan penguji
- Verifikasi independen: omzet = 2×59.000 + 35.000 + 3×57.000 + 6×45.000 = 594.000; HPP = 2×34.662,16 + 18.500 + 3×34.000 + 6×22.000 = 321.824,32; laba 272.176; nilai persediaan = 72×34.662,16 + 16×35.000 + 27×34.000 + 39×18.500 + 5×22.000 = 4.805.175,68 → Rp 4.805.176; rata-rata laku mug 7/30 = 0,233 → 21 hari. Semua cocok.
- v1.1.0 memperbaiki kalimat v1.0.0 ("12 barang dari 2 pesanan marketplace") menjadi rincian marketplace vs toko — teks script kini aman dikirim apa adanya lewat jadwal.
- **Pesanan batal setelah impor (cacat berat v1.0.0) sudah beres:** pada data uji yang sama, setelah 0002CD batal, laporan 23/09 = 5 barang, omzet Rp 243.000, HPP Rp 132.500, KAOS-PT-M hilang dari "Terlaris"; `laporan mutasi` September = Penjualan Rp 406.000 dan HPP Rp 224.500. Diuji juga pada database v1.0.0 lama (migrasi otomatis) dan pada backup v1.0.0 yang di-restore.
