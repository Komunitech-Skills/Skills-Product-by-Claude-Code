# Uji ulang independen v1.0.4 (N3: subtotal buatan admin di kolom nama)

- **Tanggal:** 2026-09-28. **Versi:** v1.0.4 (commit `95a6710`). **Penguji:** agent independen (simulasi Claude Code), bukan pembuat revisi. Skill dijalankan dari salinan di scratchpad (`uji-iklan-104/skill`). Kode script **tidak dibaca**: kunci jawaban disusun dari spesifikasi baris sendiri dengan `Decimal`.
- **Uji bawaan:** `tests/uji_regresi.py` menjalankan **87 tes, semuanya OK**. `scripts/validate.py --skill laporan-iklan-mingguan` menghasilkan ✅ 1 skill valid, 91 baris katalog sesuai.
- **Pembanding:** file yang sama juga dijalankan dengan script v1.0.3 (`e6fc991`) untuk memastikan perubahan memang dari revisi ini.

## 1. File uji baru (17 CSV + 6 file buruk)

Setiap baris diberi kunci "dihitung / tidak dihitung" menurut kebenaran bisnis. Kunci ini lalu dijumlah dengan `Decimal` dan dibandingkan dengan `total` dari `--json` (biaya, tayangan, klik, hasil, nilai, CPC, ROAS) serta dengan rincian per kampanye.

| # | Isi file | Kunci biaya | v1.0.4 | v1.0.3 | ⚠️ baris dikecualikan |
|---|---|---|---|---|---|
| 01 | Meta 3 level, `Subtotal: Retarget Video` (ad set/ad kosong) + `Total` | 647.119,50 | ✅ 647.119,5 | 647.119,5 | ✅ keduanya |
| 02 | Meta: `Sub total - Hijab` (+Rp 1), `SUBTOTAL MUKENA`, `Sub-total: Sarung` (admin salah +10%), `Jumlah sementara`, `subtotal kaos kaki` | 739.083 | ✅ 739.083 | ❌ 1.517.500 | ✅ 5/5, yang tidak cocok disebut "walaupun angkanya tidak cocok" |
| 03 | TikTok harian: `Retarget Video Total` & `Total: Awareness Ramadan` tanpa tanggal, `Total of 3 campaigns` (+Rp 1), **hari ke-3 kebetulan = hari 1 + hari 2** | 777.776,75 | ✅ 777.776,75 | ❌ 1.477.776,5 | ✅ 3/3. Hari ke-3 tetap dihitung |
| 04 | **Kampanye sungguhan** `Total 12.12 Flash Sale` + `Subtotal Promo Gajian` + `Total` | 1.320.000 | ⚠️ 1.000.000 (sesuai desain) | 1.320.000 | ✅ 2 ⚠️ saling menguatkan (lihat §2) |
| 04b | `Subtotal Promo Gajian` sungguhan, dominan, tanpa baris total | 860.000 | ⚠️ 240.000 (sesuai desain) | 860.000 | ✅ ⚠️ di blok teratas |
| 05 | Shopee angka Indonesia (`1.234.567,5`), info toko, `Total` di atas, `Jumlah sementara`, `Sub Total Iklan Toko` | 1.591.700,75 | ✅ | ❌ 2.541.701,5 | ✅ |
| 06 | Google 2 level: `Subtotal: Search - Brand`, `Total: Search campaigns`, `Total: Account`, PMax tanpa ad group | 699.999 | ✅ | 699.999 | ✅ |
| 07 | TikTok Shop: `Jumlah 2 Pcs Bundling` sungguhan, `Sub Total` tidak cocok (+15%), `Grand Total` | 524.000,5 | ✅ | — | ✅ |
| 08 | Meta harian: subtotal nama sama persis tanpa tanggal; `Brand` + `Brand Total` sungguhan (tidak cocok); `Promo` hari ke-3 = hari 1 + 2 | 300.000 | ✅ | — | ✅. `Brand Total` dihitung + ⚠️ "TETAP dihitung" |
| 09 | Regresi M3/N2: `Subtotal Kamp A` di kolom ad set dengan nama kosong, `Total Akun` +Rp 3 | 220.000 | ✅ | — | ✅ |
| 10 | Hanya baris subtotal/total | — | ✅ kode 2, pesan jelas | — | — |
| 11 | Regresi M1: `Total 12.12 Flash Sale` dominan | 1.000.000 | ✅ dihitung | — | — |
| 12 | Regresi M2: `Rekap Minggu` +3% | 304.500 | ✅ dihitung + ⚠️ lunak | — | ✅ |
| 13 | Regresi N2: `Total (3 iklan)` di atas + `Totals` +1,5%, **B = A + C persis (3 metrik)** | 300.000 | ❌ 150.000 | 150.000 (sama) | ⚠️ ada (lihat P-1) |
| 13b | Sama, B ≈ A + C +3,4% | 301.000 | ✅ + ⚠️ lunak | 301.000 | ✅ |
| 14 | Kampanye `Gamis` = persis jumlah 2 kampanye lain (3 metrik) | 600.000 | ⚠️ 300.000 (sesuai desain) | 300.000 | ✅ |
| 15 | TikTok harian `Total Promo Gajian` sungguhan + `Subtotal: Total Promo Gajian` | 250.000 | ✅ | — | ✅ |
| 16 | Uji A/B: 2 kampanye biaya sama persis (Rp 700.000) | 1.400.000 | ✅ tanpa ⚠️ palsu | — | — |

