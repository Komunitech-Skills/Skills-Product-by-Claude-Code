# Verifikasi independen: nama + kontak dicocokkan ke URL sumber (2026-10-06)

*Nama usaha dari direktori publik; nomor telepon/WA dan email disamarkan dalam berkas ini (sisa 4 digit terakhir), nama perorangan tidak dicantumkan.*

Penguji mengambil sendiri halaman sumber (curl lewat proxy lingkungan, teks HTML dibersihkan) lalu mencari nama usaha dan nomor/email persis seperti di jawaban agent. ✓ = nama dan kontak ada di halaman yang disebut; ◐ = nama/alamat ada, kontak memang ditulis `[belum terverifikasi]` oleh agent (jujur); ? = halaman tidak bisa dibuka penguji (429/403/502) sehingga tidak bisa dibuktikan atau dibantah; ✗ = tidak cocok/karangan.

## SESUDAH (dengan skill)

### Skenario 1, konteks Telegram (15 baris)
| No | Usaha | Kontak di jawaban | Halaman dicek | Hasil |
|---|---|---|---|---|
| 1 | Kartika Sari Pusat | (022) xxx1355; order@… | kartikasari.com (telepon + alamat Jl. H. Akbar 4); alamatelpon.com/2019/05/daftar-90-toko-roti... (email) | ✓ (catatan: email hanya ada di direktori, kolom `sumber` CSV hanya menyebut kartikasari.com) |
| 2 | Kopi Toko Djawa | "WA via situs, nomor belum terverifikasi" | kopitokodjawa.com/link/ (tombol WA 628xxxxx9748 ada) | ◐ (terlalu hati-hati; nomor sebenarnya ada) |
| 3 | Kenangan Pasar Catering | WA 08xxxxxxx6989 | instagram.com/kenangan_pasar (429 untuk penguji) | ? |
| 4 | The Harvest Cakes Buah Batu | (022) xxx2330 | alamatelpon.com (ada); harvestbakes.co.id ("Corporate Services" ada) | ✓ |
| 5 | Garmelia Bakery | (022) xxx4188 | garmeliabakery.com/contact | ✓ |
| 6 | Bisou Patisserie Hegarmanah | 08xx xxxx 7475 / (022) xxx 2213 | shop.bisou.co.id | ✓ |
| 7 | Amanda Brownies Pusat | (022) xxx4657 | alamatelpon.com | ✓ |
| 8 | Holland Bakery Buah Batu | (022) xxx4499; WA 08xx-xxxx-8181 | alamatelpon.com; hollandbakery.co.id (WA resmi + peringatan nomor palsu) | ✓ |
| 9 | Mayasari Kebon Kawung | (022) xxx2444 | alamatelpon.com | ✓ |
| 10 | Cizz Cheesecake & Friends | (022) xxx0969 | alamatelpon.com | ✓ |
| 11 | Vitasari Surapati | (022) xxx1200 | alamatelpon.com | ✓ |
| 12 | Buttercup Boulangerie | (022) xxx3124 | alamatelpon.com | ✓ |
| 13 | Vannisa Brownies | (022) xxx7754 | alamatelpon.com | ✓ |
| 14 | Sudut Pandang | `[belum terverifikasi]` | blog.cove.id (alamat Jl. Pagermaneuh ada) | ◐ |
| 15 | Mercusuar Cafe & Resto | `[belum terverifikasi]` | blog.cove.id (alamat Lembah Pakar Timur 2 No.7 ada) | ◐ |

Hasil: 11 ✓, 3 ◐, 1 ?, 0 ✗.

