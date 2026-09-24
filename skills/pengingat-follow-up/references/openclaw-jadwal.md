# Jadwal otomatis di OpenClaw — pengingat follow-up

**Status verifikasi.** Semua perintah di bawah diuji di OpenClaw **2026.9.5 (ec9c1a1)** dan diuji ulang di
**2026.9.6 (eb377ac)** (24 Sep 2026, hasil sama), dengan HOME sementara. Lingkungan uji: Gateway lokal `gateway run --dev --allow-unconfigured --bind loopback`,
tanpa model AI sungguhan dan tanpa kanal yang login.
- ✅ = **dijalankan sungguhan** di Gateway uji (job terbentuk, jadwal & zona waktu dicek dari hasil JSON).
- 📖 = hanya dicek lewat `--help`.
- ⚠️ = **belum bisa diverifikasi**. Beri tahu pengguna jika bagian ini dipakai.

Yang **belum** teruji sampai ujung: pesan benar-benar tiba di Telegram/WhatsApp (uji tidak memakai
token bot/nomor asli) dan agent AI menjalankan skill ini di dalam job (uji tidak memakai API key model).
Jika versi OpenClaw pengguna berbeda dan sebuah opsi ditolak, jalankan dulu `openclaw automations add --help`.

**Fallback:** jika perintah komputer (`exec`) tidak diizinkan, atau pengguna memakai Claude Code/Codex/Cursor
(tanpa Gateway), tampilkan perintah sebagai teks siap salin-tempel, atau arahkan ke Control UI (`Settings → Automations`).
Tanpa jadwal pun skill tetap berguna. Pengguna cukup mengetik "rekap pengingat" setiap pagi.

## 0. Aturan kanal (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default** untuk rekap ke pemilik.
- **WhatsApp** hanya boleh jika SEMUA syarat ini terpenuhi:
  1. Memakai **nomor terpisah** milik pemilik (bukan nomor toko/CS).
  2. Rekap hanya dikirim ke pemilik sendiri.
  3. Ada persetujuan risiko tertulis, yaitu pengguna membalas "ya, saya mengerti risikonya" setelah membaca:
     *"OpenClaw memakai WhatsApp Web (tidak resmi, lewat scan QR). Syarat Layanan WhatsApp melarang
     pesan otomatis/massal, jadi nomor bisa diblokir. Untuk rekap ke diri sendiri risikonya rendah, tapi
     tetap ada. Telegram tidak punya risiko ini."*
  4. Nomor pemilik sudah ada di `allowFrom` kanal WA itu (lihat `cek-privasi-openclaw` / skill `agen-cs-toko`).
- **Tidak ada broadcast**, tidak ada pengiriman ke grup, dan **tidak ada pesan penagihan otomatis ke pelanggan**.
  `--to` selalu berisi ID chat/nomor **pemilik**.
- Minta ringkasan + "Lanjut? (ya/tidak)" sebelum menjalankan perintah apa pun di bawah.

