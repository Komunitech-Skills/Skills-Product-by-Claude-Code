# Panduan Pasang InvenTree untuk Usaha Manufaktur, Distribusi & Grosir (bahasa awam)

InvenTree adalah program **gratis dan open-source** (lisensi MIT) untuk mengelola **stok gudang**: daftar barang, lokasi/rak, batch & kedaluwarsa, stock opname, pembelian ke supplier (PO), resep/daftar bahan (BOM), dan perintah produksi. Program ini jalan **di komputer/server Anda sendiri**: data tidak dititipkan ke perusahaan lain dan tidak ada biaya bulanan. Panduan ini menyiapkan InvenTree agar bisa dipakai skill **InvenTree Gudang** (`inventree-gudang`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pasang InvenTree, pengamanan (hanya bisa dibuka dari komputer/jaringan sendiri), mata uang Rupiah & bahasa Indonesia, impor daftar barang dari Excel, akun + token untuk AI, jadwal laporan gudang ke Telegram, dan cadangan otomatis. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan proyek InvenTree; "InvenTree" adalah nama milik pengembangnya.

**Status panduan (29 September 2026, diperbarui setelah uji independen).** Langkah dan nama menu dicocokkan dengan dokumentasi resmi (docs.inventree.org) dan kode sumber InvenTree **1.5.6** (rilis 26 Sep 2026). Komunitech **menjalankan InvenTree 1.5.6 sungguhan** (instalasi manual Linux, Python 3.12 + paket resmi ber-hash, database SQLite, terikat ke `127.0.0.1`) dan menguji semua perintah skill terhadapnya: akun & grup hak akses, token, mata uang IDR, stock opname, terima barang dari PO, BOM. **Jalur Docker (bagian 2) dijalankan penguji independen Komunitech** pada 29 Sep 2026 sampai `docker compose up -d` dan semua perintah skill terhadapnya (port hanya `127.0.0.1`, worker menyala; di sandbox uji, langkah `invoke update` diganti `invoke migrate` + `invoke static` karena batas jaringan sandbox — di komputer biasa pakai `invoke update`). Temuan uji itu (urutan mata uang, sandi akun AI) sudah dimasukkan ke bagian 5 & 6. **Belum dicoba langsung:** Windows/macOS sungguhan. Bila tampilan di komputer Anda berbeda, ikuti tulisan di layar atau hubungi kami.

## Daftar isi
1. Sebelum mulai
2. Pasang dengan Docker (cara resmi yang disarankan)
3. Menyalakan & membuka InvenTree
4. **Pengamanan wajib**
5. Setelan awal untuk usaha Indonesia (Rupiah, bahasa, satuan, stok minimum)
6. Akun khusus AI & token API (baca-saja vs gudang)
7. Menyalakan setiap hari
8. Cadangan (backup)
9. Update InvenTree
10. Copot pasang
11. Masalah umum
12. Lampiran: instalasi manual tanpa Docker (untuk teknisi)

---

## 1. Sebelum mulai
| Kebutuhan | Keterangan |
|---|---|
| Komputer | Mini PC/laptop/PC kantor yang **menyala selama jam kerja** (atau terus, bila ingin laporan pagi otomatis). RAM ≥ 4 GB disarankan (InvenTree + database + worker), ruang kosong ≥ 5 GB |
| Sistem | **Linux (Ubuntu/Debian)** paling mulus. **Windows 10/11**: lewat Docker Desktop (memakai WSL2) — resmi InvenTree mendukung Windows via WSL/Docker. **macOS**: Docker Desktop |
| Program pendukung | **Docker** + Docker Compose (gratis: Docker Engine di Linux, Docker Desktop di Windows/Mac — perhatikan syarat lisensi Docker Desktop untuk perusahaan besar) |
| Waktu | ±30–60 menit (belum termasuk mengisi data barang) |
| Keahlian | Bisa membuka terminal dan menyalin-tempel perintah. Tidak perlu bisa memprogram |

**Kapan InvenTree cocok:** punya bahan baku & produk jadi (BOM), beberapa gudang/rak, barang ber-batch/kedaluwarsa, pembelian rutin ke supplier. **Kapan tidak perlu:** seller online solo dengan puluhan SKU → skill `buku-stok` jauh lebih sederhana (tanpa server).

## 2. Pasang dengan Docker (cara resmi yang disarankan)
Sumber resmi: https://docs.inventree.org/en/latest/start/docker_install/ . InvenTree terdiri dari 5 "kotak" (container): server InvenTree, worker (pekerja latar belakang), database PostgreSQL, cache Redis, dan Caddy (pintu web). Semuanya image resmi (`inventree/inventree`, `postgres:17`, `redis:7-alpine`, `caddy:alpine`) — Komunitech membaca `docker-compose.yml` resmi versi 1.5.6: tidak ada skrip `curl | bash`, dan hanya Caddy yang membuka port ke luar kotak.

1. Buat folder, mis. `inventree` di folder rumah Anda, lalu unduh 3 file resmi **versi 1.5.6** ke folder itu (klik kanan → simpan, atau pakai perintah):
   ```bash
   mkdir -p ~/inventree && cd ~/inventree
   curl -fsSL -o docker-compose.yml https://raw.githubusercontent.com/inventree/InvenTree/1.5.6/contrib/container/docker-compose.yml
   curl -fsSL -o .env https://raw.githubusercontent.com/inventree/InvenTree/1.5.6/contrib/container/.env
   curl -fsSL -o Caddyfile https://raw.githubusercontent.com/inventree/InvenTree/1.5.6/contrib/container/Caddyfile
   ```
   (Perintah ini hanya **mengunduh file teks**, tidak menjalankan apa pun. Buka dan baca dulu bila ingin.)
2. Buka file `.env` dengan editor teks (Linux/Mac: `nano .env`, simpan dengan Ctrl+O lalu Enter, keluar Ctrl+X; Windows: klik kanan → Buka dengan → Notepad. File berawalan titik mungkin tersembunyi — aktifkan "tampilkan file tersembunyi"), ubah baris berikut (lihat juga bagian 4):
   ```
   INVENTREE_TAG=1.5.6
   INVENTREE_SITE_URL="http://localhost"
   INVENTREE_EXT_VOLUME=./inventree-data
   INVENTREE_DB_PASSWORD=<ganti-dengan-sandi-panjang-acak>
   INVENTREE_HTTP_PORT=127.0.0.1:80
   INVENTREE_HTTPS_PORT=127.0.0.1:443
   INVENTREE_PLUGINS_ENABLED=False
   ```
   (Dua baris `INVENTREE_HTTP_PORT`/`HTTPS_PORT` aslinya diawali `#`; hapus tanda `#`-nya.)
3. Siapkan database (sekali saja; **butuh internet**, bisa **5–15 menit** karena mengunduh & memasang komponen — biarkan sampai selesai):
   ```bash
   docker compose run --rm inventree-server invoke update
   ```
4. Buat akun admin (isi nama pengguna, email, sandi kuat — **sandi tidak terlihat saat diketik**, itu normal; ketik lalu Enter, lalu ulangi):
   ```bash
   docker compose run --rm inventree-server invoke superuser
   ```
5. Nyalakan:
   ```bash
   docker compose up -d
   ```

## 3. Menyalakan & membuka InvenTree
- Buka browser di komputer yang sama: **http://localhost** → login dengan akun admin.
- Cek dari AI: "Cek InvenTree saya sudah nyambung belum?" (skill memakai alamat `http://localhost` secara bawaan).
- Status kotak-kotak: `docker compose ps` (semua harus `running`/`healthy`, termasuk **inventree-worker**).

## 4. Pengamanan wajib (±5 menit, sebelum mengisi data usaha)
| Langkah | Kenapa |
|---|---|
| `INVENTREE_HTTP_PORT=127.0.0.1:80` & `INVENTREE_HTTPS_PORT=127.0.0.1:443` di `.env` | Bawaan resmi membuka port 80/443 ke **semua jaringan** (termasuk Wi-Fi tamu / internet bila router meneruskan). Dengan `127.0.0.1`, InvenTree hanya bisa dibuka dari komputer itu sendiri |
| Ganti `INVENTREE_DB_PASSWORD` | Sandi bawaan `pgpassword` sama untuk semua orang |
| `INVENTREE_PLUGINS_ENABLED=False` | Plugin = kode tambahan yang dijalankan server; matikan kecuali benar-benar perlu dan dari sumber tepercaya |
| Jangan isi `INVENTREE_ADMIN_PASSWORD` di `.env` (atau hapus setelah dipakai) | Sandi admin tidak boleh tersimpan di file teks |
| Jangan pernah meneruskan port (port forwarding) router ke InvenTree | Data stok & harga beli adalah rahasia usaha |
| Butuh dibuka dari HP/komputer lain di kantor? | Pakai jasa setup Komunitech (HTTPS di jaringan kantor/VPN). Skill hanya mau menghubungi alamat selain komputer sendiri bila Anda menegaskan `--izinkan-jarak-jauh`, dan alamat internet wajib HTTPS |

## 5. Setelan awal untuk usaha Indonesia
Semua lewat **Settings** (ikon roda/menu profil kanan atas) — nama menu sesuai InvenTree 1.5.6.
1. **Rupiah (wajib bila mencatat harga beli)** — System Settings → **Pricing**, **urutannya penting**:
   1. Isi dulu *Supported Currencies* = `IDR,USD` → simpan.
   2. Baru ubah *Default Currency* = `IDR` → simpan.
   (Bila dibalik, InvenTree 1.5.6 menolak dengan "Chosen value is not a valid option" karena IDR belum ada di daftar — diuji penguji Komunitech. Bawaan InvenTree tidak memuat IDR; tanpa langkah ini pemasok ber-mata uang IDR **ditolak**.)
2. **Bahasa Indonesia:** User Settings → **Account** (panel tema/tampilan) → *Language* → *Indonesian* (terjemahan buatan komunitas, sebagian mungkin masih Inggris). Panduan & skill ini menyebut nama menu versi Inggris.
3. **Satuan:** isi kolom *Units* barang dengan satuan standar (`kg`, `g`, `L`, `m`). Satuan lokal seperti `pcs`, `sak`, `dus`, `rim` → tambahkan dulu di Admin Center → **Custom Units**, atau kosongkan (dianggap "buah").
4. **Struktur:** buat **Stock Locations** (mis. `Gudang Utama` → `Rak A`, `Rak B`; `Ruang Produksi`; `Toko Depan`) dan **Part Categories** (mis. Bahan Baku, Kemasan, Produk Jadi).
5. **Stok minimum:** di tiap barang isi **Minimum Stock** — tanpa ini, laporan "stok menipis" tidak bisa memeriksa barang tersebut.
6. **Produk yang Anda buat sendiri:** centang **Assembly** lalu isi tab **Bill of Materials** (bahan per 1 unit, mis. singkong 0,3 kg per bungkus).
7. **Data awal dari Excel:** Admin Center → **Data Import** (unggah CSV/XLSX daftar barang), atau pakai jasa setup Komunitech.

## 6. Akun khusus AI & token API
Jangan berikan token akun admin ke AI. Buat dua grup dan dua akun:

**a. Grup** — Admin Center → **Users / Access** → **Groups** → Add, lalu atur *Roles*:
| Grup | Role yang dicentang | Dipakai untuk |
|---|---|---|
| `Agen Baca` | **View** pada: Part Categories, Parts, Bills of Material, Stock Locations, Stock Items, Build Orders, Purchase Orders | Chat harian & **jadwal laporan otomatis** |
| `Agen Gudang` | Semua View di atas **+ Add & Change** pada **Stock Items** dan **Purchase Orders** (jangan Delete) | Stock opname & terima barang (selalu lewat pratinjau + "ya") |

**b. Akun khusus AI (hak minimal)** — langkah dilakukan akun admin (superuser) di tampilan web InvenTree 1.5.6:
1. Admin Center → **Users / Access** → tabel **Users** → tombol **+ (Add User)** → isi *Username* `agen-baca` (nama depan/email boleh diisi "Bot AI" / email kantor). **Jangan** centang *Staff*/*Superuser*. Simpan. (Form ini memang **tidak meminta sandi**.)
2. Masih di tabel Users, klik menu **⋮** (titik tiga) di baris `agen-baca` → **Change Password** → isi sandi panjang acak (simpan di pengelola sandi) → Submit. Menu ini hanya muncul untuk akun superuser. Bila sandi dianggap lemah, InvenTree meminta centang *override warning* — lebih baik pakai sandi yang lebih kuat.
3. Klik baris `agen-baca` (atau ⋮ → Edit) → buka bagian **Groups** → pindahkan **hanya** grup `Agen Baca` ke daftar grup terpilih → simpan (muncul "Groups updated").
4. Ulangi 1–3 untuk `agen-gudang` dengan grup `Agen Gudang` **saja**.

**c. Token (dibuat oleh akun AI itu sendiri)** — token selalu dibuat oleh pemiliknya; panel *Tokens* di Admin Center hanya untuk melihat/mencabut.
1. Log out dari akun admin (menu profil kanan atas → Logout), lalu login sebagai `agen-baca` dengan sandi dari langkah b.2.
2. Menu profil → **User Settings → Security → Access Tokens → + (Generate Token)** → beri nama, mis. `openclaw-laptop-gudang` → Submit.
3. Token diawali `inv-` dan **hanya tampil sekali** — langsung jalankan langkah d (tempel ke `simpan-kunci`), jangan disimpan di chat/catatan. Berlaku **1 tahun** (bawaan), setelah itu buat baru.
4. Logout, login sebagai `agen-gudang`, ulangi 2–3 untuk token gudang. Terakhir login kembali sebagai admin bila perlu.
5. Token bocor/perangkat hilang? Admin Center → Users / Access → **Tokens** → cabut (revoke) token itu, lalu buat baru.

**d. Simpan token** di terminal Anda sendiri (bukan di chat):
```bash
python3 ~/.openclaw/skills/inventree-gudang/scripts/inventree.py simpan-kunci
python3 ~/.openclaw/skills/inventree-gudang/scripts/inventree.py simpan-kunci --kunci-file ~/.komunitech/inventree-kunci-gudang.txt
```
Yang pertama = token `agen-baca` (dipakai bawaan). Yang kedua = token `agen-gudang`; minta AI memakai `--kunci-file ~/.komunitech/inventree-kunci-gudang.txt` saat opname/terima barang. Windows: `python` atau `py`.

**e. Periksa:** "Cek InvenTree saya" → AI menampilkan akun & hak (lihat barang/stok/…/opname/terima barang: YA/tidak).

> **Catatan dari uji Komunitech:** perubahan hak grup diterapkan InvenTree lewat **worker** (pekerja latar belakang). Bila `cek` sudah menunjukkan "opname (tulis): YA" tetapi opname tetap ditolak **403**, pastikan kotak `inventree-worker` menyala (`docker compose ps`), tunggu ±1 menit, lalu simpan ulang grupnya.

## 7. Menyalakan setiap hari
Docker menyalakan ulang InvenTree otomatis setelah komputer restart (`restart: unless-stopped`), selama Docker sendiri ikut menyala saat login (Docker Desktop: Settings → *Start Docker Desktop when you sign in*). Manual: `cd ~/inventree && docker compose up -d`. Mematikan: `docker compose down` (data aman).

## 8. Cadangan (backup)
Semua data ada di folder `inventree-data` (di sebelah `docker-compose.yml`).
- Cara paling sederhana: `docker compose down`, salin **seluruh folder `~/inventree`** ke flashdisk/drive lain, lalu `docker compose up -d`. Lakukan minimal mingguan dan sebelum update.
- Ekspor data resmi (JSON): `docker compose run --rm inventree-server invoke export-records -f /home/inventree/data/data.json` → file muncul di `inventree-data/data.json`.
- Uji pemulihan sesekali di komputer lain (jasa setup Komunitech bisa membantu).

## 9. Update InvenTree
Backup dulu (bagian 8). Ubah `INVENTREE_TAG` di `.env` ke versi baru, lalu:
```bash
docker compose down
docker compose pull
docker compose run --rm inventree-server invoke update
docker compose up -d
```
Skill diuji dengan 1.5.6; versi lain tetap jalan tetapi `cek` akan menulis "belum diuji Komunitech" — cocokkan angka penting di layar InvenTree setelah update.

## 10. Copot pasang
`cd ~/inventree && docker compose down`, lalu hapus folder `~/inventree` (**semua data ikut terhapus** — backup dulu). Hapus juga `~/.komunitech/inventree-kunci*.txt`.

## 11. Masalah umum
| Gejala | Penyebab & solusi |
|---|---|
| Browser `http://localhost` tidak terbuka | `docker compose ps` — ada yang tidak `running`? Lihat `docker compose logs inventree-server`. Port 80 dipakai program lain → ganti `INVENTREE_HTTP_PORT=127.0.0.1:8080`, `INVENTREE_SITE_URL="http://localhost:8080"`, lalu `INVENTREE_API_HOST=http://localhost:8080` untuk skill |
| Skill: "Tidak bisa menghubungi InvenTree" | InvenTree mati, atau alamat beda dari `http://localhost` → set ENV `INVENTREE_API_HOST` |
| Skill: "401" | Token salah/kedaluwarsa/dicabut → buat token baru (bagian 6c), `simpan-kunci --ya` |
| Skill: "403" | Akun tidak punya hak aksi itu (mis. akun baca mencoba opname) → pakai token gudang, atau atur grup (bagian 6) |
| Pemasok/harga ditolak "IDR is not a valid choice" | Mata uang belum diatur (bagian 5.1) |
| Stok menipis selalu kosong | Barang belum diisi *Minimum Stock* (bagian 5.5) |
| `bom`: "bukan produk rakitan" | Centang *Assembly* pada produk & isi BOM (bagian 5.6) |
| Skill: "mengalihkan (HTTP 30x)" | Alamat yang dipakai skill diarahkan ke alamat lain (mis. `http://` → `https://`, atau port lain). Demi keamanan token skill tidak mengikuti pengalihan → pakai alamat tujuan akhir (yang tampil di address bar browser) sebagai `INVENTREE_API_HOST` |
| Skill memakai proxy kantor? | Tidak untuk alamat komputer ini/jaringan kantor — setelan `HTTP_PROXY`/`HTTPS_PROXY` sengaja diabaikan agar token tidak lewat proxy |
| Opname "BERHENTI: stok BERUBAH" | Ada barang masuk/keluar setelah lembar dicetak → buat lembar baru, hitung ulang item itu |

## 12. Lampiran: instalasi manual tanpa Docker (untuk teknisi)
Cara ini yang **dijalankan Komunitech** untuk menguji skill (Linux, 29 Sep 2026). Resmi didokumentasikan di https://docs.inventree.org/en/latest/start/install/ ; membutuhkan **Python ≥ 3.12**.
```bash
git clone --depth 1 --branch 1.5.6 https://github.com/inventree/InvenTree.git inventree-src
python3.12 -m venv venv
./venv/bin/pip install --require-hashes -r inventree-src/src/backend/requirements.txt
# set variabel lingkungan: INVENTREE_DB_ENGINE=sqlite3, INVENTREE_DB_NAME=<path>/inventree.sqlite3,
# INVENTREE_MEDIA_ROOT, INVENTREE_STATIC_ROOT, INVENTREE_BACKUP_DIR, INVENTREE_SECRET_KEY_FILE,
# INVENTREE_CONFIG_FILE, INVENTREE_SITE_URL=http://127.0.0.1:8000, INVENTREE_PLUGINS_ENABLED=False
cd inventree-src/src/backend/InvenTree
../../../../venv/bin/python manage.py migrate
../../../../venv/bin/python manage.py createsuperuser
../../../../venv/bin/gunicorn InvenTree.wsgi -b 127.0.0.1:8000
```
Catatan: cara di atas menghasilkan API yang lengkap (cukup untuk skill), tetapi **tampilan web** perlu langkah tambahan resmi (`invoke frontend-download`, `invoke static`) dan **worker** (`invoke worker`) — belum diuji Komunitech. Untuk pemakaian sehari-hari, gunakan Docker (bagian 2) atau jasa setup. Skill: `INVENTREE_API_HOST=http://127.0.0.1:8000`.
