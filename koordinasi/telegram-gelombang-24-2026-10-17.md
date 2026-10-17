# Gelombang Telegram 24 — 2026-10-17 (bot kedua)

Keputusan otomatis **104/106** (2026-10-17). Bot uji kedua `@KTclaude2bot` (OpenClaw 2026.10.2, model router Komunitech), grup uji internal Komunitech, topik baru 1955–1964. Pesan uji identik di sisi TANPA (topik `skills: []`) dan DENGAN skill; dikirim berurutan oleh bot penguji (rantai otomatis dua jalur, keputusan 93). Penilaian: satu penilai independen per skill + pemeriksa kedua yang berusaha membantah (angka dihitung ulang, kutipan dicocokkan ke id pesan); koreksi pemeriksa sudah diterapkan di tabel.

## Skor & verdik

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| buat-invoice (1.0.7) | 7,5 | 3,5 | −4 | **BELUM** (DENGAN < 8) | Dengan skill, bot menghitung angka yang sama persis dan menambah catatan meterai untuk kuitansi pelunasan, tetapi invoice lengkapnya tidak sampai ke chat dan file invoice gagal terkirim, sehingga pengguna hanya menerima ringkasan; tanpa skill, bot langsung memberi invoice lengkap siap kirim. |
| arus-kas-13minggu (1.0.5) | 4 | 8,5 | +4,5 | **LOLOS** | Dengan skill, AI tidak melewatkan satu tagihan pun, jadi menemukan kas minus Rp700.000 di minggu 3. Tanpa skill, AI melewatkan tagihan listrik 20 Okt dan menyimpulkan kas "aman". Sisi dengan skill juga memberi 4 pilihan jalan keluar yang saldonya sudah dihitung, plus tabel CSV terlampir untuk dibuka di Excel. |
| harga-jual-marketplace (1.0.6) | 6,5 | 8,5 | +2 | **LOLOS** | Hanya versi dengan skill yang ikut memotong PPh 22 marketplace 0,5% (Rp315) yang dipungut Shopee sejak 1 Oktober 2026 dan memberi harga balik modal Rp44.858. Tanpa skill, PPh 22 terlewat, sehingga untung di harga Rp55.400 tampak Rp9.502 padahal setelah dipotong pajak tinggal Rp9.225 (di bawah target 25% dari modal). |
| listing-marketplace (1.0.5) | 5 | 8,5 | +3,5 | **LOLOS** | Tanpa skill, AI cuma menulis satu deskripsi Shopee dengan tujuh klaim yang tidak pernah disebut pemilik (mis. "Tebal pas", "ga perlu obras ulang", "enak dipakein pashmina") dan menaruh harga di deskripsi. Dengan skill, AI memberi judul siap tempel untuk Shopee, Tokopedia, dan TikTok Shop yang masuk batas karakter (85/100, 69/70, 68/100), ditambah dua deskripsi yang hanya memakai fakta dari pemilik. |
| balas-ulasan-pelanggan (1.0.5) | 5 | 8,5 | +3,5 | **LOLOS** | Dengan skill, bot memberi balasan publik siap tempel yang muat batas aman 500 karakter (460 karakter, plus versi singkat 287), dan panjangnya sudah dicek. Balasan itu juga mengajak pembeli lanjut lewat Chat Toko, dan ada pesan pribadi untuk meminta nomor pesanan dan foto barang. Tanpa skill, balasannya cuma satu versi sepanjang 671 karakter (lewat batas aman) dan mengarang klaim "warna asli tetap sesuai spesifikasi". |

Pembanding uji internal (skor promosi / `examples/`):
- buat-invoice: 6,0 → 8,8 (1.0.5); skenario kuitansi diuji ulang 6 → 8,5 (1.0.7).
- arus-kas-13minggu: 6,75 → 8,4 (1.0.5).
- harga-jual-marketplace: 6,5 → 8,5 (1.0.4).
- listing-marketplace: 5,5 → 9,0 (1.0.4).
- balas-ulasan-pelanggan: 5,5 → 8,5 (1.0.4).