## 1. Rekap harian 08.00 WIB (agent AI + skill ini) ✅
```bash
openclaw automations add "0 8 * * *" \
  "Pakai skill pengingat-follow-up. Jalankan: python3 <folder-skill>/scripts/cek_jatuh_tempo.py --file <folder-kerja>/pengingat/DAFTAR.csv --timesheet-file <folder-kerja>/pengingat/timesheet.csv --teks rekap. Kirim teksnya apa adanya dalam Bahasa Indonesia. Untuk item timesheet, isi [TOTAL JAM]/[NILAI] dengan subperintah timesheet --klien. JANGAN mengubah angka, JANGAN mengirim apa pun ke pelanggan. Jika file belum ada atau script error, laporkan itu saja." \
  --name "Pengingat follow-up harian" --tz "Asia/Jakarta" --session isolated --tools exec,read \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- `--tools exec,read` ✅: agent jadwal hanya diberi alat menjalankan script & membaca file (tanpa kirim pesan,
  browser, tulis file, dll.). Tanpa opsi ini job tersimpan dengan `toolsAllow: ["*"]` (semua alat). Hasil uji:
  `payload.toolsAllow: ["exec", "read"]`. ⚠️ Belum diuji dengan model sungguhan bahwa agent tetap bisa memuat
  skill dengan dua alat ini. Jika run gagal karena alat kurang, tambahkan alat yang disebut di pesan error saja.
- Hasil uji: job terbentuk dengan `schedule: {kind: cron, expr: "0 8 * * *", tz: "Asia/Jakarta"}`.
  `nextRunAtMs` = 01.00 UTC = **08.00 WIB**. `delivery: announce -> telegram:<id> (explicit)`.
- Ini "Bentuk A": jadwal & pesan ditulis sebagai argumen posisi, **tanpa** `--cron`. Jangan dicampur
  dengan `--cron/--at/--every`. Jika salah satunya dipakai, argumen posisi pertama berubah arti menjadi nama job.
- Pakai **path lengkap** untuk `--file`. ⚠️ Folder kerja sesi `isolated` belum dipastikan sama dengan workspace chat.
- Tanpa `--agent`, CLI memberi catatan bahwa job memakai agent default. Itu normal.
- Setiap run memakai token model (biaya pengguna). Untuk rekap rutin boleh memakai `--model <model hemat>` 📖.
- Ambil `"id"` dari output JSON. `run/disable/enable/edit/rm` **hanya menerima id**. Uji membuktikan bahwa memakai nama
  menghasilkan `Automation not found`.

## 2. Alternatif hemat: tanpa AI, langsung teks script ✅ (pengiriman ⚠️)
Cocok jika pemilik cukup menerima teks rekap bawaan (draf dari template, tanpa diperhalus AI) dan ingin
**nol biaya token**:
```bash
openclaw automations add --name "Rekap pengingat (tanpa AI)" --cron "0 8 * * *" --tz "Asia/Jakarta" \
  --command "python3 /path/lengkap/pengingat-follow-up/scripts/cek_jatuh_tempo.py --file /path/lengkap/pengingat/DAFTAR.csv --teks rekap" \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- Hasil uji: `openclaw automations run <id> --wait` menjalankan script sungguhan. Ringkasan run (`summary`)
  berisi teks rekap lengkap, dan tanggalnya mengikuti WIB. Pengiriman ke Telegram gagal di lingkungan uji karena
  tidak ada token bot (`Telegram bot token missing`). Ini berarti job memang mencoba mengirim, tetapi penerimaan
  pesan di Telegram belum dibuktikan ⚠️.
- Perintah dijalankan sebagai `sh -lc` di komputer Gateway. Opsi ini cocok untuk macOS/Linux/VPS.
  ⚠️ Belum diuji di Gateway Windows. Di Windows pakai Bentuk A (§1).
- Baris tambahan dari profil shell (di mesin uji muncul kata `nvm`) bisa ikut terkirim. Jika mengganggu, pakai §1.
- Mode ini mengirim teks script **apa adanya**: draf timesheet tetap berisi placeholder `[TOTAL JAM]`/`[NILAI]`
  (tidak ada AI yang mengisinya), dan draf tidak diperhalus. Untuk timesheet, pakai §4 atau jalankan
  `timesheet --klien` sendiri.

## 3. Pengingat sekali jalan untuk janji spesifik (`--at`) ✅
"Bentuk B" (opsi penuh, tanpa argumen posisi):
```bash
openclaw automations add --name "Telepon Bu Rina (#3)" --at "2026-10-03T09:00" --tz "Asia/Jakarta" \
  --message "Ingatkan pemilik: hari ini follow-up item #3 (Bu Rina). Tampilkan draf dengan skill pengingat-follow-up: cek_jatuh_tempo.py --file <folder-kerja>/pengingat/DAFTAR.csv --teks draf --id 3. Jangan kirim apa pun ke pelanggan." \
  --session isolated --tools exec,read --announce --channel telegram --to "<ID chat Telegram pemilik>" --delete-after-run
```
- Hasil uji: `--at "2026-10-03T09:00"` + `--tz Asia/Jakarta` tersimpan sebagai `2026-10-03T02:00:00Z`
  (09.00 WIB), dengan `deleteAfterRun: true`. `--at "20m"` (20 menit dari sekarang) juga diterima.
