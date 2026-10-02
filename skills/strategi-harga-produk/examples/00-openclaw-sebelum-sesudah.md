# Uji OpenClaw sebelum/sesudah — strategi-harga-produk

**Tanggal:** 2026-10-02 (uji ulang ke-3, versi skill 1.0.6)  
**Penguji:** agent penguji independen Komunitech (bukan pembuat skill)

## Riwayat
- **1.0.4** (uji pertama 2026-10-02): rata-rata SEBELUM 7,0 → SESUDAH 8,25, verdik **LULUS dengan cacat** — harga agen sama dengan harga flash sale tanpa peringatan konflik kanal; potongan marketplace 11.11 diasumsikan 0% diam-diam; hampers makanan dinilai dengan margin minimum 30% (seharusnya pangan 40%); saran "jual dulu di harga coret beberapa hari".
- **1.0.5** (uji ulang ke-2, 2026-10-02): 7,5 → 8,5, verdik **BELUM** — ketiga cacat lama teratasi, tetapi model menghitung sendiri di luar script: "kecilkan diskon jadi 15–17% (harga promo tetap di atas Rp30.000)" salah (Rp29.050–29.750 < Rp30.000; batas sebenarnya < 14,29%), dan contoh promo Rp189.900 (margin 35,70%) disarankan di bawah lantai margin 40% tanpa peringatan.
- **1.0.6** (uji ulang ke-3, di bawah): pembuat menambah ATURAN KERAS "angka promo hanya dari script", blok `DISKON MAKSIMAL` + `--rentang` di script, dan aturan harga coret tanpa "jual dulu beberapa hari". Kedua skenario dijalankan ulang dengan pesan identik.

## Cara uji (uji ulang ke-3, 2026-10-02)
- OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech (`komunitech` → `claude-sonnet-5`), sama dengan bot member.
- SEBELUM = home OpenClaw bersih tanpa skill; SESUDAH = home bersih berisi hanya skill `strategi-harga-produk` 1.0.6. Home dibuat ulang sebelum tiap skenario.
- Pesan identik dengan dua uji sebelumnya, identik di kedua sisi, satu giliran (agent tidak bertanya balik).
- Setiap angka di balasan SESUDAH dicocokkan dengan menjalankan sendiri `scripts/strategi_harga.py` (perintah yang semestinya dipakai agent), lalu diverifikasi lagi dengan Python independen (bukan script skill); fakta aturan dicek terhadap aturan Indonesia yang berlaku.
- Catatan keamanan: tidak ada agent yang memasang paket, mengubah config, menawarkan kirim/posting otomatis ke pihak lain, atau mencari ke seluruh disk. SEBELUM tidak memakai alat; SESUDAH memakai `read` + `exec` (membaca skill & menjalankan script).

## Skenario 1 — tangga reseller/agen + flash sale 11.11
**Pesan pengguna:**

> Kak saya jual sambal bawang botol 250ml harga 35rb, modal per botol 14.500. Mau buka reseller (minimal ambil 12 botol) sama agen (minimal 100 botol), terus bulan depan mau ikut flash sale 11.11 diskon 25%. Biaya tetap sebulan (sewa dapur + gaji 2 orang) 4,5jt, laku sekitar 500 botol sebulan. Harga reseller & agen bagusnya berapa? Diskon 25% masih untung ga?

### Balasan SEBELUM (tanpa skill) — tools: tidak ada

