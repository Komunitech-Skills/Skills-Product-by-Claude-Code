# Jadwal OpenClaw siap salin — Konsultan/Freelancer

Sumber: `skills/pengingat-follow-up/references/openclaw-jadwal.md` — dokumen paling lengkap
verifikasinya di seluruh library (diuji sungguhan di OpenClaw **2026.9.5 (ec9c1a1)** DAN diuji
ulang **2026.9.6 (eb377ac)**, 24 Sep 2026, hasil sama, terhadap Gateway lokal
`gateway run --dev --allow-unconfigured --bind loopback`). Untuk sesi penyusunan paket ini, flag
yang sama **diverifikasi ulang ketiga kalinya** lewat `openclaw automations add --help`
sungguhan (via `bash scripts/uji_openclaw.sh 2026.9.6`) — tetap cocok persis.

Legenda (sama seperti sumbernya): ✅ = **dijalankan sungguhan**, job terbentuk & terverifikasi
dari JSON hasilnya. 📖 = hanya dicek `--help`. ⚠️ = belum bisa diverifikasi.

**Semua jadwal mengirim hanya ke pemilik/konsultan sendiri — tidak pernah langsung ke klien.**
Draf pesan ke klien selalu disiapkan untuk **disalin & dikirim manual**.

## 0. Aturan kanal
- **Telegram = default.** WhatsApp hanya dengan nomor terpisah + rekap hanya ke pemilik sendiri +
  persetujuan risiko tertulis: *"OpenClaw memakai WhatsApp Web (tidak resmi, lewat scan QR).
  Syarat Layanan WhatsApp melarang pesan otomatis/massal, jadi nomor bisa diblokir. Untuk rekap
  ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya risiko ini. Saya
  mengerti risikonya."*
- **Tidak ada** broadcast, tidak ada kirim ke grup, dan **tidak ada** pesan penagihan otomatis
  langsung ke klien. `--to` selalu berisi ID chat/nomor **pemilik/konsultan sendiri**.

## 1. Rekap follow-up & piutang harian, 08.00 WIB ✅
```bash
openclaw automations add "0 8 * * *" \
  "Pakai skill pengingat-follow-up. Jalankan: python3 <folder-skill>/scripts/cek_jatuh_tempo.py --file <folder-kerja>/pengingat/DAFTAR.csv --timesheet-file <folder-kerja>/pengingat/timesheet.csv --teks rekap. Kirim teksnya apa adanya dalam Bahasa Indonesia. Untuk item timesheet, isi [TOTAL JAM]/[NILAI] dengan subperintah timesheet --klien. JANGAN mengubah angka, JANGAN mengirim apa pun ke klien. Jika file belum ada atau script error, laporkan itu saja." \
  --name "Pengingat follow-up harian" --tz "Asia/Jakarta" --session isolated --tools exec,read \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- `--tools exec,read` ✅ — jadwal ini hanya boleh menjalankan script & membaca file, tidak bisa
  kirim pesan/browser/tulis file. Hasil uji nyata: `payload.toolsAllow: ["exec", "read"]`.
- Bentuk ini ("Bentuk A": jadwal & pesan sebagai argumen posisi, **tanpa** `--cron`) — jangan
  dicampur dengan `--cron`/`--at`/`--every` di perintah yang sama.
- Hasil uji nyata: `schedule: {kind: cron, expr: "0 8 * * *", tz: "Asia/Jakarta"}`, `nextRunAtMs`
  = 01.00 UTC = **08.00 WIB** — zona waktu terbukti benar.

## 2. Alternatif hemat token: tanpa AI, langsung teks script ✅ (pengiriman ⚠️)
```bash
openclaw automations add --name "Rekap pengingat (tanpa AI)" --cron "0 8 * * *" --tz "Asia/Jakarta" \
  --command "python3 /path/lengkap/pengingat-follow-up/scripts/cek_jatuh_tempo.py --file /path/lengkap/pengingat/DAFTAR.csv --teks rekap" \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Cocok untuk yang ingin **nol biaya token model** — teks rekap dikirim apa adanya (draf timesheet
tetap berisi placeholder, tidak diperhalus AI). Diuji sungguhan: script berjalan dan menghasilkan
teks rekap lengkap; pengiriman ke Telegram gagal di lingkungan uji hanya karena tidak ada token
bot asli (⚠️ pengiriman nyata belum dibuktikan, tapi job **memang mencoba** mengirim).
⚠️ Belum diuji di Gateway Windows — di Windows pakai §1.