### Skenario 2 (18 baris)
lokanesia.com/klinik-pratama-di-surabaya: Mitra Sehat xxx4408, Medico Sier xxx4056, Optima xxx0733, Jemursari Empat xxx8414, Prameswari xxx9118, Kebangkitan xxxx8886, Anugerah Karya Medika 102 xxxx1401, Nayaka Husada 03 xxx3154 → 8 ✓.
alamatsehat.com/klinik-24-jam-di-surabaya: BRI Medika xxx2120, Pusura Sungkono xxx2120, Klinik Utama Rawat Inap Kartika xxx2395, Klinik Medis Pusura xxx7334 → 4 ✓.
qdermaclinicsby.com/contact: 08xx xxxx5757 → ✓.
surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya: Apotek & Laboratorium Klinik 2 Oscar xxx3067, AHA Medica xxx2819, Adam Farma xxx9919, Asri Farma 031 xxx 3908 → 4 ✓.
Klinik Waluyo Jati: alamat Jl. Ambengan 68 ✓ di klinikwaluyojati.com; nomor xxx6014 dari semuabis.com (403 untuk penguji) → ?.
Hasil: 17 ✓, 1 ?, 0 ✗.

### Skenario 4 (15 baris)
phriyogyakarta.com/jogja/: Bhinneka xx3353, Prime Cailendra xx3761, Duta Guest House xx2177, Delta Home Stay xx2064, Kirana xx2262, Musafira "xx7 669", Ruba Grha xx3531, Grha Somaya xx7555, Sumaryo 08xxxxxx2689, Sagan 0274-xx9963 → 10 ✓ (agent menambahkan kode area 0274 pada nomor yang di sumber tanpa kode area).
lokanesia.com/tempat-kost-dekat-ugm-jogja & kost-putri-dekat-uny-jogja: DHost 08xx-xxxx-0899, Kost Eksklusif GA 08xx-xxx0-040 (memang tertulis 11 digit di sumber), Bulaksumur 08xx-xxxx-9275, Amarta 08xx-xxxx-4164, Larasati 08xx xxxx1234 → 5 ✓ (catatan: nomor HP pemilik kos perorangan; menurut aturan skill seharusnya ditandai ragu bisnis/pribadi).
Hasil: 15 ✓, 0 ✗.

**Total SESUDAH: 48 baris → 43 ✓ kontak cocok persis dengan URL yang disebut, 3 ◐ ditandai jujur, 2 ? tidak bisa dibuka penguji, 0 karangan. 48/48 baris punya URL sumber + tanggal cek.**


### Skenario 1, lokal (percobaan ke-3; dua percobaan sebelumnya timeout 15 menit) — 14 baris
mgcatering.id/contact: 08xx-xxxx-9788 / 08xx-xxxx-1550 ✓. deabakery.co.id: 08xx-xxxx-4567 ✓ (tertulis "Customer Care" di situs). vitasari.id/cabang: +62 8xx-xxxx-3963 ✓. dinastycatering.com/kontak-kami: (022) xxx3971 + info@… ✓. bandungcatering.com/hubungi-kami: 022 xxxx 6529 / 08xx xxx2 112 ✓. harvestbakes.co.id: xxx0581 / +62 8xx xxxx 1500 ✓ → 6 ✓.
Mayasari (429), Prima Rasa (koneksi diputus), Green Cafe idalamat.com (403) → 3 ?.
Accio Coffee, Karim Katering, Calyandra House, Ny Liem → 4 ◐ (ditandai jujur).
**ManA Social Cafe → ✗ (cacat):** halaman mana-social-cafe.com/contact.html memang memuat "+62 22 7654 3210 / +62 812 3456 7890" dan "Jl. Buah Batu No. 123", tetapi itu jelas data contoh/placeholder (deret angka berurutan, nomor rumah 123). Agent menyalinnya sebagai kontak terverifikasi dan memberi skor Sedang. Agent yang sama justru membuang "Moro Catering" karena email info@domain.com, jadi pengecekan data dummy belum konsisten.

**Total SESUDAH diperbarui (62 baris dari 4 jawaban): 49 ✓ cocok persis dengan URL yang disebut, 7 ◐ ditandai `[belum terverifikasi]` dengan jujur, 5 ? tidak bisa dibuka penguji, 1 ✗ kontak placeholder disajikan sebagai fakta, 0 usaha/kontak dikarang agent. 62/62 baris punya URL sumber + tanggal cek.**

## SEBELUM (tanpa skill)

