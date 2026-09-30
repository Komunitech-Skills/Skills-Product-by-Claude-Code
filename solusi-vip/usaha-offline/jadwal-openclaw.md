# Jadwal OpenClaw siap salin — Usaha Offline (Kafe/Warung/Toko Fisik/Bengkel/Laundry)

Semua perintah di bawah diambil/diturunkan **persis** dari `references/openclaw-jadwal.md` skill
terkait (`laporan-harian-usaha`, `kasir-lokal`, `kas-umkm`, `absensi-lokal`, `gaji-umkm`,
`buku-piutang`), yang sudah diverifikasi lewat `--help`/Gateway lokal OpenClaw **2026.9.5/2026.9.6**
oleh tim kurasi masing-masing skill. **Tidak ada perintah atau flag baru yang ditebak** untuk
dokumen ini — hanya menggabungkan pola yang sudah ada dan mengganti jam/periode sesuai kebutuhan
usaha offline (mis. `--periode minggu-lalu` pada `buku-piutang`, yang memang tercantum sebagai
nilai valid di `skills/buku-piutang/references/perintah.md`).

Legenda: ✅ = benar-benar dijalankan terhadap Gateway nyata (dicatat di skill sumber). 📖 = dicek
lewat `--help`/`config schema`, kombinasi utuhnya (terutama pengiriman sungguhan ke
Telegram/WhatsApp) belum dicoba ujung-ke-ujung. ⚠️ = belum diverifikasi sama sekali.

**Sebelum menjalankan apa pun:** tunjukkan ringkasan ke pemilik usaha dan tanya "Lanjut?
(ya/tidak)". Ganti `<ID chat Telegram pemilik>` (atau `<chat-id-telegram-pemilik>`) dengan angka
nyata dari Langkah 4 `PANDUAN.md`, dan `/home/NAMA/...` dengan path asli hasil perintah
`python3 -c "import os; print(os.path.expanduser(...))"` di komputer pemilik (argv **tidak**
mengenal `~`). Semua jadwal di bawah mengirim **hanya ke pemilik**, tidak pernah ke
grup/pelanggan/karyawan.

## 1. Laporan usaha harian gabungan, jam 21.00 WIB (kasir + stok + karyawan) ✅/📖
Diambil dari `skills/laporan-harian-usaha/references/openclaw-jadwal.md` (flag inti ✅ dijalankan
sungguhan di Gateway uji):
```bash
openclaw automations add --name "Laporan harian usaha" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/laporan-harian-usaha/scripts/laporan.py"]' \
  --command-cwd "/home/NAMA/.openclaw/workspace" \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- Pasang dulu `kasir-lokal`, `buku-stok`, `absensi-lokal` di folder skill yang sama — alat yang
  tidak terpasang dilewati dengan catatan, bukan error.
- Toko tutup lewat tengah malam: jadwalkan `--cron "0 7 * * *"` dan tambahkan `"--tanggal","kemarin"`
  ke dalam argv.
- Uji dulu sebelum percaya jadwal aktif: `openclaw automations run <id> --wait` (`<id>` dari field
  `"id"` hasil `add`, **wajib** UUID).

## 2. Ringkasan buku kas harian, jam 21.00 WIB (kas-umkm) 📖
Diambil dari `skills/kas-umkm/references/openclaw-jadwal.md`:
```bash
openclaw automations add --name "Ringkasan kas harian" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/kas-umkm/scripts/kas.py","rekap","--tanggal","hari-ini"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Ini **pesan terpisah** dari laporan (1) — `laporan-harian-usaha` belum membaca database `kas-umkm`.