Beda terhadap uji internal:
- **buat-invoice:** Di uji internal dan pra-cek konteks Telegram 17 Okt, invoice lengkap tampil di balasan dan berkas HTML terlampir. Di bot asli, teks invoice ditulis sebagai pesan antara yang tidak dikirim gateway, dan lampiran HTML ditolak dua kali oleh pembatasan baca berkas (pra-cek tanpa pengiriman sungguhan tidak menangkap ini). Selain itu, skenario non-PKP ini tidak punya jebakan PPN, jadi sisi TANPA sudah benar dan selisih besar seperti di uji internal tidak muncul.
- **arus-kas-13minggu:** Di bot asli, sisi DENGAN sama tepatnya dengan uji internal (13/13 minggu cocok, minus Rp700.000 di minggu 3), CSV benar-benar terlampir, dan waktu ±4 menit (uji internal skenario pertama ±8 menit). Sisi TANPA di bot lebih buruk dari rata-rata internal 6,75: listrik 20 Okt terlewat sehingga kas disimpulkan aman, mirip uji Telegram internal yang melewatkan gaji 28 Okt.
- **harga-jual-marketplace:** Sisi DENGAN di bot memberi angka yang persis sama dengan uji internal (Rp44.858 / Rp63.000 / laba Rp15.875 / margin 25,2% / PPh 22 Rp315), dan blok catatan aturan tetap utuh di Telegram. Sisi TANPA di bot memakai tafsir 25% dari modal (Rp55.400) dan menawarkan alternatif Rp62.300, sedangkan di uji internal sisi TANPA langsung memilih Rp62.300 dengan klaim 'persis 25%'. Kelemahan utamanya tetap sama: PPh 22 tidak dihitung.
- **listing-marketplace:** Uji internal 1.0.4 memakai dua giliran (AI bertanya dulu) dengan judul lebih pendek (68/47/68). Di bot, kedua giliran digabung dalam satu pesan sehingga AI langsung bekerja, judul lebih panjang (85/69/68), deskripsi 594/333 karakter, dan semua angka tetap cocok hitung ulang. Sisi TANPA kembali menambah klaim karangan (7 butir, uji internal 6), sedangkan DENGAN sedikit lebih rendah (8,5 vs 9) karena nama alat cek dan penanda pengiriman ikut tampil di balasan.
- **balas-ulasan-pelanggan:** Hasil di bot sejalan dengan uji internal skenario toko (tanpa skill 6 → dengan skill 8,5). Tanpa skill kali ini lebih pendek (669 lawan 924 karakter) tetapi tetap lewat batas dan tetap mengarang fakta, sedangkan dengan skill panjangnya hampir sama (460/287 lawan 469/308). Di bot hanya skenario toko yang diuji, skenario klinik tidak, dan ini uji pertama versi 1.0.5 di bot asli.

Catatan jujur (untuk pembeli):
- **buat-invoice:** Di bot Telegram, invoice lengkap tidak tampil di chat (hanya ringkasan angka) dan file invoice gagal terlampir, padahal balasannya menyebut invoice "sudah ditulis di atas", sehingga pengguna perlu meminta ulang. Nomor, total, sisa tagihan, dan catatan meterai tetap benar.
- **arus-kas-13minggu:** Balasan butuh sekitar 4 menit. Pilihan "mundurkan pembayaran bahan 2 minggu" hanya menggeser tagihan sampai minggu 12 tanpa dijelaskan, dan alasan beberapa minggu di bawah batas aman dirangkum terlalu umum; cek rinciannya di tabel CSV sebelum bernegosiasi.
- **harga-jual-marketplace:** "Untung 25%" otomatis dihitung sebagai 25% dari harga jual, bukan dari modal. Bila maksud Anda 25% dari modal, harga cukup sekitar Rp56.000, jadi minta hitung ulang. Persentase biaya marketplace tetap harus Anda cocokkan sendiri dengan Seller Center.
- **listing-marketplace:** Deskripsi siap tempel masih berisi penanda "[isi: info pengiriman]" yang harus diisi atau dihapus sebelum tayang, dan kalimatnya agak berulang. Judul Tokopedia 69 dari batas 70 karakter sangat mepet, jadi cek ulang batas terbaru di Seller Center.
- **balas-ulasan-pelanggan:** Balasan publik sengaja tidak menanggapi keluhan admin yang lambat dan memuat kalimat "kami tetap pantau terus" yang belum tentu dilakukan toko, jadi pemilik sebaiknya menyesuaikannya sebelum memposting. Uji di bot ini hanya memakai satu ulasan Shopee bintang 1.

