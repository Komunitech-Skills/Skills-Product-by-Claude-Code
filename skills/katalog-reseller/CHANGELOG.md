# Riwayat perubahan — katalog-reseller

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.4 (2026-10-01)
- Uji OpenClaw 2026-10-01: file CSV daftar harga mitra sempat tersimpan di folder `scripts/` skill tanpa lokasi disebut. Kini CSV ditulis ke folder kerja pengguna (path lengkap di `--csv-keluar`), script mencetak path absolut, dan agent wajib menyebut lokasi file di balasan (script `hitung_tier.py` 1.0.1).
