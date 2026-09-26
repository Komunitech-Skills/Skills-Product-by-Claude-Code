# Uji ulang independen v1.0.3 (Akun B)

- **Tanggal:** 2026-09-26. **Versi:** v1.0.3 (commit `e63c127`). **Penguji:** agent independen lintas akun (Akun B, simulasi Claude Code). Bukan pembuat skill.
- **Cara uji:** skill disalin ke scratchpad penguji (`rt-iklan/skill/`). Ada 9 CSV fiktif buatan `gen.py` milik penguji. Kunci jawaban dihitung dengan `Decimal` **hanya dari baris data yang seharusnya dihitung**, tanpa mengimpor kode skill. `run.py` menjalankan skill lewat `subprocess` (`--json` dan teks), lalu mencocokkan total biaya, CPC (rupiah terdekat, 0,5 ke atas), ROAS (1 desimal), jumlah baris, dan ⚠️ untuk setiap baris yang dikecualikan (label + biaya dalam format `Rp x.xxx`).
- **Regresi:** `tests/uji_regresi.py` menjalankan 78 tes, semuanya OK. `python3 scripts/validate.py --skill laporan-iklan-mingguan` menghasilkan ✅ 1 skill valid, 80 baris katalog sesuai.

## (a) M1: kampanye bernama Total/Jumlah
| Nama | v1.0.2 | v1.0.3 |
|---|---|---|
| `Total 12.12 Flash Sale` | dibuang tanpa ⚠️ | ✅ dihitung |
| `Jumlah 2 Pcs Bundling` | dibuang tanpa ⚠️ | ✅ dihitung |
| `Total 12.12` (sisanya hanya angka) | dibuang | ✅ dihitung |
| `TOTAL SALE`, `TOTAL SALE Gamis Motif`, `Jumlah 3 Hijab Paket Hemat`, `Total Look Kondangan` | – | ✅ dihitung |
| `Jumlah 2 Pcs Bundling` dominan (54% biaya, tidak ≈ jumlah baris lain) | – | ✅ dihitung, tanpa salah buang |

Baris total asli ditangani sebagai berikut, dan **setiap baris yang dikecualikan diberi ⚠️ nama + biaya**:
- Nama kosong di bawah (Meta): dibuang lewat cek silang karena angkanya persis sama.
- `Total` di atas (Shopee), `Total` di kolom pertama + `Grand Total` (Meta ID), dan `Jumlah` (TikTok Shop): dibuang.
- `Total: Search` / `Total: Performance Max` / `Total: Account` (Google): dibuang. Subtotal yang angkanya tidak cocok dengan jumlah semua baris juga diberi ⚠️ "tidak sama".

## (b) M2/M3: perilaku sesuai SKILL.md
- **M2.** `Rekap Mingguan` selisih 3% dari jumlah baris lain → dihitung + ⚠️ "TERHITUNG DUA KALI… seharusnya Rp 1.000.000". Sesuai SKILL.md (±5% hanya ⚠️, ±2% dibuang).
- **M3.** `Subtotal Kamp A` (kolom induk, nama iklan kosong, cocok dengan 2 baris di atasnya) → dibuang + ⚠️ "SUBTOTAL". `Subtotal Kamp B` yang angkanya salah ketik → tetap dihitung + ⚠️. Sesuai SKILL.md.

## (c) 9 CSV fiktif dan kunci `Decimal`
| # | File (jebakan) | Kunci biaya · CPC · ROAS | Skill | Status |
|---|---|---|---|---|
| 01 | Meta EN: 4 nama "Total/Jumlah…", `Results` kosong, grand total bernama kosong di bawah | 2.877.991,50 → Rp 2.877.992 · 419 · 6,4x | sama | ✅ 0 beda |
| 02 | Google: 2 baris judul, `--`, angka `1,234.00`, konversi pecahan, `Total 12.12`, 3 baris `Total:` berlapis, kampanye Paused Rp 0 | 2.698.070 · 577 · 12,2x | sama | ✅ 0 beda |
| 03 | Shopee: info toko + `Periode Data`, angka `1.234.500`, `Total` di **atas**, `TOTAL SALE Gamis Motif` | 1.989.539 · 558 · 5,3x | sama | ✅ 0 beda |
| 04 | TikTok harian: `Subtotal: <nama kampanye>` di tengah, `Subtotal`, `Total of 3 campaigns` (+Rp 1) | 597.331,25 · 532 · 3,9x | **1.102.542,5 · 531 · 4,0x** | ❌ **N3** |
| 05 | TikTok Shop: `Jumlah 2 Pcs Bundling` dominan, `Jumlah` di bawah, angka Indonesia | 4.000.000 · 465 · 5,7x | sama | ✅ 0 beda |
| 06 | Meta ID tingkat iklan: `Total` di kolom pertama (atas), `Grand Total` (bawah), sel biaya kosong | 790.800 · 433 · – | sama | ✅ 0 beda |
| 07 | M2: `Rekap Mingguan` +3% | 2.030.000 · 794 · – | sama + ⚠️ | ✅ sesuai rancangan |
| 08 | M3: subtotal admin cocok / tidak cocok | 950.000 · 693 · – | sama + 2 ⚠️ | ✅ |
| 09 | (d) iklan bernama `Overall`, `Overall - Video`, `Total Produk`, `Summary Sale` | 715.000 · 534 · 5,9x (bila semua dianggap iklan) | 250.000 · 543 · 5,4x + 3 ⚠️ | ⚠️ sesuai rancangan, lihat (d) |