Salah angka/fakta yang ditemukan:
- buat-invoice: tidak ada
- arus-kas-13minggu: TANPA: tagihan listrik+gas Rp1,2 juta tanggal 20 Okt (minggu 1) terlewat, jadi ke-13 saldo kelebihan Rp1,2 juta. Minggu 3 ditulis +0,5 jt padahal −Rp700.000, sehingga kas disimpulkan 'aman'. Saldo akhir ditulis ~23,8 jt padahal Rp22.600.000. DENGAN: tidak ada salah angka/fakta. Hitung ulang Decimal: 13/13 saldo, masuk Rp139.000.000 / keluar Rp131.400.000, batas aman Rp10.107.692, tambahan dana Rp700.000 / Rp10.807.692, dan opsi 1–4 cocok. CSV terlampir; pelunasan di Januari, bukan Desember.
- harga-jual-marketplace: tidak ada
- listing-marketplace: tidak ada
- balas-ulasan-pelanggan: TANPA (msg 1989): 'warna asli tetap sesuai spesifikasi yang kami cantumkan' adalah klaim tanpa dasar. Pesan uji tidak menyebut spesifikasi, dan pemilik justru mengakui warnanya 'beda dikit'. Ini salah fakta, jadi sisi TANPA maks. 5 (sama dengan preseden G20 laporan-insiden-usaha).

