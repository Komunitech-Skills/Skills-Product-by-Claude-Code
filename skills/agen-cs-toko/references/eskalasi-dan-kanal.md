# Setup Kanal & Otomasi OpenClaw untuk Agen CS Toko

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

Semua perintah & kunci konfigurasi di halaman ini diverifikasi lewat `--help` OpenClaw 2026.9.5, `openclaw config schema`, dan docs.openclaw.ai (channels/whatsapp, channels/pairing). Jangan menambah kunci config baru tanpa memverifikasi ulang lewat cara yang sama.

## 1. Tiga level risiko — pilih sebelum setup

| Level | Cara kerja | Siapa yang kirim ke pelanggan | Risiko blokir nomor WA |
|---|---|---|---|
| **1. Copilot (default, satu-satunya untuk agent skill ini)** | Admin menempel/meneruskan chat pelanggan ke bot (Telegram, atau WA nomor terpisah dalam mode self-chat ke diri sendiri). Bot balas dengan **draf**. | **Manusia**, selalu | Sangat rendah — tidak ada pesan otomatis ke pelanggan |
| 2. Auto-reply di nomor WA CS terpisah | Agent terpisah membalas otomatis pesan **masuk** di nomor WA khusus CS | Bot (otomatis) | **Ada** — WhatsApp Web (Baileys) adalah kanal tidak resmi; Syarat Layanan WhatsApp melarang "bulk/auto-messaging" dan "non-personal use" tanpa izin |
| 3. WhatsApp resmi (WABA lewat BSP, mis. Wati/Qontak) | Webhook BSP → OpenClaw, balasan lewat API resmi | Bot (otomatis, jalur resmi) | Rendah, tapi berbayar per percakapan; perlu jasa setup |

**Skill `agen-cs-toko` hanya menyiapkan Level 1 (Copilot) sampai tuntas.** Level 2 dan 3 hanya dijelaskan sebagai referensi setup lanjutan berbayar (jasa Komunitech) — skill tidak menjalankan/menjanjikan konfigurasinya secara otomatis, dan wajib ada persetujuan risiko tertulis dari pemilik sebelum Level 2 dipasang.

## 2. Kanal untuk pemilik (menerima draf & rekap) — Level 1

### Telegram (default, disarankan)
1. Buat bot lewat @BotFather di Telegram (dapat token).
2. Tambahkan ke OpenClaw — **perintah terverifikasi** (`openclaw channels add --help`, contoh resmi):
   ```
   openclaw channels add --channel telegram --token <token>
   ```
3. Kirim pesan pertama dari akun Telegram pemilik ke bot. Dengan `dmPolicy: "pairing"` (default), OpenClaw akan meminta persetujuan untuk pengirim baru; setujui dengan (**terverifikasi** `openclaw pairing --help`, `openclaw pairing approve --help`):
   ```
   openclaw pairing list telegram
   openclaw pairing approve telegram <KODE>
   ```
   Kode pairing berlaku 1 jam. `pairing` **aman dipakai di Telegram** karena kanal ini API resmi — tidak ada risiko nomor diblokir seperti WA Web.

### WhatsApp — **wajib nomor terpisah**, bukan nomor toko/pemilik
> **Peringatan penting (diverifikasi ulang, lihat catatan verifikasi di bawah):** pada `dmPolicy: "pairing"` di WhatsApp, OpenClaw **otomatis mengirim pesan kode pairing ke setiap pengirim baru yang belum dikenal** (kurang lebih 1×/jam per pengirim, sampai disetujui atau kedaluwarsa 1 jam). Ini berarti **bot mengirim pesan sendiri ke nomor asing lewat WA Web** — persis hal yang ingin kita hindari. Jika nomor yang ditautkan adalah nomor toko/pemilik yang juga dipakai pelanggan untuk chat, setiap pelanggan baru akan otomatis menerima pesan pairing dari bot. **Jangan pernah memakai `dmPolicy: "pairing"` di WhatsApp untuk skill ini.**
>
> Karena itu, dan sesuai keputusan pemilik Komunitech, WA **hanya** boleh dipakai dengan syarat berikut, semua wajib dipenuhi:
> 1. **Nomor WhatsApp terpisah** dari nomor yang dipakai pelanggan/toko (nomor baru khusus notifikasi ke pemilik sendiri).
> 2. **Persetujuan risiko tertulis** dari pemilik sebelum nomor ditautkan.
> 3. Konfigurasi kunci (lihat §4) yang memastikan **hanya pemilik/admin** yang bisa memicu bot di nomor itu — tidak ada `dmPolicy: "pairing"` atau `"open"`.

