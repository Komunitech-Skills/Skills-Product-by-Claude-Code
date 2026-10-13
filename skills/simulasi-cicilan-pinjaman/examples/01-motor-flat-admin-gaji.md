# 01 — Normal utama

**Input:** "Mau ambil motor 25 juta, DP 20%, 3 tahun, bunga 0,8% per bulan flat, admin 1 juta. Gaji saya 6 juta, sudah ada cicilan HP 500 ribu. Cicilannya berapa dan aman nggak?"

**Output dengan skill v1.0.1 (lokal):**

> **Simulasi cicilan motor — Rp25.000.000, 36 bulan**
> Cicilan: **Rp715.556/bulan** (36 kali, terakhir Rp715.540) · Total bayar Rp25.760.000 · Total bunga Rp5.760.000
> Bunga 0,8%/bulan flat = **efektif setara ±17,25%/tahun**; dengan biaya admin **±20,97%/tahun** (majemuk ±23,11%)
>
> | Hal | Angka |
> |---|---|
> | Harga tunai / DP | Rp25.000.000 / Rp5.000.000 |
> | Pokok pinjaman | Rp20.000.000 |
> | Biaya di muka | Rp1.000.000 (admin) |
> | Pinjaman bersih setelah biaya di muka | Rp19.000.000 |
> | Total biaya pinjaman | Rp6.760.000 |
> | Total harga lewat kredit | Rp31.760.000 (lebih mahal Rp6.760.000 = 27,0% dari tunai) |
>
> **Flat vs anuitas pada angka yang sama:** flat Rp715.556/bulan (total bunga Rp5.760.000) vs anuitas Rp641.594/bulan (total bunga Rp3.097.395) — selisih Rp2.662.605.
>
> **Jadwal angsuran per tahun** — Tahun | Pokok dibayar | Bunga dibayar | Sisa utang
> 1 | Rp6.666.672 | Rp1.920.000 | Rp13.333.328
> 2 | Rp6.666.672 | Rp1.920.000 | Rp6.666.656
> 3 | Rp6.666.656 | Rp1.920.000 | Rp0
>
> **Kemampuan bayar:** cicilan maksimal aman Rp1.300.000 (30% dari gaji Rp6.000.000, dikurangi cicilan HP Rp500.000; patokan hati-hati yang dipakai simulasi ini, bukan aturan resmi); cicilan motor ini masuk rasio total 20,3% → **AMAN**. Pinjaman maksimal aman dengan bunga & tenor sama ±Rp36.335.404.
>
> **Yang perlu diperhatikan:**
> - Bunga flat 0,8%/bulan terasa kecil tapi efektif setaranya ±17,25%/tahun karena bunga dihitung dari pokok awal, bukan sisa utang yang terus mengecil.
> - Biaya admin Rp1 juta menaikkan bunga efektif setara jadi ±20,97%/tahun (+3,7%).
> - Secara total, beli kredit lebih mahal Rp6.760.000 (27%) dibanding bayar tunai.
>
> **Asumsi:** bunga flat per bulan, DP 20% dihitung dari harga Rp25.000.000, biaya admin dibayar tunai di muka, pembulatan rupiah (selisih -Rp16 di cicilan terakhir).
>
> Catatan: simulasi, bukan penawaran atau nasihat keuangan; angka final mengikuti tabel angsuran resmi lembaga pembiayaan.
>
> Pertanyaan: ada biaya lain di muka (asuransi, provisi)? DP mau dinaikkan supaya cicilan lebih ringan? mau dibandingkan dengan penawaran leasing lain?

**Output dengan skill v1.0.1 (konteks Telegram):**

