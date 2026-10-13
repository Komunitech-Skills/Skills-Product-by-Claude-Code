# Riwayat perubahan — cek-privasi-openclaw

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.1.4 (2026-10-01)
- Uji OpenClaw 2026-10-01: agent sempat menjalankan `chmod` sebelum menampilkan daftar perbaikan. Kini semua perubahan (config, `chmod`/izin file, `--fix`) hanya dijalankan setelah daftar lengkap ditampilkan dan pemilik menjawab "ya"; "gak usah nanya" sebelum melihat daftar bukan persetujuan.
- Permintaan menyadap/memata-matai chat orang lain: penolakan kini wajib ditulis lengkap & sopan di balasan itu sendiri (alasan UU ITE Pasal 31 & UU PDP + alternatif sah), bukan hanya "tetap saya tolak".
