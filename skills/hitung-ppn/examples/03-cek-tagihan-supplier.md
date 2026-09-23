# 03 — Mengecek PPN di tagihan supplier

**Skenario:** S3 — permintaan normal: admin keuangan mengecek tagihan supplier yang tampaknya memakai 12% penuh.

**Input pengguna (persis):**
> Supplier kirim tagihan: 20 unit kursi kantor @Rp 850.000 + PPN, katanya PPN 12% jadi totalnya Rp 19.040.000. Bener gak sih itungannya?

**Perintah yang dijalankan agent:**
```bash
python3 <folder-skill>/scripts/hitung_ppn.py --harga "850.000" --qty 20
```

## Output

**Perhitungan PPN** (barang/jasa biasa)
- Jumlah: 20 × Rp 850.000
- Harga sebelum PPN (DPP): Rp 17.000.000
- DPP nilai lain (11/12): Rp 15.583.333,33
- PPN 12%: **Rp 1.870.000** (setara 11% dari harga)
- **Total yang seharusnya: Rp 18.870.000**

**Perbandingan dengan tagihan supplier**
| | Tagihan supplier | Seharusnya (non-mewah) |
|---|---:|---:|
| PPN | Rp 2.040.000 (12% × 17 juta) | Rp 1.870.000 |
| Total | Rp 19.040.000 | Rp 18.870.000 |
| Selisih | | **Rp 170.000 lebih mahal** |

Kemungkinan supplier mengalikan 12% langsung ke harga. Sejak 2025, untuk barang biasa (bukan barang mewah) PPN 12% dikalikan ke DPP nilai lain (11/12 dari harga), sehingga efektif 11%. Kursi kantor umumnya bukan barang mewah. Saran: minta supplier merevisi tagihan dan mencocokkannya dengan faktur pajak dari Coretax — angka PPN di faktur pajak yang berlaku.

Pembulatan: PPN dibulatkan ke bawah ke rupiah penuh.
⚠️ Pastikan supplier memang PKP (cek NPWP/faktur pajaknya). Jika bukan PKP, ia tidak boleh memungut PPN sama sekali.

_Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Alat bantu hitung, bukan nasihat pajak; untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

## Catatan penguji
- Kasus bernilai tinggi bagi pembeli: skill menangkap kesalahan umum (12% penuh) dan menjelaskan selisihnya. Angka dicek independen: 17.000.000 × 11% = 1.870.000.
- Tabel perbandingan disusun agent (tidak ada di format output SKILL.md) — wajar, tetapi SKILL.md belum punya pola "cek tagihan"; bisa ditambahkan sebagai contoh.
