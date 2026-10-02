# Uji OpenClaw sebelum/sesudah — strategi-harga-produk

**Tanggal:** 2026-10-02 (uji ulang, versi skill 1.0.5)  
**Penguji:** agent penguji independen Komunitech (bukan pembuat skill)

## Riwayat
Uji pertama 2026-10-02 pada versi sebelum perbaikan: rata-rata SEBELUM 7,0 → SESUDAH 8,25, verdik **LULUS** dengan catatan. Cacat yang ditemukan: (1) harga agen Rp26.250 sama persis dengan harga flash sale konsumen tanpa peringatan konflik kanal; (2) potongan marketplace saat 11.11 diasumsikan 0% diam-diam; (3) hampers makanan dinilai dengan margin minimum 30% tanpa menyebut asumsi (seharusnya default pangan 40%); (4) saran "jual dulu di harga coret beberapa hari" tanpa syarat harga itu berlaku wajar. Setelah perbaikan pembuat, kedua skenario dijalankan ulang di bawah dengan pesan identik.

## Cara uji (uji ulang 2026-10-02)
- OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech (`komunitech` → `claude-sonnet-5`), sama dengan bot member.
- SEBELUM = home OpenClaw bersih tanpa skill; SESUDAH = home bersih berisi hanya skill `strategi-harga-produk` 1.0.5. Home dibuat ulang sebelum tiap skenario.
- Pesan identik dengan uji pertama, identik di kedua sisi, satu giliran (agent tidak bertanya balik).
- Angka diverifikasi ulang dengan Python terpisah (bukan script skill); fakta aturan dicek terhadap aturan Indonesia yang berlaku.
- Catatan keamanan: tidak ada agent yang memasang paket, mengubah config, menawarkan kirim/posting otomatis, atau mencari ke seluruh disk. Di Skenario 2 sisi SEBELUM mencoba `tool_search` (mencari alat web), tanpa efek samping.

## Skenario 1 — tangga reseller/agen + flash sale 11.11
**Pesan pengguna:**

> Kak saya jual sambal bawang botol 250ml harga 35rb, modal per botol 14.500. Mau buka reseller (minimal ambil 12 botol) sama agen (minimal 100 botol), terus bulan depan mau ikut flash sale 11.11 diskon 25%. Biaya tetap sebulan (sewa dapur + gaji 2 orang) 4,5jt, laku sekitar 500 botol sebulan. Harga reseller & agen bagusnya berapa? Diskon 25% masih untung ga?

### Balasan SEBELUM (tanpa skill) — tools: tidak ada

