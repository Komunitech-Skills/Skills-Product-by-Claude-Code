# Panduan Pasang Grist untuk UMKM (bahasa awam)

Grist adalah program **gratis dan open-source** (lisensi Apache-2.0, dibuat oleh **Grist Labs
Inc.**) — gabungan antara spreadsheet (seperti Excel) dan database, tapi dengan tampilan
sederhana yang bisa dipakai orang awam. Cocok untuk daftar pelanggan, pesanan, stok sederhana,
jadwal konten, atau tabel apa pun yang selama ini dibuatkan Google Sheets/Airtable — tapi jalan
**di komputer Anda sendiri**: data tidak dititipkan ke perusahaan lain, tidak ada biaya bulanan,
dan tidak ada batas jumlah baris seperti paket gratis Airtable. Panduan ini menyiapkan Grist agar
bisa dipakai skill **Grist Usaha** (`grist-usaha`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pemasangan Grist (Docker
> atau Desktop), pembuatan 4 template usaha siap pakai, kunci API aman, cadangan otomatis, dan
> jadwal laporan ke Telegram. Hubungi admin komunitech.com.

> Komunitech tidak berafiliasi dengan Grist Labs Inc. atau produk Grist; "Grist" adalah merek
> milik pemiliknya.

## 0. Status panduan — jujur soal apa yang sudah & belum dicoba (26 September 2026)

Komunitech membaca **langsung kode sumber resmi** `grist-core` (v1.7.19) dan `grist-desktop`
(v0.3.15) dari GitHub untuk memastikan alamat unduhan, port default (**8484**), format API
(`Authorization: Bearer <kunci>`), dan format file `.grist` (SQLite) yang ditulis di bawah ini
benar — lihat `research/sources/grist-2026-09-26.md` untuk rincian.

**Yang BELUM dicoba klik/jalankan langsung** oleh Komunitech: menyalakan container Docker
`gristlabs/grist` sungguhan (lingkungan pembuatan panduan ini tidak mengizinkan menjalankan
Docker), dan aplikasi desktop Grist (tidak ada layar/GUI di lingkungan tersebut). Langkah di
bawah disusun dari `README.md` resmi `grist-core` dan halaman rilis `grist-desktop`, **bukan**
hasil klik langsung. Skill `grist-usaha` sendiri diuji dengan **file `.grist` (SQLite) tiruan**
yang skemanya disusun sama persis dengan kode sumber resmi (lihat `examples/` skill), belum
dengan dokumen Grist sungguhan. Bila tampilan di komputer Anda berbeda dari tulisan di sini,
ikuti tulisan di layar dan hubungi kami — atau pakai jasa setup berbayar di atas, yang akan
menguji langsung di komputer Anda.

## Daftar isi
1. Sebelum mulai — dua pilihan
2. Jalur A — Grist Desktop (mudah, satu pengguna, satu komputer)
3. Jalur B — Docker / grist-core (disarankan bila lebih dari satu orang memakai, atau ingin REST API)
4. Buat dokumen pertama
5. Empat template usaha siap pakai
6. Kunci API (opsional, untuk skill `grist-usaha`)
7. Cadangan (backup) & pemulihan file `.grist`
8. Keamanan — jangan buka ke internet
9. Masalah umum

---

## 1. Sebelum mulai — dua pilihan

| | Jalur A — Grist Desktop | Jalur B — Docker (grist-core) |
|---|---|---|
| Cocok untuk | 1 orang, 1 komputer, ingin paling sederhana | Beberapa orang di jaringan yang sama, atau ingin skill `grist-usaha` memakai REST API |
| Kesulitan | **Mudah** — seperti pasang aplikasi biasa | **Sedang** — butuh Docker Desktop |
| REST API untuk skill | Tidak tersedia (aplikasi berdiri sendiri, tanpa API terbuka) | **Ya** — inilah yang membuat skill `grist-usaha` bisa "menulis" (buat tabel, impor CSV) otomatis |
| File data | `.grist` di folder dokumen Anda | `.grist` di dalam folder `persist` yang Anda tentukan |

Tidak yakin? Mulai dari **Jalur A** (paling cepat dicoba). Skill `grist-usaha` tetap berguna
tanpa Jalur B — ia bisa membaca file `.grist` Anda langsung (read-only) untuk membuat ringkasan,
dan membantu merancang tabel/rumus meski Anda mengetiknya sendiri di Grist. REST API (Jalur B)
hanya menambah kemampuan "buat tabel & impor CSV otomatis".

| Kebutuhan | Keterangan |
|---|---|
| Komputer | Windows 10/11, macOS, atau Linux. RAM ≥ 4 GB, ruang kosong ≥ 1 GB |
| Waktu | Jalur A: ±5–10 menit. Jalur B: ±20–40 menit bila Docker Desktop belum ada |
| Python 3.8+ | Untuk skill `grist-usaha` (gratis di python.org; Windows: centang **Add Python to PATH**) |
| Docker Desktop (hanya Jalur B) | Gratis untuk pemakaian pribadi/UMKM kecil, unduh di docker.com |

---

## 2. Jalur A — Grist Desktop (mudah)

1. Buka halaman **Releases** resmi: https://github.com/gristlabs/grist-desktop/releases —
   pilih rilis teratas (saat panduan ditulis: **v0.3.15**).
2. Unduh sesuai OS Anda:
   - **Windows**: file `.exe` (installer) di bagian Assets.
   - **macOS**: file `.dmg`.
   - **Linux**: file `.AppImage` (jalan langsung, tanpa instalasi) atau `.deb` (Debian/Ubuntu:
     `sudo apt install ./nama-file.deb` — bukan skrip unduh-dan-eksekusi-langsung, cukup perintah
     `apt install` biasa untuk file yang sudah Anda unduh sendiri).
3. Jalankan aplikasinya. Grist Desktop tidak butuh akun online — semua tersimpan sebagai file
   `.grist` di komputer Anda (defaultnya folder Dokumen).
- ✅ **Cek berhasil:** aplikasi terbuka, muncul layar "Create empty document" / "Buat dokumen kosong".
- ❌ **Kalau gagal:** Windows SmartScreen memblokir → **More info → Run anyway** (hanya karena
  file dari github.com/gristlabs, sumber resmi). macOS: "pengembang tidak dikenal" → **System
  Settings → Privacy & Security → Open Anyway**. Linux `.AppImage` tidak jalan → klik kanan →
  Properties → izinkan "Execute as program", atau `chmod +x nama-file.AppImage` lalu jalankan.

**Catatan jujur:** langkah di atas disusun dari halaman rilis resmi & `README.md` proyek, belum
diklik langsung oleh Komunitech (lihat bagian 0).

---

## 3. Jalur B — Docker / grist-core (disarankan bila butuh REST API)

### 3.1 Pasang Docker Desktop (lewati bila sudah ada)
Unduh di https://www.docker.com/products/docker-desktop/, pasang, buka sekali sampai ikonnya
hijau/"Running". Di Windows biasanya installer meminta **restart** sekali untuk WSL2 — ini
normal (lihat `docs/panduan-stirling-pdf.md` bagian 3.1 untuk uraian yang sama, karena
prosesnya identik).

### 3.2 Jalankan Grist — **hanya untuk komputer sendiri**
Buka Terminal (macOS/Linux) atau PowerShell (Windows). Salin-tempel **persis seperti ini**
(perhatikan `127.0.0.1:8484:8484` — **bukan** `8484:8484` saja, supaya Grist **tidak** bisa
dibuka dari komputer lain di jaringan Wi-Fi yang sama):
```bash
mkdir -p grist-data
docker run -d --name grist --restart unless-stopped \
  -p 127.0.0.1:8484:8484 \
  -v "$PWD/grist-data:/persist" \
  gristlabs/grist
```
(Windows PowerShell: ganti `$PWD/grist-data` dengan path lengkap, mis.
`C:\Users\NamaAnda\grist-data`, atau jalankan dari folder itu dan pakai `${PWD}`.)

- `-p 127.0.0.1:8484:8484` mengunci Grist agar **hanya bisa dibuka dari komputer ini**
  (`localhost`). Ini beda dari contoh di `README.md` resmi Grist yang menulis `-p 8484:8484` saja
  — versi Komunitech ini **sengaja lebih ketat** (lihat bagian 8 - Keamanan).
- `-v "$PWD/grist-data:/persist"` menyimpan semua dokumen `.grist` Anda di folder `grist-data`
  supaya tidak hilang saat container di-restart/dihapus.
- `--restart unless-stopped` membuat Grist otomatis menyala lagi setiap Docker Desktop
  dinyalakan.

1. Buka `http://localhost:8484` di browser.
2. **Pertama kali pasang**, Grist menampilkan layar "Quick setup" yang meminta **boot key**.
   Lihat log container untuk kode ini:
   ```bash
   docker logs grist 2>&1 | grep -i "boot key"
   ```
   Tempel boot key itu ke layar, lalu isi **email admin** (bisa email apa saja, tidak perlu
   valid/terverifikasi untuk pemakaian 1 komputer) dan pilih mode masuk yang paling sederhana
   ("no sign-in" / tanpa login, cocok untuk 1 komputer sendiri).
- ✅ **Cek berhasil:** halaman utama Grist tampil ("Home"), bisa klik "Create empty document".
- ❌ **Kalau gagal:**
  - "port is already allocated" → sesuatu sudah memakai port 8484. Ganti jadi
    `-p 127.0.0.1:8888:8484`, lalu buka `http://localhost:8888` dan set
    `GRIST_URL=http://localhost:8888` sebelum memakai skill.
  - "Cannot connect to the Docker daemon" → Docker Desktop belum menyala, buka dulu.
  - Lupa mencatat boot key / layar sudah terlanjur ditutup → jalankan
    `docker logs grist 2>&1 | grep -i "boot key"` lagi, kodenya tetap ada di log.
  - Container sudah terlanjur dibuat **tanpa** `127.0.0.1:` (mengikuti contoh resmi apa
    adanya) → perbaiki: `docker rm -f grist` lalu jalankan ulang perintah di atas — data di
    folder `grist-data` **tidak hilang**.

### 3.3 Menyalakan Grist setiap hari
Dengan `--restart unless-stopped`, Grist otomatis menyala begitu Docker Desktop menyala. Kalau
tidak, jalankan `docker start grist`. Cek kapan saja: buka `http://localhost:8484`, atau
`python3 <folder-skill>/scripts/grist.py cek`.

---

## 4. Buat dokumen pertama

1. Di halaman Home Grist (Desktop maupun Docker), klik **Create empty document** /
   **Buat dokumen kosong**. Beri nama, mis. "Data Usaha Saya".
2. Grist otomatis membuat 1 tabel kosong bernama `Table1` dengan 3 kolom contoh (`A`, `B`, `C`).
   Anda bisa mengganti nama tabel & kolom, atau menghapusnya dan memakai salah satu **template
   usaha** di bagian 5.
3. File dokumen tersimpan sebagai **satu file `.grist`** (sebenarnya file SQLite biasa) — di
   Jalur A biasanya di folder Dokumen, di Jalur B di dalam folder `grist-data/docs/` yang Anda
   buat di langkah 3.2. Catat lokasinya; skill `grist-usaha` butuh path ini untuk membaca laporan
   secara langsung (perintah `baca`).
- ✅ **Cek berhasil:** dokumen terbuka, terlihat tabel dengan baris/kolom seperti spreadsheet.
- ❌ **Kalau gagal:** layar putih/kosong lama → tutup tab, buka lagi `http://localhost:8484`
  (Docker) atau buka ulang aplikasi (Desktop).

---

## 5. Empat template usaha siap pakai

Skill `grist-usaha` punya rancangan siap pakai untuk 4 kebutuhan UMKM paling umum — kolom, tipe
data, dan rumus (formula Python Grist) ada di `skills/grist-usaha/references/pola-tabel-umkm.md`
(dalam paket pembelian Anda, folder skill). Cukup minta agent: *"Buatkan tabel pelanggan di
Grist saya"* (atau pesanan/stok/jadwal-konten), dan agent akan:
- **Punya REST API (Jalur B/Docker) + kunci API tersimpan (bagian 6):** membuat tabel & kolomnya
  langsung di dokumen Anda lewat perintah `python3 grist.py buat-tabel ...` (selalu ditunjukkan
  pratinjau dulu, baru dieksekusi setelah Anda bilang "ya").
- **Tanpa REST API (Jalur A/Desktop):** menuntun Anda membuat kolom-kolom itu sendiri di layar
  Grist (nama kolom, tipe, dan rumus tinggal disalin-tempel ke kotak formula Grist).

Empat template itu: **Daftar Pelanggan**, **Pesanan**, **Stok Sederhana**, **Jadwal Konten**.
Lihat contoh hasil jadi di `examples/` skill.

---

## 6. Kunci API (opsional, untuk skill `grist-usaha`)

Hanya perlu bila Anda memakai **Jalur B (Docker)** dan ingin skill membuat tabel/mengimpor CSV
otomatis lewat REST API. Jalur A (Desktop) tidak menyediakan API ini — skill tetap bisa membaca
file `.grist` Anda langsung (bagian 7 & perintah `baca`).

1. Di Grist, klik ikon profil (pojok kanan atas) → **Profile Settings** (Pengaturan Profil).
2. Cari bagian **API Key** → klik **Create** (atau **Show**/**Reset** bila sudah ada) → salin
   kuncinya.
3. Buka Terminal, jalankan (sesuaikan folder skill):
   ```
   python3 <folder-skill>/scripts/grist.py simpan-kunci
   ```
   Tempel kunci (tidak terlihat saat diketik) → Enter. Script menampilkan lebih dulu ke mana
   kunci akan disimpan (`~/.komunitech/grist-kunci.txt`, izin 600 = hanya Anda yang bisa baca)
   dan **menolak menimpa** file yang sudah ada kecuali ditambah `--ya`.
4. Alamat Grist bukan `http://localhost:8484`? Atur sekali: Windows
   `setx GRIST_URL "http://localhost:8888"` (buka Terminal baru sesudahnya); Mac/Linux tambahkan
   `export GRIST_URL=...` ke `~/.bashrc`/`~/.zshrc`.
5. Uji: `python3 <folder-skill>/scripts/grist.py cek`
- ✅ **Cek berhasil:** tampil daftar dokumen yang bisa diakses kunci itu.
- ❌ **Kalau gagal:** "401"/"tidak sah" → kunci salah/belum disimpan; ulangi langkah 1–3.
  "tidak bisa dihubungi" → Grist belum menyala (bagian 3.3).

**Jangan pernah** menempel kunci API di chat AI, grup WA, atau email. Kunci bocor? Buat kunci
baru di Profile Settings (kunci lama otomatis tidak berlaku), lalu `simpan-kunci` lagi.

---

## 7. Cadangan (backup) & pemulihan file `.grist`

File `.grist` **adalah** file SQLite biasa — mudah dicadangkan, tidak perlu `mysqldump` atau
alat khusus.

1. **Tutup dulu dokumennya** di Grist (atau hentikan container: `docker stop grist`) supaya
   filenya tidak sedang ditulis saat disalin.
2. Salin file `.grist` ke **flashdisk/hard disk eksternal**:
   - Jalur A (Desktop): folder Dokumen tempat Anda menyimpan file `.grist`.
   - Jalur B (Docker): folder `grist-data/docs/` yang Anda buat di langkah 3.2 (salin **seluruh
     folder** `grist-data`, bukan cuma satu file — Grist juga menulis file pendukung kecil di
     situ).
3. Nyalakan lagi dokumen/containernya.
- ✅ **Cek berhasil:** ukuran file `.grist` > 0 KB; bisa dibuka lagi di Grist (coba di komputer
  lain bila memungkinkan, untuk memastikan cadangan benar-benar utuh).
- ❌ **Kalau gagal:** file `.grist` berukuran 0 KB atau Grist menolak membukanya → kemungkinan
  disalin saat sedang ditulis; tutup dokumen dulu, ulangi dari langkah 1.

**Pemulihan:** pasang Grist (bagian 2/3) di komputer baru, lalu salin file `.grist` (Jalur A)
atau seluruh folder `grist-data` (Jalur B) kembali ke tempatnya, nyalakan Grist. Tidak ada
"kode unik instalasi" seperti Dolibarr — file `.grist` bisa dipindah bebas ke komputer lain yang
juga menjalankan Grist versi yang sama atau lebih baru.

**Cadangan otomatis harian/mingguan** lewat jadwal OpenClaw: minta agent menjalankan salin file
terjadwal, atau gunakan jasa setup Komunitech untuk mengatur ini sekali di awal.

---

## 8. Keamanan — jangan buka ke internet

1. **Jangan** mengubah `-p 127.0.0.1:8484:8484` menjadi `-p 8484:8484` atau
   `-p 0.0.0.0:8484:8484` — itu membuka Grist ke **semua** komputer di jaringan Wi-Fi/kantor
   Anda, bukan cuma komputer sendiri.
2. **Jangan** mengatur *port forwarding* di router, memakai *tunnel* (ngrok, Cloudflare Tunnel,
   dll.), atau memasang Grist di hosting/VPS tanpa HTTPS dan login yang benar. Grist di sini
   dirancang untuk **1 komputer/jaringan pribadi**, bukan server publik. Skill `grist-usaha`
   menolak alamat selain `localhost`/`127.0.0.1` kecuali Anda menegaskan lewat environment
   variable `GRIST_ALLOW_REMOTE=1`.
3. **Jangan pernah** menjalankan skrip yang bentuknya "unduh dan langsung jalankan" (mis. `curl`
   yang hasilnya disalurkan langsung ke shell tanpa dibaca) untuk memasang Grist — semua langkah
   di panduan ini memakai installer resmi yang Anda unduh dulu, atau perintah
   `docker run`/`apt install` biasa yang bisa Anda baca isinya sebelum dijalankan.
4. Simpan kunci API (bagian 6) seperti kata sandi: tidak ditempel di chat, tidak dikirim lewat
   WA/email.
5. Cadangan (bagian 7) disimpan **terpisah** dari komputer utama (kalau komputer kena
   ransomware/rusak, cadangan di disk yang sama ikut hilang/terkunci).

---

## 9. Masalah umum

| Gejala | Penyebab | Solusi |
|---|---|---|
| Browser: "Tidak dapat menjangkau situs" (`localhost:8484`) | Grist/Docker belum menyala | `docker start grist`, atau buka aplikasi Desktop |
| Skill: "tidak bisa dihubungi" | Sama / alamat salah | Buka alamat di browser dulu; samakan `GRIST_URL` |
| Skill: "401" / "tidak sah" | Kunci API salah/belum disimpan | Bagian 6 |
| Lupa boot key saat setup pertama | Layar sudah tertutup | `docker logs grist 2>&1 \| grep -i "boot key"` |
| "port is already allocated" | Port 8484 dipakai program lain | Pakai `-p 127.0.0.1:8888:8484`, set `GRIST_URL=http://localhost:8888` |
| File `.grist` tidak mau dibuka setelah disalin | Disalin saat sedang ditulis, atau file rusak/terpotong | Tutup dokumen dulu sebelum menyalin; pulihkan dari cadangan sebelumnya |
| Jalur A (Desktop) tidak bisa "buat tabel otomatis" lewat skill | Desktop tidak punya REST API terbuka | Normal — pakai Jalur B (Docker) untuk kemampuan itu, atau buat kolom manual mengikuti panduan agent |

Butuh bantuan? **Jasa setup Komunitech** mengerjakan seluruh panduan ini bersama Anda (jarak
jauh atau datang), termasuk memilih Jalur A/B yang cocok, 4 template usaha, kunci API aman, dan
jadwal cadangan otomatis.

Sumber resmi yang dirujuk panduan ini (diakses & diverifikasi langsung dari kode sumber,
26 September 2026): github.com/gristlabs/grist-core (README.md, LICENSE.txt, NOTICE.txt,
`app/server/lib/DocApi.ts`, `app/server/lib/DocStorage.ts`, `sandbox/grist/schema.py`),
github.com/gristlabs/grist-desktop (README.md, halaman Releases), hub.docker.com/r/gristlabs/grist.
Rincian metode verifikasi ada di `research/sources/grist-2026-09-26.md`.

Komunitech tidak berafiliasi dengan Grist Labs Inc.; "Grist" adalah merek milik pemiliknya.
