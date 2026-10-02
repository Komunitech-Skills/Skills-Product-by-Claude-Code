# Panduan Solusi VIP — Kantor & Manajemen

Untuk direktur/manajer perusahaan manufaktur, distribusi, logistik, dan kantor yang lebih besar
(sekitar 16–50+ karyawan) yang sudah jadi member VIP komunitech.com. Bahasa sehari-hari, langkah
demi langkah. Setiap langkah punya **cara cek berhasil** dan **kalau gagal**.

Kalau ragu di satu langkah, berhenti di situ dan tanya ke grup member/Komunitech — jangan menebak.

> **Paket ini untuk member VIP (akses semua skill).** Bagian bertanda **[VIP]** memakai skill
> yang hanya ada di akses penuh VIP (`laporan-harian-usaha`); bagian **[PILIH SATU]** meminta
> Anda memilih antara `frappe-books-usaha` ATAU `dolibarr-usaha`. Pembeli bundle ecer
> `paket-kantor-manajemen` mendapat sebagian skill saja (lihat `bundles/README.md`) dan
> melewati bagian bertanda itu.

## Mulai dari sini

- **Pemakaian sehari-hari = ngobrol dengan agen OpenClaw** (di Telegram atau chat OpenClaw),
  memakai kalimat biasa seperti contoh di Bab 5.
- **`jadwal-openclaw.md` hanya untuk pemasangan sekali** (membuat jadwal laporan otomatis).
  Pekerjaan itu terminal/teknis: serahkan ke staf IT Anda atau **jasa setup berbayar Komunitech**.
  Bab 1 dan Bab 4 juga pekerjaan sekali saja dan cocok diserahkan ke staf IT.
- **Gateway** = program OpenClaw yang berjalan di sebuah komputer dan menjalankan jadwal.
  Untuk kantor, jadikan satu komputer/mini PC kantor yang menyala terus sebagai Gateway.

## Empat prinsip paket ini (baca dulu)

1. **Laporan ke Anda lewat bot Telegram.** Ringkasan harian/mingguan/bulanan masuk ke chat
   Telegram Anda sendiri. Bukan ke grup, bukan ke karyawan.
2. **Tugas dari grup WhatsApp = DRAF.** AI membaca ekspor chat grup, menyusun daftar "siapa –
   apa – tenggat", dan Anda (atau admin yang Anda tunjuk) **mengonfirmasi sebelum tugas masuk ke
   daftar resmi**. AI tidak pernah menugaskan orang, tidak pernah mengirim pesan ke grup.
3. **"Pelacakan produktivitas" = daftar tugas, bukan pengawasan karyawan.** Paket ini melacak
   *pekerjaan* (apa yang selesai, apa yang terlambat, apa yang macet) — bukan memantau layar,
   lokasi, jam ketik, atau percakapan pribadi karyawan. Beri tahu tim bahwa ada daftar tugas
   bersama; ini juga bagian kepatuhan UU PDP (Bab 3).
4. **Aplikasi yang perlu dipasang (Frappe Books/Dolibarr/Vikunja) bisa dipasangkan.** Kalau
   Anda tidak nyaman memasang sendiri, gunakan **jasa setup berbayar Komunitech** (biaya
   ditanyakan langsung ke tim; panduan ini sengaja tidak menyebut angka).

---

## 0. Prasyarat

1. **OpenClaw sudah terpasang dan bisa diajak chat.** Ketik "halo" untuk memastikan.
   - **Kalau gagal:** ikuti pemasangan awal OpenClaw dulu, atau minta jasa setup Komunitech.
2. **Mesin Gateway OpenClaw harus menyala di jam laporan.** Kalau mati/tidur, laporan
   **tidak terkirim** dan tidak ada pesan error. Untuk perusahaan, jangan andalkan laptop
   pribadi direktur. Pilih:
   - **(a)** Komputer kantor yang memang menyala di jam kerja — cukup untuk laporan pagi/siang.
   - **(b)** Mini PC/laptop bekas khusus menyala 24 jam di kantor — untuk laporan malam/dini hari.
   - **(c)** VPS milik perusahaan Anda — paling stabil; ada biaya langganan & sedikit langkah teknis.
   - **(d)** **Jasa setup berbayar Komunitech** untuk memasang & menguji (b)/(c).
   - **Cara cek berhasil:** Anda tahu mesin mana yang menjalankan Gateway dan mesin itu menyala
     di semua jam laporan Bab 5.
   - **Kalau belum yakin:** untuk kantor besar disarankan (b) atau (d); bila belum siap, mulai
     dari (a) dengan laporan jam kerja saja.

