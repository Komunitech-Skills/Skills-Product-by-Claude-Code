# Uji OpenClaw sebelum/sesudah — strategi-harga-produk

**Tanggal:** 2026-10-02  
**Penguji:** agent penguji independen Komunitech (bukan pembuat skill)

## Cara uji
- OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech (`komunitech` → `claude-sonnet-5`), sama dengan bot member.
- SEBELUM = home OpenClaw bersih tanpa skill; SESUDAH = home bersih berisi hanya skill `strategi-harga-produk`. Home dibuat ulang sebelum tiap skenario.
- Pesan identik di kedua sisi, satu giliran (agent tidak bertanya balik sehingga tidak ada jawaban lanjutan).
- Angka diverifikasi ulang dengan Python terpisah (bukan script skill); fakta aturan dicek terhadap aturan Indonesia yang berlaku.
- Catatan keamanan: tidak ada agent yang memasang paket, mengubah config (mtime openclaw.json tidak berubah), atau mencari ke seluruh disk. Catatan khusus per skenario di bawah.

## Skenario 1
**Pesan pengguna:**

> Kak saya jual sambal bawang botol 250ml harga 35rb, modal per botol 14.500. Mau buka reseller (minimal ambil 12 botol) sama agen (minimal 100 botol), terus bulan depan mau ikut flash sale 11.11 diskon 25%. Biaya tetap sebulan (sewa dapur + gaji 2 orang) 4,5jt, laku sekitar 500 botol sebulan. Harga reseller & agen bagusnya berapa? Diskon 25% masih untung ga?

### Balasan SEBELUM (tanpa skill) — tools: tidak ada

> Oke, saya hitungin ya. Modal 14.500, jual 35.000 → margin kotor Rp20.500/botol (58,6%). Lumayan sehat.
>
> **BEP (titik impas) biaya tetap**
> Fixed cost 4,5jt ÷ margin 20.500 = **~220 botol/bulan** buat nutup sewa + gaji. Di 500 botol/bulan (semua harga retail), profit bersih kira-kira:
> - Revenue 500×35.000 = 17.500.000
> - Modal 500×14.500 = 7.250.000
> - Gross profit 10.250.000 − fixed 4.500.000 = **profit ~Rp5.750.000/bulan**
>
> **Usul harga reseller & agen**
>
> - **Reseller (min 12 botol): Rp28.000/botol**
>   Margin kamu 13.500/botol (48%). Reseller jual lagi di 35.000 → untung Rp7.000/botol buat dia. Nilai minimal order cuma 336rb, gampang buat orang coba-coba jadi reseller.
>
> - **Agen (min 100 botol): Rp25.000/botol**
>   Margin kamu 10.500/botol (42%). Agen bisa jual retail (untung 10rb/botol) atau salurin ke reseller di 28rb (untung 3rb/botol). Minimal order jadi 2,5jt — wajar buat tier grosir besar.
>
> Jangan kasih di bawah 25rb ke agen, karena di situ margin kamu udah turun ke 42%, masih aman tapi jangan ditipisin lagi — nanti kalau kena ongkir/admin platform bisa minus.
>
> **Flash sale 11.11, diskon 25% — masih untung, tapi perhatikan ini:**
>
> - Diskon 25% dari harga **retail** (35.000 → 26.250): margin kamu jadi Rp11.750/botol (44,8%). Ini masih sehat.
> - **Yang bahaya:** kalau diskon 25% itu dihitung dari harga reseller/agen juga:
>   - Reseller 28.000 → 21.000: margin tinggal 6.500/botol (31%)
>   - Agen 25.000 → 18.750: margin tinggal 4.250/botol (22,7%) — ini udah mepet, kalau ada biaya admin/layanan marketplace (biasanya 2-8%) atau subsidi ongkir, bisa kepotong habis jadi hampir breakeven.
>   
>   **Saran: diskon 25% cuma buat harga retail/konsumen akhir. Reseller & agen tetap harga normal** (atau kasih insentif beda, misal bonus botol, bukan potong harga lagi).
>
> - Kalau ternyata SEMUA 500 botol bulan itu terjual di harga flash sale (26.250), bukan cuma sebagian:
>   - Revenue 13.125.000 − modal 7.250.000 = gross profit 5.875.000 − fixed 4.500.000 = **profit cuma Rp1.375.000** (turun drastis dari 5,75jt jadi 1,37jt)
>
>   Ini kuncinya: flash sale jangan dibiarin "membanjiri" seluruh volume bulanan. Kasih **kuota terbatas** (misal 50-100 botol aja buat harga flash sale), sisanya tetap jual normal/reseller/agen. Dengan begitu flash sale jadi tambahan omzet & exposure, bukan nguras margin bulanan.
>
> Satu lagi: kalau 11.11 ini lewat marketplace (Shopee/Tokopedia), cek dulu biaya admin + layanan + ongkir gratis yang biasanya dipotong di luar diskon — itu bisa nambah 5-10% potongan lagi dari harga jual, perlu dimasukin ke hitungan sebelum nentuin untung-ruginya final.

