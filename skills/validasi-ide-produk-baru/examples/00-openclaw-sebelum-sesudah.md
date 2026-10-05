

## Uji ulang 2026-10-01

**Penguji:** agent penguji independen (bukan pembuat skill) · **Versi diuji:** 1.0.4 · **OpenClaw:** 2026.9.7 (lokal, `openclaw agent --local`), model router Komunitech.

**Cara uji ulang:** `uji.sh` kini **terisolasi** (mount namespace; agent hanya melihat home-nya sendiri). Home `k-`/`s-` dibuat ulang sebelum tiap skenario; pesan **identik persis**; SEBELUM dijalankan ulang juga (bersih, tanpa jejak skill). Tambahan: 1 skenario **varian** (hanya SESUDAH) dengan angka lain, karena kasus keripik 4/45 → −Rp26.000 kini tertulis langsung di SKILL.md dan tes regresi (risiko "hafal soal").

### Skenario 1 (ulang) — pesan sama persis dengan Skenario 1 di atas

#### Balasan SEBELUM (tanpa skill) — tools: (tanpa alat)

`````text
Oke, dengan modal segitu ketat (margin ~Rp8.500/bungkus = 47%), strategi paling aman adalah **jangan produksi sama sekali sebelum ada uang masuk duluan**. Pakai sistem PO (pre-order), bukan nebak-nebak stok. Ini urutannya:

**1. Validasi rasa dulu (sebelum jualan)**
Bikin 1 batch kecil (bisa 10-15 bungkus) buat dikasih gratis/cicip ke orang-orang yang jujur kasih kritik — bukan cuma temen deket yang pasti bilang "enak kok". Minta feedback spesifik: pedasnya pas gak, kemasan menarik gak, harga 18rb masuk akal gak menurut mereka. Modal tahap ini kecil banget, anggap sunk cost buat riset.

**2. Tes minat dulu sebelum tes beli**
Sebelum buka PO, lempar polling ringan di IG Story: *"Kalau ada keripik tempe pedas kemasan 200gr, 18rb, kalian tertarik gak? Yes/No"*. Ini gratis, cepat, dan kasih sinyal awal — kalau response rate dari 1.200 follower rendah banget, kamu belum perlu buang modal produksi besar.

**3. Buka PO terbatas (ini kunci utamanya)**
- Produksi cuma setelah ada pembayaran (DP 50% atau full payment duluan).
- Broadcast ke 300 kontak WA + feed/story IG, dengan jumlah terbatas misal **30 bungkus** dan deadline 3-5 hari ("Open PO 30 pcs aja, slot terbatas").
- Jangan broadcast spam ke semua grup WA, kirim personal/ke kontak yang relevan dulu biar gak dianggap gangguan.
- Boleh kasih insentif kecil buat 10-20 pembeli pertama (misal gratis ongkir atau harga 15rb), tapi jangan diskon gede-gede — margin kamu udah lumayan tipis buat produk kecil.

**4. Hitung target validasi**
Modal buat batch 30 pcs = 30 × Rp9.500 = **Rp285.000**. Kalau PO dibayar di muka, modal kamu praktis Rp0 karena dibiayai uang customer duluan.
Patokan sederhana:
- PO terisi ≥30 dalam 5 hari → sinyal kuat, lanjut produksi lebih besar & mulai pikirin reseller/marketplace.
- PO di bawah 10-15 → jangan skip, evaluasi dulu: apakah rasanya yang kurang nendang, harga kemahalan, atau cara promosinya yang kurang menarik (foto/video produk perlu dibikin lebih "ngiler").

**5. Baru scale up kalau ada repeat order**
Setelah batch pertama habis dan ada yang beli ulang/rekomen ke orang lain, itu baru sinyal produk ini punya demand nyata — baru deh mikirin produksi rutin, kemasan lebih niat, sampai urus PIRT kalau mau jualan lebih luas (marketplace biasanya minta ini).

Intinya: ubah mindset dari "produksi dulu, jual belakangan" jadi **"jual (PO) dulu, produksi belakangan"**. Dengan jaringan 300 WA + 1.200 followers, target 30 pcs itu realistis dicapai kalau kamu kirim pesan personal, bukan cuma posting dan nunggu.

Mau aku bantu bikinin draft pesan broadcast WA + caption IG buat buka PO-nya?
`````