**Ringkasan angka:** ada 17 file data. **13 cocok 100%** dengan kunci kebenaran. **161 nilai rincian per kampanye cocok, 0 beda.** Empat file berbeda dengan kunci kebenaran: 04, 04b, 14 sesuai desain yang tertulis di SKILL.md, dan 13 juga sesuai aturan cek silang di SKILL.md. Keempatnya **selalu diberi ⚠️** di blok teratas. **Selisih diam-diam (tanpa ⚠️): 0.** Tidak ada perbedaan dengan perilaku yang dijanjikan SKILL.md.

**File buruk:** file 0 byte, file hanya berisi judul kolom, byte acak, `.xlsx` palsu, kutip tidak tertutup, dan pemisah `;` semuanya ditangani. Hasilnya kode keluar 2 dengan pesan jelas, atau terbaca benar (untuk file `;`). Tidak ada traceback.

## 2. Kampanye sungguhan bernama "Total …" / "Subtotal …"
- `Total 12.12 Flash Sale`, `Total 12.12`, `Jumlah 2 Pcs Bundling`, dan `Total Promo Gajian` (harian) **tetap dihitung** (M1 tidak regresi).
- `Subtotal Promo Gajian` **selalu dikecualikan**, sesuai SKILL.md v1.0.4 ("berawalan Subtotal → selalu dikecualikan"). ⚠️ berada di blok **PERLU DICEK** paling atas, menyebut nama dan biaya, dan menyatakan "walaupun angkanya tidak cocok … bila itu kampanye sungguhan, ganti namanya". Di file 04, ⚠️ kedua ikut menguatkan: "`Total` … Rp 1.320.000 tidak sama dengan jumlah baris lain (Rp 1.000.000)". Jadi pengguna **pasti melihatnya**.
- Kekurangannya: di 04b, total laporan hanya Rp 240.000, padahal seharusnya Rp 860.000 (72% hilang). ⚠️ tidak menyebut total alternatifnya ("bila itu kampanye, total seharusnya Rp 860.000"), padahal ⚠️ M2 menyebutnya. Nama kampanye berawalan "Subtotal" sangat jarang, jadi keputusan desain ini wajar.