> Oke, saya hitung ya. Modal 14.500/botol, jual eceran 35.000 → margin kotor 20.500/botol (58,6% dari harga jual, alias markup 141% dari modal). Lumayan sehat buat basis itungan reseller & agen.
>
> **Harga reseller & agen yang masuk akal:**
>
> - **Reseller (min 12 botol): Rp28.000/botol** (diskon ±20% dari harga eceran)
>   - Margin kamu: 13.500/botol (masih 93% di atas modal)
>   - Margin reseller kalau dia jual lagi di harga normal 35.000: 7.000/botol (20%) — cukup menarik buat insentif mereka jualan rutin.
>
> - **Agen (min 100 botol): Rp24.500/botol** (diskon ±30% dari harga eceran)
>   - Margin kamu: 10.000/botol (masih 69% di atas modal)
>   - Margin agen kalau jual retail langsung: 10.500/botol (30%); kalau dia distribusiin lagi ke sub-reseller di 28.000: masih dapat 3.500/botol — tipis tapi masuk akal buat volume gede.
>
> Pola ini standar FMCG: reseller diskon lebih kecil karena ambil lebih sedikit, agen diskon lebih besar karena commitment volume & biasanya mereka yang jualan ke toko/warung lagi.
>
> **Soal flash sale 11.11 diskon 25%:**
>
> Harga jadi 35.000 × 0,75 = **26.250**. Margin kotor = 26.250 − 14.500 = **11.750/botol (44,8%)**. Masih untung per botol, cuma turun dari margin normal 58,6% ke 44,8%.
>
> Tapi hati-hati, angka itu belum masuk biaya platform (admin fee marketplace, subsidi ongkir, biaya ikut campaign) yang biasanya "makan" 1.500–3.000/botol lagi. Jadi margin bersih realistis sekitar **9.000–10.000/botol (34–38%)** — tetap untung, tapi jangan kaget kalau di laporan marketplace angkanya lebih tipis dari itung manual.
>
> **Insight penting buat biaya tetap 4,5jt/bulan:** kalau penjualan normal bulanan kamu (±500 botol/bulan di harga 35rb) udah nutup fixed cost, maka tambahan botol yang laku lewat flash sale itu murni profit tambahan — fixed cost gak nambah cuma karena ikut flash sale (asal packing & stok masih sanggup tanpa nambah orang/lembur). Contoh simulasi: misal dari 500 botol itu, 150 botol terjual pas periode flash sale (26.250) dan 350 sisanya di harga normal:
>
> - Revenue: 350×35.000 + 150×26.250 = 16.187.500
> - Modal: 500×14.500 = 7.250.000
> - Gross profit: 8.937.500
> - Net profit (setelah fixed cost 4,5jt): **4.437.500**
>
> Dibanding baseline semua normal (net profit ±5.750.000), turun ±1,3jt — tapi tetap positif. Dan kalau flash sale itu narik pembeli BARU di luar 500 botol biasa (bukan cuma mindahin yang harusnya beli normal), itu malah nambah profit bersih karena fixed cost udah ketutup duluan.
>
> **Yang perlu diwaspadai:**
> 1. Jangan sampai reseller/agen ikut klaim harga flash sale — itu buat end customer, bikin aturan jelas.
> 2. Cek kapasitas dapur/packing pas lonjakan order flash sale, kalau perlu lembur/tambahan tenaga itu nambah variable cost yang belum dihitung di sini.
> 3. Cek fee riil platform tempat kamu ikut flash sale (Shopee/Tokopedia beda-beda) biar margin bersihnya presisi.
### Balasan SESUDAH (skill aktif) — tools: read, exec

