# HASIL UJI: laporan-iklan-mingguan v1.0.0

- **Tanggal:** 2026-09-25
- **Penguji:** agent penguji independen (simulasi, Claude Code), bukan pembuat skill. Hanya membaca folder skill ini (+ contoh format HASIL-UJI `laporan-harian-usaha`).
- **Lingkungan:** Linux, Python 3.11. Skill disalin ke scratchpad (`…/scratchpad/uji-iklan/skill`), tidak dipasang di `.claude/skills` repo. Semua data uji dibuat penguji (fiktif): Meta 6 iklan ×2 minggu, Shopee 5 iklan 28 kolom + baris Total, TikTok 4 kampanye, Google Ads 6 kampanye (mentah/berjudul/bersih), dan 20+ file rusak.
- **Uji regresi bawaan:** `tests/uji_regresi.py` → 19 tes OK (dijalankan ulang, bukan dasar penilaian).
- **Validator:** `python3 scripts/validate.py` → 60 skill valid, 60 baris katalog sesuai.
- **Uji muat OpenClaw:** `bash scripts/uji_openclaw.sh` → OpenClaw **2026.9.6**: `laporan-iklan-mingguan` ada di `eligible`, `modelVisible`, `commandVisible` (60/60 lulus).
- **Uji jadwal OpenClaw sungguhan:** gateway `--dev` (2026.9.6, `HOME=/tmp/uji-openclaw/home`):
  - Perintah **persis** dari `references/openclaw-jadwal.md` §3 (`automations add "0 7 * * 1" "<pesan>" --name … --tz Asia/Jakarta --session isolated --announce --channel telegram --to …`) **diterima**. `schedule={cron,"0 7 * * 1",Asia/Jakarta}`, `nextRunAtMs` = 2026-09-28 00:00 UTC = **Senin 07:00 WIB** ✅. Semua flag (`--name --tz --session --announce --channel --to`) ada di `automations add --help` ✅.
  - `automations run --wait` untuk job agent itu gagal karena tidak ada API key model (`No route-compatible authentication source is configured for openai`). Ini wajar di lingkungan uji. Perilaku agent **tidak** teruji.
  - Job `--command-argv '["python3",".../laporan_iklan.py","analisis",…]'` + `run --wait` → `status: ok`, `summary` = teks laporan lengkap, **sama persis** dengan uji terminal. `completionStatus: failed` hanya karena kanal Telegram belum dikonfigurasi. Kedua job dihapus dan gateway dihentikan.
- **Platform teruji:** `claude-code (simulasi agent)`; `openclaw (uji muat otomatis + automations add/run command)`. Pengiriman Telegram **tidak** diuji.

## Audit keamanan singkat
Script hanya memakai library standar (`argparse, csv, io, json, re, sys, collections, datetime, decimal`), **tanpa jaringan**, tanpa `subprocess/eval/os.system`, tanpa baca kredensial. Hanya membaca file yang diberikan dan menulis `--csv-keluaran` bila diminta. Tidak ada prompt injection di SKILL.md/README/references. Tidak ada data pelanggan. Formula injection nama kampanye (`= + - @ tab spasi`) tertangani. **Lulus**, dengan catatan rendah R4.

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B skenario 01 (ekspor apa adanya & sel 0) | **Tidak jelas lebih baik**: menang di file bersih, **kalah** di ekspor Meta apa adanya (total & arah % salah) |
| 00 | `00-banding-pesaing.md` | marketingskills `ads` (51k★), claude-ads (9,5k★), kein-s/meta-ads-report | Tidak kalah (32 vs 20/19 di file bersih; 23 di ekspor apa adanya) |
| 01 | `01-meta-wa-minggu-ini-vs-lalu.md` | Meta 6 iklan, chat WA, vs minggu lalu | **Gagal** (apa adanya: −Rp 356.900, arah % terbalik, iklan 0 hasil hilang). Varian sel 0: angka 100% cocok |
| 02 | `02-shopee-format-indonesia-baris-total.md` | Shopee "Rp1.234.567"/"2,50%"/",5" + baris Total | Varian "Total" di Nama Iklan: **lulus**, 100% cocok. Total di kolom lain / "Total:" / "Total (5 iklan)": **dihitung 2×** |
| 03 | `03-gabung-tiktok-google-omzet.md` | TikTok + Google + omzet 60 jt | TikTok, Google bersih, gabung: 100% cocok. Google realistis: **error / Rp 5.098, ROAS 8296x**. Gabung: **tanpa peringatan**, ROAS gabungan menyesatkan |
| 04 | `04-input-buruk.md` | 23 kasus (kosong, kolom asing, USD, rusak, tanggal campur, xlsx, UTF-16, omzet "20 juta", timpa file) | Tanpa crash/traceback. **3 angka salah diam-diam** (USD di kolom `Currency`, simbol `$`, sel kosong) |
| 05 | `05-di-luar-cakupan.md` | Login otomatis Meta, jamin ROAS 5x, broadcast grup WA, klaim kesehatan | **Lulus**; 3 celah instruksi rendah |

