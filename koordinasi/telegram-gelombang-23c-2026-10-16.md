# Gelombang Telegram 23c — 2026-10-16 (bot kedua)

Keputusan otomatis **90/92/93** (2026-10-16). Bot uji kedua `@KTclaude2bot` (OpenClaw 2026.10.2, model router Komunitech), grup uji internal Komunitech, topik baru 1693–1695. Pesan uji identik di sisi TANPA (topik `skills: []`) dan DENGAN skill; dikirim berurutan oleh bot penguji (rantai otomatis dua jalur, keputusan 93). Penilaian: satu penilai independen per skill + pemeriksa kedua yang berusaha membantah (angka dihitung ulang, kutipan dicocokkan ke id pesan); koreksi pemeriksa sudah diterapkan di tabel.

## Skor & verdik

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| ekstrak-nota-faktur (1.0.5) | 4,5 | 8,5 | +4 | **LOLOS** | AI biasa menyatakan invoice CV Cetak Kilat "sudah cocok semua" dan file Excel-nya berisi rumus yang salah, sedangkan dengan skill bot menemukan PPN jasa cetak seharusnya Rp165.000 (bukan Rp180.000, kelebihan tagih Rp15.000) dan menyarankan bertanya ke penjual sebelum bayar, sambil langsung mengirim file rekapnya di chat. |
| iterasi-dari-masukan-pelanggan (1.0.12) | 5 | 8,5 | +3,5 | **LOLOS** | Hanya versi dengan skill yang menemukan bahwa 5 dari 7 keluhan pelanggan di WhatsApp (71,4%) sama sekali belum dibalas admin. Versi itu juga menyusun 3 perbaikan lengkap dengan penanggung jawab, tenggat, dan target berangka, plus 2 draf balasan untuk dikirim manual, tanpa menyebut nama pelanggan. Versi tanpa skill berhenti di daftar masalah dengan saran umum, tanpa persentase, penanggung jawab, tenggat, atau draf balasan, dan menyebut nama pelanggan satu per satu. |
| arsip-nota (1.0.7) | 7 | 8,5 | +1,5 | **LOLOS** | Dengan skill, bot lebih dulu menunjukkan rencana (nama file lama → nama baru di folder arsip/2026/09) dan baru menyalin setelah dijawab "ya". File asli tetap utuh dan foto dobel dilewati. Tanpa skill, bot langsung mengganti nama file asli dan memindahkan foto dobel tanpa bertanya. |

Pembanding uji internal (skor promosi / `examples/`):
- ekstrak-nota-faktur: 6,0 → 9,0 (1.0.4).
- iterasi-dari-masukan-pelanggan: 5,9 → 8,5 (1.0.11).
- arsip-nota: 5,75 → 8,75 (1.0.6).

Beda terhadap uji internal:
- **ekstrak-nota-faktur:** Temuan utamanya sama dengan uji internal: PPN Rp165.000 vs Rp180.000 dan selisih Nota 1 Rp10.000. Di bot asli, sisi TANPA lebih buruk (4,5 vs 6,0) karena file Excel-nya berisi rumus salah dan invoice dinyatakan cocok. Sisi DENGAN sedikit di bawah uji internal (8,5 vs 9,0) karena berkas di kanal chat berupa CSV per nota bukan .xlsx dengan rincian item.
- **iterasi-dari-masukan-pelanggan:** Di bot asli, versi revisi 1.0.12 mendapat skor yang sama dengan uji internal (8,5), dan selisihnya lebih besar (5 → 8,5). Semua angkanya kini benar, termasuk keluhan WA yang terlewat di uji bot sebelumnya. Sisi tanpa skill di bot menghitung jumlah pesan dengan benar (berbeda dari uji internal yang salah hitung 16 vs 13), tetapi tetap menyebut nama pelanggan dan ada satu salah fakta soal rating bintang.
- **arsip-nota:** Di uji internal, sisi tanpa skill salah membaca nominal ambigu "38.5" dan membuang file asli ke Trash, sehingga selisihnya 3,0. Di bot asli, sisi tanpa skill tidak salah angka (hanya mengganti nama file asli tanpa bertanya), jadi selisih menyempit ke 1,5. Perilaku sisi dengan skill konsisten (pratinjau → "ya" → salin, nota dobel ditahan) dengan skor 8,5 vs 8,75 di uji internal.

