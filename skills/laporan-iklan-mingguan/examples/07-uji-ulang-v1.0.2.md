# Skenario 07: uji ulang v1.0.2 oleh penguji independen (Akun B)

- **Tanggal:** 2026-09-26. **Versi diuji:** v1.0.2 (commit `b2a286c`).
- **Penguji:** agent penguji independen lintas akun (Akun B, simulasi Claude Code). Bukan pembuat skill.
- **Lingkungan:** Linux, Python 3.11. Skill disalin ke `…/scratchpad/uji2-iklan/skill` dan dijalankan dari sana (tidak dipasang di `.claude/skills`).
- **Aturan kunci jawaban:** 14 CSV baru dibuat oleh `gen2.py` milik penguji. Kunci dihitung dengan `Decimal` **hanya dari baris data** (baris total/subtotal tidak ikut). Kode skill **tidak dibaca dan tidak diimpor**. Skill dijalankan lewat `subprocess`. `cek2.py` mencocokkan teks laporan, total JSON, `--csv-keluaran` per baris, nama di PERLU PERHATIAN no. 1, dan ⚠️. Pembulatan: rupiah ke terdekat (0,5 menjauhi nol), persen/ROAS 1 desimal.
- Semua data fiktif.

## 1. Ulang repro N1/N2 (file asli uji v1.0.1)

| Repro | v1.0.1 | v1.0.2 | Status |
|---|---|---|---|
| **N1** K2 Meta `Campaign name`+`Ad set name`+`Ad name` (USD, `--kurs 16350`) | 1 baris "Kamp". Advantage+ tersembunyi. Catatan menulis Rp 4.423.002 | Dirinci per `Ad name`. **Advantage+ Catalog** jadi PERLU PERHATIAN no. 1 dan saran no. 1. Catatan: "kosong di 1 baris (Advantage+ Catalog) … **Rp 1.080.735**". Total Rp 4.423.002, ROAS 3,9x, 17 nilai rincian cocok | ✅ Beres |
| **N1** K12 iklan sama di 2 ad set | Set0/Set1/Set2 | "Iklan Promo (Set0)", "Iklan Katalog", "Iklan Promo (Set1)". Rp 1.245.601 + 200.000 = kunci lama "Iklan Promo" Rp 1.445.601. Total Rp 2.445.601 | ✅ Beres (beda nama di `cek.py` lama hanya karena kuncinya per nama iklan) |
| **N2** matriks 16 label × 2 posisi (kolom nama & kolom pertama), total Rp 500.001 vs 500.000 | `Total of 2 campaigns`/`Totals`/`Total Akun` → Rp 1.000.001 | **32/32 → Rp 500.000** | ✅ Beres |
| **N2** K3 varian TikTok harian `Total of 3 campaigns` (3 file) | Rp 6.399.400 | Rp 3.199.700 ×3, baris total dicatat | ✅ Beres |
| **R-b** "1 baris" kosong di data harian | "1 baris" | "7 baris (Live Payday) … Rp 666.750" | ✅ Beres |

## 2. CSV baru buatan penguji (14 file) + kunci Decimal