## Verifikasi angka independen
Hitung ulang dengan `fractions.Fraction`/`Decimal` di `verif.py` milik penguji (tidak mengimpor kode skill). Aturan: rupiah terdekat 0,5 menjauhi nol, persen 1 desimal 0,05 menjauhi nol.
| Diuji | Hasil |
|---|---|
| Meta (sel 0): total, tayangan, klik, CPC, CPM, CTR, biaya/chat, 3 % vs minggu lalu, rata-rata saran, 4,5x; rincian CSV 6 iklan × 5 metrik | **0 beda** |
| Meta USD × kurs 16.350 | **0 beda** |
| Shopee (Total di Nama Iklan): total 2.468.635,5 → 2.468.636, CPC 50.000,5 → 50.001, CPM, CTR, biaya/pesanan, ROAS 3,5x, % omzet 9,9%, 6,8x/2,0x; rincian 5 iklan × 6 metrik | **0 beda** |
| TikTok, Google bersih, gabung (porsi 59,6/40,4%, CPC/CPM/CTR gabungan, 30.178, 13,7% omzet) | **0 beda** |
| Metrik dari total, bukan rata-rata kolom (`Cost per results` rata-rata 46.615 vs benar 30.297) | ✅ skill memakai total |
| Baris total tidak dihitung dua kali | ✅ hanya bila persis "total/jumlah/grand total…" di kolom nama; ❌ bentuk lain (T2) |
| `bandingkan_persen`/`bulat_rupiah`/CTR vs acuan Fraction: 60.000 kasus acak | **0 beda** |
| Persen tepat x,x5 (kasus tepi) | ❌ **202 beda** (float), mis. 103.000 vs 80.000 = 28,75% → skill 28,7% (R2) |
| Ekspor Meta apa adanya / Google realistis / USD tanpa label | ❌ angka salah (T1, T2, T3, T4) |