> **Simulasi cicilan motor — pokok Rp20.000.000 (harga Rp25.000.000, DP 20%), tenor 3 tahun**
> Cicilan: **Rp715.556/bulan** (36 kali; cicilan terakhir Rp715.540) · Total bayar Rp25.760.000 · Total bunga Rp5.760.000
> Bunga 0,8%/bulan flat = **efektif setara ±17,25%/tahun**; dengan biaya admin Rp1 juta jadi **±20,97%/tahun**
>
> | Hal | Angka |
> |---|---|
> | Harga tunai / DP | Rp25.000.000 / Rp5.000.000 |
> | Pokok pinjaman | Rp20.000.000 |
> | Biaya di muka | Rp1.000.000 (admin) |
> | Pinjaman bersih setelah biaya di muka | Rp19.000.000 |
> | Total biaya pinjaman | Rp6.760.000 (bunga + admin) |
> | Total harga lewat kredit | Rp31.760.000 (lebih mahal Rp6.760.000 = 27,0% dari tunai) |
>
> **Flat vs anuitas pada angka yang sama:** flat Rp715.556/bulan (total bunga Rp5.760.000) vs anuitas Rp641.594/bulan (total bunga Rp3.097.395) — selisih Rp2.662.605 lebih hemat kalau anuitas.
>
> **Jadwal angsuran per tahun:**
> | Tahun | Pokok dibayar | Bunga dibayar | Sisa utang |
> |---|---|---|---|
> | 1 | Rp6.666.672 | Rp1.920.000 | Rp13.333.328 |
> | 2 | Rp6.666.672 | Rp1.920.000 | Rp6.666.656 |
> | 3 | Rp6.666.656 | Rp1.920.000 | Rp0 |
>
> **Kemampuan bayar:** cicilan maksimal aman Rp1.300.000 (30% dari gaji bersih Rp6.000.000, sudah dikurangi cicilan HP Rp500.000; patokan hati-hati yang dipakai simulasi ini, bukan aturan resmi); cicilan motor ini masuk total cicilan 20,3% dari gaji → **AMAN**. Dengan bunga & tenor yang sama, pinjaman maksimal aman buat kamu sekitar Rp36.335.404.
>
> **Yang perlu diperhatikan:**
> - Bunga flat 0,8%/bulan terasa kecil tapi dihitung dari pokok awal terus, jadi setara efektif ±17,25%/tahun, bukan 9,6%/tahun.
> - Biaya admin Rp1 juta di muka menaikkan bunga efektif setara jadi ±20,97%/tahun.
>
> **Asumsi:** bunga flat, satuan per bulan sesuai yang disebutkan, biaya admin dibayar tunai di muka, pembulatan rupiah (selisih -Rp16 di cicilan terakhir).
>
> Catatan: simulasi, bukan penawaran atau nasihat keuangan; angka final mengikuti tabel angsuran resmi lembaga pembiayaan.
>
> Kesimpulan singkat: aman secara rasio (20,3% < 30%), tapi masih ada ruang untuk cicilan lain sampai Rp1.300.000 total. Mau saya bandingkan dengan skema anuitas (lebih hemat bunga), atau ada biaya asuransi/provisi lain yang belum disebut?

**Catatan penguji (uji ulang 1.0.1, penguji independen kedua):**
**SESUDAH 1.0.1: 9** (lokal 9, Telegram 9) — `tools: read, exec` di kedua konteks. Semua angka cocok hitungan independen (cicilan Rp715.556/terakhir Rp715.540, total bunga Rp5.760.000, EIR ±17,25% / ±20,97% dengan admin, majemuk ±23,11%, anuitas Rp641.594 & selisih Rp2.662.605, maks aman Rp1.300.000, rasio total 20,3%, pinjaman maks ±Rp36.335.404, +27,0% dari tunai). Perbaikan 1.0.0 terbukti: label "Pinjaman bersih setelah biaya di muka", tidak lagi bertanya "benar flat?", tidak ada klaim keliru cicilan berubah bila admin dipotong. Minus kecil (Telegram): kalimat penutup "masih ada ruang untuk cicilan lain sampai Rp1.300.000 total" ambigu (sisa ruang sebenarnya Rp584.444) dan menawarkan perbandingan anuitas yang sudah ditampilkan.

---

## Arsip uji 1.0.0

**Output dengan skill (konteks Telegram; versi lokal identik angkanya):**