Pemeriksa kedua:
- **buat-invoice:** setuju — Kedua kutipan cocok persis: 1966 di topik 1955 dan 1969 di topik 1956, keduanya dari KTclaude2bot. Topik 1956 hanya berisi 1968 ("Working") dan 1969. Transkrip sesi (ev/030) membuktikan teks invoice lengkap hanya ada di pesan antara yang tidak terkirim. Log gateway mencatat OutboundDeliveryError hostReadCapability 2× (11:42:45 dan 11:42:53); satu-satunya kiriman topik 1956 adalah sendMessage 1969,
- **arus-kas-13minggu:** koreksi — Skor, verdik LOLOS, salah_angka, dan pembeda cocok dengan hitung ulang Decimal saya: 13/13 saldo (18,3 … 22,6 jt), minggu 3 −700.000, masuk 139 jt / keluar 131,4 jt, net +7,6 jt, batas aman 10.107.692, tambahan 700.000 / 10.807.692, opsi 1–4 cocok (termin bawaan skrip menggeser bahan s.d. minggu 12, jadi 4,5 jt tertunda dan setelah dibayar 22,6 jt). TANPA (msg 1971) melewatkan listrik 20 Okt, jadi
- **harga-jual-marketplace:** setuju — Pesan 1977 (topik 1959) dan 1980 (topik 1960) dari KTclaude2bot ada, dan kutipannya cocok. Tabel hanya dirapikan, tidak membalik makna. Hitung ulang dengan Decimal cocok: 39.250÷0,875 → 44.858; 62.800 → 63.000; 5.040/2.520/315 → 53.875, laba 15.875, margin 25,198%. Sisi TANPA juga cocok: 55.397,7 → 55.400, potongan 7.898, untung 9.502; di 56.000 untung 26,39%; 62.301,6; dengan PPh 22 9.225 (24,28%
- **listing-marketplace:** setuju — Kedua balasan berasal dari KTclaude2bot: msg 1982 di topik 1961 dan msg 1987 di topik 1962. Kedua kutipan ditemukan berurutan dan maknanya tidak terbalik. Hitung ulang dengan Python len: judul 85/69/68 dan deskripsi 594/333, cocok dengan klaim. Entitas pre di pesan 595/334, selisih 1 karena baris baru penutup. Waktu balas cocok dengan sent-g2.jsonl: 14 dtk dan 118 dtk. Pembanding internal 1.0.4 (5
- **balas-ulasan-pelanggan:** koreksi — Kutipan dan message_id cocok: 1989 di topik 1963 dan 1992 di topik 1964, keduanya dari KTclaude2bot. Hitung ulang dengan rumus max(len, utf16): utama 460, alternatif 287, pesan pribadi 222. Data pribadi dan ajakan WA tidak ada. Yang perlu dikoreksi: penilai sendiri menyebut klaim "sesuai spesifikasi" di TANPA sebagai karangan. Menurut aturan, satu salah fakta membuat sisi itu maks. 5, jadi skor 5,

## Kutipan balasan (dipendekkan, `…` = dipotong)

### buat-invoice — TANPA (topik 1955, pesan 1966)

> Siap, ini invoicenya:
> 
> INVOICE
> No: INV/2026/10/0008
> Tanggal: 17 Oktober 2026
> Jatuh tempo: 24 Oktober 2026 (7 hari)
> 
> Dari: Dapur Bu Rini Catering
> Kepada: PT Kencana Fiktif Mandiri
> 
> Rincian:
> • Nasi box ayam bakar — 150 x Rp32.500 = Rp4.875.000
> • Snack box — 150 x Rp15.000 = Rp2.250.000, diskon 10% (−Rp225.000) = Rp2.025.000
> • Air mineral botol — 300 x Rp3.500 = Rp1.050.000
> • Ongkos kirim = Rp125.000
> 
> Subtotal: Rp8.075.000
> Keterangan: Non-PKP, tanpa PPN
> Total tagihan: Rp8.075.000
> DP (10 Okt 2026): −Rp3.000.000
> Sisa yang harus dibayar: Rp5.075.000
> …

Alasan skor TANPA: Invoice lengkap terkirim dalam satu pesan dan semua angkanya cocok dengan hitung ulang: nasi Rp4.875.000; snack Rp2.250.000 − diskon Rp225.000 = Rp2.025.000; air Rp1.050.000; ongkir Rp125.000; total Rp8.075.000; DP Rp3.000.000; sisa Rp5.075.000. Nomor INV/2026/10/0008, jatuh tempo 24 Okt 2026, dan tanpa PPN karena non-PKP. Rekening dan kalimat pelunasan siap kirim. Kekurangan: tidak ada terbilang, blok kota/penanda tangan, catatan meterai untuk pelunasan > Rp5 juta, maupun berkas (hanya menawarkan PDF/gambar). Label "Subtotal" sudah termasuk ongkir (labelnya longgar, angkanya benar). Ditutup satu pertanyaan.

### buat-invoice — DENGAN (topik 1956, pesan 1969)

> File HTML-nya gagal dilampirkan otomatis (ada pembatasan akses baca file di sisi sistem). Kalau mau saya coba kirim ulang, balas "kirim file".
> 
> Sementara itu, invoice lengkapnya sudah saya tulis di atas (angka sudah saya hitung otomatis, bisa langsung dipakai/disalin). Ringkasan untuk Bu Rini:
> 
> • No. INV/2026/10/0008 (lanjut dari 0007 ✓)
> • TOTAL Rp 8.075.000, sudah DP Rp3.000.000 → sisa tagihan Rp 5.075.000
> • Belum PKP → tidak ada PPN, sesuai permintaan
> • Kota & nama penanda tangan belum diisi — kabari kalau mau dicantumkan
> • Catatan: kalau nanti sisa Rp5.075.000 dilunasi sekaligus, kuitansi pelunasannya wajib pakai meterai Rp10.000 (karena di atas Rp5 juta)

Alasan skor DENGAN: Angka yang tampil benar: nomor 0008 lanjut dari 0007, total Rp8.075.000, DP Rp3.000.000, sisa Rp5.075.000, dan tanpa PPN. Catatan meterai Rp10.000 untuk pelunasan sekaligus juga tepat (5.075.000 > 5.000.000), dan ada pengingat kota/penanda tangan yang belum diisi. Namun yang sampai ke pengguna hanya "Working" dan satu pesan ringkasan. Tabel item, diskon, ongkir, rekening, jatuh tempo, dan terbilang tidak ada di chat, sehingga invoice tidak bisa dikirim ke klien. Kalimat "invoice lengkapnya sudah saya tulis di atas" menyesatkan karena di atasnya kosong. Berkas invoice gagal terlampir 2× (tidak ada sendDocument). Ada istilah teknis ("File HTML", "pembatasan akses baca file di sisi sistem"). Tawaran balas "kirim file" sesuai aturan, dan nama berkas/path internal tidak bocor.

### arus-kas-13minggu — TANPA (topik 1957, pesan 1971)

> Oke, aku hitung proyeksi arus kas mingguan (13 minggu) mulai Senin 19 Okt 2026 sampai Minggu 17 Jan 2027, pakai saldo awal 15 juta. … • Minggu 1 (19-25 Okt): 19,5 jt … • Minggu 3 (2-8 Nov) - beli mixer 15jt (3 Nov): 0,5 jt ⚠️ paling ketat … Kesimpulan: secara total 3 bulan ke depan kas kamu aman, malah naik dari 15 jt jadi ~23,8 jt. Tapi ada satu titik rawan: akhir minggu ke-3 (sekitar tanggal 3-8 November), saldo mepet banget cuma ~0,5 jt setelah beli mixer 15 juta. …

Alasan skor TANPA: Tabel 13 minggu rapi dan rentang tanggal benar (mulai Senin 19 Okt 2026). Namun tagihan listrik+gas 20 Okt terlewat, jadi semua saldo kelebihan Rp1,2 juta (minggu 1 ditulis 19,5 jt, seharusnya 18,3 jt; minggu 3 ditulis +0,5 jt, padahal −Rp700.000). Akibatnya pertanyaan utama "kas saya aman nggak?" dijawab "aman", dan ini keliru. Ada catatan bahwa kas "bisa sempat minus" di tengah minggu, tetapi tidak ada batas aman, tidak ada berkas, dan saran tanpa angka dampak. Ada salah angka, jadi skor maksimal 5.

### arus-kas-13minggu — DENGAN (topik 1958, pesan 1974, 1975; berkas: proyeksi-kas-13-minggu-kue.csv)

> Proyeksi Kas 13 Minggu — mulai Senin 19 Okt 2026 s/d 17 Jan 2027
> Saldo awal Rp 15.000.000 · Batas aman (asumsi rata-rata pengeluaran 1 minggu, belum Anda konfirmasi): Rp 10.107.692 … • Mg3 (2–8 Nov): 9.000.000 / 19.500.000 / -700.000 — 🔴 NEGATIF … Kas Anda sempat MINUS di minggu 3 (2–8 Nov), tekornya Rp 700.000 — penyebabnya mixer baru Rp 15.000.000 dan belanja bahan Rp 4.500.000 jatuh di minggu yang sama, sementara pemasukan cuma Rp 9.000.000. Arus kas 13 minggu: masuk Rp 139.000.000 vs keluar Rp 131.400.000 → naik Rp 7.600.000 (±Rp 584.615/minggu) … 1. Minta PT Cahaya Fiktif percepat 2 pembayaran (DP minggu 5→3, sisa minggu 13→11) — tawarkan diskon kecil. Hasil: tidak ada minggu minus, cuma minggu 2 masih di bawah batas (Rp 9.800.000), saldo akhir tetap Rp 22.600.000. … File Excel: proyeksi-kas-13-minggu-kue.csv (terlampir).

Alasan skor DENGAN: Angka-angka ini cocok dengan hitung ulang Decimal independen:
- masuk/keluar per minggu dan ke-13 saldo akhir
- batas aman Rp10.107.692 (rata-rata keluar 1 minggu, diberi label asumsi)
- minus Rp700.000 di minggu 3; minggu 2, 4, 11, 12 di bawah batas
- arus kas bersih +Rp7.600.000 (±Rp584.615/minggu)
- tambahan dana Rp700.000 / Rp10.807.692
- keempat opsi: DP dimajukan ke minggu 3 dan sisa ke minggu 11 (hanya minggu 2 di bawah batas); mixer digeser ke minggu 9; gabungan; termin bahan (minggu 3 Rp8.300.000, saldo setelah dibayar Rp22.600.000)

Hal lain yang benar: pelunasan hampers di minggu 13 (11–17 Jan), listrik 20 Jan di luar periode diingatkan, pajak/BPJS disebut belum termasuk, CSV benar-benar terlampir, dan ada kesimpulan tegas.

Kekurangan:
- Kalimat penyebab "minggu 2, 4, 11, 12 … karena gajian + sewa + bahan menumpuk" terlalu dipukul rata; di minggu 4 dan 12 tidak ada gajian/sewa.
- Opsi termin bahan hanya menggeser tagihan sampai minggu 12 tanpa dijelaskan. Nominal yang pindah tertulis Rp4,5 juta; bila semua tagihan mundur 2 minggu jumlahnya Rp9 juta, walau saldo setelah dibayar tetap Rp22,6 juta.
- CSV disebut "File Excel".
- Tidak ada contoh kalimat negosiasi.
- Balasan ±4 menit.

### harga-jual-marketplace — TANPA (topik 1959, pesan 1977)

> Rumusnya: Harga Jual = (Modal + Biaya Proses + Untung) / (1 − 8% − 4%)
> = (38.000 + 1.250 + 9.500) / 0,88
> = 48.750 / 0,88
> ≈ Rp55.400
> 
> Cek ulang kalau dijual Rp55.400: … Total potongan = Rp7.898
> • Diterima bersih = Rp47.502
> • Untung = Rp9.502 (≈25% dari modal) ✅
> 
> Saran: bulatkan jadi Rp55.500 atau Rp56.000 … Kalau mau "untung 25%" dihitung dari harga jual (bukan dari modal), hasilnya beda — sekitar Rp62.300.

Alasan skor TANPA: Hitungannya rapi dan benar menurut modelnya sendiri: (38.000 + 1.250 + 9.500) ÷ 0,88 = 55.397,7 → Rp55.400. Rinciannya: potongan Rp7.898, diterima Rp47.502, untung Rp9.502. Di harga Rp56.000 untung 26,4% dari modal, batas ongkir Rp10.000 baru berlaku di atas Rp250.000, dan tafsir 'untung dari harga jual' ≈ Rp62.300 juga benar. Jawaban ini juga menyebut dua tafsir 'untung 25%' dan menawarkan pilihan, perilaku yang baik. Kekurangannya, PPh 22 marketplace 0,5% (wajib dipungut kecuali ada surat pernyataan) tidak dihitung. Akibatnya tanda ✅ '≈25% dari modal' menyesatkan: setelah PPh 22 untung tinggal Rp9.225 (24,3%) dan target tidak tercapai. Tidak ada harga balik modal, dan tidak ada catatan agar persentase biaya dicek di Seller Center. Kekurangan ini kami anggap kelalaian model biaya, bukan salah hitung, sejalan dengan uji internal.

### harga-jual-marketplace — DENGAN (topik 1960, pesan 1980)

> Shopee – target margin 25%
> 
> • Harga minimal biar tidak rugi: Rp 44.858
> • Harga rekomendasi: Rp 63.000
> 
> | Harga tayang | Rp 63.000 |
> | Biaya admin/komisi (8%) | -Rp 5.040 |
> | Biaya layanan/ongkir (4%) | -Rp 2.520 |
> | Biaya per pesanan | -Rp 1.250 |
> | PPh 22 marketplace (0,5%) | -Rp 315 |
> | Uang diterima | Rp 53.875 |
> | Modal/HPP | -Rp 38.000 |
> | Laba bersih | Rp 15.875 (margin 25,2%) |
> 
> Status: MEMENUHI target margin 25% (margin 25,2%).
> … • PPh 22 marketplace 0,5% dari omzet (PMK 37/2025; dipungut Shopee, Tokopedia, Lazada, Blibli sejak 1 Oktober 2026). Kalau kakak orang pribadi dengan omzet setahun ≤ Rp500 juta dan sudah serahkan surat pernyataan ke Shopee, bisa dikecualikan … Alat bantu hitung, bukan nasihat pajak.

Alasan skor DENGAN: Semua angka benar dan konsisten: balik modal Rp44.858, rekomendasi Rp63.000, tabel komponen lengkap termasuk PPh 22 Rp315, diterima Rp53.875, laba Rp15.875, margin 25,2%. Baris status menyatakan target terpenuhi. Catatan aturan lengkap: PMK 37/2025, pemungut Shopee/Tokopedia/Lazada/Blibli sejak 1 Oktober 2026, pengecualian omzet ≤ Rp500 juta dengan surat pernyataan, 'berlaku per', dan 'bukan nasihat pajak'. Ada juga pengingat agar persentase biaya dicek di Seller Center, dan saran harga psikologis ditawarkan tanpa menyebut angka yang belum dihitung. Semuanya utuh di chat dan siap pakai. Nilai dikurangi karena tiga hal. Pertama, 'untung 25%' langsung ditafsirkan sebagai margin dari harga jual tanpa penjelasan bahasa awam dan tanpa menyebut tafsir '25% dari modal', yang cukup sekitar Rp56.000. Kedua, markup tidak ditampilkan meski diminta format skill, dan kata 'margin' agak teknis. Ketiga, tabel markdown dan tanggal format 2026-10-13 kurang ramah di Telegram.

### listing-marketplace — TANPA (topik 1961, pesan 1982)

> Siap, ini deskripsi produknya buat Shopee:
> 
> HIJAB VOAL MOTIF BUNGA PREMIUM - Rumah Hijab Nia
> 
> Hijab voal motif bunga yang adem dipakai seharian, gampang dibentuk, dan ga nerawang. Cocok buat daily outfit maupun acara santai.
> …
> • Tepi lasercut rapi, ga perlu obras ulang
> …
> • Adem & nyaman, ga bikin gerah
> • Bahan ga licin, enak dipakein pashmina/segiempat
> • Mudah dibentuk, hasil rapi tanpa ribet
> • Tebal pas, ga nerawang
> …
> 📌 Catatan: produk belum memiliki sertifikat.
> 
> 💰 Harga: Rp59.000 / pcs
> …

Alasan skor TANPA: Balasan langsung jadi (14 detik), rapi, dan siap tempel. Warna, ukuran, perawatan, dan isi 1 pcs sudah benar. Kelemahannya, ada tujuh klaim promosi yang tidak disebut pemilik:
(1) "Cocok buat daily outfit maupun acara santai"
(2) "Tepi lasercut rapi, ga perlu obras ulang"
(3) "ga bikin gerah"
(4) "enak dipakein pashmina/segiempat" (hijab 115x115 adalah segi empat, bukan pashmina)
(5) "hasil rapi tanpa ribet"
(6) "Tebal pas"
(7) "agar warna & kualitas kain awet"
Masalah lain:
- "Harga: Rp59.000 / pcs" ditaruh di deskripsi (jadi salah kalau harga berubah).
- Kalimat "produk belum memiliki sertifikat" ditulis di deskripsi, canggung dan merugikan penjualan.
- "Isi 1 pcs per order" membingungkan.
- Tidak ada judul terpisah dan tidak ada cek panjang karakter.
Tidak ada angka yang salah, tetapi banyak klaim karangan, sama seperti pola di uji internal (5,5). Nilai 5.

### listing-marketplace — DENGAN (topik 1962, pesan 1987)

> Semua lulus cek (panjang & klaim sesuai fakta). Ini hasilnya, siap tempel:
> …
> | Shopee      | Hijab Voal Motif Bunga 115x115 Premium Tepi Lasercut Adem Ga Nerawang Rumah Hijab Nia | 85/100             |
> | Tokopedia   | Hijab Voal Motif Bunga 115x115 Premium Tepi Lasercut Adem Ga Nerawang                 | 69/70              |
> | TikTok Shop | Hijab Voal Motif Bunga 115x115 Premium Tepi Lasercut Rumah Hijab Nia                  | 68/100             |
> 
> Deskripsi — Shopee & Tokopedia (594 karakter)
> 
> Hijab voal motif bunga dari Rumah Hijab Nia. Bahan adem, ga licin, gampang dibentuk, dan ga nerawang.
> …
> [isi: info pengiriman/kota asal pengiriman]
> …
> Deskripsi — TikTok Shop (333 karakter)
> …
> Script cek_listing.py (dengan --fakta dari teksmu) → LULUS untuk Shopee, Tokopedia, TikTok Shop.
> …
> • Harga 59rb tidak dimasukkan ke judul/deskripsi (itu diisi langsung di kolom harga Shopee)

Alasan skor DENGAN: Balasan langsung bekerja (118 detik) dan memberi lima hal: kata kunci (utama, pendukung, ekor panjang), judul tiga platform, deskripsi Shopee & Tokopedia, deskripsi TikTok Shop, serta daftar asumsi.

Hitung ulang Python len atas teks di balasan:
- Judul Shopee 85 (batas 100), Tokopedia 69 (batas 70), TikTok Shop 68 (batas 100 versi skill: 25–100). Ketiganya persis sama dengan klaim.
- Deskripsi Shopee & Tokopedia 594 dan TikTok 333, sama dengan klaim (blok teks tanpa baris baru penutup). Jauh di bawah batas 3.000/2.000.

Setiap butir sudah dicocokkan dengan fakta pemilik: voal premium, 115x115, tepi lasercut, motif bunga 4 warna, adem, ga licin, gampang dibentuk, ga nerawang, isi 1 pcs, cuci tangan tanpa pemutih. Tidak ada klaim tambahan. Harga sengaja tidak dimasukkan, sertifikat tidak diklaim, dan alasannya dijelaskan.

Potongan nilai:
- Balasan menampilkan kata proses/nama alat ("Semua lulus cek", "Script cek_listing.py (dengan --fakta dari teksmu)"), padahal pembeli awam tidak perlu melihatnya.
- Penanda "[isi: info pengiriman/kota asal pengiriman]" ada di dalam deskripsi siap tempel. Penanda ini harus diisi atau dihapus, padahal Shopee sudah menampilkan kota asal sendiri.
- Deskripsi agak berulang ("adem, ga licin, gampang dibentuk, ga nerawang" muncul 2–3 kali).
- Judul Tokopedia 69/70 sangat mepet.
Nilai 8,5.

### balas-ulasan-pelanggan — TANPA (topik 1963, pesan 1989)

> Halo Kak, mohon maaf atas ketidaknyamanannya 🙏 Kami sangat menyesal pengalaman belanjanya kurang memuaskan. Untuk keterlambatan 5 hari, itu di luar kendali kami karena proses pengiriman sudah di tangan pihak ekspedisi — tapi kami tetap minta maaf karena ini bikin Kakak menunggu lebih lama dari harapan. Soal warna, mohon dimaklumi perbedaan warna sedikit bisa terjadi karena pencahayaan saat pemotretan produk, warna asli tetap sesuai spesifikasi yang kami cantumkan. Untuk respon admin yang lambat, kami akan evaluasi lagi supaya pelayanan ke depan lebih cepat. …

Alasan skor TANPA: Balasannya sopan, menanggapi ketiga keluhan (telat, warna, admin lambat), menyebut ekspedisi dan cahaya foto sesuai permintaan pemilik, tanpa data pribadi dan tanpa janji kompensasi. Kekurangannya: isi balasan 669 karakter, lewat batas aman 500 untuk Shopee, jadi tidak bisa langsung ditempel. Ada klaim karangan "warna asli tetap sesuai spesifikasi yang kami cantumkan" padahal pemilik tidak pernah menyebut spesifikasi. "Mohon dimaklumi" terdengar agak membela diri. Tidak ada ajakan menyelesaikan lewat Chat Toko, tidak ada pesan pribadi untuk tindak lanjut, tidak ada versi alternatif, dan panjang balasan tidak dicek. "Kami akan evaluasi lagi" adalah janji tindakan yang ringan. Hasilnya layak sebagai draf, tetapi harus dipangkas dan dikoreksi sebelum diposting.

### balas-ulasan-pelanggan — DENGAN (topik 1964, pesan 1992)

> Balasan publik (utama)
> Kak, terima kasih sudah memberi tahu, dan mohon maaf atas pengalaman yang kurang nyaman ya. Untuk pengiriman, kami memakai jasa ekspedisi pihak ketiga sehingga waktu sampai kadang di luar kendali kami, tapi kami tetap pantau terus biar lebih cepat. Soal warna, perbedaan tampilan bisa muncul karena pencahayaan saat pemotretan produk. Mohon chat kami lewat Chat Toko ya Kak supaya respon lebih cepat dan bisa kami bantu lebih lanjut. Terima kasih masukannya 🙏
> Alternatif (lebih singkat)
> Mohon maaf atas ketidaknyamanannya Kak. Pengiriman memang lewat ekspedisi pihak ketiga jadi waktu sampainya di luar kendali kami langsung, …
> Hasil cek script: Lulus keduanya (shopee, negatif) — tidak ada data pribadi, tidak ada ajakan keluar platform, panjang aman (460 & 287 karakter dari batas 500).

Alasan skor DENGAN: Ada tiga hasil siap tempel: balasan publik utama 460 karakter, alternatif yang lebih singkat 287 karakter, dan pesan chat pribadi yang meminta nomor pesanan dan foto barang secara pribadi. Panjang balasan sudah dicek dan dilaporkan (lulus, ≤ 500, tanpa data pribadi, tanpa ajakan keluar platform), dan angkanya cocok dengan hitung ulang. Nadanya tidak defensif: minta maaf dulu, baru fakta ekspedisi dan cahaya foto disampaikan netral, sesuai permintaan pemilik. Pembeli diarahkan ke Chat Toko di dalam platform, bukan ke WA. Tidak ada kompensasi atau janji karangan, dan catatan untuk pemilik menjelaskan alasan setiap pilihan. Kekurangannya: (1) keluhan "admin slow respon" sengaja tidak ditanggapi di balasan publik, sehingga ajakan "chat kami supaya respon lebih cepat" bisa terasa janggal bagi pembaca; (2) "kami tetap pantau terus biar lebih cepat" adalah klaim tindakan yang belum dikonfirmasi pemilik; (3) muncul kata proses "Hasil cek script"; (4) tidak ada judul klasifikasi platform/bintang seperti format skill, dan tidak ada tawaran revisi di akhir.
