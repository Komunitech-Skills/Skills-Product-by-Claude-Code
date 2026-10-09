# Panduan Solusi VIP — Konsultan & Freelancer

Untuk konsultan, agensi kecil, dan freelancer B2B member VIP komunitech.com. Bahasa sehari-hari,
langkah demi langkah.

---

## 0. Prasyarat

1. **OpenClaw sudah terpasang dan bisa diajak chat.** Ketik "halo" untuk memastikan.
2. **Mesin yang menjalankan OpenClaw perlu menyala di jam pengingat.** Untuk konsultan/freelancer
   yang sering bekerja dari laptop yang dibawa-bawa, ini paling sering jadi kendala. Pilih:
   - **(a)** Laptop kerja yang memang menyala tiap pagi jam kerja (mis. 08.00) — cukup untuk
     pengingat pagi, asal laptop tidak dibawa mati total di jam itu.
   - **(b)** Mini PC kecil di rumah/kantor yang menyala 24 jam, terpisah dari laptop kerja yang
     dibawa bepergian.
   - **(c)** VPS milik Anda sendiri — paling stabil untuk yang sering di jalan/klien.
   - **(d)** **Jasa setup berbayar Komunitech** untuk memasang & menguji opsi (b)/(c).
   - **Cara cek berhasil:** Anda tahu mesin mana yang menjalankan Gateway, dan itu **bukan**
     laptop yang sama yang sering Anda tutup/bawa ke luar tanpa koneksi saat jam pengingat.
   - **Kalau gagal/belum yakin:** pilih jam pengingat pagi (mis. 08.00) saat laptop biasanya baru
     dinyalakan dan masih di tempat, bukan sore/malam saat sudah dibawa pergi.

---

## 1. Pasang paket skill Konsultan/Freelancer

Skill: `karyawan-ai-mulai`, `cek-privasi-openclaw`, `proposal-kerjasama`,
`surat-penawaran-harga`, `buat-invoice`, `tagih-piutang`, `pengingat-follow-up`,
`riset-calon-pelanggan`, `asisten-tulis-riset`, `presentasi-instan`, `tender-checklist`,
`kontrak-kerja-pkwt`, `perjanjian-sederhana`, `kebijakan-privasi-pdp`, `kalender-pajak`, `hledger-usaha`, `buku-piutang`,
`laporan-klien-konsultan`, dan (opsional, hanya kalau agensi punya staf tetap) `gaji-umkm`.

