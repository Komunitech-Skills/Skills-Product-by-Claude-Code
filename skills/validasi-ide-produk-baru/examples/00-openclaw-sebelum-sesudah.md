# Uji SEBELUM/SESUDAH di OpenClaw asli — validasi-ide-produk-baru

**Tanggal:** 2026-10-01 · **Penguji:** agent penguji independen (bukan pembuat skill)

## Cara uji
- OpenClaw **2026.9.6** dijalankan lokal (`openclaw agent --local`, tanpa gateway/Telegram), model router Komunitech **claude-sonnet-5** — sama dengan bot member.
- **SEBELUM** = home OpenClaw bersih tanpa skill ini (`k-validasi-ide-produk-baru`); **SESUDAH** = home bersih berisi hanya skill ini (`s-validasi-ide-produk-baru`). Home dibuat ulang sebelum setiap skenario.
- Pesan pengguna identik di kedua sisi, gaya awam WA/Telegram. File data fiktif identik disalin ke kedua home.
- Angka diverifikasi independen dengan Python oleh penguji; aturan Indonesia dicek terhadap teks aturan.


## Skenario 1 — Normal: rancang uji murah keripik tempe pedas sebelum produksi

**Pesan pengguna (identik):**

````text
Kak aku mau jual keripik tempe pedas kemasan 200 gram, rencana harga Rp18.000, modalnya kira2 Rp9.500 per bungkus. Kontak WA ku ada 300an, follower IG 1.200. Gimana caranya ngetes dulu laku apa engga sebelum produksi banyak? Ga mau rugi modal
````

### Balasan SEBELUM (tanpa skill) — tools: tool_search, memory_search, tool_call

````text
Oke, sebelum keluar modal buat produksi banyak, validasi dulu pakai sistem **pre-order (PO)** — jangan produksi dulu, baru jual kalau sudah ada yang bayar. Ini cara paling aman buat modal kamu yang segini (300 kontak WA + 1.200 followers IG, margin Rp8.500/bungkus = 47%, lumayan sehat).

**Tahap 1 — Tes rasa ke circle terdekat (modal kecil, ~Rp50-100rb)**
- Produksi 5-10 bungkus aja pakai modal sendiri, kasih ke 5-10 orang yang kamu percaya jujur kasih kritik (bukan yang cuma bilang "enak kok" basa-basi).
- Tanya spesifik: level pedas pas nggak, kemasan oke nggak, harga Rp18rb kemahalan/wajar/murah, bakal beli lagi nggak.
- Kalau feedback banyak yang negatif di sini, benerin dulu sebelum lanjut — jangan buang modal ke tahap berikutnya.

**Tahap 2 — Buka PO terbatas lewat WA + IG (ini tes validasi beneran)**
- Posting foto produk + harga di WA Story + broadcast, dan IG Story/Feed. Jelasin: sistem pre-order, closed PO [tanggal], minta DP 50% atau transfer penuh biar niat beli jelas (bukan cuma "nanti ya").
- Kasih insentif early bird kecil (misal gratis ongkir area tertentu, atau bonus 1 sachet) biar orang gerak cepat, bukan nunda-nunda.
- Produksi HANYA sejumlah PO yang sudah bayar. Nol resiko stok nganggur.

**Tolok ukur realistis buat 300 WA + 1.200 IG:**
- Jangan harap semua orang respon. Konversi wajar dari kontak dekat biasanya sekitar 1-3%.
- Reach efektif (ada overlap WA/IG) kira-kira 1.000-1.300 orang unik → target realistis **15-25 PO** dalam 2-3 hari closed PO.
- Kalau dapat di bawah 5-10 PO dari seluruh network itu → sinyal produk/harga/pesan belum klik, jangan lanjut produksi besar dulu, cari tahu alasannya (harga? pedesnya kurang unik? foto kurang menggoda?) baru coba ulang.
- Kalau tembus 15+ PO dan ada yang repeat order di gelombang berikutnya → itu sinyal kuat layak produksi lebih besar.

