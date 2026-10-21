# Gelombang Telegram A9 — 2026-10-21 (bot pertama)

Uji di grup Telegram sungguhan dengan bot pertama `@KTclaude1_bot` (Akun A), OpenClaw 2026.10.2, 21 Okt 2026 pukul 05:41–05:56 UTC, topik baru 2233–2240 (8 pesan, berurutan dengan jeda, tanpa balas-otomatis). Pesan uji sama persis di sisi TANPA (topik dengan `skills: []`; selama sisi TANPA folder skill dipindah keluar HOME bot, log tidak menunjukkan akses ke folder skill) dan DENGAN. Sebelum gelombang, berkas sisa uji lain di workspace bot dipindah ke cadangan scratchpad. Pesan, data, dan kunci dari `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json`; pra-cek di `koordinasi/pracek-telegram-akun-a-2026-10-17.md` (kelompok 6 + laporan-iklan-mingguan 1.0.12). umami-analitik memakai server tiruan Umami (rekaman fiktif) dengan geseran 21 hari agar "minggu lalu" 12–18 Okt dan minggu sebelumnya 5–11 Okt memetakan ke dua minggu rekaman yang berbeda. Penilai independen Opus per skill (bukan pembuat skill), kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian"; angka kunci dihitung ulang (Decimal, salinan data).

Acuan: **LULUS** bila DENGAN ≥ 8, selisih ≥ 1,5, dan tidak ada salah angka kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| umami-analitik | 1.0.6 | 2239 / 2240 | 3,0 | 8,5 | +5,5 | **LULUS** | Dengan skill, bot langsung membuka Umami toko dan menjawab pengunjung minggu lalu naik dari 4 jadi 11 (+175%), halaman teratas, dan separuh kunjungan dari media sosial; tanpa skill, bot bilang belum punya akses lalu meminta alamat, token, bahkan kata sandi. |
| frappe-books-usaha | 1.0.10 | 2235 / 2236 | 5,0 | 8,5 | +3,5 | **LULUS** | Dengan skill, bot menemukan piutang Agustus Rp843.600 yang sudah telat 32 hari sehingga total belum dibayar Rp3.231.100 diurutkan dari yang paling telat; tanpa skill, bot hanya melihat September (Rp2.387.500) dan utang terlama terlewat. |
| laporan-iklan-mingguan | 1.0.12 | 2233 / 2234 | 7,5 | 8,5 | +1,0 | **BELUM** | Dengan skill laporannya lebih rapi dan lengkap (CPC/CPM/CTR, catatan PPN, label "jangan dimatikan cuma karena 0 chat"), tetapi tanpa skill pun bot sudah menghitung angka dengan benar dan menyarankan mematikan iklan yang sama. |
| grist-usaha | 1.0.10 | 2237 / 2238 | 8,0 | 8,5 | +0,5 | **BELUM** | Kedua sisi sama benar (2 habis, 5 menipis, nilai stok Rp2.698.000); skill hanya menambah batas minimum dan catatan asal angka — bedanya terlalu kecil untuk dirasakan pembeli. |

Catatan acuan: laporan-iklan-mingguan dan grist-usaha lulus uji internal sebelumnya, tetapi di bot asli model tanpa skill sudah cukup kuat untuk skenario ini; selisih < 1,5 berarti tidak dipromosikan (aturan 2026-10-03). Usulan untuk Akun B (pemegang katalog/promosi): grist-usaha diuji ulang lewat keunggulan khasnya (buat tabel dengan pratinjau, tulis rumus Grist, impor CSV berantakan) + daftar belanja siap pakai; laporan-iklan-mingguan: pastikan blok "Arti istilah" terkirim, pisahkan biaya per chat kampanye WA dari trafik/awareness, tandai iklan yang baru tayang. umami-analitik: sertakan laporan UTM bila pengguna menyebut IG/WA/TikTok.

## Rincian

### umami-analitik 1.0.6 — TANPA 3,0 → DENGAN 8,5 (+5,5) LULUS