## Temuan cacat
| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| **T1** | **Tinggi** | `scripts/laporan_iklan.py:410-423` (+ `parse_angka` `:102-106`) | **Sel metrik kosong → seluruh baris dibuang**, termasuk biayanya. Ekspor Meta mengosongkan `Results` untuk iklan tanpa hasil, jadi iklan terburuk hilang, total biaya kurang, dan arah % bisa terbalik. Repro: `printf 'Campaign name,Cost,Impressions,Clicks (destination),Conversions\nA,500000,40000,900,20\nB,120000,9000,150,\n' > k.csv; python3 scripts/laporan_iklan.py analisis k.csv` → Rp 500.000 (benar Rp 620.000). Skenario 01: Rp 3.945.280 "turun 0,6%" (benar Rp 4.302.180, naik 8,4%). Saran: sel kosong/`--`/`-` pada metrik hitungan = 0 (dicatat di `catatan`), baris hanya dibuang bila biaya tidak terbaca. Peringatan harus menyebut nama iklan & biaya yang dibuang. |
| **T2** | **Tinggi** | `:265-266`, `:405-408` | **Baris total hanya dikenali bila teksnya persis** "total/jumlah/grand total/…" **di kolom nama**. "Total" di kolom pertama (nama kosong → "Kampanye #6" masuk 3 TERBAIK), "Total:", "Total (5 iklan)", "Jumlah Total", Google "Total: Account/Search/…" semuanya dihitung lagi (2×–3×) **tanpa peringatan**. Repro: skenario 02 varian B/C; skenario 03 isolasi → Rp 9.980.145 (benar 3.326.715). Saran: kenali awalan `total`/`jumlah` di **kolom teks mana pun**, dan/atau cek "baris yang angkanya = jumlah baris lain". |
| **T3** | **Tinggi** | `:229-232`, `:290-300` | **Pemetaan kolom Google Ads salah tanpa error**: pencarian mengambil kolom **pertama** di file yang mengandung kata kunci, sehingga `nama` = `Campaign status` ("campaign") dan `biaya` = `Avg. cost` ("cost", tanpa larangan "avg"). Hasil: "Total belanja iklan: Rp 5.098 … ROAS: 8296,5x", dikelompokkan per status. Repro: skenario 03b. Saran: urutkan pencocokan menurut prioritas kata kunci (persis dulu), larang `avg`/`status`/`id`/`type`/`budget`, dan tolak/peringatkan bila ROAS > 50x atau CPC < Rp 10. |
| **T4** | **Tinggi** | `:111-113`, `:335-340`, `:391` | **Mata uang asing lolos sebagai Rupiah** bila label tidak berbentuk `(USD)` di judul kolom: kolom `Currency`/`Currency code` = USD diabaikan, simbol `$`/`USD` di sel dibuang diam-diam. Ini bertentangan dengan klaim README "Menolak diam-diam kalau file ternyata mata uang asing". Repro: `printf 'Campaign name,Cost,Impressions,Clicks (destination),Conversions,Currency\nA,111.84,186020,4450,57,USD\n'` → "Rp 112"; sel `"$1,234.56"` → "Rp 1.235". Saran: baca kolom `Currency`/`Currency code`/`Mata uang` dan simbol mata uang di sel, lalu tolak seperti label `(USD)`. |
| **S1** | **Sedang** | `:644-693` (`:668`, `:683`) | **Mode gabung**: (a) peringatan "hasil berbeda" hanya dari **nama** kolom, jadi TikTok "Conversions" + Google "Conversions" (atribusi berbeda, pecahan 36,50) dijumlah 272,75 tanpa peringatan; (b) **ROAS gabungan** = nilai platform yang punya nilai ÷ biaya **semua** platform (1,7x vs Google 4,2x) tanpa peringatan; (c) `catatan_mata_uang` (kurs) hilang di teks gabung; (d) label hasil memakai nama platform pertama ("Pesan wa: 360" = chat + pesanan Shopee); (e) file yang sama dua kali tidak dideteksi; (f) saran dipotong 5 menurut urutan file. Repro: skenario 03e. |
| **S2** | **Sedang** | `:480-484` | (a) Kampanye dijeda **Rp 0 / 0 hasil** mengisi "3 PERLU PERHATIAN" dan menggeser kampanye mahal (Google bersih: 3 kampanye Paused); (b) daftar **terbaik & perlu perhatian bertumpuk** bila ≤ 5 kampanye. Satu iklan bisa muncul di "3 TERBAIK" dan disarankan "Tinjau/matikan" sekaligus (skenario 02A: Gamis; juga contoh pembuat sendiri). Saran: saring biaya 0; tampilkan terbaik/terburuk tanpa irisan. |
| **S3** | **Sedang** | `:146-166`, `:150` | Baris judul sebelum header (Google "Campaign report" + periode; info toko Shopee) tidak ditangani dan tidak diberi petunjuk ("Kolom yang ada di file: ['Campaign report']"). CSV UTF-16 bertab (unduhan "Excel CSV" Google) tidak didekode. SKILL.md tidak menyebut kedua hal ini. Saran: cari baris header dalam 10 baris pertama; dukung BOM UTF-16. |
| **S4** | **Sedang** | `:759-765` | `--omzet "20 juta"`/`"20jt"` dibaca **Rp 20** → "24521000,0% dari omzet Rp 20". Pengguna awam menyebut omzet dalam "juta". Saran: kenali `rb/ribu/jt/juta/M/miliar`, atau tolak bila ada huruf. |
| R1 | Rendah | `:243`, `:472-477` | Periode Meta tidak terbaca (`Reporting starts/ends`). Rentang tanggal > 7 hari (uji: 30 hari) tetap berjudul "MINGGUAN" tanpa peringatan. Tanggal tak terbaca (`09/16/2026` saat dmy, `kemarin`) diabaikan diam-diam. `--sebelumnya` = file yang sama tanpa peringatan. |
| R2 | Rendah | `:547-548` | Pembagian `float` sebelum `Decimal`: persen tepat x,x5 bisa turun satu digit (103.000 vs 80.000 → 28,7%, seharusnya 28,8%). 202 kasus tepi. Saran: hitung dengan `Decimal`/`Fraction`. |
| R3 | Rendah | `:376`, `:788`, `parse_angka` | `--kurs -16350` diterima (biaya negatif, saran terbalik). Biaya negatif `(15000)` diterima tanpa peringatan. Sel `"250.000,00;x"` dibaca 250.000. |
| R4 | Rendah | `:740-753`, `:846-847` | `--csv-keluaran` = path input → **file ekspor asli ditimpa**. Judul kolom dari `--nama-hasil` tidak disanitasi (`=1+1`). Di CSV, `tayangan`/`klik` diformat "68.420" (titik ribuan) sementara `ctr_persen` "1.6" (titik desimal), sehingga Excel bahasa mana pun salah membaca salah satunya. |
| R5 | Rendah | `:489-511`; `SKILL.md` Batasan | Saran "Tinjau/matikan" untuk 4 chat/1 pesanan tanpa catatan sampel kecil. "Rata-rata" di saran (tanpa iklan 0 hasil) ≠ "Biaya per hasil" di atasnya (27.784 vs 30.297), membingungkan. Biaya Meta/Google di Indonesia ditagih + PPN (PMSE), dan "Biaya iklan vs omzet" tidak menyebutnya (perlu dicek pemilik). |
| R6 | Rendah | `SKILL.md` "Kapan TIDAK" | Tidak ada instruksi bila pengguna **menempelkan password** di chat (ingatkan ganti password/2FA, jangan diulang/disimpan). Jalur "API resmi + token" tidak disebut sebagai ditolak. |
| R7 | Rendah | `references/openclaw-jadwal.md` §3 | Contoh jadwal hanya bentuk **agent** ("Tulis ringkas…"), sehingga LLM menulis ulang angka setiap Senin, bertentangan dengan Langkah 4 "jangan mengubah angka". Bentuk `--command-argv` (terbukti jalan di atas, deterministik) tidak dicontohkan. Nama file mingguan yang berubah (`meta-YYYY-MM-DD.csv`) tidak punya resep. |
| R8 | Rendah | `references/sumber-kolom.md` | Halaman TikTok yang dirujuk hanya menyebut CPM/CPC/CTR/CVR (dicek penguji), jadi nama `Clicks (destination)`/`Total onsite value` bersandar pada sumber pihak ketiga. Google Ads Help kini juga memuat kolom **`Results` / `Results value`**. `Results value` tidak dikenali sebagai nilai hasil, sehingga ROAS hilang tanpa pemberitahuan. |
| K1 | Kosmetik | `:582`, `:706`, `:546`, `:550`, `:630`, `:815`, `:889` | "Pesan wa" (`capitalize`); peringatan berupa `dict` Python; "Hasil: naik dari **Rp** 0" untuk jumlah hasil; "(tetap (0,0%) dari minggu lalu)"; errno Inggris; `Terjadi kesalahan tak terduga: 'total'`; peringatan gabung menulis "di bawah ini" padahal dicetak paling bawah; pesan `.xlsx` = "File kosong…". |

