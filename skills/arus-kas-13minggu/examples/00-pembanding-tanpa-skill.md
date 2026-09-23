# 00 — Uji A/B: S1 tanpa skill vs dengan skill

**Input (sama dengan S1):**
> Halo, saya punya usaha katering rumahan. Saldo kas + rekening sekarang kira-kira 35 juta. Pemasukan rata-rata 15 juta per minggu dari pesanan harian. PT Arunika Fiktif masih punya tagihan ke saya 24 juta, biasanya baru dibayar pertengahan November. Pengeluaran: belanja bahan 9,5 juta per minggu, gaji 5 karyawan total 15 juta tiap tanggal 28, sewa dapur 7 juta tiap tanggal 5, cicilan mobil box 3,2 juta tiap tanggal 15, listrik-gas-air sekitar 2,5 juta tiap tanggal 20. Awal November saya mau beli freezer baru 12 juta, terus tanggal 20 Desember bayar bonus akhir tahun karyawan 15 juta. Kas saya aman nggak 3 bulan ke depan?

## A. Tanpa skill (jawaban AI agent biasa, tanpa membaca skill apa pun)

> Berikut perkiraan arus kas 3 bulan ke depan (asumsi 1 bulan = 4 minggu):
>
> | Bulan | Masuk | Keluar | Saldo akhir |
> |---|---:|---:|---:|
> | Oktober | Rp 60.000.000 | Rp 65.700.000 | Rp 29.300.000 |
> | November | Rp 84.000.000 (termasuk PT Arunika) | Rp 77.700.000 (termasuk freezer) | Rp 35.600.000 |
> | Desember | Rp 60.000.000 | Rp 80.700.000 (termasuk bonus) | Rp 14.900.000 |
>
> Rincian keluar per bulan: bahan 38 jt, gaji 15 jt, sewa 7 jt, cicilan 3,2 jt, listrik 2,5 jt = 65,7 jt.
>
> **Kesimpulan:** kas Anda **aman** selama 3 bulan ke depan. Saldo terendah sekitar Rp 14,9 juta di akhir Desember setelah bonus.
>
> Tips menjaga arus kas:
> - Tagih piutang tepat waktu.
> - Sisihkan dana darurat minimal 1 bulan pengeluaran.
> - Catat pemasukan dan pengeluaran setiap hari.
> - Pertimbangkan menunda pembelian freezer bila kas menipis.

## B. Dengan skill `arus-kas-13minggu`
Lihat `01-katering-cek-aman-3-bulan.md`. Ringkasnya:
- Tabel **13 minggu** dengan tanggal. **Titik kritis minggu 6 (2–8 Nov): saldo Rp 6.300.000**, karena freezer, sewa, dan bahan jatuh di minggu yang sama, 2 minggu sebelum PT Arunika membayar. Minggu 6, 7, dan 12 berada di bawah batas aman.
- Gaji 28 September ditempatkan dengan benar di minggu 1.
- 5 opsi dengan angka hasil hitung ulang, misalnya "tunda freezer ke minggu 10 → minggu 6 jadi Rp 18.300.000" dan "tunda freezer + bonus 23 Des → semua minggu aman". Ada peringatan bahwa termin supplier memindahkan Rp 9.500.000 ke setelah minggu 13.
- Menyebut masalah struktural (keluar > masuk Rp 14.600.000) dan gaji 28 Des tepat setelah minggu 13, yang membuat saldo sekitar Rp 5.400.000 di awal Januari.
- File CSV untuk Excel (pemisah `;`, UTF-8 BOM).

## Penilaian

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Menemukan titik kritis | ❌ Tidak. Tampilan bulanan menyembunyikan penurunan ke Rp 6.300.000 di awal November. | ✅ Minggu 6, dengan penyebab per pos |
| Akurasi | ❌ Gaji 28 Sep terlewat, 1 bulan dianggap 4 minggu, saldo terendah "Rp 14,9 jt" hanya kebetulan sama dengan minggu 12. Kesimpulan "aman" menyesatkan. | ✅ Diverifikasi independen 13/13 minggu |
| Opsi tindakan | Tips generik tanpa angka | 5 opsi konkret: pos, nominal, minggu asal → tujuan, hasil hitung |
| Kejujuran simulasi | — | Kewajiban yang terdorong ke luar minggu 13 diperingatkan |
| Siap pakai | Tidak ada file | CSV siap buka di Excel |

**Kesimpulan A/B:** hasil dengan skill **jelas lebih baik**. Jawaban tanpa skill memberi kesimpulan "aman" dan melewatkan minggu kritis yang menjadi inti pertanyaan pengguna ("uang saya cukup sampai kapan"). Nilai tambah skill ada pada penempatan per tanggal yang deterministik, hitungan oleh script, dan opsi yang disimulasikan dengan angka.