#### Balasan SESUDAH (dengan skill) — tools: read

`````text
Oke, sebelum produksi banyak, test dulu pakai kontak yang udah kamu punya (WA 300an + IG 1.200) — total biaya ngetes bisa Rp0, cuma modal foto produk & waktu 7 hari. Ini rancangannya:

**1. Hipotesis**
Kami percaya kontak WA & follower IG yang suka camilan pedas mau membayar Rp18.000 untuk keripik tempe pedas kemasan 200 gram karena camilan gurih-pedas praktis buat nyemil/oleh-oleh. Kami akan tahu ini benar kalau minimal 20% dari yang ditawari lewat broadcast WA benar-benar transfer/DP dalam 7 hari.

**2. Metode uji (gabung 2 kanal)**
- Broadcast/status WA (≥30 kontak → kamu punya 300an, cocok) → ini kanal **pesanan** (yang sudah transfer/DP).
- Polling story IG (≥100 follower → kamu punya 1.200, cocok) → ini kanal **minat** saja (vote belum tentu beli). Yang vote "Ya" nanti kamu DM, tawarkan PO+DP; yang transfer baru masuk hitungan pesanan terpisah.

**3. Kriteria lulus/gagal**
Rp18.000 itu kategori harga impulsif (di bawah ~Rp30rb, orang beli tanpa mikir lama), jadi saya naikkan ambang dari default 15%/8% jadi:
- Konversi ≥ 20% → **LULUS**, lanjut produksi bertahap.
- Konversi 10%–<20% → **LULUS BERSYARAT**, ada minat tapi perlu revisi (harga/kemasan/target).
- Konversi < 10% → **GAGAL**, hentikan dulu idenya.
- Minimal ditawari 20 orang biar hasil bukan kebetulan (kamu jauh di atas itu).

**4. Pesan siap kirim**

Broadcast/status WA (isi [Nama] & tanggal sebelum kirim):
```
Halo [Nama]! 👋

Aku lagi coba mulai jual Keripik Tempe Pedas kemasan 200gr — gurih renyah, pedasnya nampol, cocok buat nyemil atau oleh-oleh.

Harga: Rp18.000 / bungkus (200gr)

Kalau cukup banyak yang minat, aku mulai produksi minggu ini.
Mau pesan? Balas "MAU + jumlah" ke chat ini sebelum [tanggal, maks 7 hari dari sekarang] ya. 🙏

Kalau minat yang masuk belum cukup dan jadinya tidak diproduksi, atau pesananmu batal karena alasan lain, uang kamu aku kembalikan 100% paling lambat 2 hari setelah tanggal batas. Kamu juga boleh batal kapan saja sebelum mulai produksi tanpa alasan, uang kembali penuh.

[Nama kamu/usaha]
```

Caption polling story IG:
```
Lagi mikir mau mulai jualan Keripik Tempe Pedas 200gr 🤔
Gurih renyah, pedas nampol, cocok temen kerja/nonton!
Harga rencana: Rp18.000

Kalau ada, kamu bakal beli? [stiker polling: Ya, mau! / Nanti dulu]

(DM aku kalau mau pesan duluan pas udah jadi 😊)
```

Buat yang jawab "nanti dulu" di WA, boleh tanya balik:
```
Oke, gak apa-apa! Boleh tau kenapa belum tertarik? (harga / belum butuh / mau lihat dulu / lainnya) — biar aku bisa perbaiki 🙏
```

**5. Form pencatatan (tempel ke Notes HP)**
Data awal:
- Ide: Keripik tempe pedas 200gr
- Calon pembeli: Kontak WA & follower IG penyuka camilan pedas
- Harga rencana: Rp18.000
- Metode uji: Broadcast WA (pesanan) + Polling story IG (minat)
- Tanggal: 1 Okt – 8 Okt 2026
- Kriteria LULUS: ≥20% | LULUS BERSYARAT: 10%–<20%

Catat tiap hari: tanggal, kanal, jumlah ditawari/dilihat, jumlah pesanan SUDAH BAYAR/DP, jumlah minat saja (vote/komen belum bayar), catatan alasan tertarik/tidak.

**Setelah 7 hari**, kirim angkanya ke aku (jumlah ditawari WA, jumlah yang sudah transfer, jumlah views IG, jumlah vote "Ya"), nanti aku hitungkan pakai script biar presisi — formatnya kira-kira gini:
```json
{"harga": 18000, "hpp": 9500, "biaya_uji": 0,
 "kanal": [{"nama": "Broadcast WA", "ditawari": 300, "preorder": 0},
           {"nama": "Polling IG", "ditawari": 1200, "minat": 0}]}
