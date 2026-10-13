# 01 — Shopee bintang 1: salah kirim ukuran + chat lambat

## Skenario
S1 — permintaan normal dan lengkap: ulasan negatif marketplace, dua masalah (salah ukuran, pelayanan chat lambat), pemilik memberi solusi yang
disetujui (tukar ukuran, ongkir retur ditanggung). Script `cek_balasan.py` dijalankan untuk balasan publik.

## Input pengguna
```
Tolong balasin ulasan Shopee bintang 1 ini buat toko aku Rumah Alya:
"Pesen gamis ukuran L yang dateng M!! Udah gitu chat seller slow respon 2 hari. Nyesel belanja di sini."
Kami mau tukar ke L, ongkir retur kami yang tanggung. Admin yang pegang chat namanya Nisa.
```

## Output

## Balasan ulasan — Shopee, ★1 (negatif: salah kirim ukuran + pelayanan chat)

### Balasan publik (utama) — 294 karakter
```
Kak, terima kasih sudah memberi tahu, dan mohon maaf gamis yang diterima tidak sesuai ukuran pesanan serta balasan chat kami lambat. Ini bukan pengalaman yang kami harapkan untuk Kakak. Kami sudah mengirim pesan lewat chat toko untuk membantu penukaran ukuran — mohon dicek ya Kak. — Rumah Alya
```

### Alternatif (lebih singkat) — 175 karakter
```
Mohon maaf atas ukuran yang tertukar dan respons chat yang lambat, Kak. Kami sudah menghubungi Kakak lewat chat toko untuk membantu penukarannya. Terima kasih atas masukannya.
```

### Pesan chat pribadi (kirim lewat chat toko Shopee)
```
Halo Kak, ini Nisa dari Rumah Alya. Kami sudah membaca ulasan Kakak dan mohon maaf gamis yang datang ukuran M, padahal Kakak memesan L. Kami bantu tukar ke ukuran L, dan ongkir retur kami yang tanggung. Boleh kirimkan foto label ukuran di gamis yang diterima? Setelah itu kami kirimkan alamat retur dan kode pengirimannya. Terima kasih sudah sabar, Kak.
```

### Hasil cek
`cek_balasan.py --platform shopee --jenis negatif` → **LULUS**, 294/500 karakter, tidak ada temuan (ada terima kasih, maaf, arahan ke chat toko; tidak
ada data pribadi/nomor pesanan; tidak ada ajakan ke WA). Draf pertama memuat "bukan pengalaman yang **seharusnya Kakak** dapat" → script menandai
**CEK** nada defensif; kalimat diganti agar tidak memicu salah baca. Alternatif: LULUS, tanpa temuan. Batas aman skill — cek batas terbaru di Shopee.

📝 Catatan untuk pemilik:
- **Kirim pesan chat pribadi dulu**, baru posting balasan publik (karena balasan publik menyebut "sudah mengirim pesan").
- Balasan publik sengaja tidak menyebut "ongkir retur kami tanggung" agar tidak menjadi janji umum untuk semua pembeli; janji itu cukup di chat pribadi.
- Jangan meminta pembeli mengubah bintang sebagai syarat penukaran. Setelah selesai, boleh tambah balasan publik singkat: "Terima kasih Kak, senang penukarannya sudah beres."
- Balasan publik tidak memuat janji perbaikan proses (mis. "ke depan kami menambah pengecekan ukuran") karena tidak diberikan pemilik; tambahkan hanya bila memang akan dilakukan (asumsi, ganti dengan data Anda).
- Balasan publik tidak mengakui "salah kami" sebelum dicek (bisa juga salah ambil varian saat checkout) — cukup minta maaf atas pengalamannya.

## Catatan penguji
- **Bagus:** kerangka negatif lengkap (terima kasih → maaf → langkah → chat toko → perbaikan), tidak defensif, tidak menyalahkan pembeli, tidak ada data
  pesanan, tidak mengarahkan ke WA. Janji kompensasi hanya di chat pribadi dan persis sesuai persetujuan pemilik. Panjang dicek ulang: 294 & 175 ✔.
- Nama admin "Nisa" dari pengguna; tidak ada data pribadi pembeli.
- **Kurang (ringan):** `POLA_DEFENSIF` (`\bseharusnya\s+(kakak|anda…)`) menandai kalimat yang justru empatik ("pengalaman yang seharusnya Kakak dapat") —
  false positive. Juga, bila pesan chat pribadi ikut dicek, script memberi SARAN "arahkan ke chat pribadi" yang tidak relevan; SKILL.md sudah benar
  hanya meminta cek balasan publik.
