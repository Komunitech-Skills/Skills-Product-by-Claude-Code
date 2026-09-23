# 01 — Keripik pisang: HPP, harga jual margin 35%, BEP

**Skenario:** S1 — permintaan normal, usaha makanan rumahan dengan konversi satuan (kg→g) dan biaya bulanan.

**Input pengguna (persis):**
> Mau hitung modal keripik pisang balado. Sekali produksi: pisang 10 kg (8 ribu/kg), minyak 2 liter (19 ribu/liter), bumbu balado 250 gram (beli 1 kg 60 ribu). Jadinya 40 bungkus. Standing pouch 85 ribu isi 100. Gas 3 kg 22 ribu buat 2x produksi. Upah yang bantu 50 ribu sekali produksi. Sewa dapur 600 ribu sebulan. Sebulan produksi 480 bungkus. Mau margin 35%, jual berapa?

**Yang dilakukan agent:** menyusun `hpp-keripik.json` (gas 22.000 ÷ 2 produksi = 11.000 per batch), lalu:
```bash
python3 <folder-skill>/scripts/hitung_hpp.py --file hpp-keripik.json
```
<details><summary>Isi hpp-keripik.json</summary>

```json
{
  "nama_produk": "Keripik Pisang Balado",
  "satuan_produk": "bungkus",
  "hasil_per_batch": 40,
  "produksi_per_bulan": 480,
  "bahan": [
    {"nama": "Pisang kepok", "harga_beli": "8.000", "isi_beli": 1, "satuan_beli": "kg", "pakai": 10, "satuan_pakai": "kg"},
    {"nama": "Minyak goreng", "harga_beli": "19.000", "isi_beli": 1, "satuan_beli": "liter", "pakai": 2, "satuan_pakai": "liter"},
    {"nama": "Bumbu balado", "harga_beli": "60.000", "isi_beli": 1, "satuan_beli": "kg", "pakai": 250, "satuan_pakai": "g"}
  ],
  "tenaga_kerja": [{"nama": "Upah bantu", "biaya": "50.000", "per": "batch"}],
  "overhead": [
    {"nama": "Gas 3 kg (1 tabung untuk 2x produksi)", "biaya": "11.000", "per": "batch"},
    {"nama": "Sewa dapur", "biaya": "600.000", "per": "bulan"}
  ],
  "kemasan": [{"nama": "Standing pouch", "harga_beli": "85.000", "isi_beli": 100, "satuan_beli": "pcs", "pakai": 1, "satuan_pakai": "pcs"}],
  "target_margin_persen": 35
}
```
</details>

## Output

## HPP Keripik Pisang Balado (per bungkus)

Hasil per batch: 40 bungkus | Produksi per bulan: 480 bungkus

| Kategori | Komponen | Cara hitung | Biaya | Per bungkus |
|---|---|---|---:|---:|
| Bahan baku | Pisang kepok | Rp 8.000 / 1 kg x pakai 10 kg | Rp 80.000 /batch | Rp 2.000 |
| Bahan baku | Minyak goreng | Rp 19.000 / 1 liter x pakai 2 liter | Rp 38.000 /batch | Rp 950 |
| Bahan baku | Bumbu balado | Rp 60.000 / 1 kg x pakai 250 g | Rp 15.000 /batch | Rp 375 |
| Tenaga kerja | Upah bantu | biaya langsung | Rp 50.000 /batch | Rp 1.250 |
| Overhead | Gas 3 kg (1 tabung untuk 2x produksi) | biaya langsung | Rp 11.000 /batch | Rp 275 |
| Overhead | Sewa dapur | biaya langsung | Rp 600.000 /bulan | Rp 1.250 |
| Kemasan | Standing pouch | Rp 85.000 / 100 pcs x pakai 1 pcs | Rp 850 /unit | Rp 850 |

**Ringkasan HPP per bungkus**

- Bahan baku: Rp 3.325
- Tenaga kerja: Rp 1.250
- Overhead: Rp 1.525
- Kemasan: Rp 850
- **HPP per bungkus: Rp 6.950**
  - biaya variabel Rp 5.700 + biaya tetap dialokasikan Rp 1.250

**Harga jual** (dibulatkan ke atas kelipatan Rp 500)

- Target margin 35% -> harga = HPP / (1 - 35%) = Rp 10.692,31 (setara markup 53,85%)
- **Harga rekomendasi: Rp 11.000** -> laba Rp 4.050 per bungkus (margin 36,82%, markup 58,27%)

**Titik impas (BEP) per bulan** pada harga Rp 11.000

- Biaya tetap bulanan: Rp 600.000 (biaya bulanan dalam HPP Rp 600.000 + penyusutan Rp 0 + biaya tetap lain Rp 0)
- Margin kontribusi per bungkus: Rp 5.300 (harga - biaya variabel Rp 5.700)
- **BEP: 114 bungkus per bulan** (tepatnya 113,21), atau omzet **Rp 1.245.284** per bulan
- BEP = 23,58% dari rencana produksi 480 bungkus

**Catatan**
- HPP ditampilkan sampai 2 angka desimal; harga rekomendasi dibulatkan KE ATAS ke kelipatan Rp 500 agar margin tidak kurang dari target.
- Biaya 'per bulan' dan penyusutan dibagi ke produksi per bulan. Jika penjualan lebih sedikit dari itu, HPP per unit sebenarnya naik.
- Margin = laba / harga jual. Markup = laba / HPP. Margin 30% setara markup 42,86%.

**Margin vs markup:** margin 35% artinya untung 35% **dari harga jual**; setara markup 53,85% dari modal. Kalau dihitung dengan markup 35% saja, harganya hanya Rp9.382,50 dan marginnya cuma 25,9% — jangan tertukar.

💡 Saran:
- Komponen terbesar adalah **pisang** (Rp2.000/bungkus, 29% HPP). Kenaikan harga pisang 10% menambah HPP Rp200/bungkus.
- Sewa dapur Rp1.250/bungkus berlaku jika produksi benar-benar 480 bungkus. Kalau hanya laku 240 bungkus, porsinya naik menjadi Rp2.500/bungkus.
- BEP 114 bungkus/bulan (24% rencana produksi) — cukup aman.

**Asumsi:** upah **Anda sendiri** sebagai pemilik belum dihitung (hanya upah pembantu Rp50.000/produksi); gas 1 tabung untuk 2 kali produksi; tidak ada susut bahan.

## Catatan penguji
- Angka dicek independen (Fraction): bahan (80.000 + 38.000 + 15.000) ÷ 40 = 3.325; HPP 6.950; 6.950 ÷ 0,65 = 10.692,31 → Rp11.000; BEP 600.000 ÷ 5.300 = 113,2 → 114; BEP rupiah Rp1.245.284. Benar.
- Konversi kg→g dan alokasi biaya bulanan (sewa ÷ 480) benar; biaya tetap tidak dihitung ganda di BEP.
- Penjelasan margin vs markup & saran berbasis angka ditambahkan agent sesuai langkah 4 SKILL.md.
