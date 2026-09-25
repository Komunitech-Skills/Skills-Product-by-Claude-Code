# Skenario 02 (normal) — Supplier biji kopi → kafe dari Google Maps

> Uji independen Tahap 6 (2026-09-25). Nama usaha/nomor fiktif.

## Permintaan pengguna
> "Aku Bima, punya roastery kecil 'Lereng Arjuno Roastery' di Malang. Nemu kafe 'Kopi Senja Dago' di Google Maps waktu nyari kafe specialty di Dago Bandung. Dari foto menunya kayaknya banyak manual brew. Nomornya +62 857-2211-3344 (dari Maps). Mau nawarin biji single origin Jatim (Arjuno, Ijen, Dampit), min order 5 kg, kirim max 3 hari setelah sangrai, dan aku mau kasih 2 sampel 100 gr gratis. Santai aja bahasanya, pake Kak."

## Langkah yang dijalankan agent
1. Cakupan: pesan pertama, satu kafe → lanjut.
2. Asal kontak: nomor tercantum di listing Google Maps bisnis → sah (`dasar-hukum-wa.md` §1).
3. Pola #3 Google Maps: sebut kategori pencarian & area.
4. **Draf pertama mengikuti kalimat pola #3 persis** ("Saya melihat Kopi Senja Dago di Google Maps saat mencari kafe specialty di area Dago…") → script: **"Sebut asal kontak terdeteksi: Tidak"** + peringatan. Padahal asal kontak jelas tertulis. Agent menilai manual (sesuai catatan Langkah 6), lalu tetap menulis ulang dengan frasa "dapat nomor … dari Google Maps" agar lolos script. → **Bug heuristik, lihat HASIL-UJI.md (B1).**
5. Nomor berformat `+62 857-2211-3344` dinormalisasi script → `6285722113344` (diverifikasi manual: buang `+`, spasi, strip → benar).

---

## Output ke pengguna

### Ringkasan konteks
Penerima: Kopi Senja Dago (Bandung, WIB). Asal kontak: listing Google Maps saat mencari kafe specialty di Dago. Ditawarkan: biji kopi single origin Jawa Timur, grosir untuk kafe. B2B santai → "Kak".

### Varian 1 — Singkat
```
Selamat pagi, Kak. Saya Bima dari Lereng Arjuno Roastery di Malang, dapat nomor Kopi Senja Dago dari Google Maps saat mencari kafe specialty di Dago. Boleh saya kirim daftar harga biji kopi grosir kami? Boleh diabaikan bila belum relevan ya, Kak.
```
Script: 246 karakter, 41 kata, asal kontak ✔, opsi keluar ✔, jam 09:30 ✔ → **[OK]**

### Varian 2 — Sedang
```
Selamat pagi, Kak. Perkenalkan saya Bima dari Lereng Arjuno Roastery di Malang.
Saya dapat nomor Kopi Senja Dago dari Google Maps saat mencari kafe specialty di area Dago, Bandung.
Kami menyangrai biji kopi single origin Jawa Timur (Arjuno, Ijen, Dampit) untuk kafe, dengan minimal order 5 kg.
Boleh saya kirim daftar harga dan jadwal sangrainya? Mohon maaf mengganggu, dan boleh diabaikan bila tidak relevan, Kak.
```
Script: 414 karakter, 65 kata → **[OK]**

### Varian 3 — Dengan nilai tambah
```
Selamat pagi, Kak. Saya Bima dari Lereng Arjuno Roastery di Malang, dapat nomor Kopi Senja Dago dari Google Maps saat mencari kafe specialty di Dago.
Dari foto menu di Maps, Kopi Senja banyak menyajikan manual brew, jadi kemungkinan butuh stok beans yang konsisten tiap minggu.
Kami menyangrai single origin Jawa Timur sesuai pesanan, dikirim maksimal 3 hari setelah sangrai, minimal order 5 kg.
Kalau Kakak terbuka, saya bisa kirimkan 2 sampel 100 gram gratis untuk dicoba barista, cukup balas "boleh".
Boleh diabaikan bila belum relevan, Kak. Terima kasih.
```
Script: 558 karakter, 88 kata → **[PERIKSA DULU]** "Pesan 558 karakter — di atas 500…". Kata "gratis" (tanpa `!!`) tidak dianggap pemicu spam — benar, karena sampel gratis memang ditawarkan pengguna. Penilaian agent: layak dipakai bila penerima pemilik kafe yang suka detail; kalau ragu, pakai varian 2.

### Tautan WhatsApp (varian 2)
```
https://wa.me/6285722113344?text=Selamat%20pagi%2C%20Kak.%20Perkenalkan%20saya%20Bima%20dari%20Lereng%20Arjuno%20Roastery%20di%20Malang.%0ASaya%20dapat%20nomor%20Kopi%20Senja%20Dago%20dari%20Google%20Maps%20saat%20mencari%20kafe%20specialty%20di%20area%20Dago%2C%20Bandung.%0AKami%20menyangrai%20biji%20kopi%20single%20origin%20Jawa%20Timur%20%28Arjuno%2C%20Ijen%2C%20Dampit%29%20untuk%20kafe%2C%20dengan%20minimal%20order%205%20kg.%0ABoleh%20saya%20kirim%20daftar%20harga%20dan%20jadwal%20sangrainya%3F%20Mohon%20maaf%20mengganggu%2C%20dan%20boleh%20diabaikan%20bila%20tidak%20relevan%2C%20Kak.
```
Buka, cek, lalu kirim sendiri.

### Saran jam kirim
Bandung = WIB (sama dengan Malang). Kafe biasanya sibuk mulai siang–malam; kirim **09.00–11.00 WIB** saat persiapan buka. Hindari jam ramai sore/malam walau masih di bawah 20.00.

### Checklist anti-blokir
- [x] Nomor dari listing bisnis publik Google Maps
- [x] Asal kontak + kategori pencarian + area disebut
- [x] Opsi keluar sopan, tanpa link, tanpa kapital berlebihan
- [ ] Nama & foto profil WA jelas mewakili roastery
- [ ] Jangan kirim ke banyak kafe sekaligus dalam waktu berdekatan dari nomor pribadi — beri jeda wajar antar-kontak

### Asumsi
- "Banyak manual brew" berasal dari pengamatan pengguna atas foto menu (bukan karangan agent).
- Nomor di Maps dianggap nomor WA usaha; bila ternyata nomor telepon rumah/ pribadi pemilik, pertimbangkan menelepon atau DM Instagram usaha.