## 3. Rekap timesheet klien, Jumat 16.00 WIB ✅
```bash
openclaw automations add "0 16 * * 5" \
  "Pakai skill pengingat-follow-up. Jalankan cek_jatuh_tempo.py --timesheet-file <folder-kerja>/pengingat/timesheet.csv --teks timesheet --periode minggu-ini, lalu untuk tiap klien jalankan lagi dengan --klien \"<nama>\" dan tampilkan draf pesan ke klien. Pemilik yang menyetujui & mengirim; JANGAN kirim ke klien." \
  --name "Rekap timesheet Jumat" --tz "Asia/Jakarta" --session isolated --tools exec,read \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 4. Pengingat sekali jalan untuk janji spesifik (`--at`) ✅
```bash
openclaw automations add --name "Telepon Pak Budi (#3)" --at "2026-10-03T09:00" --tz "Asia/Jakarta" \
  --message "Ingatkan pemilik: hari ini follow-up item #3. Tampilkan draf dengan skill pengingat-follow-up: cek_jatuh_tempo.py --file <folder-kerja>/pengingat/DAFTAR.csv --teks draf --id 3. Jangan kirim apa pun ke klien." \
  --session isolated --tools exec,read --announce --channel telegram --to "<ID chat Telegram pemilik>" --delete-after-run
```
Hasil uji nyata: `--at "2026-10-03T09:00"` + `--tz Asia/Jakarta` tersimpan sebagai
`2026-10-03T02:00:00Z` (09.00 WIB), dengan `deleteAfterRun: true`. `--at "20m"` (20 menit dari
sekarang) juga diterima.

## 5. Mengelola jadwal ✅
```bash
openclaw automations list --all
openclaw automations show "<nama persis>"           # show boleh nama ATAU id
openclaw automations edit <id> --cron "30 7 * * *" --tz "Asia/Jakarta"
openclaw automations disable <id>                   # hanya id
openclaw automations enable <id>                    # hanya id
openclaw automations run <id> --wait                # uji dulu sebelum percaya "aktif"
openclaw automations runs --id <id>
openclaw automations rm <id>                         # hanya id, permanen
```
`disable`/`enable`/`edit`/`run`/`rm` dengan **nama** (bukan id) ditolak: `Automation not found`
— dibuktikan langsung di Gateway uji.

## 6. WhatsApp nomor terpisah (hanya bila syarat §0 terpenuhi)
Ganti baris terakhir tiap perintah menjadi
`--announce --channel whatsapp --to "+62<nomor pemilik>"`. Status uji: `automations add` dengan
`--channel whatsapp` **tetap diterima** ✅ walau plugin WA belum terpasang (baru terlihat
`Unsupported channel: whatsapp` saat `list`, sampai kanalnya benar-benar ditambahkan &
login). Pengiriman nyata ke WA ⚠️ belum diuji.

## 7. Telegram: menyiapkan bot 📖
Buat bot di @BotFather → `openclaw channels add --channel telegram --token <token>` → kirim
"halo" dari akun pemilik → `openclaw pairing list telegram` → `openclaw pairing approve telegram
<KODE>` (berlaku 1 jam). ID chat untuk `--to`: lihat cara mencarinya di
`skills/laporan-otomatis-terjadwal/references/openclaw.md` §4 (via @userinfobot bila tak ada
akses Control UI/log Gateway).

## 8. Yang belum diverifikasi ⚠️
- Membuat jadwal di atas langsung dari chat ("aktifkan pengingat jam 8"). Tool `cron` untuk agent
  memang ada dan hanya untuk owner, tapi kombinasi persisnya belum dicoba tim kami. Kalau
  gagal/aneh, jalankan perintah dari terminal/Control UI.
- Balasan "selesai #3" dari Telegram langsung mengubah `DAFTAR.csv` — bergantung izin `exec`/file
  agent pengguna, belum diuji end-to-end.
- Pesan benar-benar tiba di Telegram/WhatsApp (uji internal tidak memakai token/nomor asli).

## 9. Syarat komputer menyala
Jadwal berjalan **di dalam proses Gateway**. Kalau laptop mati/tidur di jam 08.00, rekap **tidak
terkirim** dan tidak ada pesan error. Tiga opsi (tanpa harga): laptop/mini PC yang selalu
menyala, VPS milik pengguna sendiri, atau jasa setup Komunitech.
