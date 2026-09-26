# HASIL UJI - audit-akun-iklan v1.0.0 (penguji independen, Akun B)

- Tanggal: 2026-09-26 · Penguji: agent terpisah dari pembuat, hanya membaca folder skill (simulasi agent, `claude-code (simulasi agent)`)
- Tidak mengubah SKILL/README/scripts/catalog. `uji_openclaw.sh` tidak dijalankan (sesuai instruksi).

## Skor kualitas: **8/10** — layak `lulus`, dengan 4 perbaikan kecil yang dianjurkan sebelum `beta`

Alasan: hitungan 100% cocok dengan verifikasi independen; A/B menang telak (skill menemukan target ROI
di bawah impas yang terlewat tanpa skill); menang di banding pesaing untuk pasar sasaran; atribusi MIT
benar; penolakan login/jaminan jelas. Poin dikurangi karena satu saran platform sudah usang (lokasi Meta),
saran yang saling bertentangan tidak direkonsiliasi, cek CAPI tidak ada, dan dua celah kecil script.

## Ringkasan skenario
| # | File | Jenis | Hasil |
|---|---|---|---|
| 1 | `01-toko-skincare-tiktok-uji-akun-b.md` | Normal: TikTok Ads + TikTok Shop | ✅ 53,9 final; ROAS impas 2,65; ⚠️ T08 vs T09 bertentangan |
| 2 | `02-kedai-kopi-meta-uji-akun-b.md` | Normal: Meta lokal 3 km | ✅ 42,7 final; ❌ saran M08 usang; ⚠️ M18 vs M08 |
| 3 | `03-agensi-google-les-privat-uji-akun-b.md` | Normal: agensi, Google Ads | ✅ 36,5 final; cek Google akurat |
| 4 | `04-input-tidak-lengkap-uji-akun-b.md` | "iklanku boncos, cek dong" | ✅ tanya sekali, 8 pertanyaan; ⚠️ label skor pada bukti kurang |
| 5 | `05-luar-cakupan-uji-akun-b.md` | Login akun klien / jaminan ROAS | ✅ menolak dengan jalur aman |
| A/B | `00-pembanding-tanpa-skill.md` | | ✅ skill jelas lebih baik (tanpa skill: ROAS impas salah 1,56) |
| Pesaing | `00-banding-pesaing.md` | claude-ads asli + fork + google-ads-skills | ✅ 36 vs 26 vs 22 (dari 45) |

## Verifikasi angka independen (Decimal, presisi 50, kode sendiri — tidak mengimpor script)
Membandingkan skor platform, skor 8 kategori, cakupan bukti, status (final/sementara/bukti kurang),
skor gabungan (porsi belanja/rata), nilai prioritas (keparahan × kemudahan) dan "naik" per perbaikan.

| Kasus | Skor script | Independen | Cakupan | Status | Kategori | Prioritas & naik | Cocok |
|---|---|---|---|---|---|---|---|
| S1 TikTok | 51,9 | 51,9 | 95,8 = 95,8 | final | 8/8 | 15/15 | ✅ |
| S1 TikTok Shop | 55,3 | 55,3 | 100 = 100 | final | 6/6 | (termasuk) | ✅ |
| S1 gabungan (4,5 jt : 6 jt) | 53,9 | 53,9 | – | final | – | – | ✅ |
| S2 Meta (3 cek tidak_berlaku) | 42,7 | 42,7 | 90,0 = 90,0 (45/50 bobot) | final | 8/8 | 11/11 | ✅ |
| S3 Google | 36,5 | 36,5 | 100 = 100 | final | 7/7 | 12/12 | ✅ |
| Semua lulus (79 cek, 5 platform) | 100,0 | 100,0 | 100 | final; gabungan "sementara" (belanja tidak ada) | ✅ | 0 | ✅ |
| Semua gagal (79 cek) | 0,0 | 0,0 | 100 | final | ✅ | 79/79 | ✅ |
| Bukti sebagian: Meta lengkap + Shopee 4 cek | Meta 86,5 / Shopee 37,5 | sama | 100 / 33,3 | Shopee bukti kurang, dikeluarkan dari gabungan | ✅ | 9/9 | ✅ |
| Google 81,3% | 48,5 | 48,5 | 81,3 | final | ✅ | 5/5 | ✅ |
| Batas tepat 60% (TikTok Shop) | 72,2 | 72,2 | 60,0 | sementara | ✅ | – | ✅ |
| Batas tepat 80% | 50,0 | 50,0 | 80,0 | final | ✅ | – | ✅ |
| 76% | 65,6 | 65,6 | 76,0 | sementara | ✅ | – | ✅ |