### Skenario 1, konteks Telegram (15 baris, sumber hanya disebut umum di kalimat pembuka: alamatpenting.com, caribisnis.id, alamatelpon.com)
alamatpenting.com/daftar-alamat-cafe-di-bandung: Blackbone xxx0352, Bober xxx4295, Armor Kopi 08xx-xxxx-0941, Caffetto 08xx-xxxx-8606, Chatime xxx2770, Cat's Village 08xx-xxxx-4564 → 6 ✓.
alamatpenting.com/daftar-alamat-catering-di-bandung: Ayudha 022-xxxx0999 & 08xxxxxx6999, Resep Bunda xxx6848, Camelya xxx0862 → 3 ✓.
alamatelpon.com: Amanda xxx4657, Kartika Sari Djuanda xxx9500, Holland Buah Batu xxx4499 → 3 ✓. Vitasari & Mayasari hanya situs (situs aktif) → 2 ✓ (tanpa kontak).
Destiny Catering (022) xxx2500 / WA 08xx-xxxx-2019: tidak ditemukan di halaman yang dibuka agent yang bisa diambil penguji (pergimulu.com 403) → ?.
Hasil: 14 ✓, 1 ?, 0 ✗ — **tetapi 0/15 baris mencantumkan URL sumber per baris**; pembeli tidak bisa memeriksa sendiri.

### Skenario 1, lokal (cuplikan 4 baris dicek)
Hutanika WA +62 8xx-xxxx-8859 → ✓ (wa.me di hutanika.com). Bisou: 08xx xxxx x8362 & 08xx xxxx 5142 ✓, tetapi nomor ketiga ditulis "08xx-xxxx-xxxx" padahal di situs lengkap "08xx xxx8 200" (nomor terpotong). Nara Park 08xx-xxxx-1532 → tidak ada di narapark-bandung.com (alamat ada) → ?. Destiny → ?. Juga ada baris pengisi "BDGCafe network (referensi komunitas)" yang bukan prospek.

### Skenario 2 (14 baris, sumber umum: OSM, alamatsehat, semuabis, lokanesia, lewatmana)
Wisma Husada (031) xxxx 0111 → ✓ di alamatsehat.com. 13 baris lain tidak bisa diuji penguji: tanpa URL per baris, sebagian dari OpenStreetMap/Overpass yang tidak bisa diakses dari lingkungan penguji (koneksi diputus). → 1 ✓, 13 ?.

**Total SEBELUM: 44 baris → 17 ✓ cocok (semua tanpa URL per baris), 1 nomor terpotong "xxxx", 1 baris pengisi bukan prospek, sisanya tidak bisa dibuktikan; 0/44 baris punya URL sumber per baris.**

---

# Uji ulang 1.0.1 (2026-10-06, penguji independen baru)

Cara: penguji mengambil sendiri **setiap** URL sumber dari jawaban SESUDAH 1.0.1 (curl lewat proxy lingkungan, HTML dibersihkan, angka dinormalisasi) lalu mencari nama usaha dan setiap nomor/email persis. Juga dicari pola placeholder (deret 1234/3456 7890/7654 3210, "No. 123", `@domain.com`, `08xx`).

### S1 Telegram (16 baris)
✓ toomboo.id/contact (+62 8xx-xxxx-0029; hello@… ada di HTML, dilindungi Cloudflare) · jardins-cafe.com (022) xxx-7711 · bandungcatering.com/hubungi-kami 022 xxxx 6529 & 08xx xxx2 112 · dinastycatering.com/kontak-kami (022) xxx3971 & info@… · legendacatering.com 08xx-xx2-724 · heni-catering.id 022-xxxx-3732 · makanponyo.com 08xx-xxxx-5000 & [email disamarkan] · vitasari.id/cabang Kurdi +62 8xx-xxxx-3963 · mayasaribakery.com/pages/kontak-lokasi-toko 08xx-xxxx-8114 · shop.bisou.co.id 08xx xxxx 7475 & 022 xxx 2213 · delierasakue.com/kontak-delie-rasa 08xx-xxxx-3818 · arnonbakery.com +62 8xx-xxx5-999 · primarasabakery.co.id/kontak (022) xxx6468 → **13 ✓**.
◐ Heritage Resto & Cafe, Sarasa Catering (nama & alamat ada di sites.google.com; nomor memang tidak tertulis) → **2 ◐ jujur**.
? Cafe Halaman (instagram.com 429) → **1 ?**. Placeholder: 0 (ManA dibuang dengan alasan).