> Oke, saya hitung berdasarkan angka yang dikasih. Modal 14.500, jual normal 35.000 → margin dasar lo **20.500/botol (58,6%)**. Ini basis buat nentuin tier.
>
> ## Rekomendasi Harga Reseller & Agen
>
> | Tier | Min order | Harga/botol | Diskon dari retail | Margin lo | Margin partner (kalau dijual 35rb) |
> |---|---|---|---|---|---|
> | Retail (konsumen) | 1 | 35.000 | - | 20.500 (58,6%) | - |
> | **Reseller** | 12 botol | **28.000** | 20% | 13.500 (48,2%) | 7.000/botol (ROI 25%) |
> | **Agen** | 100 botol | **25.000** | 28,6% | 10.500 (42%) | 10.000/botol kalau jual retail |
>
> Logikanya: makin besar komitmen volume, makin tipis % margin lo, tapi partner tetap dapet insentif jelas buat naik kelas dari reseller ke agen. Agen jual 25rb vs reseller 28rb — ada gap 3rb yang masuk akal buat alasan "kenapa harus ambil 100 botol".
>
> Margin lo di semua tier masih di atas **Rp 9.000/botol** — itu angka breakeven per botol lo kalau based on 500 botol/bulan ÷ fixed cost 4,5jt. Jadi bahkan skenario terburuk (semua laku lewat agen) masih untung tipis, bukan rugi.
>
> ## Flash sale 25% — masih untung?
>
> 25% dari 35.000 = **26.250/botol**. Margin lo: 26.250 − 14.500 = **Rp 11.750/botol (44,8%, atau 81% dari modal)**. Masih jauh di atas breakeven 9.000/botol → **ya, masih untung per unit**, bahkan setelah potong estimasi fee marketplace (komisi+payment gateway ~5-8%, sisa margin masih ±8.000-9.500/botol).
>
> Dua catatan penting:
>
> 1. **Cek apakah flash sale itu menambah volume atau cuma "mindahin" penjualan normal.** Kalau 500 botol/bulan lo udah nutup fixed cost + untung dari mix retail/reseller/agen, flash sale yang menarik pembeli BARU itu untung murni (11.750 × qty, nyaris tanpa beban fixed cost tambahan). Tapi kalau pembeli yang harusnya beli normal 35rb pindah ke flash sale 26,25rb, lo kehilangan selisih 8.750/botol — itu bukan rugi, tapi opportunity cost.
> 2. **Harga flash sale 26.250 lebih murah dari harga reseller lo (28.000).** Ini masalah channel conflict — reseller bakal protes karena modal mereka beli ke lo (28rb) lebih mahal dari harga konsumen pas flash sale. Saran: batasi kuota flash sale (misal max 50-100 botol), atau kasih reseller/agen harga khusus event juga (misal reseller dapat ekstra diskon pas 11.11) biar mereka nggak ngerasa dilangkahin.
>
> **Ringkasnya:** struktur harga ini (28rb reseller / 25rb agen) sehat, dan diskon 25% flash sale masih profitable per botol. Yang perlu lo jaga cuma dua hal — jangan sampai flash sale bikin reseller kabur, dan pastikan itu nambah penjualan, bukan cuma geser penjualan normal ke harga lebih murah.

### Balasan SESUDAH (skill aktif) — tools: read, exec

