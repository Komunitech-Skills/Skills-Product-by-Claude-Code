# Hasil Uji: uji-pasar-produk-cepat v1.0.0

- Penguji: agent independen (bukan pembuat), hanya membaca folder skill + CLAUDE.md. Tanggal: 2026-09-29.
- Platform: `claude-code (simulasi agent)`. Belum diuji di OpenClaw/Codex/Cursor asli.
- `python3 scripts/validate.py --skill uji-pasar-produk-cepat` → ✅ lolos. `python3 tests/uji_hasil_eksperimen.py` → "Semua uji lolos."

## 1. Audit keamanan & format
| Cek | Hasil |
|---|---|
| Frontmatter hanya `name` + `description`, nama = folder, satu baris | ✅ |
| SKILL.md < 300 baris | ✅ 143 baris |
| Script hanya pustaka standar | ✅ `argparse`, `math`, `sys` (dicek via AST) |
| Jaringan / subprocess / eval / baca file / kredensial | ✅ tidak ada |
| Prompt injection di SKILL/references | ✅ tidak ditemukan |
| LICENSE-APACHE & LICENSE-MIT identik dengan repo sumber | ✅ `diff` kosong terhadap clone commit `1cef1a9` dan `8607e3b` (hash di ATTRIBUTION.md cocok) |
| NOTICE Apache | ✅ repo sumber memang tidak punya NOTICE |
| Pernyataan perubahan (Apache §4b) & tidak berafiliasi | ✅ ada di ATTRIBUTION.md dan README |
| Teks disalin dari sumber? | ✅ tidak ditemukan kalimat sumber; hanya struktur (XYZ, dampak x ketidakpastian, pivot) |

## 2. Verifikasi angka independen
Penguji menulis hitungan sendiri (Wilson lewat akar persamaan kuadrat, uji z dengan `statistics.NormalDist`, Fisher exact dengan `math.comb`, rumus sampel & power) di scratchpad, bukan memakai kode skill.

| Kasus | Script | Penguji | Status |
|---|---|---|---|
| Wilson 14/80 | 10,7%-27,3% | 10,72%-27,26% | ✅ |
| Wilson 21/120 | 11,7%-25,3% | 11,7%-25,3% | ✅ |
| Wilson 3/12, 2/40, 10/12, 0/10, 4/10, 80/1250 | cocok | cocok (0,1 poin) | ✅ |
| z 9/60 vs 15/60 | z 1,37; p 0,1709 | z 1,369; p 0,1709 | ✅ |
| z 17/140 vs 31/130 | z 2,51; p 0,0120 | z 2,513; p 0,0120 | ✅ |
| z 12/55 vs 7/55 | z -1,26; p 0,2073 | cocok | ✅ |
| Sampel m10 p20 / m10 p50 / m5 p50 / m2 p5 | 62 / 97 / 385 / 457 | 62 / 97 / 385 / 457 | ✅ |
| 0/10 vs 4/10 | p 0,0253 → "Varian B memang lebih baik, bukan kebetulan" | Fisher exact p = **0,087** (tidak signifikan) | ❌ overclaim (B1) |
| 0/20 vs 5/20 | p 0,0168 → "memang lebih baik" | Fisher p = 0,047 | ⚠️ batas |

Rumus inti benar. Masalah ada di **interpretasi** sampel kecil dan **panduan jumlah sampel dua varian**.

## 3. Vonis per skenario
Rincian di [`05-uji-independen-5-skenario.md`](05-uji-independen-5-skenario.md).

| # | Skenario | Vonis |
|---|---|---|
| S1 | Normal: pre-order WA nastar, 21/120, target 15%, "produksi 300?" | ✅ LULUS (menang A/B) |
| S2 | Normal: smoke test landing page + status WA, jasa cuci sepatu | ✅ LULUS dengan catatan (B3) |
| S3 | Normal: A/B harga keripik 12/55 vs 7/55 | ✅ LULUS, tidak overclaim (saran uji ulang lemah, B2) |
| S4 | Input tidak lengkap (tanpa penyebut) + data rusak (0, aksi > ditawari, "1.250", "15%") | ✅ LULUS |
| S5 | Di luar cakupan: pre-order menahan DP + foto merek lain | ✅ LULUS (ditolak, ditawari alternatif jujur) |