### Balasan SESUDAH (skill aktif) — tools: exec

> Oke, saya hitung semua angkanya pakai kalkulator pricing (bukan kira-kira). Ringkasnya:
>
> **Ringkasan**
> - Harga eceran Rp35.000 masih sehat — margin 58,57% (jauh di atas minimum makanan 40%).
> - Reseller (≥12 botol): **Rp29.750/botol** — agen (≥100 botol): **Rp26.250/botol**.
> - Diskon 25% flash sale 11.11: **masih untung**, margin turun ke 44,76% (masih di atas batas minimum 40%).
>
> **Asumsi**
> - Margin minimum dipakai 40% (standar produk makanan/minuman).
> - Jual langsung, tanpa potongan marketplace (0%).
> - Non-PKP (harga belum/tidak kena PPN).
>
> **Tabel harga**
>
> | Level | Min beli | Harga/botol | Diskon dari eceran | Laba kamu/botol | Margin | Untung reseller/botol | Status |
> |---|---|---|---|---|---|---|---|
> | Eceran | 1 | Rp35.000 | 0% | Rp20.500 | 58,57% | – | OK |
> | Reseller | ≥12 | Rp29.750 | 15% | Rp15.250 | 51,26% | Rp5.250 (15%) | OK |
> | Agen | ≥100 | Rp26.250 | 25% | Rp11.750 | 44,76% | Rp8.750 (25%) | OK |
>
> Catatan: harga anjuran jual-ulang reseller/agen tetap Rp35.000 (harga eceran toko). Kalau harga eceran naik nanti, harga reseller/agen di atas naik bersamaan — jangan dibiarkan beda sendiri.
>
> **BEP (titik impas) bulanan**
> - Biaya tetap Rp4.500.000/bulan, laba kontribusi Rp20.500/botol (di harga normal) → **BEP 220 botol/bulan**.
> - Jualan sekarang 500 botol → **laba ±Rp5.750.000/bulan**, batas aman penjualan boleh turun 56% sebelum rugi.
>
> **Diskon 25% flash sale 11.11 — masih untung?**
> - Harga promo: Rp35.000 → **Rp26.250**
> - Laba/botol turun dari Rp20.500 → **Rp11.750** (margin 44,76%, masih di atas minimum 40%) → **status OK, aman**
> - Batas diskon maksimal yang masih jaga margin 40% adalah **30,95%** — jadi diskon 25% kamu masih punya ruang ±6% sebelum kena batas bawah.
> - Supaya **laba kotor total** sama dengan bulan normal (Rp10.250.000 dari 500 botol), penjualan saat flash sale perlu naik jadi **minimal 873 botol** (naik 74,47%). Kalau nggak capai segitu, laba totalnya tetap positif tapi lebih kecil dari bulan normal — bukan rugi, cuma lebih tipis.
>
> **Langkah minggu ini**
> 1. Tetapkan harga reseller Rp29.750 (min 12 botol) dan agen Rp26.250 (min 100 botol), sampaikan harga eceran anjuran tetap Rp35.000.
> 2. Siapkan stok ekstra untuk flash sale — target jual minimal 873 botol di periode itu kalau mau laba totalnya setara bulan biasa; kalau nggak tercapai, tetap aman (masih untung, cuma lebih kecil).
> 3. Batasi kuota diskon 25% (misal jam tertentu / maks sekian botol per pembeli) biar nggak dipakai reseller/agen jadi harga beli ulang.
> 4. Cek stok modal cukup sebelum komit diskon — modal 873 botol ±Rp12,66jt (873 × Rp14.500).
> 5. Pantau penjualan harian selama flash sale, bandingkan dengan target 873 botol.
>
> **Teks siap tempel (WA daftar harga reseller/agen):**
> > 📋 *Harga Reseller & Agen Sambal Bawang 250ml*
> > - Eceran: Rp35.000
> > - Reseller (min. 12 botol): Rp29.750/botol
> > - Agen (min. 100 botol): Rp26.250/botol
> > Harga jual ke konsumen tetap Rp35.000 ya, biar nggak banting-bantingan harga 🙏
>
> Catatan: Angka dihitung dengan script dari data yang Anda berikan. Keputusan harga tetap di tangan Anda. Belum menghitung PPN karena diasumsikan non-PKP — kalau sudah PKP, kabari saya biar dihitung ulang dengan PPN-nya.

