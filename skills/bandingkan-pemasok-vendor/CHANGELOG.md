# Riwayat perubahan — bandingkan-pemasok-vendor

Catatan teknis per versi (dipisah dari README agar halaman pembeli ringkas).

## 1.0.0 (2026-10-14)
- Rilis awal: biaya sampai di tempat (harga grosir bertingkat, MOQ/kelipatan/isi dus, minimal belanja, diskon, ongkir franco/loco/ekspedisi, PPN PKP vs non-PKP dengan pembulatan standar library, pembeli PKP), skor tertimbang 5 kriteria dengan bobot yang bisa diubah, sensitivitas (jumlah 2x, termurah telat + hari impas, bagi pesanan 70/30), daftar `[isian]`, template pesan WA klarifikasi/negosiasi.
- Script `scripts/banding_pemasok.py` (Decimal, Python standar) + `tests/uji_regresi.py` (47 uji).
