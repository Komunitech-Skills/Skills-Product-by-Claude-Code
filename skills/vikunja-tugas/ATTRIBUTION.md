# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech** — penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang Vikunja
- Skill ini **memanggil REST API resmi** Vikunja milik pengguna (`/api/v1`, header `Authorization: Bearer tk_...`). Skill ini adalah program terpisah yang berkomunikasi lewat HTTP; **tidak** menyalin, memodifikasi, atau menyertakan kode Vikunja.
- **Vikunja** (https://github.com/go-vikunja/vikunja) berlisensi **AGPL-3.0-or-later** (file `LICENSE` di repo resminya). Vikunja **TIDAK didistribusikan** dalam paket ini; pembeli mengunduhnya sendiri dari sumber resmi (`https://dl.vikunja.io/vikunja/` atau image Docker resmi `vikunja/vikunja`) sesuai `docs/panduan-vikunja.md`.
- Nama-nama endpoint, format field, dan skema izin token API yang dipakai `scripts/vikunja.py` diverifikasi dengan membaca kode sumber resmi Vikunja 2.6.0 (routing, model token, model tugas) dan dengan **menjalankan langsung binary resmi** (checksum SHA-256 cocok) di sandbox Komunitech pada 2026-09-26 — lihat `research/sources/vikunja-2026-09-26.md` untuk metodologi lengkap. **Tidak ada baris kode Vikunja yang disalin** ke script ini.
- File `tests/fixtures/vikunja-2.6.0.json` berisi **contoh bentuk respons** API yang direkam dari Vikunja 2.6.0 yang dijalankan Komunitech dengan data fiktif (bentuk data/antarmuka, bukan kode program).
- "Vikunja" adalah merek milik pemiliknya (organisasi go-vikunja). Komunitech tidak berafiliasi dengan proyek Vikunja; nama dipakai hanya untuk menjelaskan kompatibilitas.