Catatan jujur (untuk pembeli):
- **ekstrak-nota-faktur:** File rekap yang dikirim berformat CSV (bisa dibuka di Excel), bukan .xlsx. Isinya satu baris per nota tanpa rincian barang, dan karena memakai pemisah titik koma, kolomnya bisa menumpuk jadi satu di Excel berbahasa Inggris atau aplikasi di HP. Kategori pengeluaran ditebak dari isi nota dan sebaiknya disesuaikan dengan pembukuan sendiri.
- **iterasi-dari-masukan-pelanggan:** Prioritas kemasan, porsi, dan harga ditulis "bulan ini" di tabel isu, tetapi di bagian backlog ditulis "dipantau bulan depan", jadi pemilik perlu memilih sendiri. Draf balasan masih umum (ada bagian [masalah] yang harus diisi), dan belum ada draf balasan publik untuk ulasan Shopee bintang rendah.
- **arsip-nota:** Perlu dua kali balas: bot menunjukkan rencana dulu, lalu menunggu jawaban "ya". Kategori ditebak dari nama penjual (semen masuk "Bahan baku") dan lokasi lengkap folder arsip di komputer tidak disebut di chat, jadi pembeli mungkin perlu menanyakannya atau mengoreksi kategorinya.

Salah angka/fakta yang ditemukan:
- ekstrak-nota-faktur: TANPA: menulis "Invoice CV Cetak Kilat sudah cocok semua" padahal PPN Rp180.000 = 12% × DPP penuh. Untuk jasa biasa (PMK 131/2024) PPN = 12% × 11/12 × Rp1.500.000 = Rp165.000, total Rp1.665.000, sehingga ada kelebihan tagih Rp15.000.; TANPA (isi berkas Rekap_Nota_Toko_Kue_Sep2026.xlsx): sel selisih Nota 2 berisi =I11−I12 dan merujuk sel kosong, jadi tampil −37.500 di samping "✓ COCOK". Di sheet Ringkasan, Total Hasil Cek Minimarket Berkah merujuk I11 (kosong) sehingga 0, dan total hasil cek menjadi Rp2.024.000 padahal seharusnya Rp2.061.500. Sheet faktur juga menyatakan "✓ SEMUA HITUNGAN COCOK" dengan PPN = DPP × 12%.
- iterasi-dari-masukan-pelanggan: TANPA: "Ada rambut di topping (WA - Sari, Shopee - Pembeli 7) dan ulat di sayur (Shopee - Pembeli 24). Semua jadi bintang 1" — keluhan rambut lewat WhatsApp (11/9) tidak punya rating bintang; hanya 2 ulasan Shopee (Pembeli 7 & 24) yang bintang 1. Selain itu, "Budi (pelanggan WA langganan)" tidak didukung data karena yang menulis "langganan terus" adalah pelanggan lain.
- arsip-nota: tidak ada

