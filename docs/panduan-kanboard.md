# Panduan Pasang Kanboard untuk UMKM (bahasa awam)

Kanboard adalah program **gratis dan open-source** (lisensi MIT) untuk papan kerja model *kanban* — kartu-kartu pekerjaan yang digeser dari kolom ke kolom (mis. *Order Masuk → Produksi → Siap Kirim → Selesai*). Pengganti Trello/ClickUp berbayar. Program ini jalan **di komputer Anda sendiri**: data tidak dititipkan ke perusahaan lain dan tidak ada biaya bulanan. Panduan ini menyiapkan Kanboard agar bisa dipakai skill **Kanboard Papan Kerja** (`kanboard-papan-kerja`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pasang Kanboard di laptop/mini PC/VPS Anda, pengamanan, akun tim, papan sesuai jenis usaha, token API, jadwal laporan pagi ke Telegram, dan cadangan otomatis. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan proyek Kanboard. "Kanboard" adalah nama proyek milik pembuatnya (Frédéric Guillot dan kontributor). Kanboard **tidak** disertakan di paket ini; Anda mengunduhnya sendiri dari sumber resmi.

**Status panduan (30 September 2026).** Rilis terbaru saat ditulis: **Kanboard v1.2.54** (28 Agustus 2026). Langkah dicocokkan dengan dokumentasi resmi (docs.kanboard.org) dan kode sumber resmi v1.2.54. Komunitech **mencoba langsung** Kanboard v1.2.54 dari kode sumber resmi (tag git `v1.2.54`) dengan PHP 8.4 + SQLite di Linux: login, token pribadi, token aplikasi, zona waktu, pembuatan papan/kartu, dan semua perintah skill. **Belum dicoba langsung** oleh Komunitech: image Docker resmi (perintah di bawah mengikuti dokumentasi resmi & `Dockerfile` resminya), Windows/macOS sungguhan. Bila tampilan di komputer Anda berbeda, ikuti tulisan di layar atau hubungi kami.

## Daftar isi
1. Sebelum mulai
2. Pilih cara pasang
3. Jalankan Kanboard (Docker — disarankan)
4. **Pengamanan wajib**
5. Buat akun tim & token API
6. Atur bahasa, zona waktu, dan anggota papan
7. Menyalakan Kanboard setiap hari
8. Cadangan (backup) & pemulihan
9. Update Kanboard
10. Copot pasang
11. Masalah umum

---

## 1. Sebelum mulai
| Kebutuhan | Keterangan |
|---|---|
| Komputer | Windows 10/11, macOS, atau Linux; RAM ≥ 4 GB bila memakai Docker Desktop |
| Waktu | ±20–40 menit (pertama kali) |
| Docker Desktop | Gratis untuk usaha kecil (cek syarat lisensi Docker di docker.com) |
| Python 3.8+ | Untuk skill (python.org; di Windows centang **Add Python to PATH**) |

Istilah: **papan** = satu *project* di Kanboard (mis. "Produksi Konveksi Ayu"). **Kolom** = tahap kerja. **Kartu** = satu pekerjaan/pesanan (*task*). **Token API** = "kata sandi khusus" agar AI bisa membaca/menulis papan tanpa tahu sandi akun Anda.

---

## 2. Pilih cara pasang
| Cara | Cocok untuk | Catatan |
|---|---|---|
| **A. Docker (disarankan)** | Laptop/PC kantor Windows/macOS/Linux | Satu perintah; image resmi `kanboard/kanboard` (Docker Hub, >23 juta unduhan) |
| B. Server web (Apache/Nginx + PHP ≥ 8.1) | Mini PC/VPS Linux | Cara resmi di docs.kanboard.org/v1/admin/installation/ — untuk yang terbiasa server, atau lewat jasa setup |
| C. Coba cepat dengan PHP bawaan | Sekadar mencoba 10 menit | `php -S 127.0.0.1:8080` di folder Kanboard. **Bukan** cara resmi dan **bukan** untuk dipakai sehari-hari |

Unduh **hanya** dari sumber resmi: `github.com/kanboard/kanboard` (halaman Releases) atau image Docker `kanboard/kanboard` (juga `ghcr.io/kanboard/kanboard`). Jangan dari tautan kiriman orang atau situs lain.

---

## 3. Jalankan Kanboard (Docker)
1. Pasang **Docker Desktop** dari docker.com, buka, tunggu sampai statusnya "running".
2. Buka Terminal (macOS/Linux) atau PowerShell (Windows), jalankan **satu baris** ini:
   ```bash
   docker run -d --name kanboard --restart unless-stopped -p 127.0.0.1:8080:80 -v kanboard_data:/var/www/app/data -v kanboard_plugins:/var/www/app/plugins kanboard/kanboard:v1.2.54
   ```
   - `-p 127.0.0.1:8080:80` → Kanboard **hanya bisa dibuka dari komputer ini** di alamat `http://127.0.0.1:8080` (aman; lihat bagian 4).
   - `-v kanboard_data:...` → data (database SQLite, lampiran) disimpan di *volume* bernama `kanboard_data`, **tidak hilang** saat container diperbarui.
   - `v1.2.54` → versi dikunci (disarankan dokumentasi resmi). Ganti ke versi terbaru saat update (bagian 9).
3. Buka browser ke **http://127.0.0.1:8080**. Login awal: **admin / admin**.
- ✅ **Berhasil:** muncul dasbor Kanboard.
- ❌ **"port is already allocated":** port 8080 dipakai program lain → ganti `127.0.0.1:8080:80` menjadi `127.0.0.1:8081:80`, lalu pakai alamat `http://127.0.0.1:8081` (dan beri tahu AI: `atur --url http://127.0.0.1:8081 --ya`).

---

## 4. Pengamanan wajib (±5 menit, sebelum mengisi data usaha)
1. **Ganti sandi admin sekarang juga:** klik avatar (kanan atas) → **Profil saya** → **Ganti password**. Sandi `admin/admin` diketahui semua orang.
2. **Jangan buka Kanboard ke internet** tanpa HTTPS. Perintah di bagian 3 sudah mengikat ke `127.0.0.1` (hanya komputer ini).
3. Ingin dibuka dari komputer lain di kantor? Ubah `-p 127.0.0.1:8080:80` menjadi `-p 8080:80`, lalu **di komputer tempat AI berjalan** daftarkan alamatnya sekali (pemilik yang menjalankan, bukan AI diam-diam):
   ```bash
   python3 scripts/kanboard.py atur --url http://192.168.1.20:8080 --izinkan-host --ya
   ```
   Skill akan memberi PERINGATAN karena `http` tidak terenkripsi — aman hanya di jaringan kantor sendiri.
4. Untuk akses dari internet (VPS), wajib **HTTPS** (mis. lewat reverse proxy dengan sertifikat Let's Encrypt) — skill menolak `http://` ke alamat internet. Ini sebaiknya lewat jasa setup.
5. Aktifkan **Dua faktor otentifikasi** untuk akun admin (Profil saya → Dua faktor otentifikasi). Akun dengan 2FA tetap bisa dipakai skill lewat **token**, bukan sandi.

---

## 5. Buat akun tim & token API
**Peran aplikasi Kanboard** (Pengaturan → Pengguna):
| Peran | Bisa apa (terkait skill) |
|---|---|
| Administrator | Semua. Jangan pakai akun ini untuk AI sehari-hari |
| **Manajer** (*Manager*) | Membuat **papan tim**, mengatur papan miliknya — **disarankan untuk akun AI/pemilik** |
| Pengguna (*User*) | Hanya membuat **papan pribadi** (`buat-papan --pribadi`) dan bekerja di papan tempat ia jadi anggota |

**Token pribadi (disarankan):**
1. Login sebagai akun yang akan dipakai AI (mis. akun Anda sendiri berperan Manajer).
2. Klik avatar → **Profil saya** → menu kiri **API** → **Generate token baru**. Salin token yang tampil.
3. Di **terminal Anda sendiri** (bukan di chat AI), jalankan:
   ```bash
   python3 <folder-skill>/scripts/kanboard.py simpan-kunci
   ```
   (Windows: `python` atau `py`.) Isi nama pengguna Kanboard, lalu tempel token (tidak terlihat saat ditempel). Tersimpan di `~/.komunitech/kanboard-kunci.json` berizin 600.
4. Uji: `python3 <folder-skill>/scripts/kanboard.py cek` → harus muncul **KANBOARD TERHUBUNG**.

**Token aplikasi (hanya bila perlu):** Pengaturan → **API** menampilkan token untuk nama pengguna khusus `jsonrpc`. Token ini **tanpa pemeriksaan hak** (bisa semua papan) — hanya untuk admin yang paham risikonya. Skill tetap tidak punya perintah hapus, tapi token ini jangan dipakai di jadwal otomatis.

> **Jangan pernah menempel token di chat.** Jika terlanjur, buka Profil saya → API → **Hapus token Anda**, lalu buat yang baru.

---

## 6. Atur bahasa, zona waktu, dan anggota papan
1. **Bahasa:** Pengaturan → Pengaturan aplikasi → **Bahasa** → Bahasa Indonesia (tiap pengguna juga bisa mengatur di profilnya).
2. **Zona waktu:** Pengaturan → Pengaturan aplikasi → **Zona waktu** → `Asia/Jakarta` (WIB), `Asia/Makassar` (WITA), atau `Asia/Jayapura` (WIT). Skill tetap menghitung jam jatuh tempo dengan benar walau server memakai UTC (diuji keduanya), tapi tampilan di layar Kanboard lebih mudah dibaca bila zonanya lokal.
3. **Anggota papan** (wajib sebelum menugaskan kartu dengan `--ke`): buka papan → ikon roda **Konfigurasi proyek ini** → **Izin** → tambah pengguna, pilih peran (Anggota/Manajer). Hanya anggota papan yang bisa ditugaskan.
4. **Kolom:** papan dari skill sudah berisi kolom sesuai jenis usaha. Mengubah/menghapus kolom dilakukan manusia di Konfigurasi proyek ini → **Kolom** (skill sengaja tidak menghapus apa pun). Catatan: skill menganggap **kolom paling kanan = beres** (tidak dihitung terlambat/macet).

---

## 7. Menyalakan Kanboard setiap hari
- Docker: opsi `--restart unless-stopped` membuat Kanboard ikut menyala setiap Docker Desktop menyala. Atur Docker Desktop agar **start saat login** (Settings → General).
- Untuk laporan pagi otomatis ke Telegram (lewat OpenClaw), komputer ini harus **menyala saat jadwal** — laptop/mini PC yang selalu menyala atau VPS milik Anda (jasa setup Komunitech tersedia).
- Cek cepat: `docker ps` harus menampilkan container `kanboard` berstatus `Up`.

---

## 8. Cadangan (backup) & pemulihan
**Cara termudah (dari layar):** tidak ada tombol backup bawaan; gunakan cara di bawah.

**Docker (salin database SQLite):**
```bash
docker cp kanboard:/var/www/app/data/db.sqlite ./kanboard-backup-2026-09-30.sqlite
```
Simpan file itu di tempat lain (flashdisk/cloud pribadi). Lakukan minimal **seminggu sekali**. Lampiran file ada di folder `/var/www/app/data/files` (salin dengan `docker cp kanboard:/var/www/app/data/files ./kanboard-files-backup`).

**Pemulihan:** hentikan dulu (`docker stop kanboard`), salin kembali (`docker cp ./kanboard-backup-....sqlite kanboard:/var/www/app/data/db.sqlite`), lalu `docker start kanboard`.

---

## 9. Update Kanboard
1. Baca catatan rilis di halaman Releases GitHub resmi (banyak rilis berisi perbaikan keamanan — sebaiknya update rutin).
2. **Backup dulu** (bagian 8).
3. Jalankan (ganti `v1.2.xx` dengan versi terbaru):
   ```bash
   docker pull kanboard/kanboard:v1.2.xx
   docker stop kanboard && docker rm kanboard
   docker run -d --name kanboard --restart unless-stopped -p 127.0.0.1:8080:80 -v kanboard_data:/var/www/app/data -v kanboard_plugins:/var/www/app/plugins kanboard/kanboard:v1.2.xx
   ```
   Data aman di volume `kanboard_data`. `docker rm kanboard` hanya menghapus container bernama `kanboard`, bukan data.
4. Jalankan `cek` di skill. Versi selain v1.2.54 tetap jalan dengan catatan "belum diuji Komunitech".

---

## 10. Copot pasang
```bash
docker stop kanboard && docker rm kanboard
```
Data tetap ada di volume `kanboard_data`. Hapus data **hanya bila yakin** dan sudah backup: `docker volume rm kanboard_data kanboard_plugins`. Hapus juga file kunci skill `~/.komunitech/kanboard-kunci.json` dan hapus token di Kanboard.

---

## 11. Masalah umum
| Gejala | Penyebab & solusi |
|---|---|
| `GAGAL: Kanboard di http://127.0.0.1:8080 tidak bisa dihubungi` | Kanboard/Docker belum menyala → buka Docker Desktop, `docker start kanboard`; cek alamat di browser |
| `401 ... nama pengguna atau token salah` | Token dihapus/salah salin → buat token baru (bagian 5), `simpan-kunci --ya` |
| `403 Forbidden` | Akun bukan anggota papan itu, **atau** id kartu/papan tidak ada (Kanboard memakai 403 untuk keduanya) → cek `daftar-papan`, minta admin menambahkan akun ke papan |
| `Akun ini tidak boleh membuat papan TIM` | Peran akun = Pengguna biasa → pakai `--pribadi`, atau admin ubah peran menjadi Manajer |
| `Anggota '...' tidak ditemukan di papan ini` | Orang itu belum jadi anggota papan → bagian 6 langkah 3 |
| `Kanboard mengalihkan permintaan` | Alamat kurang tepat (mis. harus `https://`, atau ada subfolder) → salin alamat persis dari browser |
| `Host ... belum ada di daftar host yang diizinkan` | Kanboard di komputer lain → pemilik menjalankan `atur --url ... --izinkan-host --ya` (bagian 4) |
| Jam jatuh tempo di layar selisih beberapa jam | Zona waktu profil pengguna berbeda → samakan di Profil saya / Pengaturan aplikasi (bagian 6) |
