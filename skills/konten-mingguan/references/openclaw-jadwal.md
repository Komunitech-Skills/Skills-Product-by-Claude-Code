# Otomasi OpenClaw — Paket Jumat Sore + Pengingat Posting Harian

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

Opsional. Skill ini berguna dipanggil manual di platform mana pun (OpenClaw, Codex, Claude Code,
Cursor). Bagian ini **hanya untuk OpenClaw** yang punya Gateway menyala terus, dan **hanya dipasang
setelah pengguna setuju** (tampilkan ringkasan lalu tanya "Lanjut? (ya/tidak)").

Semua perintah di bawah diverifikasi lewat `<perintah> --help` di OpenClaw **2026.9.5 (ec9c1a1)**.
Flag inti (`--cron`, `--tz`, `--session`, `--announce`, `--channel`, `--to`, `--tools`) sama dengan
yang dipakai & sudah diuji terhadap Gateway lokal oleh skill `laporan-otomatis-terjadwal` — lihat
`SKILL.md` skill itu untuk detail pengujian ujung-ke-ujung. Kalau versi OpenClaw pengguna berbeda dan
sebuah flag gagal, jalankan `openclaw automations add --help` dulu untuk memastikan opsinya masih sama.

**Fallback wajib:** kalau `exec`/perintah komputer tidak diizinkan, atau pengguna memakai platform
tanpa Gateway OpenClaw (Claude Code/Codex/Cursor), **jangan memaksa**. Tampilkan perintah sebagai teks
siap salin-tempel untuk dijalankan pengguna sendiri di terminal tempat OpenClaw berjalan, atau arahkan
ke Control UI (`Settings → Automations`). Skill tetap berguna tanpa otomasi ini — cukup dipanggil manual
setiap butuh paket konten.

## Kanal: Telegram default, WA hanya nomor terpisah
Ikuti keputusan pemilik Komunitech: **Telegram** adalah kanal default untuk laporan/pengingat ke
pemilik usaha. **WhatsApp** (WA Web/Baileys, tidak resmi) hanya dipasang bila pengguna memakai
**nomor terpisah** (bukan nomor utama usaha) dan menyetujui risikonya secara tertulis (nomor bisa
diblokir; lihat `references/openclaw.md` di skill `laporan-otomatis-terjadwal` untuk detail risiko).
**Tidak ada broadcast/kirim massal** lewat OpenClaw — automasi ini hanya mengirim ke chat pemilik sendiri.

Cara menyiapkan kanal (sama seperti `laporan-otomatis-terjadwal`, lihat referensinya untuk langkah
lengkap mencari ID chat Telegram / login QR WhatsApp):
```bash
openclaw channels add --channel telegram --token <token-dari-BotFather>
```

## 1. Automasi mingguan — paket konten Jumat sore

```bash
openclaw automations add "0 16 * * 5" \
  "Jalankan skill konten-mingguan untuk minggu depan memakai profil di konten/PROFIL.md. Tulis paket lengkap dalam Bahasa Indonesia, simpan arsip ke konten/minggu-<label>.md, lalu kirimkan ringkasan per hari." \
  --tz "Asia/Jakarta" --name "Paket konten Jumat sore" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- `"0 16 * * 5"` = tiap Jumat jam 16.00 (bisa diubah, tanyakan jam yang pemilik mau).
- `--tz "Asia/Jakarta"` **wajib** eksplisit — tanpa ini cron memakai zona waktu komputer Gateway.
- `--session isolated` — job tidak mencampuri sesi chat utama pengguna.
- `--announce --channel telegram --to "<...>"` **wajib** diisi eksplisit supaya paket benar-benar
  terkirim, bukan cuma tercatat di riwayat run. Untuk WA (setelah syarat di atas terpenuhi):
  `--channel whatsapp --to "+62..."` (nomor pemilik harus ada di `allowFrom` kanal WA itu).

## 2. Automasi harian — pengingat posting ringan

```bash
openclaw automations add "0 8 * * *" \
  "Baca konten/minggu-<label minggu berjalan>.md, ambil bagian untuk HARI INI saja (cocokkan tanggal), lalu kirim ringkas: platform, hook, dan caption siap tempel hari ini. Kalau arsip minggu ini belum ada, katakan itu apa adanya, jangan mengarang." \
  --tz "Asia/Jakarta" --name "Pengingat posting harian" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- Jam `08.00` contoh; sarankan jam yang biasanya pemilik/admin mulai kerja.
- Pengingat ini **ringan** (satu hari saja) supaya tidak mengulang seluruh paket setiap hari.
- Kalau pemilik ingin pengingat mendekati jam posting (bukan pagi sekali), tawarkan beberapa job
  `--at`/`--every` tambahan, atau cukup satu job pagi yang mencantumkan semua jam posting hari itu.

## 3. Mencatat id job & menguji sebelum aktif

```bash
openclaw automations run <id-dari-hasil-add> --wait   # uji sekali, tunjukkan hasilnya ke pengguna
openclaw automations list --json                       # cari id kalau lupa
openclaw automations disable <id>                       # jeda tanpa menghapus
openclaw automations rm <id>                             # hapus permanen
```
`run`/`disable`/`enable`/`edit`/`rm` **wajib pakai id (UUID)**, bukan nama — hanya `show` yang
menerima nama persis. Simpan id dari hasil `add` (field `"id"` di JSON) segera setelah dibuat.

## 4. Batasi tools agent job (disarankan)

Job ini hanya perlu membaca file & menulis pesan, bukan menjelajah sistem:
```bash
--tools "read,write"
```
Tambahkan flag ini pada `add` bila pengguna sudah memperketat profil tool secara umum, supaya job
konten tidak diam-diam mendapat akses `exec`/`browser` penuh.

## 5. Yang BELUM diverifikasi ujung-ke-ujung
- Membuat jadwal ini langsung lewat chat WhatsApp/Telegram (pengguna mengetik "aktifkan paket Jumat
  sore" di chat, bukan lewat terminal/Control UI): dukungannya ada di dokumentasi resmi, tapi kombinasi
  persisnya belum dicoba tim kami untuk skill ini. Kalau gagal/aneh, jalankan perintah yang sama dari
  terminal atau Control UI sebagai gantinya.
- **Gateway harus menyala** saat jam 16.00 Jumat dan 08.00 tiap hari — jelaskan ini ke pengguna
  (lihat penjelasan "mesin 24 jam" di skill `laporan-otomatis-terjadwal`, `references/mesin-24-jam.md`)
  sebelum mengaktifkan jadwal.
