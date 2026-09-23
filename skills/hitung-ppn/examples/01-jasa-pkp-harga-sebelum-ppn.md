# 01 — Jasa PKP, harga belum termasuk PPN

**Skenario:** S1 — permintaan normal. Pemilik usaha jasa IT yang sudah PKP ingin tahu PPN dan total tagihan.

**Input pengguna (persis):**
> Saya PKP, mau tagih jasa maintenance server ke klien Rp 12.500.000 belum termasuk PPN. PPN-nya berapa dan totalnya jadi berapa?

**Perintah yang dijalankan agent:**
```bash
python3 <folder-skill>/scripts/hitung_ppn.py --harga "12.500.000" --mode sebelum --jenis umum --status-pkp pkp
```

## Output

**Perhitungan PPN** (barang/jasa biasa)
- Harga sebelum PPN (DPP): Rp 12.500.000
- DPP nilai lain (11/12): Rp 11.458.333,33
- PPN 12%: **Rp 1.375.000** (setara 11% dari harga)
- **Total dibayar klien: Rp 13.875.000**

Cara hitung: DPP nilai lain = 11/12 × Rp 12.500.000 = Rp 11.458.333,33; PPN = 12% × Rp 11.458.333,33 = Rp 1.375.000 (sama dengan 11% × Rp 12.500.000).
Pembulatan: PPN dibulatkan ke bawah ke rupiah penuh (di kasus ini tidak ada pecahan).

Karena Anda sudah PKP, PPN ini boleh ditagihkan. Faktur pajaknya tetap dibuat di Coretax; angka DPP nilai lain Rp 11.458.333,33 dan PPN Rp 1.375.000 di atas bisa dipakai untuk mengecek isian faktur.

_Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Alat bantu hitung, bukan nasihat pajak; untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

## Catatan penguji
- Angka dicek dengan script independen (Fraction): 11/12 × 12% × 12.500.000 = 1.375.000 persis. Benar.
- Format sesuai SKILL.md; asumsi "jasa biasa (non-mewah)" wajar untuk jasa maintenance.
- Bagus: menyebut DPP nilai lain, yang diperlukan saat mengisi faktur.