| # | Bentuk | Kunci (biaya · hasil) | Hasil skill |
|---|---|---|---|
| P1 | Meta EN 3 level, angka `"845,250.50"`, `Carousel Promo` di 2 kampanye, `Results` kosong di "Katalog Dinamis" | 2.772.501 (2.772.500,50) · 37 · ROAS 2,8x | ✅ 0 beda. Katalog Dinamis PERLU PERHATIAN no. 1 + saran no. 1. Catatan menulis Rp 690.400 (biaya baris) |
| P2 | TikTok 3 level, `Totals` di bawah dengan biaya **+1,5%** (812.000 vs 800.000), `Video A` di 2 ad group, `-` di Conversions | 800.000 · 24 | ✅ 0 beda. `Totals` dilewati (dicatat, tanpa ⚠️ selisih) |
| P3 | Google laporan grup iklan, 2 baris judul, induk bernama **"Jumlah Promo Ramadan"** dan **"Total Look Hijab"**, `Total: Filtered ad groups` + `Total: Account` | 2.720.750 · 67,5 · ROAS 4,6x | ✅ 0 beda. Dirinci per `Ad group`. Kampanye induk "Jumlah…/Total…" tidak membuang baris data |
| P4 | Shopee, kampanye **"Total Look Hijab"**, **"Jumlah Terbatas - Khimar"**, "Totalitas Gamis", **"Total Diskon 50% Bergo"**, baris `Jumlah` sama persis | 1.000.000 · 25 · ROAS 3,9x | ✅ 0 beda. Keempat kampanye dihitung, hanya `Jumlah` dilewati |
| P5 | Shopee, kampanye **"Total 12.12 Flash Sale"** dan **"Jumlah 2 Pcs Bundling"** (nama diawali Total/Jumlah + angka), **tanpa** baris total | 1.000.000 · 31 · ROAS 4,4x | ❌ **Rp 150.000**. Kedua kampanye (Rp 850.000 = 85%) dibuang sebagai "baris total", **tanpa ⚠️**, hanya disebut di Catatan. Lihat **M1** |
| P6 | Label asing "Akun Toko Berkah", biaya/tayangan/klik **+1%** | 500.000 · 18 | ✅ 0 beda + ⚠️ "hampir sama (selisih ≤ 2%) … dianggap baris TOTAL" |
| P7 | Label asing sama, ketiga metrik **+3%** | 500.000 · 18 | ❌ **Rp 1.015.000**, tanpa ⚠️; "Akun Toko Berkah" tampil di TERBAIK no. 2. Lihat **M2** |
| P7b | `Total of 3 campaigns` +3% | 500.000 · 18 | ✅ 0 beda + ⚠️ "biayanya (Rp 515.000) tidak sama dengan jumlah baris lain" |
| P8 | Lembar 2 level buatan admin: `Grand Total` di **atas**, `Subtotal: Kamp A/B` di tengah (kolom induk) | 550.000 · 17 | ✅ 0 beda. 3 baris total dicatat |
| P8b | Sama, tetapi `Subtotal Kamp A` (tanpa titik dua) | 550.000 · 17 | ❌ **Rp 1.100.000**, tanpa ⚠️. Subtotal jadi "(tanpa nama, baris 5/8)" dan masuk TERBAIK/PERLU PERHATIAN. Lihat **M3** |
| P9 | Meta UI Indonesia 2 level (`Nama kampanye`+`Nama set iklan`), `"412.345,50"`, `Total Akun` biaya +Rp 3 | 850.000 · 25 | ✅ 0 beda. Per set iklan, "Set Semua" PERLU PERHATIAN no. 1 |
| P10 | TikTok, kolom `Ad name` ada tetapi kosong semua | 600.000 · 19 | ✅ 0 beda, level `Ad group name`. ⚠️ "TERHITUNG DUA KALI" muncul karena AG Satu Rp 300.000 = AG Dua + AG Tiga (kebetulan data). Angka tetap benar; ini peringatan palsu yang sesuai rancangan (rendah) |
| P11 | Kampanye asli dominan "Konversi Utama" Rp 497.000 ≈ jumlah lainnya (0,6%), tayangan/klik jauh beda | 997.000 · 75 | ✅ 0 beda. Tetap dihitung + ⚠️ "TERHITUNG DUA KALI: seharusnya Rp 500.000, bukan Rp 997.000" (bersyarat) |
| P12 | Huruf campur di 2 posisi: `grand TOTAL:` di atas (kolom tanggal), `TOTAL OF 3 KAMPANYE` di bawah (kolom nama) | 500.000 · 18 | ✅ 0 beda, 2 baris dicatat |

**Ringkasan:** 11/14 kasus 0 beda. **322 nilai cocok** (total, CPC, CPM, CTR, biaya/hasil, ROAS, tayangan/klik/hasil, rincian per baris). 3 kasus gagal, semuanya jalur baris total/nama berawalan "Total/Jumlah".

## 3. Regresi T1–T4 / S1–S4 / R (repro HASIL-UJI dan file K1–K12 v1.0.1)

