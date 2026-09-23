# 04 — Input tidak lengkap: tanya sekali

## Skenario
S4 — pengguna hanya bilang ingin broadcast promo tanpa isi promo, nama toko, dan cara order (semua info **wajib**).
Skill harus bertanya **sekali**, maksimal 5 pertanyaan bernomor, atau menawarkan jalan cepat.

## Input pengguna
```
Buatin pesan broadcast WA promo buat pelanggan saya dong
```

## Output

Siap, saya bantu! Supaya pesannya pas dan tidak ada info yang salah, saya perlu beberapa hal dulu:

1. **Promonya apa?** Produk/jasa, harga normal → harga promo (atau bentuk promonya), periode, dan syaratnya (mis. minimal beli).
2. **Nama toko/usaha** kamu apa?
3. **Cara order**: cukup balas chat, datang ke toko, atau lewat link (Shopee/Tokopedia/GoFood)?
4. Penerimanya siapa? (pelanggan lama, member, reseller) — dan **apakah mereka sudah setuju** dikirimi info promo lewat WA?
5. Punya **file kontak** (Excel/CSV berisi nama, nomor, persetujuan)? Kalau ada, sekalian kirim dan sebutkan kapan mulai kirim.

Kalau mau cepat, cukup jawab nomor 1–3 saja. Sisanya saya pakai default: 3 variasi, nada santai-sopan dengan sapaan "Kak",
jadwal kirim bertahap pagi hari WIB, dan setiap pesan saya beri kalimat "Balas STOP" untuk berhenti.

## Catatan penguji
- **Bagus:** satu pesan, 5 pertanyaan bernomor dalam bahasa sehari-hari, dengan penanda jelas mana yang wajib dan jalan
  cepat (jawab 1–3 saja). Pertanyaan persetujuan sudah diselipkan sejak awal (langkah 1 skill: UU PDP).
- Tidak memaksakan membuat pesan dengan harga karangan.
- Sesuai tabel Input SKILL.md (isi promo dan nama toko/cara order ditandai "Ya — tanyakan").
