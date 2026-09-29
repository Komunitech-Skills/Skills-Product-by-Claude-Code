# Panduan Solusi VIP — Kantor & Manajemen

Untuk direktur/manajer perusahaan manufaktur, distribusi, logistik, dan kantor yang lebih besar
(sekitar 16–50+ karyawan) yang sudah jadi member VIP komunitech.com. Bahasa sehari-hari, langkah
demi langkah. Setiap langkah punya **cara cek berhasil** dan **kalau gagal**.

Kalau ragu di satu langkah, berhenti di situ dan tanya ke grup member/Komunitech — jangan menebak.

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
   - **Kalau belum yakin:** mulai dari (a) dengan laporan jam kerja saja.

---

## 1. Pasang paket skill Kantor & Manajemen

Skill inti: `karyawan-ai-mulai`, `cek-privasi-openclaw`, `laporan-otomatis-terjadwal`,
`laporan-harian-usaha`, `laporan-status-kantor`, `ringkas-grup-wa`, `notulen-rapat`,
`analisis-excel`, `analisis-rasio-keuangan-usaha`, `arus-kas-13minggu`,
`presentasi-data-ke-atasan`, `buku-piutang`, `tagih-piutang`, `buku-stok`,
`laporan-insiden-usaha`, `dasbor-lokal`.
Skill yang butuh aplikasi tambahan (Bab 5k–5l): `vikunja-tugas`, dan salah satu dari
`frappe-books-usaha` atau `dolibarr-usaha`.

```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./laporan-otomatis-terjadwal --global
openclaw skills install ./laporan-harian-usaha --global
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
openclaw skills install ./vikunja-tugas --global
openclaw skills install ./frappe-books-usaha --global
openclaw skills install ./dolibarr-usaha --global
```
(Jalankan dari folder hasil ekstrak ZIP paket. Pasang **salah satu** dari `frappe-books-usaha`/
`dolibarr-usaha`, bukan dua-duanya. Windows tanpa WSL: salin folder skill lewat File Explorer
ke `%USERPROFILE%\.openclaw\skills\`. Lihat `docs/instalasi.md`.)

**Penting:** `laporan-harian-usaha` membaca database `buku-stok` dengan mencari skill itu **di
folder skills yang sama** — pasang semuanya sekaligus.

- **Cara cek berhasil:** `openclaw skills list` menampilkan semua nama di atas.
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
1. Di Telegram cari **@BotFather**, kirim `/newbot`, beri nama, salin **token**.
2. Jalankan:
   ```bash
   openclaw channels add --channel telegram --token <token-dari-BotFather>
   ```
3. Kirim "halo" ke bot Anda (memicu **pairing**).
4. Setujui: `openclaw pairing list telegram`, lalu `openclaw pairing approve telegram <KODE>`
   (berlaku 1 jam).
5. Catat **ID chat** Anda lewat **@userinfobot**. Angka ini dipakai di semua jadwal.

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

### a. Laporan harian manajemen, 21.00 WIB (terjadwal)
Ketik: *"Aktifkan laporan harian usaha jam 9 malam ke Telegram saya."* `laporan-harian-usaha`
merangkum penjualan/stok (dan modul lain yang terpasang) apa adanya, angka dihitung script.
Untuk perusahaan yang datanya ada di Frappe Books/Dolibarr, lihat 5l.
- **Cara cek berhasil:** jadwal diuji sekali (`automations run <id> --wait`) dan teks laporan
  ditunjukkan sebelum dinyatakan aktif.
- **Kalau gagal:** data belum ada → laporan bilang kosong, bukan error; isi data dulu.

### b. Laporan mingguan manajemen, Senin 07.00 WIB (terjadwal)
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
- **Ringkasan piutang, 07.45 WIB:** *"Aktifkan ringkasan piutang tiap pagi jam 7.45."*
  (`buku-piutang`, nama pelanggan disamarkan jadi inisial.) Draf penagihan dari `tagih-piutang`
  **disalin & dikirim oleh staf keuangan**, tidak pernah otomatis ke pelanggan.
- **Stok menipis, 07.00 WIB:** *"Kirimi saya daftar stok menipis tiap pagi."* (`buku-stok`,
  hanya baca.) Untuk gudang besar, opname tetap dikerjakan manusia; skill menghitung selisihnya.

### k. Daftar tugas Vikunja (perlu dipasang) — tawarkan jasa setup
`vikunja-tugas` mengoperasikan **Vikunja**, aplikasi daftar tugas sumber terbuka yang jalan di
komputer/server perusahaan Anda (data lokal, tanpa biaya bulanan per pengguna). Pasang
mengikuti `skills/vikunja-tugas/SKILL.md`, atau pakai **jasa setup berbayar Komunitech**. Setelah
terpasang, simpan token API **baca-saja** untuk jadwal otomatis; token baca-tulis hanya untuk
penambahan tugas yang Anda setujui. Tidak berafiliasi dengan pembuat Vikunja.

### l. Pembukuan & administrasi (Frappe Books atau Dolibarr) — tawarkan jasa setup
- **Frappe Books** (`frappe-books-usaha`): aplikasi akuntansi desktop, cocok untuk usaha yang
  ingin pembukuan sederhana.
- **Dolibarr** (`dolibarr-usaha`): ERP/CRM lebih lengkap (faktur, pelanggan, stok, proyek).
Pilih salah satu sesuai skala. Keduanya perlu dipasang; gunakan **jasa setup berbayar
Komunitech** bila tim Anda tidak punya staf IT. Laporan harian dari salah satunya bisa dikirim
otomatis (`jadwal-openclaw.md` §9). Komunitech tidak berafiliasi dengan pembuat Frappe Books
maupun Dolibarr.

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

## Batasan yang jujur
- Paket ini **bukan** pengganti akuntan, auditor, konsultan pajak, atau penasihat hukum.
- Tidak ada pengawasan karyawan (layar, lokasi, sadap chat pribadi) dan tidak ada penugasan
  otomatis oleh AI.
- Tidak ada broadcast/kirim massal lewat OpenClaw.
- Skill pihak ketiga (Vikunja, Frappe Books, Dolibarr) adalah produk terpisah; Komunitech tidak
  berafiliasi dengannya.
