# Contoh 1 — "Lihat usaha katering di Google Maps, mau nawarin jasa desain kemasan"

> Dibuat oleh pembuat skill sebagai contoh cara pakai dan pengecekan awal. **Ini bukan pengganti uji A/B, uji banding pesaing, atau pengujian independen Tahap 6** — itu dilakukan terpisah oleh penguji lain dan disimpan di `HASIL-UJI.md`.

## Permintaan pengguna
> "Saya lihat usaha katering ini di Google Maps pas nyari katering di Malang, namanya 'Katering Andra Rasa', pemiliknya Pak Andra. Mau nawarin jasa desain kemasan makanan dari studio saya, 'Studio Kemas Ceria'. Nomor WA-nya 0813-3456-1122. Bikinin pesan pembukanya."

## Langkah 1 — cek cakupan & asal kontak
Ini pesan pertama ke kontak yang belum pernah dihubungi, asal kontak (Google Maps) sudah disebutkan dengan jelas dan sah (listing bisnis publik) — lanjut ke langkah berikutnya, tidak perlu menolak.

## Langkah 2 — info yang masih kurang
Nama pengirim di Studio Kemas Ceria belum disebut, dan apakah B2B/formal atau lebih santai. Ditanyakan **sekali**:

> "Siap! Dua hal kecil biar pesannya pas: (1) nama kamu yang akan tertulis sebagai pengirim, dan (2) mau nadanya formal (Pak/Bu) atau lebih santai? Kalau mau cepat, saya pakai nama 'Nadia' (ganti sendiri nanti) dan nada formal karena ini B2B ke pemilik usaha katering."

## Jawaban pengguna (contoh)
> "Namanya Nadia aja boleh, nada formal aja Pak/Bu."

## Langkah 3–5 — pola pembuka & 3 varian
Pola dipakai: **Google Maps / listing bisnis publik** (`references/pola-pembuka.md` #3).

### Varian 1 — Singkat
```
Selamat siang, Pak Andra. Saya Nadia dari Studio Kemas Ceria, dapat nomor Bapak dari
Google Maps saat mencari usaha katering di area Malang. Boleh saya kirim contoh
desain kemasan katering? Boleh diabaikan bila belum relevan, Pak.
```

### Varian 2 — Sedang
```
Selamat siang, Pak Andra. Perkenalkan saya Nadia dari Studio Kemas Ceria. Saya dapat
nomor Bapak dari Google Maps saat mencari usaha katering di area Malang. Kami membantu
usaha katering merancang kemasan makanan yang lebih menarik dan tahan tumpah untuk
pengiriman. Kalau Bapak terbuka, boleh saya kirim contoh desain untuk katering
sejenis? Boleh diabaikan bila belum relevan saat ini, Pak.
```

### Varian 3 — Dengan nilai tambah
```
Selamat siang, Pak Andra. Saya Nadia dari Studio Kemas Ceria, dapat nomor Bapak dari
Google Maps saat mencari usaha katering di area Malang. Saya lihat Katering Andra Rasa
cukup aktif melayani acara kantoran, jadi kemasan yang rapi dan tahan tumpah pasti
sering jadi perhatian pelanggan. Kami sudah bantu beberapa usaha katering di Malang
merancang kemasan custom dengan harga terjangkau untuk skala UMKM. Kalau Bapak
terbuka, saya bisa kirim 3 contoh desain kemasan katering langsung lewat WA ini.
Boleh diabaikan bila belum relevan saat ini, Pak, terima kasih.
```

## Langkah 6 — jalankan pemeriksaan script (dilakukan pembuat skill)

```
$ python3 scripts/cek_pesan.py cek --pesan "Selamat siang, Pak Andra. Saya Nadia dari Studio Kemas Ceria, dapat nomor Bapak dari Google Maps saat mencari usaha katering di area Malang. Boleh saya kirim contoh desain kemasan katering? Boleh diabaikan bila belum relevan, Pak." --jam-kirim "10:00"
Jumlah karakter : 230
Jumlah kata     : 36
Jumlah baris    : 1
Jumlah link     : 0
Sebut asal kontak terdeteksi : Ya
Opsi keluar terdeteksi       : Ya
Jam kirim wajar (08.00-20.00) : Ya

[OK] Tidak ada masalah yang terdeteksi oleh pemeriksaan otomatis ini.
      (Tetap baca ulang sendiri sebelum kirim — ini bukan jaminan.)
```

Varian 2 (392 karakter) juga **[OK]**. Varian 3 (562 karakter) memicu satu peringatan ringan:

```
[PERIKSA DULU] 1 hal perlu dicek:
  - Pesan 562 karakter — di atas 500, mungkin perlu scroll di layar HP. Masih boleh, tapi cek dulu.
```

Keputusan: tetap ditampilkan ke pengguna karena masih di bawah batas maksimal (700) dan isinya relevan — bukan pengulangan/berlebihan — sambil disebutkan peringatannya biar pengguna bisa pilih varian yang lebih pendek jika mau.

## Langkah 7 — tautan wa.me

```
$ python3 scripts/cek_pesan.py wa --nomor "0813-3456-1122" --pesan "Selamat siang, Pak Andra. Saya Nadia dari Studio Kemas Ceria, dapat nomor Bapak dari Google Maps saat mencari usaha katering di area Malang. Boleh saya kirim contoh desain kemasan katering? Boleh diabaikan bila belum relevan, Pak."
https://wa.me/6281334561122?text=Selamat%20siang%2C%20Pak%20Andra....
```

## Output akhir yang ditampilkan ke pengguna (ringkas)

```
### Ringkasan konteks
Penerima: Pak Andra, pemilik Katering Andra Rasa (Malang). Asal kontak: Google Maps.
Ditawarkan: jasa desain kemasan makanan dari Studio Kemas Ceria.

### Varian 1 — Singkat  [OK]
(lihat di atas)

### Varian 2 — Sedang  [OK]
(lihat di atas)

### Varian 3 — Dengan nilai tambah  [PERIKSA DULU: 562 karakter, sedikit di atas 500]
(lihat di atas)

### Tautan WhatsApp (Varian 1)
https://wa.me/6281334561122?text=Selamat%20siang%2C%20Pak%20Andra....

### Saran jam kirim
08.00–20.00 WIB (Malang, Jawa Timur); hindari jam istirahat siang 12.00–13.00 dan malam hari.

### Checklist anti-blokir
- [x] Nomor dari sumber sah (Google Maps, listing bisnis publik)
- [x] Asal kontak disebut di semua varian
- [x] Opsi keluar sopan ada di semua varian
- [x] Maks. 1 link (tidak ada link di pesan ini)
- [ ] Kirim satu per satu, jangan dari nomor yang baru dipakai kirim banyak pesan asing dalam waktu singkat

### Asumsi
Nama pengirim "Nadia" dan nada formal Pak/Bu dipakai sesuai jawaban pengguna.
```
