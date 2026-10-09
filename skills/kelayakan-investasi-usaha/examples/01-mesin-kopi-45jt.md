# 01 — Beli mesin espresso Rp45 juta (skenario normal)

> Contoh pembuat skill (v1.0.0, diperbarui v1.0.1: NPV uji ketat 20%). Semua angka dari `scripts/kelayakan.py` dan diverifikasi ulang dengan hitungan Python terpisah (tes `C1`–`C14` di `tests/uji_kelayakan.py`). Belum diuji penguji independen.

## Pesan pengguna
"Kafe saya mau beli mesin espresso 45 juta. Tambahan jualan kira-kira 6 juta sebulan, bahan baku 40%, listrik + servis + part-time 1,2 juta sebulan. Mesin bekasnya mungkin laku 5 juta setelah 5 tahun. Saya bayar PPh final 0,5%. Layak nggak?"

## Pemetaan (catatan agent)
investasi 45jt · omzet 6jt/bulan · biaya variabel 40% · biaya tetap 1,2jt/bulan · 5 tahun · nilai sisa 5jt (penyusutan (45jt − 5jt) ÷ 5 = 8jt/th) · pajak 0,5% dari omzet · diskonto default 12%.
```bash
python3 scripts/kelayakan.py --investasi 45jt --omzet 6jt/bulan --hpp-persen 40 --biaya 1,2jt/bulan \
  --tahun 5 --nilai-sisa 5jt --pajak-persen 0,5 --format teks
```

## Verifikasi manual
Per tahun: omzet 72.000.000 − bahan 28.800.000 − biaya tetap 14.400.000 − pajak 360.000 = **28.440.000**; tahun 5 + nilai sisa 5.000.000 = 33.440.000.
NPV 12% = −45.000.000 + 28.440.000 × 3,604776 + 5.000.000 ÷ 1,12⁵ = **Rp60.356.969** (cocok). Balik modal = 1 + 16.560.000 ÷ 28.440.000 = 1,58 tahun. NPV 20% = −45.000.000 + 28.440.000 × 2,990612 + 5.000.000 ÷ 1,2⁵ = **Rp42.062.397** (tes `K1`).

## Contoh balasan chat
**Mesin espresso Rp45 juta: LAYAK (dengan asumsi di bawah)**
Modal kembali dalam ±1 tahun 7 bulan, dan imbal hasilnya 57,3% per tahun — jauh di atas patokan 12%.

| Ukuran | Hasil | Arti |
|---|---|---|
| Balik modal | 1 tahun 7 bulan | modal kembali dari uang bersih |
| Balik modal (nilai waktu uang) | 1 tahun 10 bulan | sudah memperhitungkan patokan 12%/tahun |
| NPV | Rp60.356.969 | kelebihan untung setara uang hari ini, patokan 12% |
| NPV uji ketat 20% | Rp42.062.397 | tetap positif dengan patokan 20%/tahun |
| IRR | 57,3%/tahun | layak bila > 12% |
| PI | 2,34 | tiap Rp1 modal kembali Rp2,34 |
| Omzet impas | Rp3.137.255/bulan | di bawah ini rugi di pembukuan |

Uji ketat: Bila hasil minimal yang diminta dinaikkan ke 20%/tahun (bunga lebih mahal atau risiko lebih besar), mesin ini masih menutup modal plus hasil itu.
Uang bersih ±Rp28.440.000 per tahun (Rp2.370.000/bulan) setelah bahan baku, biaya rutin, dan pajak 0,5%.

**Kalau meleset (NPV):** omzet −10% → Rp44.914.108 · omzet −20% → Rp29.471.247 · biaya +10% → Rp44.784.336. Ketiganya tetap layak.
**Syarat:** omzet tambahan tidak turun lebih dari 39,1% (minimal ±Rp3.654.956/bulan) dan biaya tidak naik lebih dari 38,8%.
**Asumsi:** patokan 12%/tahun (bunga KUR 6% + risiko usaha 6%, bisa diganti), masa 5 tahun, penyusutan rata Rp8 juta/tahun sampai nilai sisa Rp5 juta, PPh final 0,5% dari tambahan omzet.
Catatan: bukan nasihat keuangan; hasil tergantung asumsi, tidak ada jaminan untung.

Supaya lebih tajam:
1. Apakah 6 juta itu penjualan **tambahan**, bukan pindahan dari menu kopi lama?
2. Mesin dibeli tunai atau dicicil? Kalau dicicil, sebutkan bunganya — saya pakai sebagai patokan.
3. Omzet kafe setahun di atas Rp500 juta? (Kalau belum, PPh final bisa belum terutang dan hasilnya sedikit lebih baik.)