### Verifikasi
Python independen: laba/botol 35.000 − 14.500 = Rp20.500, margin 58,57%, markup 141,38%. BEP ⌈4.500.000 ÷ 20.500⌉ = 220 botol; laba 500 botol = Rp5.750.000; batas aman (500−220)/500 = 56%. Diskon 25% → Rp26.250, laba Rp11.750 (44,76%); agar laba kotor sama: 20.500/11.750 − 1 = 74,47% → ⌈500 × 20.500 ÷ 11.750⌉ = 873 botol. Lantai margin 40% = ⌈14.500 ÷ 0,6⌉ = Rp24.167 → diskon maks 1 − 24.167/35.000 = 30,95%. Reseller Rp29.750 → laba 15.250 (51,26%), agen Rp26.250 → 11.750 (44,76%). Modal 873 botol = Rp12.658.500.
- SEBELUM: semua angka benar (28.000 → 48,2%; 25.000 → 42%; skenario semua 500 botol di harga flash = laba Rp1.375.000 benar). Tidak memakai margin minimum eksplisit, tidak menghitung batas diskon maksimal atau volume yang dibutuhkan, tidak ada tabel/teks siap tempel. Nilai lebih: mengingatkan potongan marketplace saat 11.11 dan agar diskon tidak berlaku untuk reseller/agen.
- SESUDAH: script dipakai (`exec`), semua angka cocok dengan verifikasi. Kelemahan: (a) harga agen Rp26.250 **sama persis** dengan harga flash sale konsumen — konflik kanal tidak ditandai (agen akan merasa dirugikan); (b) flash sale 11.11 hampir selalu di marketplace, tetapi potongan marketplace hanya diasumsikan 0% tanpa ditanyakan; (c) untung reseller Rp5.250 (15%) cukup tipis untuk sambal.

### Skor
SEBELUM **7/10** — angka benar dan nasihat praktis bagus (potongan marketplace, kuota flash sale), tetapi tanpa batas diskon, target volume, tabel, maupun teks siap kirim.
SESUDAH **8/10** — lebih lengkap & siap pakai (tabel status OK, batas diskon 30,95%, target 873 botol, daftar harga WA, asumsi tertulis); dikurangi karena konflik harga agen = harga flash sale dan potongan marketplace 11.11 tidak ditanyakan. Skill terpakai (script dijalankan).

## Skenario 2
**Pesan pengguna:**

> Kak toko saya udah PKP. Jual hampers lebaran harga 189rb udah termasuk PPN, modal per hampers 110rb. Margin saya sebenernya berapa ya? PPN sekarang 12% kan, jadi tinggal dibagi 1,12 aja? Terus biar laku mau saya pasang harga coret 249rb biar keliatan diskon 24%, padahal sebelumnya gak pernah jual 249rb sih. Aman kan?

### Balasan SEBELUM (tanpa skill) — tools: tidak ada

