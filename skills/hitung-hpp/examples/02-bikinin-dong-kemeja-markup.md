# 02 — "bikinin dong" HPP kemeja (yard → meter, gross → pcs, markup 60%)

**Skenario:** S2 — permintaan singkat/malas, konveksi dengan penyusutan mesin dan biaya tetap di luar produksi.

**Input pengguna (persis):**
> bikinin dong hpp kemeja: kain 1,6 m beli per yard 45rb, kancing 1 gross 15rb pake 7, jahit 35rb, plastik 800, sewa 1,5jt/bln, mesin jahit 4,8jt umur 5 th, admin 1jt/bln, 200 kemeja sebulan. markup 60%

**Yang dilakukan agent:** menyusun CSV sederhana (`hpp-kemeja.csv`), mesin jahit 5 tahun = 60 bulan, lalu:
```bash
python3 <folder-skill>/scripts/hitung_hpp.py --file hpp-kemeja.csv --produksi-per-bulan 200 --nama-produk "Kemeja Katun" --satuan-produk kemeja --markup 60
```
<details><summary>Isi hpp-kemeja.csv</summary>

```
kategori;nama;harga_beli;isi_beli;satuan_beli;pakai;satuan_pakai;biaya;per;harga;umur_bulan
bahan;Kain katun;45.000;1;yard;1,6;m;;;;
bahan;Kancing;15.000;1;gross;7;pcs;;;;
tenaga_kerja;Ongkos jahit;;;;;;35.000;unit;;
kemasan;Plastik;;;;;;800;unit;;
overhead;Sewa tempat;;;;;;1.500.000;bulan;;
alat;Mesin jahit;;;;;;;;4.800.000;60
biaya_tetap;Admin;;;;;;1jt;;;
```
</details>

## Output

## HPP Kemeja Katun (per kemeja)

Hasil per batch: 1 kemeja | Produksi per bulan: 200 kemeja

| Kategori | Komponen | Cara hitung | Biaya | Per kemeja |
|---|---|---|---:|---:|
| Bahan baku | Kain katun | Rp 45.000 / 1 yard x pakai 1,6 m | Rp 78.740,16 /batch | Rp 78.740,16 |
| Bahan baku | Kancing | Rp 15.000 / 1 gross x pakai 7 pcs | Rp 729,17 /batch | Rp 729,17 |
| Tenaga kerja | Ongkos jahit | biaya langsung | Rp 35.000 /unit | Rp 35.000 |
| Overhead | Sewa tempat | biaya langsung | Rp 1.500.000 /bulan | Rp 7.500 |
| Kemasan | Plastik | biaya langsung | Rp 800 /unit | Rp 800 |
| Penyusutan alat | Mesin jahit | (Rp 4.800.000 - sisa Rp 0) / 60 bulan | Rp 80.000 /bulan | Rp 400 |

**Ringkasan HPP per kemeja**

- Bahan baku: Rp 79.469,32
- Tenaga kerja: Rp 35.000
- Overhead: Rp 7.500
- Kemasan: Rp 800
- Penyusutan alat: Rp 400
- **HPP per kemeja: Rp 123.169,32**
  - biaya variabel Rp 115.269,32 + biaya tetap dialokasikan Rp 7.900

**Harga jual** (dibulatkan ke atas kelipatan Rp 500)

- Markup 60% -> harga = HPP x (1 + 60%) = Rp 197.070,92 (setara margin 37,5%)
- **Harga rekomendasi: Rp 197.500** -> laba Rp 74.330,68 per kemeja (margin 37,64%, markup 60,35%)

**Titik impas (BEP) per bulan** pada harga Rp 197.500

- Biaya tetap bulanan: Rp 2.580.000 (biaya bulanan dalam HPP Rp 1.500.000 + penyusutan Rp 80.000 + biaya tetap lain Rp 1.000.000)
- Margin kontribusi per kemeja: Rp 82.230,68 (harga - biaya variabel Rp 115.269,32)
- **BEP: 32 kemeja per bulan** (tepatnya 31,38), atau omzet **Rp 6.196.593** per bulan
- BEP = 15,69% dari rencana produksi 200 kemeja

**Catatan**
- HPP ditampilkan sampai 2 angka desimal; harga rekomendasi dibulatkan KE ATAS ke kelipatan Rp 500 agar margin tidak kurang dari target.
- Biaya 'per bulan' dan penyusutan dibagi ke produksi per bulan. Jika penjualan lebih sedikit dari itu, HPP per unit sebenarnya naik.
- Margin = laba / harga jual. Markup = laba / HPP. Margin 30% setara markup 42,86%.

**Margin vs markup:** markup 60% dari modal setara margin 37,5% dari harga jual.

💡 Saran:
- **Kain** menyumbang 64% HPP (Rp78.740/kemeja). 1 yard = 0,9144 m, jadi 1,6 m ≈ 1,75 yard. Nego harga kain per rol bisa paling berpengaruh.
- Laba Rp74.330 per kemeja di atas adalah **sebelum** biaya admin Rp1 juta/bulan (≈ Rp5.000 per kemeja bila 200 kemeja). Biaya admin sudah masuk BEP (32 kemeja/bulan).

**Asumsi:** upah pemilik belum dihitung; nilai sisa mesin jahit Rp0.

## Catatan penguji
- Konversi yard→meter (91,44 cm) dan gross→pcs (144) benar: 45.000 ÷ 0,9144 × 1,6 = 78.740,16; 15.000 ÷ 144 × 7 = 729,17. Dicek independen.
- BEP: biaya tetap 1.500.000 + 80.000 + 1.000.000 = 2.580.000; kontribusi 82.230,68 → 31,38 → 32 kemeja. Benar.
- Kurang: output script menulis "laba Rp 74.330,68 per kemeja" tanpa menyebut bahwa biaya tetap lain (admin) belum dikurangkan; awam bisa mengira itu laba bersih. Agent harus menambahkan penjelasan (lihat cacat ringan di HASIL-UJI).
