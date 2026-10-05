# Skenario 03: gabungan TikTok Ads + Google Ads + omzet dari pengguna

- **Penguji:** agent penguji independen (simulasi, Claude Code), 2026-09-25.
- **Usaha fiktif:** brand skincare lokal yang beriklan di TikTok Ads Manager dan Google Ads (Search + Performance Max).
- **Permintaan:** "Gabungin laporan iklan TikTok sama Google minggu ini ya, omzet toko minggu ini 60 juta. Biaya iklan jadi berapa persen dari omzet?"

## Input TikTok Ads Manager (`tiktok.csv`)
```csv
Campaign name,Primary status,Budget,Cost,CPC (destination),CPM,Impressions,Clicks (destination),CTR (destination),Conversions,Cost per conversion,Conversion rate (CVR),Currency
Traffic Video UGC Skincare,Active,300000,1834250,412.19,9860.47,186020,4450,2.39%,57,32179.82,1.28%,IDR
Konversi Serum Vit C,Active,250000,1520700,588.73,14110.61,107770,2583,2.40%,71,21418.31,2.75%,IDR
Live Promo Payday,Inactive,500000,643810,1003.60,23480.12,27420,641,2.34%,0,0,0.00%,IDR
Spark Ads Review Kreator,Active,150000,905440,487.85,10910.53,82988,1856,2.24%,19,47654.74,1.02%,IDR
```

