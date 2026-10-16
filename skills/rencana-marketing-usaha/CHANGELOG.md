# Riwayat perubahan — rencana-marketing-usaha

## Catatan revisi 1.0.7 (2026-10-16)
- Revisi dari uji di bot Telegram asli (gelombang 18): label keluaran `target` "Minimal pesanan agar balik modal iklan" keliru bila ada laba target, karena angkanya (mis. 405) adalah syarat mencapai laba target, bukan titik impas. Kini bila ada laba target keluaran memakai "Minimal pelanggan agar sesuai target (biaya iklan maks. Rp 8.000/pelanggan, laba Rp 2.000/pelanggan)" dan menampilkan baris baru "Titik impas iklan" (mis. 324 pelanggan untuk anggaran Rp3.240.000 dan margin Rp10.000). Tanpa laba target label lama tetap, karena minimal memang sama dengan titik impas. Kunci data baru: `pesanan_impas_iklan` (dibulatkan ke atas). Rumus lain tidak berubah.
- `SKILL.md` (Format Output): untuk kanal chat dilarang menyebut kata "script", "skill", atau nama skill lain ke pengguna, dan total anggaran ditulis sebagai satu angka yang sudah termasuk cadangan ("Rp9.000.000, sudah termasuk cadangan Rp900.000").
- `scripts/uji_regresi.py`: ekspektasi label diperbarui dan uji baru untuk titik impas (324, GoFood 338, tanpa laba target, tanpa anggaran iklan). Contoh lama di `examples/` ditulis sebelum perubahan label ini.
- Contoh disegarkan (2026-10-16): keluaran script di `examples/01-kedai-kopi-q4.md`, `01-uji-warung-bakso.md`, `02-uji-skincare-lokal.md`, dan `03-uji-jasa-renovasi.md` dijalankan ulang dengan v1.0.7 (label baru + "Titik impas iklan" 135 / 324 / 230; skincare minimal 287, sebelumnya 286 karena pembulatan lama). Skor/verdik uji tidak berubah; rincian di `examples/HASIL-UJI.md` bagian "Contoh disegarkan ke v1.0.7". `00-*.md` dibiarkan sebagai catatan uji historis.

## Catatan revisi 1.0.6 (2026-10-13)
- Aturan eksplisit anti-karangan di `SKILL.md` (Batasan & Penanganan Error): jangan mengarang spesifikasi produk, bahan, ukuran, angka pasar/kanal, atau klaim hasil; yang tidak diberikan pengguna ditulis `[isi: ...]` atau ditandai asumsi.
- Contoh `examples/03-uji-jasa-renovasi.md` dijalankan ulang oleh penguji independen: klaim "70% usaha datang dari sini" dan angka lain tanpa sumber (komisi referral, laba target, wilayah, usia segmen, jumlah ulasan) diganti "DATA BELUM ADA", `[isi: ...]`, atau asumsi bertanda. Status margin 21,4% kini TIPIS sesuai ambang script saat ini. Alur kerja dan script tidak berubah.

## 1.0.5 (2026-10-13) — rujukan ke skill arsip diganti
Rujukan ke `kalender-konten-30hari` (skill arsip, tidak dijual) di `SKILL.md` (bagian "Kapan TIDAK digunakan" dan langkah 7) diganti ke `konten-mingguan`. Alur kerja tidak berubah.
