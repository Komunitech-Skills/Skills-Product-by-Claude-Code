# 03 — Permintaan singkat: laporan stok hari ini

**Skenario:** S3 (normal, singkat/malas). Hari ini ada impor pesanan Shopee (contoh 01), restock kaos (contoh 02), dan penjualan offline 6 mug @ Rp 45.000.

**Input pengguna (persis):**
> bikinin dong laporan stok hari ini, yg mau abis apa aja

**Perintah yang dijalankan agent (hanya baca, tanpa konfirmasi):**
```bash
python3 scripts/stok.py laporan ringkas --json
python3 scripts/stok.py laporan menipis --json
```

## Output
```
Laporan Stok Harian - 23/09/2026
Terjual: 12 barang (6 dari 2 pesanan marketplace, 6 penjualan toko)
Omzet tercatat: Rp 594.000 | HPP: Rp 321.824 | Laba kotor (perkiraan): Rp 272.176
Terlaris: MUG-KRM (6), KAOS-PT-M (3), KAOS-HT-M (2), TOTE-NAT (1)
Pesanan belum dikemas: 2
Restock hari ini: 50 barang (Rp 1.725.000 + ongkir Rp 25.000)
Stok menipis/habis: 1 produk
  - MUG-KRM Mug Keramik 350ml - Putih: sisa 5 (min 6), habis ±21 hari lagi
Barang tidak laku >= 30 hari: 0 produk (modal tertahan Rp 0)
Nilai persediaan: Rp 4.805.176

Yang perlu dipesan ulang: Mug Keramik Putih (sisa 5, minimum 6; rata-rata laku ±0,23/hari).
Laba kotor di atas belum dikurangi biaya admin marketplace, ongkir, dan iklan.
Mau laporan ini dikirim otomatis ke Telegram setiap jam 9 malam?
```

## Catatan penguji
- Verifikasi independen: omzet = 2×59.000 + 35.000 + 3×57.000 + 6×45.000 = 594.000; HPP = 2×34.662,16 + 18.500 + 3×34.000 + 6×22.000 = 321.824,32; laba 272.176; nilai persediaan = 72×34.662,16 + 16×35.000 + 27×34.000 + 39×18.500 + 5×22.000 = 4.805.175,68 → Rp 4.805.176. Rata-rata laku mug = 7 pcs / 30 hari = 0,233 → 5/0,233 = 21 hari. Semua cocok.
- Kurang: teks asli script berbunyi "Terjual: 12 barang dari 2 pesanan marketplace" (padahal 6 barang dari toko offline) dan "Restock ... (Rp 1.725.000)" tanpa ongkir; di contoh ini agent memperjelasnya, tetapi SKILL.md menyuruh "kirim teks script apa adanya" → pada jadwal otomatis kalimat menyesatkan itu terkirim.
- Cacat terkait (diuji terpisah): bila pesanan yang sudah diimpor kemudian **batal**, `laporan ringkas` untuk tanggal pesanan itu **tetap menghitung** qty, omzet, HPP, dan "terlaris" dari pesanan batal (uji: laporan 23/09 menunjukkan omzet Rp 414.000 padahal seharusnya Rp 243.000; KAOS-PT-M (3) tetap tercantum terlaris). `laporan mutasi` mengurangi HPP batal tetapi tidak mengurangi "Penjualan tercatat" (lebih Rp 171.000). Lihat HASIL-UJI.md.
