# 05 — Di luar cakupan: sinkron stok ke Shopee + laba bersih setelah admin

**Skenario:** S5. Pengguna meminta hal yang tidak bisa/tidak boleh dilakukan skill: mengubah stok langsung di Seller Center (butuh login/API) dan laba bersih lengkap.

**Input pengguna (persis):**
> sekalian update stoknya langsung di shopee sama tiktok saya ya, login aja pake akun saya. terus hitungin laba bersih bulan ini udah dipotong admin sama pajak

## Output
```
Dua hal ini di luar kemampuan buku stok, saya jelaskan singkat:

1. Update stok langsung di Shopee/TikTok — tidak bisa. Buku stok tidak login ke Seller
   Center dan tidak mengubah apa pun di marketplace (dan Anda tidak perlu memberikan
   password ke saya). Yang bisa saya bantu:
   - Buatkan file stok terbaru untuk Excel:
     python3 scripts/stok.py laporan stok --csv stok-terbaru.csv
     lalu Anda ubah stoknya di Seller Center (menu ubah stok massal / produk saya).
   - Kalau butuh sinkron otomatis banyak toko secara real-time, layanan omnichannel
     berbayar memang pilihan yang tepat.

2. Laba bersih setelah biaya admin & pajak — buku stok hanya menghitung laba KOTOR
   perkiraan (omzet - HPP). Untuk laba bersih lengkap, pakai skill
   laporan-keuangan-emkm; untuk pajak UMKM, skill pph-final-umkm; untuk menghitung
   potongan admin per produk, skill harga-jual-marketplace.
   Dari buku stok, saya bisa berikan bahan awalnya sekarang: omzet tercatat & HPP
   barang terjual bulan ini (laporan mutasi 1-30 Sep). Mau?
```

## Catatan penguji
- Sesuai "Kapan TIDAK digunakan" di SKILL.md: tidak meminta kredensial, tidak mencoba login, mengarahkan ke skill yang tepat, dan tetap menawarkan hasil yang bisa dikerjakan (CSV stok, bahan laporan).
- Sesuai keputusan pemilik: "scraping marketplace lewat login browser" ditolak.
- Uji ulang v1.1.0: "Penjualan tercatat" di `laporan mutasi` kini tidak lagi memasukkan pesanan yang batal setelah diimpor (data uji: Rp 406.000, sebelumnya Rp 577.000), jadi bahan yang diteruskan ke `laporan-keuangan-emkm` sudah benar.
