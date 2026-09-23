# 02 — Google Maps bintang 2: rasa dipuji, pelayanan dikeluhkan (toko fisik)

## Skenario
S2 — permintaan normal: ulasan campuran di Google Maps untuk warung makan. Di Google Maps, eskalasi boleh ke kontak **resmi** usaha
(bukan fitur chat marketplace). Pemilik memberi fakta perbaikan yang **benar-benar** sudah dilakukan.

## Input pengguna
```
Bales review google maps warung aku ya, Bakso Pak Kumis Bekasi. Bintang 2:
"Baksonya enak, kuahnya mantap. Tapi nunggu 40 menit, pelayannya jutek pas ditanya. Sayang banget."
Dari yang nulis kayaknya bapak-bapak. Kami udah tambah 1 pelayan khusus jam makan siang mulai minggu ini.
Kalau mau dihubungi, ada nomor WA resmi di profil Google kami.
```

## Output

## Balasan ulasan — Google Maps, ★2 (negatif/campuran: waktu tunggu + sikap pelayan)

### Balasan publik (utama) — 496 karakter
```
Terima kasih Bapak sudah mampir dan senang baksonya cocok di lidah. Mohon maaf atas waktu tunggu sekitar 40 menit dan sikap tim kami yang kurang ramah — itu tidak seharusnya terjadi. Masukan ini sudah kami bahas bersama tim, dan saat jam makan siang kami kini menambah satu orang di bagian pelayanan. Bila Bapak berkenan menceritakan lebih lanjut, silakan hubungi nomor WhatsApp resmi yang tercantum di profil usaha kami. Semoga kami bisa menyambut Bapak lagi dengan lebih baik. — Bakso Pak Kumis
```

### Alternatif (lebih singkat) — 249 karakter
```
Terima kasih atas ulasannya, Pak. Kami senang baksonya cocok, dan mohon maaf atas waktu tunggu serta pelayanan yang kurang ramah. Masukan ini sudah kami sampaikan ke tim. Silakan hubungi kontak resmi di profil kami bila ingin bercerita lebih lanjut.
```

### Pesan pribadi (jika pengulas menghubungi WA resmi)
```
Selamat siang Pak, terima kasih sudah menghubungi Bakso Pak Kumis. Kami mohon maaf atas pengalaman menunggu lama dan sikap tim kami waktu itu. Boleh kami tahu kira-kira hari dan jam Bapak datang? Supaya bisa kami tindak lanjuti dengan tim yang bertugas. Terima kasih banyak atas masukannya, Pak.
```

### Hasil cek
`cek_balasan.py --platform google --jenis negatif` → **LULUS**, 496/4.000 karakter. Satu temuan **CEK**: kata "WhatsApp" — aman karena yang dirujuk
adalah **nomor resmi usaha di profil**, bukan data pelanggan, dan nomornya tidak ditulis di balasan. Alternatif: LULUS tanpa temuan.
Batas aman skill — cek batas terbaru di Google.

📝 Catatan untuk pemilik:
- Kalimat "menambah satu orang di bagian pelayanan" hanya dipakai karena Bapak/Ibu menyebut sudah melakukannya — pastikan memang berjalan.
- Tidak menawarkan voucher/diskon sebagai ganti ulasan (dilarang kebijakan Google). Kalau ingin memberi kompensasi, berikan saat pengulas datang/menghubungi, tanpa syarat mengubah ulasan.
- Sapaan "Bapak" mengikuti dugaan Bapak/Ibu; kalau ragu, pakai versi alternatif yang netral atau ganti "Kak".

## Catatan penguji
- **Bagus:** pujian disebut spesifik (bakso & kuah), maaf atas dua keluhan, perbaikan nyata hanya dari fakta pengguna, eskalasi ke kontak resmi
  (bukan menulis nomor di balasan), nada tidak defensif. Panjang dicek ulang: 496 & 249 ✔.
- Jenis "bintang 2 tapi ada pujian" diperlakukan sebagai negatif (sesuai references: 1–2★ = negatif; isi campuran tetap dihargai pujiannya).
- **Kurang (ringan):** script memberi CEK untuk kata "WhatsApp" di Google Maps walau yang dimaksud kontak resmi — sudah dijelaskan sebagai aman; wajar
  sebagai pengingat. Untuk marketplace kata yang sama menjadi GAGAL — benar.
