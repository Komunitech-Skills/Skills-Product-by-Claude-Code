# Skenario 1: penjual kemasan ramah lingkungan mencari kafe/katering/toko kue di Bandung (Telegram + lokal)

- Tanggal uji: 2026-10-06 · **versi 1.0.2** · penguji independen ketiga · OpenClaw lokal, model claude-sonnet-5; konteks Telegram (`uji-tg.sh`) 5,0 menit, lokal 3,2 menit
- Perbandingan lengkap SEBELUM/SESUDAH: `00-openclaw-sebelum-sesudah.md` (bagian "Uji ulang 1.0.2"); verifikasi sumber: `data/verifikasi-sumber.md`

## Input
> Saya jual kemasan makanan ramah lingkungan di Bandung, carikan 15 calon pelanggan kafe/katering/toko kue di Bandung yang punya website atau Google Maps, kontak bisnisnya, dan mana yang paling cocok

## Output SESUDAH (skill 1.0.2), konteks lokal — 3,2 menit, 15/15 baris terbukti

Sudah saya carikan lewat halaman direktori publik (bukan membuka tiap situs usaha satu-satu). Berikut hasilnya.

**Profil ideal & asumsi:** Pembeli kemasan makanan ramah lingkungan = kafe, jasa katering, dan toko kue/bakery di Bandung yang aktif jual makanan/minuman take-away atau kirim pesanan dalam kotak — makin besar volume dan makin "branded", makin cocok. Kota: Bandung (sesuai permintaan). Komposisi dibuat merata: 5 kafe, 5 katering, 5 toko kue/bakery.

**Tabel 15 calon pelanggan**

*Nama usaha dari direktori publik; kontak disamarkan dalam contoh ini.* Kolom "Alasan cocok" hanya mengulang yang tertulis di sumber yang dikutip; skor adalah perkiraan kecocokan, bukan data ukuran atau kebutuhan usaha. Cek langsung sebelum menghubungi.