> **Ringkasan**
> - Harga eceran tetap Rp35.000 — aman, margin 58,57% (lantai minimum pangan 40% baru tembus di bawah Rp24.167).
> - Reseller (≥12 botol): **Rp30.000/botol** → untung kakak Rp15.500/botol, untung reseller Rp5.000 (14,3%) per botol kalau dijual Rp35.000.
> - Agen (≥100 botol): **Rp26.500/botol** → untung kakak Rp12.000/botol, untung agen Rp8.500 (24,3%) per botol.
> - Diskon 25% buat flash sale 11.11: **TIDAK disarankan apa adanya** — margin jatuh ke 34,76% (di bawah lantai 40%) dan harga promo Rp26.250 malah lebih murah dari harga beli reseller & agen (reseller/agen pasti protes/borong stok). Batas aman: **maksimal diskon 14%** → harga promo Rp30.100.
>
> **Asumsi**
> - Margin minimum dipakai: 40% (kategori pangan, default skill karena sambal = makanan).
> - Kanal jual langsung = potongan 0%, kecuali promo 11.11 saya hitung sebagai event marketplace → potongan marketplace diasumsikan 10% dari harga jual (perkiraan, belum dicek — kalau ikut lewat Shopee/TikTok Shop, cek dulu biaya admin asli pakai hitung potongan marketplace biar presisi).
> - HPP Rp14.500/botol dianggap pasti (sesuai angka kakak).
> - Belum PKP → harga di atas belum termasuk PPN.
>
> **Tabel harga**
> | Level | Min beli | Harga/botol | Diskon dari eceran | Laba kakak/botol | Margin | Untung reseller/agen | Status |
> |---|---|---|---|---|---|---|---|
> | Eceran | 1 | Rp35.000 | - | Rp20.500 | 58,57% | - | OK |
> | Reseller | ≥12 | Rp30.000 | 14,29% | Rp15.500 | 51,67% | Rp5.000 (14,3%) | OK |
> | Agen | ≥100 | Rp26.500 | 24,29% | Rp12.000 | 45,28% | Rp8.500 (24,3%) | OK |
>
> **BEP (titik impas)**
> - Biaya tetap Rp4.500.000/bulan, laba kontribusi Rp20.500/botol → **BEP 220 botol/bulan**.
> - Penjualan sekarang 500 botol → laba kotor ±**Rp5.750.000/bulan**. Batas aman (margin of safety) 56% — penjualan boleh turun sampai separuh lebih sedikit sebelum rugi. Sehat.
>
> **Aturan promo 11.11 — diskon 25% masih untung?**
> Tidak disarankan dipakai mentah-mentah, dua masalah sekaligus:
> 1. **Margin anjlok**: di harga Rp26.250, laba tinggal Rp9.125/botol (margin 34,76%), di bawah batas aman 40%. Supaya laba kotor TOTAL tetap sama kayak biasa, penjualan harus naik **86,3%** (dari 500 jadi minimal 932 botol) — berat untuk event sebulan.
> 2. **Bentrok kanal**: harga promo Rp26.250 lebih murah dari harga beli reseller (Rp30.000) dan agen (Rp26.500). Reseller/agen bakal dirugikan — bisa marah atau malah ikut memborong stok promo buat dijual ulang.
>
> **DISKON MAKSIMAL yang aman** (dari hitungan, bukan kira-kira):
> - Supaya margin ≥40%: diskon maksimal 17,14% (harga promo Rp29.000).
> - Supaya tidak bentrok harga reseller: diskon harus **di bawah 14,29%**.
> - Supaya tidak bentrok harga agen: diskon harus **di bawah 24,29%**.
> - **Gabungan semua batas → diskon maksimal yang aman: 14%, harga promo Rp30.100.**
>
> Opsi lain kalau mau diskon lebih besar dari 14% demi daya tarik event besar:
> - Batasi kuota (mis. maks 2 botol/pembeli) supaya reseller/agen tidak ikut memborong.
> - Kasih reseller & agen harga khusus selama promo (misal turunkan sementara jadi Rp27.000/Rp24.000) biar mereka tetap untung dibanding harga promo konsumen.
> - Atau jual varian/ukuran khusus untuk promo (bukan botol 250ml reguler yang dipakai reseller/agen) supaya kanal tidak bentrok sama sekali.
>
> **Langkah minggu ini**
> 1. Set harga reseller Rp30.000 (≥12 botol) dan agen Rp26.500 (≥100 botol) — mulai berlaku bareng harga eceran.
> 2. Untuk 11.11: pasang diskon maksimal **14%** (harga Rp30.100) kalau mau aman tanpa drama kanal; kalau mau diskon lebih dalam, pasangkan dengan kuota per pembeli atau harga khusus reseller/agen selama event.
> 3. Cek biaya admin asli platform (bukan asumsi 10%) sebelum ikut 11.11 — pakai skill harga-jual-marketplace biar potongan real, bukan kira-kira.
> 4. Siapkan stok ekstra: kalau tetap pakai diskon besar, target penjualan tetap untung minimal naik ~86% dari normal (di atas 930 botol untuk periode yang sama).
>
> **Teks siap tempel (daftar harga reseller/agen untuk WA/katalog):**
> ```
> SAMBAL BAWANG - HARGA RESELLER & AGEN
> Eceran: Rp35.000/botol
> Reseller (min. 12 botol): Rp30.000/botol
> Agen (min. 100 botol): Rp26.500/botol
> *Harga belum termasuk ongkir, berlaku sampai pemberitahuan berikutnya
> ```
>
> Catatan: Angka dihitung dengan script dari data yang kakak berikan. Keputusan harga tetap di tangan kakak. Kalau 11.11-nya lewat marketplace tertentu (Shopee/TikTok Shop dll), kabari saya platformnya biar potongan admin dihitung presisi, bukan asumsi 10%.
### Verifikasi
**Cocokkan dengan script** (`tangga --harga-ecer 35000 --hpp 14500 --kategori pangan --level Reseller:12:=30000 --level Agen:100:=26500`; `diskon --harga 35000 --hpp 14500 --diskon 25 --volume 500 --kategori pangan --harga-reseller Reseller:30000 --harga-reseller Agen:26500 --kanal marketplace --biaya-persen 10`; `bep`): semua angka di Ringkasan, Tabel harga, BEP, dan blok "DISKON MAKSIMAL" **identik** dengan keluaran script — reseller Rp30.000 (14,29%, laba Rp15.500, 51,67%), agen Rp26.500 (24,29%, laba Rp12.000, 45,28%), promo Rp26.250 → laba Rp9.125 (34,76%), naik 86,3% → 932 botol, batas margin Rp29.000/17,14%, batas reseller < 14,29%, batas agen < 24,29%, gabungan **14% → Rp30.100**, BEP 220 botol/Rp5.750.000/56%.

