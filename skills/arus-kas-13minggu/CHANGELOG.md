# Riwayat perubahan — arus-kas-13minggu

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.4 (2026-10-13)
- Batasan di SKILL.md ditambah satu aturan: setiap tarif/aturan disebut dengan dasar aturan + tahun; angka hanya dari script/input pengguna; nilai yang tidak diberikan pengguna ditandai asumsi (tanpa label "wajar/umum/lazim" yang tidak bersumber).
- Contoh uji `examples/02`: THR diberi dasar Permenaker 6/2016 (masa kerja ≥ 12 bulan = 1 bulan upah; < 12 bulan proporsional); tanggal Lebaran tidak lagi ditebak, pengguna mengisi tanggal Idulfitri menurut kalender resmi. Saldo minggu 10 dengan THR (Rp 90.500.000) dicek ulang dengan script.

## Catatan revisi 1.0.3 (2026-10-01)
Perbaikan dari uji OpenClaw asli (arus kas 13 minggu, info kurang lalu dilengkapi):
- Script kini mencetak **kejadian per minggu** (pos masuk/keluar apa saja yang jatuh di tiap minggu) dan rincian minggu kritis. AI wajib mengutip nomor minggu dan pos dari daftar ini, sehingga tidak ada lagi salah sebut "cicilan di minggu 12" padahal di minggu 11.
- Pos yang ditanyakan tetapi belum dijawab (mis. BPJS, PPh 21) ditulis jelas sebagai "Belum termasuk" di Asumsi.
- Path script ditulis jelas (subfolder `scripts/`); AI dilarang mencari file ke seluruh disk.
