# 04 — Input tidak lengkap: ulasan belum ditempel

## Skenario
S4 — pengguna meminta balasan tanpa menempelkan teks ulasan (satu-satunya info **wajib**). Skill harus meminta ulasan sekali, bersama pertanyaan
lain yang berguna (maks. 5, bernomor).

## Input pengguna
```
Tolong balasin ulasan jelek di toko saya dong, bikin kesel
```

## Output

Siap, saya bantu balas dengan tenang supaya calon pembeli yang membaca justru makin percaya. Saya perlu beberapa hal dulu:

1. **Tempel teks ulasannya** (dan bintangnya kalau ada). Kalau lebih dari satu, tempel semuanya sekaligus.
2. **Di mana ulasannya?** Shopee, Tokopedia, TikTok Shop, atau Google Maps?
3. **Nama toko** dan nama admin yang akan membalas chat (opsional, untuk tanda tangan).
4. **Fakta dari sisi toko**, kalau ada: misalnya paket sudah dikirim tanggal berapa, barang sudah dicek sebelum dikemas, stok memang habis.
5. **Solusi yang kamu setujui**, kalau ada: tukar barang, kirim ulang, refund, atau belum diputuskan.

Kalau mau cepat, cukup tempel ulasannya saja (nomor 1). Sisanya saya pakai asumsi aman: tidak menjanjikan ganti/refund, penyelesaian diarahkan ke
chat pribadi, dan tanpa tanda tangan.

## Catatan penguji
- **Bagus:** satu pesan, 5 pertanyaan bernomor, jalan cepat jelas. Nada menenangkan pengguna yang emosi ("bikin kesel") tanpa menggurui. Pertanyaan
  4–5 mencegah agent mengarang fakta toko atau menjanjikan kompensasi — sesuai tabel Input & langkah 2 SKILL.md.
