# Perintah OpenClaw yang dipakai skill ini

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

Semua perintah di bawah **diverifikasi lewat `<perintah> --help`** di OpenClaw **2026.9.5
(ec9c1a1)**. Perintah inti di §1-§3 (`automations add`/`show`/`run`/`disable`/`enable`/`edit`/
`rm`/`list`) juga **benar-benar dijalankan** terhadap Gateway lokal uji 2026.9.5
(`gateway run --dev --allow-unconfigured --bind loopback --token ...`, tanpa model AI beneran &
tanpa kanal login) -- bukan cuma dibaca dari `--help`. Bentuk `channels add --channel telegram
--token`/`channels add --channel whatsapp`/`channels login --channel whatsapp` tervalidasi lewat
`--help` tapi **belum** dijalankan sungguhan (butuh token/nomor asli). Skill/script resep lain
(`rekap-penjualan-csv`, `laporan-keuangan-emkm`, `arus-kas-13minggu`, `tagih-piutang`,
`buku-stok`) diverifikasi lewat `--help` masing-masing; lihat `SKILL.md`-nya untuk detail.
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

**PENTING soal nama/jadwal posisional vs `--name`/`--cron`:** argumen posisi pertama berarti
"jadwal" HANYA kalau `--cron`/`--at`/`--every` TIDAK dipakai; begitu salah satu dari ketiganya
dipakai, argumen posisi pertama berarti **nama job**. Memakai keduanya sekaligus (posisi +
`--name`, dengan `--cron` terpasang) ditolak CLI: *"Pass the automation name either positionally
or with --name, not both."* -- ini terbukti di Gateway uji. Pakai salah satu dari dua bentuk di
bawah (keduanya **terbukti jalan** di Gateway uji), jangan mencampur:

**Bentuk A -- jadwal & pesan sebagai posisi, TANPA `--cron` (dipakai skill ini):**
```bash
openclaw automations add "0 7 * * 1" "<pesan untuk agent>" \
  --tz "Asia/Jakarta" --name "Laporan penjualan Senin" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

**Bentuk B -- opsi penuh, TANPA argumen posisi apa pun:**
```bash
openclaw automations add --cron "0 7 * * 1" --message "<pesan untuk agent>" \
  --tz "Asia/Jakarta" --name "Laporan penjualan Senin" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

Opsi yang dipakai skill ini (semua terverifikasi via `--help`; yang bertanda ✅ juga dijalankan
sungguhan di Gateway uji):
- `--cron <expr>` ✅ -- cron 5/6 kolom (dipakai di Bentuk B; di Bentuk A cron jadi argumen posisi
  pertama). Alternatif: `--at <waktu>` (sekali jalan, mis. `"20m"` atau ISO) untuk pengingat
  sekali pakai, atau `--every <durasi>` (mis. `1h`) untuk interval.
- `--tz <iana>` ✅ -- **wajib diisi eksplisit** (`Asia/Jakarta`) karena tanpa ini cron memakai zona
  waktu komputer Gateway, bukan zona waktu pengguna.
- `--name <nama>` ✅ -- nama jadwal yang mudah dikenali untuk pengguna. **Tidak** bisa dipakai
  sebagai pengganti id di `run`/`disable`/`enable`/`edit`/`rm` (lihat §2) -- hanya `show` yang
  menerima nama persis selain id.
- `--session isolated` ✅ -- jadwal tidak mencampuri sesi chat utama pengguna dan tidak menyimpan
  hasil ke riwayat chat biasa.
- `--announce` ✅ -- kirim hasil akhir ke kanal chat (bukan hanya tersimpan). **Wajib** dipasang
  supaya laporan benar-benar terkirim, bukan cuma tercatat di riwayat run.
- `--channel <nama>` ✅ -- `telegram` atau `whatsapp` (nama plugin kanal yang sudah ditambahkan
  lewat `openclaw channels add`). Default `last` (kanal terakhir dipakai) -- skill ini SELALU
  mengisi eksplisit supaya tidak salah kirim.