- Menurut `--help`, waktu `--at` tanpa offset memakai `--tz`. Selalu sertakan `--tz "Asia/Jakarta"`.

## 4. Rekap timesheet tiap Jumat 16.00 WIB ✅
```bash
openclaw automations add "0 16 * * 5" \
  "Pakai skill pengingat-follow-up. Jalankan cek_jatuh_tempo.py --timesheet-file <folder-kerja>/pengingat/timesheet.csv --teks timesheet --periode minggu-ini, lalu untuk tiap klien jalankan lagi dengan --klien \"<nama>\" dan tampilkan draf pesan ke klien. Pemilik yang menyetujui & mengirim; JANGAN kirim ke klien." \
  --name "Rekap timesheet Jumat" --tz "Asia/Jakarta" --session isolated --tools exec,read \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 5. Mengelola jadwal ✅
```bash
openclaw automations list --all                     # semua job + id
openclaw automations show "<nama persis>"           # show menerima nama ATAU id
openclaw automations edit <id> --cron "30 7 * * *" --tz "Asia/Jakarta"   # ubah jam (hanya id)
openclaw automations disable <id>                   # jeda (hanya id)
openclaw automations enable <id>                    # aktifkan lagi
openclaw automations run <id> --wait                # uji sekarang, sebelum menyatakan "aktif"
openclaw automations runs --id <id>                 # riwayat run
openclaw automations rm <id>                        # hapus permanen
```
Semua perintah di atas dijalankan di Gateway uji. `disable "<nama>"` ditolak dengan `Automation not found`.

## 6. WhatsApp nomor terpisah (hanya jika syarat §0 terpenuhi)
Ganti baris terakhir menjadi `--announce --channel whatsapp --to "+62<nomor pemilik>"`. Status uji:
- `automations add` dengan `--channel whatsapp` **tetap diterima** ✅, bahkan saat plugin WhatsApp belum
  terpasang. `list` lalu menampilkan `Unsupported channel: whatsapp`. Jadi pastikan kanal sudah ditambahkan
  (`openclaw channels add --channel whatsapp` lalu `openclaw channels login --channel whatsapp`, scan QR) 📖.
- Pengiriman nyata ke WA ⚠️ belum diuji.

## 7. Telegram: menyiapkan bot 📖
Buat bot di @BotFather, lalu `openclaw channels add --channel telegram --token <token>`. Kirim "halo" ke bot
dari akun pemilik, lalu setujui pairing (`openclaw pairing list telegram`, `openclaw pairing approve telegram <KODE>`).
ID chat pemilik dipakai untuk `--to` (cara mencarinya: `laporan-otomatis-terjadwal/references/openclaw.md` §4).

## 8. Yang belum diverifikasi ⚠️ (katakan jujur ke pengguna jika dipakai)
- Membuat jadwal langsung dari chat ("aktifkan pengingat jam 8"). Agent memakai tool `cron` (hanya untuk owner).
  Dokumentasi menyebut fitur ini didukung, tetapi belum kami uji. Jika gagal, jalankan perintah di atas dari terminal/Control UI.
- Balasan "selesai 3" dari Telegram langsung mengubah file. Ini bergantung pada izin tool `exec`/file di agent pengguna.
- Pesan benar-benar tiba di Telegram/WhatsApp (lihat status di atas).

## 9. Syarat komputer menyala
Jadwal berjalan **di dalam proses Gateway**. Jika laptop mati atau tidur pada jam 08.00, rekap **tidak terkirim**
dan tidak ada pesan error. Tawarkan tiga opsi berikut tanpa menyebut harga:
1. Laptop/mini PC yang selalu menyala.
2. VPS milik pengguna sendiri.
3. Jasa setup Komunitech.

Detail: `laporan-otomatis-terjadwal/references/mesin-24-jam.md` (jika skill itu terpasang).
