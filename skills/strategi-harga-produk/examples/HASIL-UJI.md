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
