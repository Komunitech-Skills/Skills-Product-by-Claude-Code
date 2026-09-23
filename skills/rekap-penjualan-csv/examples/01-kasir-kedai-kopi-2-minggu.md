# Contoh 01 – Rekap 2 minggu dari ekspor kasir kedai kopi

## Skenario
S1, permintaan normal. File ekspor aplikasi kasir, pemisah koma, tanggal `dd/mm/yyyy`, kolom Total berformat `Rp 18.000`. Ada 127 baris transaksi selama 14 hari, dengan 7 menu.

## Input pengguna
```
Halo, ini file export kasir kedai kopi aku 2 minggu pertama September (kasir-kopi-sept.csv). Tolong direkap ya, mau tau menu mana yang paling laku sama hari apa yang paling rame.
```
Cuplikan file:
```
Tanggal,Produk,Qty,Total
01/09/2026,Americano,4,Rp 60.000
01/09/2026,Pisang Goreng,1,Rp 12.000
01/09/2026,Es Kopi Susu Gula Aren,1,Rp 18.000
```

## Output

## Rekap Penjualan 1 – 14 September 2026

**Total omzet:** Rp 5.084.000
**Jumlah transaksi (baris):** 127
**Rata-rata omzet per hari (kalender):** Rp 363.143  _(hari berjualan: Rp 363.143; 14 dari 14 hari ada penjualan)_

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Matcha Latte | 60 | Rp 1.320.000 | 26,0% |
| 2 | Es Kopi Susu Gula Aren | 63 | Rp 1.134.000 | 22,3% |
| 3 | Roti Bakar Coklat | 53 | Rp 848.000 | 16,7% |
| 4 | Americano | 43 | Rp 645.000 | 12,7% |
| 5 | Pisang Goreng | 36 | Rp 432.000 | 8,5% |

Dua menu lainnya (Kopi Tubruk dan Teh Tarik) digabung menyumbang Rp 705.000 (13,9%).

### Tren harian
Hari terbaik: Senin, 7 September 2026 (Rp 549.000). Hari terendah: Senin, 14 September 2026 (Rp 214.000).

Minggu pertama (1–7 Sep) omzetnya Rp 2.475.000, minggu kedua (8–14 Sep) Rp 2.609.000, naik sekitar 5,4%. Semua 127 baris terbaca, tidak ada baris yang dilewati.

### Insight
1. **Matcha Latte juara omzet walaupun bukan yang paling banyak terjual.** Qty-nya 60, lebih sedikit dari Es Kopi Susu Gula Aren (63 cup), tapi omzetnya paling besar (Rp 1.320.000). Pastikan stok bahan matcha tidak pernah kosong, dan jadikan menu ini rekomendasi utama kasir.
2. **Minuman + roti bakar adalah kombinasi utama.** Dua minuman teratas menyumbang 48,3% omzet, dan Roti Bakar Coklat ada di posisi 3 (16,7%). Coba paket "Es Kopi Susu / Matcha + Roti Bakar" untuk menaikkan nilai per transaksi.
3. **Senin, 14 September adalah hari terendah (Rp 214.000), turun jauh dari Senin sebelumnya (Rp 549.000).** Cek apakah hari itu ada jam buka yang lebih pendek, cuaca, atau stok habis. Kalau penyebabnya jelas, tidak perlu promo khusus. Kalau tidak jelas, pantau Senin berikutnya.

## Catatan penguji
- Perintah yang dijalankan: `python3 <skill>/scripts/rekap.py kasir-kopi-sept.csv --kolom-tanggal "Tanggal" --kolom-produk "Produk" --kolom-qty "Qty" --kolom-total "Total"` (exit 0, `baris_dilewati: 0`).
- **Verifikasi independen:** total, jumlah baris, rata-rata, 5 produk (qty, omzet, %), serta hari terbaik/terendah dihitung ulang dengan script Python terpisah yang tidak memakai `parse_angka` bawaan skill. Hasilnya **cocok 100%**.
- Bagus: format sesuai SKILL.md, rupiah bertitik, insight berbasis angka dan bisa ditindaklanjuti.
- Catatan: angka turunan seperti "48,3%", "Rp 705.000", dan omzet per minggu dihitung agent dari JSON script (penjumlahan sederhana). SKILL.md menyatakan "semua angka harus berasal dari output script", jadi angka turunan berada di wilayah abu-abu. Sebaiknya aturan ini dipertegas (lihat HASIL-UJI.md).
- **Uji ulang v1.1.0 (2026-09-23):** script versi baru dijalankan ulang pada file yang sama. Hasilnya identik (total Rp 5.084.000, 127 baris, top-5, hari terbaik/terendah) dan cocok dengan verifikasi independen. Baris rata-rata disesuaikan dengan format output baru (kalender + hari berjualan). Catatan "angka turunan" di atas **masih berlaku**, karena aturan di SKILL.md belum diubah.
- **Uji ulang v1.2.0 (2026-09-23):** hasil identik (Rp 5.084.000, 127 baris, top-5, hari terbaik/terendah). JSON kini juga berisi `status_dihitung` (kosong, karena tanpa kolom status) dan `nama_produk_digabung` (kosong). Catatan "angka turunan" masih berlaku.
