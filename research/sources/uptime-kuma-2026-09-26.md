# Riset sumber — Uptime Kuma (louislam/uptime-kuma)

**Tanggal riset:** 2026-09-26
**Peneliti:** sesi Komunitech Skills Factory (agent) — diverifikasi langsung terhadap kode sumber resmi dan terhadap **rilis resmi yang benar-benar dijalankan** (lihat §3).
**Konteks:** lanjutan `research/sources/instagram-repo-2026-09-26.md` (#4 uptime-kuma → "produk jalur 2"). Tugas K9: `docs/panduan-uptime-kuma.md` + `skills/pantau-website-toko/`.

## 1. Identitas & sumber resmi

| Item | Nilai |
|---|---|
| Nama produk | **Uptime Kuma** — "A fancy self-hosted monitoring tool" (pemantau uptime website/server, pengganti UptimeRobot/Pingdom/StatusCake berbayar) |
| Pembuat / pemelihara | Louis Lam (`louislam`), proyek individu tapi sangat mapan; organisasi komunitas besar di sekitarnya (Discord, forum) |
| Repo | https://github.com/louislam/uptime-kuma |
| Situs/dokumentasi | https://uptime.kuma.pet , wiki resmi di GitHub |
| Lisensi | **MIT** (dikonfirmasi dari file `LICENSE` di root repo: "MIT License, Copyright (c) 2021 Louis Lam") |
| Bintang GitHub | **±91.800★** / ±8.500 fork (jauh di atas ambang 100★ repo satu produk) |
| Versi stabil terbaru saat riset | **2.5.5** (tag git `2.5.5`). Cabang `master` sudah bergerak ke `3.0.0-beta.0` (dev/beta, butuh Node ≥26 yang belum lazim dipakai pembeli) — **skill & panduan ini memakai 2.5.5 (stabil)**, bukan beta. |
| Umur & perawatan | Rilis sejak 2021, riwayat tag rilis bertahap (2.3.x → 2.4.0 → 2.5.0…2.5.5), commit aktif s/d tanggal riset — bukan pola AI slop. |

## 2. Sinyal bukti pemakaian nyata (CLAUDE.md Tahap 2 — wajib ≥3)

1. **Popularitas**: ±91.800★ GitHub, jauh di atas ambang; image Docker resmi `louislam/uptime-kuma` dengan jutaan pull.
2. **Umur & perawatan**: proyek sejak 2021, rilis bertahap satu-satu dengan jarak wajar antar versi (bukan puluhan rilis dalam hitungan hari), dan development branch beta yang terpisah rapi dari cabang stabil.
3. **Dipakai komunitas**: ribuan fork, ratusan kontributor, dipakai luas sebagai basis banyak tutorial self-hosting (Homelab/Proxmox/Docker) dan disebut sebagai alternatif open-source utama untuk UptimeRobot/Pingdom.
4. **Kualitas isi**: kode sumber terstruktur (Node.js/Express/Vue, Socket.IO), ada `server/notification-providers/` untuk >90 kanal notifikasi bawaan (termasuk Telegram resmi, tanpa API pihak ketiga tambahan), status page publik built-in, dukungan Prometheus metrics.

**Kesimpulan:** lolos jauh di atas ambang minimum 3 sinyal → **boleh dikurasi**, bukan AI slop (sejalan kesimpulan `instagram-repo-2026-09-26.md` #4).

## 3. Cara verifikasi (kejujuran metodologi)

Uptime Kuma **berhasil diunduh, dipasang, dan DIJALANKAN sungguhan** (bukan simulasi) di sandbox Komunitech:

1. Repo di-*clone* (di luar folder `Skills/`, tidak pernah masuk git Komunitech) untuk membaca kode sumber resmi: routing status page (`server/routers/status-page-router.js`), model (`server/model/status_page.js`, `server/model/group.js`, `server/model/monitor.js`, `server/model/heartbeat.js`), konstanta status (`src/util.ts`), dan notifier Telegram bawaan (`server/notification-providers/telegram.js`). **Tidak ada kode yang disalin** ke skill; hanya dipakai memastikan nama field/endpoint benar.
2. Sempat mencoba cabang `master` (3.0.0-beta.0) tapi ditemukan butuh Node ≥26 (`engines` di `package.json`) — **diganti ke tag rilis stabil `2.5.5`** (`engines: node >= 20.4.0`, cocok dengan Node 22 di sandbox).
3. Dipasang lewat jalur resmi proyek sendiri: `npm install` (dependensi dari registry npm resmi) lalu `npm run download-dist` (skrip resmi `extra/download-dist.js` milik proyek, mengunduh `dist.tar.gz` **dari halaman GitHub Releases resmi** `github.com/louislam/uptime-kuma/releases/download/2.5.5/dist.tar.gz` — bukan `curl | bash` dari sumber tak dikenal).
4. Server **dijalankan sungguhan**, diikat ke `127.0.0.1` saja (`UPTIME_KUMA_HOST=127.0.0.1`). Terhadap instance hidup ini kami:
   - Membuat akun admin & login (lewat Socket.IO, protokol asli aplikasi ini — Uptime Kuma tidak punya endpoint setup lewat REST biasa).
   - Menambah 2 monitor HTTP, membuat status page, mempublikasikannya dengan monitor dikelompokkan.
   - Mengambil **langsung** `GET /api/status-page/<slug>` dan `GET /api/status-page/heartbeat/<slug>` — endpoint publik resmi yang memang dirancang untuk dibaca tanpa token/API key (dipakai status page publiknya sendiri). Struktur JSON yang didapat (field `config`, `publicGroupList[].monitorList[]`, `heartbeatList`, `uptimeList["<id>_24"]`) **cocok persis** dengan yang dibaca dari kode sumber, dan dipakai sebagai fixture uji (`skills/pantau-website-toko/tests/fixtures/uptime-kuma-2.5.5-*.json` — data mentah nyata, direkam apa adanya).
   - Menguji kasus gagal: slug salah → `404` `{"status":"fail","msg":"Status Page Not Found"}` (dicatat apa adanya di script & pesan galat skill).
   - Membaca kode `server/server.js` & `server/prometheus.js`: endpoint `/metrics` (Prometheus) **ada**, tapi dilindungi `apiAuth` (butuh username+password akun Uptime Kuma, bukan token terpisah) dan mencakup SEMUA monitor (bukan hanya yang dipublikasikan) — **tidak dipakai** sebagai jalur utama script kami karena butuh kredensial akun penuh (bertentangan prinsip "tanpa API key/tanpa setup" untuk pembeli awam); disebutkan di panduan sebagai opsi lanjutan opsional untuk pembeli yang paham.
5. **Belum/tidak diuji** di sandbox ini: instalasi Windows/macOS sungguhan (tidak ada mesin itu di sandbox), Docker (daemon Docker diblokir kebijakan sandbox — instalasi via Docker Compose mengikuti `docker-compose.yml` resmi di repo, dicatat sebagai ⚠️ belum diuji langsung), pengiriman notifikasi Telegram sungguhan (butuh token bot & chat id asli milik pembeli).

**Repo `louislam/uptime-kuma` yang di-*clone*/dipasang untuk riset ini ada di luar folder `Skills/` dan tidak pernah ditambahkan ke git repo Komunitech.**

## 4. Keamanan (Tahap 3 CLAUDE.md)

- **Alamat dengar default**: bawaan mendengarkan di semua antarmuka (`0.0.0.0`) kecuali diikat manual; panduan kami **mewajibkan** `UPTIME_KUMA_HOST=127.0.0.1` (dikonfirmasi bekerja: log menunjukkan `Listening on: http://127.0.0.1:<port>`) untuk instalasi yang hanya dipantau dari komputer/jaringan sendiri.
- **Status page publik**: memang **dirancang untuk publik** (itu fitur utamanya) — `/api/status-page/<slug>` sengaja tidak butuh token. Ini BUKAN celah: hanya menampilkan status naik/turun & ping monitor yang dipilih admin untuk grup publik (pesan detail `msg` disembunyikan di endpoint publik, dikonfirmasi dari `heartbeat.js toPublicJSON()`).
- **Panel admin** (menambah/mengubah monitor) tetap wajib login akun+sandi; skill `pantau-website-toko` **tidak pernah** login/menulis ke Uptime Kuma — hanya membaca endpoint status page publik atau melakukan HTTP GET biasa ke situs pengguna sendiri.
- **Notifikasi Telegram** dikonfigurasi & disimpan di dalam Uptime Kuma sendiri (Settings > Notifications), bukan oleh skill ini — sesuai keputusan pemilik 2026-09-23 (Telegram = default kanal notifikasi/laporan).

## 5. Keputusan kurasi

**Jalur:** kurasi software (jalur 2, "produk siap pakai pengganti SaaS berbayar") + skill orisinal Komunitech (jalur 1). **Uptime Kuma TIDAK didistribusikan** dalam paket Komunitech; pembeli memasangnya sendiri (Docker resmi `louislam/uptime-kuma` atau `npm`/rilis GitHub) mengikuti `docs/panduan-uptime-kuma.md`. Nilai tambah Komunitech: panduan pasang bahasa awam, daftar monitor yang disarankan khusus toko online Indonesia (checkout, domain/SSL, link WA/katalog, form pesanan), skill `pantau.py` untuk ringkasan harian/mingguan + mode tanpa Uptime Kuma sama sekali (`cek-cepat`), dan panduan jadwal Telegram lewat OpenClaw.