**Urutan wajib — set allowlist DULU, login belakangan** (supaya akun tidak pernah, walau sesaat, berstatus `dmPolicy: "pairing"`/tanpa allowlist sebelum bisa menerima pesan):
1. Tambahkan akun WA tanpa login dulu — **terverifikasi jalan**: `openclaw channels add --channel whatsapp --account cs` (memasang plugin WhatsApp & membuat entri akun "cs", belum scan QR, belum bisa menerima/mengirim pesan sungguhan).
2. Set konfigurasi allowlist **sebelum** memberi tahu nomor itu ke siapa pun (lihat §4) — **terverifikasi jalan**, ketiga perintah ini berhasil dan tervalidasi (lihat catatan verifikasi di bawah):
   ```
   openclaw config set channels.whatsapp.accounts.cs.dmPolicy allowlist
   openclaw config set channels.whatsapp.accounts.cs.allowFrom '["+62812xxxxxxx"]' --strict-json
   openclaw config set channels.whatsapp.accounts.cs.groupPolicy disabled
   openclaw config validate
   ```
   (ganti `+62812xxxxxxx` dengan nomor E.164 pemilik/admin yang sesungguhnya). Bila `allowFrom` sampai lupa diisi, OpenClaw sendiri memberi peringatan eksplisit saat `config set`: *"dmPolicy=allowlist but allowFrom is unset ... all DMs will be dropped"* — jadi kesalahan ini akan terlihat sebelum sempat dipakai, bukan diam-diam bocor.
3. Jika nomor terpisah ini dipakai untuk mengirim pesan ke diri sendiri (self-chat, mis. meneruskan draf ke nomor yang sama), pastikan `selfChatMode` sesuai kebutuhan — nilainya `true`/tidak diset berarti pesan dari nomor itu ke dirinya sendiri **diterima** sebagai input agent; `false` berarti pesan self-chat **diabaikan** (kunci `channels.whatsapp.selfChatMode`, boolean, **terverifikasi** ada di config schema).
4. **Baru setelah** allowlist terpasang dan tervalidasi, login lewat scan QR: `openclaw channels login --channel whatsapp --account cs` (dari alur onboarding OpenClaw; skill ini tidak menjalankan login, hanya menuntun urutannya).

## 3. Rekap harian terjadwal (opsional)

### 3a. Catat setiap draf ke log lokal (tanpa data pelanggan)
Automation rekap **tidak bisa membaca isi percakapan admin secara langsung** (jalan di sesi terpisah/`isolated`). Supaya rekap punya bahan yang nyata, setiap kali skill ini membuatkan draf atau menandai eskalasi, tambahkan **satu baris** ke file log harian `cs/log/<YYYY-MM-DD>.md`, format:
```
- [JAM] kategori: <FAQ/komplain/eskalasi/...> | eskalasi: ya/tidak | pertanyaan: <ringkas, TANPA nama/nomor pelanggan/pasien> | ada_di_pengetahuan: ya/tidak
```
Aturan wajib: **jangan pernah menulis nama, nomor HP, alamat, atau isi chat pelanggan/pasien secara lengkap** ke log ini — hanya kategori & ringkasan pertanyaan, sesuai UU PDP dan prinsip data minimal.