**Yang perlu dicatat selama tes:**
- Siapa yang pesan + sudah bayar (spreadsheet simpel atau catatan WA manual aja, skalanya masih kecil, nggak perlu tools ribet).
- Repeat order rate dari batch pertama — ini indikator paling jujur soal "suka beneran" vs "penasaran doang".
- Komplain soal packaging/ongkir/rasa.

**Soal angka modal:**
Margin Rp8.500/bungkus itu belum termasuk packaging, ongkir, dan effort kamu — jadi kalau mau lebih akurat, itung dulu total biaya per unit di luar bahan (plastik/kemasan, label, ongkir kalau kamu subsidi). Tapi untuk tes validasi awal, fokus dulu ke: **apakah orang mau bayar di muka** — itu sinyal paling jujur, jauh lebih reliable dari sekadar likes atau "wah enak nih".

Mau aku bantu bikinin draft teks promo PO buat WA/IG-nya sekalian?
````

### Balasan SESUDAH (dengan skill) — tools: read

````text
Oke, sebelum produksi banyak, jangan tebak-tebak — kita uji dulu pakai kontak yang udah kamu punya (WA 300an + IG 1.200 follower), selesai dalam 7 hari, baru putuskan lanjut atau tidak. Ini rancangannya:

**1. Hipotesis yang mau diuji**
"Kami percaya **pecinta camilan pedas di kontak WA & follower IG kamu** mau membayar **Rp18.000** untuk **keripik tempe pedas kemasan 200gr** karena **camilan renyah-pedas yang praktis buat ngemil/oleh-oleh**. Kami akan tahu ini benar kalau minimal sekian persen dari yang ditawari benar-benar pre-order dalam 7 hari."

Catatan: "pecinta camilan pedas" itu masih asumsi awal — kalau kamu punya segmen lebih spesifik (misal: ibu kantoran, anak kos, reseller camilan), boleh dipertajam, tapi tidak wajib untuk mulai uji.

**2. Metode uji — kamu punya 2 kanal yang cukup kuat, pakai dua-duanya:**
- **Pre-order broadcast/status WA** (kontak 300an, syarat minimal cuma 30 ✅)
- **Polling story Instagram** (follower 1.200, syarat minimal 100 ✅)

Saya hitung konversi **per kanal secara terpisah** (bukan digabung), supaya ketahuan kanal mana yang lebih efektif — nanti dari dua angka itu kita putuskan.

**3. Kriteria lulus/gagal — disesuaikan karena harga Rp18.000 termasuk murah/impulsif (<Rp30rb):**
- **LULUS** (lanjut produksi): konversi ≥ **20%**
- **LULUS BERSYARAT** (ada minat, tapi revisi dulu): konversi **10%–<20%**
- **GAGAL** (hentikan/ganti): konversi **< 10%**
- Ambang dinaikkan dari default 15%/8% karena produk murah biasanya butuh konversi lebih tinggi untuk dianggap sinyal kuat (orang gampang bilang "mau" tapi belum tentu niat beli beneran untuk barang semurah ini).
- Kalau jumlah yang ditawari di satu kanal < 20 orang, hasil kanal itu saya tandai "indikasi awal" aja, bukan kesimpulan final.

**4. Pesan siap pakai**

*Broadcast/status WA (pre-order):*
```
Halo [nama panggilan]! 👋

Aku lagi coba mulai jual Keripik Tempe Pedas 200gr — gurih, renyah, pedasnya nendang, cocok buat ngemil atau oleh-oleh.

Harga: Rp18.000 / bungkus (200gr)

Kalau minat yang masuk cukup, aku mulai produksi minggu ini.
Mau pesan? Balas "MAU + jumlah" ke chat ini sebelum [tanggal, maks 7 hari dari sekarang] ya. 🙏

Kalau minat yang masuk belum cukup dan jadinya tidak diproduksi, atau pesananmu batal karena alasan lain, uang kamu aku kembalikan 100% paling lambat 2 hari setelah [tanggal batas/keputusan]. Kamu juga boleh batal kapan saja sebelum [tanggal mulai produksi] tanpa alasan, uang kembali penuh.

[Nama kamu/usaha]
```