**Python independen:** 35.000 − 14.500 = 20.500 (58,57%; markup 141,38%); BEP ⌈4.500.000 ÷ 20.500⌉ = 220; promo 26.250 × 0,9 − 14.500 = 9.125 (34,76%); laba normal di kanal yang sama 35.000 × 0,9 − 14.500 = 17.000 → ⌈500 × 17.000 ÷ 9.125⌉ = 932 (+86,30%); lantai marketplace 14.500 ÷ 0,5 = 29.000 (17,14%), lantai jual langsung ⌈14.500 ÷ 0,6⌉ = 24.167; 1 − 30.000/35.000 = 14,29%; 1 − 26.500/35.000 = 24,29%; 35.000 × 0,86 = 30.100 (margin marketplace 41,83%). Semua benar.

**Pemeriksaan khusus:**
- *Persen/harga promo/rentang dari script:* ya untuk semua angka utama; rentang 15–17% yang salah di 1.0.5 **tidak muncul lagi** — kini batas reseller "di bawah 14,29%" dan gabungan 14% disalin dari script. Cacat 1.0.5 #1 teratasi.
- *Saran harga di bawah margin minimum:* **masih ada satu.** Opsi "Kasih reseller & agen harga khusus selama promo (misal turunkan sementara jadi Rp27.000/Rp24.000)" — angka buatan model, bukan dari script. `margin --hpp 14500 --harga 24000 --kategori pangan` → margin **39,58% DI BAWAH MIN** (lantai Rp24.167), disarankan tanpa peringatan. Selain itu Rp27.000 untuk reseller tetap **di atas** harga promo Rp26.250 bila diskon 25% dipertahankan, jadi "solusi" itu tidak menghilangkan konflik kanal (berlaku hanya untuk diskon ≤ 22%).
- *Konflik kanal:* ditandai jelas di Ringkasan dan Aturan promo untuk reseller dan agen, dengan solusi kuota, harga khusus, varian khusus. Terpenuhi.
- *Potongan marketplace:* asumsi 10% tertulis di Asumsi, "perkiraan, belum dicek", diarahkan ke harga-jual-marketplace. Terpenuhi. Catatan kecil: "+86,3% supaya laba kotor TOTAL tetap sama kayak biasa" memakai pembanding bulan normal **juga lewat marketplace** (laba Rp17.000/botol); bila 500 botol biasa dijual langsung, pembandingnya Rp20.500 dan kebutuhan volumenya jauh lebih besar (1.124 botol). Ini perilaku script, tidak dijelaskan ke pengguna.
- *Harga coret:* tidak relevan di skenario ini.