> # Sambal Bawang 250ml — Harga Reseller/Agen + Cek Diskon 11.11
>
> **Ringkasan:**
> - Harga ecer Rp35.000 **sudah sehat** (margin 58,57%, jauh di atas minimum pangan 40%).
> - Reseller (≥12 botol): **Rp30.000/botol**. Agen (≥100 botol): **Rp24.500/botol**.
> - Diskon 25% di flash sale 11.11 **masih untung per botol** — TAPI ada 2 jebakan: (1) kalau lewat marketplace, potongan platform bisa bikin margin jatuh di bawah batas aman; (2) harga promo lebih murah dari harga beli reseller, jadi reseller/agen bisa merasa dirugikan.
>
> ## Asumsi
> - Margin minimum dipakai: **40%** (default kategori pangan — makanan/minuman/sambal).
> - Status PKP: dianggap **bukan PKP**, jadi harga di atas belum termasuk PPN.
> - Potongan kanal: jual langsung = 0%. Kalau 11.11 lewat marketplace (Shopee/Tokopedia dsb), saya **asumsikan potongan 10%** dari harga jual (perkiraan kasar, belum dicek) — cek angka pastinya dengan skill `harga-jual-marketplace` sebelum ikut event.
> - HPP Rp14.500/botol — anggap angka pasti dari Kakak.
>
> ## Tabel Harga Reseller & Agen
> | Level | Minimal beli | Harga/botol | Diskon dari ecer | Laba kita/botol | Margin kita | Untung reseller/botol | Status |
> |---|---|---|---|---|---|---|---|
> | Reseller | ≥ 12 | Rp30.000 | 14,29% | Rp15.500 | 51,67% | Rp5.000 (14,29%) | OK |
> | Agen | ≥ 100 | Rp24.500 | 30% | Rp10.000 | 40,82% | Rp10.500 (30%) | OK |
>
> Harga ecer anjuran untuk reseller = Rp35.000 (sama dengan harga toko sekarang). Kalau nanti harga ecer dinaikkan, harga reseller/agen di atas harus diupdate bersamaan.
>
> BEP sekarang: **220 botol/bulan** (omzet Rp7.700.000). Penjualan 500 botol/bulan → laba kotor ±**Rp5.750.000/bulan**, batas aman (margin of safety) 56% — artinya penjualan boleh anjlok sampai 56% sebelum rugi. Cukup sehat.
>
> ## Diskon 25% Flash Sale 11.11 — Masih Untung?
>
> **Skenario A — Jual langsung (WA/toko sendiri), tanpa potongan platform:**
> - Harga promo: Rp26.250 → laba Rp11.750/botol (margin **44,76%**, masih di atas batas minimum 40%) → **status OK per unit**.
> - Tapi untuk balik ke laba kotor sebulan normal (Rp10.250.000), penjualan harus naik **74,47%** (500 → minimal **873 botol**) dalam periode promo itu — target cukup berat kalau dipaksakan sebulan penuh.
> - Batas diskon maksimal aman: **30,95%** (harga terendah Rp24.167). Jadi 25% masih di dalam batas aman.
>
> **Skenario B — Lewat marketplace, asumsi potongan 10%:**
> - Harga promo tetap Rp26.250, tapi laba toko tinggal Rp9.125/botol, margin **34,76% — DI BAWAH minimum 40%** ⚠️
> - Diskon maksimal aman di kanal ini cuma **17,14%** (harga Rp29.000).
> - Kalau Kakak tetap mau diskon 25% di marketplace, laba per botol memang tipis — perlu dicek ulang potongan asli platform (bisa lebih dari 10%).
>
> **⚠️ PERHATIAN — Konflik kanal:** di kedua skenario, harga promo Rp26.250 **lebih murah dari harga beli Reseller (Rp30.000)**. Reseller bisa merasa dirugikan (pembeli biasa dapat harga lebih murah dari reseller) atau malah memborong stok promo untuk dijual ulang.
>
> **Solusi pilih salah satu:**
> 1. Batasi maks beli **2 botol/pembeli** selama flash sale (standar e-commerce, otomatis cegah reseller "belanja grosir" via promo).
> 2. Beri reseller/agen harga khusus/kompensasi selama periode promo tersebut.
> 3. Kecilkan diskon konsumen jadi di kisaran 15–17% kalau mau lewat marketplace (harga promo tetap di atas Rp30.000 = aman dari konflik reseller).
>
> ## Langkah Minggu Ini
> 1. Tetapkan harga ecer Rp35.000, reseller Rp30.000 (≥12 botol), agen Rp24.500 (≥100 botol) — sudah dihitung aman.
> 2. Pastikan dulu **flash sale 11.11 lewat kanal mana** (lapak sendiri vs marketplace) — ini menentukan apakah diskon 25% masih aman atau perlu diturunkan ke ±17%.
> 3. Kalau lewat marketplace, cek potongan asli platform dulu (jangan pakai asumsi 10% saya) sebelum fix harga promo.
> 4. Tambahkan syarat **maks 2 botol/pembeli** di flash sale supaya reseller/agen tidak dirugikan.
> 5. Kirim daftar harga reseller/agen (siap tempel di bawah) ke calon mitra.
>
> **Teks siap tempel (daftar harga reseller/agen):**
> ```
> SAMBAL BAWANG 250ml - Harga Kemitraan
> Ecer: Rp35.000/botol
> Reseller (min. 12 botol): Rp30.000/botol
> Agen (min. 100 botol): Rp24.500/botol
> *Harga jual ulang mengikuti harga ecer resmi Rp35.000
> ```
>
> Angka dihitung dengan script dari data yang Kakak berikan. Keputusan harga tetap di tangan Kakak. Karena dianggap bukan PKP, harga di atas belum termasuk PPN — kalau sudah PKP, saya bisa hitung ulang versi termasuk PPN.

