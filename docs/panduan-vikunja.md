# Panduan Pasang Vikunja untuk UMKM (bahasa awam)

Vikunja adalah program **gratis dan open-source** (lisensi AGPL-3.0) untuk mengatur tugas & proyek tim — pengganti Trello/ClickUp/Asana. Program ini jalan **di komputer Anda sendiri** (satu file program + satu file database): data tidak dititipkan ke perusahaan lain dan tidak ada biaya bulanan (kecuali Anda memilih sendiri versi cloud berbayar mereka, yang **tidak** dibahas di sini). Panduan ini menyiapkan Vikunja agar bisa dipakai skill **Vikunja Tugas** (`vikunja-tugas`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: unduh & pasang Vikunja, pengaturan agar aman (hanya bisa dibuka dari komputer sendiri), token API berskop minimal, jadwal laporan "tugas hari ini" ke Telegram, dan cadangan otomatis. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan proyek Vikunja; Vikunja adalah merek milik pemiliknya (organisasi go-vikunja).

**Status panduan (26 September 2026, diperbarui setelah uji penguji independen).** Langkah dan nama menu dicocokkan dengan sumber resmi (vikunja.io/docs, kode sumber go-vikunja/vikunja v2.6.0). Unduhan, pengikatan ke `127.0.0.1`, pendaftaran user, dan pembuatan token API berskop **dicoba langsung** dengan binary Linux resmi v2.6.0 (checksum SHA-256 dicocokkan dengan file resmi). Bagian 6 (izin token, termasuk `--ke`/penugasan) diuji ulang lewat REST API mentah langsung ke server v2.6.0 sungguhan (bukan lewat klik di layar) untuk memastikan nama kelompok izin di tabel cocok persis dengan yang dipakai server; penugasan (`--ke`) **berhasil** saat kelompok "Tasks Assignees" dicentang, **gagal dengan pesan "401"/token tidak valid** (bukan "kurang izin") saat kelompok itu tidak dicentang — lihat catatan di bagian 6. **Belum dicoba langsung** oleh Komunitech: instalasi di Windows/macOS sungguhan dan Docker. Bila tampilan di komputer Anda berbeda, ikuti tulisan di layar atau hubungi kami.

## Daftar isi
1. Sebelum mulai
2. Unduh dari sumber resmi & cek keasliannya
3. Jalankan Vikunja (Windows / macOS / Linux)
4. **Pengamanan wajib** (hanya bisa dibuka dari komputer sendiri)
5. Buat akun pertama (jadi admin) & matikan pendaftaran terbuka
6. Buat token API berskop minimal
7. Menyalakan Vikunja setiap hari
8. Cadangan (backup) & pemulihan
9. Update Vikunja
10. Copot pasang (uninstall)
11. Masalah umum

---

## 1. Sebelum mulai
| Kebutuhan | Keterangan |
|---|---|
| Komputer | Windows 10/11 64-bit, macOS, atau Linux. RAM ≥ 2 GB, ruang kosong ≥ 500 MB |
| Waktu | ±15–30 menit |
| Python 3.8+ | Untuk skill (gratis di python.org; saat memasang di Windows centang **Add Python to PATH**) |

Istilah: **Vikunja** = programnya (satu file "binary" yang sudah berisi tampilan web + server + database). **Token API** = "kata sandi khusus" agar AI bisa membaca/menulis data Vikunja tanpa tahu sandi akun Anda.

---

## 2. Unduh dari sumber resmi & cek keasliannya
1. Buka halaman unduhan resmi: **https://dl.vikunja.io/vikunja/** → masuk ke folder versi terbaru (saat panduan ditulis: **v2.6.0**, 31 Agustus 2026).
2. Pilih file sesuai komputer Anda (semua file ini adalah `-full.zip`, sudah berisi tampilan web):
   | Komputer | Nama file |
   |---|---|
   | Windows 64-bit | `vikunja-v2.6.0-windows-4.0-386.exe-full.zip` (nama "386" tetap untuk 64-bit di rilis ini; ikuti nama file terbaru di halaman unduhan) |
   | macOS Intel | `vikunja-v2.6.0-darwin-10.15-amd64-full.zip` |
   | macOS Apple Silicon (M1/M2/M3) | `vikunja-v2.6.0-darwin-10.15-arm64-full.zip` |
   | Linux 64-bit (paling umum) | `vikunja-v2.6.0-linux-amd64-full.zip` |
3. **Jangan** mengunduh dari situs lain, forum, atau tautan yang dikirim orang — hanya dari `dl.vikunja.io` atau tautan resminya di `vikunja.io/docs/installing/`.
4. Ekstrak zip ke folder baru, misalnya `Vikunja` di Documents. Di dalamnya ada file program (`vikunja-v2.6.0-...`), `LICENSE`, `config.yml.sample`, dan file `....sha256` (cocokan keaslian).
5. **Cocokkan keaslian file** (opsional tapi disarankan, ±1 menit):
   - Windows (PowerShell): `Get-FileHash .\vikunja-v2.6.0-...exe -Algorithm SHA256` lalu bandingkan dengan isi file `.sha256` di folder yang sama.
   - macOS/Linux (Terminal): `shasum -a 256 -c vikunja-v2.6.0-*.sha256` (macOS) atau `sha256sum -c vikunja-v2.6.0-*.sha256` (Linux). Harus muncul **OK**.
   - Vikunja juga menandatangani rilis dengan GPG (file `.sig`); ini langkah lanjutan untuk yang terbiasa dengan GPG, opsional untuk kebanyakan pembeli.
- ✅ **Cek berhasil:** perintah cocok menampilkan "OK" (Linux/macOS) atau hash yang sama persis (Windows).
- ❌ **Kalau tidak cocok:** **hapus file itu**, unduh ulang dari `dl.vikunja.io`. Jangan dijalankan.

---

## 3. Jalankan Vikunja

### Windows (paling sederhana untuk awam)
1. Buka folder hasil ekstrak, klik dua kali file `.exe`. Jendela hitam (Command Prompt) akan terbuka dan tetap terbuka — **jangan ditutup**, itu tandanya Vikunja sedang menyala.
2. Windows Firewall mungkin bertanya "izinkan akses jaringan": klik **Cancel/Batal** atau **hanya izinkan jaringan Private**, **jangan** izinkan Public (lihat bagian 4).
3. Buka browser, ketik `http://127.0.0.1:3456`.
- ✅ **Cek berhasil:** tampil halaman masuk/daftar Vikunja.
- ❌ **Kalau gagal:** "This site can't be reached" → tunggu beberapa detik (Vikunja sedang menyiapkan database SQLite pertama kali), lalu muat ulang. Port 3456 dipakai program lain → lihat bagian 11.

### macOS
1. Buka Terminal, `cd` ke folder hasil ekstrak.
2. macOS akan menahan file karena "dari pengembang tak dikenal": **System Settings → Privacy & Security → Allow Anyway**, lalu jalankan sekali lagi.
3. Jalankan: `chmod +x vikunja-v2.6.0-darwin-*` lalu `./vikunja-v2.6.0-darwin-*`.
4. Buka browser ke `http://127.0.0.1:3456`.

### Linux
1. Terminal, `cd` ke folder hasil ekstrak.
2. `chmod +x vikunja-v2.6.0-linux-amd64 && ./vikunja-v2.6.0-linux-amd64`.
3. Buka browser ke `http://127.0.0.1:3456`.

**Menjalankan otomatis tiap komputer nyala** (agar jadwal laporan Telegram selalu bisa jalan): di Windows, buat shortcut file `.exe` di folder Startup (`Win+R` → `shell:startup`); di Linux, buat systemd service; di macOS, buat LaunchAgent. Langkah detail ini teknis — **jasa setup Komunitech** dapat mengerjakannya sekaligus.

---

## 4. Pengamanan wajib (±5 menit, sebelum mengisi data usaha)
**Kenapa wajib?** Secara bawaan, Vikunja **mendengarkan di semua jaringan** komputer Anda (bukan cuma "komputer ini sendiri"). Artinya siapa pun yang tersambung ke Wi-Fi yang sama (kantor, kafe) berpotensi membuka Vikunja Anda dari browser mereka. Vikunja berisi daftar tugas, nama tim, dan (bila diaktifkan) lampiran — kunci seperti brankas.

**Langkah — batasi Vikunja hanya untuk komputer ini.**
1. Di folder Vikunja, buat file teks baru bernama **`config.yml`** (bukan `.txt`), isi:
   ```yaml
   service:
     interface: 127.0.0.1:3456
     publicurl: http://127.0.0.1:3456
     enableregistration: true   # matikan (bagian 5) setelah akun pertama dibuat
   database:
     type: sqlite
     path: ./vikunja.db
   files:
     basepath: ./files
   ```
2. Tutup Vikunja yang sedang berjalan (tutup jendela hitam / Ctrl+C), lalu jalankan lagi file programnya dari folder yang sama (config.yml otomatis terbaca).
3. Log yang muncul di jendela hitam harus menyebut **`127.0.0.1:3456`**, bukan hanya `:3456` atau `0.0.0.0:3456`. Ini dicoba langsung oleh Komunitech dan terbukti bekerja (baris log: `HTTP server listening on 127.0.0.1:3456`).
- ✅ **Cek berhasil (uji dengan HP, 2 menit):**
  1. Di komputer Vikunja: cari alamat IP lokal — Windows: `ipconfig` di cmd (baris **IPv4 Address**, mis. `192.168.1.10`); macOS: System Settings → Wi-Fi → Details; Linux: `hostname -I`.
  2. Sambungkan HP ke **Wi-Fi yang sama**, buka browser HP, ketik `http://192.168.1.10:3456` (pakai angka Anda).
  3. **Benar bila HP TIDAK bisa membuka** (berputar lalu gagal). Vikunja di komputer tetap terbuka lewat `127.0.0.1:3456`.
- ❌ **Kalau HP bisa membuka halaman Vikunja:** `config.yml` belum terbaca atau salah lokasi/format (harus di folder yang sama dengan file program, nama persis `config.yml`, indentasi pakai spasi bukan tab). Ulangi, uji lagi.
4. **Jangan** mengatur *port forwarding* di router, **jangan** memakai aplikasi tunnel (ngrok, Cloudflare Tunnel dsb.) untuk membuka Vikunja dari luar. Ingin dipakai tim dari luar kantor dengan aman (HTTPS)? Itu butuh pengaturan tambahan — konsultasikan ke jasa setup Komunitech, jangan dikerjakan sendiri.

---

## 5. Buat akun pertama (jadi admin) & matikan pendaftaran terbuka
1. Di `http://127.0.0.1:3456`, klik **Register/Daftar**. Isi nama pengguna, email, sandi **kuat** (≥ 12 karakter). Akun pertama ini otomatis jadi pemilik data.
2. **Setelah** akun Anda (dan akun tim, bila ada, dibuat lewat menu **Teams/Admin** di dalam aplikasi) selesai dibuat, **matikan pendaftaran terbuka** supaya orang lain di jaringan yang sama tidak bisa mendaftar sendiri: ubah `config.yml` bagian `service`, ganti `enableregistration: true` menjadi `enableregistration: false`, lalu jalankan ulang Vikunja.
3. (Opsional) Buat proyek pertama, mis. "Toko" atau "Kantor", lewat tombol **+ New Project**.
- ✅ **Cek berhasil:** masuk ke halaman utama Vikunja, ada minimal satu proyek (bawaan bernama "Inbox").
- ❌ **Kalau gagal:** "Email sudah dipakai" → gunakan email lain atau masuk (login) bila akun sudah ada.

---

## 5a. Tambahkan anggota tim ke proyek (wajib sebelum `--ke`/penugasan)
Skill bisa menugaskan tugas ke seseorang (`tambah --ke <username>`) **hanya** kalau orang itu sudah jadi **kolaborator proyek** itu di Vikunja — cukup punya akun Vikunja **tidak** otomatis membuatnya bisa ditugaskan di semua proyek.
1. Buka proyek yang dimaksud → klik ikon **Share/Bagikan** (ikon orang, biasanya di pojok kanan atas halaman proyek, di sebelah judul proyek).
2. Pilih tab **Add User** (atau **Add Team** untuk menambah seluruh tim sekaligus, bila Anda sudah punya tim lewat menu Teams).
3. Ketik username orang itu, pilih hak akses (**Read Write** untuk anggota biasa), lalu simpan.
4. Ulangi untuk tiap proyek yang perlu — hak kolaborator per-proyek, bukan berlaku otomatis ke semua proyek.
- ✅ **Cek berhasil:** nama orang itu muncul di daftar kolaborator proyek; `tambah --ke <username>` pada proyek itu berhasil.
- ❌ **Kalau `--ke` tetap gagal** dengan "Anggota '...' tidak ditemukan di proyek ini": pastikan usernamenya persis sama (bukan nama tampilan/email), dan token Anda punya izin `projects: projectusers` (lihat bagian 6).

---

## 6. Buat token API berskop minimal
Jangan pernah memberi AI **sandi akun** Anda. Vikunja punya **token API** yang bisa dibatasi haknya (skop) — mirip kunci cadangan yang hanya bisa membuka sebagian ruangan.

1. Masuk ke Vikunja di browser → klik foto profil/avatar (pojok kanan) → **Settings** → **API Tokens**.
2. Klik **Create a token**. Beri nama, mis. `Skill Baca` untuk laporan harian.
3. **Pilih izin (permissions) SEKECIL MUNGKIN** sesuai kebutuhan. Halaman pembuatan token menampilkan
   izin sebagai **beberapa kelompok kotak centang terpisah**, masing-masing dengan judulnya sendiri
   (mis. "Projects", "Tasks", "Tasks Assignees", "Projects Users", dst., berurutan dari atas ke
   bawah) — bukan satu daftar gabungan. **Kelompok "Tasks Assignees" letaknya TERPISAH dan di BAWAH
   kelompok "Tasks"**, jadi mudah terlewat kalau Anda hanya mencentang isi kelompok "Tasks" dan
   langsung scroll ke tombol Create:

   | Kebutuhan | Izin yang dicentang (nama kelompok — kotak di dalamnya) |
   |---|---|
   | Laporan/lihat saja: `hari-ini`, `terlambat`, `minggu-ini`, `ringkasan`, `daftar-proyek`, `cek` | **Projects** — Read All, Read One · **Tasks** — Read All, Read One |
   | + Menambah tugas (`tambah`) | tambahkan **Tasks** — Create |
   | + Menandai selesai (`selesai`) | tambahkan **Tasks** — Update |
   | + Menugaskan ke anggota (`tambah --ke <username>`) | tambahkan **Tasks Assignees** — Create, Read All (kelompok TERPISAH, lihat catatan di atas) · dari kelompok **Projects** centang juga kotak **Projectusers** (satu kata, tanpa spasi — ini BUKAN kelompok "Projects Users" yang terpisah; kotak "Projectusers" ada DI DALAM kelompok "Projects", bersebelahan dengan "Read All"/"Read One") |

   Nama di atas persis seperti tulisan di layar Vikunja 2.6.0 (dicoba langsung, lihat catatan status
   di awal dokumen). Kalau tampilan versi Anda berbeda, cocokkan lewat kata kuncinya: kelompok yang
   isinya "Create"/"Read All"/"Delete"/"Update bulk" untuk aksi menugaskan orang ke tugas adalah yang
   dimaksud "Tasks Assignees" di sini, apa pun urutannya di layar.

   **Kalau `--ke` (penugasan) tetap gagal dengan pesan "401"/token tidak valid** walau token sudah
   berizin baca-tulis Tasks: 99% penyebabnya kelompok "Tasks Assignees" belum dicentang sama sekali
   (Vikunja melaporkannya sebagai "token tidak valid", BUKAN "kurang izin" — membingungkan tapi
   memang begitu perilakunya). Buat ulang token, kali ini pastikan kelompok itu ikut dicentang.

   **Disarankan (seperti skill Dolibarr kami): buat DUA token** — satu **hanya-baca** (dipakai jadwal laporan harian otomatis) dan satu **baca+tulis** (dipakai hanya saat Anda sendiri minta AI menambah/menyelesaikan/menugaskan tugas). Simpan di file berbeda (`simpan-kunci --kunci-file`).
4. Isi **Expiration date** (tanggal kedaluwarsa) — jangan pilih "tanpa batas" bila tersedia; pilih 1 tahun dan perbarui nanti.
5. Klik **Create**. Token **hanya ditampilkan SEKALI** (diawali `tk_`) — salin sekarang.
6. Buka **Terminal** (Windows: tekan Win, ketik `cmd`), jalankan (sesuaikan folder skill):
   ```
   python3 ~/.openclaw/skills/vikunja-tugas/scripts/vikunja.py simpan-kunci
   ```
   (Windows: `python` atau `py` sebagai ganti `python3`). Tempel token (tidak terlihat saat diketik) → Enter. Script menulis dulu "Token akan disimpan di: <path lengkap>"; jika file itu sudah ada, script **menolak menimpa** kecuali ditambah `--ya`.
7. Uji: `python3 ~/.openclaw/skills/vikunja-tugas/scripts/vikunja.py cek`
- ✅ **Cek berhasil:** tampil "CEK VIKUNJA", versi server, dan token tersamar `tk_****abcd`.
- ❌ **Kalau gagal:** "401" → token salah/kedaluwarsa/dihapus, buat token baru (langkah 2–5). "tidak bisa dihubungi" → Vikunja belum menyala (bagian 3, 7).

**Jangan pernah** menempel token di chat AI, grup WA, atau email. Token bocor? Hapus di **Settings → API Tokens** (ikon sampah), buat token baru, simpan lagi.

---

## 7. Menyalakan Vikunja setiap hari
- Jendela program (hitam di Windows) harus tetap berjalan agar Vikunja bisa diakses & agar jadwal laporan Telegram terjadwal jalan. Untuk kantor/toko, gunakan komputer/mini PC yang selalu menyala, atau minta **jasa setup Komunitech** memasangnya sebagai layanan latar belakang otomatis (bagian 3).
- ✅ **Cek berhasil:** `http://127.0.0.1:3456` selalu bisa dibuka setiap pagi tanpa menjalankan ulang manual.

---

## 8. Cadangan (backup) & pemulihan
Semua data Anda ada di **dua hal saja**: file database `vikunja.db` (SQLite) dan folder `files` (lampiran, bila dipakai) — keduanya di folder Vikunja Anda (lihat `config.yml`, bagian `database.path` dan `files.basepath`).

1. **Tutup Vikunja dulu** (agar file database tidak sedang ditulis saat disalin).
2. Salin file `vikunja.db` dan folder `files` ke **flashdisk/hard disk eksternal** yang dicabut setelahnya, atau folder cloud pribadi terenkripsi. Beri nama bertanggal, mis. `vikunja-2026-09-26.db`.
3. Jalankan lagi Vikunja seperti biasa.
4. **Pemulihan** (komputer baru/rusak): pasang Vikunja versi yang sama (bagian 2–3), tutup, timpa `vikunja.db` dengan salinan cadangan, jalankan lagi.
- ✅ **Cek berhasil:** ukuran `vikunja.db` > 0 KB; setelah pemulihan, proyek & tugas lama muncul lagi.
- Skill `vikunja-tugas` **tidak** membuat cadangan otomatis (tidak ada perintah `backup`) — lakukan manual tiap minggu, atau jadwalkan penyalinan file lewat Windows Task Scheduler/cron (jasa setup Komunitech bisa membantu).

---

## 9. Update Vikunja
1. **Backup dulu** (bagian 8).
2. Unduh versi baru dari `dl.vikunja.io/vikunja/` (bagian 2), cocokkan checksum.
3. Tutup Vikunja lama, ganti file programnya dengan yang baru **di folder yang sama** (`config.yml`, `vikunja.db`, `files` tetap dipakai apa adanya — jangan dihapus).
4. Jalankan file program baru. Vikunja akan menjalankan migrasi database otomatis saat pertama menyala.
- ✅ **Cek berhasil:** versi baru tampil di halaman login/`cek` skill; proyek & tugas lama tetap ada.
- ❌ **Kalau gagal setelah update:** kembalikan file program versi lama + database cadangan (bagian 8), laporkan ke dukungan Komunitech.

---

## 10. Copot pasang (uninstall)
Vikunja **tidak memasang apa pun ke sistem** — cukup **hapus folder** tempat Anda mengekstraknya (setelah backup bila datanya masih dibutuhkan). Bila dipasang sebagai layanan otomatis oleh jasa setup (bagian 3), minta bantuan yang sama untuk mencabutnya.

---

## 11. Masalah umum
| Gejala | Penyebab | Solusi |
|---|---|---|
| Browser: "This site can't be reached" | Vikunja belum menyala / baru menyala | Tunggu 5–10 detik, cek jendela program masih terbuka |
| "port 3456 sudah dipakai" / server gagal menyala | Program lain memakai port itu | Ubah `service.interface: 127.0.0.1:9456` di `config.yml`, sesuaikan `VIKUNJA_URL`/`--url` skill |
| Skill: "tidak bisa dihubungi" | Vikunja mati atau alamat/port beda dari `config.yml` | Buka alamat di browser dulu; samakan `VIKUNJA_URL` |
| Skill: "401" | Token salah, kedaluwarsa, dihapus, **atau izin token kurang** (Vikunja memberi pesan yang sama untuk kedua hal — lihat catatan §3 riset kami) | Buat token baru dengan izin lengkap sesuai kebutuhan (bagian 6) |
| HP di Wi-Fi sama bisa membuka Vikunja | `config.yml` belum terbaca / salah | Ulangi bagian 4, pastikan nama file persis `config.yml` di folder program |
| macOS menolak membuka file | "pengembang tak dikenal" | System Settings → Privacy & Security → Allow Anyway |
| Setelah update, "migrasi gagal" | File database rusak/versi terlalu lama loncat jauh | Kembalikan cadangan; hubungi dukungan Komunitech |

Butuh bantuan? **Jasa setup Komunitech** mengerjakan seluruh panduan ini bersama Anda, termasuk pengamanan wajib bagian 4, token berskop, jadwal laporan ke Telegram, dan menjalankan Vikunja otomatis setiap komputer menyala.

Komunitech tidak berafiliasi dengan proyek Vikunja; Vikunja adalah merek milik pemiliknya.