**SEBELUM:** angka benar (28.000 → laba 13.500 = 93% dari modal; 24.500 → 10.000 = 69%; 26.250 → 11.750 = 44,8%; simulasi 350 normal + 150 promo → laba bersih Rp4.437.500 vs Rp5.750.000, benar). Kelemahan: **tidak menyadari** harga flash sale Rp26.250 lebih murah dari harga beli reseller Rp28.000 (hanya "jangan sampai reseller/agen ikut klaim harga flash sale"); tanpa margin minimum, batas diskon maksimal, maupun teks siap tempel; fee platform "1.500–3.000/botol" disebut kasar.

### Skor
SEBELUM **7,0/10** — hitungan benar dan simulasi campuran berguna, tetapi melewatkan konflik kanal reseller dan tanpa batas aman/teks siap kirim.
SESUDAH **8,0/10** — paling lengkap dan kini angka promo inti persis dari script (diskon maks 14% → Rp30.100, dua konflik kanal, asumsi marketplace tertulis, teks daftar harga). Dikurangi karena contoh harga khusus agen Rp24.000 di bawah lantai 40% tanpa peringatan dan contoh reseller Rp27.000 tidak menyelesaikan konflik pada diskon 25%. Skill terpakai (read + exec).

## Skenario 2 — PKP hampers + jebakan ÷1,12 & harga coret palsu
**Pesan pengguna:**

> Kak toko saya udah PKP. Jual hampers lebaran harga 189rb udah termasuk PPN, modal per hampers 110rb. Margin saya sebenernya berapa ya? PPN sekarang 12% kan, jadi tinggal dibagi 1,12 aja? Terus biar laku mau saya pasang harga coret 249rb biar keliatan diskon 24%, padahal sebelumnya gak pernah jual 249rb sih. Aman kan?

### Balasan SEBELUM (tanpa skill) — tools: tidak ada

> Oke, dua hal ya — PPN-nya sama harga coretnya. Jawaban singkat dulu: itung PPN-nya **salah** kalau cuma dibagi 1,12, dan harga coret 249rb itu **nggak aman**, bukan sekadar strategi marketing biasa.
>
> **1. Hitungan PPN & margin yang bener**
>
> Sejak tarif PPN naik ke 12%, pemerintah pakai mekanisme "DPP Nilai Lain" biar beban pajak ke konsumen efektifnya tetap setara 11% (bukan 12% penuh). Rumusnya: PPN terutang = 12% × (11/12 × harga jual sebelum pajak) = **11% dari harga sebelum pajak**.
>
> Jadi kalau harga jual 189rb itu sudah termasuk PPN:
>
> - Harga sebelum pajak (DPP) = 189.000 ÷ 1,11 = **Rp170.270**
> - PPN yang harus kakak setorkan = **Rp18.730**
> - Modal = Rp110.000
> - **Laba kotor sebelum pajak** = 170.270 − 110.000 = **Rp60.270/hampers**
> - Margin terhadap harga jual bersih ≈ **35,4%**
> - Markup terhadap modal ≈ **54,8%**
>
> Kalau kakak pakai cara "dibagi 1,12" tadi, hasilnya DPP 168.750, PPN 20.250, margin 58.750 — beda ~2.500/pcs dan PPN yang disetor jadi lebih besar dari seharusnya. Buat e-Faktur, pakai rumus 1,11 ini (DPP Nilai Lain), bukan 1,12 langsung. Kalau mau, nanti aku bisa buatin tabel/rumus Excel-nya biar tinggal input harga jual tiap produk.
>
> **2. Harga coret 249rb → diskon 24% padahal gak pernah dijual segitu**
>
> Ini yang perlu aku tegasin: **nggak aman**, dan bukan cuma soal etika.
>
> - Hampir semua marketplace (Shopee, Tokopedia, TikTok Shop, Lazada) punya kebijakan eksplisit larang "fake strikethrough price" — harga coret harus pernah benar-benar jadi harga jual aktif produk itu. Kalau ketahuan sistem/laporan buyer, produk bisa di-takedown, bahkan akun kena penalti/suspend.
> - Secara hukum, ini masuk kategori informasi harga yang menyesatkan menurut UU Perlindungan Konsumen (UU No. 8/1999) Pasal 10 — pelaku usaha dilarang kasih info harga yang tidak benar/menyesatkan. Risikonya rendah buat UMKM kecil secara praktik, tapi tetap pelanggaran kalau ada komplain konsumen atau audit platform.
>
> Kalau tujuannya emang mau keliatan "diskon", alternatif yang lebih aman:
> - Tetap pasang 189rb sebagai harga normal, tapi kasih embel-embel "Harga Spesial Lebaran" / bundling (misal +kartu ucapan gratis) biar tetap ada daya tarik tanpa klaim harga coret palsu.
> - Kalau mau beneran pasang harga coret, jual dulu barang di harga lebih tinggi (misal 219rb) buat beberapa hari/minggu, baru turunin — jadi harga coretnya based on history asli, bukan karangan.
>
> Mau aku bantu hitungin margin buat skenario harga 219rb → diskon ke 189rb juga, biar ada perbandingan yang aman tapi tetep keliatan menarik?
### Balasan SESUDAH (skill aktif) — tools: read, exec