Urutan prioritas (prioritas ↓, naik ↓, keparahan, platform, ID) dicek manual di S1–S3: ✅.

### ROAS/ROI impas (dihitung ulang manual dengan Decimal)
| Input | Script | Independen | Cocok |
|---|---|---|---|
| 89rb, modal 32rb, 24,5%, kemas 1.500 | biaya 21.805; laba 33.695; 2,65 | 89.000/33.695 = 2,6413 → ke atas 2,65 | ✅ |
| "Rp 1,2 jt", modal 400.000, lain 50rb | laba 750.000; 1,60 | 1,6000 | ✅ |
| 28k, 11rb, lain 2.500 | laba 14.500; 1,94 | 1,9310 → 1,94 | ✅ |
| 100rb, 50rb, 12.5 (titik desimal) | 12.500; 37.500; 2,67 | 2,6667 → 2,67 | ✅ |
| 149rb/78rb/12%/2.000 (contoh pembuat) | 2,92 | 149.000/51.120 = 2,9147 → 2,92 | ✅ |
| **harga 100.000, modal 99.999,6** | **Traceback `DivisionByZero`** (kode 1) | laba 0,4 > 0 lolos cek, dibulatkan jadi 0 lalu dibagi | ❌ |
| harga 100rb, modal 60rb, 33,3333%, lain 6.666,5 | laba dibulatkan **ke atas** 0,5→1; ROAS 100.000 | seharusnya ≥ 200.000 (tidak konservatif) | ⚠️ kasus ekstrem |

## Input rusak / format Indonesia
| Kasus | Hasil | Nilai |
|---|---|---|
| CSV `;` + BOM + header `ID;Status`, "Ya/Tidak/Sudah/Sebagian/N/A", id huruf kecil | terbaca benar | ✅ |
| Status "mungkin" | → `tidak_tahu` + peringatan | ✅ |
| ID ganda status beda / sama | ditolak kode 2 / diterima | ✅ |
| Kolom salah, file kosong, ID tak dikenal, .xlsx, file tidak ada | pesan bahasa awam, kode 2 | ✅ |
| JSON benar (belanja "2jt"), JSON list, JSON rusak | jalan / kode 2 / kode 2 | ✅ |
| `--belanja google`, `yahoo=1jt`, `-1jt`, `--mulai 28-09-2026` | kode 2, pesan jelas | ✅ |
| Catatan berisi koma tanpa kutip | disambung, tidak hilang | ✅ |
| NaN, abc, negatif, persen ≥ 100, `12.000` sebagai persen | ditolak | ✅ |
| Belanja salah satu platform = 0 | platform itu berbobot 0, gabungan "FINAL" tanpa peringatan | ⚠️ kecil |
| **Semua cek kritis/tinggi ditandai `tidak_berlaku`** (Meta: 19 dari 21, termasuk yang kolom `tidak_berlaku_jika`-nya kosong) | **100,0 Sehat FINAL** tanpa peringatan | ❌ celah manipulasi/salah isi |

## Tes bawaan & validator
- `python3 tests/uji_skor_audit.py` → **29 tes OK**.
- `python3 scripts/validate.py --skill audit-akun-iklan` → **✅ 1 skill valid**.
- SKILL.md 104 baris; frontmatter hanya `name` + `description`.