Pemeriksa kedua:
- **ekstrak-nota-faktur:** setuju — Pesan 1607/1608 (topik 1594) dan 1846/1847 (topik 1693) dari KTclaude2bot ada. Ukuran dokumennya cocok: xlsx 8.422 byte dan csv 677 byte. Salinan outbound identik (cmp) dengan berkas di workspace, CSV 28 kolom, dan SKILL.md di bot sama dengan 1.0.5. Hitung ulang Python: N1 344.000−334.000=10.000, N2 37.500, DPP nilai lain 1.375.000, PPN 165.000, total 1.665.000, beda 15.000, rekap 2.051.500, kateg
- **iterasi-dari-masukan-pelanggan:** koreksi — Kutipan dan ID pesan cocok: 1640 ada di topik 1598, sedangkan 1850–1852 ada di topik 1694, semuanya dari KTclaude2bot. Hitung ulang dengan Python cocok: 13 pesan WA, sentimen 4/2/7, 5 dari 7 keluhan tanpa balasan (71,4%), 3 dari 13 pesan dibalas (23,1%), 39 masukan, pengiriman 8 (20,5%), rata-rata bintang 1,83, Shopee 13/1/12, serta keamanan, kemasan, porsi, harga, rasa, dan layanan semuanya benar
- **arsip-nota:** setuju — Saya tidak menemukan alasan untuk membantah penilaian ini. Pesan 1614 (topik 1596) serta 1855 dan 1858 (topik 1695) berasal dari KTclaude2bot. Kutipannya cocok dan tidak membalik makna. Pesan 1854 dan 1857 hanya berisi "Working". Hitungan ulang: 1.250.000 + 150.000 + 487.500 = 1.887.500, dan 150rb = 150.000. Skor 8,5 − 7 = 1,5, jadi LOLOS sesuai aturan, tanpa salah angka. Di pesan 1855, bot member

## Kutipan balasan (dipendekkan, `…` = dipotong)

### ekstrak-nota-faktur — TANPA (topik 1594, pesan 1607, 1608)

> [berkas Rekap_Nota_Toko_Kue_Sep2026.xlsx] Rekap nota belanja toko kue — Sep 2026 ⚠️ Nota 1 (Toko Bahan Kue Sari) ada selisih Rp10.000 — cek lagi fisik notanya ya ✅ Nota 2 & Invoice CV Cetak Kilat sudah cocok semua / Sudah terkirim, Kak — file Excel rekapnya nongol di grup ya. Ada yang mau ditambahin atau dicek lagi dari nota-nota itu? [isi berkas, sheet Faktur Pajak:] PPN hasil hitung ulang (= DPP x 12%) … STATUS PEMERIKSAAN: ✓ SEMUA HITUNGAN COCOK (PPN & Total sesuai dengan invoice)

Alasan skor TANPA: Kelebihan: mengirim berkas .xlsx sungguhan (3 sheet dengan rincian per item) dan benar menandai selisih Nota 1 sebesar Rp10.000. Kekurangan: kesimpulan pajaknya keliru, karena PPN 12% penuh atas jasa cetak dinyatakan cocok sehingga kelebihan tagih Rp15.000 lolos. Isi berkas yang dibuka baca-saja (sama byte dengan salinan outbound 8.422 byte) memuat rumus yang salah rujuk: selisih Nota 2 −37.500 bertanda cocok, Ringkasan Minimarket 0, total hasil cek Rp2.024.000. Di chat tidak ada total atau rekap per kategori, tidak ada dasar aturan, dan tidak ada disclaimer. Respons sekitar 5,5 menit. Ada dua salah angka/fakta, jadi skor maksimal 5, dan saya beri 4,5.

### ekstrak-nota-faktur — DENGAN (topik 1693, pesan 1846, 1847; berkas: TANPA: Rekap_Nota_Toko_Kue_Sep2026.xlsx (8.422 byte, msg 1607), DENGAN: rekap-nota-kue.csv (677 byte, msg 1846))

> [berkas rekap-nota-kue.csv] Ini rekap nota belanja toko kue kakak dalam CSV (siap buka di Excel). / … N1 · 03-09-2026 · Toko Bahan Kue Sari · nota · Rp 334.000 (tunai) · ⚠️ Ada selisih … I1 · 08-09-2026 · CV Cetak Kilat (INV-0915) · invoice · Rp 1.680.000 · ⚠️ Perlu dicek … • N1: jumlah item Tepung+Gula+Mentega = 135.000+85.000+124.000 = Rp 344.000, tapi nota tulis TOTAL Rp 334.000 — selisih Rp 10.000. … • I1 (CV Cetak Kilat): PPN ditulis Rp 180.000 = 12% dari DPP penuh (Rp 1.500.000). Itu benar KALAU barang kena PPnBM (barang mewah) — tapi stiker label jelas bukan barang mewah. Untuk barang/jasa biasa sejak 2025, PPN seharusnya 12% × 11/12 × DPP = Rp 165.000, jadi total seharusnya Rp 1.665.000, bukan Rp 1.680.000 (beda Rp 15.000 lebih bayar). … sebaiknya tanyakan ke CV Cetak Kilat sebelum bayar … • Total: Rp 2.051.500 … Bahan baku Rp 334.000 · Bahan kemasan Rp 1.717.500 (N2 + I1) …