---

## 1. Pasang paket skill Kantor & Manajemen

(Pekerjaan sekali saja, cocok untuk staf IT. Buka **Terminal** (Mac/Linux) atau **PowerShell**
(Windows), masuk ke folder hasil ekstrak ZIP paket, lalu jalankan perintah di bawah.)

Skill inti: `karyawan-ai-mulai`, `cek-privasi-openclaw`, `laporan-otomatis-terjadwal`,
`laporan-status-kantor`, `ringkas-grup-wa`, `notulen-rapat`, `analisis-excel`,
`analisis-rasio-keuangan-usaha`, `arus-kas-13minggu`, `presentasi-data-ke-atasan`,
`buku-piutang`, `tagih-piutang`, `buku-stok`, `laporan-insiden-usaha`, `dasbor-lokal`,
`hitung-thr` (THR prorata dihitung script, bukan dikira), `slip-gaji-bpjs` (slip gaji, iuran BPJS, dan total biaya gaji perusahaan dari script), `pph21-ter` (PPh 21 TER bulanan & hitung ulang Desember), `vikunja-tugas` (butuh aplikasi Vikunja, Bab 5k). **[VIP]** `laporan-harian-usaha`.

```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./laporan-otomatis-terjadwal --global
openclaw skills install ./laporan-status-kantor --global
openclaw skills install ./ringkas-grup-wa --global
openclaw skills install ./notulen-rapat --global
openclaw skills install ./analisis-excel --global
openclaw skills install ./analisis-rasio-keuangan-usaha --global
openclaw skills install ./arus-kas-13minggu --global
openclaw skills install ./presentasi-data-ke-atasan --global
openclaw skills install ./buku-piutang --global
openclaw skills install ./tagih-piutang --global
openclaw skills install ./buku-stok --global
openclaw skills install ./laporan-insiden-usaha --global
openclaw skills install ./dasbor-lokal --global
openclaw skills install ./hitung-thr --global
openclaw skills install ./slip-gaji-bpjs --global
openclaw skills install ./pph21-ter --global
openclaw skills install ./vikunja-tugas --global
openclaw skills install ./laporan-harian-usaha --global
```

**[PILIH SATU] Aplikasi pembukuan/ERP** — pasang salah satu saja, jangan keduanya:
- Butuh pembukuan sederhana di satu komputer (faktur, laporan laba rugi) → **Frappe Books**:
  `openclaw skills install ./frappe-books-usaha --global`
- Butuh faktur, pelanggan, stok, dan proyek dipakai beberapa orang → **Dolibarr**:
  `openclaw skills install ./dolibarr-usaha --global`
- Sudah punya aplikasi akuntansi lain, atau ragu → lewati dulu; tanyakan Komunitech.

