# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech**; penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang Actual Budget
- Skill ini **membaca (read-only)** file budget `db.sqlite` milik pengguna dengan pustaka standar `sqlite3` Python,
  dan **menulis file CSV** yang diimpor pengguna sendiri lewat fitur Import Actual. Skill ini adalah program terpisah;
  **tidak** menyalin, memodifikasi, atau menyertakan kode Actual Budget.
- **Actual Budget** (https://github.com/actualbudget/actual) berlisensi **MIT License**, "Copyright James Long"
  (file `LICENSE.txt` di repo). Actual **tidak didistribusikan** dalam paket ini; pembeli mengunduhnya sendiri dari
  https://actualbudget.org/download.
- Nama tabel/kolom database (`transactions`, `zero_budgets`, `category_mapping`, dst.), satuan sen, dan urutan rumus
  sisa anggaran adalah fakta format file untuk interoperabilitas. Semuanya diverifikasi dengan membaca kode sumber
  Actual 26.9.0 (rincian di `references/sumber-resmi.md`), lalu ditulis ulang dalam Python oleh Komunitech.
- Repo pengembang (folder `tests/`, tidak ikut paket pembeli) memuat budget uji yang dibuat dengan paket resmi
  `@actual-app/api` 26.9.0 berisi data fiktif, serta port kecil fungsi `looselyParseAmount` untuk keperluan uji.
  Bagian itu tunduk pada lisensi MIT Actual Budget:

  > Copyright James Long
  >
  > Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
  > documentation files (the "Software"), to deal in the Software without restriction, including without limitation
  > the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
  > to permit persons to whom the Software is furnished to do so, subject to the following conditions:
  >
  > The above copyright notice and this permission notice shall be included in all copies or substantial portions of
  > the Software.
  >
  > THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
  > THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  > AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
  > CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
  > IN THE SOFTWARE.
- Komunitech **tidak berafiliasi** dengan proyek Actual Budget atau para pengelolanya.
