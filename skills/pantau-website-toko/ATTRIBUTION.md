# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol.
Lisensi: **Proprietary Komunitech** — penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian.

## Tentang Uptime Kuma
- Skill ini **membaca endpoint status page publik resmi** Uptime Kuma milik pengguna
  (`GET /api/status-page/<slug>` dan `GET /api/status-page/heartbeat/<slug>`) lewat HTTP biasa.
  Skill ini adalah program terpisah yang berkomunikasi lewat HTTP; **tidak** menyalin,
  memodifikasi, atau menyertakan kode Uptime Kuma dengan cara apa pun. Endpoint ini memang
  dirancang untuk dibaca publik tanpa token/API key (dikonfirmasi dari kode sumber resminya).
- **Uptime Kuma** (https://github.com/louislam/uptime-kuma) berlisensi **MIT** (file `LICENSE` di
  repo resminya, Copyright (c) 2021 Louis Lam). Uptime Kuma **TIDAK didistribusikan** dalam paket
  ini; pembeli memasangnya sendiri dari sumber resmi (GitHub Releases, `npm run setup`, atau image
  Docker resmi `louislam/uptime-kuma`) sesuai `docs/panduan-uptime-kuma.md`.
- Nama field JSON, endpoint, dan konstanta status (UP/DOWN/PENDING/MAINTENANCE) yang dipakai
  `scripts/pantau.py` diverifikasi dengan membaca kode sumber resmi Uptime Kuma 2.5.5 (routing,
  model status page, model monitor/heartbeat) dan dengan **menjalankan langsung rilis resmi**
  (dipasang lewat `npm run setup` bawaan proyek, mengunduh `dist.tar.gz` dari GitHub Releases
  resmi) di sandbox Komunitech pada 2026-09-26 — lihat
  catatan riset internal kurator (tidak disertakan dalam paket) untuk metodologi lengkap. **Tidak ada baris kode
  Uptime Kuma yang disalin** ke script ini.
- File `tests/fixtures/uptime-kuma-2.5.5-status-page.json` dan `-heartbeat.json` berisi **contoh
  bentuk respons** API yang direkam apa adanya dari instance Uptime Kuma 2.5.5 sungguhan yang
  dijalankan Komunitech dengan data uji fiktif (bentuk data/antarmuka, bukan kode program).
  `tests/fixtures/skenario2-*.json` dan `skenario3-*.json` adalah data buatan tangan Komunitech (ditandai jelas di
  dalam filenya) untuk menguji jalur kode yang tidak muncul di rekaman aslinya.
- "Uptime Kuma" adalah nama proyek/merek milik pembuatnya (Louis Lam). **Komunitech tidak
  berafiliasi** dengan proyek Uptime Kuma; nama dipakai hanya untuk menjelaskan kompatibilitas.

## Mode tanpa Uptime Kuma (`cek-cepat`)
Perintah `cek-cepat` tidak menghubungi/membaca perangkat lunak pihak ketiga apa pun — hanya
mengirim satu permintaan HTTP standar dan memeriksa sertifikat TLS langsung ke alamat yang
diberikan pengguna sendiri, memakai library standar Python (`urllib`, `ssl`, `socket`).
