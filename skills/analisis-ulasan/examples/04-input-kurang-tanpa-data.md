# 04 — Minta analisis tapi belum mengirim ulasan (S4, input tidak lengkap)

## Skenario
Pengguna meminta analisis tanpa melampirkan ulasan, bintang, atau nama produk.

## Input pengguna
> Tolong analisis review toko online saya dong, lagi banyak yg komplain nih

## Output
Siap, saya bantu rangkum ulasannya. Supaya hasilnya berupa angka pasti (bukan kira-kira), saya perlu 3 hal:

1. **Ulasannya.** Pilih yang paling mudah:
   - kirim file ekspor ulasan (CSV) dari Shopee/Tokopedia/TikTok Shop, **atau**
   - tempel langsung di sini, **satu ulasan per baris**.
2. **Bintangnya**, kalau ada. Taruh di depan ulasan, contoh:
   ```
   5 | barang bagus, packing rapi
   1 | brg ga sesuai deskripsi, chat ga dibales
   ⭐⭐⭐ ukurannya kekecilan
   ```
3. **Nama toko/produk**, dan kalau ada, periode ulasannya (mis. "Agustus–September").

Minimal ±10 ulasan agar polanya terlihat. Kalau ulasan memuat nama atau nomor HP pembeli, tidak apa-apa. Nanti di laporan semuanya disamarkan.

Setelah data masuk, kamu akan dapat: sebaran bintang, keluhan & pujian terbanyak lengkap dengan jumlah dan contoh kutipan, urutan perbaikan (apa, siapa, ukuran berhasilnya), dan 3–5 ide konten dari pujian.

## Catatan penguji
- Sesuai SKILL.md: bertanya **sekali** dengan daftar singkat (ulasan, bintang, nama produk), memberi contoh format `bintang | teks`, dan menyebut batas minimal ±10 ulasan.
- Pengguna diyakinkan soal privasi. Tidak ada angka atau tema yang dikarang sebelum data ada.
