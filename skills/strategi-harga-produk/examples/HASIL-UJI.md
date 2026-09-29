# HASIL UJI — strategi-harga-produk

- **Tanggal:** 2026-09-29
- **Penguji:** agent penguji independen (bukan pembuat), Claude Code. Output skenario dibuat oleh sesi `claude -p` baru dengan skill terpasang di folder sementara (tanpa `examples/`) → `platform_teruji` yang jujur: `claude-code (simulasi agent)`.
- **Lingkungan:** `scratchpad/uji-harga/` (di luar repo), Python 3 standar.
- **Berkas:** `00-pembanding-tanpa-skill.md`, `00-banding-pesaing.md`, `01`–`05`. Contoh pembuat `contoh-01..05` dibiarkan.

## 1. Audit keamanan & format
- Frontmatter hanya `name` + `description`; `name` = nama folder; deskripsi 1 baris berisi kata kunci ID & EN ✔. `python3 scripts/validate.py --skill strategi-harga-produk` → **lolos** (1 skill valid).
- `scripts/strategi_harga.py` hanya `argparse, re, sys, decimal`; `tests/uji_regresi.py` hanya pustaka standar. Tidak ada jaringan, subprocess, baca/tulis file, kredensial, `eval/exec`, base64 ✔. Uji regresi pembuat: 35 tes OK.
- SKILL.md/README/references: tidak ada prompt injection, tidak ada data pribadi/API key ✔.
- Lisensi: kedua sumber MIT; teks lisensi lengkap disertakan (`LICENSE-MIT-marketingskills` © 2025 Corey Haines, `LICENSE-MIT-pm-skills` © 2026 Pawel Huryn); commit snapshot dicocokkan penguji dengan clone sendiri (`5b2c000…`, `8607e3b…`) ✔. `ATTRIBUTION.md` menyebut bagian turunan vs orisinal, audit sumber, dan keterangan tidak berafiliasi dengan marketplace ✔. Uji banding: tidak ada teks sumber yang tersalin utuh di skill (kerangka ditulis ulang, konteks UMKM).

## 2. Verifikasi angka independen
Script penguji (`verif.py`, Fraction/Decimal sendiri; fungsi skill hanya dibandingkan nilainya):
- **PPN** (standar CLAUDE.md): 9.045 kasus (harga 1 – 5 jt acak + tepi; mode sebelum PPN, termasuk PPN non-mewah 11% & mewah 12%), DPP termasuk-PPN dicari brute force "bulat terbesar dengan DPP + floor(PPN) ≤ harga" → **0 selisih**, sisa selalu benar.
- **Margin/harga minimum/diskon/beli-X-gratis-Y/BEP:** 3.000 kasus acak dengan potongan marketplace 0–25% → **0 selisih**; properti harga minimum (margin tercapai di H, tidak di H−1) selalu benar.
- **Harga cantik:** 3.000 kasus → **0 selisih**: setiap kandidat sesuai polanya (x.900, x9.900, x9.000, bulat, kelipatan 500), kandidat x.900 dan x9.900 terdekat di atas/bawah selalu ada, status "di bawah batas" tepat untuk kandidat < lantai.
- Contoh SKILL.md/README (BEP 394, laba Rp3.400.000, batas aman 34,33%, diskon 20% → +51,38% / 909 pcs, lantai agen Rp17.693, tangga 28.000/24.000/21.000/18.000) dan tabel cepat di `references/aturan-promo.md` (12 sel) → **benar**.
- Semua angka hasil script di skenario 01–03 benar. **Angka yang dihitung manual oleh agent** di skenario 03 ada yang salah (lihat cacat no. 1).

