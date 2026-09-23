# 04 — Input tidak lengkap: tanya sekali

## Skenario
S4 — pengguna tidak menyebut produk maupun harga (keduanya **wajib** di tabel Input SKILL.md). Skill harus bertanya sekali,
maks. 5 pertanyaan bernomor, dengan jalan cepat.

## Input pengguna
```
Buatin naskah live buat besok malem ya kak
```

## Output

Siap Kak, saya buatkan. Supaya naskahnya pas dan angka promonya benar, saya perlu info ini dulu:

1. **Produk apa saja** yang mau dijual di live? Sebut nama + keunggulan/spesifikasi utamanya (bahan, ukuran, rasa, dll.), urutkan dari yang paling diandalkan.
2. **Harga normal dan harga/promo live** tiap produk (mis. "89rb jadi 69rb", "diskon 10%", "paket 3 jadi 189rb"). Kalau tidak ada promo, tulis saja harga normalnya.
3. **Live di mana dan berapa lama?** (TikTok Live / Shopee Live / IG / FB, mis. 60 menit mulai jam 19.00)
4. **Nama toko & nama host**, plus info toko: kirim dari kota mana, jadwal kirim, bisa COD atau tidak.
5. Ada **voucher, bonus, atau stok promo yang dibatasi**? Kalau ada, sebut angka yang sebenarnya (misalnya kuota voucher 50).

Kalau mau cepat, cukup jawab nomor 1 dan 2. Sisanya saya pakai default: TikTok Live 60 menit, sapaan "Kak", nama toko/host
dikosongkan untuk diisi, dan info yang belum ada saya tandai `[isi: …]` — tidak saya karang.

## Catatan penguji
- **Bagus:** satu pesan, 5 pertanyaan bernomor, bahasa sehari-hari, contoh format harga yang biasa diketik pengguna. Pertanyaan 5 menanyakan
  stok/kuota **nyata**, sejalan dengan aturan urgensi jujur. Ada jalan cepat dan default disebut jelas.
- Tidak membuat naskah dengan harga karangan.