```
(0 tinggal diganti angka asli nanti)

Ingat: yang dihitung sebagai "pesanan" cuma yang **sudah transfer/DP**, bukan yang cuma bilang "mau" — biar hasilnya jujur dan kamu nggak salah ambil keputusan produksi besar.

Satu hal lagi: ambang 20%/10% ini heuristik praktis, bukan patokan baku — kalau nanti hasilnya mepet, kita bisa diskusikan lagi. Siap kirim broadcast-nya?
`````

### Skenario 2 (ulang) — pesan sama persis dengan Skenario 2 di atas

#### Balasan SEBELUM (tanpa skill) — tools: tool_search

`````text
Oke, aku hitung dulu angkanya sebelum jawab lanjut/nggak:

**Konversi riil (orang bayar beneran):**
- WA broadcast: 4 dari 45 → **8,9%**
- IG poll "mau beli": 52 dari 380 → 13,7%, tapi ini cuma *vote niat*, belum pegang uang. Biasanya pas ditagih beneran, yang jadi beli cuma sebagian kecil dari yang vote — jangan disamain sama konversi WA.

**Ekonomi produk:**
- Margin per bungkus: 18.000 − 9.500 = **8.500 (47%)** → sehat, harga nggak masalah.
- Biaya tes 60rb, margin kotor dari 4 PO = 4 × 8.500 = 34rb → net "rugi" tes cuma 26rb. Itu wajar, namanya ongkos belajar, bukan tanda produk gagal.

**Verdict: jangan langsung gas 200 bungkus.**

Alasannya bukan karena produknya jelek — margin oke, ada sinyal minat — tapi basis pembeli kamu sekarang cuma nyentuh ~400 orang (45 WA + 380 IG) dengan konversi riil 8,9%. Kalau pola sama, buat ngejual 200 bungkus kamu butuh reach sekitar 2.250 orang. Itu 5x lipat dari jangkauan kamu minggu ini. Keripik juga ada masa simpan — kalau 200 bungkus nyangkut, modal Rp1.900.000 bisa basi sebelum kejual.

**Saran langkah berikutnya:**
1. Produksi bertahap dulu: **50-60 bungkus** (modal ~500-570rb), bukan 200.
2. Closing-in ke 52 orang yang vote "mau beli" di IG + minta 4 yang udah PO buat refer teman/kasih testimoni — ini re-test konversi dari grup yang udah nunjukin minat, bukan broadcast random lagi.
3. Kasih insentif kecil (gratis ongkir/bundling) buat dorong niat jadi transfer beneran.
4. Kalau dari batch 50-60 ini sell-through ≥70% dalam 1-2 minggu → baru naik ke 150-200.

Mau aku bikinin draft pesan closing buat ditembak ke 52 orang IG itu?
`````

#### Balasan SESUDAH (dengan skill) — tools: read, exec