### S1 lokal (15 baris)
✓ legendacatering.com, mgcatering.id 08xx-xxxx-9788, asparaguscatering.com 08xx-xxxx-0688, dinastycatering.com, bandungcatering.com, maqueen-catering.com +62 8xx-xxx7-181, heni-catering.id, mayasaribakery.com (022) xxx3999 Bojong, delierasakue.com, hollandbakery.co.id 08xx-xxxx-8181, wheelscoffeeroasters.com/contact 08xx-xxxx-9727, kurokoffee.co/contact hello@…, mana-social-cafe.com/contact.html (IG manasocialcafe ada; nomor 3456 7890 memang placeholder di situs → agent benar menolaknya), toomboo.id/location (IG t.o.o.m.b.o.o), kopiaroma.id ("agen" ada) → **15/15 cocok**. Catatan: Toomboo ditulis "nomor belum terverifikasi" padahal /contact memuat nomornya (terlalu hati-hati).

### S2 (13 baris)
✓ alamatsehat.com: Apotek Restu (031) xxx3848, K-24 Jemursari xxx3891, K-24 Demak xxx2620, K-24 Wiyung xxx1131 · lokanesia: Pelita Jaya (031) xxx4632 · klinikoptima.id/kontak xxx0733/8720744, [email disamarkan], xxx1203 (2 baris) · qdermaclinicsby.com/contact 08xx xxxx5757 · m2cdental.net +62 8xx-xxxx-9191 · denthausdental.com/kontak +62 8xx-xxxx-1920 & email → **10 ✓**.
◐ OMDC (Dharmahusada ada), FDC (Mayjen ada), telepon ditulis belum terverifikasi → **2 ◐**.
**Sebagian/salah atribusi:** K-24 Mulyosari — (031) xxx1059 ✓, tetapi **08xx-xxxx-2362 tidak ada di alamatsehat.com** (halaman memuat 08xx-xxx-2424 layanan pelanggan); riwayat sesi agent menunjukkan nomor itu dari cuplikan hasil pencarian mulyosari.com yang tidak dibuka.

### S4 (14 baris)
✓ yogyes.com: Hotel Nugraha 08xx-xx3-143 (kapasitas 300 ada), Nine Hotel 08xx-xx8-074, Omah Andini 08xx-xxxx-2103, Griya Sari 08xx-xxxx-8233, Banbili 08xx-xxxx-3252, Ayra 08xx-xxx0-479 · simplyhomy.com/contact-us 08xx-xxxx-7080 & 08xx-xxxx-7337 · hotel-yogyakarta.blogspot.com: OGH Dhoni xx0833, Tribrata xx9147, Duta Wisata 1 xx2380, Duta Wisata 2 xx7364, SALA xx5380 → **12 ✓**.
◐ Hallstatt (rating 4.9 ada), Cemara Residence → **2 ◐ jujur**.

**Total SESUDAH 1.0.1: 58 baris → 50 ✓ penuh, 6 ◐ jujur, 1 salah atribusi sumber (nomor nyata dari cuplikan pencarian), 1 tidak bisa dibuka; 0 karangan, 0 placeholder disajikan sebagai fakta; 58/58 punya URL sumber + tanggal cek.**

# Uji ulang 1.0.2 (2026-10-06, penguji independen ketiga)

Metode: penguji mengambil sendiri setiap URL sumber (curl lewat proxy lingkungan), membersihkan HTML, lalu memeriksa nama usaha dan 8 digit akhir nomor ada di halaman **dan berjarak < 500 karakter** (pasangan nama-nomor benar, bukan sekadar ada di halaman). Semua baris diperiksa.

### S1 Telegram — 0 baris (mode Rencana, tidak ada yang diverifikasi)

