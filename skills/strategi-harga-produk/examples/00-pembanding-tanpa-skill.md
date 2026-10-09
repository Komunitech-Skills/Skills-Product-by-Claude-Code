# 00 — Uji A/B: skenario 01 tanpa skill vs dengan skill

> Tahap 6 butir 4. Kedua output dibuat oleh sesi `claude -p` baru (Claude Code, simulasi agent), prompt identik. "Tanpa skill" dijalankan di folder kosong tanpa skill dan tanpa akses tool; "dengan skill" di folder yang hanya berisi skill ini. Output lengkap "dengan skill": `01-kopi-literan-naik-harga-reseller.md`.

## Input (sama persis)
> Aku jualan kopi susu gula aren literan (botol 1 liter) di Semarang, namanya Kopi Teras. Modal per botol 22 ribu udah sama botol & stiker. Sekarang aku jual 45 ribu, laku sekitar 400 botol sebulan. Biaya tetap (sewa dapur, gaji 1 orang, listrik) 5,2 juta sebulan. Pesaing di sekitar jual 35rb, 42rb, 55rb. Banyak yang minta jadi reseller, ada kantor juga mau ambil 100 botol per minggu. Terus aku kepikiran naikin ke 49.900 karena gula aren naik. Gimana strategi harganya?

## Output TANPA skill (apa adanya)

# Strategi harga Kopi Teras

## Kondisi sekarang
- Margin per botol: 45.000 − 22.000 = **23.000**
- Laba kotor: 400 × 23rb = 9,2 jt
- Laba bersih: 9,2 jt − 5,2 jt = **±4 jt/bulan**

## Kalau naik ke 49.900
- Margin jadi 27.900 (naik 21%).
- Volume bisa turun sampai **±330 botol (−17%)** dan labamu tetap 4 jt.
- Kalau volume turun kurang dari itu, kamu untung. Kenaikan harganya 10,9%, jadi kecil kemungkinan pelanggan langsung kabur sebanyak itu.
- 49.900 masih di bawah pesaing termahal (55rb) dan di atas 42rb. Itu wajar untuk produk yang kamu posisikan lebih premium.

Satu hal perlu dicek: kalau gula aren naik, **modal 22rb itu masih berlaku atau sudah naik?** Misalnya modal jadi 24rb. Margin di 45rb tinggal 21rb, sedangkan di 49.900 jadi 25.900. Jadi alasan kenaikan harga makin kuat. Hitung dulu berapa persen porsi gula aren di modalmu.

## Jangan satu harga untuk semua
Harga eceran boleh naik, tapi reseller dan kantor perlu harga sendiri.

| Segmen | Harga | Margin/botol | Catatan |
|---|---|---|---|
| Eceran (langsung) | **49.900** | 27.900 | Harga acuan |
| Reseller | **40.000** (min. 10 botol/order) | 18.000 | Reseller dapat ±10rb (25%) kalau jual di 49.900 |
| Kantor 100 botol/minggu | **42.000**, kontrak 1–3 bulan | 20.000 | Bayar di muka atau maksimal tempo 7 hari |

- **Kantor:** 100 botol/minggu berarti ±430 botol/bulan, hampir dua kali lipat volumemu. Dengan harga 42rb, labanya sekitar 8,6 jt/bulan dari kantor saja. Order rutin dan bisa diprediksi ini lebih berharga daripada mengejar eceran.
- **Reseller:** wajibkan mereka menjual minimal di harga eceranmu (49.900), supaya tidak saling banting harga. Reseller dapat margin 10rb, kamu tetap dapat 18rb tanpa perlu cari pembeli.

## Yang perlu dicek sebelum terima order besar
1. **Kapasitas produksi.** Dengan 1 karyawan, tambahan 430 botol/bulan mungkin butuh tenaga tambahan. Misalnya part-time 1,5–2 jt, itu masih kecil dibanding tambahan laba.
2. **Arus kas.** Order kantor besar jangan diberi tempo panjang.
3. **Jangan turunkan harga eceran** demi reseller. Beri diskon lewat volume, bukan lewat harga dasar.

## Langkah praktis
1. Naikkan eceran ke 49.900 mulai bulan depan. Kasih tahu pelanggan lama satu minggu sebelumnya dan bilang alasannya (bahan baku naik).
2. Pantau penjualan 4 minggu. Kalau volume masih di atas 330 botol, kamu aman.
3. Kalau ragu, bisa mulai 47.900 dulu, tapi 49.900 sudah cukup aman secara hitungan.
4. Tawarkan paket reseller dan kontrak kantor sesuai tabel di atas.

Kalau kamu kasih tahu modal terbaru setelah gula aren naik dan kapasitas dapurmu per bulan, aku bisa hitung ulang dengan angka yang lebih pas.

## Output DENGAN skill
Lihat `01-kopi-literan-naik-harga-reseller.md`.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Ketepatan angka | Benar untuk yang dihitung (laba 4 jt, impas 330 botol) | Benar semua (diverifikasi penguji); sebagian dihitung manual |
| Titik impas (BEP) & batas aman | Tidak ada | BEP 227 botol/bulan |
| Lantai harga (margin minimum) | Tidak ada; margin hanya dalam rupiah, tidak ada % | Lantai Rp36.667 (margin 40%), diskon maks 18,52%, margin % & status OK per baris |
| Dampak naik harga | Hanya volume impas | Volume impas (pasti) + tabel ESTIMASI 3 tingkat kepekaan, dilabeli perkiraan |
| Asumsi tertulis | Tidak | Ya (HPP, margin minimum default, tanpa potongan, non-PKP) |
| Rencana naik harga | Umumkan 1 minggu, pantau | Bertahap (47.900 lalu 49.900), kesempatan harga lama, teks pengumuman siap tempel |
| Konsistensi saran | Reseller jual di harga eceran toko (konsisten) | **Inkonsisten**: toko Rp47.900, reseller disuruh jual ≥ Rp49.900 |
| Peluang kantor | Dianalisis baik (kontrak, bayar di muka) | Dianalisis baik (kontrak, batas tawar) |
| Siap pakai | Tabel harga | Tabel + 5 langkah minggu ini + teks WA |

## Kesimpulan
**Dengan skill lebih baik**, tetapi tidak menang telak: agent tanpa skill sudah kuat untuk kasus ini (volume impas benar, tangga harga masuk akal, analisis kantor dan kapasitas). Nilai tambah skill: lantai harga/margin minimum, BEP, estimasi berlabel, asumsi eksplisit, dan teks siap tempel. Kelemahan skill yang terlihat: agent tidak menjalankan `tangga` untuk harga yang direkomendasikan dan membuat saran harga reseller yang bertentangan dengan harga toko.

Bahan README "sebelum/sesudah": tanpa skill tidak ada batas bawah harga dan tidak ada angka "berapa pelanggan boleh berkurang sebelum rugi" dalam bentuk BEP; dengan skill ada.
