# Riwayat perubahan — rapor-mingguan-ai

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.1 (2026-10-06)
- Revisi dari uji OpenClaw (skor 4,75 naik ke 8,25): urutan tetap pada "3 kesalahan teratas" dan PR minggu ini: kriteria kritis (salah fakta, janji yang tidak bisa ditepati, bocor data pribadi) selalu didahulukan dan masing-masing jadi butir terpisah; nada atau panjang hanya mengisi sisa kuota. PR wajib menutup kesalahan kritis dulu.
- Privasi: nama, inisial, dan potongan nomor pelanggan (termasuk 4 digit terakhir) tidak ditulis di rapor, diganti "pelanggan A/B". PR berisi fakta usaha hanya dari info yang diberikan pengguna (selain itu `[isian]`); nama berkas internal tidak disebut ke pengguna.

## Catatan revisi 1.0.0 (2026-10-06)
- Rilis awal (status uji).
