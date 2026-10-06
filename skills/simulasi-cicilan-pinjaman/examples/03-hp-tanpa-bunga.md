# 03 — Input tidak lengkap

**Input:** "Mau kredit HP 8 juta 12 bulan, cicilannya berapa?"

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
> Jadi di kisaran bunga wajar, cicilan HP 8 juta/12 bulan ada di sekitar **Rp700–740 ribu per bulan**.
>
> Catatan: ini simulasi ilustratif, bukan penawaran atau nasihat keuangan — angka final mengikuti tabel angsuran resmi dari lembaga pembiayaannya.
>
> Biar saya hitung pasti (bukan ilustrasi), tolong jawab:
> 1. Dari penawarannya, bunganya berapa % dan per apa (bulan/tahun)? Flat atau efektif/anuitas?
> 2. Ada biaya admin/provisi/asuransi di muka, kalau ada berapa?
> 3. (Opsional) Penghasilan bersih kamu per bulan — biar saya cek apakah cicilan ini aman buat kantong.

**Catatan penguji:**
**SEBELUM 6,5** — langsung memberi tabel ilustrasi flat 1/1,5/2% per bulan (angka benar: Rp746.667/786.667/826.667, contoh DP 20% Rp629.333) yang realistis untuk kredit elektronik; tetapi menyebut "memory", berasumsi pengguna pemilik toko ("usahamu"), tanpa disclaimer.
**SESUDAH 7** — kerja dulu, ilustrasi berlabel "bukan tawaran", angka cocok script (Rp703.327/722.066/741.076), 3 pertanyaan tepat, disclaimer. Minus: ilustrasi bunga efektif 10–20%/tahun terlalu rendah untuk kredit HP (umumnya flat ±1–3%/bulan ≈ efektif ±20–60%/tahun), lalu disebut "kisaran bunga wajar ... Rp700–740 ribu" — klaim tanpa dasar yang bisa membuat pengguna meremehkan cicilan.