> **Simulasi cicilan motor — Rp25.000.000, tenor 3 tahun**
> Cicilan: **Rp715.556/bulan** (36 kali; cicilan terakhir Rp715.540) · Total bayar Rp25.760.000 · Total bunga Rp5.760.000
> Bunga 0,8%/bulan flat = **bunga efektif setara ±17,25%/tahun**; dengan admin Rp1 juta **±20,97%/tahun**
>
> | Hal | Angka |
> |---|---|
> | Harga tunai / DP | Rp25.000.000 / Rp5.000.000 |
> | Pokok pinjaman | Rp20.000.000 |
> | Biaya di muka | Rp1.000.000 (admin) |
> | Uang yang benar-benar diterima | Rp19.000.000 |
> | Total biaya pinjaman | Rp6.760.000 (bunga + admin) |
> | Total harga lewat kredit | Rp31.760.000 (lebih mahal Rp6.760.000 = 27,0% dari tunai) |
>
> **Flat vs anuitas pada angka yang sama:** flat Rp715.556/bulan (total bunga Rp5.760.000) vs anuitas Rp641.594/bulan (total bunga Rp3.097.395) — selisih Rp2.662.605 lebih mahal karena flat.
>
> **Jadwal angsuran per tahun:**
> | Tahun | Pokok dibayar | Bunga dibayar | Sisa utang |
> |---|---|---|---|
> | 1 | Rp6.666.672 | Rp1.920.000 | Rp13.333.328 |
> | 2 | Rp6.666.672 | Rp1.920.000 | Rp6.666.656 |
> | 3 | Rp6.666.656 | Rp1.920.000 | Rp0 |
>
> **Kemampuan bayar:** cicilan maksimal aman Rp1.300.000 (30% dari gaji bersih Rp6.000.000, sudah dikurangi cicilan HP Rp500.000; patokan hati-hati yang dipakai simulasi ini, bukan aturan resmi). Total cicilanmu (motor + HP) = Rp1.215.556 → rasio **20,3% dari gaji → AMAN**. Dengan bunga & tenor sama, pinjaman maksimal aman sekitar Rp36.335.404 — jadi motor 25 juta ini masih jauh di bawah batas.
>
> **Yang perlu diperhatikan:**
> - Bunga 0,8%/bulan itu flat (dihitung dari pokok awal terus-menerus, bukan sisa utang), makanya efektifnya jauh lebih tinggi: ±17,25%/tahun, bukan 9,6%/tahun seperti kesannya.
> - Biaya admin Rp1 juta di muka menaikkan lagi bunga efektif jadi ±20,97%/tahun.
> - Angka di atas asumsi admin dibayar tunai di muka — kalau ternyata dipotong dari pencairan atau dimasukkan ke pinjaman, cicilan sedikit berubah.
>
> **Asumsi:** bunga flat per bulan, DP 20% dari Rp25.000.000, admin Rp1 juta dibayar tunai, pembulatan rupiah (selisih -Rp16 di cicilan terakhir).
>
> Catatan: simulasi, bukan penawaran atau nasihat keuangan; angka final mengikuti tabel angsuran resmi lembaga pembiayaan.
>
> Pertanyaan biar lebih pasti:
> 1. Apa ada biaya lain di muka (asuransi, provisi, fidusia, notaris) selain admin Rp1 juta?
> 2. Bunga 0,8%/bulan itu dikonfirmasi flat, bukan efektif/anuitas?
> 3. Mau dibandingkan juga dengan skema DP lebih besar atau tenor lebih pendek biar total bunganya lebih hemat?

**Catatan penguji:**
**SEBELUM 6,5** — angka inti benar (cicilan Rp715.556, total bunga Rp5.760.000, rasio 20,3%), tetapi tidak menjelaskan bahwa flat 0,8%/bulan setara ±17,25%/tahun efektif (±20,97% dengan admin), tanpa perbandingan anuitas, tanpa total harga lewat kredit, tanpa disclaimer; "ruang lega sekitar Rp650–800 ribu" tidak tepat (hitungan benar: Rp584.444 s/d Rp884.444 pada batas 30–35%); versi Telegram mengarang "leasing bulatkan ke Rp716.000–750.000-an".
**SESUDAH 9** (lokal & Telegram sama) — semua angka cocok dengan script & hitungan independen (cicilan Rp715.556/terakhir Rp715.540, EIR 17,25% & 20,97%, anuitas Rp641.594, selisih bunga Rp2.662.605, maks aman Rp1.300.000, pinjaman maks Rp36.335.404); total harga lewat kredit Rp31.760.000 (+27,0%) jadi pembeda utama; disclaimer & 3 pertanyaan. Minus: menanyakan "benar flat?" padahal pengguna sudah bilang flat; baris "Uang yang benar-benar diterima Rp19.000.000" membingungkan untuk kredit barang; versi Telegram keliru menyebut cicilan berubah bila admin dipotong dari pencairan (yang berubah hanya bila admin dimasukkan ke pinjaman).