> Oke, dua hal yang perlu diluruskan dulu — satunya soal PPN, satunya lagi soal harga coret 249rb, karena keduanya ada risikonya.
>
> **1. Margin sebenarnya — bukan dibagi 1,12**
>
> PPN 12% itu dikenakan atas **DPP nilai lain = 11/12 dari harga**, jadi tarif efektifnya 11%, bukan dibagi 1,12 langsung (dasar PMK 131/2024). Untuk harga 189rb termasuk PPN:
>
> | Item | Nilai |
> |---|---|
> | DPP (harga sebelum PPN) | Rp170.271 |
> | PPN | Rp18.729 |
> | Modal | Rp110.000 |
> | Laba kotor/unit | Rp60.271 |
> | **Margin (laba/DPP)** | **35,4%** |
> | Markup (laba/modal) | 54,79% |
> | Status vs margin minimum 40% (kategori pangan/hampers) | **DI BAWAH MIN** |
>
> Jadi margin kakak sekarang 35,4%, bukan 50%-an kalau dihitung dari 189rb mentah-mentah. Dan ini sebenarnya di bawah margin aman untuk produk pangan (40%). Harga terendah yang masih aman di margin 40%: **Rp203.500** (DPP Rp183.334, laba Rp73.334/unit).
>
> **2. Harga coret 249rb — ini yang perlu hati-hati**
>
> Harga coret/"harga normal" pembanding **hanya boleh dipakai kalau harga itu memang pernah benar-benar berlaku** — dipajang dan bisa dibeli orang di harga segitu, ada buktinya (listing lama, nota, screenshot katalog). Karena 249rb itu **belum pernah dijual** dan dipasang cuma supaya kelihatan diskon 24%, itu bukan "aman" — itu informasi harga menyesatkan dan berisiko kena UU 8/1999 Perlindungan Konsumen. Saya tidak sarankan itu.
>
> Alternatif yang jujur dan tetap menjual:
> - Label **"Harga Spesial Lebaran"** tanpa harga coret palsu.
> - Atau kalau tetap mau ada kesan "diskon", mulai dari harga aman Rp203.500 (margin 40%), lalu diskon beneran — batas maksimal diskon dari harga itu biar margin tetap ≥40%:
>
> **DISKON MAKSIMAL dari Rp203.500: 9% → harga promo Rp185.185** (laba masih di atas margin minimum 40%). Lebih dari itu margin mulai tergerus di bawah 40%.
>
> **Langkah minggu ini:**
> 1. Naikkan harga tayang ke Rp203.500 (atau bulatkan jadi Rp205.000) supaya margin pangan 40% aman.
> 2. Ganti rencana "coret 249rb" dengan label "Harga Spesial Lebaran" atau paket hampers tambahan (isi lebih banyak) — bukan diskon palsu.
> 3. Kalau tetap mau promo, pakai diskon beneran maksimal ~9% dari harga baru.
>
> Catatan: Angka dihitung pakai script dari data yang kakak kasih, keputusan harga tetap di tangan kakak. Soal pajak ini bukan nasihat pajak resmi — kalau mau pasti, cek ke pajak.go.id atau konsultan pajak langganan toko.
### Verifikasi
**Cocokkan dengan script** (`margin --hpp 110000 --harga 189000 --kategori pangan --ppn termasuk`): DPP Rp170.271 + PPN Rp18.729, laba Rp60.271, margin 35,4%, markup 54,79%, DI BAWAH MIN, lantai Rp203.500 — **identik**. Rp205.000 → 40,44% OK — benar.