## Input Google Ads: bentuk ekspor tabel Kampanye (`google_mentah.csv`)
```csv
Campaign report
"September 14, 2026 - September 20, 2026"
Campaign status,Campaign,Budget,Budget type,Campaign type,Impr.,Interactions,Interaction rate,Avg. cost,Cost,Clicks,CTR,Avg. CPC,Conversions,Cost / conv.,Conv. value,Currency code
Enabled,Search - Brand Skincare,"150,000.00",Daily,Search,"8,412",913,10.85%,"409.64","374,000.00",913,10.85%,"409.64",48.00,"7,791.67","5,280,000.00",IDR
Enabled,Search - Serum Jerawat,"200,000.00",Daily,Search,"21,775","1,204",5.53%,"1,097.87","1,321,835.00","1,204",5.53%,"1,097.87",36.50,"36,214.66","3,869,000.00",IDR
Enabled,PMax - Semua Produk,"250,000.00",Daily,Performance Max,"96,340","1,702",1.77%,"958.21","1,630,880.00","1,702",1.77%,"958.21",41.25,"39,536.48","4,950,000.00",IDR
Paused,Display - Remarketing,…,0,0,--,--,0.00,0,--,--,0.00,--,0.00,IDR
Paused,Search - Kompetitor,…,0,0,--,--,0.00,0,--,--,0.00,--,0.00,IDR
Paused,Video - Tutorial,…,0,0,--,--,0.00,0,--,--,0.00,--,0.00,IDR
Total: Account,--,--,--,--,"126,527","3,819",3.02%,"873.16","3,326,715.00",…
Total: Search,--,--,--,--,"30,187","2,117",7.01%,"801.07","1,695,835.00",…
Total: Performance Max,--,--,--,--,"96,340","1,702",1.77%,"958.21","1,630,880.00",…
```
Bentuk ini mengikuti pengetahuan penguji tentang unduhan tabel statistik Google Ads: 2 baris judul/periode, kolom `Campaign status` di depan, kolom `Interactions`/`Avg. cost` untuk tampilan campuran tipe kampanye, dan baris `Total: …` di bawah. Google Ads Help "About columns in your statistics table" (https://support.google.com/google-ads/answer/2454071) memastikan kolom `Impr.`, `Cost`, `Avg. CPC`, `Interactions`, `Interaction rate`, dan "Average cost" ada. Bentuk pastinya perlu dicocokkan dengan satu unduhan asli.

### 3a. Google mentah → error (rc=2)
```
{"error": "Kolom wajib tidak terdeteksi otomatis: biaya, tayangan, klik, hasil. … Kolom yang ada di file: ['Campaign report']"}
```
Tidak ada petunjuk bahwa 2 baris pertama perlu dihapus. Agent harus menebak sendiri.

### 3b. Setelah 2 baris judul dihapus → **laporan salah tanpa error** (rc=0)
```
kolom_dipakai: {'nama': 'Campaign status', 'biaya': 'Avg. cost', 'nilai_hasil': 'Conv. value', 'hasil': 'Conversions', 'klik': 'Clicks', 'tayangan': 'Impr.'}

Total belanja iklan: Rp 5.098
Tayangan: 379.581 | Klik: 11.457 | Conversions: 377,25
CPC: Rp 0 | CPM: Rp 13 | CTR: 3,0%
Biaya per Conversions: Rp 14
ROAS: 8296,5x
3 TERBAIK: 1. Total: Account … 2. Total: Search … 3. Enabled …
SARAN 1. Belum ada kampanye yang menonjol …
```
Ada tiga kesalahan sekaligus:
1. **Kolom nama** jatuh ke `Campaign status` karena kata kunci "campaign" cocok dengan kolom pertama (`:229-230`, pencocokan mengikuti urutan kolom di file).
2. **Kolom biaya** jatuh ke `Avg. cost` karena "cost" cocok dan "avg" tidak ada di daftar larangan (`:231-232`).
3. **Baris `Total: Account/Search/Performance Max` ikut dihitung** (`:265`, `:406`).

Isolasi: tanpa kolom status dan tanpa `Avg. cost`, tetapi baris Total dibiarkan, biaya = **Rp 9.980.145**, yaitu 3× dari Rp 3.326.715 yang benar.

### 3c. Google bersih (tanpa judul, tanpa `Campaign status`/`Avg. cost`, tanpa baris Total)
```
LAPORAN IKLAN MINGGUAN — Google Ads
Total belanja iklan: Rp 3.326.715
Tayangan: 126.527 | Klik: 3.819 | Conversions: 125,75
CPC: Rp 871 | CPM: Rp 26.293 | CTR: 3,0%
Biaya per Conversions: Rp 26.455
ROAS: 4,2x

3 PERLU PERHATIAN (biaya per hasil termahal / tanpa hasil)
1. Display - Remarketing: Rp 0 terpakai, 0 Conversions
2. Search - Kompetitor: Rp 0 terpakai, 0 Conversions
3. Video - Tutorial: Rp 0 terpakai, 0 Conversions

SARAN
1. Pertimbangkan naikkan anggaran iklan 'Search - Brand Skincare': biaya per Conversions Rp 7.792, jauh di bawah rata-rata (Rp 26.455).
```
Angka ✅. **Tetapi 3 PERLU PERHATIAN berisi 3 kampanye yang dijeda dengan Rp 0**, sehingga kampanye yang benar-benar mahal (PMax Rp 39.536/konversi, Serum Rp 36.215/konversi) terdorong keluar dari daftar (`:481-484`, `tanpa_hasil` tidak menyaring biaya 0).

### 3d. TikTok (`analisis tiktok.csv --json`)
```
Total belanja iklan: Rp 4.904.200
Tayangan: 404.198 | Klik: 9.530 | Conversions: 147
CPC: Rp 515 | CPM: Rp 12.133 | CTR: 2,4%
Biaya per Conversions: Rp 33.362
3 PERLU PERHATIAN: 1. Live Promo Payday: Rp 643.810 terpakai, 0 Conversions …
SARAN 1. Tinjau/hentikan iklan 'Live Promo Payday': sudah menghabiskan Rp 643.810 tanpa Conversions sama sekali.
Catatan: Tidak ada label mata uang di file; diasumsikan IDR (Rupiah).
```
Angka ✅. Kolom `Currency` (=IDR) diabaikan. Lihat skenario 04 untuk kasus `Currency`=USD.

### 3e. Gabung + omzet
```bash
python3 scripts/laporan_iklan.py gabung tiktok.json google.json --omzet 60000000
```
```
LAPORAN IKLAN MINGGUAN — GABUNGAN SEMUA PLATFORM

Total belanja iklan (semua platform): Rp 8.230.915
- TikTok Ads Manager: Rp 4.904.200 (59,6% dari total), biaya per Conversions: Rp 33.362
- Google Ads: Rp 3.326.715 (40,4% dari total), biaya per Conversions: Rp 26.455
Tayangan: 530.725 | Klik: 13.349 | Conversions: 272,75
CPC: Rp 617 | CPM: Rp 15.509 | CTR: 2,5%
Biaya per Conversions (gabungan): Rp 30.178
ROAS gabungan: 1,7x
Biaya iklan vs omzet: 13,7% dari omzet Rp 60.000.000

SARAN
1. [TikTok Ads Manager] Tinjau/hentikan iklan 'Live Promo Payday': …
2. [Google Ads] Pertimbangkan naikkan anggaran iklan 'Search - Brand Skincare': …
```
**Verifikasi independen:** total Rp 8.230.915, porsi 59,6%/40,4%, CPC 617, CPM 15.509, CTR 2,5%, biaya/konversi gabungan 30.178, **biaya vs omzet 13,7%**: **0 beda**.

**Masalah mode gabung:**
- **Tidak ada peringatan lintas jenis hasil.** Kolom hasil kedua platform bernama "Conversions", jadi pemeriksaan `nama_hasil` berbeda (`:668`) tidak terpicu. Padahal konversi TikTok (atribusi TikTok, bilangan bulat) dan konversi Google (atribusi Google, pecahan 36,50 dan 41,25) **dijumlah menjadi 272,75** dan dibagi menjadi "biaya per Conversions (gabungan)".
- **ROAS gabungan 1,7x menyesatkan.** Pembilangnya hanya nilai konversi Google (Rp 14.099.000), sedangkan penyebutnya biaya kedua platform (`:683`). TikTok tidak punya kolom nilai. ROAS Google sendiri 4,2x. Pengguna bisa menyimpulkan "iklan rugi-rugian" tanpa ada peringatan apa pun.
- Pada uji lain, gabung Meta "pesan WA" dengan Shopee "pesanan": peringatan muncul ✅, tetapi label total tetap "Pesan wa: 360" (chat WA + pesanan Shopee) dan kalimatnya menyebut "di bawah ini", padahal peringatan dicetak di paling bawah. Catatan kurs (`catatan_mata_uang`) dari file USD **hilang** di teks gabung. Saran dipotong 5 teratas menurut urutan file, sehingga saran platform ketiga hilang. File yang sama dimasukkan dua kali tidak dideteksi (biaya dihitung dua kali).

**Hasil skenario:** angka TikTok, Google bersih, dan gabung **cocok 100%**. Ekspor Google yang realistis **gagal** (3a error, 3b angka salah tanpa error). Mode gabung **tidak memberi peringatan** pada kasus lintas jenis hasil yang namanya sama.
