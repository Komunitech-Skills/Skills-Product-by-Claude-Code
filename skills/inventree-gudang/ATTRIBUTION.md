# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech** — penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang InvenTree
- Skill ini **memanggil REST API resmi** InvenTree milik pengguna (`/api/`, header `Authorization: Token inv-...`). Skill ini adalah program terpisah yang berkomunikasi lewat HTTP; **tidak** menyalin, memodifikasi, atau menyertakan kode InvenTree.
- **InvenTree** (https://github.com/inventree/InvenTree, dokumentasi https://docs.inventree.org) berlisensi **MIT** — "Copyright (c) 2017 - InvenTree Developers" (file `LICENSE` di repo resminya). InvenTree **TIDAK didistribusikan** dalam paket ini; pembeli memasangnya sendiri dari sumber resmi (image Docker resmi `inventree/inventree` atau kode rilis GitHub) sesuai `docs/panduan-inventree.md`.
- Nama endpoint, filter, dan format data yang dipakai `scripts/inventree.py` diverifikasi dengan membaca kode sumber resmi InvenTree **1.5.6** (tag `1.5.6`, commit `284a670`) dan dengan **menjalankan InvenTree 1.5.6 sungguhan** di sandbox Komunitech pada 2026-09-29 — lihat catatan riset internal kurator (tidak disertakan dalam paket). **Tidak ada baris kode InvenTree yang disalin** ke script ini.
- File `tests/fixtures/inventree-1.5.6.json` berisi **rekaman bentuk respons** API dari InvenTree 1.5.6 yang dijalankan Komunitech dengan data fiktif (bentuk data/antarmuka, bukan kode program). Tidak berisi token.
- "InvenTree" adalah nama/merek milik pengembangnya. **Komunitech tidak berafiliasi** dengan proyek InvenTree; nama dipakai hanya untuk menjelaskan kompatibilitas (keputusan pemilik 2026-09-26: merek pihak ketiga boleh sebagai penyebut produk dengan keterangan tidak berafiliasi).
