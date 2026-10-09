# 00 - Uji A/B: skenario normal 1 tanpa skill vs dengan skill

> Uji independen Tahap 6 (2026-09-30). Prompt sama dengan `06-uji-toko-hijab-shopee-wa.md` (toko hijab Shopee + WA, pesanan Rp145.000, margin 38%, teman 10%, pengajak Rp20.000, kartu Rp1.500, 850 pelanggan, iklan Rp55.000, anggaran Rp750.000, pertanyaan opsi Rp50.000 + 20%).
>
> **Keterbatasan metode:** jawaban "tanpa skill" disusun oleh penguji dengan meniru jawaban asisten umum tanpa folder skill (tanpa script, tanpa template). Penguji sudah membaca skill sebelumnya, jadi ada kemungkinan bias; untuk rilis, disarankan diulang oleh sesi segar yang tidak pernah membaca skill.

## A. Tanpa skill (jawaban tipikal asisten umum)
> Program referral Anda cukup aman! Dengan pesanan Rp145.000 dan margin 38%, keuntungan Anda sekitar Rp55.000 per pesanan. Diskon 10% untuk teman (sekitar Rp14.500) plus Rp20.000 untuk pengajak berarti biaya sekitar Rp35.000, jadi masih untung sekitar Rp20.000. Itu lebih murah daripada iklan.
>
> Opsi Rp50.000 + 20% kurang disarankan karena totalnya hampir Rp80.000, melebihi keuntungan Anda.
>
> Tips:
> 1. Buat kode referral unik untuk tiap pelanggan.
> 2. Broadcast pengumuman program ke semua pelanggan lewat WhatsApp dan pasang di Shopee.
> 3. Beri hadiah bertingkat: ajak 5 teman dapat bonus tambahan.
> 4. Pantau hasil tiap bulan.
> 5. Buat syarat dan ketentuan yang jelas.
>
> Contoh pesan: "Ajak temanmu belanja di Kerudung Nara dan dapatkan Rp20.000! Temanmu juga dapat diskon 10%. Hubungi kami di WA 08xx."

## B. Dengan skill
Lihat `06-uji-toko-hijab-shopee-wa.md` (lengkap).

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Angka | Dikira ("sekitar Rp35.000", "sekitar Rp20.000"); **lupa biaya kartu Rp1.500** (biaya sebenarnya Rp36.000, laba Rp19.100) | Dari script, tepat: Rp36.000; Rp19.100; 24,83% / 65,34%; rugi Rp23.900 untuk opsi besar |
| Anggaran & kuota | Tidak dihitung | Rp750.000 = maks 20 referral/bulan; simulasi menunjukkan realistis/optimis melewati anggaran |
| Titik impas & batas aman | Tidak ada | Batas aman Rp99.180 (aturan praktis, disebut asumsi) |
| Anti-curang | Tidak ada | Teman belum pernah beli, nomor/alamat sama tidak sah, cair setelah lewat retur, batas per orang |
| S&K | "Buat yang jelas" saja | 9 butir siap tempel dengan angka |
| Teks ajakan | 1 teks; **menaruh nomor WA** yang bisa melanggar aturan Shopee | 3 varian, versi kartu paket aman untuk Shopee, ada opsi "STOP" |
| Etika/kepatuhan | **Menyarankan broadcast ke semua pelanggan**; tidak menyebut UU PDP/Perlindungan Konsumen; bonus bertingkat tanpa batas | Kirim satu per satu, data minimal (UU PDP), promo jelas (UU 8/1999), tanpa blast |
| Rencana tindak | Umum | 5 langkah minggu ini + uji 30 hari |

**Kesimpulan:** dengan skill **jelas lebih baik** (akurasi angka, kelengkapan siap pakai, kepatuhan). Tanpa skill, jawaban meleset Rp1.000 per referral karena melupakan biaya kartu dan menyarankan broadcast yang bertentangan dengan kebijakan Komunitech.