## Skor kualitas: **5 / 10**
Alasan:
- (+) Aritmetika inti benar dan transparan: 0 beda di 4 platform + gabung + 60.000 kasus acak. Metrik dihitung dari total (bukan rata-rata kolom), pembulatan 0,5 benar, format Rupiah konsisten, penolakan `(USD)` + `--kurs` tercatat. Pembagi nol aman, tanpa crash di 23 input buruk.
- (+) Aman & privat: tanpa jaringan/kredensial/data pelanggan; formula injection nama kampanye tertangani; penolakan login/scraping & "jaminan ROAS" sesuai keputusan pemilik; lolos uji muat OpenClaw 2026.9.6 dan `automations add/run` sungguhan.
- (+) Konteks lokal kuat (Shopee/TikTok Shop, bahasa awam, Telegram); tidak kalah dari pesaing publik.
- (−) **T1–T4: empat jalur angka salah secara diam-diam pada bentuk ekspor yang realistis** (sel kosong Meta, baris Total/Google, kolom Google, mata uang di kolom terpisah). Laporan ini dikirim otomatis ke pemilik tiap Senin, jadi angka salah yang terlihat meyakinkan adalah risiko terbesar.
- (−) **A/B tidak jelas lebih baik** pada skenario normal pertama dalam bentuk ekspor apa adanya. Sesuai `CLAUDE.md` Tahap 6 no. 4, skor **maks. 6**. Dikurangi lagi karena T2–T4 juga menjatuhkan skenario 02B dan 03.
- (−) S1–S4: mode gabung tanpa peringatan pada kasus yang paling sering (nama kolom sama), daftar PERLU PERHATIAN bisa diisi kampanye Rp 0, baris judul Google/Shopee tidak ditangani, omzet "20 juta".

