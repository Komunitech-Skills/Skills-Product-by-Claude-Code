# Riwayat perubahan — simulasi-cicilan-pinjaman

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.3 (2026-10-13)
- Teks netral untuk bunga ilustrasi (logika hitung tidak berubah): `scripts/cicilan.py` tidak lagi menyebut "kisaran umum"/"biasanya flat"; judul tabel ilustrasi dan asumsi kini berbunyi "bunga ilustrasi, bukan acuan pasar - masukkan bunga dari penawaran Anda"; bantuan `--ilustrasi` ikut disesuaikan.
- Catatan kemampuan bayar di script: "Patokan umum" → "Patokan hati-hati (bukan aturan resmi)". README dan `references/istilah-dan-jebakan.md` diselaraskan (tanpa "wajar/umum" untuk patokan 30%).
- SKILL.md (bagian "Kerjakan dulu"): label ilustrasi yang wajib disebut kini "bunga ilustrasi, bukan acuan pasar atau tawaran; masukkan bunga dari penawaran Anda".
- Contoh `examples/00-openclaw-sebelum-sesudah.md` skenario 3 (1.0.1) diselaraskan dengan `examples/03` (label asumsi ilustrasi, angka tidak berubah); catatan penguji tidak lagi menyebut kisaran bunga pasar tanpa sumber. `examples/HASIL-UJI.md` disesuaikan sama.

## Catatan revisi 1.0.2 (2026-10-13)
- Batasan di SKILL.md ditambah satu aturan: setiap tarif/aturan disebut dengan dasar aturan + tahun; angka hanya dari script/input pengguna; nilai yang tidak diberikan pengguna ditandai asumsi (tanpa label "wajar/umum/lazim" yang tidak bersumber).
- Contoh uji `examples/03`: bunga ilustrasi kredit HP ditandai "asumsi ilustrasi; masukkan bunga dari penawaran Anda", tanpa kata "wajar/umum". Contoh `01`: batas cicilan 30% dari gaji ditandai patokan hati-hati, bukan aturan resmi.

## Catatan versi
- **1.0.1 (2026-10-06):** permintaan brosur/iklan kredit "bunga 0%" lebih andal memicu pola tolak → brosur transparan; ilustrasi bunga per jenis kredit (HP, motor, KPR) bila bunga belum diketahui; penjelasan KPR fixed → floating dipertegas; label "pinjaman bersih setelah biaya di muka"; rujukan aturan OJK pinjaman daring diperbarui.
- **1.0.0 (2026-10-06):** rilis awal.

---
Sebagian rumus dan kasus uji diturunkan dari numpy-financial (BSD-3-Clause, © NumPy Developers) — lihat `ATTRIBUTION.md`. Komunitech tidak berafiliasi dengan NumPy. Simulasi, bukan penawaran atau nasihat keuangan.
