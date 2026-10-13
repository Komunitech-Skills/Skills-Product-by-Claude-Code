# Atribusi

**pdf-lokal** adalah skill **orisinal Komunitech** (komunitech.com), ditulis dari nol
(instruksi `SKILL.md`, script `scripts/pdf.py`, dokumentasi). Lisensi skill ini:
**Proprietary Komunitech** - tunduk pada `LISENSI.txt` yang disertakan dalam paket
pembelian.

## Ketergantungan pihak ketiga: Stirling-PDF

Skill ini **memanggil** REST API lokal aplikasi **Stirling-PDF**
(https://github.com/Stirling-Tools/Stirling-PDF), yang **HARUS dipasang sendiri oleh
pengguna** di komputernya (lihat `references/pasang-stirling.md`). Stirling-PDF:

- **TIDAK didistribusikan/disalin di dalam paket skill ini.** Skill ini hanya berisi
  kode yang mengirim permintaan HTTP ke `http://localhost:8080` (alamat default
  Stirling-PDF di komputer pengguna sendiri) - tidak ada baris kode, aset, atau
  binari Stirling-PDF yang disalin ke dalam paket ini.
- Inti (core) Stirling-PDF berlisensi **MIT** - bebas dipakai, termasuk untuk
  memanggil API-nya dari alat lain seperti skill ini.
- Ada folder terpisah `app/proprietary/` di kode sumber Stirling-PDF (fitur tim/SSO/
  audit/tanda tangan sertifikat bersertifikat, dll.) yang **BUKAN** MIT dan
  **butuh lisensi berbayar terpisah dari Stirling-Tools**, di luar kendali Komunitech.
  **Skill ini hanya memanggil endpoint inti/gratis** (`/api/v1/general/...`,
  `/api/v1/misc/...`, `/api/v1/security/add-password` dkk., `/api/v1/convert/...`) -
  **tidak ada satu pun endpoint `/api/v1/proprietary/...`, `/api/v1/admin/...`, atau
  `/api/v1/team/...` yang dipanggil**. Lihat `references/sumber-api-stirling.md`
  untuk daftar lengkap endpoint yang dipakai vs yang sengaja dihindari.
- Nama "Stirling-PDF" dan "Stirling-Tools" adalah milik pembuat aslinya. Komunitech
  tidak berafiliasi dengan proyek Stirling-PDF; skill ini murni alat bantu pemanggil
  API pihak ketiga.

Bila Stirling-PDF mengganti lisensi intinya di kemudian hari (sudah pernah terjadi
pada beberapa proyek open-core lain), skill ini perlu ditinjau ulang - lihat
catatan riset internal kurator (tidak disertakan dalam paket) poin risiko lisensi.

## Alat lokal jalur cadangan (v1.0.5)

`scripts/pdf_cadangan.py` hanya **memanggil** program yang sudah terpasang di komputer
pengguna bila ada: qpdf (Apache-2.0), Ghostscript (AGPL-3.0 / lisensi komersial Artifex),
dan pdftk (GPL). Tidak ada kode, binari, atau aset dari program tersebut yang disalin ke
paket ini; memanggil program terpisah lewat baris perintah tidak menjadikan skill ini
karya turunannya. Komunitech tidak berafiliasi dengan proyek-proyek tersebut.