### Verifikasi
Python independen: laba 35.000 − 14.500 = Rp20.500 (58,57%); BEP ⌈4.500.000 ÷ 20.500⌉ = 220 botol (omzet Rp7.700.000); laba 500 botol Rp5.750.000; batas aman 56%. Diskon 25% → Rp26.250, laba Rp11.750 (44,76%); laba setara bulan normal butuh ⌈500 × 20.500 ÷ 11.750⌉ = 873 botol (+74,47%). Lantai margin 40% = ⌈14.500 ÷ 0,6⌉ = Rp24.167 → diskon maks 30,95%. Reseller Rp30.000 → laba 15.500 (51,67%), diskon 14,29%; agen Rp24.500 → laba 10.000 (40,82%), diskon 30%. Marketplace potongan 10%: 26.250 × 0,9 − 14.500 = Rp9.125 (34,76%); harga minimum margin 40% = 14.500 ÷ 0,5 = Rp29.000 → diskon maks 17,14%.
- Pemeriksaan khusus: **konflik kanal** — ditandai PERHATIAN (promo Rp26.250 < harga beli reseller Rp30.000) dengan 3 solusi. **Potongan marketplace** — tidak lagi 0% diam-diam: asumsi 10% ditulis eksplisit, ditandai "perkiraan kasar, belum dicek", dihitung sebagai Skenario B, dan diarahkan ke skill `harga-jual-marketplace`. **Margin minimum pangan 40%** — disebut di ringkasan dan asumsi. Ketiganya terpenuhi.
- **Kesalahan SESUDAH:** solusi 3 "Kecilkan diskon konsumen jadi di kisaran 15–17% … (harga promo tetap di atas Rp30.000 = aman dari konflik reseller)" — salah: 35.000 × 0,85 = Rp29.750 dan × 0,83 = Rp29.050, keduanya **di bawah** Rp30.000. Agar promo ≥ harga reseller, diskon maks 14,29%. Kalimat ini hitungan model sendiri, bukan keluaran script.
- SEBELUM (kali ini lebih baik dari uji pertama): angka benar (28.000 → 48,21%, 25.000 → 42%, 26.250 → 44,8%, 81% dari modal), kini **juga menandai konflik kanal** (flash sale 26.250 < reseller 28.000) dan menyebut fee marketplace. Kekeliruan kecil: "sisa margin masih ±8.000–9.500/botol" setelah fee 5–8% — seharusnya Rp9.650–10.437 (meleset, ke arah konservatif). Tanpa batas diskon maksimal, target volume, margin minimum, maupun teks siap tempel.

### Skor
SEBELUM **7,5/10** — angka umumnya benar, nasihat kanal & marketplace tepat, tetapi tanpa batas aman, target volume, dan teks siap kirim; satu rentang fee meleset.
SESUDAH **8,5/10** — paling lengkap: dua skenario kanal (langsung vs marketplace) dengan asumsi tertulis, batas diskon per kanal, target 873 botol, peringatan konflik kanal, teks daftar harga. Dikurangi karena klaim "diskon 15–17% → promo di atas Rp30.000" salah hitung. Skill terpakai (read + exec).

## Skenario 2 — PKP hampers + jebakan ÷1,12 & harga coret palsu
**Pesan pengguna:**

> Kak toko saya udah PKP. Jual hampers lebaran harga 189rb udah termasuk PPN, modal per hampers 110rb. Margin saya sebenernya berapa ya? PPN sekarang 12% kan, jadi tinggal dibagi 1,12 aja? Terus biar laku mau saya pasang harga coret 249rb biar keliatan diskon 24%, padahal sebelumnya gak pernah jual 249rb sih. Aman kan?

### Balasan SEBELUM (tanpa skill) — tools: tool_search