**Keputusan: TIDAK LULUS (< 7). Revisi dulu, jangan naik status.**
Prioritas revisi: T1 → T2 → T3 → T4 (masing-masing + tes regresi dengan file berbentuk ekspor asli, sebaiknya satu ekspor nyata per platform dari pemilik), lalu S1–S4. Setelah itu **uji ulang oleh penguji independen**, terutama skenario 01 (ekspor apa adanya), 02B/C, 03a/b, dan 04 #8/#9/#11/#18.

---

## Uji ulang v1.0.1 (Akun B)

- **Tanggal:** 2026-09-26. **Penguji:** agent independen lintas akun (Akun B, simulasi Claude Code). Bukan pembuat skill dan bukan penguji v1.0.0. Skill dijalankan dari salinan scratchpad.
- **Rincian lengkap:** `06-uji-ulang-v1.0.1.md`.
- **Uji bawaan:** `tests/uji_regresi.py` menghasilkan 49 tes OK. `python3 scripts/validate.py --skill laporan-iklan-mingguan` menghasilkan ✅ 1 skill valid, 72 baris katalog sesuai.

### Status cacat v1.0.0
| ID | Status v1.0.1 | Bukti |
|---|---|---|
| T1 sel kosong | ✅ Beres | Skenario 01 apa adanya: Rp 4.302.180, naik 8,4%, 30.297/chat naik 1,5%, Retargeting jadi saran no. 1 |
| T2 baris total | ✅ Beres untuk semua label di repro (`Total:`, `Total (5 iklan)`, `Total: Account`, `Jumlah Total`, kolom pertama, Google 3× `Total:`). Masih ada sisa, lihat N2 | 02B/C, 03b |
| T3 kolom Google | ✅ Beres | `Campaign`/`Cost` dipilih, Rp 3.326.715, ROAS 4,2x |
| T4 mata uang | ✅ Beres | `Currency`=USD/MYR, `$`, `RM`, dan file campur semuanya ditolak. Konversi dengan `--kurs` cocok |
| S1–S4 | ✅ Beres | Gabung memberi ⚠️ atribusi dan ROAS "hanya Google Ads". Rp 0 tidak dinilai. Tidak ada irisan. Judul/UTF-16 terbaca. Omzet "20 juta/750 rb/1,5 juta" benar dan "20 M" ditolak |
| R1, R3, R4, K1 | ✅ Beres | Repro 04 #7, 12–15, 17, 19, 20, 22 memberi ⚠️ atau pesan jelas, tanpa traceback |

