# 01 — Kafe, bulanan, 8 pos (tanpa unit)

> Contoh pembuat skill (v1.0.0). Angka dari `scripts/selisih.py --file examples/data/01-kafe-juli.csv --periode "Juli 2026" --format teks`; diverifikasi ulang dengan Python terpisah (float): laba 30.000.000 → 23.750.000 (−20,83%), faktor volume 78,7/80 = 0,98375, HPP disesuaikan 23.610.000, kelebihan HPP 2.290.000, komisi disesuaikan 3.738.250.

## Pesan pengguna
"Kafe saya bulan Juli. Anggaran penjualan minuman 62 jt, realisasi 57,4 jt. Makanan 18 jt jadi 21,3 jt. HPP bahan 24 jt jadi 25,9 jt. Gaji 12 jt, sewa 6,5 jt sama. Listrik & air 2,2 jt jadi 2,95 jt. Iklan 1,5 jt jadi 3,2 jt. Komisi ojol 3,8 jt jadi 4,4 jt. Kok laba turun ya?"

## Data yang dihitung (`examples/data/01-kafe-juli.csv`)
HPP bahan baku dan komisi ojol diberi `sifat=variabel` (ikut naik-turun dengan penjualan).

## Contoh balasan chat
**Rekap Juli 2026: laba Rp23.750.000 vs rencana Rp30.000.000 (−Rp6.250.000, −20,8%)**
Pendapatan hanya kurang Rp1,3 jt (−1,6%), tapi biaya naik Rp4,95 jt (+9,9%). Penyebab terbesar: penjualan minuman turun Rp4,6 jt (sebagian tertutup makanan +Rp3,3 jt), lalu HPP bahan +Rp1,9 jt dan iklan +Rp1,7 jt.

| Pos | Selisih | Keterangan |
|---|---|---|
| Penjualan minuman | −Rp4.600.000 (−7,4%) | merugikan; terbesar |
| Penjualan makanan | +Rp3.300.000 (+18,3%) | menguntungkan |
| HPP bahan baku | +Rp1.900.000 (+7,9%) | merugikan; padahal penjualan turun |
| Iklan & promosi | +Rp1.700.000 (+113,3%) | merugikan; lebih dari 2× rencana |
| Listrik & air | +Rp750.000 (+34,1%) | merugikan |
| Komisi ojol online | +Rp600.000 (+15,8%) | merugikan |
| Gaji, sewa | Rp0 | sesuai rencana |
| **Laba** | **−Rp6.250.000 (−20,8%)** | margin 37,5% → 30,2% |

**Kenapa angkanya begitu**
- HPP: penjualan total turun sedikit, jadi wajarnya HPP malah turun ke ±Rp23.610.000. Realisasi Rp25.900.000 berarti **kelebihan Rp2.290.000 (+9,7%)** yang tidak dijelaskan oleh jumlah penjualan.
- Komisi ojol: setelah disesuaikan penjualan, kelebihannya Rp661.750 (+17,7%), jadi porsi penjualan lewat aplikasi atau persentase potongannya kemungkinan naik.

**Yang perlu dicek**
1. Minuman: jumlah cup yang turun, atau harga rata-rata per cup (promo/diskon)? Ada hari tutup, menu habis, atau pesaing baru di dekat kafe?
2. HPP: harga susu/kopi dari pemasok naik (cek nota Juli vs Juni)? Takaran resep sesuai standar? Ada bahan terbuang atau stok bulan depan yang ikut tercatat Juli?
3. Iklan: kampanye apa yang menambah Rp1,7 jt, dan berapa penjualan yang datang dari kampanye itu?
4. Listrik & air: ada alat baru (freezer/AC), jam buka lebih panjang, atau tagihan dua bulan tercatat di Juli?
5. Komisi ojol: apakah ikut program promo aplikasi yang menambah potongan?

**Tindakan bulan depan**
- Tetapkan batas iklan Rp1,5 jt/bulan (±Rp50 rb/hari) dan catat penjualan dari tiap kampanye; lanjutkan hanya yang membawa penjualan.
- Cek takaran 5 menu minuman terlaris dan catat bahan terbuang selama 2 minggu.
- Bandingkan harga 2 pemasok untuk bahan yang naik.
- Makanan laku +18,3%: pertimbangkan paket makanan + minuman untuk mengangkat penjualan minuman.

**Pesan untuk tim (siap kirim)**
> Rekap Juli: laba Rp23,75 jt, kurang Rp6,25 jt dari rencana. Makanan bagus (+Rp3,3 jt), tapi minuman −Rp4,6 jt, bahan +Rp1,9 jt, iklan +Rp1,7 jt.
> Minta tolong sebelum Jumat: (1) barista cek takaran 5 menu terlaris & catat bahan terbuang, (2) admin kirim rekap iklan Juli + penjualan dari iklan.
> Kita bahas Sabtu pagi. Terima kasih tim!

**Asumsi:** ambang material 5% atau Rp500 rb; HPP bahan dan komisi ojol dianggap ikut naik-turun dengan penjualan; pajak tidak dihitung.
Catatan: analisis untuk manajemen, bukan audit/nasihat keuangan; penyebab perlu dicek ke nota, rekening, dan catatan stok.

Supaya lebih tajam:
1. Berapa cup minuman terjual Juli (rencana vs nyata)? Bisa saya pisahkan karena jumlah cup atau harga.
2. Apakah ada pengeluaran lain yang belum ditempel (gas, internet, pajak, cicilan)?