- Uji A/B ([`00-pembanding-tanpa-skill.md`](00-pembanding-tanpa-skill.md)): **dengan skill jelas lebih baik** (rentang wajar, hitungan kebutuhan kontak, bias keluarga, kriteria & log).
- Banding pesaing ([`00-banding-pesaing.md`](00-banding-pesaing.md)): vs phuryn/pm-skills (±26,6k bintang) dan product-on-purpose/pm-skills: **skill kita menang** 32 vs 14 vs 13; kalah hanya di rigor power/MDE dua varian.

## 4. Bug & temuan
| ID | Tingkat | Temuan |
|---|---|---|
| B1 | Sedang | `banding` dengan sel < 5 tetap mencetak "Varian B memang lebih baik, bukan kebetulan (keyakinan ~95%)" lalu baru peringatan "gambaran kasar". Contoh 0/10 vs 4/10: p z-test 0,025, Fisher exact 0,087. Pesan saling bertentangan; pembeli awam membaca kalimat pertama. |
| B2 | Sedang | Panduan sampel dua varian terlalu optimis dan tanpa power: SKILL "selisih < 10 poin butuh 150-300 per varian", references "selisih 10 poin biasanya meyakinkan di 100-150 per varian" (power nyata 15%→25% di n=150 ≈ 0,58; 20%→25% butuh ±1.094 per varian). Baris script `sampel` "butuh SEBANYAK itu untuk TIAP varian" salah (n margin ≠ n pembanding; 62/varian untuk 15%→25% power ≈ 0,28). |
| B3 | Kecil | `sampel` tidak memperingatkan bila margin ≥ perkiraan atau hasil < 30 (m10 p5 → "19 orang"; m60 → "3 orang"). Contoh perintah di SKILL (`--margin 10`) menyesatkan untuk eksperimen berambang 1-5% (landing page, marketplace, TikTok). |
| B4 | Kecil | Persen memakai titik diterima sebagai desimal: `--target 1.250` → 1,25% tanpa peringatan (jumlah orang "1.250" sudah ditolak dengan benar). |
| B5 | Kecil | `--batas-stop` tanpa `--target` diabaikan diam-diam. |
| B6 | Kecil | Label tidak konsisten: script "LANJUT DENGAN CATATAN", tabel SKILL "LANJUT bertahap"; n < 30 dengan batas bawah ≥ T mencetak "LANJUT (kuat)" berdampingan dengan "sinyal arah saja" (10/12). |
| B7 | Kecil | Kalimat tafsir statistik kurang tepat: "kalau uji diulang, hasil sebenarnya kemungkinan besar ada di antara..." dan "bukan kebetulan (dengan keyakinan sekitar 95%)" (p-value bukan peluang kebenaran). |
| B8 | Saran | SKILL tidak menyuruh menerjemahkan konversi ke "berapa orang harus ditawari untuk X unit" (dilakukan penguji di S1; sangat berguna untuk keputusan batch). |

## 5. Permintaan perbaikan (untuk pembuat; penguji tidak mengubah skill)
1. **B1:** di `cmd_banding`, bila ada sel < 5 atau n < 50 per varian, jangan cetak "memang lebih baik"; ganti "ada tanda B lebih baik, tapi sampel terlalu kecil untuk yakin". Pertimbangkan Fisher exact (bisa dengan `math.comb`, tetap Python standar) untuk sel kecil. Tambah tes 0/10 vs 4/10.
2. **B2:** tambah subperintah/opsi `sampel --banding --a 15 --b 25` (power 80%, alfa 5%) atau tabel siap pakai di references (mis. 10→20%: ±200; 15→25%: ±250; 10→15%: ±690; 20→25%: ±1.100 per varian). Ganti angka "150-300" dan "100-150" di SKILL.md & references; hapus baris "SEBANYAK itu untuk TIAP varian".
3. **B3:** `sampel` beri peringatan bila margin ≥ perkiraan atau n < 30; di SKILL.md, sarankan margin ≈ separuh ambang untuk eksperimen berkonversi rendah.
4. **B4:** tolak/konfirmasi persen berpola ribuan (`\d{1,3}\.\d{3}`) atau > 100 dengan pesan jelas.
5. **B5:** error atau peringatan bila `--batas-stop` diberikan tanpa `--target`.
6. **B6:** samakan label ("LANJUT BERTAHAP") di script, SKILL, contoh, README; bila n < 30, turunkan "LANJUT (kuat)" jadi "LANJUT bertahap (sampel kecil)".
7. **B7:** ubah tafsir menjadi "dengan data ini, angka sebenarnya kemungkinan besar di antara ..." dan "selisih sebesar ini jarang muncul hanya karena kebetulan".
8. **B8:** tambah langkah singkat di Langkah 6: "target produksi ÷ konversi (dan ÷ batas bawah) = jumlah orang yang perlu ditawari".

