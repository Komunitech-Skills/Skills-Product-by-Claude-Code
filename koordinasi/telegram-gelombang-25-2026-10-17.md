# Gelombang Telegram 25 — 2026-10-17 (bot kedua)

Keputusan otomatis **104/108** (2026-10-17). Bot uji kedua `@KTclaude2bot` (OpenClaw 2026.10.2, model router Komunitech), grup uji internal Komunitech, topik baru 1993–1998. Pesan uji identik di sisi TANPA (topik `skills: []`) dan DENGAN skill; dikirim berurutan oleh bot penguji (rantai otomatis dua jalur, keputusan 93). Penilaian: satu penilai independen per skill + pemeriksa kedua yang berusaha membantah (angka dihitung ulang, kutipan dicocokkan ke id pesan); koreksi pemeriksa sudah diterapkan di tabel.

## Skor & verdik

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| promo-kalender (1.0.4) | 6,7 | 8 | +1,3 | **BELUM** (selisih < 1,5) | Dengan skill, bot menghitung batas diskon aman (maks. 46%) dan membandingkan diskon 30% dengan diskon 20% serta paket 2 botol, lengkap dengan labanya. Bot juga memberi target 6 botol untuk menyamai laba hari biasa, linimasa bertanggal, dan S&K siap tempel. Tanpa skill, bot membandingkan promo sehari dengan laba sebulan penuh, lalu menyuruh menjual ±170 botol dan menyetok 150–200 botol. |
| riset-harga-kompetitor (1.0.5) | 5 | 8 | +3 | **LOLOS** | Hanya dengan skill, bot menyebut terang baris pesaing dobel yang dibuang, lalu menghitung harga tengah pasar Rp53.125, harga balik modal Rp35.715, harga minimum dengan untung 20% dari harga jual (Rp46.297), dan harga cantik Rp52.900 beserta untungnya (Rp15.038), semuanya cocok saat dihitung ulang. Tanpa skill, bot tidak menghitung harga tengah pasar maupun harga balik modal, dan salah menghitung persen untung di harga Rp52.000–54.000. |
| pantau-pasar-kripto (1.0.11) | 4 | 5 | +1 | **BELUM** (DENGAN < 8) | Dengan skill, bot memakai aturan pajak kripto yang berlaku sekarang (0,21% di Indodax, 1% di Binance), sehingga pajak Rp420.786 dan untung bersih Rp562.124 benar. Tanpa skill, bot memakai tarif lama sehingga pajaknya terhitung terlalu kecil (Rp115.860). Namun rincian per transaksi di sisi dengan skill mengurangkan biaya bursa dua kali, sehingga baris-barisnya tidak cocok bila dihitung ulang. |

Pembanding uji internal (skor promosi / `examples/`):
- promo-kalender: 6,5 → 8,5 (1.0.3).
- riset-harga-kompetitor: 5,0 → 8,0 (1.0.5).
- pantau-pasar-kripto: 5,3 → 8,6 (1.0.10).

Beda terhadap uji internal:
- **promo-kalender:** Di bot asli, DENGAN mendapat 8,0 (uji internal 8,5). Angkanya tetap benar semua dan opsi 25% Rp66.800 dari pra-cek tidak muncul. Namun pembuka menyebut nama skill, total kampanye memakai asumsi 60 botol sehari, dan ada dua kalimat berlebihan ('hampir 2x lipat', '6 botol … sisanya laba bersih'). TANPA sama dengan uji internal (6,5): hitungan per botol benar, tetapi target 170-an botol membandingkan promo sehari dengan laba sebulan.
- **riset-harga-kompetitor:** Hasilnya sejalan dengan uji internal: semua angka sisi DENGAN cocok, dan sisi TANPA lagi-lagi salah menghitung persen untung, tetapi kali ini tidak menyarankan harga coret fiktif. Di bot asli, sisi DENGAN tidak mengulang kesalahan '9–18% di atas median' dari pra-cek. Namun saran harga coretnya masih tanpa syarat harga coret jujur, dan P25/P75 tidak dijelaskan dengan bahasa awam, padahal versi uji internal menjelaskannya.
- **pantau-pasar-kripto:** Uji internal (1.0.10) dan pra-cek konteks Telegram 17 Okt (1.0.11) tidak menemukan salah angka. Di bot asli, angka akhirnya sama persis (Rp982.910, Rp420.786, Rp562.124), tetapi bot menambahkan rincian 'proceeds − modal − fee' yang mengurangkan fee dua kali. Sisi tanpa skill di bot asli lebih lemah daripada uji internal: kali ini pencarian web mati, sehingga bot memakai tarif pajak lama, bukan aturan PMK 50/2025.

