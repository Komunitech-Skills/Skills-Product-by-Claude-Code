# Panduan Pasang Uptime Kuma untuk Pemilik Toko Online (bahasa awam)

Uptime Kuma adalah program **gratis dan open-source** (lisensi MIT) untuk memantau apakah website, halaman checkout, atau link Anda masih hidup — pengganti UptimeRobot/Pingdom/StatusCake berbayar. Program ini jalan **di komputer/mini PC/VPS Anda sendiri**: tidak ada biaya bulanan (kecuali Anda memilih sendiri layanan cloud pihak ketiga, yang **tidak** dibahas di sini). Panduan ini menyiapkan Uptime Kuma agar bisa dipakai skill **Pantau Website Toko** (`pantau-website-toko`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pasang Uptime Kuma di mini PC/VPS yang menyala 24 jam, tambahkan monitor yang disarankan di bawah, publikasikan status page, sambungkan notifikasi Telegram, dan jadwalkan ringkasan harian. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan proyek Uptime Kuma; Uptime Kuma adalah karya Louis Lam dan komunitasnya, dipakai di sini sesuai lisensi MIT-nya.

**Status panduan (26 September 2026).** Langkah dipasang & dijalankan **langsung** oleh Komunitech dengan **rilis resmi 2.5.5** (dari GitHub Releases resmi, dijalankan sungguhan di sandbox, terikat `127.0.0.1`) untuk: instalasi via npm resmi, membuat akun, menambah monitor, membuat & mempublikasikan status page, dan membaca endpoint status page publik — lihat `research/sources/uptime-kuma-2026-09-26.md` untuk metodologi lengkap. **⚠️ Belum dicoba langsung** oleh Komunitech: instalasi Docker/Docker Compose (kebijakan sandbox memblokir daemon Docker — langkahnya disalin dari `docker-compose.yml` resmi di repo, bukan dari uji langsung), instalasi Windows/macOS sungguhan, dan pengiriman notifikasi Telegram sungguhan (butuh token bot & chat id asli). Bila tampilan di komputer Anda berbeda, ikuti tulisan di layar atau hubungi kami.

## Daftar isi
1. Sebelum mulai — pilih cara pasang
2. Cara A: Docker (disarankan untuk mini PC/VPS Linux) ⚠️ belum diuji langsung
3. Cara B: npm/Node.js (dicoba langsung Komunitech, cocok Windows/macOS/Linux)
4. Buat akun pertama (jadi admin)
5. Tambah monitor & publikasikan status page (WAJIB untuk skill)
6. Notifikasi Telegram (kanal default Komunitech)
7. Daftar monitor yang disarankan untuk toko online
8. Menyalakan Uptime Kuma setiap hari
9. Cadangan (backup) & pemulihan
10. Update
11. Masalah umum

---

## 1. Sebelum mulai — pilih cara pasang
| Kebutuhan | Keterangan |
|---|---|
| Komputer/mini PC/VPS | Windows 10/11, macOS, atau Linux, yang **menyala terus** agar pemantauan tidak berhenti. RAM ≥ 1 GB, ruang kosong ≥ 500 MB |
| Waktu | ±20–30 menit |
| Python 3.8+ | Untuk skill (gratis di python.org; saat memasang di Windows centang **Add Python to PATH**) |

Dua cara resmi:
- **Docker** (bagian 2) — paling rapi untuk mini PC/VPS Linux yang sudah punya Docker, dan yang direkomendasikan Uptime Kuma sendiri untuk produksi. **Belum diuji langsung** oleh Komunitech di sandbox ini (Docker diblokir kebijakan sandbox); langkah diambil dari `docker-compose.yml` resmi di repo.
- **npm/Node.js** (bagian 3) — **dicoba langsung** Komunitech, jalan di Windows/macOS/Linux asal Node.js terpasang.

Istilah: **Status page** = halaman ringkasan status yang bisa dibuka siapa saja (mis. pelanggan Anda), sekaligus sumber data yang dibaca `pantau.py`. **Monitor** = satu hal yang dipantau (satu website, satu halaman checkout, dst).

---

## 2. Cara A: Docker (⚠️ belum diuji langsung Komunitech)
Ikuti bila Anda sudah familiar Docker (mis. di VPS Linux):
1. Pastikan Docker & Docker Compose terpasang (ikuti dokumentasi resmi Docker, di luar cakupan panduan ini).
2. Buat file `docker-compose.yml` di folder baru, isi (disalin dari repo resmi `louislam/uptime-kuma`):
   ```yaml
   services:
     uptime-kuma:
       image: louislam/uptime-kuma:1
       container_name: uptime-kuma
       volumes:
         - ./uptime-kuma-data:/app/data
       ports:
         - "127.0.0.1:3001:3001"
       restart: unless-stopped
   ```
   **Perhatikan** `127.0.0.1:3001:3001` (bukan `3001:3001` saja) — ini yang membatasi akses hanya dari komputer/VPS itu sendiri (lihat bagian 5 & Keamanan). Kalau memang ingin diakses dari luar dengan aman (HTTPS), itu butuh reverse proxy tambahan — konsultasikan ke jasa setup Komunitech, jangan buka porta langsung ke internet.
3. Jalankan: `docker compose up -d`.
4. Buka `http://127.0.0.1:3001` (di komputer/VPS yang sama, atau lewat SSH tunnel bila VPS jauh).
- Lanjut ke bagian 4.

---

## 3. Cara B: npm/Node.js (dicoba langsung Komunitech)
1. Pasang **Node.js versi 20 atau lebih baru** dari https://nodejs.org (pilih versi "LTS"). Saat memasang di Windows, biarkan opsi default (sudah termasuk `npm`).
2. Buka Terminal/Command Prompt, unduh kode sumber rilis stabil resmi (ganti `2.5.5` bila ada versi lebih baru di https://github.com/louislam/uptime-kuma/releases — pastikan yang dipilih **bukan** versi "beta"/"rc"):
   ```bash
   git clone https://github.com/louislam/uptime-kuma.git
   cd uptime-kuma
   git checkout 2.5.5
   npm run setup
   ```
   (`npm run setup` = perintah resmi proyek: memasang dependensi dari registry npm resmi lalu mengunduh tampilan web siap pakai dari GitHub Releases resmi — **bukan** skrip pihak ketiga.) Tidak punya `git`? Unduh ZIP source code dari halaman rilis GitHub, ekstrak, lalu jalankan `npm install && npm run download-dist` di dalam foldernya.
3. Jalankan (Windows: buka Command Prompt di folder itu; macOS/Linux: Terminal):
   ```bash
   UPTIME_KUMA_HOST=127.0.0.1 UPTIME_KUMA_PORT=3001 node server/server.js
   ```
   Windows (Command Prompt, satu baris):
   ```
   set UPTIME_KUMA_HOST=127.0.0.1 && set UPTIME_KUMA_PORT=3001 && node server\server.js
   ```
   **`UPTIME_KUMA_HOST=127.0.0.1` wajib** — tanpa ini Uptime Kuma mendengarkan di semua jaringan (lihat Keamanan). Jendela terminal harus **tetap terbuka** selama Uptime Kuma dipakai.
4. Buka browser: `http://127.0.0.1:3001`.
- ✅ **Cek berhasil:** tampil halaman "Create your admin account" (dikonfirmasi langsung oleh Komunitech dengan langkah persis ini pada rilis 2.5.5).
- ❌ **Kalau gagal:** "This site can't be reached" → tunggu beberapa detik lalu muat ulang. Port 3001 dipakai program lain → ganti `UPTIME_KUMA_PORT` (mis. `3011`), sesuaikan alamat yang dipakai nanti di skill.

---

## 4. Buat akun pertama (jadi admin)
1. Isi username & sandi **kuat** (≥ 12 karakter) di halaman "Create your admin account", klik **Create**.
2. Anda otomatis masuk ke Dashboard. Akun ini adalah **satu-satunya** cara masuk — Uptime Kuma tidak punya pendaftaran terbuka untuk orang lain secara default.
- ✅ **Cek berhasil:** masuk ke Dashboard kosong ("No Monitors, please add one").

---

## 5. Tambah monitor & publikasikan status page (WAJIB untuk skill)
1. Klik **+ Add New Monitor**. Untuk website/halaman biasa: **Monitor Type = HTTP(s)**, isi **Friendly Name** (nama yang jelas, mis. "Website Toko - Beranda") dan **URL** lengkap (`https://tokosaya.contoh`). **Heartbeat Interval** (jarak antar-cek) disarankan **≥ 60 detik** — jangan diset ke beberapa detik, itu membebani server Anda sendiri tanpa manfaat tambahan berarti. Klik **Save**.
2. Ulangi untuk tiap hal yang mau dipantau (lihat daftar saran di bagian 7).
3. Buat status page: menu **Status Pages** (ikon di sidebar) → **+ New Status Page**. Beri nama & **slug** (bagian alamat, mis. `toko-saya` → alamatnya jadi `.../status/toko-saya`, catat ini untuk dipakai skill).
4. Di halaman edit status page, klik **+ Add a monitor**, pilih monitor yang mau ditampilkan publik (bisa semua, bisa sebagian), atur ke dalam grup (mis. "Layanan Utama").
5. **(Disarankan)** Di pengaturan status page, aktifkan **Show Certificate Expiry** — supaya sisa hari SSL ikut ditampilkan skill.
6. Klik **Save**, lalu tombol **Publish** di pojok kanan atas — **wajib**, tanpa ini endpoint publik yang dibaca skill tidak akan mengembalikan data monitornya.
7. Catat alamat lengkap status page-nya, mis. `http://127.0.0.1:3001/status/toko-saya` — inilah `--status-url` yang dipakai `pantau.py`.
- ✅ **Cek berhasil:** buka alamat status page itu di browser, muncul daftar monitor dengan lampu hijau/merah. Lalu jalankan `python3 <folder-skill>/scripts/pantau.py cek --status-url <alamat-itu>` — harus menampilkan judul & jumlah monitor.

---

## 6. Notifikasi Telegram (kanal default Komunitech)
Sesuai keputusan pemilik Komunitech (2026-09-23), **Telegram = kanal default** untuk notifikasi. Uptime Kuma sudah punya ini bawaan:
1. Buat bot Telegram sekali (di Telegram, chat ke **@BotFather** → `/newbot` → ikuti instruksinya → catat **Bot Token**). Cari **Chat ID** Anda sendiri (chat ke **@userinfobot** di Telegram, atau ikuti wiki resmi Uptime Kuma bagian Telegram).
2. Di Uptime Kuma: **Settings → Notifications → Setup Notification**. Pilih **Telegram**, isi **Bot Token** & **Chat ID**, klik **Test** (harus muncul pesan di Telegram Anda), lalu **Save**.
3. Buka tiap monitor yang mau diawasi → centang notifikasi Telegram itu → **Save**.
- ✅ **Cek berhasil:** tombol **Test** di langkah 2 berhasil mengirim pesan ke Telegram Anda.
- Ini **satu-satunya** jalur "kirim pesan otomatis saat down" yang dipakai — skill `pantau-website-toko` sendiri **tidak** mengirim pesan otomatis, hanya meringkas saat diminta atau lewat jadwal (`references/openclaw-jadwal.md` di skill).

---

## 7. Daftar monitor yang disarankan untuk toko online
| Monitor | Tipe di Uptime Kuma | Kenapa penting |
|---|---|---|
| Website toko / beranda | HTTP(s) | Yang pertama dilihat pelanggan |
| Halaman checkout / keranjang | HTTP(s), URL persis halaman checkout | Checkout down = kehilangan penjualan langsung, sering luput dari pantauan "website utama saja" |
| Domain & sertifikat SSL | Pakai monitor HTTP(s) di atas + aktifkan **Show Certificate Expiry** (bagian 5) | SSL kedaluwarsa → browser pelanggan menampilkan peringatan "Not Secure", kepercayaan turun drastis |
| Link WA (`wa.me/...`) atau link katalog di bio (Linktree dsb.) | HTTP(s) | Sering jadi jalur utama pemesanan di media sosial, jarang dicek manual |
| Form pesanan (Google Form/Tally/dsb.) | HTTP(s), URL persis form-nya | Form yang error/kosong berarti pesanan hilang tanpa disadari |
| API/backend toko (bila pakai platform custom) | HTTP(s) atau **Port** (TCP) sesuai kebutuhan teknis | Untuk yang punya sistem sendiri di belakang website |

Untuk yang bukan HTTP biasa (mis. hanya ingin tahu servernya menyala), Uptime Kuma juga punya tipe **Port (TCP)**, **Ping**, **DNS**, dll. — pilih sesuai kebutuhan lewat dropdown **Monitor Type** saat menambah monitor.

---

## 8. Menyalakan Uptime Kuma setiap hari
Jendela program (Terminal/Command Prompt untuk Cara B, atau container Docker untuk Cara A dengan `restart: unless-stopped`) harus tetap berjalan agar pemantauan & notifikasi Telegram terus bekerja. Untuk npm/Node.js, agar berjalan otomatis setiap komputer menyala tanpa membuka Terminal manual: Windows → Task Scheduler (jalankan saat startup); Linux → systemd service; macOS → LaunchAgent. Langkah detail ini teknis — **jasa setup Komunitech** dapat mengerjakannya sekaligus, atau pakai Cara A (Docker) yang punya `restart: unless-stopped` bawaan.

---

## 9. Cadangan (backup) & pemulihan
Semua data ada di **satu folder**: `data/` di dalam folder Uptime Kuma Anda (Cara B) atau volume `./uptime-kuma-data` (Cara A Docker) — berisi `kuma.db` (SQLite).
1. **Hentikan Uptime Kuma dulu** (agar file tidak sedang ditulis).
2. Salin seluruh folder `data/` ke flashdisk/hard disk eksternal atau folder cloud pribadi terenkripsi. Beri nama bertanggal.
3. Jalankan lagi Uptime Kuma.
4. **Pemulihan**: pasang Uptime Kuma versi yang sama (bagian 2/3), hentikan, timpa folder `data/` dengan salinan cadangan, jalankan lagi.
- Skill `pantau-website-toko` **tidak** membuat cadangan otomatis untuk Uptime Kuma — lakukan manual berkala, atau jasa setup Komunitech bisa menjadwalkannya.

---

## 10. Update
1. **Backup dulu** (bagian 9).
2. Cara A (Docker): `docker compose pull && docker compose up -d`.
   Cara B (npm): `git pull && git checkout <versi-baru>` lalu ulangi `npm run setup` di folder yang sama (folder `data/` tetap dipakai apa adanya, jangan dihapus).
3. Jalankan lagi. Uptime Kuma menjalankan migrasi database otomatis saat pertama menyala.
- ❌ **Kalau gagal setelah update:** kembalikan versi lama + cadangan `data/` (bagian 9), laporkan ke dukungan Komunitech.

---

## 11. Masalah umum
| Gejala | Penyebab | Solusi |
|---|---|---|
| Browser: "This site can't be reached" | Uptime Kuma belum/baru menyala | Tunggu beberapa detik, cek jendela program/container masih berjalan |
| "port 3001 sudah dipakai" | Program lain memakai port itu | Ganti `UPTIME_KUMA_PORT` (npm) atau bagian `ports` di `docker-compose.yml`, sesuaikan alamat di skill |
| Skill: "tidak ditemukan" (slug) | Status page belum di-**Publish**, atau slug salah | Ulangi bagian 5 langkah 6; cek ejaan slug di alamat browser |
| Skill: "belum berisi monitor apa pun" | Belum ada monitor ditambahkan ke grup status page | Ulangi bagian 5 langkah 4 |
| Sisa hari SSL tidak muncul di ringkasan | "Show Certificate Expiry" belum diaktifkan, atau monitornya `http://` bukan `https://` | Aktifkan di pengaturan status page (bagian 5 langkah 5) |
| Test Telegram gagal | Bot Token/Chat ID salah, atau bot belum pernah di-`/start` di chat itu | Buka chat dengan bot Anda di Telegram, kirim `/start` sekali, coba Test lagi |
| HP di Wi-Fi yang sama bisa membuka Uptime Kuma | `UPTIME_KUMA_HOST=127.0.0.1` belum diset (npm) atau `ports` di Docker tidak diawali `127.0.0.1:` | Ulangi bagian 2/3 dengan pengaturan alamat yang benar |

Butuh bantuan? **Jasa setup Komunitech** mengerjakan seluruh panduan ini bersama Anda: instalasi, monitor yang disarankan, status page, notifikasi Telegram, dan menjalankannya otomatis setiap komputer/VPS menyala.

Komunitech tidak berafiliasi dengan proyek Uptime Kuma; "Uptime Kuma" adalah nama proyek milik pembuatnya (Louis Lam).
