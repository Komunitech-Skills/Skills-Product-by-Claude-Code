# Contoh 1 - Toko gamis, Shopee Ads

> Contoh uji pembuat (simulasi agent, 2026-09-26). Data fiktif yang meniru kasus UMKM nyata;
> bukan hasil uji independen (itu dilakukan penguji terpisah sesuai CLAUDE.md Tahap 6).

## Permintaan pengguna
"Tolong audit iklan Shopee toko gamis saya. Anggaran 50rb/hari tapi ROAS jelek, kayaknya boros."

## Bukti yang diberikan (diringkas agent ke file jawaban)
Agent bertanya sekali (screenshot daftar iklan + target ROAS, laporan kata kunci 14 hari, halaman
produk, harga/modal/biaya Shopee). Jawaban pemilik diringkas di
[`uji-pembuat-01-jawaban-toko-fashion-shopee.csv`](uji-pembuat-01-jawaban-toko-fashion-shopee.csv). Gamis andalan: harga
Rp149.000, modal Rp78.000, biaya Shopee 12% (dari rincian penghasilan pesanan), kemas Rp2.000.

## Perintah yang dijalankan
```bash
python3 scripts/skor_audit.py roas-impas --harga 149rb --modal 78rb --biaya-persen 12 --biaya-lain 2000
python3 scripts/skor_audit.py hitung examples/uji-pembuat-01-jawaban-toko-fashion-shopee.csv --usaha "Toko gamis (Shopee)" --mulai 2026-09-28
```

## Output script (disalin apa adanya)
```
Harga jual            : Rp 149.000
Modal (HPP)           : Rp 78.000
Biaya platform        : Rp 17.880
Biaya lain            : Rp 2.000
Laba kotor/pesanan    : Rp 51.120
Biaya iklan maks/pesanan (impas): Rp 51.120
ROAS/ROI impas        : 2,92 (di bawah angka ini iklan rugi; dibulatkan ke atas)

AUDIT KESEHATAN AKUN IKLAN - Toko gamis (Shopee)
================================================
Skor gabungan: 41,3 / 100 (Kritis) - FINAL; bobot: satu platform

PER PLATFORM
- Shopee Ads (juga iklan pencarian marketplace lain): 41,3/100 (Kritis); bukti 97,2% (final)
    Pelacakan & konversi: 0,0 (bobot 10)
    Struktur & akses akun: 62,5 (bobot 15)
    Target & audiens: 50,0 (bobot 10)
    Anggaran & bidding: 0,0 (bobot 20)
    Materi iklan: 75,0 (bobot 15)
    Halaman tujuan / etalase: 78,6 (bobot 20)
    Pengecualian: 0,0 (bobot 10)

PRIORITAS PERBAIKAN (dampak x kemudahan; skor tertinggi dikerjakan dulu)
1. [S06] Target ROAS/bid di atas ROAS impas - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +10,0 bila beres
   Perbaikan: Naikkan target ROAS ke minimal ROAS impas; turunkan bid kata kunci yang ROAS-nya di bawah impas
   Catatan audit: Target ROAS 2, padahal ROAS impas 2,92 (biaya Shopee 12% + kemas Rp2.000)
2. [S07] Anggaran tidak habis sebelum jam ramai - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +10,0 bila beres
   Perbaikan: Naikkan anggaran harian iklan yang untung, atau kurangi jumlah iklan supaya anggaran cukup sampai malam
   Catatan audit: Anggaran Rp50rb/hari habis jam 14.00
3. [S14] Kata kunci/iklan boros dihentikan - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +10,0 bila beres
   Perbaikan: Nonaktifkan atau turunkan bid kata kunci/iklan tersebut
   Catatan audit: Kata kunci "gamis murah" habis Rp212rb, 0 pesanan
4. [S03] Hanya produk siap jual yang diiklankan - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +5,6 bila beres (status: sebagian)
   Perbaikan: Hentikan iklan produk yang stoknya tipis atau ratingnya rendah; alihkan ke produk terlaris
   Catatan audit: 2 dari 6 produk diiklankan stoknya tinggal <1 minggu
5. [S01] Kinerja dipantau per iklan/produk - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +5,0 bila beres
   Perbaikan: Ekspor laporan iklan tiap minggu dan buat laporan dengan laporan-iklan-mingguan
   Catatan audit: Hanya lihat ringkasan toko di aplikasi
6. [S02] ROAS impas diketahui per produk - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +5,0 bila beres
   Perbaikan: Hitung dengan perintah roas-impas; tulis angkanya di catatan iklan
   Catatan audit: Belum pernah hitung; gamis Rp149.000 modal Rp78.000
7. [S12] Harga, voucher, dan varian lengkap - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +4,3 bila beres (status: sebagian)
   Perbaikan: Pasang voucher toko kecil; lengkapi tabel ukuran; tutup varian yang kosong
   Catatan audit: Tabel ukuran belum ada
8. [S10] Judul produk memuat kata kunci utama - Shopee Ads; tinggi, mudah; prioritas 9; skor platform naik +3,8 bila beres (status: sebagian)
   Perbaikan: Tulis ulang judul: kata kunci utama di depan, maks. 1 merek (milik sendiri)
   Catatan audit: Judul diawali nama toko
9. [S05] Kata kunci relevan dengan bahasa pembeli - Shopee Ads; tinggi, sedang; prioritas 6; skor platform naik +5,0 bila beres (status: sebagian)
   Perbaikan: Tambah kata kunci dari saran pencarian Shopee; hapus yang tidak sesuai produk
   Catatan audit: Ada kata kunci "baju wanita" terlalu umum

RENCANA 7 HARI (maks. kira-kira 1-2 jam kerja per hari)
Hari 1 (Senin, 28 Sep 2026):
  - PERBAIKI [S06] Target ROAS/bid di atas ROAS impas - Naikkan target ROAS ke minimal ROAS impas; turunkan bid kata kunci yang ROAS-nya di bawah impas
  - PERBAIKI [S07] Anggaran tidak habis sebelum jam ramai - Naikkan anggaran harian iklan yang untung, atau kurangi jumlah iklan supaya anggaran cukup sampai malam
  - PERBAIKI [S14] Kata kunci/iklan boros dihentikan - Nonaktifkan atau turunkan bid kata kunci/iklan tersebut
Hari 2 (Selasa, 29 Sep 2026):
  - PERBAIKI [S03] Hanya produk siap jual yang diiklankan - Hentikan iklan produk yang stoknya tipis atau ratingnya rendah; alihkan ke produk terlaris
  - PERBAIKI [S01] Kinerja dipantau per iklan/produk - Ekspor laporan iklan tiap minggu dan buat laporan dengan laporan-iklan-mingguan
  - PERBAIKI [S02] ROAS impas diketahui per produk - Hitung dengan perintah roas-impas; tulis angkanya di catatan iklan
Hari 3 (Rabu, 30 Sep 2026):
  - PERBAIKI [S12] Harga, voucher, dan varian lengkap - Pasang voucher toko kecil; lengkapi tabel ukuran; tutup varian yang kosong
  - PERBAIKI [S10] Judul produk memuat kata kunci utama - Tulis ulang judul: kata kunci utama di depan, maks. 1 merek (milik sendiri)
Hari 4 (Kamis, 1 Okt 2026):
  - PERBAIKI [S05] Kata kunci relevan dengan bahasa pembeli - Tambah kata kunci dari saran pencarian Shopee; hapus yang tidak sesuai produk
Hari 5 (Jumat, 2 Okt 2026):
  - Tidak ada tugas baru; pantau hasil harian dan catat perubahan.
Hari 6 (Sabtu, 3 Okt 2026):
  - Jangan ubah pengaturan besar; biarkan iklan belajar setelah perbaikan. Catat biaya & hasil harian.
Hari 7 (Minggu, 4 Okt 2026):
  - Ekspor data iklan 7 hari lalu buat laporan dengan skill laporan-iklan-mingguan; audit ulang cek yang sudah diperbaiki dan bandingkan skornya.

Aturan aman: ubah anggaran paling banyak 20% per 2-3 hari dan jangan ubah banyak hal sekaligus di satu kampanye. Skor ini alat bantu prioritas, bukan jaminan hasil iklan.
```

