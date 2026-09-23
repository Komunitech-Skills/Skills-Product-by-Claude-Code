# HASIL UJI — hitung-ppn

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja `/tmp/uji-hitung-ppn/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (00)

## Audit keamanan
- `scripts/hitung_ppn.py`: hanya `argparse, json, re, sys, decimal`. Tidak ada jaringan, subprocess, penulisan file, atau pembacaan kredensial.
- SKILL.md/README/references: tidak ada prompt injection atau instruksi berbahaya. **Aman.**

## Verifikasi angka (independen)
- Script terpisah (`verif.py`, memakai `fractions.Fraction`, tidak mengimpor script skill) membandingkan **600 kasus acak** (harga 0–10^9, qty 1/3/12, umum/mewah, pembulatan bawah/terdekat, mode sebelum & termasuk PPN) → **0 selisih**.
- Mode termasuk PPN dicek dengan brute force "DPP bulat terbesar dengan DPP + PPN ≤ harga" → identik.
- Contoh di SKILL.md/README (7,5 jt termasuk PPN → DPP 6.756.757, DPP nilai lain 6.193.693,92, PPN 743.243) dan contoh 1 jt → PPN 110.000: **benar**.
- Data tepi: "Rp 1.500.000", "1.500.000,50", "Rp 1.250.000,-", "1.500rb", "1 500 000", "4,8M", "0" → terbaca benar; "1,250,000.50", "abc", "", "-5000", qty 0 → ditolak dengan `ERROR:` yang jelas.

## Konsistensi lintas library (PENTING)
- `hitung-ppn` dan `buat-invoice` membulatkan PPN **ke bawah**; `surat-penawaran-harga` membulatkan **ke terdekat** (ROUND_HALF_UP). Dari 10.000 harga uji (Rp1–Rp10.000), **50%** menghasilkan PPN berbeda Rp1.
- Contoh nyata: harga Rp 1.000.005 → SPH: PPN Rp 110.001 / total Rp 1.110.006; hitung-ppn & invoice: PPN Rp 110.000 / total Rp 1.110.005. Penawaran dan invoice untuk transaksi yang sama akan berbeda Rp1.
- Mode harga termasuk PPN juga beda algoritma: Rp 11.100.050 → SPH: DPP 10.000.045 + PPN 1.100.005 (total = harga); hitung-ppn: DPP 10.000.045 + PPN 1.100.004 + selisih Rp1.
- **Rekomendasi satu standar:** PPN = tarif efektif × DPP dihitung dari nilai tepat, **dibulatkan sekali ke bawah** (buang pecahan rupiah) — tidak pernah menagih lebih dari tarif, sesuai praktik faktur yang lazim, dan sudah dipakai 2 dari 3 skill. Nilai rupiah lain (jumlah baris, diskon) tetap dibulatkan ke terdekat. Mode termasuk PPN: DPP bulat terbesar sehingga DPP + PPN ≤ harga (algoritma hitung-ppn), selisih ditampilkan. Satukan dalam satu modul bersama (mis. `hitung_ppn.py` yang juga dipakai SPH), dan cantumkan di semua SKILL.md bahwa perilaku Coretax belum diverifikasi (sudah ada di `references/regulasi.md` skill ini).

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Kata kunci ID/EN lengkap, batas dengan buat-invoice & pph-final-umkm jelas |
| Kemudahan awam | 9 | Cukup satu kalimat; format angka Indonesia fleksibel |
| Kualitas output | 8 | Rapi, lengkap (DPP nilai lain, pembulatan, disclaimer); belum ada pola "cek tagihan supplier" |
| Akurasi (angka/fakta) | 9 | 0 selisih pada 600 kasus; dasar aturan bertanggal; pembulatan tidak konsisten dengan SPH (lintas skill) |
| Penanganan input kurang | 9 | Default & asumsi jelas, tanya sekali |
| Penanganan di luar cakupan | 8 | Daftar di luar cakupan jelas; belum ada contoh jawaban baku |
| Keamanan | 10 | Bersih |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: dengan skill lebih baik (kelengkapan, pembulatan, dasar aturan, pengingat PKP), tetapi selisih moderat untuk kasus angka bulat. Tidak ada cacat berat.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Pembulatan PPN berbeda dengan `surat-penawaran-harga`** (lihat bagian konsistensi). Saran: tetapkan standar "ke bawah" di seluruh library; ubah `surat-penawaran-harga/scripts/hitung_sph.py` bagian PPN (saat uji di baris ±235–247: `bulat(Fraction(dpp) * efektif)` dan cabang harga termasuk PPN) agar memakai `hitung_ppn.hitung_ppn_dari_dpp(..., "bawah")`, dan perbarui SKILL.md SPH langkah 4 ("Bulatkan sekali ke rupiah terdekat").

### Ringan
2. `parse_angka("2.5")` dibaca Rp 2,50 tanpa peringatan. Pengguna yang mengetik "2.5" (maksud 2,5 juta) akan mendapat hasil absurd. Saran: bila hasil < Rp 100 dan ada titik desimal, tambahkan catatan "Apakah maksud Anda 2,5 juta?" di output.
3. Mode `--qty` dengan pecahan (mis. 2,5) diterima tanpa catatan; wajar untuk kg/jam, tetapi sebaiknya label "Jumlah" menyebut satuan. Opsional.
4. SKILL.md bagian "Format output" belum punya pola untuk "cek tagihan supplier" (S3), padahal ini kegunaan yang disebut di "Kapan digunakan". Saran: tambahkan contoh tabel "Tagihan supplier vs seharusnya".
5. SKILL.md "Batasan": tambahkan kalimat baku untuk kasus di luar cakupan (PPN besaran tertentu, dibebaskan) agar agent tidak mengarang tarif.
