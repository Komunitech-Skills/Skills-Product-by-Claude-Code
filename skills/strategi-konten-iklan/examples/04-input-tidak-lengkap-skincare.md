# Contoh 04 - Input tidak lengkap dan ambigu

**Permintaan:** "Bagi anggaran iklan Rp1,500 sebulan untuk toko skincare saya." (tanpa harga, tanpa margin)

## Langkah 1 - script menolak angka ambigu
```
python3 scripts/alokasi_anggaran.py --anggaran 1,500 --aov 100rb --margin 40%
```
```
GAGAL: --anggaran '1,500' ambigu: '1,500' bisa ribuan (gaya Inggris) atau desimal. Tulis 1.500 / 1500 untuk seribu lima ratus, atau 1,5jt untuk satu setengah juta.
(kode keluar: 2)
```

## Langkah 2 - script menolak data yang kurang
```
python3 scripts/alokasi_anggaran.py --anggaran 1,5jt
```
```
GAGAL: Untuk tujuan 'penjualan' wajib isi --aov (harga rata-rata per pesanan) dan --margin (margin kotor, mis. 40%). Tanpa keduanya target CPA/ROAS tidak bisa dihitung.
```

## Langkah 3 - margin ambigu
```
python3 scripts/alokasi_anggaran.py --anggaran 1,5jt --aov 100rb --margin 0,4
```
```
GAGAL: --margin '0,4' ambigu: 0,4 berarti 0,4% atau 40%? Tulis '40%' (atau '0,4%').
```

## Pesan ke pengguna (satu kali, berisi semua pertanyaan)
"Sebelum saya bagi anggarannya, mohon konfirmasi:
1. Anggaran maksudnya Rp1.500 atau Rp1,5 juta atau Rp1.500.000 per bulan?
2. Harga rata-rata satu pesanan berapa?
3. Margin kotor berapa persen (setelah modal, biaya admin marketplace, dan ongkir yang Anda tanggung)? Bila belum tahu, kirim harga jual, modal, dan biaya admin; saya bantu hitung.
4. Punya toko di Shopee/TikTok Shop, atau hanya IG?
5. Skincare termasuk kategori yang punya aturan iklan sendiri: apakah produk sudah terdaftar resmi dan tidak ada klaim penyembuhan?"

Setelah dijawab (mis. Rp1,5 juta, harga Rp100rb, margin 40%, hanya IG), jalankan ulang dengan `--kategori kesehatan --kanal meta`; catatan aturan kategori terbatas ikut tercetak.