`````text
Jawabannya: **belum sat-set lanjut 200 bungkus, Kak — tapi juga belum gagal.** Hasilnya LULUS BERSYARAT. Sudah aku hitung pakai script biar bukan feeling:

**Hipotesis yang diuji**
Kami percaya kontak WA/follower IG yang kenal brand ini mau bayar Rp18.000 untuk keripik tempe pedas 200gr karena jadi cemilan pedas praktis. Akan terbukti benar kalau cukup banyak dari yang ditawari benar-benar transfer dalam 7 hari.

**Per kanal (pesanan vs minat, dua hal beda — minat ga pernah dihitung jadi uang):**
- Broadcast WA: 45 ditawari → **4 PO bayar = 8,9%** (ini yang dipakai hitung keputusan, karena ini pesanan beneran)
- Polling IG: 380 dilihat → 52 vote "mau beli" = 13,7% — ini **minat**, bukan pesanan, karena belum ada yang bayar. Nilainya tetap sinyal bagus, tapi belum masuk hitungan untung/rugi.

**Ambang keputusan:** LULUS ≥15%, LULUS BERSYARAT 8%–<15%, GAGAL <8% (default skill).
→ 8,9% dari WA = masuk kotak **LULUS BERSYARAT**.

**Uang:**
- Margin per bungkus: Rp18.000 − Rp9.500 = **Rp8.500**
- Total margin dari 4 PO: 4 × Rp8.500 = **Rp34.000**
- Biaya tes: Rp60.000
- Selisih: Rp34.000 − Rp60.000 = **−Rp26.000** (uji ini sendiri belum balik modal, itu wajar — namanya juga tes)

**Artinya:** ada minat nyata (52 vote IG lumayan besar relatif ke 380 views), tapi konversi jadi pembeli beneran di WA masih di bawah target kuat (15%). Kalau langsung produksi 200 bungkus pakai rate 8,9%, risikonya kebanyakan nyangkut.

**Rekomendasi: UBAH dulu, jangan HENTIKAN, jangan langsung LANJUT 200 pcs.**
Pilih SATU variabel buat direvisi (bukan sekaligus semua, biar ketahuan yang ngaruh apa):
1. **Harga** — coba turunkan dikit atau bikin paket bundle (misal 2 bungkus Rp32.000) buat naikkan urgensi beli.
2. **Penawaran/kemasan** — tambah DP ringan (bayar nanti pas terima) atau diskon early-bird buat 10 pemesan pertama, biar yang "minat" di IG berani commit bayar.
3. **Target pembeli** — broadcast WA ke 45 orang itu siapa? Kalau campur random, coba fokus ke yang emang doyan pedas/snack dulu.

Satu hal yang bisa bantu aku kasih saran lebih tajam: **dari 41 orang WA yang ga PO, ada yang kasih alasan kenapa ga jadi beli?** (kemahalan, ga doyan pedas, ragu kualitas, dll). Kalau ada, itu jadi petunjuk kuat variabel mana yang paling perlu diubah.

Setelah revisi, uji ulang 7 hari lagi dengan hipotesis baru (misal: "dengan DP ringan, konversi PO naik ke ≥15%"). Kalau hasil kedua ini LULUS, baru lanjut ke hitung HPP/BEP produksi 200 bungkus biar modal besarnya aman — bisa aku bantuin pakai skill `hitung-hpp` kapan aja.
`````

### Skenario varian (generalisasi, hanya SESUDAH) — sambal botol, pesanan vs minat dengan angka baru

**Pesan:**

````text
Kak, aku udah tes jual sambal bawang botol 150ml harga Rp35.000 dua minggu ini. Status WA dilihat 120 orang, yang udah transfer 9. Terus di grup arisan 30 orang, yang bilang 'mau dong' 14 orang tapi belum bayar. Modal per botol Rp21.000, biaya tes Rp150.000. Lanjut produksi 100 botol ga?
````

#### Balasan SESUDAH — tools: read, exec

`````text
Udah aku hitung pakai rumus baku (bukan feeling ya, Kak):

**HASIL UJI 2 MINGGU**

*Kanal pesanan (status WA):*
- Dilihat: 120 orang
- Transfer (pesanan beneran): 9
- Konversi: 9 ÷ 120 = **7,5%**

*Kanal minat (grup arisan):*
- 30 orang, 14 bilang "mau dong" tapi belum bayar → ini **minat**, bukan pesanan, jadi gak ikut dihitung ke omzet/margin.

*Margin & biaya uji:*
- Margin/botol: Rp35.000 − Rp21.000 = Rp14.000
- Total margin dari 9 pesanan: 9 × Rp14.000 = Rp126.000
- Biaya tes: Rp150.000
- Selisih: Rp126.000 − Rp150.000 = **−Rp24.000** (belum balik modal)

**KLASIFIKASI: GAGAL** (ambang: lulus ≥15%, lulus bersyarat ≥8%, gagal <8%)

Tapi jujur, Kak, ini **mepet banget** — 7,5% vs ambang 8%, beda cuma 1 pre-order doang (10/120 = 8,3% udah masuk "lulus bersyarat"). Jadi bukan GAGAL telak, lebih ke "belum cukup kuat buat lanjut 100 botol sekaligus."

**Saran aku, bukan HENTIKAN total dulu, tapi:**
1. Jangan produksi 100 botol — modal Rp2.1jt terlalu besar buat data semepet ini.
2. Sebelum nyerah, coba 1 revisi aja (pilih satu, biar jelas apa yang kerja):
   - Turunin harga jadi Rp28-30rb, atau
   - Tawarin bundling 2 botol, atau
   - Follow-up 14 orang grup arisan yang bilang "mau" — minta mereka transfer/DP beneran (ini ngubah minat jadi pesanan asli, dan sample-nya kecil tapi gratis buat dicoba).
3. Kalau sempat, tanya ke yang lihat tapi gak beli (111 orang) kenapa gak jadi — alasan itu bahan revisi paling berharga.

Produksi bertahap kecil dulu (misal 20-30 botol) buat uji revisi itu, baru naik ke 100 kalau konversi tembus 15%.

Mau aku bantu susun pesan follow-up buat 14 orang grup arisan itu (ngubah minat jadi DP)? Atau kalau mau hitung HPP/BEP produksi 100 botol buat jaga-jaga, aku bisa bantu pakai skill `hitung-hpp`.
`````

