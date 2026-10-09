# 02 — Normal kedua

**Input:** "KPR 500 juta DP 10%, 15 tahun, bunga fixed 5% selama 3 tahun lalu floating 11%, provisi 1%. Berapa cicilan per bulan sebelum dan sesudah fixed berakhir, dan total bunganya?"

**Output dengan skill v1.0.1:**

> **Simulasi KPR — pokok Rp450.000.000 (harga Rp500.000.000, DP 10%), tenor 15 tahun**
> Cicilan bulan 1–36 (fixed): **Rp3.558.571/bulan** · Cicilan bulan 37–180 (floating): **Rp4.823.129/bulan**
> Total bayar Rp822.639.197 · Total bunga Rp372.639.197
>
> | Hal | Angka |
> |---|---|
> | Harga tunai / DP | Rp500.000.000 / Rp50.000.000 |
> | Pokok pinjaman | Rp450.000.000 |
> | Biaya di muka (provisi 1%) | Rp4.500.000 |
> | Pinjaman bersih setelah biaya di muka | Rp445.500.000 |
> | Total biaya pinjaman | Rp377.139.197 (bunga + provisi) |
> | Total harga lewat kredit | Rp877.139.197 (lebih mahal Rp377.139.197 dari tunai) |
>
> Bunga efektif setara (anuitas, rata-rata sepanjang tenor): **±8,49%/tahun** (tanpa biaya), **±8,65%/tahun** dengan provisi (majemuk ±9,00%). Lebih mahal Rp377.139.197 itu jumlah bunga + biaya selama 15 tahun, bukan kenaikan harga rumah.
>
> **Jadwal angsuran per tahun** (Tahun | Pokok dibayar | Bunga dibayar | Sisa utang):
> | Tahun | Pokok | Bunga | Sisa |
> |---|---|---|---|
> | 1 | Rp20.672.324 | Rp22.030.528 | Rp429.327.676 |
> | 2 | Rp21.729.960 | Rp20.972.892 | Rp407.597.716 |
> | 3 | Rp22.841.706 | Rp19.861.146 | Rp384.756.010 |
> | 4 | Rp16.363.050 | Rp41.514.498 | Rp368.392.960 (mulai bulan ke-37: bunga 11,00%/tahun, cicilan Rp4.823.129) |
> | 5 | Rp18.256.564 | Rp39.620.984 | Rp350.136.396 |
> | 6 | Rp20.369.191 | Rp37.508.357 | Rp329.767.205 |
> | 7 | Rp22.726.290 | Rp35.151.258 | Rp307.040.915 |
> | 8 | Rp25.356.149 | Rp32.521.399 | Rp281.684.766 |
> | 9 | Rp28.290.334 | Rp29.587.214 | Rp253.394.432 |
> | 10 | Rp31.564.059 | Rp26.313.489 | Rp221.830.373 |
> | 11 | Rp35.216.616 | Rp22.660.932 | Rp186.613.757 |
> | 12 | Rp39.291.842 | Rp18.585.706 | Rp147.321.915 |
> | 13 | Rp43.838.647 | Rp14.038.901 | Rp103.483.268 |
> | 14 | Rp48.911.605 | Rp8.965.943 | Rp54.571.663 |
> | 15 | Rp54.571.663 | Rp3.305.950 | Rp0 |
>
> **Yang perlu diperhatikan:**
> - Biaya provisi Rp4.500.000 menaikkan bunga efektif setara dari ±8,5% jadi ±8,6%/tahun (+0,2%).
> - Cicilan **naik** saat fixed berakhir: Rp3.558.571 → Rp4.823.129/bulan (mulai bulan ke-37).
> - Bunga 11% floating itu asumsi dari angka yang kamu sebut; bunga floating sebenarnya ditentukan bank saat itu tiba, bisa lebih tinggi atau lebih rendah.
>
> **Asumsi:** bunga anuitas/efektif; bunga bertahap 5%/tahun selama 36 bulan lalu 11%/tahun selama 144 bulan, cicilan dihitung ulang di awal tahap kedua dari sisa pokok; provisi 1% dibayar tunai di muka; pembulatan rupiah per bulan.
>
> Catatan: simulasi, bukan penawaran atau nasihat keuangan; angka final mengikuti tabel angsuran resmi lembaga pembiayaan.
>
> Ada biaya lain di muka (admin, asuransi jiwa/kebakaran, notaris)? Berapa penghasilan bersih per bulan biar saya cek rasio cicilan amannya? Mau dibandingkan kalau DP dinaikkan jadi 20-30%?

**Catatan penguji (uji ulang 1.0.1, penguji independen kedua):**
**SESUDAH 1.0.1: 9** — `tools: read, exec`. Angka persis & cocok independen (Rp3.558.571 → Rp4.823.129 mulai bulan ke-37, sisa pokok akhir bulan 36 Rp384.756.010, total bunga Rp372.639.197, EIR ±8,49% / ±8,65% dengan provisi, majemuk ±9,00%, jadwal 15 tahun cocok per baris). Cacat 1.0.0 hilang: catatan tahun ke-4 kini disalin dari hasil hitungan ("mulai bulan ke-37: bunga 11,00%/tahun ...") tanpa anotasi karangan; "lebih mahal" diberi kalimat netral "jumlah bunga + biaya ..., bukan kenaikan harga rumah". Minus kecil: frasa "biar saya cek rasio" (kata proses yang dilarang, meski bermakna wajar), tabel jadwal 4 kolom (diizinkan).

