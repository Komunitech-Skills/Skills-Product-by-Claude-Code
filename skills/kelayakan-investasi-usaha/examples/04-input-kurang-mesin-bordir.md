# 04 — Input tidak lengkap: "Mesin bordir 85 juta, layak nggak?"

> Contoh pembuat skill (v1.0.0). Angka dari `--cari-minimal`, diverifikasi: 85.000.000 × 0,12 ÷ (1 − 1,12⁻⁵) = 23.579.827 per tahun (tes `H1`–`H3`).

## Pesan pengguna
"Saya mau beli mesin bordir komputer 85 juta. Layak nggak?"

## Perilaku yang diharapkan
Belum ada angka hasil (omzet/penghematan). Jangan membalas hanya dengan pertanyaan: hitung **uang bersih minimal** dulu, lalu tanya maks. 3 hal.
```bash
python3 scripts/kelayakan.py --investasi 85jt --cari-minimal --format teks
```

## Contoh balasan chat
Belum bisa saya putuskan layak atau tidak, karena perkiraan tambahan pemasukannya belum ada. Tapi ini patokannya:

| Patokan (masa 5 tahun) | Uang bersih minimal | Arti |
|---|---|---|
| Sekadar balik modal | Rp1.416.667/bulan | modal 85 juta kembali dalam 5 tahun |
| Layak (patokan 12%/tahun) | Rp1.964.986/bulan | modal kembali + hasil minimal 12%/tahun |

"Uang bersih" = tambahan omzet bordir − benang/bahan − listrik, servis, operator − pajak. Jadi kalau mesin ini menambah uang bersih **di atas ±Rp2 juta per bulan**, kemungkinan besar layak.

**Asumsi:** masa 5 tahun, patokan 12%/tahun (asumsi tingkat diskonto contoh; ganti dengan bunga pinjaman Anda + premi risiko yang Anda pilih), mesin dianggap tidak bernilai jual di akhir (hati-hati).
Catatan: bukan nasihat keuangan; hasil tergantung asumsi.

Jawab 3 hal ini, nanti saya hitung lengkap (balik modal, NPV, IRR, dan kalau omzet meleset):
1. Perkiraan tambahan order bordir per bulan (jumlah potong × harga, atau rupiah)?
2. Biaya benang/bahan per potong (atau persen dari harga) dan biaya rutin per bulan (listrik, operator, servis)?
3. Kira-kira mesin masih laku berapa setelah 5 tahun?