Hasil: **7/9 file cocok dengan kunci tanpa selisih, dan semua ⚠️ untuk baris yang dikecualikan ada, lengkap dengan nama dan biaya.** Laporan teks mencetak angka yang sama dengan JSON.

## (d) Keputusan pembuat: label ringkasan murni tetap dibuang
Klasifikasi dari `jenis_label_total`: `Total`, `Totals`, `Total 4 kampanye`, `Summary`, `Ringkasan`, `Keseluruhan`, dan `Overall` tergolong **kuat**. Label **sedang** meliputi `Overall - Video`, `Total Produk`, `Total Store`, `Total Shop`, `Jumlah Toko`, `Total Video`, `Total Search`, `Total Performance`, `Total Item`, dan `Jumlah Hari`.
- **Nama kampanye yang persis "Total", "Totals", atau "Total 4 kampanye"** hampir tidak mungkin ada di akun nyata. Keputusan ini wajar.
- **Kasus nyata yang paling mungkin terkena adalah `Overall`.** Di fashion UMKM Indonesia, "overall" adalah nama produk (baju kodok/overall anak), dan nama iklan di ekspor tingkat iklan sering hanya berupa nama produk. File 09 menunjukkan `Overall` dan `Overall - Video` ikut dibuang. Hal yang sama berlaku untuk nama toko/katalog seperti `Total Produk` atau `Total Store`. Dampaknya **tidak diam-diam**: ⚠️ menyebut nama + biaya dan "tidak sama dengan jumlah baris lain… ganti namanya". Pengguna tetap bisa memulihkannya, tetapi angka utama di laporan sudah salah. Saran (rendah):
  1. Keluarkan `overall` dari kata kepala, atau hanya jadikan "kuat" bila disertai tanda baca/cakupan **dan** angkanya cocok.
  2. Pada ekspor bertingkat (kolom nama = `Ad name`, induk terisi), label "kuat/sedang" yang angkanya jauh dari jumlah baris lain lebih masuk akal **dihitung + ⚠️** daripada dibuang, karena baris total ekspor bertingkat biasanya punya induk kosong.

## Temuan baru
| ID | Keparahan | Temuan |
|---|---|---|
| **N3** | Sedang | Subtotal buatan lembar kerja **di kolom nama itu sendiri** yang memuat nama kampanye, yaitu `Subtotal: Total 12.12 Flash Sale`, `Subtotal: Retarget Video` (pola Data > Subtotal/pivot), atau `Retarget Video Total`, tergolong "lemah" atau tidak dikenali. Akibatnya baris itu **dihitung sebagai kampanye → total 2× tanpa ⚠️ untuk baris itu**. Repro file 04: Rp 1.102.543, padahal seharusnya Rp 597.331. "Kampanye" `Subtotal: …` bahkan masuk TERBAIK no. 1. Repro kecil (`Retarget Video` ×2 + `Subtotal: Retarget Video` + 2 kampanye) → Rp 294.240, padahal seharusnya Rp 202.120, tanpa ⚠️ sama sekali. **Ini bukan regresi** (v1.0.2 sama). Ekspor platform asli tidak membuat baris seperti ini, jadi kasusnya hanya pada lembar olahan admin. Saran: kata kepala `subtotal`/`sub total` hampir tidak pernah dipakai sebagai nama kampanye, jadi selalu perlakukan sebagai kandidat subtotal (cek tetangga ±2% seperti M3, atau minimal ⚠️). Baris `X Total` / `Total: X` dengan X = nama baris lain di file juga perlu diperlakukan sebagai kandidat subtotal. Grand total "kuat" yang biayanya ≈ ½ jumlah baris terhitung adalah tanda subtotal ikut terhitung, sehingga layak diberi ⚠️ khusus. |
| R-e | Rendah | ⚠️ M2 positif palsu. Pada Google (file 02), kampanye sah `PMax - Semua Produk` (Rp 1.380.000, 4,7% di atas jumlah baris lain) diberi ⚠️ "TERHITUNG DUA KALI". Ini sesuai rancangan ±5%, tetapi kalimatnya bisa membuat awam panik untuk akun dengan 1 kampanye dominan. Saran: lunakkan kalimat ("mungkin") atau syaratkan tayangan/klik juga ±5%. |
| R-f | Rendah | Label `Overall`/`Total Produk`/`Total Store` dibuang (lihat d). |

## Skor: **8 / 10**
- (+) M1 beres. Kelima nama berawalan Total/Jumlah dihitung di 4 platform, termasuk saat dominan. Setiap baris yang dikecualikan kini diberi ⚠️ nama + biaya.
- (+) M2 dan M3 berperilaku persis seperti SKILL.md. Tidak ada regresi (78 tes OK, validate lolos). 7/9 CSV baru cocok dengan kunci `Decimal` tanpa selisih.
- (−) N3: subtotal lembar olahan yang memuat nama kampanye masih dihitung 2× tanpa ⚠️ untuk barisnya (hanya ada ⚠️ tak langsung pada grand total).
- (−) Ekspor asli per platform masih belum diverifikasi dengan file nyata (PERLU REVIEW, sudah tercatat sebelumnya).

**Keputusan: LULUS.** Perbaiki N3 (dengan tes regresi) sebelum beta bila memungkinkan. Uji ulang singkat cukup untuk file 04 dan repro kecil N3.