*Polling story Instagram:*
```
Lagi mikir mau mulai jualan Keripik Tempe Pedas 200gr 🤔
Gurih, renyah, pedasnya nampol — enak buat ngemil kapan aja
Harga rencana: Rp18.000

Kalau ada, kamu bakal beli? [stiker polling: Ya, mau! / Nanti dulu]

(DM aku kalau mau pesan duluan pas udah jadi 😊)
```

Catatan wajib: isi bagian kurung siku tanggal & kebijakan batal sebelum kirim — jangan skip, itu supaya calon pembeli nggak merasa ditipu kalau ternyata gak jadi produksi.

**5. Form pencatatan (tempel ke Notes/spreadsheet)**
- Tanggal mulai–selesai: _____ – _____
- WA: Jumlah dikirimi/lihat status: ___ | Jumlah balas "MAU": ___
- IG: Jumlah views story: ___ | Jumlah vote "Ya" yang lanjut DM serius: ___
- Catatan alasan yang bilang "nanti dulu" (harga/belum butuh/lainnya): _____

**6. Setelah 7 hari, hitung begini**
Rumus manual: konversi (%) = (jumlah pre-order ÷ jumlah ditawari) × 100

Atau kirim angka hasilnya ke aku (jumlah ditawari & pre-order per kanal), nanti aku hitungkan pakai script otomatis — sekalian langsung dapat margin & cek balik modal biaya uji. Formatnya kira-kira:
```
python3 hitung_validasi.py --ditawari 50 --preorder 12 --harga 18.000 --hpp 9.500 --biaya-uji 50.000
```
(angka 50/12/50.000 cuma contoh, nanti isi angka asli dari hasil ujimu)

Margin per bungkus kamu sekarang: Rp18.000 − Rp9.500 = **Rp8.500/bungkus** — lumayan sehat (±47%), jadi kalau hasil uji LULUS, ruang profitnya cukup oke buat lanjut ke hitung HPP/BEP yang lebih rinci.

Mau aku bantu tajamkan target pembeli dulu, atau langsung aja kamu jalankan ujinya minggu ini dan laporan hasilnya ke aku nanti?
````

### Verifikasi independen

Margin Rp18.000 − Rp9.500 = **Rp8.500/bungkus = 47,2% dari harga** — kedua sisi benar. SEBELUM: target "15–25 PO" dari jangkauan 1.000–1.300 orang dengan konversi wajar 1–3% (1–3% × 1.000–1.300 = 10–39, konsisten kasar). SESUDAH: ambang dinaikkan ke 20%/10% sesuai aturan skill untuk produk < Rp30rb. Untuk broadcast ke 300 kontak, LULUS ≥20% berarti ≥60 PO dalam 7 hari — sangat ketat dibanding pengalaman umum respons broadcast; ambang ini heuristik skill, bukan fakta, dan berisiko memberi vonis GAGAL pada ide yang sebenarnya layak. Kalimat hipotesis SESUDAH masih berisi "minimal sekian persen" (belum diisi angka). Template WA SESUDAH berisi janji refund padahal pembeli hanya diminta membalas "MAU" (belum membayar).

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | **7** | Nasihat praktis & benar (PO dulu, tes rasa, catat repeat order, margin), tapi tanpa kriteria lulus/gagal yang ditetapkan di awal, tanpa teks siap kirim, tanpa form pencatatan. |
| SESUDAH | **8** | Lengkap & siap pakai: hipotesis, 2 metode sesuai kanal, kriteria lulus/gagal sebelum uji, teks WA & polling IG, form pencatatan, rumus. Kurang: hipotesis belum berangka, teks refund tidak cocok dengan alur "balas MAU", ambang 20% untuk broadcast 300 kontak terlalu ketat tanpa penjelasan dasar. |

