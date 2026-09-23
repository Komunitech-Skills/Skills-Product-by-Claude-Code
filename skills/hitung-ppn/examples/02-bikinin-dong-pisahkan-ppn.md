# 02 — "bikinin dong", harga sudah termasuk PPN

**Skenario:** S2 — permintaan singkat/malas. Status PKP tidak disebut.

**Input pengguna (persis):**
> bikinin dong itungan ppn, harga 3.330.000 udah include ppn

**Perintah yang dijalankan agent:**
```bash
python3 <folder-skill>/scripts/hitung_ppn.py --harga "3.330.000" --mode termasuk
```

## Output

**Perhitungan PPN** (barang/jasa biasa)
- Harga termasuk PPN: Rp 3.330.000
- Harga sebelum PPN (DPP): Rp 3.000.000
- DPP nilai lain (11/12): Rp 2.750.000
- PPN 12%: **Rp 330.000** (setara 11% dari DPP)
- **Total: Rp 3.330.000** (tanpa selisih pembulatan)

Cara hitung: DPP = 3.330.000 × 100/111 = Rp 3.000.000; PPN = 11% × 3.000.000 = Rp 330.000.
Pembulatan: PPN dibulatkan ke bawah ke rupiah penuh.

⚠️ Pastikan penjualnya sudah dikukuhkan sebagai PKP sebelum menagih PPN. Kalau belum PKP, jangan cantumkan PPN di tagihan — seluruh Rp 3.330.000 adalah harga jual biasa.

Asumsi: barang/jasa biasa (bukan barang mewah). Kalau barangnya kena PPnBM, kabari saya supaya dihitung ulang dengan 12% penuh.

_Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Alat bantu hitung, bukan nasihat pajak; untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

## Catatan penguji
- Default "belum tahu PKP" menghasilkan pengingat PKP otomatis dari script. Bagus.
- Angka benar (dicek independen: DPP bulat terbesar dengan DPP + floor(11% DPP) ≤ 3.330.000 → 3.000.000).
- Agent menyebut asumsi non-mewah sesuai tabel Input.
