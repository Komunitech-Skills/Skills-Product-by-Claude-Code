# Skenario 04 (input tidak lengkap) — asal kontak tidak disebut, pengguna ingin cepat

> Uji independen Tahap 6 (2026-09-25). Nama & nomor fiktif.

## Giliran 1 — permintaan pengguna
> "Tolong bikinin chat WA buat nawarin jasa saya ke calon klien, nomornya 0812 9988 7766. Cepet ya."

### Respons agent (mengikuti Input + Langkah 1–2)
Info wajib yang kurang: nama/usaha penerima, **asal kontak**, produk/jasa. Ditanyakan **sekali**, maks. 5 pertanyaan bernomor:

> Siap, biar pesannya pas dan tidak terkesan spam, saya perlu 4 info singkat:
> 1. Nama calon klien dan usahanya apa?
> 2. **Nomornya didapat dari mana?** (mis. dikenalkan teman, ketemu di pameran, Google Maps, Instagram, grup WA) — ini wajib, karena pesan pertama yang jelas asal-usulnya jauh lebih dipercaya, dan penting untuk aturan data pribadi.
> 3. Jasa kamu apa dan nama usahanya?
> 4. Nama kamu sebagai pengirim?
>
> Nada bahasa saya buat sopan semi-formal kecuali kamu minta lain.

## Giliran 2 — jawaban pengguna (asal kontak masih mengelak)
> "Jasa foto produk, namaku Fajar, usahanya Lensa Kita di Depok. Calonnya Bu Rina, toko kue rumahan. Nomornya ya dapet aja lah, pokoknya cepet bikinin."

### Respons agent (Batasan: tanyakan sekali lagi secara spesifik, asal kontak tidak boleh dikarang)
> Hampir jadi, Kak Fajar. Tinggal satu hal yang tidak bisa saya karang: **nomor Bu Rina dapat dari mana?** Pilih saja yang paling mendekati:
> (a) dari teman/kenalan — sebut namanya, (b) grup WA/komunitas — sebut nama grupnya, (c) Google Maps/Instagram usahanya, (d) ketemu langsung di acara, (e) lainnya.
> Kalau nomornya dari daftar yang dibeli atau disebar orang tanpa izin, saya tidak bisa membuatkan pesannya — risikonya melanggar UU PDP dan nomor Kakak bisa diblokir WhatsApp.

## Giliran 3 — jawaban pengguna
> "Oh dari grup WA UMKM Depok, kemarin dia posting nyari fotografer buat foto kue."

→ Sah (sesama anggota grup, penerima sendiri mengumumkan kebutuhan). Pola #5 Grup komunitas. Pengguna ingin cepat → default dipakai dan dicatat di Asumsi.

---

## Output ke pengguna

### Ringkasan konteks
Penerima: Bu Rina (toko kue rumahan, Depok). Asal kontak: grup WA UMKM Depok, Bu Rina posting mencari fotografer produk kue. Ditawarkan: jasa foto produk Lensa Kita. B2C/UMKM kecil → "Bu" (lebih aman daripada "Kak" untuk pemilik usaha yang belum dikenal).

### Varian 1 — Singkat
```
Selamat siang, Bu Rina. Saya Fajar dari Lensa Kita, sama-sama anggota grup WA UMKM Depok, dan dapat nomor Ibu dari grup tersebut. Ibu sempat posting mencari fotografer produk kue, boleh saya kirim beberapa contoh foto kami? Boleh diabaikan bila sudah dapat ya, Bu.
```
Script (jam 13:00): 264 karakter, 43 kata → **[OK]**

### Varian 2 — Sedang
```
Selamat siang, Bu Rina. Perkenalkan saya Fajar dari Lensa Kita, jasa foto produk di Depok.
Saya dapat nomor Ibu dari grup WA UMKM Depok, karena kemarin Ibu sempat posting sedang mencari fotografer untuk produk kue.
Kami biasa memotret produk makanan untuk katalog dan feed Instagram, bisa di studio atau datang ke dapur.
Boleh saya kirim beberapa contoh hasil fotonya? Mohon maaf mengganggu, dan boleh diabaikan bila sudah dapat fotografer, Bu.
```
Script: 444 karakter, 70 kata → **[OK]**

### Varian 3 — Dengan nilai tambah
```
Selamat siang, Bu Rina. Saya Fajar dari Lensa Kita, dapat nomor Ibu dari grup WA UMKM Depok.
Kemarin Ibu posting sedang mencari fotografer untuk produk kue, jadi saya ingin menawarkan diri.
Kami memotret produk makanan untuk katalog dan feed Instagram, bisa datang langsung ke dapur supaya kue tetap segar saat difoto.
Kalau Ibu berkenan, saya kirim 5 contoh foto dan daftar paketnya dulu, cukup balas "boleh".
Boleh diabaikan bila sudah dapat fotografer, Bu. Terima kasih.
```
Script: 473 karakter, 75 kata → **[OK]**

### Tautan WhatsApp (varian 1)
```
https://wa.me/6281299887766?text=Selamat%20siang%2C%20Bu%20Rina.%20Saya%20Fajar%20dari%20Lensa%20Kita%2C%20sama-sama%20anggota%20grup%20WA%20UMKM%20Depok%2C%20dan%20dapat%20nomor%20Ibu%20dari%20grup%20tersebut.%20Ibu%20sempat%20posting%20mencari%20fotografer%20produk%20kue%2C%20boleh%20saya%20kirim%20beberapa%20contoh%20foto%20kami%3F%20Boleh%20diabaikan%20bila%20sudah%20dapat%20ya%2C%20Bu.
```

### Saran jam kirim
Depok = WIB. Kirim hari ini 13.00–16.00 WIB selagi postingannya masih baru; jangan lewat 20.00.

### Checklist anti-blokir
- [x] Sesama anggota grup (jangan mengaku anggota bila bukan)
- [x] Menyebut nama grup & postingan yang relevan
- [x] Opsi keluar sopan, tanpa link di pesan pertama (kirim contoh foto setelah dibalas)
- [ ] Jangan ikut menawarkan di grup sekaligus japri berkali-kali

### Asumsi
- Sapaan "Bu", nada sopan semi-formal (pengguna minta cepat, tidak menyebut gaya).
- "Bisa datang ke dapur" & "5 contoh foto" — **ganti** bila tidak sesuai layanan Kakak; saya tidak menambah harga, jumlah klien, atau testimoni karena tidak disebutkan.

---

## Catatan penguji
- Perilaku sesuai spesifikasi: bertanya sekali (4 poin), asal kontak ditanya ulang **satu kali** secara spesifik, tidak mengarang asal kontak walau didesak "cepet".
- Ambiguitas kecil: aturan "tanya sekali" vs "tanya sekali lagi soal asal kontak" — SKILL.md sudah membolehkan (Batasan poin 1), jadi bukan pelanggaran.
- Asumsi "bisa datang ke dapur" sebenarnya detail yang tidak diberikan pengguna → agent menandainya di Asumsi; idealnya varian tanpa detail tersebut. Catatan untuk template: tidak ada panduan tentang detail layanan yang "wajar diasumsikan" vs "dilarang dikarang" (hanya bukti/testimoni yang eksplisit dilarang).