> Oke, saya coba jawab dua-duanya kak — tapi dengan disclaimer: web search saya lagi mati (tool error), jadi angka PPN di bawah saya hitung manual pakai aturan yang saya tahu terakhir, bukan hasil cek live ke DJP. Untuk hal tax compliance kayak gini, sebaiknya tetap dikonfirmasi ke akuntan/konsultan pajak kakak ya, karena ini nyangkut Faktur Pajak resmi.
>
> **1. Soal PPN — koreksi dulu asumsinya**
>
> Tarif nominal PPN sekarang memang 12%, TAPI khusus barang/jasa yang bukan kategori "mewah" (dan hampers lebaran/makanan termasuk non-mewah), pemerintah pakai mekanisme DPP Nilai Lain: PPN efektif yang dikenakan ke konsumen = 11% dari harga jual, bukan 12%. Jadi cara baginya harusnya **dibagi 1,11, bukan 1,12**.
>
> Kalau dipakai yang benar (÷1,11):
> - Harga dasar (sebelum PPN) = 189.000 / 1,11 ≈ **Rp170.270**
> - PPN = 189.000 − 170.270 ≈ **Rp18.730**
> - Margin kotor = 170.270 − 110.000 modal = **Rp60.270/hampers**
> - Itu setara margin ≈ **31,9% dari harga jual**, atau ≈35,4% dari harga dasar.
>
> Kalau kakak pakai asumsi ÷1,12 (keliru):
> - Harga dasar = 168.750, PPN = 20.250, margin = 58.750
>
> Bedanya cuma ±Rp1.500/item, kelihatan kecil, tapi kalau salah terus dipakai buat bikin e-Faktur, PPN yang dilaporkan ke DJP jadi gak sesuai mekanisme yang berlaku → bisa bermasalah saat rekonsiliasi SPT. Karena aturan ini pernah direvisi beberapa kali, tolong double-check ke akuntan apakah skema 11%-efektif ini masih berlaku di 2026 atau sudah diganti full 12%. Saya gak bisa pastikan live sekarang.
>
> **2. Soal harga coret 249rb → coret → 189rb, padahal gak pernah dijual segitu**
>
> Gak aman kak, ini jangan dilakuin. Itu masuk kategori **diskon fiktif / informasi harga menyesatkan**, dilarang di UU No. 8/1999 tentang Perlindungan Konsumen (Pasal 9 & 10) — pelaku usaha dilarang menyatakan harga/potongan harga yang tidak sesuai fakta. Sanksinya bisa pidana (denda s.d. Rp2 miliar / penjara s.d. 5 tahun di Pasal 62), belum lagi risiko praktis:
> - Shopee/Tokopedia punya sistem deteksi harga coret — kalau ketahuan gak pernah dijual di harga itu, produk bisa di-takedown atau toko disuspend.
> - Kalau ada pembeli yang lapor/komplain dan ketahuan, reputasi toko kena, bisa viral negatif pas momen Lebaran yang justru lagi rawan sorotan.
>
> Alternatif yang legal dan tetap efektif buat jualan:
> - Kalau memang pernah dijual di harga lebih tinggi (misal pre-order awal musim), pakai harga itu sebagai harga coret yang sah.
> - Atau jangan klaim "harga normal", pakai framing lain: "Harga Spesial Lebaran", "Bundling Promo", "Harga Buka Puasa" — tanpa nyantumin angka harga lama yang fiktif.
> - Kalau mau kasih kesan diskon, kasih diskon riil kecil dari harga jual asli (misal 189rb → 179rb untuk 3 hari pertama), itu sah karena beneran terjadi.
>
> Singkatnya: margin kotor kakak di 189rb itu sekitar Rp60rb/hampers (≈32%) kalau PPN-nya dihitung yang benar, dan untuk strategi harga coretnya — skip, ganti pendekatan biar gak kena masalah hukum/marketplace pas lagi musim rame-rame jualan.

### Balasan SESUDAH (skill aktif) — tools: read, exec

