# Contoh 2: Hampers Lebaran kue kering (bundling + harga cantik)

> Contoh kerja pembuat skill (bukan hasil uji independen). Toko dan angka fiktif. Angka dari `scripts/strategi_harga.py`.

## Input pengguna
"Mau bikin hampers Lebaran isi nastar, kastengel, putri salju masing-masing toples 250 g. Satuannya saya jual 85rb, 90rb, 80rb. Modal 38rb, 42rb, 33rb. Box kayu + pita + kartu 22 ribu. Enaknya hampers-nya dijual berapa? Kepikiran 219.900."

## Perintah yang dijalankan
```
python3 scripts/strategi_harga.py bundel --item "Nastar 250g:85000:38000" --item "Kastengel 250g:90000:42000" --item "Putri Salju 250g:80000:33000" --harga-bundel 219900 --biaya-tambahan 22000 --margin-min 35
python3 scripts/strategi_harga.py bundel ... --harga-bundel 229000 ...   (opsi pembanding)
python3 scripts/strategi_harga.py cantik --harga 229000 --hpp 135000 --margin-min 35
```

## Output agent

**Ringkasan:** Pasang **Rp229.000** (bukan Rp219.900). Hampers dibeli untuk hadiah: pembeli lebih peduli "cantik, siap kirim" daripada hemat Rp10.000. Margin tetap 41,05%.

**Asumsi:** margin minimum 35%; dijual lewat WA/IG (tanpa potongan); bukan PKP.

| | Rp219.900 | **Rp229.000** |
|---|---|---|
| Total beli satuan | Rp255.000 | Rp255.000 |
| Pembeli hemat | Rp35.100 (13,76%) | Rp26.000 (10,2%) |
| HPP paket (isi Rp113.000 + box Rp22.000) | Rp135.000 | Rp135.000 |
| Laba per hampers | Rp84.900 (38,61%) | **Rp94.000 (41,05%)** |
| Transaksi tambahan agar laba = jual satuan | 67,26% | 51,06% |

Harga hampers terendah yang aman (margin 35%): **Rp207.693**.

Kandidat harga cantik di sekitar Rp229.000: Rp219.900 (38,61%), Rp228.900 (41,02%), **Rp229.000** (41,05%), Rp229.900 (41,28%), Rp230.000 (41,3%) — semua di atas batas. Rp229.000 dipilih karena rapi dan tetap terasa "di bawah 230".

**Susunan 3 pilihan (good-better-best)** — HPP tiap pilihan perlu dihitung dulu dengan hitung-hpp:
- *Mini* (2 toples + kotak kertas) — pintu masuk untuk hadiah rekan kerja.
- *Favorit* (3 toples + box kayu) Rp229.000 — tandai "paling laris" bila memang terbukti.
- *Premium* (3 toples + kue tambahan + box kayu besar + kartu tulisan tangan + antar) ±1,5–2× Favorit.

**Aturan promo:** jangan didiskon mendekati Lebaran (permintaan tinggi). Bila ingin mendorong pesanan awal: "pesan sebelum H-21 gratis kartu ucapan custom" (tambahan HPP kecil) daripada potong harga.

_Angka dihitung dengan script dari data yang Anda berikan. Keputusan harga tetap di tangan Anda._