```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./proposal-kerjasama --global
openclaw skills install ./surat-penawaran-harga --global
openclaw skills install ./buat-invoice --global
openclaw skills install ./tagih-piutang --global
openclaw skills install ./pengingat-follow-up --global
openclaw skills install ./riset-calon-pelanggan --global
openclaw skills install ./asisten-tulis-riset --global
openclaw skills install ./presentasi-instan --global
openclaw skills install ./tender-checklist --global
openclaw skills install ./kontrak-kerja-pkwt --global
openclaw skills install ./perjanjian-sederhana --global
openclaw skills install ./kebijakan-privasi-pdp --global
openclaw skills install ./kalender-pajak --global
openclaw skills install ./hledger-usaha --global
openclaw skills install ./buku-piutang --global
openclaw skills install ./laporan-klien-konsultan --global
openclaw skills install ./gaji-umkm --global
```
(Jalankan dari folder hasil ekstrak ZIP paket. Windows tanpa WSL: salin folder skill lewat File
Explorer ke `%USERPROFILE%\.openclaw\skills\`. Lewati baris `gaji-umkm` kalau Anda tidak punya
staf tetap yang digaji bulanan.)

- **Cara cek berhasil:** `openclaw skills list` menampilkan 18 nama skill di atas (atau 19 kalau
  memasang `gaji-umkm`).
- **Kalau gagal:** sama seperti paket lain — "already exists" aman dilewati, skill tidak terbaca
  → buka sesi baru, `exec` ditolak → salin manual lewat File Explorer/Finder.

---

## 2. Jalankan `karyawan-ai-mulai`

Ketik: **"mulai karyawan AI, saya konsultan/freelancer"**. Jawab pertanyaan singkat (bidang jasa,
skala tim/solo, 3 pekerjaan paling menyita waktu — biasanya follow-up prospek, bikin proposal,
atau menagih piutang, kanal favorit, privasi/komputer menyala).

- **Cara cek berhasil:** Anda menerima rekomendasi 3 skill pertama + 1 hasil nyata (mis. draf
  proposal atau pesan follow-up) dalam percakapan yang sama.
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

### WAJIB untuk konsultan: tambahkan "Aturan konsultan Komunitech" di bawah blok umum
Uji gabungan 3 Okt 2026 menemukan AI mencari skill perjanjian ke seluruh disk (`find /`) lalu
mematikan prosesnya sendiri. Tempel blok berikut di bawah blok umum di `AGENTS.md` (cara sama seperti di atas):

```markdown
## Aturan konsultan Komunitech (wajib)

Berlaku di SETIAP percakapan, juga saat tidak ada skill yang dibuka. Jelaskan alasannya singkat bila menolak.

1. Skill ada di folder skills OpenClaw. Jangan mencari skill/file ke seluruh disk (`find /`, `locate`), jangan mematikan proses, jangan memeriksa/mengubah config OpenClaw. Bila skill yang dibutuhkan tidak terpasang, katakan dan sarankan memasangnya.
2. Pesan & laporan untuk klien = DRAF untuk konsultan; konsultan yang mengirim. Jangan menawarkan kiriman otomatis ke klien.
3. Draf kontrak/perjanjian/proposal selalu diberi catatan "bukan nasihat hukum — tinjau dengan konsultan hukum". Peringatkan klausul yang tidak wajar (mis. denda harian sangat tinggi) dan beri alternatif yang lazim.
4. Jangan memakai logo, merek, atau testimoni klien tanpa izin tertulis; jangan mengarang testimoni/surat/dokumen.
5. Angka invoice, pajak (PPh 23/PPN), piutang, dan penawaran wajib dari script skill. Ikuti pola nomor invoice yang disebut pengguna.
6. Data tiap klien terpisah; jangan mencampur nama/angka klien lain. Password/token yang ditempel tidak diulang (sebagian maupun utuh) — sarankan segera ganti.
```

- **Cara cek berhasil:** sesi baru, ketik "apa aturan konsultan Komunitech?" — AI menyebut 6 aturan di atas.

---

## 3. Jalankan `cek-privasi-openclaw`

Ketik: **"cek privasi saya"**. Penting khusus untuk konsultan karena Anda menyimpan data klien
(kontak, nilai proyek, piutang) di daftar pantauan lokal (Langkah 5).

- **Cara cek berhasil:** laporan lampu lalu lintas + ringkasan UU PDP untuk data klien.
- **Kalau gagal:** ikuti fallback salin-tempel.

---

## 4. Hubungkan bot Telegram

Sama seperti paket lain: @BotFather → `openclaw channels add --channel telegram --token <token>`
→ kirim "halo" ke bot → setujui pairing → catat ID chat lewat @userinfobot.

- **Cara cek berhasil:** bot membalas, ID chat tercatat di catatan pribadi Anda.
- **Kalau gagal:** lihat langkah setara di `toko-online/PANDUAN.md` §4.

WhatsApp untuk konsultan hanya untuk pengingat ke **diri sendiri**, nomor terpisah, dengan
persetujuan risiko tertulis — lihat `jadwal-openclaw.md`. **Tidak pernah** untuk mengirim
tagihan/follow-up otomatis langsung ke klien lewat WA Web.

---

## 5. Rutinitas Konsultan/Freelancer

### a. Daftar pantauan follow-up, piutang, dan timesheet
Sebelum jadwal bisa jalan, isi daftar sekali: ketik ke bot, mis. *"Ingatkan saya follow-up Bu
Rina tanggal 3 kalau belum bayar Rp4,5 juta"* — ini otomatis ditambahkan ke
`pengingat/DAFTAR.csv` di workspace Anda. Untuk klien dengan tagihan jam kerja, isi juga
`pengingat/timesheet.csv` (atau kirim Excel/CSV yang sudah ada).
- **Cara cek berhasil:** ketik "tampilkan daftar pantauan saya" — item yang baru ditambahkan
  muncul.
- **Kalau gagal:** kalau formatnya aneh (tanggal "3 Okt" atau nominal "4,5 jt"), skill akan
  menafsirkannya dan **menunjukkan hasil tafsirannya untuk dikonfirmasi** sebelum disimpan —
  jangan biarkan tersimpan kalau tafsirannya salah.

### b. Pengingat follow-up & piutang harian, jam 08.00 WIB (terjadwal)
Ketik: *"Aktifkan pengingat follow-up harian jam 8 pagi."* Tiap pagi Anda menerima: yang jatuh
tempo hari ini, yang terlambat, dan H-1, masing-masing **dengan draf pesan siap kirim** (dari
`follow-up-prospek`/`tagih-piutang`). **Anda yang menyalin & mengirim** ke klien — bot tidak
pernah mengirim langsung ke klien.
- **Cara cek berhasil:** jadwal diuji sekali (`automations run --wait`) dan hasilnya ditunjukkan
  sebelum jadwal dinyatakan aktif.
- **Kalau gagal:** kalau daftar masih kosong, rekap akan bilang "belum ada item jatuh tempo" —
  bukan error.

### c. Rekap timesheet klien, Jumat jam 16.00 WIB (terjadwal)
Ketik: *"Kirimi saya rekap timesheet tiap Jumat sore."* Anda menerima total jam & nilai per
klien plus draf pesan ke klien — **Anda yang menyetujui dan mengirim**.

### d. Pengingat sekali jalan untuk janji spesifik
Untuk janji telepon/meeting yang tidak berulang: *"Ingatkan saya telepon Pak Budi besok jam 9
pagi soal follow-up #3."* — ini otomasi sekali jalan (`--at`), otomatis terhapus setelah
dijalankan.

### e. Proposal, penawaran, invoice — manual, dipicu Anda
Ketika ada calon klien baru: *"Buatkan proposal kerja sama untuk [nama proyek]"* /
*"Buatkan surat penawaran harga untuk [klien]"* / *"Buatkan invoice untuk [klien], item: ..."*.
Ini bukan jadwal otomatis — dipakai kapan pun Anda butuh, satu per satu.

### f. Riset calon pelanggan & materi tertulis — manual
`riset-calon-pelanggan` untuk menyusun profil pelanggan ideal & daftar calon klien dari sumber
publik. `asisten-tulis-riset` untuk artikel/materi presentasi berbasis riset dengan sitasi.
`presentasi-instan` untuk membuat slide HTML siap pakai dari materi yang sudah ada.

### g. Ikut tender/pengadaan pemerintah (manual, dipicu Anda)
Kalau Anda/agensi ingin ikut tender/lelang pemerintah (LPSE/SPSE, e-katalog), ketik: *"Saya mau
ikut tender pengadaan jasa desain di LPSE kabupaten, apa saja yang harus disiapkan?"*
`tender-checklist` membantu menilai **layak ikut atau tidak**, menyiapkan checklist dokumen,
jadwal mundur dari batas unggah, dan **memeriksa rincian harga penawaran** (dihitung script,
termasuk PPN) supaya tidak gugur karena hitungan salah.
- **Kalau gagal:** kalau Anda belum tahu HPS/pagu paket, skill tetap membantu checklist &
  kelayakan; hanya bagian cek harga yang menunggu data itu.

### h. Kontrak kerja staf/asisten kontrak (manual, dipicu Anda)
Merekrut asisten atau staf admin dengan status kontrak? Ketik: *"Buatkan kontrak kerja 6 bulan
untuk asisten riset saya."* `kontrak-kerja-pkwt` menyusun draf PKWT sesuai aturan dan menghitung
kompensasi akhir kontrak — bukan untuk kontrak kerja sama dengan klien (itu `proposal-kerjasama`/
gunakan `perjanjian-sederhana`).

### i. Kebijakan privasi untuk layanan/website Anda (manual, dipicu Anda)
Kalau Anda mengumpulkan data klien lewat website/formulir/WA Business, ketik: *"Buatkan kebijakan
privasi untuk jasa konsultan saya."* `kebijakan-privasi-pdp` juga bisa membuat kalimat persetujuan
data untuk formulir/Google Form, atau mengecek kebijakan yang sudah ada.

### j. Kalender pajak & pengingat jatuh tempo (terjadwal, opsional)
Ketik: *"Ingatkan saya jadwal pajak bulanan lewat Telegram."* `kalender-pajak` menyusun tanggal
pasti setor/lapor (PPh, PPN bila PKP) sesuai profil pajak Anda, sudah digeser bila jatuh di hari
libur — **bukan** penghitung besaran pajak. Cara mengaktifkan pengingat otomatisnya:
`jadwal-openclaw.md` §8.
- **Cara cek berhasil:** jadwal diuji sekali dan hasilnya (tanggal-tanggal nyata, bukan contoh)
  ditunjukkan sebelum dinyatakan aktif.

### k. Laporan pembukuan bulanan (hledger-usaha, terjadwal, tanggal 1 jam 07.50 WIB)
Untuk pembukuan berpasangan (debit/kredit) tanpa aplikasi berbayar — cocok kalau Anda/agensi
ingin laporan laba rugi & neraca yang benar secara akuntansi, bukan sekadar catatan kas. Ketik:
*"Aktifkan laporan bulanan pembukuan tiap tanggal 1 jam 7.50 pagi."*
- **Cara cek berhasil:** jadwal diuji sekali, hasilnya (laba rugi bulan lalu) ditunjukkan sebelum
  aktif.
- **Kalau gagal:** jurnal belum ada/neraca tidak seimbang → skill akan bilang jujur (kode keluar
  sengaja gagal) — perbaiki dulu pencatatan sebelum percaya laporannya.

### l. Ringkasan piutang retainer/termin (buku-piutang, terjadwal, 07.45 WIB)
Punya klien retainer/termin yang belum lunas? Ketik: *"Aktifkan ringkasan piutang klien jam 7.45
pagi."* Sama seperti paket lain, nama klien **disamarkan jadi inisial secara default**.
- **Cara cek berhasil:** jadwal diuji sekali, hasilnya ditunjukkan sebelum aktif.
- **Kalau gagal:** database piutang belum ada → catat piutang pertama dulu.

### m. Pengingat gaji & setoran staf tetap (gaji-umkm, opsional, terjadwal 07.00 WIB)
**Hanya kalau agensi/kantor Anda punya staf tetap yang digaji bulanan** (bukan honor per proyek —
untuk itu tetap pakai `buat-invoice`/kesepakatan proyek). Ketik: *"Aktifkan pengingat gaji &
setoran BPJS/PPh 21 tiap pagi jam 7."* Anda menerima pengingat tenggat (tanggal gajian, BPJS,
PPh 21) berisi **total perusahaan saja**, tanpa nama/NIK/rekening karyawan.
- **Cara cek berhasil:** jadwal diuji sekali, hasilnya ditunjukkan sebelum aktif.
- **Kalau tidak punya staf tetap:** lewati langkah ini, tidak perlu memasang skillnya.

### n. Draf laporan progres ke klien (laporan-klien-konsultan, terjadwal, Jumat 16.00 WIB)
Ini mengisi celah "laporan status ke klien" yang sebelumnya belum ada polanya. Cocok kalau Anda
mencatat pekerjaan harian per klien (jam, status, kendala) dan ingin draf laporan progres
mingguan/bulanan disiapkan otomatis — **bukan** dikirim otomatis ke klien. Ketik: *"Catat: hari
ini saya kerjakan rekonsiliasi bank untuk PT Maju, 2,5 jam, selesai"* setiap kali selesai
mengerjakan sesuatu, lalu: *"Aktifkan draf laporan mingguan untuk PT Maju tiap Jumat jam 4
sore."*
- **Cara cek berhasil:** jadwal diuji sekali, draf laporan (versi email, WA, dan markdown)
  ditunjukkan sebelum dinyatakan aktif.
- **Satu klien = satu jadwal.** Untuk beberapa klien, ulangi dengan jam berbeda-beda (mis.
  16.00, 16.10, 16.20) agar tidak menumpuk.
- **Draf ini hanya terkirim ke Anda.** Anda yang meninjau lalu menyalin ke email/WA klien —
  tidak pernah otomatis ke klien.

### o. Merek, positioning & harga jasa Anda (manual, dipicu Anda)
Semua skill di bawah dipicu satu kalimat; tanpa jadwal. Pasang: `openclaw skills install ./<nama> --global`.
- **`strategi-merek-usaha`:** *"Bantu saya menamai agensi baru dan merumuskan penawarannya."* Isi:
  10 opsi nama dengan skor, cek arti negatif, panduan cek domain/handle/merek DJKI.
- **`positioning-persona-usaha`:** *"Susun persona klien ideal dan positioning saya."* Hasil: segmen
  berskor, value proposition, tagline, message house untuk profil/proposal.
- **`analisis-pesaing-strategis`:** *"Bandingkan saya dengan 3 agensi pesaing."* Dari halaman
  publik atau teks yang Anda tempel.
- **`strategi-harga-produk`:** untuk tarif jasa: paket good-better-best, retainer, diskon yang aman.
  Hasilnya masuk ke `surat-penawaran-harga` dan `proposal-kerjasama`.
- **`rencana-marketing-usaha`:** rencana kuartalan untuk mendapat klien (kanal, anggaran, target).
- **Cara cek berhasil:** ada dokumen siap pakai, bukan saran umum. **Kalau gagal:** jawab pertanyaan
  singkat yang diajukan agent (sekali, dalam satu pesan).
- Komunikasi ke calon klien tetap draf yang **Anda kirim sendiri**, bukan kirim massal.

---

## 6. Setelah semua jadwal aktif

- Cek jadwal aktif: *"jadwal apa saja yang aktif?"*
- Jeda sementara (mis. cuti): *"jeda dulu pengingat follow-up saya."*
- Data piutang/klien di `pengingat/DAFTAR.csv` adalah data pribadi pihak ketiga — simpan
  seperlunya, dan jangan bagikan file itu ke luar workspace Anda sendiri.
- Isi `CEKLIS.md` untuk serah-terima.
