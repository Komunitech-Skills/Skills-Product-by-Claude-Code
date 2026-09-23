# 04 — Input kurang: harga tidak disebut

**Skenario:** S4 — input tidak lengkap. Info wajib (harga) tidak ada.

**Input pengguna (persis):**
> Tolong pisahin PPN dari tagihan saya dong

## Output (balasan pertama — bertanya sekali)

Siap, saya bantu pisahkan PPN-nya. Saya perlu beberapa info dulu:

1. Berapa nilai tagihannya? (boleh ditulis `18.500.000` atau `18,5jt`)
2. Nilai itu **sudah termasuk** PPN, kan? (dari kata "pisahin" saya anggap sudah termasuk)
3. Barangnya barang/jasa biasa atau barang mewah (kena PPnBM)? Kalau tidak yakin, saya anggap biasa.
4. Penjualnya sudah PKP?

**Balasan pengguna:**
> 18,5 juta, iya udah termasuk, jasa konsultasi biasa, saya PKP

**Perintah:** `python3 <folder-skill>/scripts/hitung_ppn.py --harga "18,5jt" --mode termasuk --status-pkp pkp`

## Output (balasan kedua)

**Perhitungan PPN** (barang/jasa biasa)
- Harga termasuk PPN: Rp 18.500.000
- Harga sebelum PPN (DPP): Rp 16.666.667
- DPP nilai lain (11/12): Rp 15.277.778,08
- PPN 12%: **Rp 1.833.333** (setara 11% dari DPP)
- **Total: Rp 18.500.000** (tanpa selisih pembulatan)

Cara hitung: DPP = 18.500.000 × 100/111 ≈ Rp 16.666.667; PPN = 11% × 16.666.667 = Rp 1.833.333,37 → dibulatkan ke bawah Rp 1.833.333. DPP + PPN = Rp 18.500.000 pas.
Pembulatan: PPN dibulatkan ke bawah ke rupiah penuh. Angka di Coretax bisa berbeda Rp1 pada kasus tertentu; bila berbeda, ikuti Coretax.

_Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Alat bantu hitung, bukan nasihat pajak; untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

## Catatan penguji
- Bertanya sekali, 4 pertanyaan bernomor, dengan default yang disebut — sesuai aturan SKILL.md.
- Angka dicek independen (brute force DPP terbesar yang muat): 16.666.667 / 1.833.333. Benar.
