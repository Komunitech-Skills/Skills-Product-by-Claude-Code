# 00 — Uji A/B: S1 dengan skill vs tanpa skill

**Permintaan (sama):** THR Idul Fitri 1448 H (10 Maret 2027) untuk Budi (tetap, sejak 2019), Rina (kontrak, masuk 15 Juni 2026), Joko (harian lepas, upah bulanan bervariasi), Wati (tetap, PHK 20 Februari 2027) + pengumuman. Lihat `01-thr-lebaran-4-karyawan.md`.

Metode: jawaban "tanpa skill" disimulasikan penguji sebagai AI agent biasa tanpa membuka SKILL.md/script. Penguji sudah membaca Permenaker 6/2016, jadi simulasi ini cenderung optimistis.

## Berdampingan

| Aspek | Tanpa skill (AI agent biasa) | Dengan skill `hitung-thr` |
|---|---|---|
| Budi | Rp 5.500.000 | Rp 5.500.000 |
| Rina | "Masa kerja Juni 2026–Maret 2027 ± 9 bulan → 9/12 × 4,8 jt = Rp 3.600.000" (menghitung bulan kalender, bukan bulan penuh) | 8 bulan penuh (15 Jun → 15 Feb; belum sampai 15 Mar) → **Rp 3.200.000**, cara hitung masa kerja disebut sebagai asumsi |
| Joko (harian) | "Rata-rata upah Rp ±3 jt" (dihitung kasar dari semua data) | Rata-rata tepat 12 bulan terakhir **Rp 3.008.333**, dengan dasar aturan harian lepas |
| Wati (PHK) | Sering dijawab "sudah bukan karyawan, tidak wajib THR" atau ragu-ragu | Berhak (PKWTT, PHK ≤ 30 hari sebelum hari raya, Permenaker 6/2016 Pasal 7) → **Rp 5.200.000** |
| PPh 21 atas THR | "THR kena PPh 21, digabung gaji bulan dibayar" — tanpa angka | Tambahan PPh 21 per orang dari TER (Budi Rp 286.500, Rina Rp 120.000) + peringatan bila bruto bulan bayar tidak diisi |
| Batas bayar | "Paling lambat H-7" | Tanggal pasti: **Rabu, 3 Maret 2027**, peringatan denda 5% bila terlambat |
| Pengumuman | Bisa dibuat, kadang memuat nominal pribadi | Draf siap kirim tanpa nominal pribadi |
| Rekap | Di chat saja | Juga file CSV |

## Penilaian singkat
Tanpa skill, total THR bisa meleset (Rina kelebihan Rp 400.000 bila memakai bulan kalender; Wati berisiko tidak dibayar padahal berhak → pelanggaran), dan potongan pajak tidak dihitung. Dengan skill, besaran THR benar dan lengkap dengan batas bayar, PPh 21, dan pengumuman. **Skill jelas lebih baik.** (v1.0.1: PPh 21 THR karyawan yang sudah berhenti kini memakai aturan Mantan Pegawai — Wati Rp 260.000 — dan DTP dicek tahun & batas Rp 10 jt.)
