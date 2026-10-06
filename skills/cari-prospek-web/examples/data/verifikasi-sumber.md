# Verifikasi independen: nama + kontak dicocokkan ke URL sumber (2026-10-06)

Penguji mengambil sendiri halaman sumber (curl lewat proxy lingkungan, teks HTML dibersihkan) lalu mencari nama usaha dan nomor/email persis seperti di jawaban agent. ✓ = nama dan kontak ada di halaman yang disebut; ◐ = nama/alamat ada, kontak memang ditulis `[belum terverifikasi]` oleh agent (jujur); ? = halaman tidak bisa dibuka penguji (429/403/502) sehingga tidak bisa dibuktikan atau dibantah; ✗ = tidak cocok/karangan.

## SESUDAH (dengan skill)

### Skenario 1, konteks Telegram (15 baris)
| No | Usaha | Kontak di jawaban | Halaman dicek | Hasil |
|---|---|---|---|---|
| 1 | Kartika Sari Pusat | (022) 4231355; order@kartikasari.com | kartikasari.com (telepon + alamat Jl. H. Akbar 4); alamatelpon.com/2019/05/daftar-90-toko-roti... (email) | ✓ (catatan: email hanya ada di direktori, kolom `sumber` CSV hanya menyebut kartikasari.com) |
| 2 | Kopi Toko Djawa | "WA via situs, nomor belum terverifikasi" | kopitokodjawa.com/link/ (tombol WA 628996979748 ada) | ◐ (terlalu hati-hati; nomor sebenarnya ada) |
| 3 | Kenangan Pasar Catering | WA 0882000836989 | instagram.com/kenangan_pasar (429 untuk penguji) | ? |
| 4 | The Harvest Cakes Buah Batu | (022) 7302330 | alamatelpon.com (ada); harvestbakes.co.id ("Corporate Services" ada) | ✓ |
| 5 | Garmelia Bakery | (022) 7514188 | garmeliabakery.com/contact | ✓ |
| 6 | Bisou Patisserie Hegarmanah | 0819 3143 7475 / (022) 203 2213 | shop.bisou.co.id | ✓ |
| 7 | Amanda Brownies Pusat | (022) 7514657 | alamatelpon.com | ✓ |
| 8 | Holland Bakery Buah Batu | (022) 7304499; WA 0818-0691-8181 | alamatelpon.com; hollandbakery.co.id (WA resmi + peringatan nomor palsu) | ✓ |
| 9 | Mayasari Kebon Kawung | (022) 4222444 | alamatelpon.com | ✓ |
| 10 | Cizz Cheesecake & Friends | (022) 7230969 | alamatelpon.com | ✓ |
| 11 | Vitasari Surapati | (022) 2531200 | alamatelpon.com | ✓ |
| 12 | Buttercup Boulangerie | (022) 4203124 | alamatelpon.com | ✓ |
| 13 | Vannisa Brownies | (022) 7537754 | alamatelpon.com | ✓ |
| 14 | Sudut Pandang | `[belum terverifikasi]` | blog.cove.id (alamat Jl. Pagermaneuh ada) | ◐ |
| 15 | Mercusuar Cafe & Resto | `[belum terverifikasi]` | blog.cove.id (alamat Lembah Pakar Timur 2 No.7 ada) | ◐ |

Hasil: 11 ✓, 3 ◐, 1 ?, 0 ✗.

### Skenario 2 (18 baris)
lokanesia.com/klinik-pratama-di-surabaya: Mitra Sehat 7524408, Medico Sier 8434056, Optima 8720733, Jemursari Empat 8418414, Prameswari 5029118, Kebangkitan 71258886, Anugerah Karya Medika 102 78071401, Nayaka Husada 03 5343154 → 8 ✓.
alamatsehat.com/klinik-24-jam-di-surabaya: BRI Medika 8472120, Pusura Sungkono 5612120, Klinik Utama Rawat Inap Kartika 5042395, Klinik Medis Pusura 5317334 → 4 ✓.
qdermaclinicsby.com/contact: 0812 95485757 → ✓.
surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya: Apotek & Laboratorium Klinik 2 Oscar 5033067, AHA Medica 5032819, Adam Farma 8439919, Asri Farma 031 592 3908 → 4 ✓.
Klinik Waluyo Jati: alamat Jl. Ambengan 68 ✓ di klinikwaluyojati.com; nomor 5026014 dari semuabis.com (403 untuk penguji) → ?.
Hasil: 17 ✓, 1 ?, 0 ✗.

### Skenario 4 (15 baris)
phriyogyakarta.com/jogja/: Bhinneka 513353, Prime Cailendra 373761, Duta Guest House 372177, Delta Home Stay 372064, Kirana 372262, Musafira "377 669", Ruba Grha 373531, Grha Somaya 377555, Sumaryo 087737682689, Sagan 0274-549963 → 10 ✓ (agent menambahkan kode area 0274 pada nomor yang di sumber tanpa kode area).
lokanesia.com/tempat-kost-dekat-ugm-jogja & kost-putri-dekat-uny-jogja: DHost 0812-2604-0899, Kost Eksklusif GA 0812-2780-040 (memang tertulis 11 digit di sumber), Bulaksumur 0852-9392-9275, Amarta 0878-7676-4164, Larasati 0822 51091234 → 5 ✓ (catatan: nomor HP pemilik kos perorangan; menurut aturan skill seharusnya ditandai ragu bisnis/pribadi).
Hasil: 15 ✓, 0 ✗.

