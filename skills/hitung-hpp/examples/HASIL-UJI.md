# HASIL UJI — hitung-hpp

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja `/tmp/uji-hitung-hpp/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (00)

## Audit keamanan
- `scripts/hitung_hpp.py`: hanya `argparse, csv, json, re, sys, decimal`. Hanya membaca file `--file`; tidak menulis file, tidak ada jaringan/subprocess/kredensial.
- SKILL.md/README/references/templates: tidak ada prompt injection. **Aman.**

## Verifikasi angka (independen)
- Script terpisah (`verif.py`, tabel satuan & rumus sendiri dengan `fractions.Fraction`, tidak mengimpor script skill) membandingkan **250 resep acak** (1–4 bahan dengan konversi kg/g, l/ml, yard/m, m/cm, lusin/kodi/gross/rim, ons, inch/mm; susut 0–10%; upah per jam per unit/batch; overhead per batch/bulan; kemasan; alat; biaya tetap lain; margin 0–80% atau markup 0–200%; pembulatan 1/500/1000) → **0 selisih** pada HPP, biaya variabel, biaya tetap bulanan, harga rekomendasi, BEP unit, dan BEP rupiah.
- Template `contoh-hpp.json` / contoh SKILL.md (brownies: HPP Rp47.158,33; harga Rp78.597,22 → Rp79.000; BEP 17 loyang / Rp1.280.767; coklat Rp10.000/loyang): **benar**. README "HPP Rp47.158, Rp79.000, BEP 17": **benar**.
- Konversi: 1 yard = 91,44 cm, 1 gross = 144, 1 kodi = 20, 1 lusin = 12, 1 rim = 500, 1 ons = 100 g — benar.
- Alokasi overhead: biaya per bulan ÷ produksi per bulan; per batch ÷ hasil per batch; BEP memakai biaya tetap bulanan (bulanan dalam HPP + penyusutan + biaya tetap lain) tanpa dihitung ganda. **Benar.**
- Margin vs markup: margin = laba ÷ harga, markup = laba ÷ HPP; kesetaraan m/(1−m) dan k/(1+k) benar.
- Data tepi: "Rp 14.000", "1.500.000,50", CSV `;` dengan "1jt", isi_beli 0, margin 100%, margin + markup bersamaan, satuan "sdm", liter→gram, CSV kosong, CSV tanpa kolom kategori, JSON rusak, file tidak ada, bahan kosong, biaya bulanan tanpa produksi per bulan → ditolak dengan `ERROR:` yang jelas.

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Contoh frasa awam lengkap ("modal per pcs berapa", "HPP resep", "BEP") + EN |
| Kemudahan awam | 8 | Pengguna cukup bercerita; agent yang menyusun JSON/CSV. Data yang dibutuhkan memang banyak |
| Kualitas output | 9 | Tabel "cara hitung" yang bisa dicek ulang, ringkasan variabel vs tetap, BEP + % dari rencana produksi |
| Akurasi (angka/fakta) | 10 | 0 selisih pada 250 resep acak; semua contoh dokumen benar |
| Penanganan input kurang | 9 | Tanya sekali, 5 butir, antisipasi takaran sendok |
| Penanganan di luar cakupan | 8 | Rujukan jelas; tanpa kalimat cadangan bila skill rujukan tidak dimiliki |
| Keamanan | 10 | Bersih |

## SKOR AKHIR: **9 / 10** — LULUS

Uji A/B: dengan skill jelas lebih baik — agent tanpa skill menukar margin dengan markup (harga Rp9.500 vs Rp11.000, margin nyata ±26,8% bukan 35%) dan tidak memberi BEP. Tidak ada cacat berat atau sedang.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- Tidak ada.

### Ringan
1. "Laba per unit" di bagian Harga jual belum dikurangi `biaya_tetap_lain` (mis. admin Rp1 juta/bulan di S2 ≈ Rp5.000/kemeja), tanpa label. Awam bisa mengira itu laba bersih. Saran: di `teks()` baris "Harga rekomendasi", tulis "laba kotor … (sebelum biaya tetap lain ±Rp…/unit)" bila `biaya_tetap_lain` ada.
2. Pengingat "upah pemilik belum dihitung" hanya ada di SKILL.md (langkah 5), tidak dicetak script. Saran: bila `tenaga_kerja` kosong, tambahkan catatan otomatis di output.
3. Judul "**Harga jual** (dibulatkan ke atas kelipatan Rp 500)" tetap tampil pada mode cek harga saja (S3), padahal tidak ada pembulatan. Saran: tampilkan keterangan pembulatan hanya bila ada `harga_rekomendasi`/`pilihan_margin`.
4. Angka seperti "1.250" pada `pakai` dibaca 1.250 (ribu), bukan 1,25. Sudah konsisten dengan aturan format Indonesia dan terdokumentasi, tetapi untuk takaran (kg/liter/meter) rawan salah ketik. Saran: bila satuan pakai kg/l/m/yard dan nilai ≥ 1.000, beri peringatan "apakah maksud Anda 1,25?".
5. SKILL.md "Kapan TIDAK digunakan": tambahkan kalimat cadangan bila `harga-jual-marketplace`, `laporan-keuangan-emkm`, atau `surat-penawaran-harga` tidak terpasang.
