# 03 — Input tidak lengkap

**Input:** "Mau kredit HP 8 juta 12 bulan, cicilannya berapa?"

**Output dengan skill v1.0.1:**

> Belum ada info bunganya, jadi ini ilustrasi kredit HP dengan bunga flat per bulan (asumsi ilustrasi; masukkan bunga dari penawaran Anda) — bukan tawaran lembaga mana pun:
>
> **Kredit HP 8 juta, 12 bulan — ilustrasi (belum tahu bunganya)**
>
> | Bunga flat | Cicilan/bulan | Total bunga | Efektif setara/tahun |
> |---|---|---|---|
> | 1,50%/bulan | Rp786.667 | Rp1.440.000 | 31,7% |
> | 2,00%/bulan | Rp826.667 | Rp1.920.000 | 41,7% |
> | 3,00%/bulan | Rp906.667 | Rp2.880.000 | 61,0% |
>
> Bunga 1,5%, 2%, dan 3% per bulan di tabel adalah asumsi ilustrasi; masukkan bunga dari penawaran Anda. Cicilan sebenarnya bisa lebih rendah atau lebih tinggi tergantung penyedia.
>
> Catatan: simulasi, bukan penawaran atau nasihat keuangan; angka final mengikuti tabel angsuran resmi lembaga pembiayaan.
>
> Supaya bisa saya hitungkan pasti (bukan ilustrasi):
> 1. Berapa bunga yang ditawarkan, dan per bulan/per tahun?
> 2. Itu bunga flat atau efektif/anuitas?
> 3. Ada biaya admin/asuransi di muka?

**Catatan penguji (uji ulang 1.0.1, penguji independen kedua):**
**SESUDAH 1.0.1: 8,5** — `tools: read, exec`. Ilustrasi kini flat 1,5% / 2% / 3% per bulan (Rp786.667 / Rp826.667 / Rp906.667; efektif setara 31,7% / 41,7% / 61,0% — cocok independen), berlabel "asumsi ilustrasi; masukkan bunga dari penawaran Anda", tanpa kata "wajar/normal/umum" dan tanpa kesimpulan "cicilanmu sekitar ...". 3 pertanyaan bernomor, disclaimer. Minus: tabel 4 kolom (aturan maks. 3 kolom), kalimat "bukan tawaran" diulang dua kali.

---

## Arsip uji 1.0.0

**Output dengan skill:**

> Belum ada info bunga/cicilan dari penawarannya, jadi ini ilustrasi dulu (bukan tawaran):
>
> **Simulasi cicilan HP — Rp8.000.000, 12 bulan (ilustrasi 3 angka bunga efektif/tahun)**
>
> | Bunga efektif/tahun | Cicilan/bulan | Total bunga |
> |---|---|---|
> | 10,0% | Rp703.327 | Rp439.924 |
> | 15,0% | Rp722.066 | Rp664.792 |
> | 20,0% | Rp741.076 | Rp892.912 |
>
> Bunga 10%, 15%, dan 20% per tahun di tabel adalah asumsi ilustrasi; masukkan bunga dari penawaran Anda.
>
> Catatan: ini simulasi ilustratif, bukan penawaran atau nasihat keuangan — angka final mengikuti tabel angsuran resmi dari lembaga pembiayaannya.
>
> Biar saya hitung pasti (bukan ilustrasi), tolong jawab:
> 1. Dari penawarannya, bunganya berapa % dan per apa (bulan/tahun)? Flat atau efektif/anuitas?
> 2. Ada biaya admin/provisi/asuransi di muka, kalau ada berapa?
> 3. (Opsional) Penghasilan bersih kamu per bulan — biar saya cek apakah cicilan ini aman buat kantong.

**Catatan penguji:**
**SEBELUM 6,5** — langsung memberi tabel ilustrasi flat 1/1,5/2% per bulan (angka benar: Rp746.667/786.667/826.667, contoh DP 20% Rp629.333); tetapi menyebut "memory", berasumsi pengguna pemilik toko ("usahamu"), tanpa disclaimer.
**SESUDAH 7** — kerja dulu, ilustrasi berlabel "bukan tawaran", angka cocok script (Rp703.327/722.066/741.076), 3 pertanyaan tepat, disclaimer. Minus: angka bunga ilustrasi 10–20%/tahun dipilih tanpa sumber dan semula disajikan sebagai kisaran pasar disertai kesimpulan cicilan; kini ditandai asumsi ilustrasi (diperbarui 2026-10-13). Ilustrasi yang tidak ditandai bisa membuat pengguna meremehkan cicilan.