Alasan skor DENGAN: Semua angka cocok dengan hitung ulang Python: N1 135.000+85.000+124.000 = 344.000 vs tertulis 334.000 (selisih 10.000); N2 3×12.500 = 37.500 cocok; I1 DPP nilai lain 1.375.000, PPN 165.000, total seharusnya 1.665.000, beda 15.000; terbilang cocok dengan 1.680.000; rekap 2.051.500; kategori 334.000 / 1.717.500. Isi CSV yang terkirim identik dengan salinan di folder kerja dan memuat angka yang sama. Temuan PPN disampaikan sebagai "tanyakan ke penjual, jangan dituduh". Format chat rapi (satu baris per dokumen, tanpa tabel Markdown), tidak menyebut jalur atau folder, dan mencantumkan dasar aturan serta Kring Pajak 1500200. Respons sekitar 1,5 menit. Kekurangan: pengguna minta "ke Excel" tetapi yang dikirim CSV, bukan .xlsx. Isinya satu baris per nota tanpa rincian item, 28 kolom yang sebagian besar kosong, dan pemisah ";" bisa tidak terbagi kolom di Excel berbahasa Inggris atau aplikasi HP. Kalimat "PMK 131/2024 (berlaku per 23 Sep 2026)" bisa terbaca seolah aturan baru berlaku tanggal itu, padahal maksudnya status per tanggal tersebut (aturannya berlaku sejak 2025, dan balasan sendiri menulis "sejak 2025"), jadi tidak saya hitung sebagai salah fakta. Kategori "Bahan kemasan" untuk stiker label hanya tebakan, tetapi disebut terang sebagai tebakan.

### iterasi-dari-masukan-pelanggan — TANPA (topik 1598, pesan 1640)

> Udah saya baca semua — 18 chat WA + 26 ulasan Shopee bulan September. Ini ringkasannya, diurutkan dari yang paling perlu dibenahi duluan:
> 
> 1. Higiene dapur & packing — paling urgent walau kejadiannya cuma 3x
> Ada rambut di topping (WA - Sari, Shopee - Pembeli 7) dan ulat di sayur (Shopee - Pembeli 24). Semua jadi bintang 1 dengan komentar "jijik", "tidak akan beli lagi". …
> 
> 2. Kurir/pengiriman telat — paling sering muncul
> 5 dari 11 ulasan bintang rendah di Shopee soal telat (sampe 90 menit–2 jam), ditambah 2 keluhan serupa di WA dari Budi. …

Alasan skor TANPA: Sebagian besar hitungan benar: 18 chat dan 26 ulasan, 5 dari 11 ulasan Shopee bintang 1–2 soal telat ditambah 2 keluhan telat di WA, kemasan 2 Shopee + 1 WA, serta 2 kasus akurasi pesanan. Urutannya juga masuk akal: kebersihan dulu, lalu pengiriman. Kekurangannya:
- Ada salah fakta "Semua jadi bintang 1", padahal keluhan WA tidak berbintang, ditambah klaim langganan yang tidak didukung data. Karena itu skor maks 5.
- Nama pelanggan disebut (Sari, Budi, Rahmat, Dewi Lestari lengkap), jadi privasi bocor.
- Tidak menangkap temuan terpenting, yaitu keluhan WA yang tidak dibalas admin.
- Tidak ada persentase, tabel isu, backlog berpenanggung jawab, tenggat, atau ukuran keberhasilan.
- Tidak ada draf balasan ke pelanggan.
Hasilnya ringkas dan mudah dibaca, tetapi masih berupa saran umum, belum rencana kerja.

### iterasi-dari-masukan-pelanggan — DENGAN (topik 1694, pesan 1850, 1851, 1852)