### 3b. Buat automation yang membaca log itu
Dibuat lewat `openclaw automations create` (alias `openclaw cron`; **terverifikasi** `openclaw automations create --help`, flag yang dipakai: `--cron`, `--tz`, `--session`, `--announce`, `--channel`, `--to`, `--name`). Contoh — kirim rekap CS tiap hari jam 20.00 WIB ke Telegram pemilik:
```
openclaw automations create \
  --cron "0 20 * * *" --tz "Asia/Jakarta" \
  --name "Rekap CS harian" \
  --message "Baca isi file cs/log/<tanggal hari ini>.md di workspace. Ringkas: jumlah baris (chat dibalas), 5 kategori pertanyaan terbanyak, daftar yang eskalasi:ya, dan pertanyaan dengan ada_di_pengetahuan:tidak (bahan perbaikan cs/PENGETAHUAN.md). Jika file belum ada/kosong, katakan belum ada aktivitas hari ini, jangan mengarang angka. Bahasa Indonesia, maksimal 15 baris." \
  --session isolated \
  --announce --channel telegram --to "<chat id Telegram pemilik>"
```
Catatan:
- `--tz "Asia/Jakarta"` wajib disebut eksplisit; tanpa ini cron memakai zona waktu komputer Gateway.
- `--session isolated` supaya sesi rekap tidak bercampur dengan sesi chat lain (flag tervalidasi di `--help`, nilai yang diterima: `main|isolated|current|session:<id>`).
- Uji sekali dulu sebelum jadwal aktif: `openclaw automations run <id>` (perlu id job hasil `create`; ada di keluaran `create` — **terverifikasi** subcommand ada lewat `openclaw automations --help`, dan wajib argumen id lewat `openclaw automations run --help`; tidak dijalankan otomatis oleh skill ini, tunjukkan hasilnya ke pemilik sebelum lanjut).
- **Gateway (komputer yang menjalankan OpenClaw) harus menyala** saat jadwal jatuh. Kalau laptop mati/tidur, rekap tidak terkirim — jelaskan ini ke pengguna dan sarankan mini PC/laptop yang selalu menyala, atau VPS milik member (opsional, jasa setup Komunitech).

## 4. Allowlist pengirim — jangan pernah pakai `allowFrom: ["*"]`
Kunci berikut **terverifikasi ada** di `openclaw config schema` (level channel, mis. `channels.telegram.*` dan `channels.whatsapp.*`), bisa diset lewat `openclaw config set <path> <nilai>` — **diuji sungguhan** (bukan hanya `--dry-run`, yang menurut OpenClaw sendiri "does not run schema/resolvability checks" untuk mode nilai biasa): ketiga kunci WA di §2 langkah 2 benar-benar ditulis ke `openclaw.json`, lalu dikonfirmasi valid lewat `openclaw config validate` (keluaran: `Config valid: ~/.openclaw/openclaw.json`) dan `openclaw config get channels.whatsapp.accounts.cs` menunjukkan nilai yang sama persis yang di-set:
- `dmPolicy` — enum: `pairing` (default) | `allowlist` | `open` | `disabled`.
- `allowFrom` — daftar pengirim DM yang diizinkan (array string, format nomor E.164 untuk WA mis. `+62812xxxxxxx`, username/id untuk Telegram).
- `groupPolicy` — enum: `open` | `disabled` | `allowlist` (default `allowlist`).
- `groupAllowFrom` — daftar pengirim yang boleh memicu bot **di dalam grup** (array string). **Bila `groupAllowFrom` tidak diisi, sistem otomatis memakai isi `allowFrom` sebagai gantinya** (fallback ini terverifikasi di dokumentasi resmi) — jadi mengisi `allowFrom` dengan nomor pemilik juga membatasi siapa yang bisa memicu bot di grup, selama `groupAllowFrom` sengaja dikosongkan.
- `channels.whatsapp.groups` (per-grup, object keyed ID grup `…@g.us`) — untuk aturan **khusus per grup** (boleh diabaikan bila `groupPolicy: "disabled"`, yang berarti bot tidak merespons di grup sama sekali).

**Aturan per kanal untuk skill ini:**
- **Telegram (pemilik):** `dmPolicy: "pairing"` (default, aman) + setujui manual lewat `openclaw pairing approve telegram <KODE>` — lihat §2.
- **WhatsApp (nomor terpisah, wajib):** `dmPolicy: "allowlist"` dengan `allowFrom` **hanya** nomor pemilik/admin, **tidak pernah** `"pairing"` atau `"open"`. `groupPolicy: "disabled"` (bot tidak perlu merespons grup di nomor CS). **Jangan pernah** memakai `allowFrom: ["*"]` di kanal manapun yang menerima chat dari luar.

`session.dmScope` (terverifikasi di schema, enum: `main` | `per-peer` | `per-channel-peer` | `per-account-channel-peer`) — untuk agen CS yang nanti melayani banyak pengirim (Level 2/3), wajib `per-channel-peer` atau lebih isolatif, supaya konteks tiap pelanggan tidak tercampur. Untuk Level 1 (hanya pemilik yang chat bot), skema default biasanya cukup.

## 5. Level 2 (auto-reply nomor WA CS terpisah) — HANYA lewat jasa setup, bukan swalayan
Bagian ini murni referensi untuk tim Komunitech saat mendampingi member yang memilih Level 2 dengan persetujuan risiko tertulis. **Skill ini tidak menjalankan langkah-langkah berikut secara otomatis, dan tidak menyarankan pengguna awam menjalankannya sendiri.**