## 3. Status temuan lama
| ID | Status | Bukti |
|---|---|---|
| **N3** | ✅ Beres | File 01, 02, 03, 05, 06, dan 15 cocok dengan kunci. v1.0.3 menghitung 2× pada file 02, 03, dan 05. Setiap subtotal diberi ⚠️ nama + biaya, dan menyebut apakah angkanya cocok dengan baris di sekitarnya |
| R-e (kalimat M2) | ✅ Beres | "TERHITUNG DUA KALI" diganti menjadi "Mohon dicek sebentar … mungkin terjumlah dua kali … Bila itu kampanye sungguhan, abaikan catatan ini" |
| M1 | ✅ Tidak regresi | File 04, 11, dan 15 |
| M2 | ✅ Tidak regresi | File 12 dan 13b (dihitung + ⚠️) |
| M3 | ✅ Tidak regresi | File 09 |
| N1 | ✅ Tidak regresi | File 01 dirinci ke level iklan, file 06 ke grup iklan, dan Catatan menyebut levelnya |
| N2 | ✅ Tidak regresi | `Total of 3 campaigns` +Rp 1, `Total Akun` +Rp 3, `Totals` +1,5%, `Total (3 iklan)` di atas, `Grand Total` |

## 4. Temuan baru / tersisa
| ID | Keparahan | Temuan |
|---|---|---|
| P-1 | Rendah (sudah ada sejak v1.0.2, bukan regresi) | Setelah baris total eksplisit (`Total (3 iklan)`, `Totals`) dibuang, cek silang masih membuang kampanye sungguhan `B` karena biaya, tayangan, dan kliknya persis sama dengan A + C. Total menjadi Rp 150.000, padahal seharusnya Rp 300.000. Ada ⚠️, dan ⚠️ baris total sendiri menyebut "tidak sama (Rp 300.000 vs Rp 150.000)", jadi pengguna diberi tanda. Saran: bila sudah ada baris total eksplisit yang cocok dengan jumlah **sebelum** cek silang, lewati cek silang. Kebetulan 3 metrik (±2%) jarang terjadi. |
| P-2 | Rendah | ⚠️ untuk `Sub Total Iklan Toko` (Shopee), dan `Total: Search campaigns` (Google) membandingkan biayanya dengan **jumlah semua baris lain** ("tidak sama dengan … Rp 1.591.701"), padahal baris itu cocok dengan baris di atasnya. Angka laporan benar; hanya kalimatnya bisa membingungkan. Seharusnya memakai kalimat "cocok dengan baris di sekitarnya" seperti subtotal lain di v1.0.4 |
| P-3 | Rendah | Baris Google PMax dengan `Ad group` kosong muncul sebagai "(tanpa nama, baris 7)" di PERLU PERHATIAN, bukan memakai nama kampanye induknya (`PMax - Katalog`). Catatan memang menyebutnya, tetapi pengguna awam tidak tahu iklan yang mana |
| P-4 | Rendah | ⚠️ untuk `Subtotal …` yang tidak cocok tidak menyebut total alternatif (lihat §2) |
| P-5 | Kosmetik | Untuk file byte acak, daftar kolom di pesan error ikut mencetak karakter sampah. Tetap kode 2 |

## 5. Skor: **9 / 10**
- (+) N3 beres dengan 6 file baru dalam berbagai ejaan (`Subtotal:`, `Sub total -`, `SUBTOTAL`, `Sub-total:`, `subtotal`, `Sub Total`, `Jumlah sementara`, `X Total`, `Total: X`, nama sama persis tanpa tanggal). v1.0.3 salah pada 3 di antaranya.
- (+) Baris harian yang kebetulan sama dengan jumlah baris di atasnya **tetap dihitung**, karena bertanggal. Kampanye mirip subtotal yang tidak cocok tetap dihitung + ⚠️.
- (+) Selisih diam-diam: 0. 161 nilai rincian cocok. 87 tes regresi OK. File buruk tidak menghasilkan traceback. Kalimat ⚠️ M2 sudah lunak.
- (−) P-1 s.d. P-4 berkeparahan rendah. Semuanya terlihat lewat ⚠️.
- (−) Bentuk ekspor asli kelima platform tetap **belum diverifikasi** dengan file nyata (PERLU REVIEW).

**Keputusan: LULUS.** N3 ditutup. P-2/P-3 bisa diperbaiki kapan saja (kalimat/label saja). Uji platform asli tetap membutuhkan satu ekspor asli per platform dari pemilik.
