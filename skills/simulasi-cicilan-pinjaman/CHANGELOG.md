# Riwayat perubahan — simulasi-cicilan-pinjaman

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.2 (2026-10-13)
- Batasan di SKILL.md ditambah satu aturan: setiap tarif/aturan disebut dengan dasar aturan + tahun; angka hanya dari script/input pengguna; nilai yang tidak diberikan pengguna ditandai asumsi (tanpa label "wajar/umum/lazim" yang tidak bersumber).
- Contoh uji `examples/03`: bunga ilustrasi kredit HP ditandai "asumsi ilustrasi; masukkan bunga dari penawaran Anda", tanpa kata "wajar/umum". Contoh `01`: batas cicilan 30% dari gaji ditandai patokan hati-hati, bukan aturan resmi.

## Catatan versi
- **1.0.1 (2026-10-06):** permintaan brosur/iklan kredit "bunga 0%" lebih andal memicu pola tolak → brosur transparan; ilustrasi bunga per jenis kredit (HP, motor, KPR) bila bunga belum diketahui; penjelasan KPR fixed → floating dipertegas; label "pinjaman bersih setelah biaya di muka"; rujukan aturan OJK pinjaman daring diperbarui.
- **1.0.0 (2026-10-06):** rilis awal.

---
Sebagian rumus dan kasus uji diturunkan dari numpy-financial (BSD-3-Clause, © NumPy Developers) — lihat `ATTRIBUTION.md`. Komunitech tidak berafiliasi dengan NumPy. Simulasi, bukan penawaran atau nasihat keuangan.
