# Batas & Aturan Listing per Platform

> **Status: batas AMAN yang dipakai skill, dicatat 2026-09-23 — BUKAN batas resmi terverifikasi.**
> Marketplace sering mengubah batas karakter (kadang berbeda per kategori). Skill sengaja memakai angka yang
> sama dengan atau lebih ketat dari batas resmi yang pernah berlaku, supaya teks tidak terpotong/ditolak.
> Selalu beri label **"cek batas terbaru di Seller Center"** di output. Jika pengguna memberi batas terbaru,
> pakai angka pengguna (script: `--batas-judul` dan `--batas-deskripsi`).

## Tabel batas aman

| Platform | Judul (aman) | Deskripsi (aman) | Catatan |
|---|---|---|---|
| Shopee | maks **100** karakter | maks **3.000** karakter | Batas resmi pernah lebih longgar dan bisa berbeda per kategori. Tidak ada kolom "poin keunggulan" terpisah → taruh di awal deskripsi. |
| Tokopedia | maks **70** karakter | maks **2.000** karakter | Judul paling ketat → buat versi judul paling ringkas di sini. Sejak bergabung dengan TikTok, alur Seller Center bisa berubah; cek ulang. |
| TikTok Shop | **25–100** karakter | maks **2.000** karakter | Pernah ada batas minimum judul. Pembeli datang dari video/live → deskripsi harus cepat dipindai. |

Area judul yang biasanya terlihat di kartu hasil pencarian HP: kira-kira **40 karakter pertama**
(perkiraan; tergantung ukuran layar). Karena itu kata kunci utama wajib di awal judul.

Cara hitung panjang di script: diambil yang terbesar antara jumlah karakter dan unit UTF-16 (emoji = 2),
agar tidak lolos di skill lalu ditolak di platform.

## Aturan konten yang umum di ketiga platform (ringkasan praktis)

Ini kebiasaan aturan yang sudah lama berlaku; detail resmi ada di pusat edukasi penjual masing-masing.

1. **Dilarang mencantumkan kontak/transaksi di luar platform:** nomor HP/WA, link, @akun sosmed, email,
   "transfer langsung ke rekening". Risiko: produk diturunkan, poin penalti, toko dibekukan.
2. **Dilarang spam kata kunci:** mengulang kata yang sama, menumpuk merek lain yang tidak terkait
   ("mirip Uniqlo", "bukan Zara"), atau kata kunci yang tidak sesuai produk.
3. **Tidak boleh menyesatkan:** harga, ukuran, bahan, isi paket, dan foto harus sesuai.
4. **Klaim yang butuh bukti/izin:** halal (sertifikat BPJPH), izin edar BPOM / PIRT (pangan olahan rumahan),
   SNI (produk wajib SNI), "original" untuk barang bermerek, klaim kesehatan. Hanya tulis jika pengguna
   menyebutkannya — idealnya dengan nomor izin.
5. **Barang tiruan (KW/replika)** melanggar hak merek dan kebijakan marketplace → tolak membantu listing-nya.
6. **Produk terlarang/terbatas** (obat keras, senjata, satwa dilindungi, dsb.) → jangan dibuatkan listing;
   minta pengguna cek daftar produk terlarang di Seller Center.

## Kata kunci: dari mana dan dipakai di mana

- Sumber ide: kolom saran pencarian (ketik produk di kolom cari marketplace, catat saran yang muncul),
  judul pesaing yang laku, cara pembeli menyebut produk (bahasa sehari-hari, singkatan, typo populer).
- Shopee dan Tokopedia tidak punya kolom "tag" umum → kata kunci dimasukkan secara alami ke judul
  dan deskripsi, serta dipakai untuk iklan (Iklan Shopee / TopAds) jika pengguna beriklan.
- TikTok Shop: kata kunci juga berguna untuk caption video & hashtag (arahkan ke skill `konten-mingguan`).
- Jenis kata kunci: **utama** (1, volume besar, masuk awal judul), **pendukung** (3–5, spesifik: bahan,
  ukuran, fungsi), **ekor panjang** (3–6 frasa 3–5 kata, mis. "sambal cumi pedas untuk oleh oleh").

## Pola judul yang dipakai skill

`[Kata kunci utama] + [Pembeda utama] + [Spesifikasi: ukuran/varian/bahan] + [Isi/jumlah] + [Untuk siapa/fungsi]`

Contoh (Tokopedia, 63 karakter): `Sambal Cumi Asin Pedas 200 ml Tanpa Pengawet Oleh Oleh Sidoarjo`
