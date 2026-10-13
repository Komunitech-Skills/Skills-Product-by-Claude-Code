# Riwayat perubahan — kelayakan-investasi-usaha

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.3 (2026-10-13)
- Batasan di SKILL.md ditambah satu aturan: setiap tarif/aturan disebut dengan dasar aturan + tahun; angka hanya dari script/input pengguna; nilai yang tidak diberikan pengguna ditandai asumsi (tanpa label "wajar/umum/lazim" yang tidak bersumber).
- Contoh uji `examples/01`–`03`: patokan 12% ditulis sebagai asumsi tingkat diskonto contoh (ganti dengan bunga pinjaman Anda + premi risiko pilihan Anda), tidak lagi menyebut tarif KUR tanpa sumber.

## Catatan revisi 1.0.2 (2026-10-05)
- Format rupiah di hasil script ditulis "Rp1.000.000" (tanpa spasi setelah Rp).
- Balik modal terdiskonto dihitung dari arus kas operasional saja (nilai sisa atau jual kembali tidak dimasukkan); bila nilai sisa besar, hal ini disebut dalam satu kalimat. Agent tidak boleh menulis "balik modal lebih lama dari masa pakai" bila angkanya masih di dalam masa pakai.

## Catatan revisi 1.0.1 (2026-10-05)
- Pertanyaan kripto/trading/deposito/"pasti untung" kini tetap memakai skill dengan pola penolakan tetap + arahan ke hitungan usaha.
- `--nilai-sisa` dan `--nilai-residu` disatukan (hasil identik, omzet impas konsisten).
- Opsi `--jenis penghematan`/`pemasukan` untuk label hasil.
- NPV uji ketat 20% selalu ditampilkan.
- Rujukan bunga KUR disamakan (Permenko Perekonomian No. 1 Tahun 2026 Pasal 37 & 44).
- Disclaimer wajib di semua balasan.

## Catatan revisi 1.0.0 (2026-10-05)
- Rilis awal.

---
Sebagian rumus dan kasus uji diturunkan dari numpy-financial (BSD-3-Clause, © NumPy Developers) — lihat `ATTRIBUTION.md`. Komunitech tidak berafiliasi dengan NumPy. Hasil hitungan adalah simulasi dari angka yang Anda masukkan, bukan nasihat keuangan atau pajak dan bukan jaminan untung.
