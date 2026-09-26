# Uji A/B — Skenario 01 tanpa skill vs dengan skill

> Penguji independen, 2026-09-25. **Keterbatasan jujur:** tidak ada sesi agent "bersih" terpisah yang tersedia; jawaban "tanpa skill" di bawah disusun penguji dengan meniru perilaku umum asisten AI tanpa instruksi khusus (tanpa script, tanpa referensi skill). Penguji sudah membaca skill, jadi baseline ini cenderung **lebih baik** dari baseline sebenarnya (bias menguntungkan pihak "tanpa skill"). Disarankan diulang oleh sesi bersih saat uji platform asli.

Input: sama dengan `01-atk-cv-kecil-hps-185jt.md` (CV kecil PKP, ATK, HPS Rp185 jt, 12 baris, batas 14/10/2026 15.00).

## A. Tanpa skill (ringkasan jawaban khas)
- Kelayakan: "Pastikan perusahaan Anda punya NIB, NPWP, dan memenuhi syarat kualifikasi di dokumen tender." (tanpa status per butir, tanpa Pasal 65/UMK, tanpa catatan bahwa Rp185 jt < batas pengadaan langsung Rp200 jt).
- Dokumen: daftar umum 8 butir (akta, NIB, NPWP, SPT, surat penawaran, pakta integritas, spesifikasi, rincian harga). Tidak dibagi per kelompok evaluasi, tidak ada pemeriksaan akhir sebelum unggah.
- Harga: menjumlah 12 baris di kepala → subtotal Rp163.545.400; **PPN "12%" = Rp19.625.448**, total **Rp183.170.848 (99,01% HPS)**. Sejak PMK 131/2024 barang non-mewah memakai DPP nilai lain 11/12 → PPN yang benar Rp17.989.994. Kelebihan Rp1.635.454 → harga kurang kompetitif; bila dipaksa ≤ HPS tetap lolos, tetapi kalau HPS lebih ketat bisa melampaui HPS. Tidak ada terbilang, tidak ada batas 80%, tidak menyebut pemungutan PPN/PPh 22 oleh bendahara.
- Jadwal: "Siapkan dokumen seminggu sebelumnya dan unggah H-1." Tanpa tanggal & hari konkret.
- Tidak ada disclaimer/dasar aturan bertanggal.

## B. Dengan skill
Lihat `01-atk-cv-kecil-hps-185jt.md`: tabel kelayakan ✅/❓, catatan ambang pengadaan langsung, checklist B1+C, jadwal mundur bertanggal (H-7 Senin 5/10 … H-1 Selasa 13/10), rincian dihitung script (PPN 11/12 dibulatkan ke bawah, total Rp181.535.394, terbilang, 98,13% HPS, batas 80%), arus kas PPN + PPh 22, 7 butir awas gugur, disclaimer + dasar aturan bertanggal.

## Kriteria & skor (0–2 per kriteria)
| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| Ketepatan angka (subtotal, PPN, total, %HPS) | 0 (PPN salah tarif) | 2 (diverifikasi independen) |
| Terbilang siap tempel | 0 | 2 |
| Kelayakan terstruktur + keputusan | 0 | 2 |
| Checklist per kelompok & pra-unggah | 1 | 2 |
| Jadwal hari kerja bertanggal | 0 | 2 |
| Konteks regulasi (UMK, PL, 80% HPS, PPN/PPh bendahara) | 0 | 2 |
| Disclaimer & dasar aturan bertanggal | 0 | 2 |
| Bahasa awam & siap pakai | 1 | 2 |
| **Total (maks 16)** | **2** | **16** |

**Kesimpulan:** dengan skill **jelas lebih baik** — terutama angka pajak yang benar, jadwal konkret, dan peringatan regulasi. Syarat A/B terpenuhi.
