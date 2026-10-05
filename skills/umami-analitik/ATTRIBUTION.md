# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech** — penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang Umami
- Skill ini **memanggil REST API resmi** Umami milik pengguna (`/api/...`, header `Authorization: Bearer <kunci API>`). Skill ini adalah program terpisah yang berkomunikasi lewat HTTP; **tidak** menyalin, memodifikasi, atau menyertakan kode Umami.
- **Umami** (https://github.com/umami-software/umami, situs https://umami.is) berlisensi **MIT** — "Copyright (c) 2022 Umami Software, Inc." (file `LICENSE` di repo resminya). Umami **TIDAK didistribusikan** dalam paket ini; pembeli memasangnya sendiri dari sumber resmi (image Docker resmi `ghcr.io/umami-software/umami` atau kode rilis GitHub) sesuai `docs/panduan-umami.md`.
- Nama endpoint, parameter, dan rumus angka (bounce, rata-rata lama, kanal) yang dipakai `scripts/umami.py` diverifikasi dengan membaca kode sumber resmi Umami **3.4.0** (tag `v3.4.0`, commit `ec0ff50`) dan dengan **menjalankan Umami 3.4.0 sungguhan** di sandbox Komunitech pada 2026-09-29 — lihat `examples/uji-pembuat/`. **Tidak ada baris kode Umami yang disalin** ke script ini. Contoh `docker-compose.yml` di panduan adalah file konfigurasi resmi Umami (MIT) dengan perubahan pengamanan yang ditandai.
- File `tests/fixtures/umami-3.4.0.json` berisi **rekaman bentuk respons** API dari Umami 3.4.0 yang dijalankan Komunitech dengan data fiktif (bentuk data/antarmuka, bukan kode program). Tidak berisi kunci/token (disensor).
- "Umami" adalah nama/merek milik Umami Software, Inc. **Komunitech tidak berafiliasi** dengan Umami Software, Inc.; nama dipakai hanya untuk menjelaskan kompatibilitas (keputusan pemilik 2026-09-26: merek pihak ketiga boleh sebagai penyebut produk dengan keterangan tidak berafiliasi).