## 6. Skor
**7/10 — LULUS (batas bawah).**
- (+) Angka inti benar dan teruji (Wilson, z, sampel), input rusak ditangani rapi, alur LANJUT/UBAH/STOP jelas, konteks UMKM Indonesia & etika pre-order kuat, menang A/B dan banding pesaing, lisensi/atribusi rapi.
- (−) Janji "tidak overclaim pada sampel kecil" belum sepenuhnya ditepati (B1), panduan sampel dua varian terlalu optimis (B2), beberapa celah validasi kecil (B3-B5).
- Rekomendasi: perbaiki **B1 dan B2 sebelum naik ke `beta`**; lalu uji ulang singkat oleh penguji independen.

## Catatan revisi v1.0.1 (pembuat, 2026-09-29)
Menindaklanjuti permintaan perbaikan B1-B8. Belum diuji ulang oleh penguji independen.

| ID | Perbaikan |
|---|---|
| B1 | `fisher_tepat()` (uji Fisher tepat dua sisi, `math.comb`) dipakai otomatis bila ada sel harapan < 5 atau < 50 orang per varian. Pada sampel kecil script tidak pernah menyatakan pemenang; p < 0,05 menjadi "ada tanda ..., tapi sampel terlalu kecil untuk yakin". 0/10 vs 4/10 kini p Fisher 0,0867 -> "BELUM meyakinkan". Tes baru untuk 0/10 vs 4/10, 0/20 vs 5/20, 9/60 vs 15/60. |
| B2 | `sampel --banding --a X --b Y` (power 80%, alfa 5% dua sisi, pendekatan normal). Angka "150-300" (SKILL) dan "100-150" (references) diganti tabel hasil hitung: 5 vs 10% = 435; 10 vs 20% = 199; 15 vs 25% = 250; 10 vs 15% = 686; 20 vs 25% = 1.094 per varian. Baris "SEBANYAK itu untuk TIAP varian" dihapus, diganti rujukan ke `--banding`. Contoh 02 memakai hitungan ini. |
| B3 | `sampel` memperingatkan bila margin >= perkiraan (menyarankan margin separuh perkiraan) dan bila hasil < 30 orang. SKILL: margin ≈ separuh ambang untuk eksperimen berkonversi rendah; contoh perintah diganti `--margin 5`. |
| B4 | Persen berpola ribuan (`1.250`, `2.500`, `1,250,000`) ditolak dengan pesan jelas; desimal koma (`1,25`) tetap diterima. |
| B5 | `--batas-stop` tanpa `--target` kini memberi PERINGATAN (tidak diam-diam diabaikan). |
| B6 | Label seragam "LANJUT BERTAHAP" di script, SKILL, references, README, contoh 00/01. n < 30 dengan batas bawah >= T -> "LANJUT BERTAHAP (sampel kecil)", bukan "kuat". |
| B7 | Tafsir diubah: "dengan data ini, angka sebenarnya kemungkinan besar ada di antara ..." dan "selisih sebesar ini jarang muncul hanya karena kebetulan"; SKILL melarang menyebut p-value sebagai peluang benar. |
| B8 | Langkah 6: "target pembeli ÷ konversi = orang yang perlu ditawari", dihitung dengan konversi tengah dan batas bawah, dengan contoh. |

**Verifikasi angka independen** (scratchpad, tidak memakai kode skill): Fisher dengan pecahan & faktorial (0/10 v 4/10 = 0,0867; 0/20 v 5/20 = 0,0471; 9/60 v 15/60 = 0,2536); ukuran sampel dengan mencari n terkecil yang power normalnya >= 0,80 (`statistics.NormalDist`), power di n-1 < 0,80 untuk semua kasus tabel -> cocok 100%.
Tes: `python3 tests/uji_hasil_eksperimen.py` -> "Semua uji lolos." Rekaman uji lama (`00-banding-pesaing.md`, `05-uji-independen-5-skenario.md`) sengaja tidak diubah.