## Penjelasan bahasa awam yang ditambahkan agent (3 masalah terbesar)
1. **Target ROAS 2 padahal titik impas 2,92.** Artinya tiap Rp1 iklan hanya menghasilkan Rp2
   penjualan, padahal agar tidak rugi butuh Rp2,92. Iklan "laku" tapi toko rugi per pesanan.
   Benahi: Iklan Shopee → iklan gamis → ubah target ROAS ke minimal 2,92 (±5 menit).
2. **Anggaran Rp50rb habis jam 14.00.** Pembeli Shopee paling ramai malam (19.00–22.00), iklan
   Anda sudah mati saat itu. Benahi: hentikan 2 iklan produk yang stoknya tipis supaya anggaran
   terkumpul di gamis andalan, atau naikkan anggaran iklan yang ROAS-nya di atas 2,92.
3. **Kata kunci "gamis murah" menghabiskan Rp212rb tanpa pesanan** — lebih dari laba 4 pesanan
   (Rp51.120 per pesanan). Benahi: nonaktifkan kata kunci itu (±2 menit).

## Catatan pemeriksaan pembuat
- Skor 41,3 dicek manual: kategori pelacakan 0/6, struktur 2,5/4, audiens 1,5/3, anggaran 0/6,
  materi 4,5/6, etalase 5,5/7, pengecualian 0/3 → (0×10 + 62,5×15 + 50×10 + 0×20 + 75×15 +
  78,571×20 + 0×10)/100 = 41,34 → 41,3. Cakupan 35/36 = 97,2% (S08 tidak_tahu). Cocok.
- ROAS impas: 149.000 − 78.000 − 17.880 − 2.000 = 51.120; 149.000/51.120 = 2,9147 → ke atas 2,92. Cocok.