**Kesalahan berat — klaim "DISKON MAKSIMAL" bertentangan dengan script.** Balasan: "**DISKON MAKSIMAL dari Rp203.500: 9% → harga promo Rp185.185** (laba masih di atas margin minimum 40%)", diulang di Langkah minggu ini ("diskon beneran maksimal ~9%"). Script yang sama (`diskon --harga 203500 --hpp 110000 --kategori pangan --ppn termasuk --diskon 9` dan `--rentang 5-10`) mencetak:
- `Harga saat promo : Rp185.185 -> laba Rp56.834/unit (margin 34,07%)` + `PERHATIAN: margin saat promo 34,07% DI BAWAH minimum 40%`
- `DISKON MAKSIMAL ... harga normal Rp203.500 sudah di/bawah batas ini -> TIDAK ADA ruang diskon` / `0% -> promo diskon TIDAK DISARANKAN`

Logikanya pun jelas: Rp203.500 adalah harga terendah bermargin 40%, jadi diskon berapa pun menembus lantai. Rp185.185 bahkan di bawah harga sekarang Rp189.000 yang sudah DI BAWAH MIN. Ini persis jenis cacat yang ingin dicegah ATURAN KERAS 1.0.6 (harga promo di bawah margin minimum, disertai klaim palsu "masih di atas 40%").

**Python independen** (DPP bulat terbesar dengan DPP + ⌊11% × DPP⌋ ≤ harga): 189.000 → DPP 170.271, PPN 18.729, laba 60.271, margin 35,40%; 203.500 → DPP 183.334, laba 73.334 (40,00%), 203.499 → 39,9998% (jadi Rp203.500 memang terendah); 185.185 → DPP 166.834, laba 56.834, **34,07%**; 205.000 → 40,44%; ÷1,12 → DPP 168.750. Kalimat "margin kakak sekarang 35,4%, bukan 50%-an kalau dihitung dari 189rb mentah-mentah" juga keliru kecil: (189.000 − 110.000) ÷ 189.000 = 41,8%, bukan 50%-an.

**Pemeriksaan khusus:**
- *Aturan harga coret:* **diperbaiki** — "hanya boleh kalau harga itu memang pernah benar-benar berlaku … ada buktinya"; tidak ada lagi saran "jual dulu beberapa hari lalu dicoret"; dasar UU 8/1999 disebut tanpa nomor pasal (jadi tidak perlu tanda PERLU REVIEW). Cacat 1.0.5 #3 teratasi.
- *Margin pangan 40% & lantai:* benar dan dari script.
- *Saran harga di bawah margin minimum:* **gagal** (lihat di atas).
- *PPN:* PMK 131/2024, DPP nilai lain 11/12, efektif 11% — benar; catatan cek pajak.go.id/konsultan ada.

**SEBELUM:** DPP Rp170.270/PPN Rp18.730 (selisih Rp1 pembulatan), margin 35,4%, markup 54,8% — benar; menolak harga coret palsu dengan UU 8/1999 Pasal 10 (benar). Kesalahan: "beda ~2.500/pcs" antara ÷1,12 dan ÷1,11 — seharusnya Rp1.520; dan menyarankan "jual dulu barang di harga lebih tinggi (misal 219rb) buat beberapa hari/minggu, baru turunin" — pola harga coret formalitas yang tetap menyesatkan. Tanpa lantai harga/margin minimum.

