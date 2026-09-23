# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Aku jual hijab voal, modal 28 ribu udah sama packing. Di Shopee admin aku 8,25%, ikut gratis ongkir xtra 4% maks 20 ribu, biaya proses 1.250 per pesanan. Mau untung 25% dari harga jual. Harga jualnya berapa? Aku belum nyerahin surat pernyataan omzet ke Shopee.

## Output TANPA skill (AI agent biasa, tanpa membaca skill)
```
Total potongan persen = 8,25% + 4% = 12,25%
Target untung 25%

Harga jual = (28.000 + 1.250) / (1 − 0,1225 − 0,25)
           = 29.250 / 0,6275
           = Rp46.614 → dibulatkan Rp47.000

Di harga Rp47.000:
- Admin 8,25% = Rp3.878
- Gratis ongkir 4% = Rp1.880
- Biaya proses = Rp1.250
- Diterima = Rp39.992
- Untung = Rp11.992 (25,5%)

Soal surat pernyataan, itu terkait pajak; sebaiknya tanyakan ke Shopee.
```

## Output DENGAN skill
Lihat `01-hijab-shopee-target-margin.md`: harga minimal Rp33.525, harga tepat Rp46.988, **rekomendasi Rp47.000**, rincian termasuk **PPh 22 0,5% (Rp235)**, laba **Rp11.758 (margin 25,02%)**, markup 41,99%, catatan asumsi (dasar biaya, sumber persen, pengecualian PPh 22 dengan surat pernyataan), dan saran hitung ulang tanpa PPh 22 setelah surat pernyataan diserahkan.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| PPh 22 marketplace 0,5% | **Terlewat** — padahal pengguna sendiri menyinggungnya; laba dilebih-lebihkan Rp235/barang | Dihitung, dan pengecualiannya dijelaskan (OP, omzet ≤ Rp500 juta, surat pernyataan) |
| Harga tepat target | Rp46.614 (salah karena PPh 22 terlewat) | Rp46.988 (diverifikasi independen) |
| Harga minimal (impas) | Tidak ada | Rp33.525 |
| Batas maks biaya layanan | Diabaikan (kebetulan tidak berpengaruh) | Diperhitungkan otomatis |
| Margin vs markup | Hanya margin | Keduanya |
| Catatan asumsi & tanggal berlaku | Tidak ada | Ada |

## Penilaian
Skill **jelas lebih baik**: agent tanpa skill melewatkan PPh 22 (sehingga harga tepat dan laba salah) dan tidak memberi harga impas. Pada contoh ini harga bulat tetap Rp47.000 karena pembulatan, tetapi untuk produk lain selisihnya bisa menggeser harga rekomendasi.