## Atribusi & lisensi (claude-ads, MIT)
- ✅ Commit `ac21644…` ada dan = HEAD `main` per 2026-09-11; LICENSE MIT "Copyright (c) 2026 agricidaniel" disalin utuh di `LICENSE-MIT`.
- ✅ Klaim ATTRIBUTION akurat: `ads/references/scoring-system.md` memuat status pass/fail/unknown/not_applicable, bobot 5/3/1, rumus kategori, normalisasi bobot, ambang 80/60; `meta/tiktok/google-audit.md` hanya berisi nama cek + disposisi generik (tanpa kriteria) — jadi kriteria memang ditulis baru.
- ✅ Keterangan "telah diubah" dan "tidak berafiliasi" ada. README menyebut sumber MIT.
- Catatan: `THIRD_PARTY_NOTICES.md` claude-ads tidak menambah kewajiban untuk bagian yang dipakai.

## Tumpang tindih dengan `laporan-iklan-mingguan`
Tidak membingungkan: deskripsi audit menulis "Bukan untuk laporan angka mingguan (pakai
laporan-iklan-mingguan)", README punya FAQ pembeda, rencana hari 7 merujuk ke laporan. Kekurangan kecil:
deskripsi `laporan-iklan-mingguan` belum menyebut balik `audit-akun-iklan` (hanya "bukan audit strategi
iklan penuh" di baris 236 SKILL.md-nya). Permintaan ambigu ("boncos") ditangani di uji 04.

## Kebenaran faktual cek platform (dicek 2026-09-26)
| Cek | Klaim | Status | Sumber |
|---|---|---|---|
| M08 | "untuk layanan lokal pilih orang yang **tinggal** di lokasi tersebut" | ❌ **Usang** – Meta menghapus pilihan Tinggal di/Baru-baru ini/Bepergian; tersisa "tinggal di atau baru-baru ini berada di" | [Search Engine Land](https://searchengineland.com/new-update-to-meta-ads-location-targeting-404124), [Jon Loomer](https://www.jonloomer.com/big-change-to-meta-ads-location-targeting/) |
| M01/M02 | Pixel + hasil tercatat; **tidak ada cek Conversions API / deduplikasi** | ⚠️ Celah – Meta merekomendasikan CAPI bersama pixel untuk website; claude-ads punya cek ini | [Meta CAPI](https://www.facebook.com/business/help/AboutConversionsAPI) |
| M05 | Tujuan tidak bisa diganti setelah terbit | ✅ | [Meta Help – edit kampanye](https://www.facebook.com/business/help/2169779963333459) |
| M06 | ±50 hasil/minggu per ad set untuk keluar fase belajar | ✅ masih berlaku 2026 | [Pigeon Digital](https://www.pigeondigital.com/insight/facebook-ads-learning-phase-50-conversions-rule-2026) |
| M09/M20 | Audiens khusus & pengecualian pembeli | ✅ Pengecualian audiens khusus tetap berlaku di Advantage+ audience/sales. Catatan: skill tidak menyebut **Advantage+** sama sekali; di kampanye Advantage+ sales batas anggaran pelanggan lama sudah dihapus, jadi pengecualian makin penting | [Jon Loomer](https://www.jonloomer.com/existing-customers-exclusion-for-meta-ads/), [Madgicx](https://madgicx.com/blog/advantage-shopping-campaigns-farewell-customer-budget-cap) |
| M15 | Foto sebelum-sesudah (kesehatan/kecantikan) berisiko ditolak | ✅ sesuai kebijakan Meta | – |
| M18/M19, T15, S07, TS06, G13 | Ambang frekuensi, CTR −30%, jam 19–22, 5 video, 4 sitelink | ✅ M18 diberi label "patokan Komunitech"; lainnya tidak dilabeli tapi juga tidak diklaim resmi. Saran: tambahkan label patokan di kolom `lulus_jika` agar konsisten | – |
| T08 | Anggaran ≈ 20× target CPA "panduan umum TikTok" | ✅ sesuai TikTok Help (disebut juga 10× CPA 7 hari di artikel lain); sudah diberi "cek ulang". Tidak konsisten kecil: SKILL.md menyebutnya patokan Komunitech, CSV menyebutnya panduan TikTok | [TikTok – Budget](https://ads.tiktok.com/resources/help/article/budget?lang=en) |
| T17 | Pangle | ✅ | – |
| TS01–TS11 | GMV Max, target ROI, video afiliasi berizin, keluarkan video | ✅ GMV Max wajib untuk iklan TikTok Shop sejak Jul/Sep 2025; target ROI ada; **pengecualian video** ada (bulk creative exclusion, maks 200), tapi TikTok memperingatkan bisa menurunkan performa — perlu disebut di TS11 | [TikTok – buat Product GMV Max](https://ads.tiktok.com/help/article/how-to-create-a-product-gmv-max-campaign-in-tiktok-ads-manager), [TikTok – bulk creative exclusion](https://ads.tiktok.com/help/article/about-bulk-creative-exclusion-filters-for-product-gmv-max?lang=en) |
| S04/S06 | Iklan otomatis vs manual, target ROAS ≥ impas | ✅ secara logika. Shopee Indonesia kini memakai istilah **GMV Max Auto / GMV Max ROAS** (dan menyarankan tidak mengubah target ROAS saat fase belajar) — tidak disebut; alias `gmvmax` di script hanya dipetakan ke TikTok Shop sehingga "GMV Max Shopee" bisa salah rute | [Shopee Ads – GMV Max ROAS](https://iklan.shopee.co.id/learn/faq/549/1746), [FAQ GMV Max](https://iklan.shopee.co.id/learn/faq/57/2031) |
| G03, G07, G08, G12 | One/Every, Display di Search, opsi Kehadiran, Kekuatan iklan | ✅ | Google Ads Help |
| G10 | tCPA/tROAS setelah ±15–30 konversi/30 hari | ✅ diberi label patokan umum (Google Help: minimum lama 15 konversi tROAS) | [Google – Target ROAS](https://support.google.com/google-ads/answer/6268637?hl=en) |
| G12/G15/G16 `tidak_berlaku_jika` | "Hanya Performance Max" / "Tidak ada kampanye Penelusuran" → negatif tidak berlaku | ⚠️ **Usang sebagian** – sejak 2025 Performance Max punya kata kunci negatif tingkat kampanye (hingga 10.000) dan laporan istilah penelusuran | [Google blog 2025](https://blog.google/products/ads-commerce/new-performance-max-features-2025/) |

Aturan praktis Komunitech secara umum **tidak** disajikan sebagai aturan resmi (Batasan SKILL.md, README FAQ, metode-skor §4). ✅

## Temuan & rekomendasi perbaikan (urut prioritas)
1. **M08 perbaikan usang** → ganti dengan "pasang pin lokasi + radius (mis. 3 km); Meta kini otomatis
   menyasar orang yang tinggal/baru-baru ini di area itu".
2. **Rekonsiliasi saran bertentangan** → tambahkan aturan di SKILL.md Langkah 5: bila biaya per hasil
   di atas batas untung (M10/T09/S06/TS04 gagal), jangan menaikkan anggaran (T08, S07, TS05) sebelum
   itu beres; untuk usaha hiperlokal, M18 diatasi dengan materi baru/turunkan anggaran, bukan perluas audiens.
3. **Script**: (a) cek `laba` **setelah** pembulatan dan bulatkan laba **ke bawah** (konservatif) →
   hilangkan Traceback `DivisionByZero`; (b) jangan cetak skor/label untuk platform bukti kurang;
   (c) beri peringatan bila `tidak_berlaku` dipakai pada cek yang kolom `tidak_berlaku_jika`-nya kosong
   (terutama kritis).
4. **Tambah cek CAPI/deduplikasi** (Meta & TikTok Events API) untuk iklan ke website, dan sebut
   Advantage+ (Meta) serta GMV Max Auto/ROAS (Shopee); perbarui `tidak_berlaku_jika` G15/G16 untuk PMax;
   sebut peringatan TikTok di TS11.
5. Kecil: label "patokan Komunitech" konsisten (T08, S07, TS06, G13); `laporan-iklan-mingguan` merujuk
   balik ke skill ini; jelaskan bahwa "+x bila beres" = skor, bukan ROAS.

Butir 1–3 mudah (< 1 jam); tidak ada yang memblokir kelulusan skor ≥ 7, tetapi butir 1 dan 3a sebaiknya
dibereskan sebelum `beta`.

## platform_teruji yang jujur
`claude-code (simulasi agent)` — belum ada uji platform asli.
