# Contoh 4: Input kurang — tanya sekali

> Contoh kerja pembuat skill (bukan hasil uji independen).

## Input pengguna
"Bolu pandan saya enaknya dijual berapa ya?"

## Output agent
Siap bantu. Supaya harganya tidak bikin rugi, saya perlu beberapa info singkat (jawab yang Anda tahu saja):

1. **Modal per loyang** berapa? (Kalau belum tahu, kirim resep + harga beli bahan, saya hitungkan dengan hitung-hpp.)
2. **Ukuran** bolunya (diameter/berat) dan dijual per loyang atau per potong?
3. **Jual di mana?** Langsung/WA, Shopee/Tokopedia, atau GoFood/GrabFood?
4. **Harga toko lain** untuk bolu serupa yang Anda tahu (2–3 contoh cukup).
5. Ingin **untung minimal** berapa persen? (Kalau tidak tahu, saya pakai 40%, lazim untuk kue.)

Kalau mau cepat: sebut saja modal per loyang, saya langsung hitung harga dengan asumsi jual langsung, margin 40%, dan harga cantik.

## Contoh lanjutan (pengguna: "modal 19rb, jual lewat WA, cepat aja")
```
python3 scripts/strategi_harga.py margin --hpp 19000 --margin 40
python3 scripts/strategi_harga.py cantik --harga 31667 --hpp 19000 --margin-min 40
```
- Harga minimum untuk margin 40%: **Rp31.667** (19.000 ÷ 0,6, dibulatkan ke atas).
- Kandidat harga cantik di atas batas: Rp31.900, Rp32.000, Rp39.900. Saran: **Rp32.000** untuk jual tunai/WA (mudah kembalian), atau Rp39.900 bila bolu Anda memakai bahan premium (pandan asli, butter) dan dijelaskan di promosi.
- Asumsi: margin 40%, tanpa potongan, bukan PKP, belum dibandingkan harga pesaing. Kirim 2–3 harga pesaing untuk memastikan posisinya.
