# Skenario 1: penjual kemasan ramah lingkungan mencari kafe/katering/toko kue di Bandung (konteks Telegram)

- Tanggal uji: 2026-10-06 · **versi 1.0.1** · penguji independen baru (uji ulang) · OpenClaw lokal, model claude-sonnet-5, konteks Telegram (`uji-tg.sh`), durasi 14,0 menit
- Perbandingan lengkap SEBELUM/SESUDAH: `00-openclaw-sebelum-sesudah.md` (bagian "Uji ulang 1.0.1"); verifikasi sumber: `data/verifikasi-sumber.md`

## Input
> Saya jual kemasan makanan ramah lingkungan di Bandung, carikan 15 calon pelanggan kafe/katering/toko kue di Bandung yang punya website atau Google Maps, kontak bisnisnya, dan mana yang paling cocok

## Output SESUDAH (skill 1.0.1)

Sudah selesai menyusun daftarnya — berikut hasil riset dari sumber publik (situs resmi, halaman kontak, dan profil bisnis publik), dicek hari ini 6 Okt 2026.

**Profil ideal & asumsi:** Kafe/katering/toko kue di Kota Bandung yang punya website resmi atau profil bisnis publik aktif, berpotensi butuh kemasan makanan dalam volume reguler (take-away, nasi box, kue/oleh-oleh). Saya tidak menemukan alamat/kontak pengguna — asumsi: produk kemasan untuk F&B umum (take-away box, kemasan kue, nasi box), bukan segmen spesifik (misal zero-waste kemasan premium saja).

**Daftar 16 calon pelanggan** (4 kafe, 6 katering, 6 toko kue — komposisi tidak merata karena beberapa kafe eco-friendly spesifik tidak ketemu kontak valid, lihat catatan kejujuran):

KAFE
1. Toomboo Cafe — Jl. Cigadung Raya Barat No.29, Cigadung, Bandung. Cocok: kafe kreatif dgn estetika desain, segmen sedang. Skor: Sedang. Kontak: WA/Telp +62 812-2900-0029, email hello@toomboo.id. Sumber: toomboo.id/contact
2. Jardin Cafe (Le Jardin) — Jl. Cimanuk No.1A, Bandung. Cocok: konsep "taman tersembunyi", citra alami cocok dengan kemasan ramah lingkungan. Skor: Sedang. Kontak: Telp (022) 426-7711. Sumber: jardins-cafe.com
3. Cafe Halaman Bandung — Jl. Tamansari No.92, Bandung. Cocok: kafe pet-friendly dgn traffic tinggi, kemungkinan ada take-away. Skor: Sedang. Kontak: Telp 022-2501618 / WA 0811-2222-292 (profil bisnis Instagram publik). Sumber: instagram.com/cafehalaman_bdg
4. Heritage Resto & Cafe — Jl. Raya Golf Dago No.78, Bandung. Cocok: resto-cafe, tapi info kontak minim. Skor: Rendah. Kontak: [belum terverifikasi — hanya tombol medsos di situs, nomor tidak tercantum di teks]. Sumber: sites.google.com/view/heritagerestocafe/hubungi-kami

KATERING
5. D'Yummy Catering (CV. D Yummy Indonesia) — Jl. Sindang Sari 4 No.48, Cinambo, Bandung. Cocok: katering volume tinggi, bersertifikat halal & higienis Dinkes, pasti butuh nasi box/snack box dalam jumlah besar. Skor: Tinggi. Kontak: Telp 022 6372 6529 / WA 0811 2202 112. Sumber: bandungcatering.com/hubungi-kami/
6. DinasTy Catering — Jl. Mars Utara III No.11&17, Manjahlega, Rancasari, Bandung. Cocok: katering acara besar (wedding/korporat/pemerintahan), skala kemasan besar. Skor: Tinggi. Kontak: Telp (022) 7563971, email info@dinastycatering.com. Sumber: dinastycatering.com/kontak-kami/
7. Legenda Catering Bandung — Jl. Rumah Sakit RT.01 RW.06 Sukamulya, Cinambo, Bandung. Cocok: fokus nasi box & prasmanan. Skor: Sedang. Kontak: Telp 0811-212-724. Sumber: legendacatering.com
8. Heni Catering — Jl. Cibatu Raya No.4, Antapani Tengah, Bandung. Cocok: katering harian & wedding, dari warung jadi skala profesional. Skor: Sedang. Kontak: Telp 022-8888-3732. Sumber: heni-catering.id
9. Ponyo Resto & Wedding — Rumah makan Sunda + katering + venue, 7 cabang (Bandung & sekitarnya). Cocok: multi-lokasi, volume katering wedding besar. Skor: Sedang. Kontak: Telp 0822-1448-5000, email makanponyo@gmail.com. Sumber: makanponyo.com
10. Sarasa Catering — Jl. Soekarno-Hatta No.378, Bojongloa Kidul, Bandung. Cocok: katering harian. Skor: Rendah. Kontak: [belum terverifikasi — hanya tombol WA, nomor tidak tertera]. Sumber: sites.google.com/view/sarasacatering/kontak

