# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Mau hitung modal keripik pisang balado. Sekali produksi: pisang 10 kg (8 ribu/kg), minyak 2 liter (19 ribu/liter), bumbu balado 250 gram (beli 1 kg 60 ribu). Jadinya 40 bungkus. Standing pouch 85 ribu isi 100. Gas 3 kg 22 ribu buat 2x produksi. Upah yang bantu 50 ribu sekali produksi. Sewa dapur 600 ribu sebulan. Sebulan produksi 480 bungkus. Mau margin 35%, jual berapa?

## Output TANPA skill (AI agent biasa, tanpa membaca skill)
```
Biaya per produksi (40 bungkus):
- Pisang 10 kg x 8.000 = 80.000
- Minyak 2 x 19.000 = 38.000
- Bumbu 250 g = 15.000
- Pouch 40 x 850 = 34.000
- Gas = 11.000
- Upah = 50.000
Total = 228.000 → per bungkus = Rp5.700

Sewa 600.000 / 480 = Rp1.250 per bungkus
Modal per bungkus = Rp6.950

Harga jual dengan untung 35%: 6.950 x 1,35 = Rp9.382 → jual Rp9.500
```

## Output DENGAN skill
Lihat `01-keripik-pisang-margin-35.md`: tabel rincian per komponen (cara hitung, per batch/bulan, per bungkus), HPP Rp6.950 (variabel Rp5.700 + tetap Rp1.250), harga tepat margin 35% **Rp10.692,31 → Rp11.000** (margin 36,82%, markup 58,27%), BEP **114 bungkus/bulan** atau omzet Rp1.245.284, penjelasan margin vs markup, saran berbasis angka, dan asumsi (upah pemilik belum dihitung).

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| HPP per bungkus | Benar (Rp6.950) | Benar, dengan rincian per komponen |
| Harga untuk "margin 35%" | **Salah** — memakai markup (×1,35) → Rp9.500, margin sebenarnya hanya ±26,8% | Benar: HPP ÷ (1 − 35%) → Rp11.000, margin 36,82% |
| Selisih harga | | **Rp1.500 per bungkus** (≈ Rp720.000/bulan pada 480 bungkus) |
| BEP | Tidak ada | 114 bungkus/bulan + omzet BEP |
| Pemisahan biaya variabel vs tetap | Tidak | Ya |
| Asumsi (upah pemilik) | Tidak disebut | Disebut |

## Penilaian
Skill **jelas lebih baik**. Agent tanpa skill melakukan kesalahan paling umum di UMKM — menukar margin dengan markup — sehingga harga Rp1.500/bungkus terlalu murah dan margin nyata jauh di bawah target. Skill mencegahnya lewat rumus yang eksplisit dan menampilkan margin serta markup berdampingan, plus BEP yang tidak ada di jawaban biasa.