Catatan jujur (untuk pembeli):
- **promo-kalender:** Bot menyebut laba diskon 20% 'hampir 2x lipat' dibanding diskon 30%, padahal hanya sekitar 1,6 kali. Kalimat '6 botol … sisanya laba bersih' maksudnya laba promo sudah menyamai hari biasa, karena setiap botol promo tetap untung Rp12.574. Total kampanye juga dihitung dengan asumsi 60 botol laku dalam sehari; bot menandainya optimis dan menawarkan hitung ulang.
- **riset-harga-kompetitor:** Istilah P25/P75 tidak dijelaskan, dan jawaban tidak menyebut bahwa target untung 20% dihitung dari harga jual. Saran memasang harga coret juga tidak disertai pengingat bahwa harga coret harus harga yang benar-benar pernah dipakai.
- **pantau-pasar-kripto:** Total untung, sisa koin, dan pajaknya benar, tetapi rincian per transaksi menuliskan biaya bursa dikurangkan dua kali, sehingga baris itu tidak cocok bila Anda hitung ulang dengan kalkulator. Balasan juga masih memakai istilah Inggris seperti 'proceeds', dan belum mengingatkan bahwa pajak 1% atas penjualan di Binance wajib Anda setor sendiri bila bursa itu tidak memungutnya.

Salah angka/fakta yang ditemukan:
- promo-kalender: tidak ada
- riset-harga-kompetitor: TANPA: untuk harga Rp52.000–54.000 ditulis margin '~29-30% dari harga jual, ~50%+ dari modal'; yang benar 27,4–29,6% dari harga jual dan 47,5–53,3% dari modal (di Rp52.000: laba Rp14.250 = 27,4% dari harga jual = 47,5% dari modal)
- pantau-pasar-kripto: TANPA: pajak dihitung dengan tarif lama PMK 68/2022 (0,1% Indodax / 0,2% Binance) untuk penjualan Agustus–September 2026. Aturan yang berlaku adalah PMK 50/2025 (sejak 1 Agustus 2025): 0,21% di PAKD dalam negeri dan 1% di bursa luar negeri. Akibatnya PPh ditulis Rp115.860 padahal seharusnya Rp420.786, dan 'laba bersih setelah pajak Rp686.510' seharusnya Rp562.124 (bila PPh belum dipotong).; TANPA: 'modal rata-rata tersisa Rp4.663.950' (BTC), Rp17.572.560 (ETH), dan Rp47.391.750 (SOL) sebenarnya adalah TOTAL modal sisa, bukan rata-rata. Rata-rata per koin dengan metode rata-rata tertimbang: BTC Rp1.554.650.000, ETH Rp58.575.200, SOL Rp3.159.450.; DENGAN: keempat baris rincian ditulis 'proceeds − modal − fee = hasil', padahal proceeds sudah dikurangi fee (17.050.000 − 51.150 = 16.998.850), jadi fee terhitung dua kali dan persamaannya tidak cocok. BTC 5 Agu: 16.998.850 − 15.245.600 − 51.150 = 1.702.100 (ditulis 1.753.250). ETH: 30.508.200 − 29.287.600 − 91.800 = 1.128.800 (ditulis 1.220.600). SOL: 28.813.300 − 31.594.500 − 86.700 = −2.867.900 (ditulis −2.781.200). BTC 25 Sep: 8.683.870 − 7.893.610 − 26.130 = 764.130 (ditulis 790.260). Hasil akhir tiap baris, total, sisa, dan PPh sendiri benar.; TANPA: pajak dihitung dengan tarif lama PMK 68/2022 (0,1% Indodax / 0,2% Binance) untuk penjualan Agustus–September 2026. Aturan yang berlaku adalah PMK 50/2025 (sejak 1 Agustus 2025): 0,21% di PAKD dalam negeri dan 1% di bursa luar negeri. Akibatnya PPh ditulis Rp115.860 padahal seharusnya Rp420.786, dan 'laba bersih setelah pajak Rp686.510' seharusnya Rp381.584 menurut metode rata-rata tertimbang yang dipakai bot (802.370 − 420.786), atau Rp562.124 bila memakai FIFO (keduanya bila PPh belum dipotong).