| No | Nama usaha | Kota | Jenis | Alasan cocok | Skor | Kontak bisnis publik | Sumber (URL) | Dicek |
|---|---|---|---|---|---|---|---|---|
| 1 | Kartika Sari Pusat | Bandung | Toko kue/bakery | Menurut halaman direktori: 9 outlet; situs dan email tercantum (perlu dicek langsung) | Tinggi | (022) xxx1355, order@…, kartikasari.com | alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html | 6 Okt 2026 |
| 2 | Amanda Brownies Pusat | Bandung | Toko kue/bakery | Menurut halaman direktori: gerai pusat dengan situs resmi; cabang Hj. Juanda juga terdaftar (perlu dicek langsung) | Tinggi | (022) xxx4657, amandabrownies.co.id | alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html | 6 Okt 2026 |
| 3 | Holland Bakery Buah Batu | Bandung | Toko kue/bakery | Menurut halaman direktori: gerai Buah Batu dengan situs resmi tercantum (perlu dicek langsung) | Sedang | (022) xxx4499, hollandbakery.co.id | alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html | 6 Okt 2026 |
| 4 | Amanda Brownies Hj. Juanda | Bandung | Toko kue/bakery | Menurut halaman direktori: cabang kedua merek yang sama (Hj. Juanda) dengan situs resmi (perlu dicek langsung) | Sedang | (022) xxx6123, amandabrownies.co.id | alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html | 6 Okt 2026 |
| 5 | Kartika Sari Cake Shop (Jl. Ir. H. Djuanda) | Bandung | Toko kue/bakery | Menurut halaman direktori: gerai di Jl. Ir. H. Djuanda dengan situs resmi tercantum (perlu dicek langsung) | Sedang | (022) xxx9500, kartikasari.com | alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html | 6 Okt 2026 |
| 6 | Cita Rasa Catering | Bandung | Katering | Menurut halaman direktori: katering di komplek perumahan (Taman Holis Indah); kebutuhan kemasan belum diketahui (perlu dicek langsung) | Tinggi | (022) xxx0781 | alamatpenting.com/daftar-alamat-catering-di-bandung/ | 6 Okt 2026 |
| 7 | Citra Boga Bandung (by [nama pemilik]) | Bandung | Katering | Menurut halaman direktori: terdaftar sebagai katering (perlu dicek langsung) | Tinggi | (022) xxx1921 | alamatpenting.com/daftar-alamat-catering-di-bandung/ | 6 Okt 2026 |
| 8 | Adinda Catering | Bandung | Katering | Menurut halaman direktori: terdaftar sebagai katering (perlu dicek langsung) | Sedang | (022) xxx1884 | alamatpenting.com/daftar-alamat-catering-di-bandung/ | 6 Okt 2026 |
| 9 | Asparagus Catering | Bandung | Katering | Menurut halaman direktori: katering di area Lengkong (perlu dicek langsung) | Sedang | (022) xxx3730 | alamatpenting.com/daftar-alamat-catering-di-bandung/ | 6 Okt 2026 |
| 10 | Bey Catering Service & Wedding Organizer | Bandung | Katering | Menurut halaman direktori: katering sekaligus wedding organizer (perlu dicek langsung) | Sedang | (022) xxx0039, 08xx-xxxx1490 | alamatpenting.com/daftar-alamat-catering-di-bandung/ | 6 Okt 2026 |
| 11 | Armor Kopi | Bandung (Cimenyan) | Kafe | Menurut halaman direktori: kafe di kawasan Cimenyan, nomor kontak tercantum (perlu dicek langsung) | Tinggi | 08xx-xxxx-0941 | alamatpenting.com/daftar-alamat-cafe-di-bandung/ | 6 Okt 2026 |
| 12 | 56 Degrees Cafe | Bandung | Kafe | Menurut halaman direktori: alamat di Paskal Hyper Square (perlu dicek langsung) | Sedang | (022) xxxx0668 | alamatpenting.com/daftar-alamat-cafe-di-bandung/ | 6 Okt 2026 |
| 13 | 13 Cups Coffee House | Bandung | Kafe | Menurut halaman direktori: coffee house di area ruko (perlu dicek langsung) | Sedang | 08xx-xxxx-1313 | alamatpenting.com/daftar-alamat-cafe-di-bandung/ | 6 Okt 2026 |
| 14 | Abraham And Smith | Bandung | Kafe | Menurut halaman direktori: cafe & eatery di Bandung (perlu dicek langsung) | Sedang | (022) xxxx3371 | alamatpenting.com/daftar-alamat-cafe-di-bandung/ | 6 Okt 2026 |
| 15 | 18 Hrs Cafe | Bandung | Kafe | Menurut halaman direktori: cafe di area Setiabudhi (perlu dicek langsung) | Rendah | (022) xxx2600 | alamatpenting.com/daftar-alamat-cafe-di-bandung/ | 6 Okt 2026 |

**3 prospek prioritas**
1. **Kartika Sari Pusat** — menurut halaman direktori punya 9 outlet dan email resmi, jadi bisa dihubungi tertulis lebih dulu (ukuran usaha dan kebutuhan kemasan perlu dicek langsung). *Pembuka:* "Selamat siang, saya lihat Kartika Sari punya banyak gerai di Bandung — apakah boleh saya kirimkan contoh kemasan makanan ramah lingkungan untuk kebutuhan kue dan hampers Bapak/Ibu?"
2. **Cita Rasa Catering** — terdaftar di direktori sebagai katering di Komplek Taman Holis Indah; kebutuhan kotak makan dan minat pasokan rutin belum diketahui (perlu dicek langsung). *Pembuka:* "Selamat siang, saya melihat Cita Rasa Catering di Komplek Taman Holis Indah — kami sediakan kemasan makanan ramah lingkungan untuk box katering, apakah boleh saya kirim info produknya?"
3. **Armor Kopi** — kafe di kawasan Cimenyan dengan nomor kontak tercantum di direktori; minat pada kemasan ramah lingkungan perlu ditanyakan langsung. *Pembuka:* "Halo, saya lihat Armor Kopi di kawasan Cimenyan — mungkin cocok juga pakai kemasan to-go yang ramah lingkungan, boleh saya kirim contohnya?"

Mau saya buatkan pesan pembuka lengkap (versi WA) untuk ketiganya?