## 3. Stok menipis, jam 07.00 WIB (opsional, terpisah dari laporan malam) 📖
Diambil dari `skills/kasir-lokal`/`skills/laporan-otomatis-terjadwal` (pola sama yang dipakai di
`solusi-vip/toko-online/jadwal-openclaw.md` §2, ✅ dijalankan sungguhan untuk bentuk agent ini):
```bash
openclaw automations add --name "Laporan stok menipis" --cron "0 7 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill buku-stok: jalankan laporan menipis (hanya baca) dan kirim daftarnya apa adanya." \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 4. Rekap absensi harian, jam 10.00 WIB (opsional) ✅/📖
Diambil dari `skills/absensi-lokal/references/openclaw-jadwal.md`. Usaha pola 6 hari kerja
(kebanyakan kafe/warung/bengkel):
```bash
openclaw automations add --name "Absensi harian" --cron "0 10 * * 1-6" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/absensi-lokal/scripts/absensi.py","harian"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Usaha pola 5 hari: ganti `1-6` menjadi `1-5`.

## 5. Pengingat gajian, BPJS & PPh 21, jam 07.00 WIB setiap hari ✅/📖
Diambil dari `skills/gaji-umkm/references/openclaw-jadwal.md` (tenggat 3 hari ke depan; hari tanpa
tenggat tetap mengirim satu baris "Tidak ada tenggat ..."):
```bash
openclaw automations add --name "Pengingat gaji & setoran" --cron "0 7 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/gaji-umkm/scripts/gaji.py","pengingat","--rentang","3"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Kalau terlalu sering, ganti cron ke tanggal-tanggal tertentu saja (mis. sekitar tanggal gajian,
BPJS tgl 10, PPh 21 tgl 15/20): `--cron "0 7 7,12,17,22 * *"` dengan `--rentang 5`.

## 6. Ringkasan piutang harian, jam 07.45 WIB (opsional, kalau punya pelanggan bon/langganan) 📖
Diambil dari `skills/buku-piutang/references/openclaw-jadwal.md` (disamarkan secara default):
```bash
openclaw automations add --name "Ringkasan piutang harian" --cron "45 7 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/buku-piutang/scripts/piutang.py","ringkasan","--samarkan"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 7. Rekap piutang mingguan, Senin jam 07.50 WIB (opsional) 📖
Sama seperti §6, memakai perintah `rekap` dengan nilai `--periode` yang terdaftar di
`skills/buku-piutang/references/perintah.md` (`minggu-lalu` valid; contoh referensi memakai
`bulan-lalu`, di sini diganti mingguan dan cron-nya Senin pagi):
```bash
openclaw automations add --name "Rekap piutang mingguan" --cron "50 7 * * 1" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/buku-piutang/scripts/piutang.py","rekap","--periode","minggu-lalu","--samarkan"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 8. Mengelola jadwal (semua ✅, dibuktikan di Gateway uji oleh skill-skill sumber)
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

## 9. Skill tambahan (referral, harga, masukan pelanggan, rencana marketing): tanpa jadwal
Dipicu manual (lihat `PANDUAN.md` §5m). Tidak ada jadwal baru dan tidak ada kiriman massal ke pelanggan.

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
`--channel whatsapp` **diterima** ✅ di skill sumber walau plugin belum terpasang, tapi pengiriman
nyata ke WA ⚠️ belum diverifikasi ujung-ke-ujung oleh tim kurasi.

## Yang BELUM diverifikasi ujung-ke-ujung ⚠️
- Membuat jadwal di atas langsung lewat chat WhatsApp/Telegram (mengetik "aktifkan laporan jam 9
  malam" di chat, bukan lewat terminal/Control UI). Dukungannya ada di dokumentasi resmi, tapi
  belum dicoba tim kami. Kalau gagal/aneh, jalankan perintah yang sama dari terminal atau Control
  UI (`Settings → Automations`).
- Pesan benar-benar tiba di Telegram/WhatsApp pembeli (uji internal tidak memakai token bot/nomor
  asli — hanya struktur job yang diverifikasi per skill sumber).
- Perilaku agent AI sungguhan menjalankan skill di dalam job terjadwal (uji internal tidak
  memakai API key model), kecuali bagian yang sudah dicatat ✅ di skill sumber.
- Kombinasi jadwal §7 (`buku-piutang rekap --periode minggu-lalu`) — nilai `--periode` terdaftar
  resmi di `references/perintah.md` skill itu, tapi kombinasi persis untuk jadwal mingguan belum
  dicoba di Gateway oleh tim kurasi (baru §6 harian yang dicoba).