Skill terpakai: SEBELUM tidak. SESUDAH ya (SKILL.md + templates).

## Skenario 2 — Jebakan: hasil uji campuran (PO yang sudah transfer vs vote polling IG) — lanjut produksi 200 bungkus?

**Pesan pengguna (identik):**

````text
Kak, aku udah tes jual keripik tempe pedas 200gr harga Rp18.000 seminggu ini. Broadcast WA ke 45 orang, yang PO (udah transfer) 4 orang. Terus polling story IG dilihat 380 orang, yang vote "mau beli" 52. Modal per bungkus Rp9.500, biaya tes (sampel + ongkir) Rp60.000. Jadi lanjut produksi 200 bungkus ga nih?
````

### Balasan SEBELUM (tanpa skill) — tools: (tanpa alat)

````text
Oke, run angkanya dulu ya biar jelas gambarannya — jangan lompat ke 200 bungkus dulu, aku kasih alasannya.

**Konversi riil (yang bayar beneran):**
- WA broadcast: 4 PO / 45 orang = **8,9%**. Ini dari network hangat (kenalan sendiri), basisnya kecil banget (n=45), jadi margin errornya gede — next batch bisa cuma dapet 1 orang, bisa juga 8.
- IG poll "mau beli": 52/380 = 13,7%. Tapi ini **soft interest**, bukan uang keluar. Orang klik vote di poll itu gratis, gak ada komitmen. Biasanya yang beneran convert ke beli kalau ditodong harga fix cuma sekitar 20-30%-nya → realistis cuma ~10-15 orang dari 52 itu yang bakal checkout.

Jadi total demand real + potensial yang udah tervalidasi sekarang: **~15-20 orang**, bukan 200.

**Soal margin:** Rp18.000 - Rp9.500 = Rp8.500/bungkus (47% margin). Ini sehat, produknya worth dilanjutin dari sisi angka.

**Masalahnya di jumlah produksi:**
- 200 bungkus itu modal Rp1.900.000.
- BEP-nya butuh jual ~106 bungkus (1.900.000 ÷ 18.000) buat balik modal produksi itu doang.
- Demand tervalidasi kamu baru ~15-20 orang. Itu jauh di bawah 106. Keripik juga bukan barang awet — kalau nggak laku-laku, kualitasnya turun (apek/melempem), jadi stok nyangkut = duit mati + rugi beneran, bukan cuma opportunity cost.

**Saran aku, jangan 200 dulu:**
1. **DM langsung** 52 orang yang vote "mau beli" di poll — kasih harga fix + cara order (transfer/DP). Ini validasi murah buat ubah soft interest jadi hard data, gratis dan cepat.
2. **Buka PO round 2** seminggu lagi ke audience lebih luas (grup WA lain, keluarga jauh, dll) biar sample size lebih besar dari 45 — biar persentase konversinya lebih bisa dipercaya.
3. **Produksi sesuai PO real + buffer kecil** (misal jumlah PO terkumpul + 20%), bukan angka bulat 200. Model pre-order gini bikin risiko stok nyangkut nol.
4. Begitu udah collect 40-60 PO real dari dua putaran ini, baru masuk akal mikir produksi 100-200 pcs sekaligus buat stok jual bebas (bukan PO).

Intinya: produknya oke secara margin, tapi datanya masih terlalu tipis buat lompat ke 200. Kumpulin PO real dulu, biar produksi ngikutin demand yang udah ada duitnya, bukan tebak-tebakan.
````

### Balasan SESUDAH (dengan skill) — tools: read, exec

````text
Oke, aku hitung pakai script skill-nya. Ringkasnya:

**1. Hipotesis**
Ibu-ibu/pekerja yang suka ngemil pedas di kontak WA & follower IG kakak mau bayar Rp18.000 untuk keripik tempe pedas 200gr karena cocok buat cemilan pedas praktis. Akan terbukti benar kalau konversi "beli/mau beli" cukup tinggi dari yang ditawari dalam 7 hari.

