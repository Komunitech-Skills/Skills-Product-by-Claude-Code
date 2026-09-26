# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech** — penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang Grist
- Skill ini **memanggil REST API resmi** Grist milik pengguna (`/api/docs/...`, header
  `Authorization: Bearer <kunci>`) dan **membaca (read-only)** file `.grist` (SQLite) milik
  pengguna dengan pustaka standar `sqlite3` Python. Skill ini adalah program terpisah yang
  berkomunikasi lewat HTTP/membaca file — **tidak** menyalin, memodifikasi, atau menyertakan
  kode Grist.
- **Grist** (`grist-core` dan `Grist Desktop`) dibuat oleh **Grist Labs Inc.** dan berlisensi
  **Apache License 2.0** (https://github.com/gristlabs/grist-core,
  https://github.com/gristlabs/grist-desktop, file `LICENSE.txt` masing-masing repo). Salinan
  teks lisensi Apache-2.0 dan `NOTICE.txt` resmi (`grist-core`) dilampirkan di folder ini
  (`LICENSE-grist-apache-2.0.txt`, `NOTICE-grist.txt`) sebagai referensi, sesuai semangat
  keterbukaan Apache-2.0 — meski tidak wajib karena kami tidak mendistribusikan/memodifikasi
  kode Grist itu sendiri.
- **Grist TIDAK didistribusikan** dalam paket ini; pembeli mengunduhnya sendiri dari sumber
  resmi (github.com/gristlabs/grist-desktop/releases untuk aplikasi Desktop, atau
  `docker pull gristlabs/grist` / Docker Hub resmi untuk `grist-core`) sesuai
  `docs/panduan-grist.md`.
- Struktur file `.grist` (nama tabel metadata `_grist_Tables`/`_grist_Tables_column`, dan aturan
  "tabel data pengguna = tabel SQLite biasa bernama tableId, kolom `id INTEGER PRIMARY KEY`")
  dikonfirmasi dengan membaca langsung kode sumber resmi `grist-core` v1.7.19
  (`sandbox/grist/schema.py`, `app/server/lib/DocStorage.ts`) — nama tabel/kolom adalah fakta
  format file untuk keperluan interoperabilitas, bukan kode yang disalin. Rincian lengkap &
  metodologi verifikasi ada di `research/sources/grist-2026-09-26.md`.
- File `tests/fixtures/buat_fixture.py` membuat file `.grist` **TIRUAN** untuk keperluan uji
  (bukan hasil ekspor Grist sungguhan) — lihat catatan kejujuran di dalam file itu dan di
  `examples/HASIL-UJI.md`.
- "Grist" adalah merek milik pemiliknya. **Komunitech tidak berafiliasi** dengan Grist Labs Inc.
  atau proyek Grist; nama dipakai hanya untuk menjelaskan kompatibilitas.
