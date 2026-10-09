# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol. Lisensi skill & panduan: **Proprietary Komunitech**; penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang Fider
- Skill ini **memanggil REST API resmi** Fider milik pengguna (`/api/v1/...`, header `Authorization: Bearer <kunci API>`). Skill adalah program terpisah yang berkomunikasi lewat HTTP; **tidak** menyalin, memodifikasi, atau menyertakan kode maupun teks dokumentasi Fider. Panduan `docs/panduan-fider.md` dan berkas `docker-compose.yml` di dalamnya ditulis sendiri oleh Komunitech.
- **Fider** (https://github.com/getfider/fider, situs https://fider.io) berlisensi **GNU AGPL-3.0**. Fider **TIDAK didistribusikan** dalam paket ini; pembeli memasangnya sendiri dari sumber resmi (image Docker `getfider/fider`) sesuai panduan. Karena Fider tidak disertakan dan tidak diubah, kewajiban AGPL atas kode Fider tetap pada Fider dan pemakainya. Pembeli yang mengubah kode Fider dan menyajikannya ke publik wajib memenuhi AGPL (menyediakan kode sumber ubahannya).
- Nama endpoint, parameter, dan perilaku (mis. status yang sah, batas judul 100 karakter, filter status pada daftar pos) diverifikasi dengan membaca dokumentasi resmi (https://docs.fider.io/api) dan **menjalankan Fider v0.38.0 sungguhan** (Docker + PostgreSQL 17) pada 2026-09-29. Tidak ada baris kode Fider yang disalin ke script.
- "Fider" adalah nama/merek milik pengembangnya. **Komunitech tidak berafiliasi** dengan Fider/getfider; nama dipakai hanya untuk menjelaskan kompatibilitas (keputusan pemilik 2026-09-26).
