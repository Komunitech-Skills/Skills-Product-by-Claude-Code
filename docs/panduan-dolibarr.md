# Panduan Pasang Dolibarr untuk UMKM (bahasa awam)

Dolibarr adalah program **gratis dan open-source** (lisensi GPL-3.0) untuk pelanggan, invoice, produk, stok, kasir, dan lain-lain. Program ini jalan **di komputer Anda sendiri**: data tidak dititipkan ke perusahaan lain dan tidak ada biaya bulanan. Panduan ini menyiapkan Dolibarr agar bisa dipakai skill **Dolibarr Usaha** (`dolibarr-usaha`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pemasangan DoliWamp, pengaturan Indonesia (IDR, PPN), user API aman, cadangan otomatis, dan jadwal laporan ke Telegram. Hubungi admin komunitech.com.

> Komunitech tidak berafiliasi dengan proyek Dolibarr; Dolibarr adalah merek milik pemiliknya.

**Status panduan (24 September 2026; bagian 2.4 ditambahkan 25 September 2026):** langkah dan nama menu dicocokkan dengan sumber resmi (wiki.dolibarr.org, SourceForge, kode sumber Dolibarr 22.0.4 & 24.0.1). Pengaturan Indonesia (IDR, id_ID, tarif PPN), modul, user API berhak minimal, kunci API (termasuk kunci terenkripsi), serta cadangan & pemulihan database lewat mysqldump **dicoba langsung** pada Dolibarr asli 22.0.4 & 24.0.1 di Linux (lewat database/CLI, bukan klik di layar). Halaman Backup di layar Dolibarr dicocokkan dengan kode sumbernya, belum diklik langsung. **Installer DoliWamp di Windows belum dicoba Komunitech secara langsung**; bila tampilan Anda berbeda, ikuti tulisan di layar dan hubungi kami.

## Daftar isi
1. Sebelum mulai
2. Pasang di Windows (DoliWamp) — **disarankan** (termasuk **2.4 Pengamanan wajib**)
3. Pasang di Linux / macOS (lebih sulit)
4. Pengaturan awal Indonesia
5. Aktifkan modul
6. Buat user khusus API ("baca dulu")
7. Buat & simpan kunci API
8. Menyalakan Dolibarr setiap hari
9. Cadangan (backup) & pemulihan
10. Keamanan
11. Masalah umum

---

## 1. Sebelum mulai
| Kebutuhan | Keterangan |
|---|---|
| Komputer | Windows 10/11 64-bit (paling mudah). RAM ≥ 4 GB, ruang kosong ≥ 2 GB |
| Waktu | ±30–60 menit untuk Windows; ±1–3 jam untuk Linux/macOS |
| Hak | Akun Windows **administrator** (untuk memasang) |
| Python 3.8+ | Untuk skill (gratis di python.org; saat memasang di Windows centang **Add Python to PATH**) |

Istilah: **Dolibarr** = programnya. **DoliWamp** = paket Windows yang sekaligus memasang Dolibarr + server web (Apache) + database (MariaDB) + PHP. **Kunci API** = "kata sandi khusus" agar AI bisa membaca data Dolibarr.

---

## 2. Pasang di Windows (DoliWamp) — disarankan
Tingkat kesulitan: **mudah–sedang** (seperti memasang aplikasi biasa, lalu mengisi formulir di browser).

### 2.1 Unduh dari sumber resmi
1. Buka https://sourceforge.net/projects/dolibarr/files/ → folder **"Dolibarr installer for Windows (DoliWamp)"** → pilih versi teratas (saat panduan ditulis: **22.0.4**, 9 Jan 2026) → unduh file `DoliWamp-…exe`.
2. **Jangan** mengunduh dari situs lain (bisa berisi virus).
- ✅ **Cek berhasil:** file `DoliWamp-22.0.4.exe` (atau lebih baru) ada di folder Unduhan.
- ❌ **Kalau gagal:** unduhan lambat/terputus → coba lagi, atau pilih server (mirror) lain di halaman SourceForge.

> Versi Dolibarr terbaru adalah 24.0.1, tetapi paket DoliWamp resmi terbaru masih 22.0.4. Skill ini sudah diuji dengan keduanya.

### 2.2 Jalankan installer
1. Klik kanan file → **Run as administrator** (Jalankan sebagai administrator). Jika Windows SmartScreen muncul: **More info → Run anyway** hanya bila file memang dari SourceForge Dolibarr.
2. Ikuti layar: bahasa → setuju lisensi → folder (biarkan `C:\dolibarr`).
3. Layar **port & sandi**: biarkan port Apache **80** dan MySQL **3306**. **Ganti sandi database** dari `changeme` menjadi sandi kuat, lalu **catat di kertas/brankas sandi**.
4. Jika Windows Firewall bertanya "izinkan akses jaringan" untuk Apache (`httpd.exe`) atau MariaDB (`mysqld.exe`): **jangan centang Public**, klik **Cancel/Batal**. Dolibarr tetap bisa dibuka dari komputer ini.
5. Selesai → installer membuka browser ke `http://localhost/dolibarr`.
- ✅ **Cek berhasil:** browser menampilkan halaman instalasi Dolibarr (pilih bahasa).
- ❌ **Kalau gagal:**
  - "port 80 sudah dipakai" → program lain (IIS, Skype lama, XAMPP) memakai port itu. Ulangi installer dan isi port Apache **8080**; alamat Dolibarr menjadi `http://localhost:8080/dolibarr`.
  - Browser "tidak dapat dijangkau" → buka menu **Start → Dolibarr → Tools → Start DoliWamp server**, tunggu 30 detik, muat ulang.
  - Antivirus memblokir → izinkan folder `C:\dolibarr` (hanya bila file dari sumber resmi).

### 2.3 Wizard instalasi di browser
1. Pilih bahasa → **Next**. Halaman pemeriksaan harus hijau/oke.
2. Konfigurasi: biasanya sudah terisi otomatis oleh DoliWamp. Bila diminta sandi database, isi sandi dari langkah 2.2.3.
3. Buat **akun admin Dolibarr**: login mis. `admin`, sandi kuat (≥ 12 karakter). Catat.
4. Selesai → klik tautan ke halaman login → masuk dengan akun admin.
- ✅ **Cek berhasil:** tampil halaman **Home/Beranda** Dolibarr.
- ❌ **Kalau gagal:** "Access denied for user" → sandi database salah; ulangi dengan sandi dari 2.2.3. Halaman minta "install.lock" → instalasi sudah selesai, buka `http://localhost/dolibarr` biasa.

### 2.4 Pengamanan wajib (±10 menit, sebelum mengisi data usaha)
**Kenapa wajib?** DoliWamp memasang "server" kecil di komputer Anda. Dengan pengaturan bawaan, orang lain yang tersambung ke Wi-Fi yang sama (toko, kantor, kafe) bisa mencoba membuka Dolibarr Anda. Berisi data pelanggan dan uang, jadi kuncilah seperti brankas. Tiga langkah ini **tidak boleh dilewati**:

**Langkah 1 — Ganti sandi database bawaan.**
- Sandi bawaan DoliWamp (`changeme`) diketahui semua orang. Paling mudah diganti **saat memasang** (2.2 langkah 3).
- Sandi yang kuat: minimal 12 karakter, campuran huruf dan angka, **bukan** nama toko atau tanggal lahir. Catat di brankas sandi atau kertas yang disimpan aman.
- Sudah terlanjur memakai `changeme`?
  - **Belum ada data penting:** cara paling aman adalah copot pasang DoliWamp lalu pasang ulang dengan sandi baru.
  - **Sudah ada data:** jangan mencoba sendiri. Sandi harus diganti di database **dan** di file pengaturan Dolibarr sekaligus; bila hanya satu yang diganti, Dolibarr tidak bisa dibuka. Buat cadangan dulu (bagian 9), lalu minta teknisi atau **jasa setup Komunitech**.

**Langkah 2 — Pastikan Dolibarr hanya bisa dibuka dari komputer ini.**
- Selalu buka Dolibarr lewat `http://localhost/dolibarr`. *localhost* artinya "komputer ini sendiri".
- Windows Firewall: jangan izinkan Apache (`httpd.exe`) dan MariaDB (`mysqld.exe`) (2.2 langkah 4). Terlanjur klik **Allow/Izinkan**? Buka **Start** → ketik **"Allow an app through Windows Firewall"** (Izinkan aplikasi melalui Windows Firewall) → **Change settings** (Ubah pengaturan) → cari baris bernama Apache/httpd dan MariaDB/mysqld → **hapus centang Private dan Public** → **OK**.
- ✅ **Cek berhasil (uji dengan HP, 2 menit):**
  1. Di komputer Dolibarr: **Start** → ketik `cmd` → Enter → ketik `ipconfig` → Enter → catat angka **IPv4 Address** (mis. `192.168.1.10`).
  2. Sambungkan HP ke **Wi-Fi yang sama**, buka browser HP, ketik `http://192.168.1.10/dolibarr` (pakai angka Anda).
  3. **Benar bila HP TIDAK bisa membuka** (lama berputar lalu gagal). Dolibarr di komputer tetap terbuka lewat `localhost`.
- ❌ **Kalau HP bisa membuka halaman login Dolibarr:** komputer Anda masih terbuka ke jaringan. Ulangi pengaturan firewall di atas, lalu uji lagi. Masih terbuka? Hentikan dulu pemakaian di Wi-Fi umum dan minta bantuan teknisi/jasa setup.
- Pengamanan yang lebih kuat (teknis): membatasi Apache dan MariaDB agar hanya melayani `127.0.0.1` (alamat "komputer ini"). Ini mengubah file pengaturan server, jadi serahkan ke teknisi atau jasa setup Komunitech.

**Langkah 3 — Jangan buka Dolibarr ke internet.**
- Jangan atur *port forwarding*, *virtual server*, atau *DMZ* di router.
- Jangan pakai aplikasi "tunnel" (mis. ngrok, Cloudflare Tunnel) atau aplikasi remote untuk membuka Dolibarr dari luar.
- Ingin membuka dari rumah/cabang? Itu butuh HTTPS dan pengamanan tambahan. Jangan dikerjakan sendiri; konsultasikan ke jasa setup Komunitech.

Catatan jujur: langkah Windows di atas disusun dari dokumentasi Windows dan DoliWamp, **belum dicoba langsung** oleh Komunitech di Windows. Bila nama menu di komputer Anda berbeda, ikuti yang paling mirip atau minta bantuan. **Jasa setup berbayar Komunitech** dapat mengerjakan seluruh langkah pengamanan ini, termasuk uji dari HP, bersama Anda.

---

## 3. Pasang di Linux / macOS (lebih sulit)
Jujur: tidak ada paket "sekali klik" yang setara DoliWamp untuk Mac. Jika Anda tidak terbiasa dengan Terminal, pilih salah satu: **(a)** pakai komputer/mini PC Windows khusus toko, atau **(b)** jasa setup Komunitech.

### Linux (Ubuntu/Debian) — sedang
Paket resmi **DoliDeb** tersedia di SourceForge (folder "Dolibarr installer for Debian-Ubuntu (DoliDeb)"; diperbarui 6 Sep 2026).
1. Unduh file `.deb` terbaru dari folder itu.
2. Terminal: `sudo apt install ./dolibarr_*.deb` (apt memasang Apache/PHP yang dibutuhkan). Jika belum ada database: `sudo apt install mariadb-server`.
3. Buka `http://localhost/dolibarr` dan ikuti wizard seperti 2.3 (buat database & user database saat diminta).
- ✅ **Cek berhasil:** halaman login Dolibarr terbuka.
- ❌ **Kalau gagal:** alamat berbeda (mis. `http://localhost/dolibarr/htdocs`) → pakai alamat yang terbuka, lalu atur `DOLIBARR_URL` sesuai alamat itu (bagian 7).

**Linux & macOS juga wajib bagian 2.4:** sandi database kuat, Dolibarr dibuka lewat `localhost`, dan diuji dari HP di Wi-Fi yang sama (alamat IP komputer: Linux `hostname -I`, macOS System Settings → Wi-Fi → Details). Di Ubuntu, firewall bawaan diaktifkan dengan `sudo ufw enable` (menolak sambungan masuk). Bila komputer diatur jarak jauh oleh teknisi, minta teknisi yang melakukannya agar aksesnya tidak terputus.

### macOS — sulit
Pilihan realistis: **Docker Desktop** + image resmi `dolibarr/dolibarr` (https://hub.docker.com/r/dolibarr/dolibarr), atau MAMP + paket zip Dolibarr (manual). Keduanya butuh pengetahuan teknis (volume data, port, pembaruan). Alamat biasanya `http://localhost:8080` (tanpa `/dolibarr`) → atur `DOLIBARR_URL=http://localhost:8080`. Paket DoliMamp lama sudah tidak dirawat.

---

## 4. Pengaturan awal Indonesia
Semua menu di bawah ada di **Home → Setup (Pengaturan)**. Terjemahan Indonesia di Dolibarr belum lengkap, jadi nama menu ditulis **Indonesia / Inggris**.

### 4.1 Perusahaan & mata uang
**Pengaturan → Perusahaan/Organisasi** (Company/Organization): isi nama usaha, alamat, **Negara: Indonesia**, **Mata Uang (Main currency): Rupiah Indonesia (IDR)**. Simpan.
- ✅ Cek: di halaman yang sama tertulis Indonesia & IDR.
- ❌ Kalau IDR tidak ada di daftar: **Pengaturan → Kamus (Dictionaries) → Mata uang** → aktifkan IDR.

### 4.2 Bahasa
**Pengaturan → Tampakan Display (Display)** → **Bahasa default: Indonesia (id_ID)** → Simpan.
- ✅ Cek: menu berubah ke Bahasa Indonesia (sebagian masih Inggris; itu normal).

### 4.3 PPN (12% × DPP 11/12)
Dolibarr **tidak punya** tarif PPN Indonesia bawaan dan **tidak punya** fitur "DPP nilai lain 11/12". Cara yang dipakai skill: tarif efektif **11%** (= 12% × 11/12) untuk barang/jasa umum.
1. Jika usaha Anda **PKP**: di **Perusahaan/Organisasi** centang **Pajak penjualan digunakan** (Sales tax used). Bukan PKP → jangan dicentang, dan buat invoice dengan pilihan "tanpa PPN".
2. **Pengaturan → Kamus (Dictionaries) → Tarif PPN atau Tarif Pajak Penjualan** (VAT Rates) → pilih negara **Indonesia**, tambahkan 3 baris:
   | Tarif | Catatan |
   |---|---|
   | 11 | PPN 12% × DPP 11/12 (umum) |
   | 12 | PPN 12% penuh (barang mewah) |
   | 0 | Tidak kena PPN / dibebaskan |
3. Saat membuat produk, pilih tarif **11** untuk barang/jasa umum.
4. (Opsional) **Pengaturan → Batas dan akurasi** (Limits and accuracy): "Maks. desimal untuk harga total" = **0** agar Dolibarr tidak menyimpan sen. Catatan: Dolibarr tetap membulatkan PPN **per baris ke terdekat**, sedangkan standar Komunitech membulatkan PPN total **ke bawah**; selisih Rp 0–beberapa rupiah akan dilaporkan skill.
- ✅ Cek: buat produk uji, di kolom PPN muncul pilihan 11/12/0.
- ❌ Kalau tarif tidak muncul: pastikan negara perusahaan = Indonesia dan baris kamus berstatus aktif.

> **Penting:** cetakan invoice Dolibarr akan menulis "PPN 11%". Faktur pajak resmi (menyebut PPN 12% dan DPP nilai lain) **tetap dibuat di Coretax DJP**. Dasar: UU HPP & PMK 131/2024, per 24 September 2026. Ini bukan nasihat pajak; tanyakan kasus khusus ke DJP (Kring Pajak 1500200) atau konsultan.

---

## 5. Aktifkan modul
**Pengaturan → Modul / Aplikasi** (Modules/Applications). Klik tombol aktif (ikon saklar) pada:
| Modul (Indonesia / Inggris) | Untuk |
|---|---|
| Pihak ketiga / Third Parties | pelanggan & pemasok |
| Nota / Invoices | invoice pelanggan |
| Produk / Products | daftar barang & jasa |
| Stok / Stocks | jumlah stok & gudang |
| Bank & Uang Tunai / Banks & Cash | mencatat pembayaran (dipakai manusia) |
| **API / Layanan Web (server REST)** / API / Web services (REST server) | **wajib** untuk skill |
- ✅ **Cek berhasil:** buka `http://localhost/dolibarr/api/index.php/status` di browser. Muncul tulisan JSON berisi `"code": 401` (artinya API hidup dan meminta kunci).
- ❌ **Kalau gagal:** muncul "Modul **Api** harus diaktifkan" → modul API belum aktif; ulangi. Halaman "Not Found" → alamat salah (cek port, mis. `localhost:8080`).

---

## 6. Buat user khusus API ("baca dulu")
Jangan memakai akun **admin** untuk AI. Buat akun terpisah dengan hak sekecil mungkin. Disarankan **dua** user:

| User | Dipakai untuk | Kunci disimpan di |
|---|---|---|
| `api_baca` (**baca saja**) | laporan harian terjadwal, piutang, stok, cari pelanggan | file kunci default (`simpan-kunci`) — dipakai jadwal OpenClaw |
| `api_draf` (opsional, belakangan) | tambah pelanggan & membuat **draf** invoice | file kunci terpisah, dipakai hanya saat Anda sendiri meminta (`--kunci-file`) |

### 6.1 User baca-saja (wajib)
1. **Pengguna & Grup (Users & Groups) → Pengguna Baru (New user)**: nama "API Baca", login `api_baca`, **Administrator: Tidak**, sandi acak panjang (tidak perlu diingat). Simpan.
2. Buka user itu → tab **Izin (Permissions)** → beri **hanya** hak berikut (klik tanda tambah di barisnya):
   | Modul | Hak | Wajib? |
   |---|---|---|
   | Pihak ketiga | Baca pihak ketiga yang tertaut ke pengguna (121) | ya |
   | Pihak ketiga | Perluas akses ke semua pihak ketiga (262) | ya (tanpa ini daftar pelanggan kosong) |
   | Nota | Baca faktur pelanggan (dan pembayaran) (11) | ya |
   | Produk | Membaca Produk (31) | ya |
   | Stok | Baca gudang dan stok (1001) | ya, bila modul Stok dipakai |
3. (Opsional) Hak **Buat/ubah pengguna sendiri (342)** membuat perintah `cek` bisa menampilkan daftar hak dan memberi peringatan hak berisiko. **Tanpa hak 342, `cek` tidak bisa melihat daftar hak**, jadi peringatan "hak invoice juga bisa memvalidasi" (6.2) tidak muncul; `cek` tetap berjalan (menguji baca satu per satu). "Modul Stok mati" vs "hak stok kurang" dibedakan lewat daftar API Dolibarr, tidak butuh 342 (kecuali Explorer API dimatikan).

### 6.2 User pembuat draf (opsional, setelah 1–2 minggu yakin)
Buat user kedua `api_draf` dengan hak 6.1 **ditambah** **Buat/modifikasi pihak ketiga (122)** dan **Membuat/Merubah Nota Pelanggan (12)**. Simpan kuncinya ke file lain, mis. `python3 dolibarr.py simpan-kunci --kunci-file ~/.komunitech/dolibarr-kunci-draf.txt` (script menampilkan path lengkap file yang akan ditulis dan **menolak menimpa** file kunci yang sudah ada kecuali ditambah `--ya`), dan minta AI memakai `--kunci-file` itu hanya saat membuat pelanggan/draf.

> ⚠️ **Jujur soal risiko (diuji di Dolibarr 24.0.1, 25 Sep 2026):** di Dolibarr, hak **"Membuat/Merubah Nota Pelanggan" (12)** lewat API **juga cukup untuk MEMVALIDASI invoice, mengembalikannya ke draf, dan MENANDAI LUNAS/BELUM LUNAS**, serta mengubah/menghapus baris invoice. Hak "Validasi faktur" (14) hanya berlaku di layar Dolibarr bila izin lanjutan aktif, **tidak** di API. Yang tetap ditolak untuk hak 12 saja: **mencatat pembayaran** (butuh hak 16) dan **menghapus invoice** (butuh hak 19). Hak 122 juga bisa **mengubah** data pelanggan yang sudah ada.
> Skill Dolibarr Usaha **tidak punya** perintah validasi, tandai lunas, bayar, ubah, atau hapus, dan agent dilarang memanggil API di luar script. Tetapi siapa pun yang memegang kunci `api_draf` secara teknis **mampu** melakukannya. Karena itu: jangan pakai kunci `api_draf` untuk jadwal otomatis, jangan bagikan, dan buat kunci baru bila curiga bocor.
> Sumber: `htdocs/compta/facture/class/api_invoices.class.php` (24.0.1) — `validate`, `settodraft`, `settopaid`, `settounpaid` memeriksa `hasRight('facture','creer')`; `payments` memeriksa `paiement`; hapus memeriksa `supprimer`.

### 6.3 Jangan pernah berikan ke user API
Terbitkan pembayaran (16), Hapus (faktur 19 / pihak ketiga 125 / produk 34), Buat/ubah produk (32), Pergerakan stok (1005), Pengguna & grup (251–256), dan jangan jadikan Administrator.

- ✅ **Cek berhasil:** jalankan `cek` (bagian 7). Semua modul "aktif, bisa dibaca". Untuk `api_baca` tidak ada catatan "hak berisiko". Untuk `api_draf` (bila diberi hak 342) muncul catatan bahwa hak invoice bisa memvalidasi/menandai lunas — itu pengingat risiko di atas, bukan galat.
- ❌ **Kalau gagal:** "TIDAK BISA DIBACA" → hak baca modul itu belum diberikan (atau modulnya belum aktif). Daftar pelanggan kosong padahal ada → hak 262 belum diberikan. "Modul Stok belum aktif" → aktifkan Stok (bagian 5) atau abaikan bila tidak memakai stok.

---

## 7. Buat & simpan kunci API
1. Buka user `api_komunitech` → **Ubah (Modify)** → kolom **Token for API** → klik ikon **putar/refresh** di sebelahnya (membuat kunci acak) → **Simpan**. Kunci disembunyikan; salin dengan tombol **salin** di sebelahnya.
2. Buka **Terminal** (Windows: tekan Win, ketik `cmd`), jalankan (sesuaikan folder skill):
   ```
   python %USERPROFILE%\.openclaw\skills\dolibarr-usaha\scripts\dolibarr.py simpan-kunci
   ```
   (Mac/Linux: `python3 ~/.openclaw/skills/dolibarr-usaha/scripts/dolibarr.py simpan-kunci`). Tempel kunci (tidak terlihat) → Enter. Script menulis dulu "Kunci akan disimpan di: <path lengkap>". Jika file itu sudah ada, script menolak menimpa; tambahkan `--ya` hanya bila memang ingin mengganti kunci lama.
3. Alamat Dolibarr bukan `http://localhost/dolibarr`? Atur sekali: Windows `setx DOLIBARR_URL "http://localhost:8080/dolibarr"` (buka Terminal baru sesudahnya); Mac/Linux tambahkan `export DOLIBARR_URL=...` ke `~/.bashrc`/`~/.zshrc`.
4. Uji: `python ...\dolibarr.py cek`
- ✅ **Cek berhasil:** tampil "CEK DOLIBARR", versi, dan kunci tersamar `****abcd`.
- ❌ **Kalau gagal:** "401" → kunci salah/belum disimpan di Dolibarr; ulangi langkah 1–2. "tidak bisa dihubungi" → Dolibarr belum menyala (bagian 8).

**Jangan pernah** menempel kunci di chat AI, grup WA, atau email. Jika kunci bocor: buat kunci baru (langkah 1) → kunci lama langsung tidak berlaku → simpan lagi (langkah 2).

---

## 8. Menyalakan Dolibarr setiap hari
- DoliWamp memasang Apache & MariaDB sebagai layanan Windows. Setelah komputer dinyalakan ulang, buka `http://localhost/dolibarr`.
- ✅ **Cek berhasil:** halaman login tampil.
- ❌ **Kalau gagal:** **Start → Dolibarr → Tools → Start DoliWamp server**. Supaya laporan terjadwal jalan, komputer & DoliWamp harus menyala pada jam laporan (komputer toko yang tidak dimatikan, mini PC, atau jasa setup Komunitech). Perilaku nyala-otomatis ini belum diuji Komunitech di Windows; cek sendiri dengan restart sekali.

---

## 9. Cadangan (backup) & pemulihan
Data usaha Anda **hanya ada di komputer ini**. Komputer rusak/hilang/terkena ransomware tanpa cadangan = data hilang.

### 9.1 Cadangan mingguan (lewat Dolibarr)
1. Masuk sebagai admin → **Home → Pengaturan → Alat Admin (Admin tools) → Backup**.
2. **Langkah 1:** pilih **MySQL Dump (mysqldump)**, kompresi **gzip** → **Generate backup / Buat cadangan** → unduh file `.sql.gz`.
3. **Langkah 2:** di halaman yang sama, buat arsip folder **documents** (berisi PDF invoice, lampiran) → unduh `.zip`.
4. Simpan kedua file di **flashdisk/hard disk eksternal** yang dicabut setelahnya (dan, bila mau, satu salinan di cloud pribadi yang terenkripsi).
- ✅ **Cek berhasil:** ukuran file `.sql.gz` > 0 KB dan bisa dibuka (klik kanan → buka dengan 7-Zip memperlihatkan isi `.sql`).
- ❌ **Kalau gagal:** "mysqldump tidak ditemukan / not allowed" → di DoliWamp, alat dump ada di `C:\dolibarr\bin\mariadb\mariadb<versi>\bin\`. Cara manual (Terminal):
  ```
  "C:\dolibarr\bin\mariadb\mariadb<versi>\bin\mysqldump.exe" -u root -p dolibarr > D:\cadangan\dolibarr-2026-09-24.sql
  ```
  (isi sandi database dari 2.2.3). Salin juga folder `C:\dolibarr\dolibarr_documents`.

### 9.1b Simpan juga file konfigurasi (sekali, dan tiap ganti versi)
Salin `C:\dolibarr\www\dolibarr\htdocs\conf\conf.php` ke tempat cadangan yang **aman** (berisi sandi database). File ini memuat "kode unik instalasi" yang dipakai Dolibarr untuk mengenkripsi kunci API dan beberapa data lain. Tanpa file ini, setelah pemulihan kunci API lama tidak berlaku (buat kunci baru, bagian 7).

### 9.2 Pemulihan (setelah komputer diganti)
1. Pasang DoliWamp versi **sama** (bagian 2), selesaikan wizard.
2. **Alat Admin → Restore (Mengembalikan)** menampilkan perintah pemulihan untuk database Anda. Cara manual:
   ```
   "C:\dolibarr\bin\mariadb\mariadb<versi>\bin\mysql.exe" -u root -p dolibarr < D:\cadangan\dolibarr-2026-09-24.sql
   ```
   (file `.sql.gz` diekstrak dulu dengan 7-Zip).
3. Ekstrak zip documents ke `C:\dolibarr\dolibarr_documents`.
4. Masuk dengan **login & sandi yang berlaku saat cadangan dibuat**.
- ✅ **Cek berhasil:** pelanggan, invoice, dan stok terakhir tampil; `cek` skill berhasil.
- ❌ **`cek` menjawab 401 setelah pemulihan** → kode unik instalasi berbeda (conf.php tidak ikut dipulihkan); buat kunci API baru (bagian 7).
- ❌ **Kalau gagal:** "Access denied" → sandi database salah. Data tidak muncul → database yang dipulihkan beda nama; lihat nama database di Alat Admin → Backup.

**Uji pemulihan** minimal sekali (mis. di laptop lain) supaya yakin cadangan benar-benar bisa dipakai.

---

## 10. Keamanan
1. **Jangan buka Dolibarr ke internet**: jangan port-forward di router, jangan pakai tunnel (ngrok dsb.), jangan pasang di hosting tanpa HTTPS. Skill menolak alamat selain komputer ini kecuali Anda menegaskannya.
2. Konfigurasi bawaan DoliWamp membuat Apache mendengar di **semua jaringan**. Jadi di Windows Firewall, **jangan izinkan** `httpd.exe` dan `mysqld.exe` untuk jaringan Private maupun Public, lalu buktikan dengan uji HP (2.4 langkah 2). Bila ragu, minta teknisi/jasa setup untuk membatasi Apache ke `127.0.0.1`.
3. Ganti sandi database bawaan `changeme` (2.2.3 dan 2.4 langkah 1) dan pakai sandi admin Dolibarr yang kuat.
4. AI memakai **user khusus API** berhak minimal (bagian 6), bukan admin. Jadwal otomatis memakai kunci **baca-saja**; kunci yang bisa membuat draf juga bisa memvalidasi/menandai lunas lewat API (6.2), jadi simpan terpisah.
5. Perbarui DoliWamp bila ada versi baru (cadangkan dulu, bagian 9).
6. Pasang antivirus, aktifkan Windows Update, dan kunci layar komputer toko.
7. Cadangan disimpan terpisah dari komputer (ransomware bisa ikut mengunci file di disk yang sama).

---

## 11. Masalah umum
| Gejala | Penyebab | Solusi |
|---|---|---|
| Browser: "Tidak dapat menjangkau situs" | DoliWamp mati | Start → Dolibarr → Tools → Start DoliWamp server |
| Skill: "tidak bisa dihubungi" | Sama / alamat salah | Buka alamat di browser; samakan `DOLIBARR_URL` |
| Skill: "Modul API ... belum aktif" | Modul REST mati | Bagian 5 |
| Skill: "401" | Kunci salah/diganti | Bagian 7 |
| Skill: "403" / "TIDAK BISA DIBACA" | Hak user API kurang / modul mati | Bagian 5 & 6 |
| Daftar pelanggan kosong | Hak 262 belum ada | Bagian 6 |
| PPN beda Rp 1 dengan skill | Pembulatan per baris Dolibarr | Wajar; ikuti Coretax untuk faktur pajak |
| Tampilan campur Inggris | Terjemahan id_ID belum lengkap | Normal |

Butuh bantuan? **Jasa setup Komunitech** mengerjakan seluruh panduan ini bersama Anda (jarak jauh atau datang), termasuk pengamanan wajib 2.4, jadwal laporan ke Telegram, dan uji pemulihan cadangan.

Komunitech tidak berafiliasi dengan proyek Dolibarr; Dolibarr adalah merek milik pemiliknya.
