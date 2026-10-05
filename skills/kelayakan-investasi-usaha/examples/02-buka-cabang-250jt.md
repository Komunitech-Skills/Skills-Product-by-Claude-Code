# 02 — Buka cabang warung bakso Rp250 juta (skenario normal, hasil kurang layak)

> Contoh pembuat skill (v1.0.0, diperbarui v1.0.1: omzet impas memakai penyusutan sampai nilai sisa, NPV uji ketat 20%). Angka dari script, diverifikasi ulang dengan Python terpisah (NPV & IRR identik: 17.299.801 / 14,32%; tes `D10`–`D11`).

## Pesan pengguna
"Mau buka cabang kedua warung bakso. Modal 250 juta untuk renovasi, peralatan, dan modal awal. Perkiraan omzet tahun pertama 380 juta, lalu 470, 500, 520, 540 juta. Bahan baku 45% dari omzet. Gaji, sewa, listrik 14,5 juta sebulan, naik 5% per tahun. Peralatan mungkin laku 40 juta di tahun ke-5. Pajak PPh final 0,5%. Kapan balik modal, layak?"

```bash
python3 scripts/kelayakan.py --investasi 250jt --omzet "380jt;470jt;500jt;520jt;540jt" --hpp-persen 45 \
  --biaya 14,5jt/bulan --kenaikan-biaya 5 --nilai-sisa 40jt --pajak-persen 0,5 --format teks
```

## Verifikasi manual (tahun 1)
380.000.000 − 171.000.000 (45%) − 174.000.000 (14,5jt × 12) − 1.900.000 (0,5%) = **33.100.000**. Tahun 2: 470jt − 211,5jt − 182,7jt − 2,35jt = 73.450.000. Kumulatif menutup modal di tahun ke-4 → 3 + 62.785.000 ÷ 81.973.250 = 3,77 tahun. Omzet impas = (174.000.000 + (250jt − 40jt) ÷ 5) ÷ (1 − 0,45 − 0,005) = 396.330.275/tahun = **Rp33.027.523/bulan**. NPV 20% = **−Rp35.845.401**.

## Contoh balasan chat
**Cabang kedua Rp250 juta: KURANG LAYAK (dengan asumsi di bawah)**
Di atas kertas masih untung tipis (imbal hasil 14,3%/tahun vs patokan 12%), tetapi kalau omzet meleset 10% saja hasilnya sudah rugi dibanding patokan.

| Ukuran | Hasil | Arti |
|---|---|---|
| Balik modal | 3 tahun 9 bulan | dari uang bersih |
| Balik modal (nilai waktu uang) | belum dalam 5 tahun | butuh hasil jual peralatan di akhir |
| NPV | Rp17.299.801 | kelebihan tipis di atas patokan 12% |
| NPV uji ketat 20% | −Rp35.845.401 | rugi bila patokan 20%/tahun |
| IRR | 14,32%/tahun | hanya sedikit di atas 12% |
| PI | 1,07 | tiap Rp1 kembali Rp1,07 |
| Omzet impas | Rp33.027.523/bulan | tahun 1 (±Rp31,7 jt/bulan) masih di bawahnya |

Uji ketat: Bila hasil minimal yang diminta dinaikkan ke 20%/tahun (bunga lebih mahal atau risiko lebih besar), cabang ini tidak lagi menutup modal plus hasil itu.

| Tahun | Uang bersih | Kumulatif |
|---|---|---|
| 1 | Rp33.100.000 | −Rp216.900.000 |
| 2 | Rp73.450.000 | −Rp143.450.000 |
| 3 | Rp80.665.000 | −Rp62.785.000 |
| 4 | Rp81.973.250 | Rp19.188.250 |
| 5 | Rp122.801.912 (termasuk jual peralatan Rp40 jt) | Rp141.990.162 |

**Kalau meleset (NPV):** omzet −10% → −Rp75.717.359 · omzet −20% → −Rp168.734.518 · biaya +10% → −Rp128.060.244.
**Kenapa kurang layak:** batas amannya sangat sempit — omzet hanya boleh turun 1,9% dan biaya naik 1,2%. Hasil positif juga bergantung pada peralatan laku Rp40 juta di akhir.
**Agar layak:** omzet rata-rata minimal ±Rp38.721.639/bulan bila sama tiap tahun; atau tekan modal (peralatan bekas, renovasi bertahap) dan biaya tetap; atau uji dulu dengan gerobak/booth kecil.
**Asumsi:** patokan 12%/tahun (bunga KUR 6% + risiko usaha 6%, bisa diganti), masa 5 tahun, biaya tetap naik 5%/tahun, PPh final 0,5% dari omzet cabang.
Catatan: bukan nasihat keuangan; hasil tergantung asumsi, tidak ada jaminan untung.

Supaya lebih tajam:
1. Omzet 380 juta tahun pertama itu dari mana — perbandingan dengan cabang pertama di bulan-bulan awal?
2. Apakah sewa ruko dibayar di muka (masuk modal 250 juta) atau bulanan (masuk 14,5 juta)?
3. Modal dari tabungan atau pinjaman? Bila pinjaman, berapa bunganya?
