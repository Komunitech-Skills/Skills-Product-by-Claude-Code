# Jadwal OpenClaw siap salin — Toko Online

Semua perintah di bawah diambil/diturunkan dari `references/openclaw*.md` skill terkait
(`laporan-otomatis-terjadwal`, `buku-stok`, `konten-mingguan`, `agen-cs-toko`), yang sudah
diverifikasi lewat `--help` OpenClaw **2026.9.5/2026.9.6**, dan sebagian **dijalankan sungguhan**
terhadap Gateway lokal uji. Untuk sesi penyusunan paket ini, **flag-flag yang dipakai di bawah
diverifikasi ulang** dengan menjalankan `bash scripts/uji_openclaw.sh 2026.9.6` lalu memeriksa
`openclaw automations add --help` dan `openclaw channels add --help` sungguhan di OpenClaw
**2026.9.6 (eb377ac)** — semua flag (`--cron`/argumen posisi, `--tz`, `--name`, `--session`,
`--announce`, `--channel`, `--to`, `--tools`, `--best-effort-deliver`, `--model`) **cocok
persis** dengan yang tertulis di `--help`. **Tidak ada perintah baru yang ditebak** untuk
dokumen ini.

Legenda: ✅ = benar-benar dijalankan terhadap Gateway nyata (dicatat di skill sumber). 📖 = dicek
lewat `--help`/`config schema` (termasuk verifikasi ulang sesi ini), kombinasi utuhnya belum
dicoba ujung-ke-ujung. ⚠️ = belum diverifikasi sama sekali.

**Sebelum menjalankan apa pun:** tunjukkan ringkasan ke pemilik toko dan tanya "Lanjut?
(ya/tidak)". Ganti `<ID chat Telegram pemilik>` dengan angka nyata dari Langkah 4 `PANDUAN.md`.
Semua jadwal di bawah mengirim **hanya ke pemilik**, tidak pernah ke grup/pelanggan.

## 1. Laporan toko harian, jam 21.00 WIB ✅/📖

Kalau memakai `buku-stok` untuk stok (disarankan — laporannya sudah mencakup omzet, stok
menipis, barang tidak laku, nilai persediaan dalam satu pesan) — bentuk ini **diverifikasi lewat
`--help`** di dokumentasi `buku-stok/SKILL.md` (flag intinya sama dengan yang **dijalankan
sungguhan** ✅ oleh `laporan-otomatis-terjadwal`):
```bash
openclaw automations add --name "Laporan stok & omzet harian" --cron "0 21 * * *" \
  --tz "Asia/Jakarta" --session isolated --tools exec,read \
  --message "Pakai skill buku-stok: jalankan laporan ringkas hari ini (hanya baca, jangan jalankan perintah tulis atau --ya) lalu kirim teksnya apa adanya dalam Bahasa Indonesia." \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

Kalau sumber data Anda adalah **file ekspor penjualan CSV/Excel** (marketplace/kasir) tanpa
`buku-stok`, pakai pola `laporan-otomatis-terjadwal` — **Bentuk A, flag intinya ✅ dijalankan
sungguhan** di Gateway uji:
```bash
openclaw automations add "0 21 * * *" \
  "Jalankan resep laporan/RESEP-penjualan-harian.md untuk hari ini (pakai rekap-penjualan-csv). Tulis dalam Bahasa Indonesia, maksimal 12 baris, sebutkan jika data belum ada — jangan mengarang angka." \
  --tz "Asia/Jakarta" --name "Laporan penjualan harian" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- `--tz "Asia/Jakarta"` wajib eksplisit — tanpa ini cron memakai zona waktu komputer Gateway.
- `--tools exec,read` (dipakai contoh `buku-stok`) membatasi jadwal hanya boleh membaca laporan,
  **tidak boleh** menjalankan transaksi tulis (`--ya`).
- Uji dulu sebelum percaya jadwal aktif: `openclaw automations run <id> --wait` (✅, `<id>`
  didapat dari field `"id"` hasil `add`, **wajib** UUID — memakai nama pada `run` gagal dengan
  pesan `Automation not found`, dibuktikan di Gateway uji).

## 2. Stok menipis terpisah (opsional, kalau tidak digabung ke laporan harian) 📖
```bash
openclaw automations add --name "Laporan stok menipis" --cron "0 8 * * *" --tz "Asia/Jakarta" \
  --session isolated --tools exec,read \
  --message "Pakai skill buku-stok: jalankan laporan menipis (hanya baca) dan kirim daftarnya apa adanya." \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 3. Paket konten mingguan — Jumat jam 16.00 WIB ✅/📖
Flag inti sama dengan §1 (dikonfirmasi via `--help` sesi ini, dan sudah diuji sungguhan lewat
`laporan-otomatis-terjadwal`):
```bash
openclaw automations add "0 16 * * 5" \
  "Jalankan skill konten-mingguan untuk minggu depan memakai profil di konten/PROFIL.md. Tulis paket lengkap dalam Bahasa Indonesia, simpan arsip ke konten/minggu-<label>.md, lalu kirimkan ringkasan per hari." \
  --tz "Asia/Jakarta" --name "Paket konten Jumat sore" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 4. Pengingat posting harian, jam 08.00 WIB ✅/📖