**Angka kunci (dihitung ulang dari rekaman, `/stats`, `/metrics/expanded` periode 21–27 Sep vs pembanding 14–20 Sep):**
- Pengunjung unik 11 vs 4 → +7, **+175%**. Kunjungan 12 vs 4 → +8, **+200%**. Tayangan 23 vs 6 → **+283%**.
- Bounce: 3/12 = **25%** minggu lalu, sebelumnya 2/4 = **50%**, jadi membaik. (Catatan: teks kunci pra-cek "bounce 50% → 25%" artinya dari minggu sebelumnya ke minggu lalu; label tanggal "5–11 Okt" di kunci adalah sisa pra-cek dengan tanggal lain. Kunci yang benar untuk uji 21 Okt adalah 12–18 Okt.)
- Halaman teratas (pengunjung): / 10 (11 tayangan) = 10/11 = 91%; /produk/keripik-balado 5 (45%); /cara-pesan 3 (27%); /produk/keripik-original 2; /terima-kasih 2.
- Kanal (kunjungan): media sosial organik 6/12 = **50%**, langsung 4/12 = **33%**, pencarian 2/12 = **17%**. Perujuk: l.instagram.com 3, tiktok.com 2, google.com 2, l.facebook.com 1.
- UTM minggu yang sama (tidak ditanyakan bot): utm_source instagram 3, tiktok 2, **whatsapp 2** (kampanye promo-gajian-sep 7).

Sisi DENGAN benar semua untuk angka yang ditulis: periode Sen 12–Min 18 Okt, 11 vs 4 (+175%), 12 vs 4 (+200%), tayangan 23 vs 6, bounce 50% → 25%, lima halaman beserta persennya, kanal 50/33/17 dengan jumlah kunjungan, dan rincian perujuk. Persentase kenaikan tayangan (+283%) tidak ditulis, tetapi kedua angkanya ada. Tidak ada angka karangan.

Kutipan DENGAN:
> Periode **minggu lalu (Senin 12 Okt – Minggu 18 Okt 2026)** vs minggu sebelumnya (5–11 Okt): **Pengunjung: NAIK** — Pengunjung unik: 11 (sebelumnya 4 → naik 7, +175%) … Bounce rate: 25% (sebelumnya 50%, jadi membaik)
> Media sosial (organik, dari klik IG/TikTok/FB): 50% — 6 kunjungan · Langsung (termasuk WhatsApp/Telegram/aplikasi …): 33% · Pencarian Google: 17%

**Alasan skor DENGAN 8,5:**
- (+) Menjawab ketiga pertanyaan (naik/turun, halaman teratas, asal pengunjung) dalam satu pesan, dengan angka nyata dari Umami, periode jelas, dan perbandingan dengan selisih serta persen.
- (+) Aturan skill dipatuhi: angka halaman/sumber disebut sebagai pengunjung per baris dan tidak dijumlah antarbaris; "Langsung" dijelaskan mencakup klik WA; satu saran berlabel tawaran (UTM).
- (+) Bahasa awam ("bounce rate … jadi membaik", istilah UTM dijelaskan sebagai "kode pelacak khusus"), tanpa jalur berkas, tanpa kunci, tanpa nama skrip.
- (−) Pengguna menyebut WA secara khusus, dan data UTM minggu itu justru sudah mencatat **whatsapp 2 pengunjung** (kampanye promo-gajian-sep sudah ber-UTM). Bot tidak membuka laporan UTM dan malah menulis "klik dari WA tidak kebaca sumbernya" serta menawarkan membuatkan UTM. Ini bukan salah angka kunci, tetapi jawaban untuk "WA" kurang lengkap dan sedikit menyesatkan.
- (−) Kenaikan tayangan tidak diberi persen, dan "Udah dicek" sedikit berbau kata proses (ringan).

**Alasan skor TANPA 3,0:**
- (+) Jujur: tidak mengarang angka. Mengakui belum punya akses dan mengingatkan agar token/kata sandi tidak ditempel di grup.
- (−) Tidak ada hasil sama sekali untuk tiga pertanyaan pengguna. Tidak menemukan kunci Umami yang sudah tersedia di komputer bot.
- (−) Meminta tiga hal teknis sekaligus, termasuk username/password. Tidak ada jalan alternatif (mis. cara membaca layar Overview Umami sendiri).
- (−) Salah membaca periode: menulis "minggu ini vs minggu lalu", padahal pengguna bertanya minggu lalu vs minggu sebelumnya.

