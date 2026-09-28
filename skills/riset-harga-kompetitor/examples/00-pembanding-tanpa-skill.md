# Uji A/B - Skenario 01 tanpa skill vs dengan skill

> Penguji independen, 2026-09-28. Input sama persis dengan `01-normal-kopi-bubuk.md` (3 link + 6 teks tempelan, modal 30.000, biaya Shopee 8% + 4% + 0,5% + Rp1.250, harga sekarang 58.000). Jawaban "tanpa skill" = jawaban agent umum yang sama tanpa SKILL.md (disimulasikan penguji, hitungan di kepala seperti agent biasa).

## A. Tanpa skill (ringkas, isi utama jawaban)
> Saya coba buka linknya; link Shopee tidak menampilkan data, jadi saya pakai data yang ada.
> Rata-rata harga pesaing (disetarakan ke 250 g): sekitar **Rp 55.600**. Harga termurah sekitar Rp 48.000 (Kedai Seduh 1/2 kg), termahal Rp 80.000.
> Dengan modal 30.000 dan potongan Shopee sekitar 12,5% + 1.250, di harga 58.000 kamu untung kira-kira Rp 19.500 (±34%).
> Saran: harga kamu sedikit di atas rata-rata. Kamu bisa turun ke **Rp 54.900 - Rp 55.900** supaya bersaing, atau tetap 58.000 kalau kualitas lebih baik. Pertimbangkan juga promo gratis ongkir dan bundling.

Kelemahan yang diamati:
- Memakai **rata-rata** yang tertarik oleh outlier Rp 80.000 (rata-rata 55.646 vs median 53.125); tidak ada kuartil.
- **Tidak menghitung harga minimum** (batas untung sesuai target 20%): pengguna tidak tahu batas bawah aman (Rp 46.297).
- Rekomendasi Rp 54.900-55.900 berada di atas 5 dari 7 pesaing, tidak dikaitkan ke strategi.
- Tidak ada tabel per pesaing, per 100 g, harga coret/diskon rata-rata, pesaing terlaris, duplikat Kopi Rakyat tidak disebut (dihitung dua kali bila agent tidak teliti), tidak ada tanggal cek/asumsi.
- Link gagal disebut sambil lalu, tanpa meminta pengguna menempel teks/screenshot.
- Angka "±34%" dan "±" lain dari hitungan kepala, tidak bisa diaudit.

## B. Dengan skill
Lihat `01-normal-kopi-bubuk.md`: tabel 7 pesaing setara 250 g + per 100 g, statistik terendah/P25/median/P75/tertinggi, posisi harga kita (lebih mahal dari 6 dari 7, persentil 86), harga balik modal Rp 35.715 & **minimum Rp 46.297**, rentang Rp 49.375 - Rp 54.825, titik Rp 53.125, harga cantik **Rp 52.900** (laba Rp 15.038, margin 28,43%), promo/harga coret, duplikat dibuang, link gagal dilaporkan + diminta teks. Semua angka **0 selisih** terhadap verifikasi Decimal independen.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Penyetaraan ukuran | Ada, hitung kepala | Script, per 100 g juga |
| Statistik tahan outlier | Rata-rata | Median + kuartil |
| Batas untung (minimum) | Tidak ada | Ada, dibulatkan ke atas |
| Laba/margin di harga rekomendasi | Tidak | Ya (titik & harga cantik) |
| Duplikat / baris rusak | Tidak ditangani | Dibuang + dilaporkan |
| Link gagal | Disebut singkat | Dilaporkan + diminta tempel teks, tanpa bypass |
| Bisa diaudit | Tidak | Rumus + asumsi tertulis |

**Kesimpulan:** dengan skill **jelas lebih baik** (akurasi, batas untung, konsistensi format, keamanan). Syarat nilai tambah Tahap 6 butir 4 terpenuhi. Catatan: bug parser `1/2 kg` (T1) justru membuat versi skill salah di percobaan pertama pada baris itu, sedangkan agent tanpa skill membaca "1/2 kg" dengan benar - perlu diperbaiki agar skill tidak kalah di kasus ini.
