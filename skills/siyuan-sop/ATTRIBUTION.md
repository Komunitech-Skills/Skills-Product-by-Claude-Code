# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech** - penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang SiYuan
- Skill ini **memanggil kernel API resmi** SiYuan milik pengguna sendiri (`http://127.0.0.1:6806/api/...`,
  header `Authorization: Token ...`). Skill ini adalah program terpisah yang berkomunikasi lewat
  HTTP; **tidak** menyalin, memodifikasi, atau menyertakan kode sumber SiYuan.
- **SiYuan** berlisensi **AGPL-3.0** (https://github.com/siyuan-note/siyuan, file `LICENSE`).
  SiYuan **TIDAK didistribusikan** dalam paket ini; pembeli mengunduhnya sendiri dari GitHub
  Releases resmi sesuai `docs/panduan-siyuan.md`.
- Nama endpoint & struktur field API (`docs/API.md` proyek SiYuan) dirujuk sebagai **fakta teknis**
  (nama endpoint, nama field) untuk memastikan skill memanggil API dengan benar - bukan salinan
  teks dokumentasi. Lihat `references/api-endpoints.md` untuk daftar & sumbernya (URL + tanggal
  verifikasi).
- Templat SOP/FAQ (`references/template-sop-faq.md`) dan seluruh panduan instalasi/keamanan
  (`docs/panduan-siyuan.md`) ditulis dari nol oleh Komunitech berdasarkan riset & pengujian
  langsung (`research/sources/siyuan-2026-09-26.md`), bukan salinan dokumentasi SiYuan.
- "SiYuan" dan "b3log" adalah nama/merek milik pemiliknya. **Komunitech tidak berafiliasi dengan
  proyek SiYuan atau b3log**; nama dipakai hanya untuk menjelaskan kompatibilitas.

## Uji integrasi
File `tests/fixtures/` (bila ada) berisi contoh **bentuk respons** API yang direkam dari kernel
SiYuan resmi v3.8.5 yang dijalankan Komunitech dengan data uji fiktif (bentuk data/antarmuka,
bukan kode program SiYuan).
