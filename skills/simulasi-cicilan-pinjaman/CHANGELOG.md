# Riwayat perubahan — simulasi-cicilan-pinjaman

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.4 (2026-10-15)
- **Dasar batas biaya pinjaman daring diganti** ke SEOJK No. 19/SEOJK.06/2025 Romawi XIV angka 2–3 (ditetapkan dan berlaku 31 Juli 2025). SEOJK No. 19/SEOJK.06/2023 yang dirujuk sebelumnya sudah dicabut (Romawi XXII angka 1), sehingga angka lama 0,1%/hari konsumtif dan 0,067%/hari produktif "sejak 1 Januari 2026" dihapus. Batas yang berlaku: konsumtif 0,3%/hari (tenor sampai 6 bulan) dan 0,2%/hari (di atas 6 bulan); produktif nilai pinjaman paling tinggi Rp50 juta 0,275%/hari (tenor sampai 6 bulan) dan 0,1%/hari (di atas 6 bulan); produktif di atas Rp50 juta 0,1%/hari. Sumber: PDF resmi SEOJK 19/SEOJK.06/2025 di ojk.go.id (temuan penguji independen putaran kedua verifikasi aturan C29).
- Definisi "manfaat ekonomi" disesuaikan dengan Romawi XIV angka 2: bunga/margin + admin/komisi/fee platform + biaya lain selain denda keterlambatan, biaya tanda tangan elektronik bersertifikat, dan pajak (bea meterai tidak lagi disebut).
- `scripts/cicilan.py`: batas dipilih otomatis menurut jenis (konsumtif/produktif), tenor (sampai 180 hari = sampai 6 bulan, asumsi 1 bulan = 30 hari seperti simulasi di SEOJK; tenor 181–184 hari diberi catatan), dan nilai pinjaman di perjanjian (sampai/di atas Rp50 juta). Pembanding batas kini memakai cara hitung SEOJK: (bunga + biaya) ÷ nilai pinjaman ÷ hari, bukan dari uang yang diterima (biaya per hari dari uang diterima tetap ditampilkan). Peringatan palsu hilang: mis. konsumtif 14 hari 0,3%/hari dan 90 hari 0,25%/hari tidak lagi diberi peringatan. Bila jenis pinjol tidak disebut, konsumtif dicatat sebagai asumsi. Logika lama "tenor 365 hari ke atas tidak dibandingkan" dihapus. Rumus cicilan dan angka hitungan lain tidak berubah.
- Tes regresi: I9–I12 ditulis ulang, I13–I17 baru (tabel batas, pemilih batas per tenor/nilai, tanpa peringatan palsu, produktif, dasar nilai pinjaman, tenor 183 hari, asumsi jenis) — 57 cek lolos.
- `references/istilah-dan-jebakan.md`: tabel batas pinjol diganti (3 baris × tenor), cara hitung + contoh, asumsi 6 bulan = 180 hari; catatan rasio pembayaran ke penghasilan untuk pinjaman daring konsumtif (Romawi XIII angka 2: maks. 40% pada 2025, 30% sejak 2026 — aturan penilaian penyelenggara, patokan 30% skill tetap asumsi). Bagian baru: kredit bank umum konvensional — POJK No. 13 Tahun 2024 (Transparansi dan Publikasi SBDK) mengarahkan bank memberi tahu konversi bunga flat ke setara efektif di surat penawaran kredit (bukan untuk leasing non-bank).
- SKILL.md (Format output pinjaman harian & Batasan): dasar aturan, tanggal berlaku, dan batas per golongan disesuaikan; tetap "cek aturan OJK terbaru". README: versi terkini 1.0.4.

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
