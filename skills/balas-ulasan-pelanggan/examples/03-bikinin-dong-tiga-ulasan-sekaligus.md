# 03 — "balesin dong" 3 ulasan Tokopedia sekaligus (permintaan singkat)

## Skenario
S3 — permintaan singkat/malas dengan banyak ulasan sekaligus (positif, netral, negatif). Tidak ada fakta toko & solusi yang disetujui.
Skill harus langsung membalas dengan asumsi aman, tidak menjanjikan kompensasi, dan tidak memakai pembuka yang sama untuk semua ulasan.

## Input pengguna
```
balesin dong review tokped sambal roa aku:
1. ⭐5 "mantap, barang sesuai, pengiriman cepet"
2. ⭐3 "rasanya enak tp kurang pedes"
3. ⭐1 "udh seminggu ga dateng2 barangnya"
```

## Output

## 1. Balasan ulasan — Tokopedia, ★5 (positif)

### Balasan publik — 175 karakter
```
Makasih banyak Kak! Senang sambal roanya sampai dengan cepat dan sesuai pesanan. Selamat menikmati, semoga cocok jadi teman makan di rumah. Ditunggu order berikutnya ya Kak 🙏
```
### Alternatif (lebih singkat)
```
Terima kasih Kak, senang pesanannya sampai cepat dan sesuai. Selamat menikmati sambal roanya!
```

## 2. Balasan ulasan — Tokopedia, ★3 (netral: rasa kurang pedas)

### Balasan publik — 218 karakter
```
Terima kasih ulasannya, Kak. Senang rasanya cocok, dan masukan soal level pedas yang kurang nendang sudah kami catat untuk tim dapur. Kalau Kakak punya saran seberapa pedas yang pas, boleh ceritakan lewat chat toko ya.
```
### Alternatif (lebih singkat)
```
Makasih masukannya, Kak! Senang rasanya enak. Catatan soal pedasnya kami simpan untuk perbaikan resep.
```

## 3. Balasan ulasan — Tokopedia, ★1 (negatif: pesanan belum sampai)

### Balasan publik — 295 karakter
```
Kak, terima kasih sudah memberi tahu dan mohon maaf pesanannya belum sampai setelah seminggu — kami paham menunggu selama itu sangat mengecewakan. Kami sudah mengirim pesan lewat chat toko untuk mengecek status pengirimannya bersama Kakak. Mohon dicek ya Kak, kami bantu sampai pesanannya jelas.
```
### Alternatif (lebih singkat)
```
Mohon maaf pesanannya belum sampai, Kak. Kami sudah menghubungi Kakak lewat chat toko untuk membantu mengecek pengirimannya.
```
### Pesan chat pribadi
```
Halo Kak, ini [nama admin] dari [nama toko]. Kami sudah membaca ulasan Kakak dan mohon maaf pesanan sambal roanya belum sampai. Kami sedang cek status pengirimannya di sistem. Boleh Kakak konfirmasi apakah alamat di pesanan sudah benar? Nanti kami kabari hasil pengecekannya dan langkah selanjutnya secepatnya. Terima kasih sudah sabar, Kak.
```

### Hasil cek
`cek_balasan.py --platform tokopedia`: ulasan 1 (positif) **LULUS** 175/500; ulasan 2 (netral) **LULUS** 218/500; ulasan 3 (negatif) **LULUS** 295/500.
Tidak ada temuan (tidak ada data pesanan/resi, tidak ada ajakan ke WA, ada maaf & arahan chat untuk ulasan negatif). Batas aman — cek batas terbaru di Tokopedia.

📝 Catatan untuk pemilik:
- Ulasan 3: saya **tidak** menjanjikan kirim ulang atau refund karena belum ada keputusan dari Bapak/Ibu. Cek resi dulu; kalau paket hilang, sebutkan
  solusi yang disetujui (kirim ulang / refund) supaya pesan chat bisa dilengkapi. Balasan publik tidak menyalahkan kurir.
- Kirim pesan chat pribadi dulu, baru posting balasan publik ulasan 3.
- Ulasan 2: kalau memang ada varian yang lebih pedas, beri tahu saya — bisa ditambahkan "coba varian extra pedas" di balasan.
- Asumsi: nama toko & admin tidak disebut → pesan chat memakai `[nama toko]` / `[nama admin]`; balasan publik tanpa tanda tangan.

## Catatan penguji
- **Bagus:** tiga jenis ulasan ditangani dengan kerangka berbeda dan pembuka berbeda (sesuai "jangan memakai kalimat pembuka yang sama persis"); tidak
  bertanya ulang untuk permintaan singkat; tidak menjanjikan kompensasi; tidak menebak penyebab keterlambatan. Panjang dicek ulang: 175/218/295 ✔.
- Ulasan 2 tidak mengarang varian "extra pedas" — hanya ditawarkan sebagai opsi bila memang ada.
- **Kurang (ringan):** SKILL.md meminta "1 balasan utama + 1 alternatif" per ulasan; untuk banyak ulasan sekaligus output jadi panjang. Bisa ditambahkan
  aturan "untuk ≥ 3 ulasan, alternatif opsional" agar lebih ringkas bagi pengguna awam.
