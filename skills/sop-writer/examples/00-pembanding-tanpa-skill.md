# Pembanding A/B – Permintaan S1 dengan dan tanpa skill

**Permintaan yang sama (S1):**
```
Tolong buatkan SOP packing pesanan untuk online shop skincare saya, Glowria Skin di Tangerang. Pesanan sekitar 150 paket per hari dari Shopee dan TikTok Shop. Staf packing ada 2 orang, dicek sama admin (Mbak Sinta). Kurir pickup jam 15.00. Masalah kami: sering komplain botol toner pecah dan salah kirim varian (misal serum 20 ml malah dikirim 30 ml).
```

## A. Tanpa skill (AI agent biasa, tanpa membaca skill apa pun)

> **STANDAR OPERASIONAL PROSEDUR (SOP) PACKING PESANAN – GLOWRIA SKIN**
>
> **Tujuan:** Menjamin proses pengemasan pesanan berjalan efektif dan efisien sehingga meminimalkan kesalahan pengiriman dan kerusakan produk.
>
> **Ruang Lingkup:** SOP ini berlaku untuk seluruh staf packing Glowria Skin.
>
> **Prosedur:**
> 1. **Persiapan:** Staf packing wajib mempersiapkan seluruh perlengkapan packing seperti bubble wrap, kardus, lakban, dan printer resi sebelum memulai pekerjaan, serta memastikan area kerja dalam kondisi bersih dan rapi.
> 2. **Verifikasi pesanan:** Pesanan yang masuk dari Shopee dan TikTok Shop diverifikasi oleh admin dan dicetak resinya. Staf packing melakukan pengecekan kesesuaian produk, varian, dan jumlah dengan detail pesanan secara teliti untuk menghindari kesalahan pengiriman.
> 3. **Pengemasan:** Produk yang mudah pecah seperti toner harus dibungkus dengan bubble wrap secukupnya dan dimasukkan ke dalam kardus agar aman selama pengiriman. Pastikan tidak ada ruang kosong di dalam kardus.
> 4. **Quality control:** Admin melakukan pengecekan akhir terhadap paket sebelum diserahkan ke kurir.
> 5. **Pengiriman:** Paket harus siap sebelum kurir datang pada pukul 15.00 dan diserahkan dengan tanda terima.
>
> **Target Kinerja:**
> - Waktu packing maksimal 3 menit per paket
> - Tingkat kesalahan pengiriman di bawah 1%
> - Kerusakan produk 0%
>
> **Tips Tambahan:**
> - Lakukan pelatihan rutin kepada staf packing.
> - Gunakan sistem barcode scanner untuk meminimalkan kesalahan.
> - Evaluasi SOP secara berkala.

## B. Dengan skill `sop-writer`
Output lengkap ada di `01-sop-packing-olshop-skincare.md`. Ringkasnya:
- Tabel kontrol dokumen (kode SOP-GS-01, versi 1.0, tanggal berlaku, pembuat/penyetuju) dan riwayat revisi.
- 21 langkah pendek (≤ 12 kata), satu tindakan per langkah, diawali kata kerja, dibagi 4 bagian dengan jam.
- 3 langkah kritis ⚠️ yang langsung menjawab masalah pengguna: cocokkan **ukuran ml**, video packing, dan botol kaca **wajib kardus + bubble wrap 2 lapis**.
- Tabel "Jika terjadi masalah" (4 kondisi: stok varian habis, botol retak, resi rusak, kurir datang lebih awal) dengan pihak yang dihubungi.
- Indikator terukur berlabel "(usulan, sesuaikan)". Checklist mingguan 11 butir siap cetak dengan paraf.
- Catatan PDP untuk video packing yang memuat alamat pembeli.

## Penilaian singkat
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Bahasa untuk karyawan | Kalimat panjang dan pasif ("diverifikasi", "melakukan pengecekan kesesuaian"), 1 butir berisi banyak tindakan. | Kalimat perintah pendek, satu tindakan per langkah. |
| Menjawab masalah pengguna | Umum: "bubble wrap **secukupnya**", "cek varian secara teliti". | Spesifik: 2 lapis + kardus, cocokkan ukuran ml, stiker FRAGILE, video. |
| Angka target | Dikarang sebagai target pasti ("3 menit/paket", "0% kerusakan"). | Diberi label usulan dan bisa disesuaikan. |
| Kondisi tidak normal | Tidak ada. | 4 skenario "Jika... maka... lapor ke". |
| Checklist siap cetak | Tidak ada. | Ada (11 butir, Sen–Min, paraf). |
| Kontrol dokumen & revisi | Tidak ada. | Ada. |
| Saran | Generik ("pelatihan rutin", beli barcode scanner). | Konkret dan murah (foto benar vs salah, poster A4). |

**Kesimpulan: hasil dengan skill jelas lebih baik.** SOP tanpa skill terbaca seperti dokumen formal yang sulit dipraktikkan karyawan baru dan tidak menjawab dua masalah spesifik pengguna. SOP dengan skill bisa langsung dicetak, ditempel, dan diaudit lewat checklist harian.
