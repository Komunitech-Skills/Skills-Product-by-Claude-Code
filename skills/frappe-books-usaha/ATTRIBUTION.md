# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol: instruksi `SKILL.md`, script
`scripts/frappe_books.py`, dokumentasi `references/`, contoh, dan uji. Lisensi: **Proprietary Komunitech** — penggunaan
tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang Frappe Books (perangkat lunak terpisah)
- **Frappe Books** adalah software akuntansi desktop karya **Frappe Technologies Pvt. Ltd. dan para kontributor**, berlisensi
  **GNU AGPL-3.0** (https://github.com/frappe/books, file `LICENSE`; situs: https://frappe.io/books).
- Frappe Books **TIDAK disertakan, disalin, dimodifikasi, atau didistribusikan** dalam paket ini. Pembeli mengunduh dan
  memasangnya sendiri dari sumber resmi (`references/panduan-pasang.md`).
- Skill ini adalah program terpisah yang **membaca** file data SQLite milik pengguna (read-only) dan **menulis file CSV** dalam
  format yang diterima fitur Import Wizard Frappe Books. Tidak ada kode Frappe Books di dalam skill ini.
- Kode sumber Frappe Books (tag `v0.36.0` dan cabang `main` per 20 Sep 2026) **dibaca** untuk memastikan nama tabel, kolom,
  dan format data (lihat `references/sumber-resmi.md`). Nama tabel/kolom dipakai sebatas antarmuka data agar kompatibel.
- File uji internal `tests/data/skema-frappe-books-v0.36.0.sql` berisi daftar tabel/kolom/tipe yang dibangkitkan Komunitech dari
  file skema resmi (data struktur, bukan kode program) dan hanya dipakai di repo pengembang; tidak ikut paket pembeli.
  Semua data contoh (usaha, pelanggan, angka) **fiktif**.
- "Frappe" dan "Frappe Books" adalah merek milik pemiliknya. **Komunitech tidak berafiliasi, tidak disponsori, dan tidak
  didukung** oleh Frappe Technologies maupun proyek Frappe Books; nama dipakai hanya untuk menjelaskan kompatibilitas.
