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
`riset-calon-pelanggan`, `asisten-tulis-riset`, `presentasi-instan`.

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
```
(Jalankan dari folder hasil ekstrak ZIP paket. Windows tanpa WSL: salin folder skill lewat File
Explorer ke `%USERPROFILE%\.openclaw\skills\`.)

- **Cara cek berhasil:** `openclaw skills list` menampilkan ke-10 nama skill di atas.
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

---

## 6. Setelah semua jadwal aktif

- Cek jadwal aktif: *"jadwal apa saja yang aktif?"*
- Jeda sementara (mis. cuti): *"jeda dulu pengingat follow-up saya."*
- Data piutang/klien di `pengingat/DAFTAR.csv` adalah data pribadi pihak ketiga — simpan
  seperlunya, dan jangan bagikan file itu ke luar workspace Anda sendiri.
- Isi `CEKLIS.md` untuk serah-terima.
