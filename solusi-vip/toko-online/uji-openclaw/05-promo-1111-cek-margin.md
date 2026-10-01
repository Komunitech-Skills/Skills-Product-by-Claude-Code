# Uji OpenClaw — Toko Online · Promo 11.11 diskon 30% — masih untung? + rencana

Tanggal uji: 2026-10-01 (Asia/Jakarta) · Penguji independen · Skill yang diharapkan: `promo-kalender`

OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`) yang sama dengan bot. SEBELUM = home `kosong-toko-online` (tanpa skill). SESUDAH = home `sol-toko-online` (paket skill solusi terpasang). Pesan identik.

## Pesan member

> kak 11.11 nanti aku mau diskon 30% buat serum wajah aku. harga normal 89rb, modal 41rb. jualnya di shopee potongan admin dll totalnya kira2 12% + 1250 per pesanan. masih untung ga? biasanya sebulan laku 60 botol. bikinin rencana promonya skalian ya

## Balasan SEBELUM (tanpa skill) — utuh

_Alat yang dipakai agent: `tidak ada` · model jawaban: `claude-sonnet-5` · durasi 54 detik_

> Oke, aku itung dulu baru susun rencananya.
>
> **1. Untung per botol pas diskon 30%**
> - Harga promo: Rp89.000 × 70% = **Rp62.300**
> - Fee Shopee (12% + Rp1.250): 12%×62.300 + 1.250 = **Rp8.726**
> - Diterima bersih: 62.300 − 8.726 = **Rp53.574**
> - Modal: Rp41.000
> - **Untung bersih: Rp12.574/botol (margin ~20%)**
>
> Dibanding harga normal (Rp89.000), untung bersihnya **Rp36.070/botol (margin ~40%)**. Jadi diskon 30% itu motong margin hampir separuh — tapi masih positif, bukan jual rugi.
>
> **2. Titik impas vs omzet bulan biasa**
> Kalau target kamu "minimal profitnya nggak kalah sama bulan normal" (60 botol × 36.070 = Rp2.164.200), maka pas promo butuh jual sekitar:
> 2.164.200 ÷ 12.574 ≈ **173 botol** biar total profit-nya samain bulan normal.
>
> Masuk akal nggak? 11.11 biasanya emang bikin lonjakan 2–4x dari hari biasa karena ada boost traffic dari Shopee + orang nunggu tanggal kembar, jadi 150-200an botol dalam periode promo itu realistis asal listing & ads disiapin.
>
> **3. Kalau mau main aman, ini perbandingan tier diskon:**
>
> | Diskon | Harga | Untung/botol | Margin |
> |---|---|---|---|
> | 0% (normal) | 89.000 | 36.070 | 40,5% |
> | 20% | 71.200 | 20.406 | 28,7% |
> | 25% | 66.750 | 16.490 | 24,7% |
> | 30% | 62.300 | 12.574 | 20,2% |
>
> Kalau nggak yakin bisa tembus 150+ botol, 25% udah cukup "nendang" buat 11.11 tapi margin lebih aman.
>
> **4. Rencana Promo 11.11**
>
> *H-7 s/d H-1 (persiapan):*
> - Pastikan stok cukup buat skenario 150-200 botol (jangan sampai out of stock pas puncak)
> - Update foto produk + judul, kasih badge "DISKON 30% 11.11" biar nongol di pencarian
> - Daftar ke Shopee Flash Sale / Kampanye 11.11 kalau toko eligible (biasanya naikin exposure signifikan, worth it meski kuota terbatas)
> - Siapin bundling 2 botol sekali order (misal "beli 2 diskon tambahan dikit") — ini trik bagus karena fee Rp1.250/pesanan jadi dibagi 2 botol, margin per botol ikut naik
> - Mulai teaser di status WA/IG H-3, bikin FOMO ("30% off cuma 11.11, stok terbatas")
>
> *H-Day (11 November):*
> - Pantau stok real-time, update kalau menipis
> - Fast respon chat, karena hari gini persaingan ketat & buyer gampang pindah toko
> - Kalau ada budget, aktifin Shopee Ads buat jam-jam ramai (10.00, 13.00, 20.00-22.00 biasanya puncak)
>
> *H+1 s/d H+3 (follow up):*
> - Cek review masuk, balas cepat biar rating kejaga
> - Rekap: botol terjual, omzet, profit — cocokin sama proyeksi breakeven 173 botol di atas
>
> **Kesimpulan:** diskon 30% masih untung, bukan jual rugi — tapi baru "sepadan" sama bulan biasa kalau laku ±173 botol. Kalau nggak yakin bisa segitu, aku saranin mulai dari 25% dulu atau pakai bundling biar margin lebih tebal tapi tetap menarik.
>
> Mau aku bikinin draft caption/teaser promonya juga?

## Balasan SESUDAH (dengan paket skill) — utuh

_Alat yang dipakai agent: `read, exec` · model jawaban: `claude-sonnet-5` · durasi 127 detik_

> Oke kak, aku udah hitung pakai kalkulator margin biar bukan kira-kira. Ini hasilnya:
>
> **JAWABAN SINGKAT: Diskon 30% MASIH UNTUNG, aman kok.** Tapi laba per botol anjlok lumayan — dari normalnya Rp36.070 jadi cuma Rp12.574/botol (margin turun dari 40,5% jadi 20,2%). Diskon maksimal sebelum rugi itu di angka 46%, jadi 30% masih ada jarak aman.
>
> Asumsi yang kupakai (tolong cek lagi ya):
> • Harga normal Rp89.000, modal Rp41.000
> • Potongan Shopee total 12% + Rp1.250/pesanan (dari kamu)
> • Penjualan normal 60/bulan ≈ 6 botol per 3 hari (periode promo yang kupakai)
>
> *PERBANDINGAN 3 OPSI (per botol, promo 3 hari 10-12 Nov):*
>
> 1️⃣ **Diskon 30%** → harga jadi Rp62.300
> Laba/botol: Rp36.070 → Rp12.574 (margin 20,2%) ✅ AMAN
> Biar laba 3 hari sama kayak hari biasa, harus laku 18 botol (2,87x lipat dari normal)
>
> 2️⃣ **Diskon 25%** (alternatif lebih ringan) → harga jadi Rp66.800
> Laba/botol: Rp16.534 (margin 24,8%) ✅ AMAN
> Butuh 14 botol buat samain laba normal (2,18x)
>
> 3️⃣ **Bundling 2 serum = Rp150.000** (saranku, laba paling tebal)
> Laba/botol: Rp24.375 (margin 32,5%), hemat nyata ke pembeli 15,7%
> Butuh cuma 9 botol (1,48x) buat samain laba normal — jauh lebih ringan
>
> 💡 **Saran:** diskon 30% kamu tetap aman kalau mau tetap pakai itu untuk menarik perhatian. Tapi kalau mau margin lebih tebal dengan risiko lebih kecil, bundling 2 botol Rp150.000 itu laba per botolnya 2x lipat dari diskon 30%. Bisa juga dipakai berbarengan: **bundling jadi promo utama, diskon 30% buat yang beli satuan.**
>
> **RENCANA 11.11 — Serum Wajah**
> Periode: Rabu, 11 Nov 2026 (bisa diperpanjang 10-12 Nov kalau mau 3 hari)
> Target: 18 botol (diskon 30%) atau 9 botol (bundling) biar minimal samai laba hari biasa — anggap ini kebutuhan minimal, bukan jaminan laku
>
> Linimasa:
> • H-14 (28 Okt): fix mekanisme, cek margin lagi kalau harga berubah, siapkan stok (≥25 botol + cadangan), daftar kampanye 11.11 di Seller Center
> • H-7 (4 Nov): mulai teaser — umumin tanggal & promo, ajak follow toko/simpan produk
> • H-3 (8 Nov): broadcast ke pelanggan yang udah opt-in (bukan blast sembarangan)
> • H-1 (10 Nov): cek harga & kuota udah ke-set bener di sistem
> • H (11 Nov): PROMO JALAN — pantau stok & chat tiap 2-3 jam, live kalau bisa
> • H+3 (14 Nov): selesaikan kirim, mulai balas ulasan
> • H+7 (18 Nov): evaluasi — botol laku vs target, laba bersih (bukan omzet), stok sisa
>
> Syarat & ketentuan (draf, tempel di postingan):
> 1. Periode promo: 11 November 2026, 00.00-23.59 WIB
> 2. Harga normal Rp89.000 (harga yang benar-benar berlaku sebelumnya — jangan naikin dulu baru "didiskon")
> 3. Harga promo berlaku selama periode di atas atau sampai stok promo habis (sebutkan kuota pastinya)
> 4. Tidak bisa gabung dengan voucher toko lain
> 5. Dikirim maks 2 hari kerja setelah bayar
>
> Catatan: angka potongan 12%+Rp1.250 itu dari kamu — cek sekali lagi di Seller Center menjelang 11.11 siapa tahu ada perubahan. Ini bukan ramalan penjualan, cuma hitungan biar kamu tahu titik amannya.
>
> Mau aku buatin juga draf caption/materi promonya, atau fokusin ke salah satu opsi dulu (diskon 30% vs bundling)?

## Verifikasi angka & fakta (independen)

Dihitung ulang dengan Python (laba = harga − 12%×harga − 1.250 − 41.000):

| Hal | Hitung ulang | SEBELUM | SESUDAH |
|---|---|---|---|
| Laba normal Rp 89.000 | Rp 36.070 (40,5%) | ✅ | ✅ |
| Diskon 30% → Rp 62.300 | laba Rp 12.574 (20,2%) | ✅ | ✅ |
| Diskon 25% | Rp 66.750 → 16.490 (24,7%); dibulatkan Rp 66.800 → 16.534 (24,8%) | ✅ (66.750) | ✅ (66.800) |
| Diskon 20% → Rp 71.200 | 20.406 (28,7%) | ✅ | — |
| Diskon maksimal sebelum rugi | harga min 48.011,36 → 46,05% | — | ✅ "46%" |
| Bundling 2 = Rp 150.000 | laba/botol 24.375 (32,5%), hemat 15,7% | — | ✅ |
| Unit agar laba promo = laba normal | sebulan: 2.164.200 ÷ 12.574 = 172,1 → 173 · per 3 hari (6 botol normal): 17,2 → 18 · 25%: 14 · bundling: 9 | ✅ 173 (bandingkan 1 bulan penuh) | ✅ 18 / 14 / 9 |
| 11 Nov 2026 | Rabu; H-14 = 28 Okt | — | ✅ |

Catatan: PPh 22 0,5% tidak ditambahkan di kedua sisi; wajar karena member menyebut "potongan admin dll totalnya kira-kira 12%" (bila belum termasuk, laba diskon 30% turun ke Rp 12.263).

Kesalahan/kelemahan:
- **SEBELUM:** pembanding "173 botol" memakai laba **sebulan penuh** padahal promo 11.11 hanya 1–3 hari — target menyesatkan (terdengar mustahil/terlalu besar). Klaim tanpa dasar: "11.11 biasanya bikin lonjakan 2–4x", "150–200an botol realistis" (padahal itu 2,5–3,3x penjualan sebulan), jam puncak iklan "10.00, 13.00, 20.00–22.00". Menyarankan teaser "stok terbatas" untuk FOMO tanpa menyebut kuota nyata (berisiko klaim menyesatkan). Tidak ada S&K promo.
- **SESUDAH:** asumsi periode 3 hari (10–12 Nov → normal 6 botol) tetapi rencana & S&K memakai 1 hari (11 Nov 00.00–23.59) dengan target tetap 18 botol — tidak konsisten (untuk 1 hari, pembanding normal ±2 botol → ±6 botol). S&K butir "Dikirim maks 2 hari kerja" adalah janji yang tidak diberikan pemilik (seharusnya ditandai sebagai isian).

## Nilai

| | SEBELUM | SESUDAH |
|---|---|---|
| Skor (1–10) | 6.5 | 8.0 |

- **SEBELUM 6,5/10** — angka per botol benar dan tabel tier diskon berguna, tapi target 173 botol salah kerangka (sebulan vs periode promo), beberapa klaim pasar tanpa dasar, dan anjuran "stok terbatas" tanpa kuota.
- **SESUDAH 8/10** — skill terpakai (`read` + `exec` `cek_promo.py`). Jawaban langsung "MASIH UNTUNG", batas diskon 46%, 3 opsi dihitung (termasuk bundling yang labanya 2x), target realistis per periode, linimasa bertanggal (hari & tanggal benar), S&K dengan peringatan harga coret palsu. Minus: inkonsistensi 3 hari vs 1 hari dan satu janji pengiriman yang dikarang di S&K.

Kriteria: ketepatan, langsung siap pakai, kepatuhan aturan Indonesia, keamanan/privasi, kejelasan untuk awam.