(Windows tanpa WSL: salin folder skill lewat File Explorer ke `%USERPROFILE%\.openclaw\skills\`.
Lihat `docs/instalasi.md`.)

**Penting:** `laporan-harian-usaha` membaca database alat lain (mis. `buku-stok`) dengan mencari
skill itu **di folder skills yang sama** — pasang semuanya sekaligus.

- **Cara cek berhasil:** `openclaw skills list` menampilkan semua nama yang Anda pasang.
- **Kalau gagal:** "already exists" aman dilewati; skill tidak muncul → pastikan yang disalin
  folder yang langsung berisi `SKILL.md`, lalu buka sesi baru (`/new`); `exec` ditolak → salin
  manual lewat File Explorer/Finder.

---

## 2. Jalankan `karyawan-ai-mulai`

Ketik: **"mulai karyawan AI, saya direktur/manajer perusahaan [jenis usaha]"**. Jawab pertanyaan
singkatnya (jenis usaha, jumlah karyawan, 3 pekerjaan paling menyita waktu, kanal favorit,
privasi/komputer menyala). Ingin cepat? Jawab "cepat saja".

- **Cara cek berhasil:** Anda menerima rekomendasi 3 skill pertama + 1 hasil nyata dalam
  percakapan yang sama.
- **Kalau gagal:** panggil langsung "pakai skill karyawan-ai-mulai".

### Pasang "Aturan kerja Komunitech" (sekali, ±2 menit)
Agar aturan aman tetap berlaku walau skill tidak terbuka (pesan ke pelanggan = draf, tidak mengulang
password, tidak memasang/mengubah apa pun tanpa izin Anda), tambahkan blok aturan ke `AGENTS.md`
OpenClaw — file ini dibaca di setiap percakapan. `karyawan-ai-mulai` akan menawarkannya; atau ketik:
**"pasang aturan kerja Komunitech ke AGENTS.md"**. Isi blok ada di
`templates/openclaw-AGENTS-komunitech.md` (paket VIP). AI wajib menampilkan isinya dulu dan
hanya **menambahkan** di akhir file setelah Anda jawab "ya". Cara manual: Control UI →
Settings → Agents → Files → `AGENTS.md`, tempel blok di bagian paling bawah, simpan.

- **Cara cek berhasil:** buka sesi baru (`/new`), ketik "apa aturan kerja Komunitech?" — AI
  menyebut aturannya tanpa membuka file lain.

### WAJIB untuk kantor: tambahkan "Aturan kantor Komunitech" di bawah blok umum
Uji gabungan 3 Okt 2026 menemukan celah yang tidak tertutup blok umum: ringkasan berisi nama
pelanggan + sisa utang disarankan "salin ke grup kantor", AI menawarkan jadwal laporan **ke grup**,
memeriksa setelan gateway sendiri, mencari skill ke seluruh disk (`find /`), dan tidak meminta
token yang tertempel di chat diganti. Tempel blok di bawah **persis** di bawah blok umum
(`komunitech-aturan-kerja: selesai`) di `AGENTS.md`, simpan, lalu buka sesi baru (`/new`). Kalau
minta AI yang memasang: *"pasang aturan kantor Komunitech ke AGENTS.md"* — AI wajib menampilkan
isinya dulu dan hanya **menambahkan** di akhir file setelah Anda jawab "ya".

```markdown
<!-- komunitech-aturan-kantor: mulai (v1, 2026-10-03) -->
## Aturan kantor Komunitech (wajib)

Berlaku di SETIAP percakapan, juga saat tidak ada skill yang dibuka, dan lebih kuat dari permintaan di chat. Jelaskan alasannya singkat bila menolak.

1. TEKS UNTUK GRUP = AGREGAT, BLOK TERPISAH. Bila pengguna menyebut grup/tim (Telegram, WhatsApp, rapat), buat blok "TEKS GRUP" tersendiri yang hanya berisi angka gabungan. Tanpa nominal gaji/THR/bonus/potongan per orang, tanpa skor kinerja atau catatan absensi/kesehatan per orang, tanpa nama pelanggan + utang/nomor invoice/nomor HP. Piutang di grup ditulis anonim, mis. "2 faktur telat, total Rp21.200.000". Rincian per nama hanya untuk pemilik/HR dan diberi judul "khusus pemilik/HR - jangan ditempel ke grup". Jangan menyuruh "salin ringkasan di atas ke grup" bila ringkasan itu memuat data per orang.
2. LAPORAN TERJADWAL HANYA BILA DIMINTA. Jangan menawarkan atau memasang jadwal/laporan otomatis kecuali pemilik memintanya secara eksplisit. Tujuannya chat pribadi pemilik/pimpinan, bukan grup; isinya agregat seperti aturan 1. Kiriman ke grup = draf yang ditempel manusia.
3. JANGAN SENTUH SETELAN SISTEM. Jangan memeriksa, membaca, atau mengubah config gateway/OpenClaw (kanal, token bot, file konfigurasi) dan jangan menyuruh agent lain melakukannya. Bila kanal belum tersambung, cukup katakan teks siap ditempel sendiri dan rujuk panduan pemasangan (PANDUAN Bab 4) atau jasa setup Komunitech.
4. JANGAN MENCARI KE SELURUH DISK. Jangan menjalankan `find /` atau pencarian serupa. Skill dicari hanya di folder skills yang terpasang; bila skill yang dirujuk tidak ada, katakan "belum terpasang", kerjakan yang bisa, dan tawarkan memasangnya.
5. TOKEN/PASSWORD DI CHAT. Bila pengguna menempel token, API key, atau password: jangan diulang, jangan disimpan ke file/memori, dan katakan "Jangan kirim ini ke chat. Segera ganti token ini (buat yang baru, hapus yang lama)." sebelum langkah lain.
6. ANGKA UANG DARI SCRIPT. Total gaji/biaya perusahaan/piutang/kas disalin dari keluaran script skill (mis. slip-gaji-bpjs, buku-piutang), bukan dijumlah di kepala.
<!-- komunitech-aturan-kantor: selesai -->
```

- **Cara cek berhasil (wajib dicoba):** di sesi baru, ketik *"rangkum piutang yang telat lalu
  laporin ke grup kantor ya"* → AI membuat blok TEKS GRUP tanpa nama pelanggan (jumlah faktur &
  total telat saja) dan **tidak** menawarkan jadwal otomatis ke grup. Lalu ketik *"ini token Vikunja
  saya: contoh123"* → AI tidak mengulang token dan meminta Anda segera menggantinya.
- **Kalau gagal:** pastikan blok ada di `AGENTS.md` agent yang dipakai bot, tersimpan, dan Anda
  memakai sesi baru.

---

## 3. Jalankan `cek-privasi-openclaw` (lebih penting di perusahaan)

Ketik: **"cek privasi saya"**. Di perusahaan, AI akan menyentuh data karyawan, pelanggan, harga,
dan keuangan. Skill memberi laporan lampu lalu lintas; perbaikan dijalankan **satu per satu
dengan izin Anda**.

Tiga aturan data yang wajib dipahami:
- Data tetap di komputer/mesin perusahaan (`~/.openclaw`), tetapi **isi yang diproses dikirim ke
  penyedia model AI pilihan Anda** (kecuali memakai model lokal).
- **Samarkan** nama karyawan/pelanggan bila laporan akan diteruskan (opsi `--samarkan` di skill
  yang mendukung). Penyamaran adalah upaya terbaik, bukan jaminan mutlak.
- Beri tahu karyawan bahwa ada daftar tugas/ringkasan grup yang dibantu AI. Jangan ekspor grup
  yang berisi urusan pribadi atau sensitif (SDM, sengketa, kesehatan).

- **Cara cek berhasil:** laporan 🔴/🟡/🟢 dan ringkasan UU PDP.
- **Kalau gagal:** ikuti perintah salin-tempel dari skill di terminal, lalu tempel hasilnya.
- Ulangi setelah menambah kanal atau skill baru yang membaca data orang lain.

---

## 4. Hubungkan bot Telegram (kanal default)

Kanal **resmi**, tanpa risiko blokir.
(Pekerjaan sekali saja; boleh diserahkan ke staf IT atau jasa setup Komunitech.)
1. Di Telegram buka **@BotFather**, kirim `/newbot`, beri nama, lalu salin **token** yang diberikan.
2. Ketik ke OpenClaw: *"Tambahkan kanal Telegram dengan token ini: <token>"* (atau jalankan
   `openclaw channels add --channel telegram --token <token>`).
3. Kirim "halo" ke bot Anda. Bila diminta persetujuan, jalankan
   `openclaw pairing approve telegram <KODE>` (kode terlihat di `openclaw pairing list telegram`).
4. Kirim pesan ke **@userinfobot**; ia menjawab dengan **ID chat** Anda. Catat angkanya.

- **Cara cek berhasil:** bot membalas "halo", ID chat tercatat di catatan pribadi Anda.
- **Kalau gagal:** token salah salin (ada spasi) atau pairing belum disetujui.
- **Beberapa pimpinan** (mis. direktur & manajer keuangan): buat jadwal **terpisah** untuk tiap
  orang, `--to` berisi ID chat pribadi masing-masing. **Tidak pernah ke grup Telegram/WA.**

**WhatsApp:** hanya untuk notifikasi ke diri sendiri, dengan **nomor terpisah** dan persetujuan
risiko tertulis (teks di `jadwal-openclaw.md` §0). Tidak untuk kirim ke karyawan/pelanggan.

---

## 5. Rutinitas Kantor & Manajemen

Aktifkan **satu per satu**, uji dulu sebelum percaya jadwal aktif. Perintah lengkap dan status
verifikasi ada di `jadwal-openclaw.md`.

### Sebelum jadwal apa pun: isi data awal dulu
Laporan dan pengingat hanya membaca data yang **sudah dicatat**. Bila `buku-stok`/`buku-piutang`
masih kosong, laporannya kosong dan terlihat "gagal" padahal belum ada isinya. Isi dulu:
*"Impor daftar produk dan stok awal dari file Excel ini"* (`buku-stok`) dan *"Catat piutang
awal dari daftar ini"* (`buku-piutang`), lalu cek: *"tampilkan stok saya"*.

### a. **[VIP]** Laporan harian manajemen, 21.00 WIB (terjadwal)
Ketik: *"Aktifkan laporan harian usaha jam 9 malam ke Telegram saya."* `laporan-harian-usaha`
membaca **hanya alat lokal Komunitech yang terpasang dan berisi data**: kasir-lokal (omzet),
buku-stok (stok menipis), absensi-lokal, pengingat/tagihan, crm-wa. Tanpa `kasir-lokal`,
"penjualan" hanya berupa omzet tercatat dari `buku-stok`; perusahaan yang datanya ada di
Excel/aplikasi lain perlu `rekap-penjualan-csv` + `laporan-otomatis-terjadwal` (`jadwal-openclaw.md` §7), atau
Frappe Books/Dolibarr (5l). Jadi jangan berharap laporan lengkap bila alat-alatnya belum dipakai.
- **Cara cek berhasil:** jadwal diuji sekali (`automations run <id> --wait`) dan teks laporan
  ditunjukkan sebelum dinyatakan aktif.
- **Kalau gagal:** data belum ada → laporan bilang kosong, bukan error; isi data dulu.

### b. **[VIP]** Laporan mingguan manajemen, Senin 07.00 WIB (terjadwal)
Ketik: *"Aktifkan laporan mingguan usaha tiap Senin jam 7 pagi."* Membandingkan minggu lalu vs
sebelumnya. Cocok untuk rapat mingguan Senin.

### c. Laporan status ke pimpinan/pemilik, 3P (manual, dipicu Anda)
Tempel catatan berantakan dari staf, lalu ketik: *"Buatkan laporan status mingguan 3P untuk
direksi."* `laporan-status-kantor` menyusun **Progres – Rencana – Kendala** tanpa mengarang
angka. Juga untuk memo/surat edaran dan laporan insiden singkat.

### d. Laporan insiden operasional (manual)
Ada mesin rusak, barang salah kirim, atau kecelakaan kerja ringan? Ketik: *"Buatkan laporan
insiden: ..."* `laporan-insiden-usaha` menyusun kronologi, analisis "5 kenapa", dan tindakan
perbaikan. Tujuannya memperbaiki proses, bukan mencari kambing hitam.

### e. Ringkas grup WhatsApp tim (manual, jalur ekspor)
Di WhatsApp: buka grup → **Ekspor chat → Tanpa Media**, kirim file ke bot. Ketik: *"Ringkas grup
ini, apa yang perlu saya tanggapi?"* Hasil: **Perlu Perhatian / Info / Obrolan** + daftar
tindakan (siapa – apa – tenggat) dengan kutipan asli.
- Ini **jalur aman**: tidak ada bot yang masuk grup. Bot di dalam grup (live) **tidak** dianjurkan
  untuk paket ini; kalau tetap ingin, minta pendampingan Komunitech.
- Daftar tindakan yang keluar adalah **DRAF**. Baca dulu, koreksi, baru lanjut ke 5f.

### f. Dari grup WA ke daftar tugas (draf → konfirmasi manusia → Vikunja)
*Bagian f–g memerlukan Vikunja (5k). Lewati sampai Vikunja terpasang; sementara pakai daftar tindakan dari 5e.*
Setelah 5e: *"Jadikan draf tugas dari daftar tindakan tadi."* `vikunja-tugas` (perintah `dari-teks`)
menyusun draf (judul, penanggung jawab, tenggat) sebagai file lokal — **belum masuk Vikunja**. Tugas baru tercatat hanya
setelah **Anda mengetik "ya"** untuk draf itu. Tugas tanpa penanggung jawab/tenggat jelas
ditandai ⚠️ untuk dilengkapi manusia.
- **Cara cek berhasil:** tugas yang dikonfirmasi muncul di Vikunja; yang tidak dikonfirmasi tidak.
- **Kalau gagal:** Vikunja belum terpasang → lihat 5k; sementara pakai daftar tindakan dari 5e.

### g. Digest tugas tim, 07.00 WIB (terjadwal)
Ketik: *"Kirimi saya tugas hari ini dan yang terlambat tiap pagi."* Dua pesan: tugas hari ini
(07.00) dan tugas terlambat (07.05). Jadwal ini **hanya membaca**, tidak menambah/menyelesaikan
tugas. Fokusnya **pekerjaan macet**, bukan siapa "malas" — gunakan untuk bertanya "apa yang
menghambat?", bukan untuk menghukum.

### h. Notulen rapat (manual)
Tempel catatan/transkrip rapat: *"Buatkan notulen rapat ini."* `notulen-rapat` menyusun
keputusan dan daftar tindakan (siapa – apa – tenggat). Tanggal relatif ("Jumat depan")
dikonversi lewat script. Tugas dari notulen mengikuti aturan yang sama: draf dulu, Anda yang
konfirmasi.

### i. Keuangan & arus kas (manual, bulanan)
- **Rasio keuangan:** *"Analisis rasio dari laporan keuangan ini."* (`analisis-rasio-keuangan-usaha`,
  rasio dihitung script; ini alat baca kondisi, bukan pengganti akuntan/auditor.)
- **Arus kas 13 minggu:** *"Buatkan proyeksi arus kas 13 minggu."* (`arus-kas-13minggu`) —
  untuk melihat minggu mana kas menipis sebelum terjadi.
- **Data Excel:** *"Analisis file Excel ini: penjualan per cabang."* (`analisis-excel`).
- **Presentasi ke atasan/komisaris/bank:** *"Ubah angka ini jadi ringkasan 1 halaman untuk
  direksi."* (`presentasi-data-ke-atasan`.)

### j. Piutang dan stok (terjadwal & manual)
- **Catatan data:** piutang dan stok harus diisi dulu (lihat "isi data awal" di atas).
- **Ringkasan piutang, 07.45 WIB:** *"Aktifkan ringkasan piutang tiap pagi jam 7.45."*
  (`buku-piutang`, nama pelanggan disamarkan jadi inisial.) Draf penagihan dari `tagih-piutang`
  **disalin & dikirim oleh staf keuangan**, tidak pernah otomatis ke pelanggan.
- **Stok menipis, 07.00 WIB:** *"Kirimi saya daftar stok menipis tiap pagi."* (`buku-stok`,
  hanya baca.) Untuk gudang besar, opname tetap dikerjakan manusia; skill menghitung selisihnya.

### k. Daftar tugas Vikunja (perlu dipasang; kerjakan lebih dulu sebelum 5f–5g) — tawarkan jasa setup
`vikunja-tugas` mengoperasikan **Vikunja**, aplikasi daftar tugas sumber terbuka yang jalan di
komputer/server perusahaan Anda (data lokal, tanpa biaya bulanan per pengguna). Pasang
mengikuti `skills/vikunja-tugas/SKILL.md`, atau pakai **jasa setup berbayar Komunitech**. Setelah
terpasang, simpan token API **baca-saja** untuk jadwal otomatis; token baca-tulis hanya untuk
penambahan tugas yang Anda setujui. Tidak berafiliasi dengan pembuat Vikunja.

### l. **[PILIH SATU]** Pembukuan & administrasi (Frappe Books ATAU Dolibarr) — tawarkan jasa setup
- **Frappe Books** (`frappe-books-usaha`): aplikasi akuntansi desktop, cocok untuk usaha yang
  ingin pembukuan sederhana.
- **Dolibarr** (`dolibarr-usaha`): ERP/CRM lebih lengkap (faktur, pelanggan, stok, proyek).
Pilih salah satu sesuai skala (panduan pemilihan di Bab 1). Keduanya perlu dipasang; gunakan **jasa setup berbayar
Komunitech** bila tim Anda tidak punya staf IT. Laporan harian dari salah satunya bisa dikirim
otomatis (`jadwal-openclaw.md` §9). Komunitech tidak berafiliasi dengan pembuat Frappe Books
maupun Dolibarr.

### l2. **[VIP, PILIHAN ERP]** Odoo untuk usaha mapan (`odoo-usaha`) — tawarkan jasa setup
Alternatif ketiga selain Frappe Books/Dolibarr **bila perusahaan sudah memakai Odoo** (Community/
Enterprise/Odoo Online) atau butuh ERP lebih besar. Ketik: *"Kirim laporan harian Odoo jam 9 malam
ke Telegram."* Isi: penjualan hari itu, piutang (nama disamarkan), stok menipis. Memakai kunci
pengguna khusus **Bot Laporan** (bukan admin); jadwal hanya membaca, tidak pernah membuat
penawaran/faktur. Perintah di `jadwal-openclaw.md` §9b. Odoo lokal harus menyala saat jadwal.
Komunitech tidak berafiliasi dengan Odoo S.A.

### l3. **[VIP]** KPI tim (`kpi-tim`) — bulanan tanggal 2, 07.00 WIB (terjadwal)
Ketik: *"Buat KPI untuk tim sales dan gudang saya dari Excel ini."* Agent memilih KPI dari
katalog per peran, membuat rencana (bobot 100%), lalu menghitung skor dari realisasi yang Anda isi
(angka dari script, bukan dikira). Laporan bulanan dikirim **hanya ke pimpinan** di Telegram; skor
per orang **tidak boleh** ke grup karyawan (untuk grup pakai `--tanpa-nama`). KPI = alat
pembinaan, bukan pengawasan. Perintah di `jadwal-openclaw.md` §9c.
- **Cara cek berhasil:** contoh laporan pertama diperlihatkan dan disetujui sebelum jadwal aktif.
- **Kalau gagal:** realisasi periode itu belum diisi, laporan akan bilang "data belum lengkap", bukan angka nol.

### l4. **[VIP]** Peringatan dini operasional (`peringatan-dini-operasional`) — harian 20.00 WIB (terjadwal)
Untuk produksi/distribusi yang punya log harian (output, reject, stok bahan, telat kirim, keluhan).
Ketik: *"Pantau log harian ini dan beri peringatan dini tiap jam 8 malam."* Script menghitung tren,
batas kendali, dan sisa hari stok; yang menyimpang ditandai. Log diisi **satu file tetap** sebelum
jam kirim. Perintah di `jadwal-openclaw.md` §9d. Untuk kejadian besar tetap pakai
`laporan-insiden-usaha` (manual).

### m. Dasbor lokal (opsional)
`dasbor-lokal` membaca (hanya-baca, tidak pernah menulis) database alat Komunitech di komputer
Anda seperti stok dan piutang, lalu menampilkan ringkasan siap pakai; tampilan interaktif di
browser opsional lewat Datasette (perangkat lunak terpisah). Ketik: *"Tampilkan dasbor usaha saya."*

---

## 6. Setelah semua jadwal aktif

- Cek jadwal aktif: *"jadwal apa saja yang aktif?"* (`openclaw automations list --all`).
- Jeda saat libur panjang: *"jeda dulu laporan harian saya."*
- Ulangi `cek-privasi-openclaw` tiap ada kanal/skill baru.
- Data karyawan dan pelanggan di workspace adalah data pribadi pihak ketiga: simpan seperlunya,
  jangan bagikan file ke luar workspace perusahaan.
- Isi `CEKLIS.md` untuk serah-terima.

## Catatan untuk tim Komunitech (bukan untuk member)

- **2026-10-03 (uji gabungan paket):** `slip-gaji-bpjs` dan `pph21-ter` ditambahkan ke skill inti
  §1 (kini 20 skill) karena `hitung-thr` merujuknya dan agent sampai mencari keduanya dengan
  `find /`. Ditambahkan blok "Aturan kantor Komunitech" (§2).
- **Usulan komposisi bundle (perlu persetujuan pemilik, `bundles/` TIDAK diubah):** tambahkan
  `slip-gaji-bpjs` dan `pph21-ter` ke `bundles/paket-kantor-manajemen.txt` (bila belum ada) agar
  pembeli bundle mendapat jalur THR + slip gaji yang lengkap.

## Batasan yang jujur
- Paket ini **bukan** pengganti akuntan, auditor, konsultan pajak, atau penasihat hukum.
- Tidak ada pengawasan karyawan (layar, lokasi, sadap chat pribadi) dan tidak ada penugasan
  otomatis oleh AI.
- Tidak ada broadcast/kirim massal lewat OpenClaw.
- Skill pihak ketiga (Vikunja, Frappe Books, Dolibarr) adalah produk terpisah; Komunitech tidak
  berafiliasi dengannya.