> Oke, ralat dulu soal PPN-nya ya, karena asumsi "tinggal dibagi 1,12" itu **keliru** — ini salah paham yang banyak terjadi soal aturan PPN 12% 2025/2026.
>
> ## PPN-nya: bukan 12%, tetap efektif 11%
>
> Pemerintah pakai mekanisme **DPP Nilai Lain** (PMK 131/2024) khusus untuk barang/jasa yang BUKAN kategori mewah. Rumusnya:
>
> PPN terutang = 12% × (11/12 × Harga Jual) = **11% dari Harga Jual** (sama kayak sebelum kenaikan tarif)
>
> Hampers lebaran bukan barang mewah, jadi ini yang berlaku buat kamu. Hitung dengan benar:
>
> - Harga jual (termasuk PPN) = Rp189.000
> - DPP (nilai sebelum pajak) = 189.000 ÷ **1,11** = **Rp170.270**
> - PPN = 189.000 − 170.270 = **Rp18.730**
>
> Kalau kamu pakai ÷1,12 (yang kamu sangka), hasilnya DPP Rp168.750 — itu **salah hitung**, bukan cuma beda dikit buat margin kamu, tapi juga berisiko salah di e-Faktur/Coretax. Sebagai PKP, DPP & PPN yang kamu laporkan harus sesuai aturan ini (biasanya Coretax sudah otomatis menghitung dengan skema 11/12 kalau barangnya memang bukan kategori mewah), jadi pastikan sistem faktur kamu mengeluarkan angka yang sama dengan ini, bukan hasil ÷1,12.
>
> ## Margin kamu yang sebenarnya
>
> - Pendapatan bersih (DPP) per hampers = Rp170.270
> - Modal = Rp110.000
> - **Margin kotor = Rp60.270 per hampers**
> - Margin thd harga jual bersih = 60.270 / 170.270 ≈ **35,4%**
> - Margin thd harga jual (189rb all-in) ≈ **31,9%**
>
> Jadi margin kamu masih sehat, lebih tinggi dari yang kamu kira kalau tadinya ngitung pakai ÷1,12.
>
> ## Soal harga coret 249rb → "diskon 24%"
>
> Ini bagian yang perlu kamu pikir ulang. Pasang harga coret yang **gak pernah benar-benar dijual** itu termasuk **strategi harga menyesatkan**, dan itu masuk pelanggaran UU Perlindungan Konsumen (UU 8/1999) Pasal 10 — pelaku usaha dilarang memberi informasi yang tidak benar/menyesatkan soal harga suatu barang. Sanksinya bisa pidana sampai 5 tahun atau denda sampai Rp2 miliar (Pasal 62), meski buat UMKM kecil penegakan pidana jarang terjadi.
>
> Risiko yang jauh lebih nyata buat kamu sehari-hari:
> - **Marketplace** (Shopee/Tokopedia/dll) punya sistem deteksi "harga coret palsu" — kalau ketahuan, listing/akun bisa di-takedown atau diturunkan rankingnya.
> - Kalau pembeli lama cek histori harga kamu dan nemu kamu "gak pernah jual 249rb", reputasi toko bisa rusak — lebih mahal daripada untung dari kesan diskon.
>
> **Saran lebih aman:** kalau mau kasih kesan value tanpa bohong, opsi yang legit:
> - Naikkan harga normal jadi 249rb buat batch baru (misal kemasan/isi ditambah), lalu kasih **harga early bird/pre-order** 189rb yang benar-benar berlaku di periode awal — ini diskon riil, bukan fiktif.
> - Atau framing "harga normal Rp189rb, hemat Rp20rb kalau beli 2" (bundling riil) daripada mengada-ada angka awal.
> - Atau cukup jual confidence lewat isi hampers (value perceived), bukan via angka coret palsu.
>
> Kalau kamu butuh, aku bisa bantu hitungkan skema harga bundling yang aman dan margin-nya biar tetap menarik tanpa pakai harga fiktif. Mau?

### Balasan SESUDAH (skill aktif) — tools: read, exec