## 3. Data rusak (script)
Ditolak dengan `GAGAL: …` kode 2 dan bahasa awam: HPP "abc", "28.000.00", "1e5", margin + potongan ≥ 100%, potongan 100%, diskon 100%, potongan ≥ harga, beli 2:0, level "Reseller:sepuluh:15", item jumlah "x", paket 1 item, elastisitas positif, perubahan −100%, tanpa skenario, harga 0, BEP saat harga < HPP. Paket rugi / tangga terbalik / promo rugi → PERHATIAN yang jelas.
Temuan (lihat cacat): harga < HPP di `margin` tidak diberi peringatan; batas aman negatif ditulis "boleh turun −31,33%"; `--hari-jual -5` diterima ("−78 unit"); traceback `DivisionByZero` bila harga jadi Rp0 (harga ecer Rp300 + `--kelipatan 500`, atau harga Rp1 diskon 60%); "12.5" dibaca Rp12,5 tanpa peringatan (markup 223.900%).

## 4. Skenario
| # | Skenario | Hasil | Nilai |
|---|---|---|---|
| 01 | Normal: kopi literan naik harga + reseller + kantor | Lengkap & benar; harga rekomendasi dihitung manual; saran harga reseller bertentangan dengan harga toko | 7,5 |
| 02 | Normal + potongan marketplace 17%: diskon 11.11 vs beli 2 gratis 1 | Benar, batas diskon maks 27,12%, alternatif jelas; 1 angka kasar tanpa script | 8 |
| 03 | Normal + PKP/PPN: harga termasuk PPN, margin dari DPP, BEP, paket | PPN/margin/BEP/estimasi benar; 2 angka alternatif paket salah (manual) | 6,5 |
| 04 | Input kurang (keripik pisang) | Tanya sekali, 5 pertanyaan, default disebut | 9 |
| 05 | Di luar cakupan (kartel semen) | Menolak + alternatif sah; ada klaim hukum tambahan kurang tepat | 8,5 |

**Uji A/B:** dengan skill **lebih baik** (BEP, lantai margin, estimasi berlabel, asumsi, teks siap tempel), tetapi selisihnya sedang karena agent tanpa skill sudah kuat di kasus ini.
**Uji banding pesaing:** menang atas `coreyhaines31/marketingskills` `pricing` (±62 rb instal): 8,2 vs 6,2.

## 5. Skor
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Frasa awam ("diskon 20% masih untung?", "harga 49.900 atau 50.000") + EN; skill terpanggil otomatis di 5/5 skenario |
| Kemudahan awam | 8 | Satu kalimat cukup; input angka gaya Indonesia |
| Kualitas output | 8 | Format 7 bagian konsisten, siap tempel |
| Akurasi | 7 | Script 0 selisih; tetapi agent masih menghitung manual untuk harga rekomendasi (S1–S3) dan 2 angka salah di S3 |
| Input kurang / di luar cakupan | 9 | Sesuai aturan |
| Keamanan & lisensi | 10 | Bersih |

## SKOR AKHIR: **7 / 10 — LULUS (bersyarat)**
Tidak ada batas skor 6: A/B dan uji pesaing dimenangkan. Cacat no. 1–3 sebaiknya diperbaiki sebelum status `beta`/uji platform asli; setelah perbaikan, uji ulang skenario 03 oleh penguji independen.