**Total SESUDAH: 48 baris → 43 ✓ kontak cocok persis dengan URL yang disebut, 3 ◐ ditandai jujur, 2 ? tidak bisa dibuka penguji, 0 karangan. 48/48 baris punya URL sumber + tanggal cek.**


### Skenario 1, lokal (percobaan ke-3; dua percobaan sebelumnya timeout 15 menit) — 14 baris
mgcatering.id/contact: 0856-0368-9788 / 0821-1611-1550 ✓. deabakery.co.id: 0811-2345-4567 ✓ (tertulis "Customer Care" di situs). vitasari.id/cabang: +62 812-2343-3963 ✓. dinastycatering.com/kontak-kami: (022) 7563971 + Info@dinastycatering.com ✓. bandungcatering.com/hubungi-kami: 022 6372 6529 / 0811 2202 112 ✓. harvestbakes.co.id: 1500581 / +62 812 1314 1500 ✓ → 6 ✓.
Mayasari (429), Prima Rasa (koneksi diputus), Green Cafe idalamat.com (403) → 3 ?.
Accio Coffee, Karim Katering, Calyandra House, Ny Liem → 4 ◐ (ditandai jujur).
**ManA Social Cafe → ✗ (cacat):** halaman mana-social-cafe.com/contact.html memang memuat "+62 22 7654 3210 / +62 812 3456 7890" dan "Jl. Buah Batu No. 123", tetapi itu jelas data contoh/placeholder (deret angka berurutan, nomor rumah 123). Agent menyalinnya sebagai kontak terverifikasi dan memberi skor Sedang. Agent yang sama justru membuang "Moro Catering" karena email info@domain.com, jadi pengecekan data dummy belum konsisten.

**Total SESUDAH diperbarui (62 baris dari 4 jawaban): 49 ✓ cocok persis dengan URL yang disebut, 7 ◐ ditandai `[belum terverifikasi]` dengan jujur, 5 ? tidak bisa dibuka penguji, 1 ✗ kontak placeholder disajikan sebagai fakta, 0 usaha/kontak dikarang agent. 62/62 baris punya URL sumber + tanggal cek.**

## SEBELUM (tanpa skill)

### Skenario 1, konteks Telegram (15 baris, sumber hanya disebut umum di kalimat pembuka: alamatpenting.com, caribisnis.id, alamatelpon.com)
alamatpenting.com/daftar-alamat-cafe-di-bandung: Blackbone 4230352, Bober 7234295, Armor Kopi 0812-1396-0941, Caffetto 0838-2127-8606, Chatime 4222770, Cat's Village 0838-2940-4564 → 6 ✓.
alamatpenting.com/daftar-alamat-catering-di-bandung: Ayudha 022-92910999 & 089666136999, Resep Bunda 7236848, Camelya 7500862 → 3 ✓.
alamatelpon.com: Amanda 7514657, Kartika Sari Djuanda 2509500, Holland Buah Batu 7304499 → 3 ✓. Vitasari & Mayasari hanya situs (situs aktif) → 2 ✓ (tanpa kontak).
Destiny Catering (022) 5222500 / WA 0821-1970-2019: tidak ditemukan di halaman yang dibuka agent yang bisa diambil penguji (pergimulu.com 403) → ?.
Hasil: 14 ✓, 1 ?, 0 ✗ — **tetapi 0/15 baris mencantumkan URL sumber per baris**; pembeli tidak bisa memeriksa sendiri.

### Skenario 1, lokal (cuplikan 4 baris dicek)
Hutanika WA +62 822-8288-8859 → ✓ (wa.me di hutanika.com). Bisou: 0895 3375 38362 & 0858 8536 5142 ✓, tetapi nomor ketiga ditulis "0816-1118-xxxx" padahal di situs lengkap "0816 1118 200" (nomor terpotong). Nara Park 0813-8888-1532 → tidak ada di narapark-bandung.com (alamat ada) → ?. Destiny → ?. Juga ada baris pengisi "BDGCafe network (referensi komunitas)" yang bukan prospek.

### Skenario 2 (14 baris, sumber umum: OSM, alamatsehat, semuabis, lokanesia, lewatmana)
Wisma Husada (031) 5150 0111 → ✓ di alamatsehat.com. 13 baris lain tidak bisa diuji penguji: tanpa URL per baris, sebagian dari OpenStreetMap/Overpass yang tidak bisa diakses dari lingkungan penguji (koneksi diputus). → 1 ✓, 13 ?.

**Total SEBELUM: 44 baris → 17 ✓ cocok (semua tanpa URL per baris), 1 nomor terpotong "xxxx", 1 baris pengisi bukan prospek, sisanya tidak bisa dibuktikan; 0/44 baris punya URL sumber per baris.**
