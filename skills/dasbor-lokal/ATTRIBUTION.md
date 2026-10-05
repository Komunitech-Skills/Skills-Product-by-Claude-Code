# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech** — penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang Datasette
- Skill ini menyiapkan **perintah** untuk menjalankan **Datasette** (dibuat oleh Simon Willison, https://datasette.io/, kode: https://github.com/simonw/datasette) dan menyiapkan file `metadata.yml` (canned queries) untuknya. Skill ini **tidak menyalin, memodifikasi, atau menyertakan** kode Datasette dengan cara apa pun.
- Datasette berlisensi **Apache-2.0** (lihat `LICENSE` di repo resminya). Datasette **TIDAK didistribusikan** dalam paket ini; pengguna memasangnya sendiri dari **PyPI resmi** (`pip`/`pipx install datasette`) sesuai `docs/panduan-datasette.md`.
- Bila Datasette tidak terpasang, skill ini tetap berfungsi penuh lewat `scripts/dasbor.py`, yang hanya memakai library standar Python (`sqlite3`) dan tidak bergantung pada Datasette sama sekali.
- "Datasette" adalah nama proyek/merek milik pembuatnya. **Komunitech tidak berafiliasi** dengan proyek Datasette atau Simon Willison; nama dipakai hanya untuk menjelaskan kompatibilitas.

## Tentang alat lokal Komunitech yang dibaca
`scripts/dasbor.py` membaca (baca-saja) database SQLite milik skill Komunitech lain yang sudah dipasang pengguna sendiri: `buku-stok`, `kasir-lokal`, `crm-wa`, `absensi-lokal`, `buku-piutang`, `kas-umkm`. Skill-skill itu adalah karya Komunitech yang terpisah; `dasbor-lokal` tidak mengubah data atau perilakunya.