Pemeriksa kedua:
- **promo-kalender:** koreksi — Kutipan ada kata per kata di msg 2001 (topik 1993) dan msg 2004 (topik 1994), keduanya dari KTclaude2bot. Log gateway: msg 2004 terkirim satu potong, ±3 menit. Hitung ulang dengan Decimal, semua angka cocok: 62.300/12.574 (20,2%), 71.200/20.406 (28,7%), paket 129.000 → 15.135 (23,5%; hemat 27,5% → 27%), diskon maks 46,05%, total 754.440/1.224.360/908.100, 6 botol (75.444 ≥ 72.140), 11 Nov hari Rab
- **riset-harga-kompetitor:** koreksi — Pesan 2006 (topik 1995) dan 2009 (topik 1996) dari KTclaude2bot ada, dan kutipannya persis sama. Hitung ulang dengan Decimal cocok semua: P25 49.375, median 53.125, P75 54.825, laba 19.500 (33,6%), balik modal 35.715 (dibulatkan ke atas), minimum 46.297, harga cantik 52.900, laba 15.037,5 → 15.038 (28,4%), coret 17,4%. Sisi TANPA memang salah angka: di Rp52.000 untungnya 27,4% dari harga jual dan 
- **pantau-pasar-kripto:** koreksi — Skor 4→5 dan verdik BELUM tetap berlaku. Pesan 2012 (topik 1997) dan 2015 (topik 1998) dari KTclaude2bot ada di updates-g2.jsonl, dan kedua kutipan sama kata per kata. Hitungan Decimal saya cocok: FIFO 1.753.250 / 1.220.600 / −2.781.200 / 790.260 dengan total 982.910, sisa 0,003@1.614.830.000, 0,3@58.575.200, 15@3.159.450, PPh 420.786, dan bersih 562.124. Persamaan pada pesan 2015 memang memotong 

## Kutipan balasan (dipendekkan, `…` = dipotong)

### promo-kalender — TANPA (topik 1993, pesan 2001)