**Lintas cek:**
- Log server tiruan (blok terakhir): bot DENGAN memanggil `/api/websites` dan tim, lalu `/stats` untuk 12–18 Okt dan 5–11 Okt, `/metrics/expanded type=path`, `type=channel`, dan `type=referrer`, semuanya dengan geseran 21 hari. Data dibaca langsung, tidak ditebak. Tidak ada panggilan `utmSource`, yang cocok dengan kekurangan soal WA di atas.
- Semua angka DENGAN cocok dengan rekaman (dihitung ulang dari `visitors`/`visits`/`pageviews`/`bounces`). Jawaban ganda di transkrip tidak ada.
- Pembanding: pra-cek konteks Telegram 8,5 (SIAP KIRIM). Hasil di bot asli sama.

**Saran perbaikan (opsional, tidak menghalangi LULUS):** bila pengguna menyebut IG/WA/TikTok, sertakan laporan UTM (`utm`) di jawaban yang sama. Jangan menulis "WA tidak terbaca" bila `utm_source=whatsapp` sudah ada datanya.

### frappe-books-usaha 1.0.10 — TANPA 5,0 → DENGAN 8,5 (+3,5) LULUS

**Angka kunci (dihitung ulang dengan Decimal dari salinan berkas SQLite; berkas asli tidak disentuh):**
- Invoice penjualan September yang final (submitted=1, cancelled=0) ada 4: SINV-1001 sampai SINV-1004. SINV-1005 masih draf dan SINV-1006 dibatalkan, jadi keduanya tidak dihitung.
- DPP 1.360.000 + 1.250.000 + 160.000 + 2.040.000 = **Rp4.810.000**. Total 1.509.600 + 1.387.500 + 160.000 + 2.264.400 = **Rp5.321.500**. PPN **Rp511.500**.
- Sisa tagihan September 1.387.500 + 1.000.000 = **Rp2.387.500**, jadi yang sudah terbayar **Rp2.934.000**.
- Piutang keseluruhan: SINV-1007 Toko Maju Jaya (20 Agu) Rp843.600 + Rp2.387.500 = **Rp3.231.100** (3 invoice). Toko Maju Jaya sudah belum bayar sejak akhir September.
- HPP 1.100.000 + 1.000.000 + 120.000 + 1.550.000 = **Rp3.770.000**. Laba kotor **Rp1.040.000**. Beban sewa 500.000 + listrik 300.000 = **Rp800.000**. Laba bersih **Rp240.000**.
- Cek keterlambatan (dengan asumsi tempo 30 hari dan hari ini 21 Okt): SINV-1007 jatuh tempo 19 Sep, jadi telat 32 hari. SINV-1002 jatuh tempo 8 Okt, jadi telat 13 hari. SINV-1004 jatuh tempo 22 Okt. Semuanya benar.
- Kunci di `kandidat-a-cepat.json` cocok dengan hitungan ulang ini.

Sisi DENGAN benar semua, termasuk rincian per pelanggan (CV Karya Bangun 2 invoice Rp3.651.900). Sisi TANPA benar untuk penjualan, HPP, dan laba. Namun piutangnya salah: bot menulis "PIUTANG per akhir September … Total piutang: Rp 2.387.500", padahal SINV-1007 Rp843.600 juga belum dibayar pada tanggal itu. Ini salah angka kunci, jadi skor TANPA maksimal 5.

Kutipan DENGAN:
> Total piutang belum lunas: **Rp 3.231.100** (3 invoice)
> - Toko Maju Jaya - SINV-1007 (20 Agu) - Rp 843.600 - **telat 32 hari** ⚠️
> - CV Karya Bangun - SINV-1002 (8 Sep) - Rp 1.387.500 - telat 13 hari
> - CV Karya Bangun - SINV-1004 (22 Sep) - Rp 1.000.000 - belum jatuh tempo (JT 22 Okt)
>
> Catatan: ini piutang keseluruhan per hari ini, bukan khusus transaksi September (Toko Maju Jaya invoicenya Agustus).