### Verifikasi independen (uji ulang, Python + `scripts/hitung_validasi.py`)

- **Skenario 1:** margin Rp18.000 − Rp9.500 = Rp8.500 (47,2%) — kedua sisi benar. SEBELUM: modal batch 30 × Rp9.500 = Rp285.000 benar. SESUDAH: ambang 20%/10% (produk < Rp30rb); untuk broadcast ke 300 kontak berarti **≥ 60 orang transfer dalam 7 hari** untuk LULUS.
- **Skenario 2:** pesanan 4 ÷ 45 = **8,9%**; vote 52 ÷ 380 = 13,7% (minat). Margin 4 × Rp8.500 = **Rp34.000**; Rp34.000 − Rp60.000 = **−Rp26.000**; modal 200 bungkus = Rp1.900.000; impas ≈ 105,6 → 106 bungkus. SESUDAH: semua angka benar, vote tidak dijumlahkan, satu set ambang (15%/8%) → LULUS BERSYARAT. SEBELUM: angka juga benar (8,9%, 13,7%, Rp34rb, −Rp26rb, Rp1,9 jt), "reach ~2.250 orang untuk 200 bungkus" = 200 ÷ 0,089 ≈ 2.250 benar.
- **Varian sambal (SESUDAH):** 9 ÷ 120 = **7,5%**; margin Rp35.000 − Rp21.000 = Rp14.000; 9 × Rp14.000 = Rp126.000; − Rp150.000 = **−Rp24.000**; 10/120 = 8,3%; modal 100 botol = Rp2.100.000. Script skill memberi hasil identik (GAGAL, −Rp24.000). Semua angka di balasan benar; 14 "mau dong" dilaporkan sebagai minat.

### Status cacat lama

| # | Cacat uji pertama | Status | Bukti uji ulang |
|---|---|---|---|
| 1 | Vote polling dijumlahkan dengan PO → klaim balik modal +Rp416.000 | **Tuntas** | Skenario 2: "4 PO bayar = 8,9% … 52 vote … ini **minat**, bukan pesanan"; selisih **−Rp26.000**. Varian dengan angka baru juga benar (−Rp24.000, minat terpisah). Tidak muncul 56/425/416. |
| 2 | Script tidak tahu jenis sinyal | **Tuntas** | `--minat` & mode `kanal` ada; skenario 1 SESUDAH memberi contoh JSON per kanal (pesanan vs minat). |
| 3 | Dua klasifikasi dengan ambang berbeda dalam satu jawaban | **Tuntas di dalam satu jawaban** | Skenario 2 hanya memakai 15%/8%. **Tetapi** lihat regresi: skenario 1 untuk produk yang sama memakai 20%/10%. |
| 4 | Ambang 20% untuk broadcast ratusan kontak tanpa dasar | **Sebagian** | Skenario 1 kini menyebut "heuristik praktis, bukan patokan baku", tetapi tetap menetapkan LULUS ≥ 20% (≥ 60 transfer dari 300 kontak) tanpa membedakan kanal. |
| 5 | Teks refund padahal pembeli hanya diminta balas "MAU" | **Belum** | Skenario 1 SESUDAH: "Balas "MAU + jumlah"…" lalu "uang kamu aku kembalikan 100%…". Sumbernya `templates/pesan-uji-murah.md` #1 yang masih meminta balasan "MAU". Kini lebih serius: menurut aturan hitung baru, balasan "MAU" = **minat**, jadi template utama WA tidak menghasilkan "pesanan" yang bisa dinilai, sementara hipotesis jawaban yang sama mensyaratkan "benar-benar transfer/DP". |