### Skor
SEBELUM **7,0/10** — pajak & hukum inti benar, tetapi satu selisih salah hitung, saran harga coret "jual dulu beberapa hari", tanpa lantai harga.
SESUDAH **6,5/10** — PPN, margin, lantai Rp203.500 dan aturan harga coret kini benar dan rapi, tetapi rekomendasi promo utama ("diskon maks 9% → Rp185.185, masih di atas 40%") salah fakta, bertentangan dengan keluaran script, dan mengarahkan pengguna menjual di bawah margin minimum. Skill terpakai (read + exec).

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---|---|
| 1. Tangga reseller/agen + flash sale 25% | 7,0 | 8,0 |
| 2. PKP hampers + jebakan ÷1,12 & harga coret palsu | 7,0 | 6,5 |
| **Rata-rata** | **7,0** | **7,25** |

**VERDIK: BELUM** — cacat 1.0.5 yang diminta teratasi (rentang 15–17% hilang; diskon maksimal skenario 1 persis dari script; aturan harga coret benar), tetapi muncul **kesalahan angka baru yang lebih berat**: di Skenario 2 model menulis "DISKON MAKSIMAL 9% → Rp185.185 (masih di atas margin 40%)" padahal script mencetak 34,07% DI BAWAH MIN dan "TIDAK ADA ruang diskon". Ditambah satu contoh harga agen Rp24.000 di bawah lantai di Skenario 1. Sesudah < 8 dan tidak bebas kesalahan angka. Catatan jujur: tanpa skill model juga cukup baik pada fakta pajak/hukum; pembeda skill ada di lantai harga, batas diskon per kanal, konflik kanal, dan teks siap tempel — tetapi pembeda itu baru bernilai bila tidak dibatalkan oleh angka karangan.

## Cacat untuk pembuat
1. **Model masih menulis label "DISKON MAKSIMAL" dengan angka karangan** — bukti S2: "DISKON MAKSIMAL dari Rp203.500: 9% → harga promo Rp185.185 (laba masih di atas margin minimum 40%)"; script: 0%, TIDAK ADA ruang diskon, 9% = 34,07% DI BAWAH MIN. Saran: (a) di SKILL.md, tambah aturan eksplisit "bila harga normal = lantai (atau di bawahnya), jangan tawarkan diskon persen; tawarkan bonus/paket/kuota" + contoh kasus ini; (b) script `margin` yang mencetak lantai juga mencetak satu baris "Dari harga lantai ini: TIDAK ADA ruang diskon" agar model tidak menghitung sendiri; (c) di Format output, wajibkan kalimat "DISKON MAKSIMAL" hanya ditulis dengan menyalin baris script apa adanya (termasuk "0% -> TIDAK DISARANKAN").
2. **Contoh harga khusus reseller/agen saat promo tidak dicek** — S1: "misal turunkan sementara jadi Rp27.000/Rp24.000"; Rp24.000 = 39,58% DI BAWAH MIN (lantai Rp24.167) dan Rp27.000 > promo Rp26.250. Saran: aturan keras mencakup "harga khusus reseller/agen selama promo" — jalankan `tangga ... --harga-promo <promo> --kategori` dan salin status; atau script `diskon` dengan `--harga-reseller` mencetak "harga khusus reseller tertinggi agar tidak bentrok = promo − Rp1, dan lantai margin = Rp…".
3. **Pembanding "laba normal" saat `--kanal marketplace`** — script memakai laba normal di marketplace (Rp17.000) sebagai pembanding volume (+86,3%), sementara penjualan 500 botol pengguna kemungkinan jual langsung (laba Rp20.500 → butuh 1.124 botol). Saran: script mencetak pembanding yang dipakai ("dibanding harga normal di kanal yang sama") atau keduanya.
4. Minor: "bukan 50%-an kalau dihitung dari 189rb mentah-mentah" — angka tanpa dasar (seharusnya 41,8%).

## Cuplikan jualan
- Dengan skill: "Diskon 25% … harga promo Rp26.250 malah lebih murah dari harga beli reseller & agen … Gabungan semua batas → diskon maksimal yang aman: 14%, harga promo Rp30.100." (tanpa skill: tidak menyadari harga flash sale di bawah harga beli reseller)
- Dengan skill: "Harga coret/'harga normal' pembanding hanya boleh dipakai kalau harga itu memang pernah benar-benar berlaku … ada buktinya." (tanpa skill: menyarankan "jual dulu di 219rb beberapa hari/minggu, baru turunin")
