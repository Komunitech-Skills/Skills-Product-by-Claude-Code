# Riwayat perubahan — analisis-rasio-keuangan-usaha

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: jenis/skala usaha untuk ambang tidak dilabeli asumsi.
- Kini wajib ditulis "Asumsi: jenis usaha …, skala …".

## Catatan revisi 1.0.4 (2026-10-01)
Perbaikan dari uji OpenClaw asli (bahan rapat komisaris):
- Utang bank yang jatuh tempo ≤ 12 bulan kini dicatat terpisah dan **dibandingkan langsung dengan kas**. Bila utangnya lebih besar dari kas, hasil menyebut risiko likuiditas (mis. "SEDANG") beserta alasannya, rasio kas tidak lagi hijau, dan saran pertama adalah mengurus jadwal/perpanjangan pinjaman.
- Kesimpulan likuiditas selalu bertingkat (rendah / rendah–sedang / sedang / tinggi). Tidak ada lagi kalimat "tidak ada risiko gagal bayar".
- Skala usaha (mikro/kecil/menengah/besar) dihitung dari penjualan setahun; usaha menengah ke atas memakai ambang kas & cakupan bunga yang lebih ketat.
- Jenis usaha yang dipilih AI sendiri wajib ditulis sebagai asumsi. Path script ditulis jelas; AI dilarang mencari ke seluruh disk.
