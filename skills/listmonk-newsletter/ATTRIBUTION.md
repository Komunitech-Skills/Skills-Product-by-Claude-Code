# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech** - penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang listmonk
- Skill ini **memanggil REST API** listmonk milik pengguna (`/api/...`, header `Authorization: token <pengguna>:<token>`). Skill adalah program terpisah yang berkomunikasi lewat HTTP; **tidak** menyalin, memodifikasi, menautkan (linking), atau menyertakan kode maupun teks dokumentasi listmonk.
- **listmonk** (https://github.com/knadh/listmonk, situs https://listmonk.app) berlisensi **AGPL-3.0** (Kailash Nadh dan kontributor). listmonk **TIDAK didistribusikan** dalam paket ini; pembeli memasangnya sendiri dari sumber resmi (image Docker resmi `listmonk/listmonk` atau rilis GitHub) mengikuti `docs/panduan-listmonk.md`. Sumber kode listmonk tersedia di repositori resminya.
- Perilaku endpoint yang dipakai (impor, opt-in, uji kirim, status kampanye, analitik) diverifikasi dari dokumentasi/Swagger resmi dan dengan **menjalankan listmonk 6.2.0 sungguhan** di sandbox Komunitech pada 2026-09-29 (`examples/uji-pembuat/`). `docker-compose.yml` di panduan adalah **tulisan sendiri** (bukan salinan file resmi).
- Tidak ada kode listmonk yang disalin; bila pembeli mengubah kode listmonk dan menyediakannya bagi orang lain lewat jaringan, kewajiban AGPL-3.0 berlaku bagi pembeli.
- "listmonk" adalah nama proyek milik pengembangnya. **Komunitech tidak berafiliasi** dengan proyek listmonk maupun Kailash Nadh; nama dipakai hanya untuk menjelaskan kompatibilitas. Mailchimp adalah merek pihak ketiga yang disebut sebagai pembanding; Komunitech tidak berafiliasi dengannya.
- Nama/harga Brevo dan Amazon SES di panduan hanyalah contoh penyedia SMTP; tidak berafiliasi, harga dapat berubah.
