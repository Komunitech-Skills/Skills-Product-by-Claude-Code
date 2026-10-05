# morluto/rea — Reverse Engineer Anything

- URL: https://github.com/morluto/rea
- Pembuat: morluto (+ kolaborator N0zoM1z0, rudycelekli, kaoru0822-kitauji)
- Lisensi: MIT (file LICENSE, "Copyright (c) 2026 morluto")
- Dicek: 2026-10-05. Bintang ±5k, fork 515, 923 commit, rilis 0.2.0 (2026-07-12) → 3.2.1 (2026-10-03). Umur ±3 bulan, 318 PR (banyak dari non-owner), 55 issue terbuka, ada CI, SECURITY.md, CONTRIBUTING.md.
- Isi: CLI + MCP server (TypeScript/Node 22+) untuk reverse engineering binary (Hopper/Ghidra), Electron/ASAR, .NET, APK/IPA, observasi browser (CDP/Playwright). Ada `skills/reverse-engineer-anything/SKILL.md` + `references/` yang sepenuhnya bergantung pada MCP server REA.
- Audit keamanan (install.sh dibaca penuh): hanya `npm install --global rea-agents@<versi>` + `rea setup` (menulis konfigurasi MCP dengan backup, opsional instal Hopper). Tidak ada exfiltrasi/kredensial. Pola `curl | bash` standar.

## Keputusan: TIDAK DIKURASI (hanya inspirasi)
1. Domain reverse engineering binary bukan kebutuhan UMKM/profesional awam.
2. SKILL.md tidak berdiri sendiri: butuh MCP server, Hopper/Ghidra, Node 22, macOS/Linux — melanggar prinsip "tanpa setup".
3. Proyek sangat muda, churn tinggi (breaking change 5 Okt 2026).
4. Risiko etika/HAKI bila dipromosikan sebagai cara meniru fitur aplikasi lain.

Yang layak ditiru (struktur, bukan isi): routing berdasarkan jenis target, prinsip pisahkan observasi/inferensi/tidak diketahui, `references/` dibaca hanya bila relevan, minta persetujuan sebelum setup menulis konfigurasi.