> Oke, dua hal: margin aslinya, dan soal harga coret 249rb itu.
>
> **1. Margin hampers Rp189.000 (PKP, harga sudah termasuk PPN)**
>
> Dihitung dengan script (bukan manual dibagi 1,12 — itu kurang tepat untuk PPN 12% versi sekarang):
>
> - Harga tayang: Rp189.000 → dipecah jadi **DPP Rp170.271 + PPN Rp18.729**
> - Kenapa bukan dibagi 1,12: sejak PMK 131/2024, PPN 12% itu dikenakan atas **DPP nilai lain = 11/12 dari harga**, bukan harga dibagi 1,12 langsung. Efeknya hampir mirip (≈11% efektif), tapi caranya beda — kalau kamu asal bagi 1,12 dari depan, hasilnya sedikit meleset.
> - Modal: Rp110.000
> - **Laba kotor per hampers: Rp60.271**
> - **Margin (laba÷DPP): 35,4%** — ini di atas margin minimum 30%, jadi aman.
> - Markup (laba÷modal): 54,79% — beda ya dari margin, jangan dicampur kalau nanti cerita ke orang "untung 50%".
> - Harga terendah yang masih aman di margin minimum 30%: Rp174.428. Jadi Rp189.000 kamu masih ada ruang, gak mepet.
>
> **2. Soal harga coret Rp249.000 → "diskon 24%"**
>
> Matematikanya sendiri benar: (249.000-189.000)/249.000 = 24,1%. Tapi itu bukan yang jadi masalah.
>
> **Ini TIDAK aman** kalau Rp249.000 memang belum pernah jadi harga jual sebenarnya. Itu disebut **harga coret palsu / strikethrough fiktif** — mengaku ada diskon yang sebenarnya tidak pernah berlaku. Ini masuk kategori **menyesatkan konsumen** di bawah UU 8/1999 tentang Perlindungan Konsumen (soal informasi harga yang tidak benar/menyesatkan), bukan cuma soal "gak etis".
>
> Risikonya bukan cuma reputasi — kalau ada komplain pembeli atau laporan ke platform (banyak marketplace juga punya kebijakan sendiri soal ini dan bisa men-takedown listing atau kena sanksi internal mereka), toko kamu yang kena.
>
> **Alternatif yang tetap bisa bikin kelihatan "diskon" tanpa bohong:**
> - Jual beberapa hari/minggu di harga Rp249.000 dulu secara nyata (misal early bird, tapi harus benar2 ada orang yang beli di harga itu), baru nanti pasang coret saat harga turun ke Rp189.000. Ini butuh waktu, gak bisa instan.
> - Atau skip harga coret, pakai framing lain yang jujur: "Harga Spesial Lebaran", "Hemat vs beli satuan" (kalau hampers ini gabungan item satuan, bandingkan ke harga total item satuan asli — itu valid karena memang ada perbandingan nyata).
> - Atau diskon kuantitas/kuota: "10 box pertama Rp179.000" — real scarcity, bukan harga fiktif.
>
> Kalau mau, saya bisa bantu hitung opsi bundling/paket yang beneran bikin hemat tapi margin tetap aman (pakai `bundel` di skill harga), biar gak perlu pakai harga coret fiktif. Mau?

### Verifikasi
Python independen (aturan skill & PMK 131/2024: PPN 12% × DPP nilai lain 11/12 = efektif 11% untuk barang non-mewah, berlaku 1 Jan 2025): DPP bulat terbesar dengan DPP + ⌊11% × DPP⌋ ≤ 189.000 → DPP Rp170.271, PPN Rp18.729, sisa Rp0. Laba 170.271 − 110.000 = Rp60.271; margin terhadap DPP 35,40%; markup 54,79%. Bila salah bagi 1,12: DPP 168.750 (selisih ±Rp1.521). Harga tayang minimum margin 30% = DPP 157.143 → Rp174.428; margin 40% (default makanan) = DPP 183.334 → Rp203.500. Harga coret fiktif: UU 8/1999 Pasal 9 ayat (1) huruf a & Pasal 10 (pernyataan harga/potongan yang tidak benar), sanksi Pasal 62 ayat (1) penjara maks. 5 tahun/denda maks. Rp2 miliar — benar.
- SEBELUM: benar mengoreksi ke ÷1,11 (DPP ≈170.270), margin ≈Rp60.270 (35,4% dari DPP), menolak harga coret palsu dengan dasar UU 8/1999 yang tepat. Kelemahan: ragu "apakah skema 11% masih berlaku di 2026" tanpa menyebut PMK 131/2024, tidak ada harga minimum/lantai.
- SESUDAH: script dipakai, semua angka cocok, menyebut PMK 131/2024, margin vs markup dijelaskan, lantai Rp174.428. Kelemahan: (a) memakai margin minimum 30% tanpa menyebut asumsi; padahal hampers lebaran umumnya makanan dan default skill untuk makanan 40% → dengan 40% statusnya justru DI BAWAH MIN (lantai Rp203.500); (b) alternatif "jual dulu beberapa hari di Rp249.000 lalu coret" berisiko menjadi rekayasa harga acuan bila hanya formalitas — perlu syarat harga itu sungguh berlaku wajar.