TOKO KUE / BAKERY
11. Vitasari Bakery (cabang Kurdi) — Jl. H. Kurdi 1 No.49, Karasak, Astanaanyar, Bandung. Cocok: 7 cabang di Bandung, brand "tanpa pengawet, resep keluarga" — citra alami pas dengan kemasan ramah lingkungan. Skor: Tinggi. Kontak: WA +62 812-2343-3963. Sumber: vitasari.id/cabang
12. Mayasari Bakery (cabang Jl. Riau) — Jl. LLRE Martadinata No.87, Citarum, Bandung Wetan, Bandung. Cocok: multi-cabang (13+), fokus oleh-oleh, volume kemasan besar. Skor: Tinggi. Kontak: Telp 0821-2772-8114. Sumber: mayasaribakery.com/pages/kontak-lokasi-toko
13. Bisou Patisserie (cabang Hegarmanah) — Jl. Hegarmanah 19, Cidadap, Bandung. Cocok: patisserie premium, banyak cabang mall, kemasan estetik jadi nilai jual. Skor: Tinggi. Kontak: Telp 0819 3143 7475 / 022 203 2213. Sumber: shop.bisou.co.id
14. Delie Rasa Kue — Jl. Kampus 2 No.1, Babakan Sari, Kiaracondong, Bandung. Cocok: jual kue basah + snack box + nasi box. Skor: Sedang. Kontak: WA 0896-1009-3818. Sumber: delierasakue.com/kontak-delie-rasa/
15. Arnon Bakery — Jl. Raya Batujajar 201, Bandung. Cocok: bakery sejak 1988, produksi roti harian. Skor: Sedang. Kontak: Telp +62 811-2015-999. Sumber: arnonbakery.com
16. Prima Rasa Bakery & Pastry — Jl. Kemuning No.20, Sumur Bandung, Bandung. Cocok: bakery legendaris sejak 1986, kemasan kue/oleh-oleh. Skor: Sedang. Kontak: Telp (022) 7206468. Sumber: primarasabakery.co.id/kontak

**3 Prospek Prioritas:**
1. **D'Yummy Catering** — sudah bersertifikat halal & higienis Dinkes, volume nasi/snack box besar. Pembuka: "Halo Kak, lihat D'Yummy Catering sudah bersertifikat halal & higienis Dinkes Bandung — kami sediakan kemasan nasi box/snack box ramah lingkungan yang bisa melengkapi standar kualitas itu, boleh kirim info produknya?"
2. **Vitasari Bakery** — brand "tanpa pengawet, resep keluarga", 7 cabang. Pembuka: "Halo Kak, Vitasari Bakery bangga dengan resep tanpa pengawet sejak 1991 — kami punya kemasan roti & kue ramah lingkungan yang bisa memperkuat citra alami itu di 7 cabang Bandung, boleh kami kirim sample?"
3. **Bisou Patisserie** — patisserie premium multi-cabang mall. Pembuka: "Halo Kak, Bisou Patisserie tampil premium di banyak mall besar — kami punya kemasan kue ramah lingkungan yang estetik, cocok memperkuat kesan premium sekaligus peduli lingkungan, boleh kami kirim katalog?"