## 6. Permintaan perbaikan (tidak diperbaiki penguji)
### Sedang
1. **Jalur PKP belum bisa dihitung sepenuhnya oleh script** → agent hitung manual dan salah (S3: lantai paket "Rp176.700" seharusnya Rp176.675; Rp169.900 margin "~38,9%" seharusnya 37,61%, sisa Rp1). Saran: tambahkan opsi `--harga-termasuk-ppn` (atau `--ppn termasuk`) pada `margin`, `bundel`, `cantik`, `tangga`, `elastisitas` yang mengubah harga tayang ke DPP dengan `hitung_ppn` lalu menghitung margin dari DPP; dan pada `margin --margin X --ppn termasuk` tampilkan harga tayang minimum termasuk PPN. Tambahkan tes regresi untuk 169.900 dan 176.675.
2. **Agent tidak menjalankan script untuk harga yang akhirnya direkomendasikan** (S1 tabel akhir, S2 "diskon 25% ±600 pcs", S3 tabel alternatif). Saran di SKILL.md Langkah 4: "Setiap harga di Ringkasan dan Tabel harga WAJIB dari satu perintah script (mis. `tangga --harga-ecer <harga baru> --level Nama:min:=harga`). Jangan tulis 'dihitung manual' bila script bisa dijalankan." Tambahkan juga ke Format output: kolom Status OK/DI BAWAH MIN wajib dari script, dan harga di bawah margin minimum pilihan pengguna harus ditandai (S3 menyarankan 35,7% padahal minimum 40% tanpa tanda).
3. **Konsistensi harga antar-kanal** (S1: toko Rp47.900 tetapi reseller "jual minimal Rp49.900"). Saran di `references/pilihan-strategi.md` bagian tangga + Format output: "Harga eceran anjuran reseller = harga eceran toko yang berlaku; bila harga naik bertahap, perbarui keduanya bersamaan."
### Ringan
4. `margin` dengan harga ≤ HPP: tampilkan `PERHATIAN: harga di bawah modal, setiap unit rugi` (SKILL.md menjanjikan GAGAL/peringatan untuk HPP ≥ harga).
5. `bep --volume` di bawah BEP: ganti "Batas aman: −31,33% penjualan boleh turun" menjadi "Penjualan masih kurang X unit (Y%) dari titik impas".
6. `--hari-jual` ≤ 0 → GAGAL; `--hari-jual 0` saat ini diam-diam diabaikan.
7. Tangkap pembagian nol (harga hasil diskon/kelipatan = Rp0) → `GAGAL: harga hasil pembulatan menjadi Rp0`.
8. `parse_rupiah`: angka dengan satu titik dan 1–2 desimal ("12.5") ambigu; beri GAGAL/konfirmasi, atau peringatan bila HPP < 1% harga.
9. `cetak_diskon`: laba promo ditampilkan bersen ("Rp14.231,90") sementara laba normal dibulatkan; samakan (bulatkan tampilan, hitung tetap presisi).
10. Kasus di luar cakupan (kartel): tambahkan di SKILL.md bahwa penolakan cukup menyebut UU 5/1999 tanpa klaim sanksi/penerapan spesifik (agent S5 menulis "toko kecil juga bisa kena", padahal Pasal 50 huruf h mengecualikan usaha kecil).
11. Tawarkan `bundel` saat ada peluang paket (pesaing menyarankan "2 botol Rp95.000", agent kita tidak).

---

## Catatan revisi 1.0.1 (oleh pembuat, 2026-09-29)
Teks penguji di atas tidak diubah. Status tetap `uji`; perlu uji ulang independen (terutama skenario 03).