**Alasan skor DENGAN 8,5:**
- (+) Semua angka kunci benar. Draf dan invoice batal dikeluarkan dari hitungan, dan bot menyebutkannya.
- (+) Piutang dihitung lengkap lintas bulan, dengan umur tagihan dan catatan jujur bahwa angkanya bukan khusus September. Ini yang paling berguna untuk menagih.
- (+) Asumsi tempo 30 hari disebut terang. Ada catatan bahwa ini bukan laporan keuangan resmi atau pajak, dan bot menawarkan format WA di akhir (1 pertanyaan).
- (+) Tidak ada jalur berkas, kata proses, atau tabel mentah. Jawaban utuh dalam 1 pesan dan panjangnya wajar.
- (−) Masih ada istilah "DPP" dan "zona WIB" yang kurang awam, tanpa penjelasan singkat. Label "Pajak" tidak menyebut PPN 11%.
- (−) Format tebal Markdown dan daftar bernomor belum benar-benar siap diteruskan ke grup WA, padahal pengguna menyebut ingin meneruskannya. Bot baru menawarkan format WA, bukan langsung memberikannya.
- (−) Tidak ada catatan bahwa pembelian semen Rp6.105.000 tidak masuk beban, padahal sisi TANPA menjelaskannya dengan baik.

**Alasan skor TANPA 5,0 (dibatasi salah angka kunci):**
- (+) Penjualan, PPN, HPP, laba kotor, dan laba bersih benar. Rincian per invoice beserta status lunas jelas. Draf dan invoice batal disebut terpisah.
- (+) Ada penjelasan yang baik bahwa pembelian stok tidak masuk biaya. Bahasanya awam dan ada 1 pertanyaan di akhir.
- (−) Piutang per akhir September salah, Rp2.387.500 seharusnya Rp3.231.100. Toko Maju Jaya, penunggak terlama, tidak muncul sama sekali, padahal pengguna bertanya "siapa aja yang belum bayar".
- (−) Tidak ada umur tagihan atau jatuh tempo, dan tidak ada disclaimer bukan laporan resmi. Ada beberapa emoji judul.

**Lintas cek:**
- Istilah proses dan jalur berkas: TANPA menyebut nama berkas "Sumber Rejeki.books.db". Nama itu dari pengguna sendiri, jadi wajar. DENGAN tidak menyebut nama berkas. Tidak ada kata skill/script/path di kedua sisi.
- Tabel mentah: tidak ada di kedua sisi.
- Terpotong: tidak ada. Keduanya selesai dengan pertanyaan penutup.
- Panjang: keduanya 1 pesan dengan panjang sedang.
- Data asli: tidak diubah. MD5 berkas `.books.db` di workspace bot sama dengan berkas sumber pilot (ab299c9a…), dan kedua jawaban hanya membaca data.
- Tidak ada jawaban ganda yang identik di transkrip.

### laporan-iklan-mingguan 1.0.12: TANPA 7,5 → DENGAN 8,5 (+1,0), BELUM

**Angka kunci (dihitung ulang, Decimal):**
- Belanja: Rp4.200.000 vs Rp3.000.000, **naik 40,0%**. Chat WA: 114 vs 93, **naik 22,6%**.
- Biaya per chat dari semua belanja: 4.200.000 ÷ 114 = **Rp36.842** (minggu lalu Rp32.258), **naik 14,2%**.
- Biaya per chat dari belanja kampanye WA saja: 2.950.000 ÷ 114 = Rp25.877 (minggu lalu 1.600.000 ÷ 93 = Rp17.204), naik 50,4%.
- Biaya iklan dibanding omzet: 4.200.000 ÷ 18.500.000 = **22,7%**.
- Hijab Instan Baru: Rp91.667 per chat. Ini **2,49x (≈2,5x)** rata-rata semua belanja, atau 5,05x rata-rata dua kampanye WA lainnya (Rp18.137). Retarget: **Rp15.789** per chat, yang termurah.
- Total minggu ini: CPC 656,25, CPM 7.843, CTR 1,195%.

Sisi DENGAN benar semua dan cocok dengan kunci. Sisi TANPA juga tidak punya salah angka. Rp25.877 dan "+~50%" di TANPA benar untuk definisi "kampanye WA saja", yang ditulis jelas sebagai "3 campaign WA". Nilai "hampir 5x" sebenarnya 5,05x, selisih yang bisa diabaikan.