```bash
openclaw automations add "0 8 * * *" \
  "Baca konten/minggu-<label minggu berjalan>.md, ambil bagian untuk HARI INI saja, lalu kirim ringkas: platform, hook, dan caption siap tempel hari ini. Kalau arsip minggu ini belum ada, katakan itu apa adanya, jangan mengarang." \
  --tz "Asia/Jakarta" --name "Pengingat posting harian" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
**Ingat:** ini hanya menyiapkan & mengingatkan. OpenClaw **tidak** memposting otomatis ke
Instagram/TikTok/Facebook (tidak ada plugin/kanal resmi untuk itu).

## 5. Rekap harian CS (mode Copilot), jam 20.00 WIB 📖
```bash
openclaw automations add \
  --cron "0 20 * * *" --tz "Asia/Jakarta" \
  --name "Rekap CS harian" \
  --message "Baca isi file cs/log/<tanggal hari ini>.md di workspace. Ringkas: jumlah chat dibalas, 5 kategori pertanyaan terbanyak, daftar yang dieskalasi, dan pertanyaan yang belum ada di cs/PENGETAHUAN.md. Jika file belum ada/kosong, katakan belum ada aktivitas hari ini, jangan mengarang angka. Bahasa Indonesia, maksimal 15 baris." \
  --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Log `cs/log/<tanggal>.md` **tidak boleh** berisi nama/nomor HP/alamat/isi chat lengkap pelanggan —
hanya kategori & ringkasan pertanyaan (lihat aturan di `skills/agen-cs-toko/references/eskalasi-dan-kanal.md` §3a).

## 6. Mengelola jadwal (semua ✅, dibuktikan di Gateway uji)
```bash
openclaw automations list --all                     # semua jadwal + id
openclaw automations show "<nama persis>"           # show boleh pakai nama ATAU id
openclaw automations run <id> --wait                # uji sekarang sebelum percaya "aktif"
openclaw automations disable <id>                   # jeda (hanya id, BUKAN nama)
openclaw automations enable <id>                     # aktifkan lagi (hanya id)
openclaw automations edit <id> --cron "0 22 * * *" --tz "Asia/Jakarta"   # ubah jam (hanya id)
openclaw automations rm <id>                         # hapus permanen (hanya id, tak bisa dibatalkan)
```
`run`/`disable`/`enable`/`edit`/`rm` **wajib** pakai `id` (UUID dari hasil `add`) — memakai nama
di perintah-perintah ini ditolak dengan `Automation not found: <nama>`.

## WhatsApp (hanya bila syarat berikut semua terpenuhi)
1. **Nomor terpisah** — bukan nomor toko/CS yang dikenal pelanggan.
2. Hanya mengirim ke **pemilik sendiri**.
3. Persetujuan risiko tertulis, contoh kalimat: *"OpenClaw memakai WhatsApp Web (tidak resmi,
   lewat scan QR). Syarat Layanan WhatsApp melarang pesan otomatis/massal, jadi nomor bisa
   diblokir. Untuk kirim ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya
   risiko ini. Saya mengerti risikonya."*
4. Jalankan `cek-privasi-openclaw` setelah nomor WA ditautkan, untuk memastikan
   `dmPolicy: "allowlist"` (bukan `pairing`/`open`) dan `allowFrom` hanya berisi nomor pemilik.

Ganti baris terakhir tiap perintah `add` di atas menjadi
`--announce --channel whatsapp --to "+62<nomor pemilik>"`. Status: `add` dengan
`--channel whatsapp` **diterima** ✅ walau plugin belum terpasang, tapi pengiriman nyata ke WA
⚠️ belum diverifikasi ujung-ke-ujung oleh tim kurasi.

## Yang BELUM diverifikasi ujung-ke-ujung ⚠️
- Membuat jadwal di atas langsung lewat chat WhatsApp/Telegram (pengguna mengetik "aktifkan
  laporan jam 9 malam" di chat, bukan lewat terminal/Control UI). Dukungannya ada di dokumentasi
  resmi, tapi belum dicoba tim kami. Kalau gagal/aneh, jalankan perintah yang sama dari terminal
  atau Control UI (`Settings → Automations`).
- Pesan benar-benar tiba di Telegram/WhatsApp pembeli (uji internal tidak memakai token bot/nomor
  asli — hanya struktur job yang diverifikasi).
- Perilaku agent AI sungguhan menjalankan skill di dalam job terjadwal (uji internal tidak
  memakai API key model).