**CSV siap tempel**
```
nama,kota,jenis,alasan,skor,kontak,website,sumber,tanggal_cek
"Kartika Sari Pusat","Bandung","Toko kue/bakery","9 outlet menurut direktori; situs dan email tercantum","Tinggi","(022) xxx1355; order@…","kartikasari.com","alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html","6 Okt 2026"
"Amanda Brownies Pusat","Bandung","Toko kue/bakery","Gerai pusat dengan situs resmi, tercantum di direktori","Tinggi","(022) xxx4657","amandabrownies.co.id","alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html","6 Okt 2026"
"Holland Bakery Buah Batu","Bandung","Toko kue/bakery","Gerai Buah Batu dengan situs resmi, tercantum di direktori","Sedang","(022) xxx4499","hollandbakery.co.id","alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html","6 Okt 2026"
"Amanda Brownies Hj. Juanda","Bandung","Toko kue/bakery","Cabang kedua merek yang sama, tercantum di direktori","Sedang","(022) xxx6123","amandabrownies.co.id","alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html","6 Okt 2026"
"Kartika Sari Cake Shop","Bandung","Toko kue/bakery","Gerai di Jl. Ir. H. Djuanda, tercantum di direktori","Sedang","(022) xxx9500","kartikasari.com","alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html","6 Okt 2026"
"Cita Rasa Catering","Bandung","Katering","Katering di komplek perumahan menurut direktori; kebutuhan kemasan belum diketahui","Tinggi","(022) xxx0781","","alamatpenting.com/daftar-alamat-catering-di-bandung/","6 Okt 2026"
"Citra Boga Bandung","Bandung","Katering","Terdaftar sebagai katering di direktori","Tinggi","(022) xxx1921","","alamatpenting.com/daftar-alamat-catering-di-bandung/","6 Okt 2026"
"Adinda Catering","Bandung","Katering","Terdaftar sebagai katering di direktori","Sedang","(022) xxx1884","","alamatpenting.com/daftar-alamat-catering-di-bandung/","6 Okt 2026"
"Asparagus Catering","Bandung","Katering","Katering di area Lengkong menurut direktori","Sedang","(022) xxx3730","","alamatpenting.com/daftar-alamat-catering-di-bandung/","6 Okt 2026"
"Bey Catering Service & Wedding Organizer","Bandung","Katering","Katering sekaligus wedding organizer menurut direktori","Sedang","(022) xxx0039; 08xx-xxxx1490","","alamatpenting.com/daftar-alamat-catering-di-bandung/","6 Okt 2026"
"Armor Kopi","Bandung","Kafe","Kafe di kawasan Cimenyan menurut direktori","Tinggi","08xx-xxxx-0941","","alamatpenting.com/daftar-alamat-cafe-di-bandung/","6 Okt 2026"
"56 Degrees Cafe","Bandung","Kafe","Alamat di Paskal Hyper Square menurut direktori","Sedang","(022) xxxx0668","","alamatpenting.com/daftar-alamat-cafe-di-bandung/","6 Okt 2026"
"13 Cups Coffee House","Bandung","Kafe","Coffee house di area ruko menurut direktori","Sedang","08xx-xxxx-1313","","alamatpenting.com/daftar-alamat-cafe-di-bandung/","6 Okt 2026"
"Abraham And Smith","Bandung","Kafe","Cafe & eatery di Bandung menurut direktori","Sedang","(022) xxxx3371","","alamatpenting.com/daftar-alamat-cafe-di-bandung/","6 Okt 2026"
"18 Hrs Cafe","Bandung","Kafe","Cafe di area Setiabudhi menurut direktori","Rendah","(022) xxx2600","","alamatpenting.com/daftar-alamat-cafe-di-bandung/","6 Okt 2026"
```

**Catatan kejujuran:** Semua 15 baris terverifikasi dari 3 halaman direktori (alamatpenting.com untuk kafe & katering, alamatelpon.com untuk toko kue/bakery) — nama, alamat, dan telepon sama persis seperti tercantum di sana; alamat lengkap ada di kolom sumber jika perlu dicek lagi. Beberapa toko kue yang ditemukan di direktori "sini.id" ternyata usaha manufaktur/pemasok bahan kue (bukan toko retail), jadi tidak dipakai agar tidak keliru jenisnya.

**Cara cek:** buka URL di kolom "Sumber" untuk verifikasi langsung sebelum menghubungi (data bisa berubah, info dicek 6 Okt 2026).

**Langkah lanjut:** hubungi satu-satu lewat telepon/WA bisnis yang tercantum, sebutkan dari mana Anda melihat kontaknya. Mau saya buatkan pesan pembuka WA lengkap untuk 3 prioritas di atas, atau prospeknya diperluas ke kota sekitar (Cimahi/KBB) juga?

## Output SESUDAH (skill 1.0.2), konteks Telegram — 5,0 menit, 0 prospek

