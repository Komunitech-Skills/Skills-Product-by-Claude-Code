# Gelombang Telegram 23 — 2026-10-16 (bot kedua)

Keputusan otomatis **90/92/93** (2026-10-16). Bot uji kedua `@KTclaude2bot` (OpenClaw 2026.10.2, model router Komunitech), grup uji internal Komunitech, topik baru 1683–1688. Pesan uji identik di sisi TANPA (topik `skills: []`) dan DENGAN skill; dikirim berurutan oleh bot penguji (rantai otomatis dua jalur, keputusan 93). Penilaian: satu penilai independen per skill + pemeriksa kedua yang berusaha membantah (angka dihitung ulang, kutipan dicocokkan ke id pesan); koreksi pemeriksa sudah diterapkan di tabel.

## Skor & verdik

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| dasbor-lokal (1.0.4) | 8,5 | 7,5 | −1 | **BELUM** (DENGAN < 8) | Dengan skill, bot hanya menambahkan lokasi rak (A1, B1), daftar data yang ditemukan, dan keterangan bahwa data cuma dibaca tanpa diubah. Angka stok dan saldo sama persis dengan versi tanpa skill, padahal versi tanpa skill sudah memberi total kas Rp2.123.000 dan jumlah kekurangan stok. |
| audit-seo-toko-online (1.0.6) | 5 | 8,5 | +3,5 | **LOLOS** | Dengan skill, bot memberi 8 perbaikan yang masing-masing diberi label Dampak dan Kemudahan, menghitung panjang judul dengan pasti (118 → 59 karakter, deskripsi 144 karakter), memberi tanda [isi: ...] untuk link checkout yang belum diketahui, dan terus terang bahwa kecepatan belum diukur; tanpa skill temuannya sama dan noindex juga didahulukan, tetapi sisa daftarnya tanpa label prioritas, panjang judul hanya ditulis "110+", dan ada salah hitung "Bandung" 3x (padahal 2x). |
| analisis-excel (1.0.18) | 7,3 | 8,5 | +1,2 | **BELUM** (selisih < 1,5) | Hanya versi dengan skill yang memberi omzet tiap bulan sampai rupiah beserta persen naik-turun per bulan (puncak April Rp34.340.000, terendah Juli Rp17.476.000 = -45,6 %) dan menunjuk persis sel Total yang kosong (Q2 baris 68, Q3 baris 79 & 98) beserta cara memperbaikinya. Tanpa skill, angka bulanan hanya dibulatkan ke juta dan trennya keliru disebut "naik terus dari Jan sampai April", padahal Februari turun 25 %. Penurunan Q2→Q3 -28,8 % didapat oleh kedua sisi. |

Pembanding uji internal (skor promosi / `examples/`):
- dasbor-lokal: 7,0 → 8,75 (1.0.4).
- audit-seo-toko-online: 7,0 → 8,75 (1.0.4).
- analisis-excel: 7,25 → 8,75 (1.0.17).

Beda terhadap uji internal:
- **dasbor-lokal:** Pada uji internal, keunggulan skill ada di ketepatan angka: tanpa skill, rata-rata per nota salah karena nota void ikut dihitung. Di bot asli pertanyaannya lebih sederhana (stok menipis dan saldo per akun), dan model dasar membaca SQLite sendiri dengan benar, sehingga keunggulan itu tidak muncul. Hasilnya malah terbalik: tanpa 8,5 vs dengan 7,5.
- **audit-seo-toko-online:** Di uji internal, sisi TANPA mengarang fakta dan mengubah file tanpa diminta. Di bot asli, sisi TANPA tidak mengarang, menemukan ketujuh cacat, dan hanya salah hitung "Bandung 3x", sehingga keunggulan DENGAN bergeser ke prioritas, hitungan karakter, dan batasan. Skor DENGAN di bot (8,5) hampir sama dengan uji internal (8,75).
- **analisis-excel:** Hasil di bot asli hampir sama dengan uji internal (7,0 → 8,5 vs 7,25 → 8,75, selisih tetap 1,5), padahal file kali ini lebih sulit: 3 sheet, sheet tersembunyi, angka berupa teks, dan rumus tanpa nilai tersimpan. Sisi tanpa skill kini juga menangani jebakan data dengan benar dan kalah terutama di narasi tren, sedangkan sisi dengan skill akurat penuh tetapi kurang terbuka soal baris TOTAL bawaan dan retur.

