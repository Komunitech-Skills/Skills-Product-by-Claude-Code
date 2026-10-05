# Skenario 06: uji ulang v1.0.1 oleh penguji independen (Akun B)

- **Tanggal:** 2026-09-26
- **Penguji:** agent penguji independen lintas akun (Akun B, simulasi Claude Code). Bukan pembuat skill dan bukan penguji v1.0.0.
- **Lingkungan:** Linux, Python 3.11. Skill disalin ke `…/scratchpad/uji-iklan/skill` dan dijalankan dari sana, tidak dipasang di `.claude/skills`.
- **Aturan kunci jawaban:** semua CSV baru dibuat oleh `gen.py` milik penguji dari data Python, dan kuncinya dihitung dengan `Decimal`. Kode skill **tidak dibaca dan tidak diimpor**. Skill dijalankan lewat `subprocess`, lalu `cek.py` mencocokkan teks laporan, JSON total, dan `--csv-keluaran` per kampanye. Pembulatan: rupiah ke rupiah terdekat (0,5 menjauhi nol), persen/ROAS 1 desimal (0,05 menjauhi nol), perubahan = (sekarang − lalu) ÷ lalu × 100.
- Semua data fiktif.

## 1. Ulang repro HASIL-UJI v1.0.0

| Cacat | Repro diulang | v1.0.1 | Status |
|---|---|---|---|
| **T1** sel `Results` kosong | Skenario 01 apa adanya (`meta_ini.csv` + `meta_lalu.csv`); `kosong.csv` (04 #11) | Rp **4.302.180**, **naik 8,4%** dari Rp 3.970.000, pesan WA 142 (naik 6,8%), biaya/pesan WA Rp **30.297 naik 1,5%**, Retargeting (Rp 356.900, 0 chat) jadi PERLU PERHATIAN no. 1 dan saran no. 1. Catatan menyebut sel kosong, nama iklan, dan biayanya. `kosong.csv` = Rp 620.000 | ✅ **Beres** (cocok 100% dengan kolom "Benar" di `01`) |
| **T2** baris total | Shopee 02A/B; varian C `Total:`, `Total (5 iklan)`, `Total: Account`, `Jumlah Total`, `Grand Total`, `TOTAL`, `Subtotal`; Google `Total: Account/Search/Performance Max` | Semua Rp **2.468.636** / Rp **3.326.715**, dan baris total dicatat. Total di kolom `Urutan` juga dikenali | ✅ **Beres** untuk semua label di repro. Ada sisa untuk label lain, lihat N2 |
| **T3** kolom Google | `google_mentah.csv` (2 baris judul, `Campaign status`, `Avg. cost`, 3 baris `Total:`) | Kolom dibaca: nama=`Campaign`, biaya=`Cost`. Rp 3.326.715, CPC 871, CPM 26.293, CTR 3,0%, 26.455/konversi, ROAS 4,2x. Judul dilewati, periode dibaca dari baris judul | ✅ **Beres** |
| **T4** mata uang | 04 #8 (`Currency`=USD), #9 (`"$1,234.56"`) | Keduanya ditolak (rc=2) dengan sumber deteksi disebut. `--kurs 16350` → Rp 1.828.584 (111,84 × 16.350, cocok) | ✅ **Beres** |
| S1 gabung | 03e TikTok+Google "Conversions"; JSON sama dua kali | ⚠️ atribusi berbeda, dan hasil gabungan diberi label "(perkiraan)". ROAS gabungan 4,2x "(hanya Google Ads)". JSON ganda ditolak | ✅ |
| S2 terbaik/terburuk | Google 3 kampanye dijeda; Shopee 02A | Kampanye Rp 0 hanya dicatat. TERBAIK dan PERLU PERHATIAN tidak beririsan. Gamis tidak lagi disarankan "matikan" (1,9x < 2x rata-rata baru) | ✅ |
| S3 baris judul / UTF-16 | Google mentah; Shopee + 4 baris info toko; UTF-16 bertab | Semua terbaca. UTF-16: Rp 375.000, CTR 10,8%, 7.813/konversi, cocok | ✅ |
| S4 omzet | `"20 juta"`, `"20jt"`, `"750 rb"`, `"Rp20.000.000"`, `"1,5 juta"`, `"20 M"`, `"dua puluh juta"`, `0` | 20.000.000 / 750.000 / 1.500.000 benar. `M` ambigu, teks, dan 0 ditolak (rc=2) | ✅ (`--omzet -5jt` tanpa `=` ditangkap argparse sebagai opsi, rendah) |
| R1/R3/R4/K1 | #7 kurs negatif, #12 `;x`, #13 `(15000)`, #14 tanggal campur 30 hari, #15 xlsx, #17 file tak ada, #19 file sama, #20 JSON asing, #22 timpa input | Semua ditolak atau diberi ⚠️ dengan pesan Bahasa Indonesia. Tidak ada traceback. sha256 file input tidak berubah | ✅ |

## 2. CSV baru buatan penguji + kunci jawaban Decimal

| # | File (bentuk) | Kunci: biaya · hasil · CPC · CPM · CTR · biaya/hasil · ROAS · vs lalu | Skill |
|---|---|---|---|
| K1 | Meta **UI Bahasa Indonesia** (`Nama iklan`, `Jumlah yang dibelanjakan (IDR)`, `Impresi`, `Klik tautan`, `Hasil`), angka format Indonesia `1.030.000` / `"19.807,69"`, 1 sel `Hasil` kosong, **2 minggu** dengan tepi x,x5% | 2.575.000 · 115 · 878 · 12.617 · 1,4% · 22.391 · – · biaya **naik 28,8%** (tepat 28,75%) dari 2.000.000; hasil naik 25,0% dari 92; biaya/hasil naik 3,0% dari 21.739 | ✅ 0 beda (20 nilai rincian). Platform tertulis "Tidak diketahui" (kosmetik) |
| K2 | Meta Inggris `Amount spent (USD)` + `Purchases conversion value`, sel `Results` kosong, kolom `Campaign name`+`Ad set name`+`Ad name` | Tanpa kurs: harus ditolak. `--kurs 16350`: 4.423.002 · 49 · 1.723 · 27.343 · 1,6% · 90.265 · 3,9x | ✅ ditolak. ✅ total 0 beda. ⚠️ dikelompokkan per **Campaign** (1 baris), lihat **N1** |
| K3 | TikTok Ads Manager **harian** (21 baris, kolom `By Day`), `-` di `Conversions`, baris `Total of 3 campaigns` di kolom tanggal, **2 minggu** (minggu lalu 1 kampanye tidak ada) | 3.199.700 · 98 · 574 · 12.986 · 2,3% · 32.650 · – · biaya naik 26,3% dari 2.532.950; hasil naik 16,7% dari 84; biaya/hasil naik 8,3% dari 30.154 | ✅ 0 beda. Total tertangkap **hanya** lewat cek angka, lihat **N2** |
| K4 | TikTok Shop GMV Max **MYR** (kolom `Currency`) dan varian `RM412.60` di sel | Keduanya harus ditolak. `--kurs 3480.5`: 2.438.960 · 59 · 1.276 · 29.740 · 2,3% · 41.338 · 5,5x | ✅ ditolak 2×. ✅ 0 beda (12 nilai) |
| K5 | TikTok Shop IDR Bahasa Indonesia, `Rp1.234.567`, ROI `"7,99"`, kampanye bernama **"Total Look Hijab"**, kampanye Rp 0, baris `Total 4 kampanye` | 2.561.110 · 104 · 651 · 13.515 · 2,1% · 24.626 · 5,5x | ✅ 0 beda (22 nilai). "Total Look Hijab" tetap dihitung, sedangkan "Total 4 kampanye" dilewati |
| K6 | Shopee: 4 baris info toko, `Jumlah` di kolom `Urutan`, `"Rp523.456,5"` / `"Rp99.999,5"`, iklan dijeda, `--omzet "12,5 juta"`, **2 minggu** | 833.456 · 28 · 548 · 12.419 · 2,3% · 29.766 · 4,8x · 6,7% omzet · biaya naik 4,2% dari 800.000; hasil naik 7,7% dari 26; biaya/hasil **turun 3,3%** dari 30.769 | ✅ 0 beda (22 nilai, termasuk 99.999,5 → 100.000) |
| K7 | Google Inggris: 2 baris judul, `Campaign status`, `Avg. cost`, `Currency code`=**USD**, `Total: Campaigns` + `Total: Account`, konversi pecahan | Tanpa kurs: harus ditolak. `--kurs 16410`: 4.200.960 · 52,75 · 2.468 · 49.952 · 2,0% · 79.639 · 10,6x | ✅ ditolak. ✅ 0 beda (17 nilai) |
| K8 | Google **UI Bahasa Indonesia**: `Laporan kampanye`, `Status kampanye`, `Biaya rata-rata`, `Biaya` `"1.321.835,00"`, `Konversi` `"36,50"`, `Nilai konv.`, `Total: Akun` | 3.326.715 · 125,75 · 871 · 26.293 · 3,0% · 26.455 · **4,2x** | ✅ angka 0 beda. ❌ `Nilai konv.` tidak dikenali, sehingga **ROAS hilang tanpa pemberitahuan** dan platform "Tidak diketahui" (R-a) |
| K9 | Meta traffic: kolom `Results` kosong **semua** | 240.000 · 0 · 267 · 6.857 · 2,6% · "-" | ✅ 0 beda. Kedua iklan masuk PERLU PERHATIAN |
| K10 | Satu file berisi IDR dan USD | Harus ditolak, juga dengan `--kurs` | ✅ ditolak 2× |
| K11 | Shopee, baris total **tanpa label** (angka = jumlah) | 500.000 · 15 · 1.000 · 27.778 · 2,8% · 33.333 | ✅ 0 beda + ⚠️ "dianggap baris TOTAL" |
| K12 | Meta Inggris `"1,245,600.50"` / `"68,420"`, 1 iklan di 2 ad set | 2.445.601 · 85 · 1.299 · 19.044 · 1,5% · 28.772 | ✅ total 0 beda. Dikelompokkan per `Ad set name` (N1) |
| Gabung | K1 (pesan WA) + K6 (pesanan) + K4 (MYR, kurs) + `--omzet "50 juta"` | Total 5.847.416 (5.847.416,375); porsi 44,0/14,3/41,7%; CPC 919; CTR 1,8%; ROAS gabungan 5,3x (Shopee + TikTok Shop saja); 11,7% omzet | ✅ 0 beda. Hasil tidak dijumlah (⚠️). Catatan kurs MYR ikut |

**Ringkasan:** 12 file baru + 1 gabung, 11 kasus dihitung dan 6 penolakan wajib. Hasilnya **0 beda** pada total, CPC, CPM, CTR, biaya/hasil, ROAS, dan perubahan minggu-ke-minggu (termasuk tepi 28,75% → 28,8%), serta pada 143 nilai rincian per kampanye yang levelnya sama dengan kunci. Keenam penolakan mata uang (USD, MYR, RM, campur) benar.

## 3. Temuan baru

### N1: Sedang. Ekspor Meta berisi `Campaign name` + `Ad set name` + `Ad name` dirangkum ke level **teratas**
K2: tiga iklan dalam satu kampanye "Kamp" menjadi satu baris. Akibatnya:
- Iklan **Advantage+ Catalog** (Rp 1.080.735, 0 hasil) **tidak muncul** di PERLU PERHATIAN maupun SARAN. Laporan justru menulis "Belum ada kampanye yang menonjol". Ini dampak yang sama dengan T1 lama (iklan terburuk tersembunyi), hanya lewat jalur lain.
- **Catatan menulis angka yang salah:** "Sel 'Results' kosong di 1 baris (Kamp) … biayanya (**Rp 4.423.002**) tetap masuk total". Biaya baris kosong itu sebenarnya Rp 1.080.735. Yang ditulis adalah biaya seluruh kampanye.
- K12: `Ad set name` dipilih, bukan `Ad name`, sehingga laporan menampilkan "Set0/Set1/Set2".
- `--kolom-nama "Ad name"` memperbaiki semuanya (Advantage+ jadi saran no. 1). Namun SKILL.md tidak menyuruh agent memakainya, dan ekspor tingkat iklan dari Ads Manager umumnya memuat ketiga kolom itu.
- Total, CPC, CPM, CTR, dan ROAS tetap benar.
- Saran: bila ada beberapa kolom nama, pakai level **paling rinci** (`Ad name` > `Ad set name` > `Campaign name`), atau tulis levelnya di laporan. Angka biaya di catatan sel kosong harus biaya **baris** tersebut.

### N2: Sedang. Label total di luar daftar tidak dikenali, sehingga dihitung 2× bila angkanya tidak persis sama
Matriks label (baris total Rp 500.001 vs jumlah baris Rp 500.000, di kolom nama dan kolom pertama):
- Dikenali: `Total`, `Total:`, `Total (2 iklan)`, `TOTAL - Semua`, `Total: Akun`, `Total Keseluruhan`, `Jumlah`, `Jumlah Keseluruhan`, `Grand total`, `Summary`, `Ringkasan`, `Sub total`, `Subtotal`.
- **Tidak dikenali:** `Total of 2 campaigns`, `Totals`, `Total Akun`. Hasilnya **Rp 1.000.001 tanpa ⚠️ apa pun**, dan "Total of 2 campaigns" tampil sebagai kampanye di TERBAIK no. 2.
- K3 varian: `Total of 3 campaigns` di kolom tanggal dengan biaya total selisih Rp 0,01 menghasilkan **Rp 6.399.400** (benar 3.199.700). Satu-satunya ⚠️ yang muncul adalah "isi kolom tanggal tidak terbaca … angkanya tetap dihitung", yang tidak menjelaskan bahwa total terhitung dua kali.
- Bila angkanya persis sama, cek angka menangkapnya (K3, K11 ✅). Jadi risikonya bersyarat (label tak biasa **dan** total dibulatkan platform), tetapi hasilnya tetap angka salah diam-diam.
- Saran: kenali awalan `total`/`totals`/`jumlah` diikuti kata apa pun kecuali bila ada nama kampanye lain yang sama. Minimal, tambahkan `total of`, `totals`, dan `total akun`. Beri ⚠️ bila satu baris berisi ≥ 90% dari jumlah biaya baris lain.

### Rendah / kosmetik
- **R-a:** Google UI Indonesia `Nilai konv.` tidak dikenali, sehingga ROAS hilang tanpa catatan. Platform "Tidak diketahui" juga muncul untuk Meta UI Indonesia (K1), TikTok Shop berkolom Inggris (K4), dan Google Indonesia (K8). Angka tidak terpengaruh.
- **R-b:** K3 menulis "Sel 'Conversions' kosong di **1 baris** (Live Payday)", padahal ada 7 baris harian. Hitungannya per kampanye, bukan per baris.
- **R-c:** Shopee `Periode Data,14/09/2026 - 20/09/2026` di baris info toko tidak dipakai sebagai periode (Google "September 14, 2026 - …" terbaca).
- **R-d:** `--omzet -5jt` (tanpa `=`) jatuh ke pesan usage argparse Inggris (rc=2).

## 4. Uji bawaan & validator
- `python3 tests/uji_regresi.py` (salinan scratchpad dan lokasi repo): **49 tes OK**. Tidak ada `__pycache__` yang tertinggal di repo.
- `python3 scripts/validate.py --skill laporan-iklan-mingguan` (root repo): **✅ 1 skill valid, 72 baris katalog sesuai.**

## 5. A/B skenario 01 (ekspor apa adanya)
Pada v1.0.0, A/B "tidak jelas lebih baik" hanya karena T1. Di v1.0.1 keluaran skill untuk File-1 sama dengan kolom "Benar" di `00-pembanding-tanpa-skill.md`: total, arah perubahan, biaya/chat dari total, iklan 0 chat di saran no. 1, dan catatan sampel kecil. Agent tanpa skill tetap salah di biaya/chat (rata-rata kolom Rp 46.615, "turun 18,7%"). **Dengan skill kini jelas lebih baik**, jadi batas skor maks. 6 tidak berlaku lagi. Banding pesaing tidak diulang, karena perubahan v1.0.1 hanya memperkuat sisi skill.
