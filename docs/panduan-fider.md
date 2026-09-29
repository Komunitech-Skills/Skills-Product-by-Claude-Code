# Panduan Fider: Papan Masukan & Voting Fitur di Komputer Sendiri (bahasa awam)

Fider adalah program **gratis dan open-source** (lisensi AGPL-3.0) untuk mengumpulkan **masukan pelanggan**: pelanggan menulis usulan ("tolong ada pembayaran QRIS"), pelanggan lain memberi **suara** (vote) dan komentar, lalu Anda menandai statusnya (Direncanakan, Sedang dikerjakan, Selesai). Cara kerjanya mirip Canny atau UserVoice, tetapi **jalan di komputer/server Anda sendiri**, tanpa biaya bulanan per pengguna. Panduan ini menyiapkan Fider agar bisa dikelola skill **Masukan Pelanggan Fider** (`fider-masukan-pelanggan`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: siapkan komputer/VPS, domain + HTTPS, pasang Fider + database, atur email pengirim, buat kunci API untuk AI, tag awal, dan jadwal ringkasan mingguan ke Telegram. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan tim Fider (getfider). "Fider" adalah nama milik pengembangnya.

**Status panduan (29 September 2026).** Ditulis sendiri oleh Komunitech, dicocokkan dengan Fider **v0.38.0** (rilis terbaru saat ditulis). Komunitech **menjalankan Fider v0.38.0 sungguhan** lewat **Docker Compose** dengan PostgreSQL 17 (Linux), membuat situs, kunci API, dan mencoba semua perintah skill. **Belum dicoba langsung:** Windows dan macOS (langkahnya sama karena memakai Docker Desktop, tetapi belum kami jalankan di sana), HTTPS lewat Caddy di VPS sungguhan, dan pengiriman email lewat penyedia SMTP sungguhan (kami memakai penampung email tiruan). Bila tampilan di layar Anda berbeda, ikuti tulisan di layar atau hubungi kami.

## Daftar isi
1. Sebelum mulai: apa yang Anda butuhkan
2. Pasang Docker (Windows / macOS / Linux)
3. Siapkan folder & pengaturan
4. Jalankan Fider
5. Buat papan pertama & akun pemilik
6. Kunci API untuk AI
7. Tag awal & pengaturan yang disarankan
8. Dipakai pelanggan: HTTPS & alamat publik
9. Privasi, UU PDP & lisensi AGPL
10. Cadangan, update, copot pasang
11. Masalah umum

---

## 1. Sebelum mulai: apa yang Anda butuhkan
- Komputer/server dengan RAM minimal 2 GB kosong dan ±2 GB ruang disk.
- **Docker** (bagian 2). Fider dan database jalan sebagai dua "kotak" (container).
- **Akun email pengirim (SMTP)** untuk login: Fider tidak memakai sandi. Pemilik dan pelanggan masuk lewat **tautan yang dikirim ke email**. Tanpa email yang bisa mengirim, Anda tidak bisa masuk. Pilihan: Gmail dengan "sandi aplikasi", Brevo/Mailgun/Zoho, atau email hosting domain Anda. Siapkan: alamat server (host), port (biasanya 587), nama pengguna, sandi.
- Untuk dipakai pelanggan di internet: **domain** (mis. `saran.tokosaya.id`) dan server yang menyala terus (VPS). **Laptop yang dimatikan = papan ikut mati.** Untuk sekadar mencoba, komputer sendiri cukup.

## 2. Pasang Docker
Sumber resmi: https://docs.docker.com/get-started/get-docker/
- **Windows 10/11:** pasang *Docker Desktop*, nyalakan ulang komputer bila diminta, buka aplikasinya sampai tertulis "Engine running". Semua perintah di bawah diketik di **PowerShell**.
- **macOS:** pasang *Docker Desktop* (pilih Apple Silicon atau Intel sesuai komputer), buka aplikasinya. Perintah diketik di **Terminal**.
- **Linux (Ubuntu/Debian):** ikuti petunjuk resmi "Install Docker Engine" di dokumentasi Docker (jangan memakai skrip dari situs tak dikenal). Perintah diketik di terminal.

Cek berhasil: `docker --version` dan `docker compose version` menampilkan nomor versi.

## 3. Siapkan folder & pengaturan
1. Buat folder: `mkdir fider` lalu masuk `cd fider` (Windows PowerShell sama).
2. Buat dua rahasia acak:
   - Linux/macOS: `openssl rand -hex 32` (untuk JWT_SECRET) dan `openssl rand -hex 16` (sandi database).
   - Windows PowerShell: `-join ((48..57)+(97..102) | Get-Random -Count 64 | % {[char]$_})` (jalankan dua kali). Atau ketik 40+ huruf/angka acak sendiri.
3. Buat file `docker-compose.yml` (Notepad di Windows: "Simpan sebagai" > Semua file; Linux/macOS: `nano docker-compose.yml`):
   ```yaml
   services:
     db:
       image: postgres:17
       restart: unless-stopped
       environment:
         POSTGRES_USER: fider
         POSTGRES_DB: fider
         POSTGRES_PASSWORD: ${DB_PASSWORD}
       volumes:
         - fider-db:/var/lib/postgresql/data
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U fider -d fider"]
         interval: 5s
         timeout: 5s
         retries: 10

     fider:
       image: getfider/fider:v0.38.0        # versi dikunci agar tidak berubah sendiri
       restart: unless-stopped
       depends_on:
         db:
           condition: service_healthy
       ports:
         - "127.0.0.1:${FIDER_PORT:-3000}:3000"   # hanya komputer ini; HTTPS di depannya (bagian 8)
       environment:
         BASE_URL: ${BASE_URL}
         DATABASE_URL: postgres://fider:${DB_PASSWORD}@db:5432/fider?sslmode=disable
         JWT_SECRET: ${JWT_SECRET}
         EMAIL_NOREPLY: ${EMAIL_NOREPLY}
         EMAIL_SMTP_HOST: ${SMTP_HOST}
         EMAIL_SMTP_PORT: ${SMTP_PORT:-587}
         EMAIL_SMTP_USERNAME: ${SMTP_USER:-}
         EMAIL_SMTP_PASSWORD: ${SMTP_PASSWORD:-}
         # Sebagian penyedia SMTP (port 587) meminta STARTTLS: tambahkan baris EMAIL_SMTP_ENABLE_STARTTLS: "true"
         # (menurut docs.fider.io; belum kami coba dengan penyedia sungguhan)

   volumes:
     fider-db:
   ```
4. Buat file `.env` **di folder yang sama** (isi rahasia Anda; jangan dibagikan atau diunggah):
   ```
   BASE_URL=http://localhost:3000
   DB_PASSWORD=<sandi database acak>
   JWT_SECRET=<64 karakter acak>
   EMAIL_NOREPLY=noreply@tokosaya.id
   SMTP_HOST=smtp.contoh.com
   SMTP_PORT=587
   SMTP_USER=<pengguna SMTP>
   SMTP_PASSWORD=<sandi SMTP>
   ```
   **Penting:** `BASE_URL` harus **persis sama dengan alamat yang Anda ketik di peramban** (termasuk `http`/`https` dan port). Salah alamat = tidak bisa login. Setelah HTTPS dipasang (bagian 8), ganti ke `https://saran.tokosaya.id`.
   Linux/macOS: setelah membuat `.env`, jalankan `chmod 600 .env`.

## 4. Jalankan Fider
```bash
docker compose up -d
docker compose ps        # db = healthy, fider = Up
docker compose logs fider --tail 20
```
Pertama kali, Docker mengunduh image (beberapa menit). Fider menyiapkan tabel database sendiri saat menyala (log berisi "migrations have been applied"). Buka `http://localhost:3000` di peramban.

## 5. Buat papan pertama & akun pemilik
1. Halaman awal meminta **nama papan** (mis. "Saran untuk Toko Saya"), **nama Anda**, dan **email**. Centang persetujuan lalu kirim.
2. Cek email Anda, klik tautan verifikasi. Akun ini otomatis menjadi **Administrator**.
3. Tambahkan logo dan judul di **Settings > General** bila perlu.

## 6. Kunci API untuk AI
1. Login, klik nama/foto Anda di pojok kanan atas > **Settings** > **API Key** > **Regenerate API Key**. Kunci muncul **satu kali saja**; salin.
2. Di komputer yang menjalankan AI Anda, ketik (Windows: `python` atau `py`):
   ```bash
   python3 scripts/fider.py simpan-alamat http://localhost:3000
   python3 scripts/fider.py simpan-kunci
   ```
   Kunci ditempel ke layar tersembunyi (tidak terlihat) dan disimpan di `~/.komunitech/fider-kunci.txt` (izin 600). **Jangan tempel kunci di chat dengan AI.** Terlanjur? Buat kunci baru (Regenerate) sehingga yang lama mati.
3. Uji: `python3 scripts/fider.py cek`.

**Peran akun.** Kunci mengikuti peran pemiliknya. **Administrator** bisa semua (termasuk membuat tag). **Collaborator** bisa mengubah status, menandai tag yang sudah ada, dan menggabung duplikat, tetapi tidak bisa membuat tag baru. Untuk lebih aman, undang satu akun khusus AI sebagai Collaborator (Settings > Users) dan pakai kuncinya.
Semua tindakan AI tercatat atas nama pemilik kunci di papan (mis. komentar "Pemilik Toko").

## 7. Tag awal & pengaturan yang disarankan
- Tag contoh: Pembayaran, Pengiriman, Tampilan, Harga, Produk baru, Layanan. Dibuat lewat Settings > Tags atau perintah skill `tag-buat` (butuh Administrator).
- **Settings > Privacy**: pilih papan **publik** (siapa pun boleh melihat) atau **privat** (harus login). Bila papan publik, jangan menaruh data pribadi pelanggan di pos (bagian 9).
- **Moderasi:** halaman Administration memiliki pengaturan *Content Moderation* (pos baru menunggu persetujuan Anda) bila Anda khawatir spam. Nama menu bisa sedikit berbeda antar versi.
- Statusnya: **Terbuka** (baru), **Direncanakan**, **Sedang dikerjakan**, **Selesai**, **Ditolak**, **Duplikat**.

## 8. Dipakai pelanggan: HTTPS & alamat publik
Agar pelanggan dapat membuka papan dari internet, pakai server (VPS) dengan alamat ber-**HTTPS**. Cara paling ringkas: **Caddy** (web server yang mengurus sertifikat otomatis).
1. Arahkan domain `saran.tokosaya.id` ke IP server (catatan DNS "A").
2. Pasang Caddy dari paket resmi: https://caddyserver.com/docs/install (bukan dari skrip tak dikenal).
3. Isi `/etc/caddy/Caddyfile`:
   ```
   saran.tokosaya.id {
       reverse_proxy 127.0.0.1:3000
   }
   ```
4. `sudo systemctl reload caddy`. Ubah `BASE_URL=https://saran.tokosaya.id` di `.env`, lalu `docker compose up -d`.
5. Buka tautan itu; pasang di menu website, bio Instagram, atau kirim ke pelanggan.

*(Langkah HTTPS ini mengikuti dokumentasi resmi Caddy dan belum dijalankan Komunitech di VPS sungguhan; jasa setup kami yang menanganinya.)*
Jangan membuka port 3000 langsung ke internet tanpa HTTPS; kunci API dan sesi login akan lewat tanpa terenkripsi. Skill menolak alamat `http://` untuk server di internet.

## 9. Privasi, UU PDP & lisensi AGPL
- **Papan publik = semua orang bisa membaca.** Catatan dari WhatsApp/marketplace sering memuat nomor HP, email, atau nama. Skill **menyamarkan nomor HP dan email otomatis** sebelum menulis pos/komentar, tetapi nama dan detail pesanan tetap Anda periksa sendiri di pratinjau.
- Simpan **hanya usulan**, bukan data pelanggan lengkap. Bila ingin tahu siapa yang mengusulkan, biarkan pelanggan sendiri login dan menulis.
- Pelanggan yang login memberi Fider **nama dan email** mereka: itu data pribadi. Beri tahu di halaman papan (Settings > General, deskripsi) bagaimana data dipakai; untuk bisnis serius, lihat skill `kebijakan-privasi-pdp`.
- **Lisensi AGPL-3.0:** memakai Fider apa adanya tidak menimbulkan kewajiban tambahan. Bila Anda (atau teknisi Anda) **mengubah kode Fider** lalu menyajikannya ke publik, Anda wajib menyediakan kode sumber versi ubahan itu. Ini bukan nasihat hukum.

## 10. Cadangan, update, copot pasang
- **Cadangan** (jalankan berkala, simpan di tempat lain, mis. flashdisk atau penyimpanan awan Anda):
  ```bash
  docker compose exec -T db pg_dump -U fider fider > cadangan-fider-$(date +%F).sql
  ```
  (Windows PowerShell: `docker compose exec -T db pg_dump -U fider fider | Out-File -Encoding utf8 cadangan-fider.sql`.) Uji pulihkan di komputer lain sebelum Anda benar-benar membutuhkannya.
- **Update:** cek rilis di https://github.com/getfider/fider/releases, baca catatan rilisnya, **cadangkan dulu**, ganti nomor versi di `docker-compose.yml`, lalu `docker compose pull && docker compose up -d`. Update rutin penting karena rilis Fider sering memuat perbaikan keamanan.
- **Berhenti sementara:** `docker compose stop`. **Copot pasang + hapus data:** `docker compose down -v` (data papan **hilang**).

## 11. Masalah umum
| Gejala | Penyebab & cara |
|---|---|
| Tidak ada email masuk | SMTP salah. Lihat `docker compose logs fider`; periksa host/port/pengguna/sandi; cek folder spam; Gmail butuh "sandi aplikasi". |
| Setelah klik tautan email, muncul galat/berputar | `BASE_URL` tidak sama dengan alamat di peramban. Samakan lalu `docker compose up -d`. |
| `docker compose up` gagal "port already allocated" | Port 3000 dipakai program lain. Isi `FIDER_PORT=3100` di `.env` dan `BASE_URL` yang sesuai. |
| Gagal mengunduh image (429 / rate limit) | Batas unduhan Docker Hub; tunggu beberapa menit atau login `docker login`. |
| `GALAT: Kunci API ditolak` | Kunci salah atau sudah di-Regenerate. Buat baru, `simpan-kunci --ya`. |
| `GALAT: Akses ditolak` | Akun pemilik kunci bukan Collaborator/Administrator, atau aksi khusus Administrator (buat tag). |
| Halaman kosong di layar HP pelanggan | Pastikan mengakses lewat HTTPS dan alamat yang sama dengan `BASE_URL`. |
| Laptop tidur, papan tidak bisa dibuka | Wajar. Untuk dipakai pelanggan, pakai VPS/mini PC yang menyala terus (jasa setup Komunitech tersedia). |