**2. Hasil per kanal (ambang default 15% lulus / 8% bersyarat)**
- *WA broadcast (PO = transfer beneran):* 4 dari 45 → konversi 8.9% → LULUS BERSYARAT (nyaris GAGAL, mepet banget di batas bawah)
- *Polling story IG (cuma vote niat, belum transfer):* 52 dari 380 → konversi 13.7% → LULUS BERSYARAT
- *Gabungan:* 56 dari 425 → konversi 13.2% → LULUS BERSYARAT

Karena keripik tempe ini produk murah & impulsif (di bawah Rp30rb), aku cek juga pakai ambang yang lebih ketat (20% lulus / 10% bersyarat, sesuai aturan skill untuk produk harga rendah) — hasilnya tetap LULUS BERSYARAT untuk gabungan & IG, tapi WA-nya malah jatuh ke GAGAL (8.9% < 10%).

**3. Yang perlu kakak tahu soal datanya**
- Vote IG "mau beli" itu niat tanpa komitmen uang — biasanya lebih optimis dari kenyataan. Angka yang lebih bisa dipercaya adalah WA PO (4 orang beneran transfer), dan itu yang paling lemah (8.9%).
- Jadi real demand kemungkinan lebih dekat ke sinyal WA daripada ke angka gabungan 13.2%.

**4. Uang**
- Margin per bungkus: Rp8.500 (18.000 − 9.500)
- Total margin dari 56 pre-order: Rp476.000
- Biaya tes: Rp60.000 → sudah balik modal tes +Rp416.000 (bagian positifnya)

**Keputusan: UBAH dulu, jangan langsung produksi 200 bungkus.**
Sinyalnya ada minat, tapi belum cukup kuat buat lompat ke 200 bungkus sekaligus — risikonya kebesaran kalau cuma modal "kayaknya laku". Saran konkret, pilih SATU dulu biar jelas apa yang berubah:
- Follow-up personal ke 52 orang yang vote "mau beli" di IG, tawarkan closing PO beneran (transfer) — ini langsung ngetes apakah niat itu beneran jadi uang.
- Atau coba turunkan sedikit harga / kasih promo "beli 2 gratis ongkir" ke broadcast WA susulan, lihat apakah konversi naik.
- Atau coba kemasan/porsi beda (misal 100gr lebih murah) buat target yang masih ragu.

Lalu uji ulang 7 hari lagi dengan hipotesis baru itu sebelum commit produksi 200 bungkus. Kalau nanti hasil ulangnya tembus ≥15% (atau ≥20% kalau mau standar ketat produk murah), baru aman lanjut — dan kalau udah di titik itu aku bisa bantu hitung HPP/BEP produksi 200 bungkus biar ga rugi.
````

### Verifikasi independen

Konversi PO nyata (sudah transfer): 4 ÷ 45 = **8,9%**. Vote polling 52 ÷ 380 = 13,7% — ini niat, bukan pembelian. Script skill (`hitung_validasi.py --ditawari 45 --preorder 4 --harga 18000 --hpp 9500 --biaya-uji 60000`) memberi: margin Rp8.500 × 4 = **Rp34.000**, biaya uji Rp60.000 → **selisih −Rp26.000 (BELUM balik modal uji)**. Ambang produk murah (<Rp30rb) menurut skill 20%/10% → WA 8,9% = **GAGAL**; ambang default 15%/8% → LULUS BERSYARAT. Modal 200 bungkus = Rp1.900.000; titik impas penjualan ≈ 1.900.000 ÷ 18.000 = 106 bungkus.