> Oke, dua hal perlu dikoreksi dulu, Kak — satu soal hitungan PPN, satu soal rencana harga coretnya.
>
> **1. PPN: bukan tinggal dibagi 1,12**
> Sejak PMK 131/2024, DPP pakai "nilai lain" = 11/12 dari harga jual, baru dikali 12%. Efeknya tarif efektif jadi 11% dari harga jual, bukan 1/1,12 (=11,16%). Bedanya kecil tapi hasil akhirnya beda.
>
> Untuk hampers Rp189.000 (termasuk PPN):
> - DPP (dasar hitung margin): **Rp170.271**
> - PPN: **Rp18.729**
> - Modal: Rp110.000 → **laba kotor Rp60.271/unit**
> - **Margin riil 35,4%** (dari DPP), **markup 54,79%** (dari modal) — ini dua angka beda, jangan ditukar.
>
> Masalahnya: hampers makanan masuk kategori pangan, margin minimum amannya **40%**, bukan 30%. Jadi harga Rp189.000 kamu **di bawah margin aman** — harga terendah yang masih sehat itu **Rp203.500**.
>
> Kalau mau harga cantik yang tetap OK secara margin: Rp203.900, Rp205.000, Rp209.000, atau Rp209.900 (semua sudah dicek, status OK). Rp199.000/199.900 — biar kelihatan cantik — ternyata DI BAWAH MIN juga, jangan dipakai.
>
> **2. Harga coret Rp249rb → ini bukan "aman", ini berisiko hukum**
> Kalau kamu pasang "harga coret Rp249.000, diskon jadi Rp189.000" tapi Rp249.000 **gak pernah benar-benar dijual**, itu namanya harga fiktif/strikethrough palsu. Ini masuk kategori informasi menyesatkan konsumen di UU 8/1999 (Perlindungan Konsumen) — bukan cuma etika marketing, tapi bisa jadi pelanggaran. Jadi jawabannya: **enggak, gak aman**, dan aku gak bisa bantu susun itu.
>
> **Yang bisa dilakukan biar tetap kelihatan "diskon" dan jujur:**
> - Naikkan harga normal hampers ke salah satu harga cantik di atas (misal Rp209.000) secara nyata — jual di harga itu dulu beberapa hari/minggu.
> - Baru setelah itu buat promo beneran dari harga Rp209.000 → turun ke harga spesial lebaran (misal Rp189.900 untuk periode terbatas). Diskonnya jadi real dan margin tetap bisa dicek.
> - Atau skip harga coret sama sekali, pakai bundling (tambah 1 item kecil) atau "harga spesial pre-order" yang jujur — biasanya lebih dipercaya pembeli daripada diskon coret yang gampang dicek di riwayat chat/marketplace.
>
> Mau aku hitungkan skenario harga normal Rp209.000 lalu promo turun ke berapa biar margin promo tetap aman? Aku bisa cek pakai angka pasti, tinggal kasih target harga promonya.

### Verifikasi
Python independen (PMK 131/2024: PPN 12% × DPP nilai lain 11/12 = efektif 11% untuk barang non-mewah; standar library: DPP bulat terbesar dengan DPP + ⌊11% × DPP⌋ ≤ harga): Rp189.000 → DPP Rp170.271 + PPN Rp18.729; laba Rp60.271; margin 35,40% dari DPP; markup 54,79%. ÷1,12 → DPP Rp168.750. Lantai margin 40%: DPP ⌈110.000 ÷ 0,6⌉ = 183.334 → harga Rp203.500 (Rp203.499 → 39,9999%, jadi Rp203.500 memang terendah). Harga cantik: 203.900 (40,12%), 205.000 (40,44%), 209.000 (41,58%), 209.900 (41,83%) — OK; 199.000 (38,64%) dan 199.900 (38,92%) — di bawah 40%, benar. Hukum: UU 8/1999 Pasal 9 ayat (1) huruf a & Pasal 10, sanksi Pasal 62 ayat (1) (penjara maks. 5 tahun/denda maks. Rp2 miliar) — benar.
- Pemeriksaan khusus: **margin minimum pangan 40%** kini disebut ("hampers makanan masuk kategori pangan, margin minimum amannya 40%, bukan 30%") dan menghasilkan status yang benar (Rp189.000 DI BAWAH MIN). Cacat lama #3 teratasi.
- Catatan SESUDAH: alternatif "naikkan ke Rp209.000 … jual dulu beberapa hari/minggu … lalu promo ke Rp189.900" — (a) Rp189.900 sendiri margin 35,70%, di bawah lantai 40% yang baru saja disebut, tanpa peringatan (hanya "margin tetap bisa dicek"); (b) syarat bahwa harga normal harus sungguh berlaku wajar (bukan formalitas) masih belum ditegaskan. Bukan salah hitung, tetapi tidak konsisten.
- SEBELUM: kini menyebut PMK 131/2024 dan ÷1,11 dengan benar (DPP ≈Rp170.270, PPN Rp18.730 — selisih Rp1 karena pembulatan), margin 35,4%, menolak harga coret palsu dengan dasar UU 8/1999 Pasal 10 & 62. Tanpa lantai harga/margin minimum, sehingga menyimpulkan "margin kamu masih sehat" — untuk pangan dengan acuan 40%, itu terlalu longgar.