> Jadi masih untung, bukan rugi — tapi profit per botol anjlok sekitar 65% pas diskon 30%. Kalau target jualan tetap 60 botol doang pas 11.11, profit totalnya cuma ±754 ribu, jauh di bawah profit bulanan biasa (±2,16 juta). Supaya untung total minimal setara bulan normal, kamu butuh jual sekitar 170-an botol pas event itu (±2,9x lipat dari rata-rata bulanan).
> …
> • H-3: siapin stok minimal 150-200 botol + cek packing biar aman kena lonjakan pesanan
> • H-1: daftarin produk ke kampanye 11.11 Shopee (gratis ongkir & cashback dari Shopee, bukan dari kantong sendiri…

Alasan skor TANPA: Hitung ulang dengan Decimal. Biaya Shopee saat promo 8.726, laba 12.574 (20,2%). Saat harga normal: biaya 11.930, laba 36.070 (40,5%). Laba per botol turun 65,1%. 60 × 12.574 = 754.440; 60 × 36.070 = 2.164.200; 2.164.200 ÷ 12.574 = 172,1 botol (2,87x). Semua angka TANPA cocok. Tulisan '12% × 62.300 = 7.480' (yang benar 7.476) hanya selisih pembulatan Rp4 dan hasilnya ditulis '±12.570', jadi tidak dihitung salah angka. Kekurangan: (1) promo SATU hari dibandingkan dengan laba SEBULAN, sehingga keluar target 170-an botol dan saran menyetok 150–200 botol (±3 bulan penjualan), berisiko menumpuk stok; (2) tidak ada batas diskon maksimal dan tidak ada opsi pembanding berangka; (3) linimasa tanpa tanggal, dan 'H-1 daftarin ke kampanye 11.11 Shopee' terlambat; (4) klaim 'gratis ongkir & cashback dari Shopee, bukan dari kantong sendiri' tanpa dasar; (5) tanpa S&K; ada istilah awam-sulit seperti 'AOV' dan 'FOMO'. Kelebihan: langsung menjawab 'masih untung', ada pembanding dengan harga normal, dan tips praktis (jam flash sale, batas per pembeli, minta ulasan); satu tawaran di akhir. Rincian: kebenaran 5,5, siap pakai 6, kepatuhan 7, perilaku 8, bahasa 7 → 6,5.

### promo-kalender — DENGAN (topik 1994, pesan 2004)

> Jawaban singkat: Ya kak, diskon 30% itu masih untung, tapi marginnya lumayan menipis (20,2%). Ada opsi lain yang laba bersihnya lebih gede kalau mau dipertimbangkan.
> …
> • Diskon 30% → harga jual Rp 62.300, laba Rp 12.574/botol, margin 20,2% ✅ AMAN
> • Diskon 20% → harga jual Rp 71.200, laba Rp 20.406/botol, margin 28,7% ✅ AMAN (laba hampir 2x lipat dari diskon 30%)
> • Bundling 2 botol = Rp 129.000 → harga efektif Rp 64.500/botol (hemat 27%), laba Rp 15.135/botol, margin 23,5% ✅ AMAN
> 
> Diskon maksimal biar nggak rugi: 46% (jadi 30% masih jauh dari batas bahaya).
> …
> Kalau tetap mau 30% (biar kelihatan gede & menarik di 11.11), impas biasa tercapai cuma dari 6 botol — sisanya udah laba bersih.
> 
> 3. Linimasa persiapan 11.11 (jatuh hari Rabu, 11 Nov 2026)
> 
> • H-14 (28 Okt) — kunci mekanisme, siapin stok ekstra, daftar campaign di Seller Center
> …

Alasan skor DENGAN: Balasan utuh dalam satu pesan (3.249 karakter, tanpa tabel, ±3 menit; 'Working' diabaikan), tanpa berkas. Kelebihan: jawaban singkat di awal ('masih untung, margin 20,2%'); tiga opsi dihitung (diskon 30%, diskon 20%, paket 2 botol) dengan status AMAN; batas diskon 46%; total omzet/laba per opsi; target 6 botol untuk menyamai laba hari biasa; linimasa bertanggal (Rabu 11 Nov, H-14 28 Okt s.d. H+7 18 Nov) dengan daftar kampanye di H-14; S&K siap tempel memakai [isi: …] tanpa janji karangan; peringatan harga coret harus jujur dan cek biaya terbaru; satu tawaran di akhir. Semua angka cocok dengan hitung ulang. Cek pra-cek: opsi 25% Rp66.800 tidak muncul lagi; salah ketik 'kanus' dan klaim 'traffic naik jauh' juga tidak ada. Kekurangan: (1) pembuka 'cek margin-nya dulu pake skill promo-kalender' memakai kata proses/nama alat; (2) 'laba hampir 2x lipat dari diskon 30%' berlebihan, sebenarnya 1,62x; (3) 'impas biasa tercapai cuma dari 6 botol — sisanya udah laba bersih' menyesatkan bagi awam, karena setiap botol sudah untung Rp12.574 (maksudnya menyamai laba hari biasa); (4) total kampanye memakai asumsi 60 botol dalam sehari (bot menandainya optimis dan menawarkan hitung ulang 15–20 botol); (5) istilah 'opt-in'. Rincian: kebenaran 8, siap pakai 8,5, kepatuhan 7, perilaku 9, bahasa 7,5 → 8,0.

### riset-harga-kompetitor — TANPA (topik 1995, pesan 2006)

> Cek margin di harga 58.000 (modal 30.000):
> …
> • Untung = 49.500 − 30.000 = Rp19.500
> • Margin dari modal = 65%, margin dari harga jual = 33,6%
> …
> 2. Tapi kalau mau lebih kompetitif buat gaet volume kayak Kopi Rakyat/Gayo Roastery (yang jualan ribuan), kamu punya ruang gede buat turun ke Rp52.000–54.000 dan margin masih tetap sehat (~29-30% dari harga jual, ~50%+ dari modal) — jauh di atas target 20% kamu.

Alasan skor TANPA: Penyetaraan ke 250 gr benar (Gayo Roastery ≈53.100, nilai persisnya 53.125). Duplikat tidak ikut dihitung, tapi hal itu tidak disebutkan. Rincian potongan di harga 58.000 benar (8.500, laba 19.500, 65% dari modal / 33,6% dari harga jual). Harga Rp42.600 untuk untung 20% dari modal juga benar (42.571), walau keliru disebut "harga impas". Saran turun ke 54.000 dengan untung Rp16.000 benar. Namun persen untung untuk rentang 52–54 ribu salah hitung, sehingga skor dibatasi maks 5. Kekurangan lain: tidak ada median, harga balik modal, harga minimum dengan target dari harga jual, maupun ringkasan harga coret. Tidak terlihat pencarian web.

### riset-harga-kompetitor — DENGAN (topik 1996, pesan 2009)

> Statistik pasar: terendah Rp48.000, P25 Rp49.375, median Rp53.125, P75 Rp54.825, tertinggi Rp80.000.
> 
> Posisi harga kamu (Rp58.000): lebih mahal dari 6 dari 7 pesaing, cuma lebih murah dari Sidikalang Jaya. Laba sekarang Rp19.500/pcs (margin 33,6%) — masih aman, tapi kamu di atas pasar.
> 
> Batas untung kamu (modal 30rb + kemasan, biaya proses 1.250, admin 8%+ongkir 4%+PPh 0,5% = 12,5%, target margin 20%):
> • Harga balik modal: Rp35.715
> • Harga minimum (biar margin 20% tercapai): Rp46.297
> 
> Rekomendasi (strategi tengah pasar): rentang Rp49.375–Rp54.825, titik Rp53.125, harga cantik terdekat Rp52.900 (laba Rp15.038/pcs, margin 28,4%).
> …
> 2. Pesaing terlaris (Kopi Rakyat) pakai harga coret + harga murah (49rb) — pertimbangkan kasih harga coret juga biar kelihatan promo, bukan cuma turun harga polos.
> …

Alasan skor DENGAN: Semua angka cocok dengan hitungan ulang Decimal. Duplikat Gayo Roastery dibuang secara terang, harga semua pesaing disetarakan ke 250 gr, dan statistik pasar lengkap. Posisi Rp58.000 benar (lebih mahal dari 6 dari 7, 'termahal kedua'). Laba saat ini, harga balik modal, harga minimum margin 20%, rentang tengah, dan harga cantik beserta labanya semuanya benar. Balasan ringkas (±1.960 karakter) tanpa tabel, cocok untuk Telegram, dan ditutup catatan sumber data. Kesalahan pra-cek '9–18% di atas median' tidak terulang. Kekurangan: P25/P75 tidak dijelaskan dengan bahasa awam. Saran memasang harga coret 'biar kelihatan promo' tidak disertai syarat harga coret harus jujur, padahal itu diwajibkan SKILL.md; ini masalah serupa pra-cek walau lebih ringan dan tidak menyuruh menaikkan harga normal. Tidak disebutkan bahwa margin 20% dihitung dari harga jual. Ada frasa 'modal 30rb + kemasan', padahal member bilang 30 ribu sudah termasuk kemasan. Rentang Pak Darmo 54.900–62.900 tidak disebut, dan tidak ada ringkasan harga coret pesaing (3/7, rata 17,4%). Tidak terlihat pencarian web.

### pantau-pasar-kripto — TANPA (topik 1997, pesan 2012)

> Angka pajak di bawah aku pakai acuan terakhir yang aku tahu pasti (PMK 68/2022): PPh Final Pasal 22 0,1% dari nilai transaksi jual kalau lewat exchange terdaftar PFAK (Indodax), dan 0,2% kalau lewat exchange nggak terdaftar di Indonesia (Binance, berlaku buat jual ETH 19 Agu). … Total laba bersih (realized, sebelum pajak): Rp802.370 … • Total estimasi PPh = Rp115.860
> 
> Perkiraan laba bersih setelah pajak: Rp686.510

Alasan skor TANPA: Hitungan dengan metode rata-rata tertimbang (bukan FIFO, pengguna tidak menyebut metode) cocok dengan hitung ulang: P/L 1.452.350 / 910.620 / 1.220.600 / −2.781.200, total Rp802.370. Bot juga jujur bahwa pencarian web mati. Namun permintaan inti 'pajaknya pakai aturan yang baru' gagal. Bot memakai tarif PMK 68/2022 sehingga PPh terhitung terlalu kecil (Rp115.860 vs Rp420.786) dan untung setelah pajak salah (Rp686.510). Total modal sisa ditulis sebagai 'modal rata-rata'. Bot menebak PPh belum dipotong, lalu menyajikan satu angka bersih walau sendiri menyebut Indodax biasanya sudah memotong. Ada spekulasi soal PPN, tanpa disclaimer, dengan komentar 'posisi SOL perlu diwaspadai'. Ada salah angka/fakta, jadi skor dibatasi maks 5; diberi 4.

### pantau-pasar-kripto — DENGAN (topik 1998, pesan 2015)

> • BTC jual 5 Agu (0,010 BTC): proceeds Rp16.998.850 − modal Rp15.245.600 − fee Rp51.150 = +Rp1.753.250 (+11,5%) … Total untung bersih (sebelum pajak): Rp982.910
> 
> Sisa koin + rata-rata modal (cost basis FIFO)
> • BTC: 0,003 @ rata-rata Rp1.614.830.000
> • ETH: 0,3 @ rata-rata Rp58.575.200
> • SOL: 15,0 @ rata-rata Rp3.159.450
> 
> Estimasi pajak (PPh Pasal 22 final, PMK 50/2025, berlaku sejak 1 Agustus 2025 — dasar: nilai transaksi JUAL, bukan dari untung)
> Karena semua jual di Indodax (PAKD dalam negeri, 0,21%) KECUALI ETH 19 Agustus di Binance (bursa luar negeri, 1%): … Total estimasi PPh: Rp420.786 … saya TIDAK menebak. … • Kalau PPh belum terpotong di kolom biaya itu → untung bersih setelah pajak = Rp982.910 − Rp420.786 = Rp562.124. … Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.

Alasan skor DENGAN: Semua angka yang diminta benar dan cocok dengan hitung ulang Decimal (FIFO, fee beli masuk modal, fee jual mengurangi hasil): P/L per transaksi dan persentasenya (+11,5% / +4,17% / −8,8% / +10,01%), total Rp982.910, sisa koin beserta rata-rata modal FIFO, PPh per transaksi 35.805 / 306.000 / 60.690 / 18.291 dengan total Rp420.786, serta dua skenario PPh (sudah atau belum masuk kolom biaya → Rp982.910 / Rp562.124) tanpa menebak. Aturan PMK 50/2025 disebut dengan benar (sejak 1 Agustus 2025, basis nilai jual, 0,21% PAKD, 1% luar negeri). Tidak ada tabel, ada saran ke konsultan pajak/DJP, disclaimer baku ada, dan tidak ada sinyal, auto-trading, atau kunci API. Kekurangannya: persamaan di keempat baris rincian mengurangkan fee dua kali sehingga tidak cocok bila dihitung ulang (salah angka → maks 5). Selain itu tidak ada pengingat bahwa PPh 1% Binance disetor sendiri, dan ada jargon Inggris ('proceeds', 'realized P/L', 'cost basis') serta frasa proses '(bukan hitungan manual)'.
