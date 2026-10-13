# Riwayat perubahan — crm-wa

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.9 (2026-10-02)
- Temuan uji gabungan paket Toko Online: permintaan "daftar pelanggan buat promo" tidak memicu skill ini, dan rujukan ke `broadcast-wa` (tidak ada di paket Toko Online) membingungkan.
- Pemicu baru: "daftar pelanggan buat promo", "data pelanggan", "kontak pembeli". Aturan 10: promo hanya ke kontak berlabel `setuju-promo`; pembeli marketplace default belum setuju; tanpa broadcast (termasuk WhatsApp Business) ke kontak yang belum setuju.