| # | Permintaan | Perbaikan | Tes regresi |
|---|---|---|---|
| 1 | Jalur PKP dihitung penuh oleh script | Opsi `--ppn termasuk\|belum` (+ `--mewah`) di `margin`, `bep`, `tangga`, `diskon`, `bundel`, `elastisitas`, `cantik`. Harga tayang → DPP dengan standar CLAUDE.md (DPP bulat terbesar, PPN ke bawah sekali, sisa ditampilkan); margin dari DPP; potongan % dari harga tayang; harga minimum dikembalikan sebagai harga tayang. `margin --margin 40 --ppn termasuk` (HPP 95.500) → **Rp176.675** (DPP 159.167 + PPN 17.508); `margin --harga 169.900 --ppn termasuk` → DPP 153.063, sisa Rp1, margin **37,61%** | `Revisi101Pkp` (9 tes: 176.675, 169.900, 164.900, bundel S3, BEP 523 & volume impas 644, mode `belum`, cantik/tangga PPN, markup, CLI) |
| 2 | Semua harga rekomendasi wajib dari script | SKILL.md Langkah 4: setiap harga di Ringkasan/Tabel/teks siap tempel (eceran baru, reseller, paket alternatif, promo, harga cantik) WAJIB dari satu perintah script; "dihitung manual" hanya bila Python tidak ada. Status OK/DI BAWAH MIN wajib disalin dari script. Baru: `margin --harga X --margin-min Y` memberi status; `diskon --margin-min` menandai promo di bawah minimum | `Revisi101Dokumen`, `test_status_margin_min_pada_margin_dan_diskon` |
| 3 | Harga reseller konsisten dengan harga toko | `tangga` menampilkan kolom "Untung reseller/unit" (harga anjuran − harga beli reseller). Anjuran default = `--harga-ecer`; `--harga-anjuran` berbeda → PERHATIAN. PERHATIAN juga bila reseller tidak untung, untung < `--margin-reseller-min` (default 10%), atau harga level > eceran. SKILL.md bagian 6b + `references/pilihan-strategi.md`: anjuran = harga toko, diperbarui bersamaan | `Revisi101Reseller` (4 tes, termasuk kasus S1 47.900 vs 49.900) |
| 4 | `margin` harga ≤ HPP | `PERHATIAN: harga di bawah modal ... setiap unit RUGI Rp...` | `test_4_harga_di_bawah_modal` |
| 5 | Batas aman negatif | Diganti "penjualan masih kurang X unit (Y%) dari titik impas"; volume 0 ditangani | `test_5_batas_aman_tidak_negatif` |
| 6 | `--hari-jual` ≤ 0 | GAGAL (juga teks non-angka) | `test_6_hari_jual_harus_positif` |
| 7 | Pembagian nol | GAGAL "... menjadi Rp0" di `tangga` (kelipatan), `diskon`, `elastisitas`; plus jaring pengaman ArithmeticError → GAGAL tanpa traceback | `test_7_tanpa_pembagian_nol` |
| 8 | "12.5" ambigu | Angka bertitik yang bukan pola ribuan ditolak (GAGAL, contoh penulisan benar); `margin` memberi PERHATIAN bila HPP < 1% harga | `test_8_angka_ambigu_ditolak` |
| 9 | Laba promo bersen | Tampilan laba dibulatkan (hitungan tetap presisi); harga beli-X-gratis-Y diberi label "harga efektif per unit" | `test_9_laba_promo_dibulatkan_di_tampilan` |
| 10 | Klaim hukum kartel | SKILL.md: cukup sebut UU 5/1999 tanpa klaim sanksi/penerapan spesifik (ada pengecualian, mis. usaha kecil) | `test_kartel_tanpa_klaim_sanksi` |
| 11 | Tawarkan `bundel` | SKILL.md 6b: bila ada peluang paket, tawarkan satu opsi paket yang dicek `bundel --margin-min` | `Revisi101Dokumen` |

**Hasil:** `python3 tests/uji_regresi.py` → 57 tes OK (35 lama + 22 baru). `python3 scripts/validate.py --skill strategi-harga-produk` → lolos.
**Verifikasi angka independen** (Fraction + brute force, di luar repo; hanya nilai hasil script yang dibandingkan): harga minimum PKP/non-PKP 4.000 kasus (mode termasuk/belum/tanpa, PPN 11%/12%, potongan 0–25%, margin 0–70%; setiap hasil memenuhi target dan 300 harga di bawahnya tidak) → 0 selisih; margin PKP 4.000 → 0; bundel PKP 2.000 → 0; untung reseller & peringatan 2.000 → 0; diskon PKP 2.000 → 0. Verifikasi pertama menemukan 6 kasus salah pada potongan sangat besar (margin + 2 × potongan > 100%, laba naik-turun karena pembulatan PPN); pencarian DPP minimum diganti menjadi scan dari batas bawah matematis → 0 selisih.
**Tidak berubah untuk non-PKP:** keluaran 11 perintah contoh dibandingkan dengan 1.0.0; perbedaan hanya kolom untung reseller, label "DI BAWAH MIN" di `cantik`, dan keterangan "dari harga".