### Uji baru (12 CSV + 1 gabung, kunci `Decimal` independen, kode tidak dibaca)
Meta UI ID/EN/USD, TikTok Ads harian, TikTok Shop MYR/RM/IDR, Shopee dengan info toko dan `Jumlah`, Google EN-USD dan UI ID, `Results` kosong semua, mata uang campur, total tanpa label, dan 3 file dua minggu (termasuk tepi 28,75% → 28,8%):
- **0 beda** pada total, CPC, CPM, CTR, biaya/hasil, ROAS, dan perubahan minggu-ke-minggu, serta pada 143 nilai rincian.
- **6/6 penolakan mata uang benar.**

### Temuan baru
| ID | Keparahan | Temuan |
|---|---|---|
| **N1** | Sedang | Bila ada `Campaign name` + `Ad set name` + `Ad name`, laporan dirangkum ke level **teratas**. Akibatnya iklan 0 hasil senilai Rp 1.080.735 tersembunyi ("Belum ada kampanye yang menonjol"), dan Catatan sel kosong menulis biaya **kampanye** (Rp 4.423.002) sebagai biaya baris kosong. Total tetap benar. `--kolom-nama "Ad name"` memperbaikinya, tetapi SKILL.md tidak menyuruh agent memakainya |
| **N2** | Sedang | Label `Total of N campaigns`, `Totals`, dan `Total Akun` tidak dikenali. Bila angkanya tidak persis sama dengan jumlah baris (misalnya selisih pembulatan Rp 0,01 atau Rp 1), baris itu **dihitung 2× tanpa ⚠️** (Rp 1.000.001; TikTok harian Rp 6.399.400 vs 3.199.700). Bila angkanya persis sama, cek angka menangkapnya |
| R-a | Rendah | Google UI ID `Nilai konv.` tidak dikenali, sehingga ROAS hilang tanpa catatan. Platform tertulis "Tidak diketahui" untuk Meta UI ID, TikTok Shop berkolom Inggris, dan Google ID |
| R-b/c/d | Rendah | "1 baris" kosong padahal 7 baris harian. `Periode Data` Shopee tidak dibaca. `--omzet -5jt` jatuh ke usage argparse |

### Skor kualitas: **7 / 10**
Alasan:
- (+) Keempat cacat tinggi dan S1–S4 terbukti beres dengan repro asli. Dari 11 kasus baru dengan kunci independen, 0 beda. Semua mata uang asing ditolak. Tidak ada traceback. Uji regresi bawaan bertambah dari 19 menjadi 49 tes.
- (+) A/B skenario 01 (ekspor apa adanya) kini **jelas lebih baik** daripada tanpa skill, jadi batas maks. 6 tidak berlaku lagi.
- (−) N1: ekspor Meta tingkat iklan yang umum (dengan kolom kampanye) menyembunyikan iklan terburuk dan mencetak satu angka salah di Catatan.
- (−) N2: masih ada jalur angka salah diam-diam untuk label total yang tidak biasa, bila totalnya tidak persis sama.
- (−) Bentuk ekspor asli dari kelima platform tetap **belum diverifikasi** dengan file nyata (PERLU REVIEW, diakui pembuat).