### Regresi / temuan baru

- **Ambang tidak konsisten antar-percakapan untuk produk yang sama (sedang):** skenario 1 menetapkan 20%/10% untuk keripik Rp18.000; skenario 2 (hasil uji produk yang sama) menilai dengan 15%/8% → LULUS BERSYARAT. Dengan 20%/10%, 8,9% = GAGAL. SKILL.md hanya "boleh naikkan", jadi model memilih berbeda-beda; ini persis "menggeser target setelah lihat hasil" yang ingin dicegah skill. Rekomendasi tetap masuk akal (UBAH, jangan 200 bungkus), jadi tidak menyesatkan, tetapi klasifikasinya bergantung pada pilihan acak model.
- Skenario 2: saran "tambah DP ringan (bayar nanti pas terima)" bertentangan sendiri (DP = bayar di muka). Minor.
- Skenario 2 & varian menyarankan skill `hitung-hpp` yang tidak terpasang di home uji (rujukan silang ke produk lain). Minor.
- Perilaku: SESUDAH hanya `read`/`exec` (script skill), tanpa instal/kirim/posting. SEBELUM bersih (tools: tidak ada / `tool_search`).

### Skor uji ulang

| Skenario | SEBELUM | SESUDAH | Alasan singkat |
|---|---|---|---|
| 1 Rancang uji | **7** | **8** | SEBELUM: alur PO benar, target 30 bungkus & modal Rp285.000 benar, tanpa teks siap kirim & tanpa kriteria berbasis persentase; menyebut margin 47% "tipis". SESUDAH: hipotesis kini berangka, pesanan vs minat dipisah per kanal, kriteria ditetapkan di awal, teks WA/IG, form, contoh JSON. Dikurangi: template "balas MAU" + kalimat refund (cacat 5), ambang 20% untuk 300 kontak. |
| 2 Hasil campuran | **8** | **8,5** | Keduanya angka benar & memisahkan vote. SESUDAH lebih terstruktur (per kanal, ambang, rumus tiap baris uang, satu variabel revisi, tanya alasan 41 orang). Dikurangi: ambang beda dengan skenario 1, "DP … bayar nanti". |
| Varian sambal (SESUDAH saja) | — | **9** | Angka baru semua benar, minat dipisah, GAGAL tipis dijelaskan jujur ("beda 1 pesanan"), saran bertahap. |

**Rata-rata (skenario sama):** SEBELUM 7,5 → SESUDAH **8,25**.

### VERDIK: **LULUS**

SESUDAH ≥ 8 di kedua skenario, ≥ SEBELUM, dan **tidak ada kesalahan angka** (cacat fatal "vote = pesanan" tuntas, terbukti juga pada angka baru). Keunggulan atas SEBELUM pada skenario 2 tipis (model tanpa skill sudah menghitung benar kali ini); nilai tambah utama ada di skenario 1 (rancangan uji siap pakai). Sisa yang sebaiknya diperbaiki berikutnya: (a) template #1 meminta transfer/DP atau mengganti kalimat refund dengan "belum perlu bayar sekarang" (cacat 5); (b) tetapkan ambang produk < Rp30rb secara pasti (bukan "boleh") atau minta agent menanyakan/mengingat ambang yang dipakai saat merancang uji; (c) bedakan ambang untuk broadcast massal.

### Cuplikan jualan (jujur, dari uji ulang)

> "Broadcast WA: 45 ditawari → 4 PO bayar = 8,9% … 52 vote 'mau beli' = 13,7% — ini **minat**, bukan pesanan … Selisih: Rp34.000 − Rp60.000 = **−Rp26.000**." Skill memisahkan orang yang sudah bayar dari yang baru bilang "mau", menghitung untung-rugi uji dengan rumus yang ditampilkan, lalu memberi keputusan LANJUT/UBAH/HENTIKAN, bukan sekadar semangat.