- `--to <tujuan>` ✅ -- ID chat Telegram, atau nomor WhatsApp format E.164 (`+62...`). **Wajib**
  diisi eksplisit; tanpa ini automation tidak tahu ke mana mengirim proaktif.
- `--best-effort-deliver` -- (hanya dicek `--help`) opsional; kalau dipasang, job tidak dianggap
  gagal hanya karena pengiriman gagal (berguna kalau kanal sedang bermasalah, tetap ingin run
  tercatat).
- `--model <model>` -- (hanya dicek `--help`) opsional, model yang lebih hemat untuk laporan
  rutin bila pengguna meminta menghemat biaya token.

Hasil `add` (JSON) memuat field `"id"` (UUID) -- **catat/ambil nilai ini**, dipakai di §2-§3.

Model risiko WhatsApp: lihat `SKILL.md` §Langkah kerja 4. Ringkas: `--channel whatsapp` hanya
dipasang setelah nomor terpisah + persetujuan risiko tertulis pengguna.

## 2. Melihat, menjeda, mengubah, menghapus jadwal

**`run`/`disable`/`enable`/`edit`/`rm` hanya menerima `id` (UUID), BUKAN nama** -- dibuktikan di
Gateway uji: memakai nama pada perintah-perintah ini menjawab `"Automation not found: <nama>.
Run 'openclaw cron list' to see recent automation ids."`. Hanya `show` yang menerima nama persis
selain id.

```bash
openclaw automations list --all        # semua jadwal termasuk yang nonaktif
openclaw automations list --json       # untuk dibaca terprogram -- cari "id" dari "name" di sini
openclaw automations show <id-atau-"nama persis"> --json   # show SAJA yang boleh pakai nama
openclaw automations disable <id>      # jeda (job tetap ada, tidak dihapus) -- WAJIB id
openclaw automations enable <id>       # aktifkan lagi -- WAJIB id
openclaw automations edit <id> --cron "0 8 * * 1" --tz "Asia/Jakarta"   # WAJIB id
openclaw automations edit <id> --to "<tujuan baru>"                     # WAJIB id
openclaw automations rm <id>           # hapus permanen (tidak bisa dibatalkan) -- WAJIB id
```
Semua flag `add` (kecuali argumen posisi jadwal/pesan) juga tersedia di `edit` sebagai patch
(hanya field yang disebut yang berubah), termasuk `--clear-to`, `--clear-channel`, dll. untuk
menghapus satu pengaturan tanpa mengubah yang lain.

## 3. Menguji jadwal sebelum diaktifkan

```bash
openclaw automations run <id> --wait
```
`<id>` **wajib** id (UUID dari hasil `add`, atau dicari lewat `list --json`) -- `run` dengan nama
gagal (lihat §2). `--wait` menunggu hasil run selesai sebelum perintah kembali, supaya bisa
langsung ditunjukkan ke pengguna sebagai bukti. Ada juga `--due` (hanya jalan kalau memang sudah
waktunya) -- untuk uji manual pertama, **jangan** pakai `--due` supaya run terjadi langsung.

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

**Cara konkret mencari ID chat Telegram** (`channels list --all` HANYA menampilkan katalog kanal
yang bisa dipasang, BUKAN chat id -- jangan pakai itu untuk ini):
1. Minta pengguna membuka chat dengan bot mereka di Telegram dan mengirim pesan apa saja
   (mis. "halo").
2. Karena ini pesan pertama dari pengguna, OpenClaw meminta persetujuan "pairing" untuk DM itu
   (lihat dokumentasi resmi `channels/pairing`) -- pairing ini biasanya menampilkan/mencatat
   chat id pengirim di Control UI atau log Gateway.
3. Kalau pengguna/agent bisa membaca Control UI (`Settings → Channels → Telegram`) atau log
   Gateway, chat id itu yang tercatat di sana dipakai untuk `--to`.
4. Kalau tidak ada akses ke Control UI/log, arahkan pengguna ke bot pihak ketiga seperti
   `@userinfobot` di Telegram untuk melihat chat id mereka sendiri, lalu tempel angkanya ke sini.

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