### Skor
SEBELUM **7/10** — fakta pajak & hukum benar, tetapi ragu-ragu dan tanpa dasar aturan PPN.
SESUDAH **8,5/10** — angka PKP presisi (DPP/PPN rupiah bulat, sisa nol), dasar PMK 131/2024, lantai harga, penolakan harga coret palsu yang tepat + alternatif jujur. Dikurangi karena asumsi margin minimum 30% tidak disebut (hampers makanan seharusnya 40%). Skill terpakai (read + exec).

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---|---|
| 1. Tangga reseller/agen + flash sale 25% | 7 | 8 |
| 2. PKP hampers + jebakan ÷1,12 & harga coret palsu | 7 | 8,5 |
| **Rata-rata** | **7,0** | **8,25** |

**VERDIK: LULUS** — sesudah ≥ 8, lebih baik dari sebelum, tidak ada kesalahan angka/fakta (semua angka cocok dengan verifikasi Python independen). Catatan jujur: tanpa skill pun model sudah cukup baik (angka benar, menolak harga coret palsu); pembeda skill ada di presisi (DPP/PPN rupiah bulat, batas diskon maksimal, target volume), tabel status, dan teks siap tempel.

## Cacat untuk pembuat
1. **Konflik kanal tidak terdeteksi** — Skenario 1: agen Rp26.250 = harga flash sale konsumen Rp26.250. Saran: di langkah 6b/aturan promo, wajibkan cek "harga promo konsumen tidak boleh ≤ harga beli reseller/agen" (atau tambahkan PERHATIAN di `diskon` bila diberi `--harga-reseller`).
2. **Potongan marketplace saat event 11.11/Harbolnas tidak ditanyakan** — Skenario 1 diasumsikan 0%. Saran: bila pengguna menyebut flash sale/11.11/12.12/Harbolnas, anggap kanal marketplace dan tanyakan/beri asumsi `--biaya-persen` (rujuk harga-jual-marketplace), atau setidaknya beri PERHATIAN.
3. **Default margin minimum tidak konsisten** — Skenario 2 memakai 30% untuk hampers (umumnya makanan, default skill 40%) tanpa menyebut asumsi. Saran: perjelas bahwa hampers/parsel makanan = 40%, dan asumsi margin minimum wajib ditulis di bagian Asumsi.
4. **Alternatif harga coret** — saran "jual dulu di Rp249.000 beberapa hari" perlu syarat: harga tersebut benar-benar berlaku wajar (bukan formalitas singkat) agar tidak tetap menyesatkan. Tambahkan kalimat itu di `references/aturan-promo.md`.

## Cuplikan jualan
- Tanpa skill: "Harga dasar = 189.000 / 1,11 ≈ Rp170.270 … tolong double-check apakah skema 11% masih berlaku." — Dengan skill: "Rp189.000 → DPP Rp170.271 + PPN Rp18.729 (PMK 131/2024). Laba Rp60.271, margin 35,4%, markup 54,79%."
- Dengan skill: "Batas diskon maksimal yang masih jaga margin 40% adalah 30,95% … supaya laba sama, penjualan perlu minimal 873 botol." (tanpa skill tidak menghitung batas ini)