> Udah saya baca semuanya ya kak — chat WA September (18 pesan, 3 balasan admin saya skip) + 26 ulasan Shopee, saya proses pakai alat analisis masukan pelanggan terus saya cek satu-satu manual biar nggak salah baca. Total 39 masukan nyata dari pelanggan (Shopee 26, WA 13).
> 
> Ringkasan cepat — 3 hal berangka + 1 tindakan minggu ini
> 
> • 71,4% keluhan di WA (5 dari 7) sama sekali nggak dibalas admin — ini yang paling genting, bukan soal produk tapi soal respons.
> • Pengiriman telat = keluhan #1: 8 dari 39 masukan (20,5%), muncul di Shopee DAN WA, rata-rata bintang pelanggan yang komplain cuma 1,8.
> • Ada 3 laporan keamanan pangan (rambut 2x, ulat 1x) — kecil jumlahnya tapi dampaknya tertinggi, wajib Segera.
> • Tindakan minggu ini: bikin jadwal cek & balas chat WA minimal 2-3x sehari (pagi/siang/sore), terutama yang nada komplain.
> …

Alasan skor DENGAN: Semua angka benar menurut hitungan ulang penilai dengan Python:
- 39 masukan = 26 ulasan Shopee + 13 pesan WA. Ke-13 pesan WA = 18 baris − 3 pesan admin − 1 media − 1 "Pesan ini dihapus".
- Sentimen WA 4/2/7.
- Keluhan WA tanpa balasan 5 dari 7 = 71,4%. Pesan WA yang dibalas 3 dari 13 = 23%.
- Pengiriman 8/39 = 20,5% (6 Shopee + 2 WA). Rata-rata bintang ulasan telat 1,83.
- Keamanan 3 (rambut 2, ulat 1; label terpisah) dengan skor 15 = 3×5. Pengiriman skor 24 = 8×3.
- Kemasan, porsi, dan harga masing-masing 3 (7,7%). Kemasan dihitung setelah koreksi kata "kotak/box" yang benar.
- Ketepatan pesanan 2. Rasa 2 keluhan dan 12 pujian dari 14. Pujian layanan 3.
- Sentimen Shopee 13/1/12 konsisten dengan koreksi ulasan bintang 3 soal porsi.

Satu-satunya permintaan menu (varian tanpa telur) masuk Saran, lengkap dengan masalah di baliknya dan uji murah 10–20 porsi.

Kelebihan lain: tanpa nama pelanggan, keamanan pangan ditandai Segera, backlog 3 butir dengan Siapa/Tenggat/Ukuran berangka, ada catatan bias kanal dan data 1 bulan, serta 2 draf balasan untuk dikirim manual.

Nilai dikurangi karena:
- Kemasan, porsi, dan harga diberi prioritas "Bulan ini" di tabel, tetapi di bawahnya ditulis "dipantau bulan depan".
- Draf balasan masih umum (ada isian [masalah]).
- Tidak ada draf balasan publik untuk ulasan Shopee bintang rendah, juga tidak ada rencana bulan depan dengan pertanyaan survei.
- Dua kutipan pujian diparafrasekan tetapi diberi tanda kutip.
- "Rata-rata bintang 1,8" tidak menyebut bahwa itu hanya dari Shopee.
- Ada sedikit kata proses ("alat analisis", "cek satu-satu manual").

### arsip-nota — TANPA (topik 1596, pesan 1614)

> Selesai dirapiin! 📁 File yang direname (format: Tanggal_Penjual_Keterangan_Nominal): • 2026-09-20_Toko-Bangunan-Sinar-Jaya_Semen_Rp1.250.000.jpg • 2026-09-22_SPBU-Pertamina_Bensin_Rp150.000.jpg • 2026-09-25_PLN_Tagihan-Listrik_Rp487.500.pdf File IMG_20260920_101 (1).jpg saya cek hash-nya — memang identik 100% sama nota Sinar Jaya yang pertama, jadi saya pindah ke nota/duplikat/ biar nggak dobel kehitung. … | Material/Bangunan | Rp 1.250.000 | … | TOTAL | Rp 1.887.500 | Rekap lengkap + rincian per nota saya simpan di rekap-pengeluaran-sept2026-nota.csv di root workspace.