Kutipan DENGAN:
> Biaya per chat WA masuk: Rp 36.842 (naik 14,2% dari minggu lalu Rp 32.258)
> TUJUAN BERBEDA (bukan untuk chat WA, jangan dimatikan cuma karena 0 chat)
> → **WA - Hijab Instan Baru** — biaya per chat WA-nya Rp 91.667, 2,5x lebih mahal dari rata-rata (Rp 36.842) … paling layak distop atau dirombak materinya dulu.

**Alasan skor DENGAN 8,5:**
- (+) Semua angka kunci benar dan susunannya tetap: ringkasan, vs minggu lalu, terbaik, perlu perhatian, tujuan berbeda, lalu jawaban langsung untuk "mana yang dimatikan".
- (+) "Chat WA masuk" dipahami sebagai hasil iklan. Bot tidak menawarkan sambung WhatsApp, gateway, atau pairing, jadi salah paham di versi lama sudah hilang.
- (+) Iklan trafik dan awareness dipisahkan dengan benar, tanpa saran mematikan karena 0 chat. Ada saran memindahkan anggaran ke Retarget dan catatan jujur soal PPN di tagihan.
- (−) Istilah CPC, CPM, dan CTR tidak dijelaskan. Blok "Arti istilah" yang diwajibkan skill tidak ikut terkirim, padahal pembacanya awam.
- (−) "Rata-rata" Rp36.842 ikut menghitung belanja trafik dan awareness, jadi kesan "naik 14,2%" lebih ringan daripada kenyataannya. Untuk kampanye WA saja, biaya per chat naik ±50%. Pembanding "2,5x" juga lebih kecil dari 5x di antara sesama kampanye WA.
- (−) Tidak disebut bahwa Hijab Instan Baru baru tayang minggu ini (tidak ada di data minggu lalu), dan bot tidak bertanya apakah tujuan trafik/awareness masih dibutuhkan.

**Alasan skor TANPA 7,5:**
- (+) Semua angka benar, termasuk +40%, 114 chat (+23%), 22,7% dari omzet, dan Rp91.667 untuk Hijab. Rekomendasi matikan Hijab dan pertahankan Retarget/Promo Gamis sama dengan kunci.
- (+) Perbandingan per kampanye dengan minggu lalu lebih kaya (64 dari 55, 38 tetap, Hijab "baru tayang minggu ini", CPC trafik 600 → 447, reach awareness +25%). Biaya per chat untuk kampanye WA saja malah lebih tajam.
- (+) Trafik dan awareness tidak disuruh dimatikan ("memang bukan tujuannya"). Tidak ada salah paham soal WA.
- (−) Tidak ada CPC, CPM, atau CTR keseluruhan, dan tidak ada catatan PPN. Istilah CPR/CPC juga tidak dijelaskan.
- (−) Emoji banyak dan gaya tulisannya tidak tetap dari satu bagian ke bagian lain. "Hampir 5x" sedikit kurang tepat (5,05x).
- (−) Ada giliran tambahan "NO_REPLY" setelah notifikasi exec. Kemungkinan tidak tampil di grup, tapi menandakan sisa proses.

**Lintas cek:**
- Istilah proses/jalur berkas: tidak ada di kedua sisi, baik nama berkas, skrip, gateway, maupun pairing. Notifikasi "[OpenClaw exec completion]" hanya muncul di log sisi TANPA, sebagai giliran sistem.
- Tabel mentah: tidak ada di kedua sisi. Isinya daftar baris, aman untuk Telegram.
- Terpotong: tidak ada.
- Panjang: masing-masing satu pesan, kurang lebih sama panjang dan wajar untuk chat.

**Perbaikan paling berdampak (urut dampak):**
1. Tampilkan juga biaya per chat untuk kampanye WA saja di samping rata-rata semua belanja, supaya kenaikan ±50% tidak tertutup trafik/awareness.
2. Pastikan blok "Arti istilah" (CPC/CPM/CTR dalam satu kalimat awam) benar-benar ikut terkirim di konteks Telegram.
3. Tandai kampanye yang baru muncul minggu ini ("baru, belum ada pembanding").
4. Di bagian TUJUAN BERBEDA, tutup dengan satu pertanyaan apakah tujuan trafik/awareness masih dibutuhkan, sesuai aturan skill.

### grist-usaha 1.0.10 — TANPA 8,0 → DENGAN 8,5 (+0,5) BELUM