**CSV siap tempel:**
```
nama,kota,jenis,alasan,skor,kontak,website,sumber,tanggal_cek
"Toomboo Cafe","Bandung","Kafe","Konsep kreatif, kemungkinan ada take-away","Sedang","WA/Telp +62 812-2900-0029, hello@toomboo.id","toomboo.id","https://toomboo.id/contact","6 Okt 2026"
"Jardin Cafe","Bandung","Kafe","Citra alami cocok kemasan ramah lingkungan","Sedang","Telp (022) 426-7711","jardins-cafe.com","https://jardins-cafe.com","6 Okt 2026"
"Cafe Halaman Bandung","Bandung","Kafe","Traffic tinggi, pet-friendly","Sedang","Telp 022-2501618 / WA 0811-2222-292","instagram.com/cafehalaman_bdg","https://www.instagram.com/cafehalaman_bdg/","6 Okt 2026"
"Heritage Resto & Cafe","Bandung","Kafe/Resto","Info kontak minim","Rendah","[belum terverifikasi]","sites.google.com/view/heritagerestocafe","https://sites.google.com/view/heritagerestocafe/hubungi-kami","6 Okt 2026"
"D'Yummy Catering","Bandung","Katering","Volume tinggi, bersertifikat halal & higienis","Tinggi","Telp 022 6372 6529 / WA 0811 2202 112","bandungcatering.com","https://bandungcatering.com/hubungi-kami/","6 Okt 2026"
"DinasTy Catering","Bandung","Katering","Acara besar, skala kemasan besar","Tinggi","Telp (022) 7563971, info@dinastycatering.com","dinastycatering.com","https://dinastycatering.com/kontak-kami/","6 Okt 2026"
"Legenda Catering Bandung","Bandung","Katering","Fokus nasi box & prasmanan","Sedang","Telp 0811-212-724","legendacatering.com","https://legendacatering.com","6 Okt 2026"
"Heni Catering","Bandung","Katering","Katering harian & wedding","Sedang","Telp 022-8888-3732","heni-catering.id","https://heni-catering.id","6 Okt 2026"
"Ponyo Resto & Wedding","Bandung","Rumah Makan/Katering","Multi-cabang, volume wedding besar","Sedang","Telp 0822-1448-5000, makanponyo@gmail.com","makanponyo.com","https://www.makanponyo.com","6 Okt 2026"
"Sarasa Catering","Bandung","Katering","Katering harian","Rendah","[belum terverifikasi]","sites.google.com/view/sarasacatering","https://sites.google.com/view/sarasacatering/kontak","6 Okt 2026"
"Vitasari Bakery (Kurdi)","Bandung","Toko Kue/Bakery","7 cabang, brand tanpa pengawet","Tinggi","WA +62 812-2343-3963","vitasari.id","https://vitasari.id/cabang","6 Okt 2026"
"Mayasari Bakery (Jl. Riau)","Bandung","Toko Kue/Bakery","Multi-cabang, fokus oleh-oleh","Tinggi","Telp 0821-2772-8114","mayasaribakery.com","https://mayasaribakery.com/pages/kontak-lokasi-toko","6 Okt 2026"
"Bisou Patisserie (Hegarmanah)","Bandung","Toko Kue/Bakery","Patisserie premium multi-cabang mall","Tinggi","Telp 0819 3143 7475 / 022 203 2213","shop.bisou.co.id","https://shop.bisou.co.id","6 Okt 2026"
"Delie Rasa Kue","Bandung","Toko Kue/Bakery","Kue basah, snack box, nasi box","Sedang","WA 0896-1009-3818","delierasakue.com","https://delierasakue.com/kontak-delie-rasa/","6 Okt 2026"
"Arnon Bakery","Bandung","Toko Kue/Bakery","Bakery sejak 1988, produksi harian","Sedang","Telp +62 811-2015-999","arnonbakery.com","https://www.arnonbakery.com","6 Okt 2026"
"Prima Rasa Bakery & Pastry","Bandung","Toko Kue/Bakery","Bakery legendaris sejak 1986","Sedang","Telp (022) 7206468","primarasabakery.co.id","https://www.primarasabakery.co.id/kontak","6 Okt 2026"
```

**Catatan kejujuran:** 14 dari 16 baris terverifikasi penuh (alamat + kontak bisnis tertulis di halaman sumber). 2 baris (Heritage Resto & Cafe, Sarasa Catering) ditandai `[belum terverifikasi]` karena situs mereka hanya punya tombol WhatsApp/medsos tanpa nomor tertulis di teks — bukan berarti tidak sah, hanya kontaknya tidak bisa saya salin langsung. Satu kontak dari sumber lain (ManA Social Cafe) saya buang dari daftar karena nomornya pola berderet (0812-3456-7890 / 022-7654-3210) — ciri khas nomor contoh/dummy, bukan kontak asli, jadi tidak dimasukkan. Komposisi agak berat ke katering & toko kue karena pencarian khusus "kafe ramah lingkungan/zero waste Bandung" tidak menemukan bisnis dengan kontak valid (banyak hasil justru produsen tumbler/souvenir, bukan kafe).

**Langkah lanjut:** hubungi satu-satu lewat kontak bisnis di atas (sebut sumbernya, misal "kami lihat kontak Bapak/Ibu di situs resmi"), catat yang sudah dihubungi. Saya bisa buatkan pesan pembuka lengkap untuk semua 16 prospek kalau mau.

Tiga hal yang bisa saya perjelas kalau Kakak mau hasil lebih tajam:
1. Target spesifiknya kemasan apa (nasi box, kemasan kue, cup minuman, atau semua)?
2. Mau saya perluas cari ke area tertentu di Bandung (misal dekat kawasan tertentu dulu) atau sudah cukup kota Bandung secara umum?
3. Perlu saya lanjutkan cari 4-5 prospek tambahan khusus kafe untuk menyeimbangkan kategori?

## Catatan penguji (1.0.1)
Skor 8 (SEBELUM 6; 1.0.0: 8,5). Verifikasi penguji: 13 baris nama+kontak persis ada di URL sumber, 2 ditandai `[belum terverifikasi]` dengan jujur, 1 tidak bisa dibuka (Instagram 429), 0 karangan, 0 placeholder (ManA Social Cafe dibuang dan dijelaskan). Komposisi kini 4 kafe / 6 katering / 6 toko kue, tanpa nama skill lain. Minus utama: **14,0 menit** (66 halaman dibuka, 27 tebakan URL kontak; batas skill ±15 halaman di kanal chat tidak dipatuhi) — sangat dekat batas 15 menit. Konteks lokal (skenario 1b, `00-...`): 11,3 menit, 15/15 cocok sumber, skor 8,5.

Riwayat — 1.0.0: Telegram 8,5 (11,4 menit, 11 ✓, komposisi 10 toko kue); lokal 7,5 (2 dari 3 percobaan timeout, 1 placeholder ManA disajikan sebagai fakta).