SEBELUM: semua angka benar (8,9%, 13,7%, margin, modal Rp1.900.000, ~106 bungkus) dan memisahkan vote dari PO. **SESUDAH: salah angka** — menggabungkan vote dengan PO ("56 dari 425 → 13,2%") lalu menghitung "Total margin dari 56 pre-order: Rp476.000… sudah balik modal tes +Rp416.000". Yang benar hanya 4 PO → Rp34.000, belum balik modal (−Rp26.000). Keputusan akhirnya (UBAH, jangan 200 bungkus) tetap masuk akal.

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | **8** | Membedakan vote vs uang masuk, angka benar, ada hitung modal & titik impas 200 bungkus, saran bertahap (DM 52 voter, PO putaran 2, produksi sesuai PO). Kurang: biaya tes Rp60.000 tidak dihitung; perkiraan "20–30% voter jadi beli" tanpa dasar. |
| SESUDAH | **5** | Format keputusan rapi dan memperingatkan bahwa vote IG bukan komitmen, tapi tetap menjumlahkan vote sebagai pre-order sehingga laporan uang salah (mengklaim balik modal +Rp416.000 padahal −Rp26.000) dan konversi gabungan menyesatkan. Kesalahan angka pada keputusan modal = fatal. |

Skill terpakai: SEBELUM tidak. SESUDAH ya (`scripts/hitung_validasi.py` dijalankan dengan angka gabungan).

## Ringkasan

- **Skor rata-rata:** SEBELUM 7,5 → SESUDAH 6,5
- **VERDIK: BELUM** — Ada kesalahan angka di skenario 2 (vote polling dihitung sebagai pre-order → klaim balik modal yang salah). Model tanpa skill lebih tepat di skenario itu.

### Cacat untuk pembuat (bukti + saran)

1. **Instruksi menggabungkan metode menyesatkan (penyebab utama)** — bukti: skenario 2 SESUDAH "Gabungan: 56 dari 425 → 13.2%" dan "Total margin dari 56 pre-order: Rp476.000… sudah balik modal tes +Rp416.000"; SKILL.md Langkah 2: "hasilnya digabung sebagai total 'ditawari' dan total 'pre-order/beli'". Saran: larang menjumlahkan sinyal berbeda jenis; hanya tindakan berkomitmen (transfer/DP/beli) yang masuk `--preorder` & perhitungan margin; vote/klik/"minat" dilaporkan terpisah sebagai metrik minat. Tambahkan uji regresi untuk kasus ini.
2. **Script tidak tahu jenis sinyal** — saran: tambah argumen `--minat` (vote/balasan tanpa bayar) yang dilaporkan tapi tidak ikut margin/balik modal, atau peringatan bila `--preorder` > 30% dari `--ditawari` untuk kanal polling.
3. **Ambang produk murah diterapkan tidak konsisten** — bukti: skenario 2 menampilkan ambang default lebih dulu (WA "LULUS BERSYARAT"), padahal produk Rp18.000 menurut SKILL.md memakai 20%/10% (WA = GAGAL). Saran: tentukan satu ambang di awal sesuai harga, jangan dua.
4. **Ambang 20% untuk broadcast WA ke ratusan kontak** (skenario 1) tidak dijelaskan dasarnya dan bisa terlalu ketat; saran: bedakan ambang per kanal (broadcast massal vs sampel ke pelanggan tetap) atau beri sumber/alasan.
5. Template pre-order: teks refund dipakai walau pembeli belum diminta membayar — saran: sesuaikan dengan alur (minta DP/transfer atau hapus kalimat refund).

### Catatan perilaku agent (keamanan/privasi)

- Tidak ada pemasangan paket, perubahan config, tawaran kirim/posting otomatis, atau pencarian disk di kedua sisi.

### Cuplikan jualan

_(Pakai hanya setelah cacat 1 diperbaiki & diuji ulang.)_

> Dari satu kalimat ide, skill langsung memberi hipotesis, kriteria LULUS/GAGAL yang ditetapkan **sebelum** uji, teks pre-order WA + polling IG siap tempel (lengkap kebijakan batal/refund), dan form pencatatan 7 hari — tanpa skill, jawabannya berupa saran umum tanpa kriteria berangka.