**Angka kunci (dihitung ulang dari berkas, Decimal):**
- Tabel `Stok` berisi 12 baris. Untuk setiap baris, StokMasuk − StokKeluar = StokSaatIni, jadi kolom rumus konsisten.
- Barang HABIS: Indomie Goreng (0, batas minimum 3) dan Sabun Cuci Piring 780ml (0, batas minimum 6).
- Barang MENIPIS: Minyak Goreng 2L 5/10, Telur Ayam 6/10, Teh Celup 3/6, Air Galon 3/5, Gas LPG 3/4.
- Barang AMAN ada 5: Beras, Gula, Kopi, SKM, dan Tepung.
- Total nilai stok (sisa × harga beli) = **Rp2.698.000**. Hasil ini cocok dengan kunci.

Kedua sisi benar semua. Tidak ada salah angka atau fakta, dan tidak ada barang yang terlewat atau dikarang.

Kutipan DENGAN:
> Indomie Goreng — HABIS (sisa 0, batas min 3 dus) … Gas LPG 3kg — MENIPIS (sisa 3 tabung, batas min 4)
> **Total nilai stok saat ini (sisa x harga beli):** Rp 2.698.000
> _(catatan: ini saya hitung sendiri dari kolom Sisa Stok x Harga Beli, bukan nilai bawaan Grist …)_
> Mau saya tambahin kolom rumus "NilaiStok" langsung di Gristnya biar kehitung otomatis ke depannya?

**Alasan skor DENGAN 8,5:**
- (+) Semua angka dan status benar, dan status diambil dari kolom yang sudah dihitung Grist. Ini sesuai maksud skill.
- (+) Bot jujur memisahkan nilai yang berasal dari Grist dan nilai hasil hitung bot sendiri. Batas minimum ditampilkan juga untuk barang yang habis.
- (+) Jawaban ringkas, berupa satu pesan berisi daftar. Tidak ada tabel mentah dan tidak ada jalur berkas.
- (+) Di akhir hanya ada satu tawaran yang relevan, yaitu kolom rumus NilaiStok.
- (−) Ada istilah yang agak teknis untuk pembeli awam: "tabel Stok", "rumus Sisa Stok & Status yang sudah dihitung Grist", dan "kolom rumus".
- (−) Tidak ada saran jumlah belanja untuk besok, misalnya selisih ke batas minimum beserta perkiraan biayanya. Padahal pengguna menulis "buat belanja besok". Justru sisi TANPA yang menawarkan hal ini.

**Alasan skor TANPA 8,0:**
- (+) Angka dan status sama benarnya, dan bahasanya awam.
- (+) Pengelompokan HABIS, MENIPIS, dan AMAN jelas. Bot juga menawarkan daftar belanja beserta perkiraan biaya isi ulang, dan tawaran ini lebih dekat ke tujuan pengguna.
- (−) Batas minimum tidak ditampilkan untuk barang yang habis.
- (−) Bot tidak menjelaskan asal angka, apakah dari Grist atau hasil hitungannya sendiri.
- (−) Ada emoji penanda, tetapi ini tidak mengganggu.

Model dasar tanpa skill sudah sanggup membaca berkas .grist (SQLite) dengan benar untuk tugas ini. Akibatnya, nilai tambah skill di skenario ringkasan stok sangat tipis.

**Saran bila ingin dinaikkan (urut dampak):**
1. Skenario uji kurang cocok: membaca stok sudah dikuasai model dasar. Untuk menonjolkan skill, uji kekuatan khasnya, misalnya membuat tabel dari kalimat bebas dengan pratinjau, menulis rumus Grist, atau mengimpor CSV berantakan.
2. Untuk permintaan "belanja besok", tambahkan daftar belanja siap pakai: jumlah sampai batas minimum (atau sampai target) dan perkiraan biaya dari harga beli.
3. Ganti istilah "tabel/kolom rumus" dengan bahasa awam, misalnya "angka sisa dan status yang sudah otomatis di Grist Anda".

**Lintas cek:**
- Istilah proses atau jalur berkas: tidak ada jalur di kedua sisi. Sisi DENGAN memakai istilah "tabel" dan "kolom rumus" (ringan).
- Tabel Markdown mentah: tidak ada.
- Terpotong: tidak ada.
- Panjang: 1 pesan per sisi, dan keduanya ringkas.