Catatan jujur (untuk pembeli):
- **dasbor-lokal:** Untuk pertanyaan sederhana seperti stok menipis dan saldo kas, asisten tanpa skill pun sudah menjawab sama tepatnya. Balasan dengan skill masih memakai istilah teknis (nama database, "read-only", Datasette) dan belum menampilkan total kas maupun ringkasan penjualan dari kasir.
- **audit-seo-toko-online:** Tanpa skill pun AI sudah menemukan cacat-cacat utama halaman ini; kelebihan versi berskill ada pada urutan prioritas, hitungan karakter yang pasti, dan keterusterangan soal batasan. Kecepatan halaman tidak diukur (perlu dicek sendiri di PageSpeed), dan judul baru diberikan sebagai teks biasa, bukan tag yang langsung bisa ditempel.
- **analisis-excel:** Transaksi yang totalnya masih berupa rumus belum tersimpan tidak ikut dihitung (di uji ini 3 transaksi, ±Rp409.000), jadi file perlu dibuka dan disimpan sekali di Excel agar angkanya lengkap. Jawaban juga belum menjelaskan kenapa baris TOTAL bawaan file berbeda dari hasil hitungan, dan tidak menyebut adanya retur.

Salah angka/fakta yang ditemukan:
- dasbor-lokal: tidak ada
- audit-seo-toko-online: TANPA: menyebut judul mengulang "Bandung" 3x, padahal di <title> kata itu muncul 2x (dihitung ulang)
- analisis-excel: tidak ada