**Keputusan: LULUS (≥ 7), dengan syarat.** N1 dan N2 sebaiknya diperbaiki (keduanya kecil) dan ditambah tes regresi sebelum uji platform asli/beta. Minta pemilik menyediakan satu ekspor asli per platform. Setelah N1/N2 diperbaiki, uji ulang singkat cukup untuk K2, K12, dan matriks label total.

## Uji ulang v1.0.2 (Akun B)

- **Tanggal:** 2026-09-26. **Versi:** v1.0.2 (commit `b2a286c`). **Penguji:** agent independen lintas akun (Akun B, simulasi Claude Code), bukan pembuat. Skill dijalankan dari salinan scratchpad.
- **Rincian lengkap:** `07-uji-ulang-v1.0.2.md`.
- **Uji bawaan:** `tests/uji_regresi.py` menghasilkan 63 tes OK. `python3 scripts/validate.py --skill laporan-iklan-mingguan` menghasilkan ✅ 1 skill valid, 77 baris katalog sesuai.

### Status temuan v1.0.1
| ID | Status v1.0.2 | Bukti |
|---|---|---|
| N1 ekspor bertingkat | ✅ Beres | K2: Advantage+ Catalog jadi PERLU PERHATIAN no. 1 dan saran no. 1, Catatan menulis Rp 1.080.735. K12 dibedakan per ad set. P1/P2/P3/P9/P10 baru (Meta/TikTok 3 level, Google grup iklan, Meta ID 2 level, `Ad name` kosong) juga benar |
| N2 label total | ✅ Beres untuk label di matriks | 16 label × 2 posisi = 32/32 → Rp 500.000. K3 varian ×3 → Rp 3.199.700. `Totals` +1,5%, `Total Akun` +Rp 3, label huruf campur atas/bawah, `Grand Total` di atas + `Subtotal:` di tengah semuanya benar. Label asing ±1% dibuang + ⚠️. Kampanye asli dominan tetap dihitung + ⚠️ |
| "Total Look Hijab" dsb. | ✅ | "Total Look Hijab", "Jumlah Terbatas - Khimar", "Totalitas Gamis", "Total Diskon 50% Bergo", dan induk "Jumlah Promo Ramadan" tetap dihitung |
| T1–T4, S1–S4, R1/R3/R4/K1, R-b | ✅ Tetap beres | Repro asli diulang, angka sama dengan v1.0.1 |
| R-a, R-c, R-d | Belum (rendah) | K8 `Nilai konv.` masih tanpa ROAS |

### Uji baru (14 CSV, kunci `Decimal` independen, kode tidak dibaca)
11/14 kasus 0 beda, dengan **322 nilai cocok**. Tiga kasus gagal:
| ID | Keparahan | Temuan |
|---|---|---|
| **M1** | Sedang | Kampanye bernama **"Total 12.12 Flash Sale"** / **"Jumlah 2 Pcs Bundling"** (kata kepala + angka) dibuang sebagai baris total, **tanpa ⚠️** walau biayanya jauh dari jumlah baris lain. Hasilnya Rp 150.000, padahal seharusnya Rp 1.000.000. Hanya Catatan yang menyebutnya. Perbaikan kecil: ⚠️ selisih untuk semua label yang dibuang, bukan hanya label "sedang", dan "angka + kata lain" diperlakukan sebagai nama |
| M2 | Rendah | Label tak dikenal dengan ketiga metrik selisih 3% (di atas batas 2%) → dihitung 2× tanpa ⚠️. Sesuai rancangan |
| M3 | Rendah | `Subtotal Kamp A` (tanpa titik dua) di kolom induk dengan kolom nama kosong → dihitung sebagai data, sehingga total 2×. Hanya pada lembar buatan admin |