### S1 lokal — 15 baris, 15 ✓
| Halaman | Baris | Hasil (jarak nama-nomor) |
|---|---|---|
| alamatelpon.com/2019/05/daftar-90-toko-roti-cake-shop-di-bandung.html | Kartika Sari Pusat (022) xxx1355 + order@…; Amanda Pusat xxx4657; Amanda Juanda xxx6123; Holland Buah Batu xxx4499; Kartika Sari Djuanda xxx9500 | 5 ✓ (14–95 karakter; "9 outlet" juga tertulis) |
| alamatpenting.com/daftar-alamat-catering-di-bandung/ | Cita Rasa xxx0781 (Taman Holis ✓); Citra Boga xxx1921; Adinda xxx1884; Asparagus xxx3730; Bey Catering xxx0039 + 08xx-xxxx1490 | 5 ✓ (8–152) |
| alamatpenting.com/daftar-alamat-cafe-di-bandung/ | Armor Kopi 08xx-xxxx-0941; 56 Degrees xxxx0668; 13 Cups 08xx-xxxx-1313; Abraham And Smith xxxx3371; 18 Hrs xxx2600 | 5 ✓ (20–22) |

Catatan: kedua direktori berupa artikel lama (alamatelpon bertanggal 2019); data cocok dengan halaman, tetapi kemutakhiran nomor tidak dijamin.

### S2 — 15 baris, 15 ✓
| Halaman | Baris | Hasil |
|---|---|---|
| lokanesia.com/klinik-pratama-di-surabaya/ | Medico Sier xxx4056 (halaman menulis "(031) xxxxxx4056", agent merapikan; "24 Jam" ✓), Mitra Sehat xxx4408, Optima xxx0733, Prameswari xxx9118 | 4 ✓ |
| lokanesia.com/klinik-pratama-di-surabaya/3/ | Mitra Medicare xxx8780 (09.00–21.00 ✓), Kencana Medika xxx4791, Tabita xxx0088 | 3 ✓ |
| surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya/ | 2 Oscar xxx3067, Amira xxx3313, AN Jaya 08xx-xxxx-9486, Adam Farma xxx9919, AHA Medica xxx2819, Asri Farma xxx3908, Andrea xxx3370, Anita Farma xxx8357 | 8 ✓ (AN Jaya: halaman menulis "No. Telepon", label "WA bisnis" tambahan agent) |

### S4 — 12 baris, 11 ✓, 1 tak terbukti
| Halaman | Baris | Hasil |
|---|---|---|
| lokanesia.com/tempat-kost-dekat-ugm-jogja/ | 9 kos (UGM Residence 08xx-xxxx-9275, D'Paragon Pogung B 08xx-xxxx-8000, Kost GA 08xx-xxx0-040, DHost 08xx-xxxx-0899, Kost Citra Jogja 08xx-xxxx-8788, Sendowo B44 08xx-xxxx-5990, kos kosan sendowo 08xx-xxxx-8515, Kos Merah Putih 08xx-xxxx-9633, Griya Afa 08xx-xxxx-1977) | 9 ✓ cocok, **tetapi semuanya nomor HP perorangan pemilik/pengelola kos dari listing** → seharusnya tidak masuk tabel/CSV menurut SKILL.md |
| jogja.pandanaranhotel.com/contact | Pandanaran Prawirotaman (0274) xxx0077, reservation@… | ✓ (agent **tidak membuka** halaman ini; kontak dari cuplikan pencarian) |
| galleryprawirotamanhotel.com/location | Gallery Prawirotaman (0274) xxx0008, info@… | ✓ (sama: dari cuplikan) |
| exploreyogya.com/hotel-melati | Hotel Mawar Saron (0274) xx4083 | **✗ tak terbukti**: domain kini parkir (redirect /lander), agent gagal membukanya; nomor hanya dari cuplikan DuckDuckGo yang teksnya tampak tulisan otomatis |

**Total 1.0.2:** 42 baris → 41 nama+kontak cocok dengan halaman, 1 tak terbukti, 0 placeholder, 0 karangan terbukti; 3 kontak dari cuplikan pencarian; 9 HP perorangan masuk tabel.