Pemeriksa kedua:
- **dasbor-lokal:** setuju — Kedua balasan ada di log dari KTclaude2bot: msg 1818 di topik 1683 dan msg 1824 di topik 1684. Kutipan DENGAN sama persis dengan pesannya. Kutipan TANPA hanya melewati paragraf mutasi di bagian "…", jadi maknanya tidak berubah. Saya hitung ulang dari salinan data dalam mode baca-saja. Laci 500.000+50.000−120.000=430.000, Bank 2.000.000−350.000=1.650.000, QRIS 43.000, total 2.123.000. Stok KRP-001 
- **audit-seo-toko-online:** koreksi — Kutipan, message_id 1829–1830 (topik 1685) dan 1833–1835 (topik 1686) cocok. Hitung ulang: title 118, "Bandung" muncul 2x, title baru 59, meta 144, semuanya benar. Batas maks. 5 untuk TANPA sah, jadi verdik LOLOS tetap berlaku. Yang perlu dikoreksi pembedanya, karena terlalu melebih-lebihkan kekurangan TANPA. TANPA (1829) menulis "Temuan paling fatal duluan" dan menutup dengan "Fokus utama ya poin
- **analisis-excel:** koreksi — Kutipan msg 1839 (topik 1687) dan 1842 (topik 1688) ada kata per kata, keduanya dari KTclaude2bot. Hitung ulang dengan openpyxl cocok: TANPA Rp97.322.500/Rp69.329.500 (3 sel diisi qty×harga), DENGAN cocok kunci, termasuk persen per bulan dan Jan→Sep +5,5 %. Tidak ada salah angka. Rincian TANPA 6+7+7,5+8+8 rata-ratanya 7,3, bukan 7,0. Gelombang 21 memakai rata-rata persis, dan DENGAN di sini juga (

## Kutipan balasan (dipendekkan, `…` = dipotong)

### dasbor-lokal — TANPA (topik 1683, pesan 1818)

> 📊 Dasbor Toko — 17 Okt 2026
> 
> ⚠️ Stok Menipis (stok di bawah batas minimum)
> • Keripik Pedas Bandung (250 gr) — sisa 12 pak, minimum 20 (kurang 8)
> • Basreng Pedas (150 gr) — sisa 5 pak, minimum 10 (kurang 5)
> 
> Produk lain masih aman: Sambal Bawang (30 botol), Keripik Singkong Balado (40 pak), Kemasan Standing Pouch (400 pcs).
> 
> 💰 Saldo Kas per Akun
> • Laci kas (tunai): Rp430.000
> • Bank: Rp1.650.000
> • QRIS: Rp43.000
> • Total: Rp2.123.000
> …
> Mau saya buatkan rekomendasi jumlah restock untuk Keripik Pedas Bandung dan Basreng Pedas?

Alasan skor TANPA: Semua angka cocok dengan hitung ulang sendiri (sqlite3 mode baca-saja pada salinan data). Stok menipis: KRP-001 12 (min 20, kurang 8) dan BSK-001 5 (min 10, kurang 5); tidak ada yang habis. Tiga produk lain aman (30 botol, 40 pak, 400 pcs). Saldo: Laci kas Rp430.000, Bank Rp1.650.000, QRIS Rp43.000, total Rp2.123.000. Mutasi: 2 masuk (Rp93.000), 2 keluar (Rp350.000 + Rp120.000), semua aktif. Tanggal 17 Okt sesuai WIB (dibalas 01.01 WIB). Hasil utuh di chat, bahasanya awam, tanpa kata proses, ditutup dengan satu tawaran. Kekurangan: ringkasan penjualan dari kasir.db tidak ditampilkan padahal pengguna minta "buka dasbor toko", dan frasa "status aktif" agak teknis.

### dasbor-lokal — DENGAN (topik 1684, pesan 1824)

> Dasbor toko (hasil cek database Komunitech):
> 
> Database ditemukan: buku-stok, kasir-lokal, kas-umkm. (crm-wa, absensi-lokal, buku-piutang, kpi-tim belum ada — wajar kalau belum pernah dipakai.)
> 
> 📉 Stok menipis/habis:
> 
> • Keripik Pedas Bandung (250 gr) — sisa 12, batas minimal 20, lokasi A1
> • Basreng Pedas (150 gr) — sisa 5, batas minimal 10, lokasi B1
> 
> Keduanya sudah di bawah stok minimal, perlu restok.
> 
> 💰 Saldo kas per akun:
> 
> • Bank: Rp 1.650.000
> • Laci kas (tunai): Rp 430.000
> • QRIS: Rp 43.000
> 
> Semua dibaca langsung dari database lokal (read-only), tidak ada data yang diubah. Mau saya buka juga versi browser interaktifnya (Datasette) atau cek data lain seperti penjualan harian?

Alasan skor DENGAN: Semua angka benar: stok menipis KRP-001 12/20 dan BSK-001 5/10 plus lokasi A1/B1, saldo Bank Rp1.650.000, Laci kas Rp430.000, QRIS Rp43.000. Daftar database yang ada dan tidak ada juga sesuai dengan data. Klaim read-only konsisten dengan cara kerja skill (koneksi baca-saja), dan tidak ada tanda data diubah. Kekurangannya: memakai kata proses dan nama alat internal ("hasil cek database Komunitech", buku-stok, kasir-lokal, kas-umkm, crm-wa, absensi-lokal, buku-piutang, kpi-tim), memakai istilah "read-only" dan "Datasette" ke pengguna awam, tidak ada total kas, tidak ada jumlah kekurangan stok, tidak menyebut produk yang aman, dan penjualan kasir tidak ditampilkan meski kasir-lokal ditemukan. Secara isi tidak lebih baik dari versi tanpa skill.

### audit-seo-toko-online — TANPA (topik 1685, pesan 1829, 1830)

> Udah saya cek halaman-produk.html-nya. Temuan paling fatal duluan, baru yang lain. … 1. KRITIS — Halaman di-blokir dari Google! Ada <meta name="robots" content="noindex,follow"> di <head>. … 2. Judul (title tag) kepanjangan & keyword stuffing Judul sekarang 110+ karakter, Google bakal motong di hasil pencarian dan kata "Terlaris... Baru 2026" + pengulangan "Bandung" 3x bisa kebaca spammy. … <title>Keripik Pedas Bandung 250 gr Renyah & Gurih | Toko Renyah Jaya</title> 3. Meta description-nya kosong … 4. Dua H1 dalam satu halaman … 5. Gambar tanpa alt text …

Alasan skor TANPA: Ketujuh cacat yang ditanam ditemukan semua: noindex (ditandai paling kritis), title kepanjangan, meta description kosong, 2 H1, gambar tanpa alt dan alt kosong, tanpa JSON-LD dan tanpa OG. href="#" juga ditemukan, tetapi hanya sebagai catatan tambahan. Kode siap tempelnya lengkap: title dalam tag, JSON-LD dengan brand, OG ditambah twitter card. Kekurangannya: tidak ada urutan prioritas selain poin 1, panjang judul hanya ditulis "110+", kecepatan/ukuran halaman dan batasan audit tidak disebut. Meta description usulannya sendiri mengulang "Bandung" 3x dan menghilangkan syarat "sebelum jam 14.00" dari klaim kirim same-day. Ada salah fakta ("Bandung 3x" di judul, padahal 2x), jadi skor dibatasi maks. 5. Tanpa batas itu nilainya ±7,5.

### audit-seo-toko-online — DENGAN (topik 1686, pesan 1833, 1834, 1835)

> 🔴 Temuan paling kritis duluan: halaman ini pakai <meta name="robots" content="noindex,follow"> … Daftar Perbaikan (prioritas) 1. Hapus noindex — Dampak Tinggi · Mudah. … 2. Perbaiki link "Beli Sekarang" — Dampak Tinggi · Mudah. Hrefnya cuma #, tombolnya tidak mengarah ke mana-mana (bisa kehilangan penjualan). 3. Pendekin title — Dampak Tinggi · Mudah. 118 karakter, berpotensi terpotong di hasil pencarian … 4. Isi meta description … 5. Betulkan 2 H1 jadi 1 … 6. Isi alt text 2 gambar … 7. Tambah Open Graph tags … 8. Tambah JSON-LD Product schema … Title baru (59 karakter): Keripik Pedas Bandung 250gr Renyah Gurih - Toko Renyah Jaya … <a href="[isi: link keranjang/checkout produk ini]" class="btn">Beli Sekarang</a> … • Kecepatan di HP: — belum dicek (saya tidak bisa mengukur beneran, coba cek sendiri di https://pagespeed.web.dev/ — kirim hasilnya kalau mau dibantu artikan)

Alasan skor DENGAN: Ketujuh cacat ditemukan, ditambah href="#", dan semuanya masuk ke daftar 8 perbaikan berurut Dampak × Kemudahan dengan ringkasan per bagian. Panjang judul lama 118, judul baru 59, dan meta 144 karakter, semuanya benar saat dihitung ulang. Teks perbaikan hanya diambil dari isi halaman (harga Rp25.000, kirim sebelum jam 14.00, domain dari canonical), dan link checkout yang tidak diketahui ditandai [isi: ...]. Kecepatan diakui belum diukur dan pengguna diarahkan ke PageSpeed. Batasan dan asumsi disebut, tidak ada klaim peringkat/trafik, dan balasan ditutup dengan tawaran menempelkan perbaikan ke file. Kekurangannya: menyebut "pakai skill audit SEO" (kata proses), judul baru tidak dibungkus tag <title>, og:image diberi placeholder padahal JSON-LD memakai URL lengkap, dan ukuran halaman (±3,3 KB) tidak disebut.

### analisis-excel — TANPA (topik 1687, pesan 1839)

> • 3 baris total-nya kosong, saya hitung ulang dari qty × harga satuan. … • Semen — Rp105.444.000 (qty 1.683) ← juara, ~45% dari total omzet … • Feb: Rp17,9jt
> • Mar: Rp25,5jt
> • Apr: Rp34,3jt ← puncak … • Jul: Rp17,5jt ← anjlok tajam … Polanya: naik terus dari Jan sampai puncak di April, lalu jatuh keras di Juli, dan baru pulih pelan-pelan di Agustus-September tapi belum balik ke level Q2. … • Q2: Rp97.322.500 (171 transaksi)
> • Q3: Rp69.329.500 (181 transaksi)
> • Selisih: -Rp27.993.000 (-28,8%) …

Alasan skor TANPA: Hitung ulang Python dengan cara TANPA (3 sel Total kosong diisi qty × harga, teks "Rp 68.000" dan retur "(185.000)" dibaca sebagai angka, kategori dirapikan) cocok semua: Semen Rp105.444.000 (qty 1.683, ~45 %), Pipa & Sanitasi Rp25.652.000 (qty 152), Alat & Perkakas Rp8.404.000 (qty 220), Mei Rp30,9 jt, Agu Rp26,6 jt, Q2 Rp97.322.500 (171 trx), Q3 Rp69.329.500 (181 trx), turun Rp27.993.000 (−28,8 %), rata-rata per transaksi ±Rp569 rb → ±Rp383 rb. Mengisi 3 sel kosong dari qty × harga itu sah karena rumusnya =E×F, jadi selisihnya dengan kunci (+Rp210.000 di Q2, +Rp199.000 di Q3) tidak dihitung salah angka. Kelebihan: jujur soal mutu data (retur, angka berupa teks, baris TOTAL bawaan lebih kecil karena SUM melewati teks) dan memberi wawasan bagus bahwa transaksi Q3 lebih banyak tetapi nilai belanjanya lebih kecil. Kekurangan: (1) narasi tren keliru, "naik terus dari Jan sampai puncak di April" padahal Feb turun ±25 %, dan "pulih pelan-pelan di Agustus-September" padahal Agustus melonjak ±52 % lalu September turun. Sesuai preseden gelombang 21, ini dicatat sebagai narasi tidak tepat, bukan salah angka. (2) Menyebut ada "typo" nama kategori, padahal yang ada hanya beda huruf besar-kecil dan spasi. (3) Angka bulanan hanya dibulatkan ke juta, tanpa persen perubahan dan tanpa tabel. Perilaku baik: dikerjakan dulu, satu tawaran di akhir. Rincian: kebenaran 6, siap pakai 7, kepatuhan 7,5, perilaku 8, bahasa 8 → 7,0.

### analisis-excel — DENGAN (topik 1688, pesan 1842)

> | Semen           | Rp 105.444.000 | 149       | … → Semen jauh di atas kategori lain, 45,2% dari total omzet Rp 233.556.000. … | Apr   | Rp 34.340.000 | +34,6%              | … | Jul   | Rp 17.476.000 | -45,6%              | … → Puncak di April (Rp 34,3 jt), titik terendah di Juli (Rp 17,5 jt — anjlok 45,6% dari Juni). Dari Jan ke Sep naik tipis 5,5% secara keseluruhan, tapi fluktuatif naik-turun, bukan tren lurus. … • Q2 (Apr-Jun): Rp 97.112.500
> • Q3 (Jul-Sep): Rp 69.130.500
> • Turun 28,8% (selisih -Rp 27.982.000), didorong anjloknya Juli. … • 3 sel Total kosong karena rumus tanpa nilai tersimpan (Q2 baris 68, Q3 baris 79 & 98) — tidak ikut dihitung. Saran: buka file di Excel, tekan Simpan sekali biar rumusnya ke-cache, baru dipakai lagi. …

Alasan skor DENGAN: Semua angka cocok persis dengan hitung ulang Python dan kunci: Semen Rp105.444.000 (45,2 % dari Rp233.556.000), lima kategori lain, jumlah transaksi per kategori 149/88/60/50/85/67, sembilan angka bulanan sampai rupiah, persen per bulan (−25,2; +42,6; +34,6; −10,7; +4,7; −45,6; +51,3; −4,6), Jan→Sep +5,5 %, Q2 Rp97.112.500 → Q3 Rp69.130.500, turun Rp27.982.000 (−28,8 %). Narasinya tepat ("fluktuatif, bukan tren lurus", penurunan Q3 didorong Juli). Sel bermasalah ditunjuk tepat (Q2 baris 68, Q3 baris 79 & 98) dengan saran perbaikan praktis (buka dan simpan sekali di Excel). Baris TOTAL tiap sheet dikeluarkan, kategori digabung, merge H4:H6 dikenali. Tabel tampil rapi sebagai blok monospace di Telegram. Kekurangan: (1) tidak menjelaskan kenapa baris TOTAL bawaan sheet Q1/Q3 (Rp66.633.000 / Rp68.786.500) lebih kecil dari hasilnya, padahal penyebabnya angka berupa teks; tim yang mencocokkan dengan file bisa bingung. (2) Retur Rp185.000 dan konversi angka teks diam-diam ikut dihitung tanpa disebut. (3) Tiga transaksi kosong (Rp409.000) dikeluarkan alih-alih dihitung dari qty × harga, tetapi hal ini terbuka disampaikan. (4) Kolom "Transaksi" Pipa (50) dan Alat (67) ikut menghitung baris yang nilainya tidak dijumlah. (5) Ada istilah teknis ("rumus SUM", "ke-cache", "sel gabungan merge H4:H6") dan "Sudah saya cek". Rincian: kebenaran 9,5, siap pakai 8,5, kepatuhan 8, perilaku 9, bahasa 7,5 → 8,5.