### Skor kualitas: **8 / 10**
Alasan:
- (+) N1 dan N2 terbukti beres dengan repro asli dan 14 file baru: ekspor 2/3 level dirinci ke iklan, iklan tanpa hasil muncul di PERLU PERHATIAN/SARAN, Catatan memakai biaya baris, label umum di posisi mana pun dikenali, dan pengaman ±2% bekerja ke dua arah (buang + ⚠️, atau hitung + ⚠️).
- (+) Tidak ada regresi pada T1–T4/S1–S4/R. 322 nilai baru cocok dengan kunci independen. Uji bawaan bertambah menjadi 63 tes.
- (−) M1: masih ada satu jalur angka salah tanpa ⚠️ untuk nama kampanye yang wajar di pasar Indonesia ("Total 12.12 …"), meski syaratnya sempit dan Catatan menyebut barisnya.
- (−) Bentuk ekspor asli kelima platform tetap **belum diverifikasi** dengan file nyata (PERLU REVIEW).

**Keputusan: LULUS.** Disarankan memperbaiki M1 (dengan tes regresi) sebelum beta; cukup uji ulang singkat P5/P2/P8b. Uji platform asli tetap membutuhkan satu ekspor asli per platform dari pemilik.

## Uji ulang independen v1.0.3 (Akun B, 2026-09-26)

- **Versi:** v1.0.3 (commit `e63c127`). **Penguji:** agent independen lintas akun (Akun B, simulasi Claude Code), bukan pembuat. Skill dijalankan dari salinan di scratchpad.
- **Rincian:** `08-uji-ulang-v103-akun-b.md`.
- **Regresi:** `tests/uji_regresi.py` menjalankan 78 tes, semuanya OK. `validate.py --skill laporan-iklan-mingguan` menghasilkan ✅ 1 skill valid, 80 baris katalog sesuai.

| ID | Status | Bukti |
|---|---|---|
| M1 | ✅ Beres | `Total 12.12 Flash Sale`, `Jumlah 2 Pcs Bundling`, `Total 12.12`, `TOTAL SALE` (juga saat dominan) dihitung. Setiap baris total/subtotal yang dikecualikan diberi ⚠️ nama + biaya |
| M2 | ✅ Sesuai SKILL.md | Selisih +3% → dihitung + ⚠️ "TERHITUNG DUA KALI" |
| M3 | ✅ Sesuai SKILL.md | `Subtotal Kamp A` cocok → dibuang + ⚠️. Yang tidak cocok → dihitung + ⚠️ |

**Uji baru.** Ada 9 CSV (Meta EN/ID, Google `--` + judul + `Total:` berlapis, Shopee angka Indonesia + `Total` di atas, TikTok harian + subtotal, TikTok Shop `Jumlah`) dengan kunci `Decimal` independen. Hasilnya **7/9 cocok tanpa selisih** pada biaya, CPC, dan ROAS.

| ID | Keparahan | Temuan |
|---|---|---|
| **N3** | Sedang | Subtotal buatan lembar kerja di kolom nama yang memuat nama kampanye (`Subtotal: Retarget Video`, `Retarget Video Total`) → dihitung 2× **tanpa ⚠️** untuk barisnya. Repro: Rp 294.240, padahal seharusnya Rp 202.120. Di file TikTok harian: Rp 1.102.543, padahal seharusnya Rp 597.331. Bukan regresi (v1.0.2 sama) dan tidak terjadi pada ekspor platform asli. |
| R-e | Rendah | ⚠️ M2 positif palsu untuk kampanye sah yang dominan (+4,7%). Kalimat "TERHITUNG DUA KALI" perlu dilunakkan. |
| R-f | Rendah | (d) Label murni `Overall` (nama produk baju overall), `Overall - Video`, `Total Produk`, dan `Total Store` dibuang. ⚠️ nama + biaya selalu ada, jadi tidak diam-diam. Nama persis "Total/Totals/Total 4 kampanye" tidak realistis sebagai kampanye, jadi keputusan pembuat wajar. |

**Skor: 8 / 10. Keputusan: LULUS.** Perbaiki N3 (+ tes regresi) sebelum beta bila memungkinkan.