- **T1:** skenario 01 Rp 4.302.180, naik 8,4%; 142 pesan WA (naik 6,8%); Rp 30.297/pesan (naik 1,5%); Retargeting PERLU PERHATIAN + saran no. 1. `kosong.csv` Rp 620.000. ✅
- **T2:** Shopee A/B/C/info toko semuanya Rp 2.468.636, ROAS 3,5x. ✅
- **T3:** Google mentah Rp 3.326.715, CPC 871, CPM 26.293, CTR 3,0%, 26.455/konversi, ROAS 4,2x. ✅
- **T4:** `Currency`=USD dan `$` ditolak (rc 2). `--kurs 16350` → Rp 1.828.584. ✅
- **S1:** gabung TikTok+Google diberi ⚠️ atribusi, "(perkiraan)", ROAS "hanya Google Ads". JSON ganda ditolak. ✅
- **S3:** UTF-16 Rp 375.000, CTR 10,8%. ✅
- **S4:** `20 juta`/`20jt`/`Rp20.000.000` → 20.000.000; `750 rb`, `1,5 juta` benar; `20 M`, `dua puluh juta`, `0` ditolak. ✅
- **R/K:** kurs negatif, `;x`, xlsx, tanggal 30 hari/tak terbaca, file sama, file tak ada, JSON asing, `--csv-keluaran` menimpa input → semuanya pesan Indonesia/⚠️, tanpa traceback. ✅
- `cek.py` v1.0.1 (K1–K12, 6 penolakan): semua cocok **kecuali** K8 `Nilai konv.` (R-a, belum ditangani, diakui pembuat) dan beda nama K12 yang disengaja (N1).

## 4. Temuan baru

| ID | Keparahan | Temuan | Saran |
|---|---|---|---|
| **M1** | Sedang | Nama kampanye **"Total/Jumlah + angka"** ("Total 12.12 Flash Sale", "Jumlah 2 Pcs Bundling") dianggap label total **kuat**, lalu dibuang. Pengaman silang tidak dipakai untuk label kuat: biayanya (600.000/250.000) jauh dari jumlah baris lain, tetapi tidak ada ⚠️. Laporan kehilangan 85% belanja, dan PERLU PERHATIAN/SARAN berubah. Hanya Catatan yang menyebut namanya. P2 (`Totals` +1,5%) juga tanpa ⚠️ selisih. | Untuk **semua** label yang dibuang (kuat maupun sedang), bila biayanya tidak ≈ jumlah baris lain (> 2%), beri ⚠️ yang sama seperti P7b. Pertimbangkan juga: "Total/Jumlah + angka + kata lain" (mis. `12.12 Flash Sale`, `2 Pcs`) = lemah, kecuali angka diikuti kata cakupan (`Total 4 kampanye`). Tambahkan tes regresi. |
| **M2** | Rendah | Label tak dikenal dengan ketiga metrik selisih 3% (di atas batas 2%) → dihitung 2× tanpa ⚠️ (Rp 1.015.000). Sesuai batas yang dirancang; pembulatan platform nyata jarang sampai 3%. | Opsional: ⚠️ ringan bila biaya **dan** tayangan **dan** klik satu baris ada dalam ±5% dari jumlah baris lain. |
| **M3** | Rendah | `Subtotal Kamp A` (tanpa titik dua) di kolom induk, dengan kolom nama kosong → dihitung sebagai baris data "(tanpa nama, baris N)" → total 2×, tanpa ⚠️. Hanya terjadi pada lembar buatan admin, bukan ekspor platform. | Baris yang kolom namanya kosong tetapi kolom teks lain diawali kata kepala total → perlakukan sebagai total, atau minimal beri ⚠️. |
| R-a/c/d | Rendah | Belum ditangani (diakui di UJI-PEMBUAT-v1.0.2). Platform "Tidak diketahui" juga untuk lembar bergaya Shopee di P5/P8. | — |

## 5. Uji bawaan & validator
- `python3 tests/uji_regresi.py` (salinan scratchpad dan lokasi repo): **63 tes OK**. `__pycache__` yang terbentuk di repo sudah dihapus.
- `python3 scripts/validate.py --skill laporan-iklan-mingguan` (root repo): **✅ 1 skill valid, 77 baris katalog sesuai.**
- `scripts/uji_openclaw.sh` tidak dijalankan (sesuai instruksi).
