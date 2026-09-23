# Perintah OpenClaw yang dipakai skill ini

Semua perintah di bawah **diverifikasi langsung** dengan `<perintah> --help` di OpenClaw
**2026.9.5 (ec9c1a1)** (mesin uji terisolasi, `HOME` terpisah, **tanpa Gateway aktif, tanpa
login kanal apa pun**). Tidak ada satu pun perintah di sini yang belum dicek lewat `--help`.
Kalau versi OpenClaw pengguna berbeda dan sebuah flag gagal, jalankan
`openclaw automations add --help` (atau subperintah lain terkait) dulu untuk memastikan opsinya
masih sama, lalu beri tahu pengguna.

**Fallback wajib:** kalau `exec`/perintah komputer tidak diizinkan (tidak ada respons, ditolak,
atau pengguna memakai platform selain OpenClaw seperti Claude Code/Codex/Cursor yang tidak
punya Gateway OpenClaw), **jangan memaksa**. Tampilkan perintah sebagai teks siap salin-tempel
untuk dijalankan pengguna sendiri di terminal tempat OpenClaw berjalan, atau arahkan ke Control
UI (`Settings → Automations`).

Nama subperintah resminya adalah **`automations`** (alias yang lebih pendek: **`cron`** --
keduanya jalan sama). Contoh di bawah memakai `automations` agar jelas maksudnya bagi pengguna
awam.

## 1. Membuat jadwal (`openclaw automations add`)

```bash
openclaw automations add "<schedule-atau-nama>" "<pesan untuk agent>" \
  --cron "0 7 * * 1" --tz "Asia/Jakarta" \
  --name "Laporan penjualan Senin" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Opsi yang dipakai skill ini (semua terverifikasi via `openclaw automations add --help`):
- `--cron <expr>` -- cron 5/6 kolom. Alternatif: `--at <waktu>` (sekali jalan, mis. `"20m"` atau
  ISO) untuk pengingat sekali pakai, atau `--every <durasi>` (mis. `1h`) untuk interval.
- `--tz <iana>` -- **wajib diisi eksplisit** (`Asia/Jakarta`) karena tanpa ini cron memakai zona
  waktu komputer Gateway, bukan zona waktu pengguna.
- `--name <nama>` -- nama jadwal yang mudah dikenali (dipakai lagi di `show`/`edit`/`rm` sebagai
  pengganti id).
- `--session isolated` -- jadwal tidak mencampuri sesi chat utama pengguna dan tidak menyimpan
  hasil ke riwayat chat biasa.
- `--announce` -- kirim hasil akhir ke kanal chat (bukan hanya tersimpan). **Wajib** dipasang
  supaya laporan benar-benar terkirim, bukan cuma tercatat di riwayat run.
- `--channel <nama>` -- `telegram` atau `whatsapp` (nama plugin kanal yang sudah ditambahkan
  lewat `openclaw channels add`). Default `last` (kanal terakhir dipakai) -- skill ini SELALU
  mengisi eksplisit supaya tidak salah kirim.
- `--to <tujuan>` -- ID chat Telegram, atau nomor WhatsApp format E.164 (`+62...`). **Wajib**
  diisi eksplisit; tanpa ini automation tidak tahu ke mana mengirim proaktif.
- `--best-effort-deliver` -- opsional; kalau dipasang, job tidak dianggap gagal hanya karena
  pengiriman gagal (berguna kalau kanal sedang bermasalah, tetap ingin run tercatat).
- `--model <model>` -- opsional, model yang lebih hemat untuk laporan rutin bila pengguna
  meminta menghemat biaya token.

Model risiko WhatsApp: lihat `SKILL.md` §Langkah kerja 4. Ringkas: `--channel whatsapp` hanya
dipasang setelah nomor terpisah + persetujuan risiko tertulis pengguna.

## 2. Melihat, menjeda, mengubah, menghapus jadwal

```bash
openclaw automations list --all        # semua jadwal termasuk yang nonaktif
openclaw automations list --json       # untuk dibaca terprogram
openclaw automations show <id-atau-nama> --json
openclaw automations disable <id>      # jeda (job tetap ada, tidak dihapus)
openclaw automations enable <id>       # aktifkan lagi
openclaw automations edit <id> --cron "0 8 * * 1" --tz "Asia/Jakarta"
openclaw automations edit <id> --to "<tujuan baru>"
openclaw automations rm <id>           # hapus permanen (tidak bisa dibatalkan)
```
Semua flag `add` (kecuali argumen posisi jadwal/pesan) juga tersedia di `edit` sebagai patch
(hanya field yang disebut yang berubah), termasuk `--clear-to`, `--clear-channel`, dll. untuk
menghapus satu pengaturan tanpa mengubah yang lain.

## 3. Menguji jadwal sebelum diaktifkan

```bash
openclaw automations run <id-atau-nama> --wait
```
`--wait` menunggu hasil run selesai sebelum perintah kembali, supaya bisa langsung ditunjukkan
ke pengguna sebagai bukti. Ada juga `--due` (hanya jalan kalau memang sudah waktunya) --
untuk uji manual pertama, **jangan** pakai `--due` supaya run terjadi langsung.

```bash
openclaw automations runs <id>         # riwayat run (untuk cek run terjadwal berikutnya)
```

## 4. Menyiapkan kanal Telegram (default)

```bash
openclaw channels add --channel telegram --token <token-dari-BotFather>
```
Langkah sebelum ini (di luar cakupan skill): buat bot lewat @BotFather di Telegram, salin
token-nya. Setelah kanal ditambahkan, pengguna perlu mengirim pesan pertama ke bot itu supaya
"pairing" DM disetujui (lihat dokumentasi resmi `channels/pairing`) -- baru setelah itu ID chat
mereka bisa dipakai di `--to`.

Untuk mencari ID chat Telegram: minta pengguna kirim pesan apa saja ke bot, lalu cek log/Control
UI, atau jalankan `openclaw channels list --all` untuk melihat kanal yang tersedia sebelum
`--channel`.

## 5. Menyiapkan kanal WhatsApp (hanya nomor terpisah + izin risiko)

```bash
openclaw channels add --channel whatsapp
openclaw channels login --channel whatsapp
```
Login **hanya lewat scan QR** dengan nomor terpisah. Setelah login, nomor pemilik perlu ada di
daftar `allowFrom` kanal WA itu supaya automation boleh mengirim proaktif ke DM -- ini bagian
konfigurasi kanal (`channels.whatsapp.allowFrom`), bukan flag `automations`. Sarankan pengguna
menjalankan `cek-privasi-openclaw` setelah kanal WA aktif untuk memeriksa pengaturan ini.

## 6. Yang BELUM diverifikasi ujung-ke-ujung (beri tahu pengguna kalau dipakai)

- **Membuat jadwal lewat chat WhatsApp** (pengguna mengetik "buatkan jadwal..." langsung di WA,
  bukan lewat terminal/Control UI): dukungannya ada di dokumentasi resmi, tapi kombinasi
  persisnya belum dicoba tim kami. Kalau gagal/aneh, jalankan perintah yang sama dari terminal
  atau Control UI sebagai gantinya.
- **`--trigger-script`** (job hanya jalan bila skrip kondisi mengembalikan status tertentu):
  flag-nya ada dan terverifikasi lewat `--help`, tapi skill ini tidak memakainya (laporan rutin
  cukup cron biasa). Disebut di sini untuk kelengkapan kalau pengguna lanjut ke kebutuhan lebih
  rumit (mis. notifikasi ambang harga) di skill lain.