Saya sudah coba cari langsung (Google Maps, Bing, DuckDuckGo, direktori kuliner/wedding seperti Pergikuliner, Weddingku, Bridestory, Zomato, Tripadvisor) tapi semuanya gagal diakses dari sini — mesin pencari diblokir/terbatas, halaman butuh JavaScript, dan browser tidak tersedia di environment ini. Jadi saya tidak bisa menjamin 15 nama usaha nyata dengan kontak terverifikasi tanpa mengarang, dan saya tidak akan menebak-nebak data itu.

Supaya tetap jalan cepat, ini saya siapkan paket pencarian siap pakai — Anda (atau saya lewat HP/laptop yang bisa buka Google Maps) tinggal tempel kata kuncinya, salin 10-30 nama+link yang muncul, lalu saya rapikan, skor kecocokan, dan buatkan CSV + pesan pembuka.

Profil ideal (asumsi): usaha F&B/katering di Bandung yang butuh kemasan ramah lingkungan — kafe dine-in/takeaway, katering rumahan-menengah (box/nasi kotak), toko kue/bakery dengan kemasan kue/roti. Fokus usaha yang kelihatan aktif (ada ulasan terbaru, situs/IG bisnis jalan) dan bervolume cukup (bukan usaha rumahan super kecil).

Kata kunci siap tempel di Google Maps (satu per kecamatan biar hasil lengkap, ganti [kecamatan]):
• kafe [kecamatan] Bandung
• katering [kecamatan] Bandung
• toko kue / bakery [kecamatan] Bandung
Kecamatan yang ramai usaha F&B: Coblong, Sukajadi, Cidadap, Bandung Wetan, Lengkong, Buahbatu, Cibeunying Kaler.

Kata kunci Google biasa:
• "kafe" Bandung "hubungi kami" OR kontak
• katering Bandung terpercaya acara kantor/pernikahan
• toko kue Bandung site:instagram.com (lihat IG bisnis mereka, bukan untuk login)
• daftar anggota APKRINDO/asosiasi restoran kafe Jawa Barat

Direktori yang relevan untuk tempel manual: Google Maps, Instagram bisnis (profil publik), Pergikuliner, Weddingku vendor katering, Kadin Jawa Barat (daftar anggota bila ada).

Kriteria saring cepat: usaha aktif (ulasan/posting ≤12 bulan), kemasan saat ini kelihatan masih konvensional/plastik (potensi upgrade), ada kontak bisnis publik (telepon/WA toko, bukan nomor pribadi pemilik), skala cukup (bukan 1 meja kecil).

Tabel kosong untuk Anda isi (nama usaha, kota/kecamatan, jenis, tautan Maps/situs, catatan singkat) — tempel balik ke saya dan saya lanjutkan jadi daftar 15 dengan skor + CSV:
1. 
2. 
3.

Pertanyaan saya (maks 3, biar lebih presisi saat Anda tempel hasilnya nanti):
1. Fokus ke kafe/katering/bakery yang mana paling prioritas, atau tiga-tiganya rata?
2. Target skala usaha: UMKM kecil-menengah, atau juga mau yang sudah punya banyak cabang?
3. Ada kecamatan/area Bandung tertentu yang paling dekat/strategis buat pengiriman dari tempat Anda?

## Catatan penguji (1.0.2)
- **Lokal: 8,5.** 5 halaman direktori, 15/15 nama + nomor cocok dengan halaman sumber, komposisi 5/5/5, CSV, prioritas, cara cek. Minus: sumber direktori 2019 tanpa peringatan usia data; 4 dari 5 toko kue dari 2 merek yang sama.
- **Telegram: 5.** Pesan dan waktu yang sama, tetapi agent tidak menemukan direktori teks yang bisa dibuka (9 direktori yang dicoba memblokir/butuh JavaScript) lalu beralih ke mode Rencana: **0 prospek**. Jujur, tetapi gagal memenuhi permintaan; SEBELUM (tanpa skill) memberi 15 baris. Pembeda lokal vs Telegram di sini kemungkinan karena pilihan direktori yang dicoba (acak), bukan karena kanal; tetap berarti hasil tidak andal.

Riwayat — 1.0.1: Telegram 8 (14,0 mnt), lokal 8,5 (11,3 mnt). 1.0.0: Telegram 8,5 (11,4 mnt), lokal 7,5 (2/3 timeout).