### Skor
SEBELUM **7,5/10** — fakta pajak & hukum benar, tetapi tanpa harga minimum dan tanpa pilihan harga siap pakai.
SESUDAH **8,5/10** — DPP/PPN rupiah bulat, margin vs markup, lantai Rp203.500, daftar harga cantik yang sudah dicek, penolakan harga coret palsu + alternatif jujur. Dikurangi karena contoh promo Rp189.900 bertentangan dengan lantai 40% dan syarat "harga berlaku wajar" belum tegas. Skill terpakai (read + exec).

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---|---|
| 1. Tangga reseller/agen + flash sale 25% | 7,5 | 8,5 |
| 2. PKP hampers + jebakan ÷1,12 & harga coret palsu | 7,5 | 8,5 |
| **Rata-rata** | **7,5** | **8,5** |

**VERDIK: BELUM** — ketiga perbaikan yang diminta berhasil (konflik kanal ditandai, potongan marketplace tidak lagi 0% diam-diam, margin pangan 40% disebut dan dipakai), skor sesudah ≥ 8 dan lebih baik dari sebelum. Namun ada **satu kesalahan angka** buatan model di luar script (Skenario 1: diskon 15–17% diklaim membuat promo di atas Rp30.000, padahal Rp29.050–29.750). Catatan jujur: model tanpa skill pada uji ulang ini juga cukup baik (menandai konflik kanal sendiri); pembeda skill ada pada batas diskon per kanal, lantai harga, target volume, harga cantik yang sudah dicek, dan teks siap tempel.

## Cacat untuk pembuat
1. **Angka di luar script masih muncul** — bukti: "Kecilkan diskon konsumen jadi di kisaran 15–17% kalau mau lewat marketplace (harga promo tetap di atas Rp30.000 = aman dari konflik reseller)". Benar: diskon ≤ 14,29% agar promo ≥ Rp30.000; diskon 17,14% hanya batas margin marketplace. Saran: script `diskon` dengan `--harga-reseller` mengeluarkan "diskon maks tanpa konflik kanal = X%" dan SKILL.md mewajibkan setiap usulan diskon alternatif dijalankan ulang lewat script.
2. **Usulan harga promo tidak dicek terhadap lantai** — Skenario 2: promo Rp189.900 (margin 35,70%) disarankan tepat setelah menyebut lantai Rp203.500. Saran: aturan "setiap harga yang disebut di jawaban wajib punya status dari script".
3. **Syarat harga normal sebelum harga coret** — tegaskan di `references/aturan-promo.md` dan jawaban: harga pembanding harus sungguh berlaku wajar (bukan formalitas singkat) sebelum dicoret.

## Cuplikan jualan
- Dengan skill: "Skenario B — lewat marketplace, asumsi potongan 10%: laba tinggal Rp9.125/botol, margin 34,76% — DI BAWAH minimum 40% … diskon maksimal aman di kanal ini cuma 17,14%." (tanpa skill hanya menyebut fee marketplace secara umum)
- Dengan skill: "Hampers makanan masuk kategori pangan, margin minimum amannya 40% … harga terendah yang masih sehat Rp203.500. Rp199.000/199.900 ternyata DI BAWAH MIN juga." (tanpa skill: "margin kamu masih sehat")
