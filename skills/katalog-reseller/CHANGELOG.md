# Riwayat perubahan — katalog-reseller

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-13)
- Pemindaian contoh uji: contoh S&K dan pesan rekrut memuat syarat kirim/retur, batas hari, dan layanan pendukung yang tidak diberikan pengguna (jam potong kirim, retur 3 hari, "foto & materi promosi disediakan").
- Aturan baru di langkah S&K: jangan mengarang atribut produk/layanan, syarat kirim/retur, angka, atau klaim yang tidak diberikan pengguna; tulis `[isian: ...]` atau tandai sebagai asumsi. Contoh `examples/01` diperbaiki. Logika hitung tidak berubah.

## Catatan revisi 1.0.4 (2026-10-01)
- Uji OpenClaw 2026-10-01: file CSV daftar harga mitra sempat tersimpan di folder `scripts/` skill tanpa lokasi disebut. Kini CSV ditulis ke folder kerja pengguna (path lengkap di `--csv-keluar`), script mencetak path absolut, dan agent wajib menyebut lokasi file di balasan (script `hitung_tier.py` 1.0.1).