---

## Arsip uji 1.0.0

**Output dengan skill:**

> **Simulasi KPR Rp500.000.000 — DP 10%, tenor 15 tahun**
> Cicilan tahap fixed: **Rp3.558.571/bulan** (bulan 1–36) → tahap floating: **Rp4.823.129/bulan** (bulan 37–180)
> Bunga 5%/tahun (fixed) lalu 11%/tahun (floating) efektif/anuitas = **bunga efektif setara ±8,49%/tahun** (tanpa biaya); **±8,65%/tahun** termasuk biaya provisi
>
> | Hal | Angka |
> |---|---|
> | Harga tunai / DP | Rp500.000.000 / Rp50.000.000 |
> | Pokok pinjaman | Rp450.000.000 |
> | Biaya di muka | Rp4.500.000 (provisi 1%) |
> | Uang yang benar-benar diterima | Rp445.500.000 |
> | Total biaya pinjaman | Rp377.139.197 (bunga + biaya) |
> | Total harga lewat kredit | Rp877.139.197 (lebih mahal Rp377.139.197 = 75,4% dari harga tunai) |
>
> **Jadwal angsuran per tahun** (Tahun | Pokok dibayar | Bunga dibayar | Sisa utang):
> 1 | Rp20.672.324 | Rp22.030.528 | Rp429.327.676
> 2 | Rp21.729.960 | Rp20.972.892 | Rp407.597.716
> 3 | Rp22.841.706 | Rp19.861.146 | Rp384.756.010
> 4 | Rp16.363.050 | Rp41.514.498 | Rp368.392.960 *(tahun ini bulan 1-3 masih fixed, bulan 4-12 sudah floating → cicilan naik di tengah tahun)*
> 5 | Rp18.256.564 | Rp39.620.984 | Rp350.136.396
> 6 | Rp20.369.191 | Rp37.508.357 | Rp329.767.205
> 7 | Rp22.726.290 | Rp35.151.258 | Rp307.040.915
> 8 | Rp25.356.149 | Rp32.521.399 | Rp281.684.766
> 9 | Rp28.290.334 | Rp29.587.214 | Rp253.394.432
> 10 | Rp31.564.059 | Rp26.313.489 | Rp221.830.373
> 11 | Rp35.216.616 | Rp22.660.932 | Rp186.613.757
> 12 | Rp39.291.842 | Rp18.585.706 | Rp147.321.915
> 13 | Rp43.838.647 | Rp14.038.901 | Rp103.483.268
> 14 | Rp48.911.605 | Rp8.965.943 | Rp54.571.663
> 15 | Rp54.571.663 | Rp3.305.950 | Rp0
>
> **Yang perlu diperhatikan:**
> - Cicilan **naik otomatis** saat masa fixed berakhir: Rp3.558.571 → Rp4.823.129 per bulan (kenaikan Rp1.264.558, atau +35,5%), dihitung ulang dari sisa pokok Rp384.756.010 pada awal bulan ke-37.
> - Angka 11%/tahun untuk periode floating hanyalah **asumsi/perkiraan** — bunga floating sesungguhnya ditentukan bank saat itu dan bisa naik/turun dari angka ini.
> - Biaya provisi 1% (Rp4.500.000) menaikkan bunga efektif setara dari 8,49% jadi 8,65%/tahun.
>
> **Asumsi:** Bunga dihitung cara efektif/anuitas (menurun), bukan flat. Cicilan dihitung ulang di awal tiap tahap dari sisa pokok. Provisi 1% dibayar tunai di muka. Tidak ada asuransi/biaya bulanan lain yang dimasukkan karena tidak disebutkan.
>
> Catatan: simulasi, bukan penawaran atau nasihat keuangan; angka final mengikuti tabel angsuran resmi lembaga pembiayaan.
>
> Tiga hal yang bisa mengubah hasil ini: (1) Bunga floating 11% itu asumsi dari Kakak atau sudah ada indikasi dari bank? (2) Ada biaya lain di muka seperti asuransi jiwa/kebakaran atau notaris? (3) Perlu dibandingkan dengan skema fixed lebih lama (misalnya 5 tahun) untuk lihat selisihnya?

**Catatan penguji:**
**SEBELUM 7** — cicilan ≈Rp3.558.600 → ≈Rp4.823.000 dan total bunga ≈Rp372.644.000 benar sebagai pembulatan kasar (selisih sisa pokok ±Rp5.000), ditandai "≈"; tidak ada bunga efektif setara, tanpa jadwal, tanpa disclaimer.
**SESUDAH 8** — angka persis & cocok independen (Rp3.558.571 → Rp4.823.129, naik Rp1.264.558 = +35,5%, sisa pokok Rp384.756.010, total bunga Rp372.639.197, EIR 8,49%/8,65% dengan provisi, total biaya Rp377.139.197), jadwal per tahun 15 baris, floating ditandai perkiraan, disclaimer, 3 pertanyaan. Minus: anotasi tahun ke-4 SALAH ("bulan 1-3 masih fixed") — masa fixed 36 bulan habis tepat di akhir tahun 3; baris "Uang yang benar-benar diterima" dan "75,4% lebih mahal dari harga tunai" tanpa penjelasan untuk KPR terasa menakutkan bagi awam.
