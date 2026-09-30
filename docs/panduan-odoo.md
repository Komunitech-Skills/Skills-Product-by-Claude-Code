# Panduan Menyambungkan Odoo ke AI (skill Odoo Usaha) — bahasa awam

Odoo adalah software bisnis lengkap (penjualan, faktur, stok, pembelian, CRM, dan lain-lain). Edisi **Community** gratis dan open-source (lisensi LGPL-3.0) dan bisa dipasang di komputer/server sendiri; edisi **Enterprise** dan **Odoo Online** (`namausaha.odoo.com`) berbayar dari Odoo S.A. Panduan ini menyiapkan Odoo **yang sudah Anda punya** agar bisa dipakai skill **Odoo Usaha** (`odoo-usaha`), plus ringkasan cara memasang Odoo Community bila belum punya.

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pemasangan Odoo Community di mini PC/VPS milik Anda, pengaturan Indonesia (IDR, PPN), pengguna API aman, cadangan otomatis, dan jadwal laporan ke Telegram. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan Odoo S.A. "Odoo" adalah merek milik Odoo S.A.

**Status panduan (30 September 2026, jujur):** langkah API (kunci API, XML-RPC, JSON-2, syarat paket Custom) dicocokkan dengan **dokumentasi resmi Odoo 19.0 & 20.0** (https://www.odoo.com/documentation/19.0/developer/reference/external_api.html dan `external_rpc_api.html`). Perintah Docker dicocokkan dengan dokumentasi image resmi `odoo` di Docker Hub. Skill `odoo-usaha` sudah diuji ke **Odoo Community 18 & 19 asli** (Docker lokal, data uji) oleh penguji independen, termasuk hak pengguna di §5; belum ke Odoo Online, Enterprise, atau versi 16/17/20. Nama menu bisa sedikit berbeda antar versi dan bahasa. Bila tampilan Anda berbeda, ikuti tulisan di layar dan hubungi kami.

## Daftar isi
1. Sebelum mulai (cek versi & paket)
2. Belum punya Odoo? Ringkasan pasang Odoo Community (Docker)
3. Pengamanan wajib untuk Odoo di komputer/server sendiri
4. Pengaturan awal Indonesia
5. Buat pengguna khusus AI (berhak minimal)
6. Buat & simpan kunci API
7. Aturan stok minimum (agar "stok menipis" bisa dinilai)
8. Sambungkan & uji
9. Masalah umum

---

## 1. Sebelum mulai (cek versi & paket)
| Pertanyaan | Cara cek | Artinya untuk skill |
|---|---|---|
| Odoo versi berapa? | Pengaturan → gulir ke bawah (tulisan versi), atau tanya penyedia | Dirancang untuk **16–20**. 19+ memakai JSON-2 (tanpa nama database), 16–18 memakai XML-RPC (butuh nama database + login) |
| Odoo Online (`*.odoo.com`)? | Alamat di browser | API hanya tersedia di **paket Custom**. Paket **One App Free/Standard tidak** membuka API (dokumentasi resmi) → skill tidak bisa dipakai, kecuali paket dinaikkan |
| Self-host (server sendiri/VPS/Odoo.sh)? | Alamat bukan `*.odoo.com` | Bisa; server Anda harus didaftarkan sekali (`atur --izinkan-host`) |
| Aplikasi terpasang? | Menu Aplikasi | Penjualan (Sales), Faktur/Akuntansi (Invoicing), Inventori. Yang tidak terpasang akan dilaporkan "tidak bisa dibaca" |
| Python 3.8+ di komputer yang menjalankan AI | `python3 --version` (Windows: `py --version`) | Gratis di python.org; saat memasang di Windows centang **Add Python to PATH** |

---

## 2. Belum punya Odoo? Ringkasan pasang Odoo Community (Docker)
Tingkat kesulitan: **sedang–sulit** (perlu terbiasa dengan terminal). Untuk usaha dengan banyak transaksi, pakai mini PC/VPS yang menyala terus atau jasa setup.
1. Pasang **Docker Desktop** (Windows/Mac) atau Docker Engine (Linux) dari docker.com.
2. Jalankan database dan Odoo (perintah dari dokumentasi image resmi, **ditambah `127.0.0.1`** agar hanya bisa dibuka dari komputer ini; ganti `SANDI-KUAT`):
   ```bash
   docker run -d -v odoo-db:/var/lib/postgresql/data -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=SANDI-KUAT \
     -e POSTGRES_DB=postgres --name db postgres:15
   docker run -d -v odoo-data:/var/lib/odoo -p 127.0.0.1:8069:8069 --name odoo --link db:db \
     -e PASSWORD=SANDI-KUAT -t odoo
   ```
3. Buka `http://localhost:8069` → formulir **buat database**: isi *Master Password* (catat!), nama database (mis. `tokomaju`, huruf kecil tanpa spasi), email & sandi admin, bahasa **Indonesian / Bahasa Indonesia**, negara **Indonesia**. **Jangan centang data demo** untuk database usaha sungguhan.
- ✅ **Cek berhasil:** tampil halaman Aplikasi Odoo.
- ❌ **Kalau gagal:** "port is already allocated" → ganti `127.0.0.1:8069` menjadi `127.0.0.1:8070` (alamat jadi `http://localhost:8070`); halaman tidak terbuka → `docker logs odoo` dan tunggu 1 menit.

Setelah itu pasang aplikasi **Penjualan**, **Faktur (Invoicing)**, dan **Inventori** dari menu Aplikasi.

---

## 3. Pengamanan wajib (Odoo di komputer/server sendiri)
- **Hanya bisa dibuka dari komputer ini**, atau lewat **https** bila dibuka dari internet (pasang di belakang reverse proxy dengan sertifikat, mis. Let's Encrypt — tugas teknisi). Skill menolak alamat internet tanpa https.
- **Master Password** (pengelola database) harus kuat dan dicatat; bila server dibuka ke internet, minta teknisi mematikan halaman pengelola database (`list_db = False` di konfigurasi Odoo).
- **Cadangan rutin:** menu pengelola database (`/web/database/manager`) → *Backup*, atau `pg_dump` oleh teknisi. Simpan salinan di luar komputer itu. Coba pulihkan sekali untuk memastikan cadangan bisa dipakai.
- Odoo Online: keamanan server diurus Odoo S.A.; tugas Anda menjaga sandi & kunci API.

---

## 4. Pengaturan awal Indonesia
1. **Pengaturan → Perusahaan**: nama, alamat, **mata uang IDR**. Skill menjumlahkan dalam mata uang perusahaan; pesanan bermata uang lain dilaporkan terpisah.
2. **Faktur/Akuntansi → Konfigurasi → Pajak**: pastikan pajak penjualan PPN sesuai kebutuhan (paket lokalisasi Indonesia `l10n_id` terpasang otomatis bila negara perusahaan Indonesia). Skill **membandingkan** pajak Odoo dengan standar Komunitech (12% × DPP 11/12 = 11% efektif) dan melaporkan BEDA bila tidak sama; pengaturan pajak tetap keputusan Anda/akuntan. e-Faktur resmi tetap lewat Coretax DJP.
3. **Zona waktu pengguna** (Preferensi): Asia/Jakarta (WIB), Asia/Makassar (WITA), atau Asia/Jayapura (WIT). Skill memakai `--tz` untuk menentukan "hari ini".

---

## 5. Buat pengguna khusus AI (berhak minimal)
Kenapa? Agar kalau kunci bocor, kerusakannya terbatas, riwayat perubahan di Odoo tercatat atas nama "Bot", dan kunci bisa dicabut tanpa mengganggu akun Anda. Menu: **Pengaturan → Pengguna & Perusahaan → Pengguna → Baru**.

**Terus terang dulu:** Odoo **tidak punya** peran "hanya baca" murni untuk Penjualan. Hak *Penjualan: User* di Odoo (Own Documents maupun All Documents) juga boleh membuat penawaran — untuk *All Documents* + Akuntansi *Read-only* ini terbukti saat uji di Odoo 18 & 19 (draf berhasil dibuat). Yang mencegah AI mengubah data adalah **pengaman di dalam skill** (daftar metode yang boleh dipanggil: hanya baca + draf penawaran; hapus/konfirmasi/posting/bayar ditolak bahkan dengan kunci administrator). Hak Odoo di bawah ini membatasi kerusakan **bila kunci dicuri dan dipakai di luar skill**.

| Pengguna | Untuk | Hak minimum yang realistis |
|---|---|---|
| **Bot Laporan** | Chat harian, laporan terjadwal, piutang | Penjualan: ***User: All Documents*** (wajib untuk angka lengkap); Akuntansi/Faktur: ***Read-only*** (bukan *Billing* — *Billing* juga boleh memposting faktur); Inventori: *User*. **Bukan** Administrator/Pengaturan |
| **Bot Penjualan** (opsional) | Membuat draf penawaran | Sama dengan Bot Laporan, atau Penjualan *User: All Documents* saja. Gunanya kunci terpisah: riwayat "dibuat oleh" jelas dan kunci pembuat draf bisa dicabut sendiri — **bukan** pemisahan hak baca/tulis |

- **Jangan pakai *User: Own Documents* untuk laporan.** Dengan hak itu Odoo hanya memperlihatkan pesanan & faktur **milik pengguna itu** (atau tanpa penjual). Laporan akan menunjukkan angka jauh lebih kecil (bisa Rp 0). Sejak versi 1.0.1 skill memeriksa grup pengguna API dan menulis **PERINGATAN DATA SEBAGIAN** + kode keluar 9 (jadwal tercatat gagal), tetapi solusinya tetap memberi hak *All Documents*.
- **Piutang per tanggal lampau** (`piutang --per-tanggal 2026-06-30`) butuh hak Akuntansi baca (*Read-only* atau *Billing*) agar tanggal pelunasan bisa dibaca. Tanpa itu skill memberi PERINGATAN.
- Nama hak berbeda-beda antar versi (Odoo 19 memakai "peran"). Prinsipnya: **bisa melihat semua** Penjualan, Faktur, Inventori; **tidak** berhak Administrator.
- Odoo Online/Enterprise menghitung biaya per pengguna. Bila tidak ingin menambah pengguna, kunci API boleh dibuat dari akun Anda sendiri, tetapi **jangan akun Administrator**, pastikan hak Penjualan Anda *All Documents*, dan simpan kunci hanya di komputer Anda.
- `cek` menampilkan "Cakupan data" (SEMUA / HANYA milik pengguna API ini) dan CATATAN "RISIKO ... ADMINISTRATOR" bila kunci milik admin. Aturan akses buatan sendiri (record rule khusus) atau pembatasan multi-perusahaan tidak terdeteksi — cocokkan angka pertama kali dengan layar Odoo.

---|---|---|
| **Bot Laporan** | Chat harian, laporan terjadwal | Penjualan: *User: All Documents* (atau hak baca); Faktur/Akuntansi: hak **baca** (*Read-only* bila tersedia, selain itu *Billing*); Inventori: *User*. **Bukan** Administrator/Pengaturan |
| **Bot Penjualan** (opsional) | Membuat draf penawaran | Penjualan: *User: Own Documents* atau *All Documents*. Tanpa hak Pengaturan |

- Nama hak akses berbeda-beda antar versi (Odoo 19 memakai "peran"). Prinsipnya: **bisa melihat** Penjualan, Faktur, Inventori; **tidak** berhak Administrator.
- Odoo Online/Enterprise menghitung biaya per pengguna. Bila tidak ingin menambah pengguna, kunci API boleh dibuat dari akun Anda sendiri, tetapi **jangan akun Administrator** dan simpan hanya di komputer Anda.
- `cek` akan menulis CATATAN "RISIKO ... ADMINISTRATOR" bila kunci milik admin.

---

## 6. Buat & simpan kunci API
1. Masuk ke Odoo **sebagai pengguna bot** (atur sandinya dulu di menu Pengguna).
2. Klik foto profil (kanan atas) → **Preferensi / My Profile** → tab **Keamanan Akun (Account Security)** → **Kunci API Baru (New API Key)**. Odoo meminta sandi sekali lagi.
3. Isi keterangan jelas, mis. `AI laporan - laptop toko`. Odoo 19+ meminta **masa berlaku** (maksimal ±3 bulan menurut dokumentasi resmi): catat tanggal habisnya di kalender, dan buat kunci baru sebelum itu.
4. Salin kunci. **Kunci hanya tampil sekali.** Jangan ditempel di chat, email, atau grup.
5. Di terminal komputer yang menjalankan AI (bukan di chat):
   ```bash
   python3 ~/.openclaw/skills/odoo-usaha/scripts/odoo.py simpan-kunci
   ```
   Tempel kunci → Enter (tidak tampil). Tersimpan di `~/.komunitech/odoo-kunci.txt`, hanya bisa dibaca akun Anda. Kunci kedua (Bot Penjualan): `simpan-kunci --kunci-file ~/.komunitech/odoo-kunci-draf.txt`.
- Kunci bocor/tertempel di chat? Hapus kunci itu di tab Keamanan Akun, lalu buat yang baru dan `simpan-kunci --ya`.

---

## 7. Aturan stok minimum (agar "stok menipis" bisa dinilai)
**Inventori → Operasi/Konfigurasi → Aturan Pemesanan Ulang (Reordering Rules)** → Baru: pilih produk, isi **Min** (batas menipis) dan **Maks** (stok ideal). Skill memberi status MENIPIS bila stok < Min, dan saran pesan = Maks − stok perkiraan. Produk tanpa aturan hanya diperiksa bila stoknya habis/minus.

---

## 8. Sambungkan & uji
```bash
# Odoo Online (database otomatis = nama subdomain)
python3 <folder-skill>/scripts/odoo.py atur --url https://tokomaju.odoo.com
# Self-host Odoo 16-18 (XML-RPC butuh database + login pengguna bot)
python3 <folder-skill>/scripts/odoo.py atur --url http://localhost:8069 --db tokomaju --login bot-laporan@tokomaju.id
# Server sendiri di internet (hanya bila server itu milik Anda, wajib https)
python3 <folder-skill>/scripts/odoo.py atur --url https://erp.tokomaju.id --izinkan-host
python3 <folder-skill>/scripts/odoo.py cek
```
- ✅ **Cek berhasil:** `cek` menampilkan versi, pengguna "Bot Laporan", "bisa dibaca" untuk aplikasi yang terpasang, dan "Cakupan data: SEMUA data" (bukan "HANYA milik pengguna API ini").
- Lalu cocokkan sekali: jalankan `penjualan --tanggal kemarin` dan bandingkan dengan menu Penjualan → Pesanan (filter tanggal kemarin, status Pesanan Penjualan).

---

## 9. Masalah umum
| Gejala | Penyebab | Solusi |
|---|---|---|
| "Login ke Odoo ditolak" / "Kunci API ditolak" | Kunci salah, dihapus, kedaluwarsa; login/database salah | Buat kunci baru; cek `atur` (login = email pengguna bot, database = nama database) |
| "Akses XML-RPC ditolak" / "bukan API Odoo" di odoo.com | Paket bukan Custom | Naikkan paket, atau pakai skill lain |
| "Endpoint XML-RPC ... tidak ada" | Odoo 22 / Odoo Online 21.1 ke atas menghapus XML-RPC | `atur --protokol json2` (Odoo 19+) |
| "Nama database ... belum diatur" | Odoo ≤18 butuh nama database | Lihat di halaman pilih database (`/web/database/selector`) atau tanya penyedia hosting |
| "Hak akses ... kurang" | Pengguna bot belum diberi hak aplikasi itu | Atur hak di menu Pengguna (§5) |
| "PERINGATAN DATA SEBAGIAN" / kode 9 / penjualan Rp 0 padahal ada pesanan | Hak Penjualan *Own Documents*, atau piutang lampau tanpa hak Akuntansi baca | Ubah hak jadi *All Documents* + Akuntansi *Read-only* (§5) |
| "mengalihkan permintaan" | Alamat http padahal server memakai https, atau alamat lama | Pakai alamat persis dari browser |
| "Sertifikat HTTPS ... tidak valid" | Sertifikat server kedaluwarsa/buatan sendiri | Pasang sertifikat resmi (teknisi) |
| Angka beda dengan layar Odoo | Filter tanggal/zona waktu, mata uang lain, faktur draf | Samakan filter; laporkan ke dukungan Komunitech (tanpa kunci) |