Alasan skor TANPA: Selesai dalam satu giliran (±1,5 menit) dan angkanya benar semua. Nama baru rapi (tanggal_penjual_keterangan_nominal), foto dobel dikenali dari isi file lalu dipindah ke nota/duplikat/ (tidak dihapus). Kategori pas (Material/Bangunan, Transportasi/BBM, Utilitas/Listrik) dan total Rp1.887.500 benar. Minus: (1) Nama file asli di nota/ langsung diganti tanpa pratinjau atau persetujuan, dan foto dobel dipindah tanpa ditanya. (2) Pemetaan nama lama → nama baru tidak ditulis jelas. (3) Tidak ada susunan folder per bulan atau catatan yang bisa dicari ulang. (4) Ada istilah teknis "hash", "direname", dan "root workspace", dan lokasi berkas CSV tidak bisa dipahami atau dibuka pengguna Telegram. (5) Tabelnya markdown mentah, jadi tampil sebagai garis tegak di Telegram.

### arsip-nota — DENGAN (topik 1695, pesan 1855, 1858)

> [giliran 1] Sudah saya cek, ini pratinjau 4 notanya (belum ada yang disalin/tersimpan): 1. Toko Bangunan Sinar Jaya Dari: IMG_20260920_101.jpg Ke: arsip/2026/09/2026-09-20_Toko-Bangunan-Sinar-Jaya_1250000.jpg (disalin) Tanggal 20/09/2026 | Rp 1.250.000 | Kategori: Bahan baku (tebakan) … 4. IMG_20260920_101 (1).jpg Isinya memang identik (hash sama persis) dengan nota #1 … Lanjutkan simpan nota 1-3 (dan skip nota 4 karena dobel)? Balas "ya" untuk lanjut. [giliran 2, setelah "ya"] Sudah, 3 nota tersimpan di arsip (nota #4 dilewati karena memang dobel dengan nota #1): … REKAP PENGELUARAN SEPTEMBER 2026 Jumlah nota: 3 | Total: Rp 1.887.500 Per kategori: • Bahan baku: 1 nota, Rp 1.250.000 • Listrik/air/internet: 1 nota, Rp 487.500 • Transportasi: 1 nota, Rp 150.000 File asli tetap ada di folder nota/, yang disimpan di arsip adalah salinannya.

Alasan skor DENGAN: Giliran 1 (±1 menit) berisi pratinjau 4 nota. Tiap nota diberi "Dari → Ke" yang jelas ke arsip/2026/09/ dengan nama baku sesuai aturan skill (2026-09-20_Toko-Bangunan-Sinar-Jaya_1250000.jpg, 2026-09-22_SPBU-Pertamina_150000.jpg, 2026-09-25_PLN_487500.pdf), bertanda "(disalin)", kategori diberi label "(tebakan)", dan ada penegasan bahwa belum ada yang disalin. Nota #4 dikonfirmasi identik dari isi file dan diusulkan dilewati. Bot menutup dengan satu pertanyaan "Balas ya". Giliran 2 setelah "ya": 3 nota tersimpan, nota dobel dilewati, rekap per kategori rapi dan benar (Rp1.887.500), dan ada pengingat bahwa file asli tetap di nota/ (yang diarsip adalah salinan), lalu tawaran CSV/buku kas. Tidak ada lagi nama skill lain, jalur ~/KomunitechData, atau kata "script" seperti di G18. Minus: (1) Butuh dua giliran. (2) Semen ditebak "Bahan baku", kurang pas dibanding "Material/Bangunan" di sisi TANPA. (3) Lokasi lengkap folder arsip di komputer tidak disebut, hanya "arsip/2026/09/…". (4) Masih ada istilah "hash", "skip", dan "sistem bakal menolaknya otomatis". Bukti hanya dari balasan bot; isi folder tidak diperiksa penilai.