- `tools.profile` (terverifikasi di schema: `agents.entries.<id>.tools.profile`, enum `minimal` | `coding` | `messaging` | `full`) — agent yang membaca pesan dari luar (pelanggan) **wajib** dibatasi `profile: "messaging"`, bukan `full` (default onboarding OpenClaw).
- Buat agent terpisah **tanpa** `--role` (nilai `coordinator/researcher/writer/reviewer` di `agents add --help` memberi identitas & susunan subagent bawaan untuk peran manajerial umum, bukan untuk agen CS — hasil ujinya salah, mis. identitas "Chief of Staff" dengan subagent yang tidak dipakai). Pakai `--workspace` + `--non-interactive`, lalu tulis aturan CS sendiri di `AGENTS.md`/`SOUL.md` workspace itu (dari `ATURAN.md` hasil wawancara skill ini):
  ```
  openclaw agents add cs --workspace <folder-workspace-cs> --non-interactive
  openclaw config set agents.entries.cs.tools.profile messaging
  ```
  (kedua perintah **terverifikasi jalan** di OpenClaw 2026.9.5: `agents add` tanpa `--role` menghasilkan identitas bersih `{"name":"cs", ...}`, dan `config set` mengonfirmasi `agents.entries.cs.tools.profile = "messaging"`.)
- Ikat ke akun WA CS terpisah lewat binding channel (`--bind whatsapp:cs` pada `agents add`, atau lewat `bindings` di config) — dilakukan bersama tim setup, bukan langkah mandiri.
- Nama-nama grup tool lain yang di-deny (mis. akses file/exec) mengikuti panduan "hardened baseline" resmi OpenClaw — cek docs.openclaw.ai/gateway/security/hardened-baseline sebelum dipasang.

## 6. Ringkasan larangan (Keputusan pemilik Komunitech, 2026-09-23)
- WA hanya dengan **nomor terpisah** untuk notifikasi ke pemilik sendiri, dan hanya dengan **persetujuan risiko tertulis**.
- **Jangan pernah** memakai `dmPolicy: "pairing"` di WhatsApp untuk skill ini — pakai `allowlist` + `allowFrom` nomor pemilik saja.
- Agen CS di WA = **Copilot**: AI menyiapkan draf, manusia yang mengirim. **Tidak ada** auto-send ke pelanggan lewat WA Web dari skill ini.
- **Tidak ada broadcast/blast** lewat OpenClaw.

## Catatan verifikasi (untuk kurator, bukan bagian panduan pembeli)
Peringatan pairing WA di §2 diverifikasi lewat pembacaan docs.openclaw.ai/channels/whatsapp (ringkasan: "unknown senders request pairing; owner approves") dan docs.openclaw.ai/channels/pairing ("the bot only sends the pairing message when a new request is created, roughly once per hour per sender") — kedua sumber sama-sama menegaskan **bot mengirim pesan pairing otomatis ke pengirim baru** saat permintaan dibuat, yang berarti pesan keluar ke nomor asing tanpa dikirim manusia. `channels.whatsapp.selfChatMode` dan `channels.whatsapp.groups` (per-grup) serta fallback `groupAllowFrom → allowFrom` juga dikonfirmasi lewat halaman yang sama dan `openclaw config schema`.

**v1.0.2 — urutan setup & validasi config (diuji ulang di HOME uji sementara, tanpa login kanal sungguhan):** `openclaw channels add --channel whatsapp --account cs` berhasil menambah akun WA "cs" tanpa scan QR. Setelahnya `openclaw config set channels.whatsapp.accounts.cs.dmPolicy allowlist`, `.allowFrom '["+6281234567890"]' --strict-json`, dan `.groupPolicy disabled` ketiganya berhasil ("Updated ..."), dan `openclaw config validate` mengembalikan `Config valid: ~/.openclaw/openclaw.json`; `openclaw config get channels.whatsapp.accounts.cs` mengonfirmasi ketiga nilai tersimpan persis. OpenClaw juga menampilkan peringatan sendiri saat `dmPolicy: allowlist` di-set sebelum `allowFrom` diisi ("all DMs will be dropped") — dicatat di §2 sebagai jaring pengaman tambahan. Ini menggantikan klaim versi sebelumnya yang hanya memakai `--dry-run` (yang menurut pesan OpenClaw sendiri tidak menjalankan pengecekan skema untuk mode nilai biasa).
