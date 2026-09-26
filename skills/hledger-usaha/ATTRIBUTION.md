# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol: instruksi `SKILL.md`, script `scripts/hledger_usaha.py`, template jurnal & aturan bank, dokumentasi, dan panduan `docs/panduan-hledger.md`.
Lisensi: **Proprietary Komunitech** — penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang hledger (perangkat lunak terpisah)
- **hledger** adalah program akuntansi teks karya **Simon Michael dan para kontributor**, berlisensi **GPL-3.0-or-later** (https://hledger.org, kode sumber: https://github.com/hledgerorg/hledger).
- hledger **TIDAK disertakan, disalin, atau dimodifikasi** dalam paket ini. Pembeli mengunduhnya sendiri dari sumber resmi mengikuti `docs/panduan-hledger.md`.
- Skill ini adalah program terpisah yang **menjalankan** hledger sebagai program luar (perintah baris `hledger print -O json`, `hledger check`) bila terpasang, dan menulis file jurnal serta file aturan CSV dalam **format data** yang dibaca hledger. Tidak ada kode hledger di dalam skill ini.
- Template `templates/jurnal-awal.journal` dan `templates/aturan-bank.rules` ditulis Komunitech (bagan akun & kata kunci berbahasa Indonesia), mengikuti format yang didokumentasikan di hledger.org.
- "hledger" adalah nama milik pembuatnya. **Komunitech tidak berafiliasi** dengan proyek hledger maupun Simon Michael; nama dipakai hanya untuk menjelaskan kompatibilitas.
- Versi yang diuji: hledger 1.52.4 (lihat `references/sumber-resmi.md`).
