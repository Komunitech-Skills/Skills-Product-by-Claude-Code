# Setup Kanal & Otomasi OpenClaw untuk Agen CS Toko

Semua perintah & kunci konfigurasi di halaman ini diverifikasi lewat `--help` OpenClaw 2026.9.5, `openclaw config schema`, dan docs.openclaw.ai (dicatat statusnya). Jangan menambah kunci config baru tanpa memverifikasi ulang lewat cara yang sama.

## 1. Tiga level risiko — pilih sebelum setup

| Level | Cara kerja | Siapa yang kirim ke pelanggan | Risiko blokir nomor WA |
|---|---|---|---|
| **1. Copilot (default, satu-satunya untuk agent skill ini)** | Admin menempel/meneruskan chat pelanggan ke bot (Telegram, atau chat WA ke diri sendiri). Bot balas dengan **draf**. | **Manusia**, selalu | Sangat rendah — tidak ada pesan otomatis ke pelanggan |
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
3. Kirim pesan pertama dari akun Telegram pemilik ke bot, lalu setujui *pairing* (DM pertama harus disetujui).

### WhatsApp ke diri sendiri (nomor pemilik, bukan nomor CS)
- Boleh dipakai **hanya** untuk menerima draf/rekap ke diri sendiri (self-chat), bukan untuk membalas pelanggan otomatis.
- Login tetap lewat scan QR: `openclaw channels login --channel whatsapp` (dari alur onboarding OpenClaw; skill ini tidak menjalankan login).
- **Jangan** set `dmPolicy: "open"` atau `allowFrom: ["*"]` pada akun ini — cukup nomor pemilik sendiri di `allowFrom` (lihat §4).

## 3. Rekap harian terjadwal (opsional)
Dibuat lewat `openclaw automations create` (alias `openclaw cron`; **terverifikasi** `openclaw automations create --help`, flag yang dipakai: `--cron`, `--tz`, `--session`, `--announce`, `--channel`, `--to`, `--name`). Contoh — kirim rekap CS tiap hari jam 20.00 WIB ke Telegram pemilik:
```
openclaw automations create \
  --cron "0 20 * * *" --tz "Asia/Jakarta" \
  --name "Rekap CS harian" \
  --message "Baca log draf balasan CS hari ini, ringkas: jumlah chat dibalas, 5 pertanyaan terbanyak, daftar yang dieskalasi, dan pertanyaan yang belum ada jawabannya di cs/PENGETAHUAN.md. Bahasa Indonesia, maksimal 15 baris." \
  --session isolated \
  --announce --channel telegram --to "<chat id Telegram pemilik>"
```
Catatan:
- `--tz "Asia/Jakarta"` wajib disebut eksplisit; tanpa ini cron memakai zona waktu komputer Gateway (terverifikasi lewat docs.openclaw.ai/automation/cron-jobs/schedules, sudah dicatat di riset internal 2026-09-23).
- `--session isolated` supaya sesi rekap tidak bercampur dengan sesi chat lain (flag tervalidasi di `--help`, nilai yang diterima: `main|isolated|current|session:<id>`).
- Uji sekali dulu sebelum jadwal aktif: `openclaw automations run <id>` (perlu id job hasil `create`; tidak dijalankan otomatis oleh skill ini, tunjukkan hasilnya ke pemilik sebelum lanjut).
- **Gateway (komputer yang menjalankan OpenClaw) harus menyala** saat jadwal jatuh. Kalau laptop mati/tidur, rekap tidak terkirim — jelaskan ini ke pengguna dan sarankan mini PC/laptop yang selalu menyala, atau VPS milik member (opsional, jasa setup Komunitech).

## 4. Allowlist pengirim — jangan pernah pakai `allowFrom: ["*"]`
Kunci berikut **terverifikasi ada** di `openclaw config schema` (level channel, mis. `channels.telegram.*` dan `channels.whatsapp.*`):
- `dmPolicy` — enum: `pairing` (default) | `allowlist` | `open` | `disabled`.
- `allowFrom` — daftar pengirim DM yang diizinkan (array string).
- `groupPolicy` — enum: `open` | `disabled` | `allowlist` (default `allowlist`).
- `groupAllowFrom` — daftar pengirim yang boleh memicu bot di dalam grup (array string).

Untuk agen CS Level 1 (pemilik menerima draf lewat Telegram/WA sendiri): pakai `dmPolicy: "pairing"` (default, cukup aman — pengirim baru harus disetujui) atau `dmPolicy: "allowlist"` + `allowFrom` berisi **hanya** nomor/username pemilik. **Jangan** memakai `dmPolicy: "open"` dengan `allowFrom: ["*"]` di kanal ini — itu berarti siapa pun bisa DM bot dan memicu balasan.

`session.dmScope` (terverifikasi di schema, enum: `main` | `per-peer` | `per-channel-peer` | `per-account-channel-peer`) — untuk agen CS yang nanti melayani banyak pengirim (Level 2/3), wajib `per-channel-peer` atau lebih isolatif, supaya konteks tiap pelanggan tidak tercampur. Untuk Level 1 (hanya pemilik yang chat bot), skema default biasanya cukup; tetap sebutkan opsi ini bila pemilik ingin menyiapkan Level 2.

## 5. Batasan tool untuk agent CS (bila nanti naik ke Level 2)
`tools.profile` (terverifikasi di schema, enum: `minimal` | `coding` | `messaging` | `full`) — agent yang membaca pesan dari luar (pelanggan) sebaiknya dibatasi `profile: "messaging"`, bukan `full` (default onboarding OpenClaw). Agent terpisah dibuat dengan:
```
openclaw agents add cs --role coordinator --bind whatsapp:cs
```
(`--role` dan `--bind` terverifikasi lewat `openclaw agents add --help`). Detail nama-nama grup tool yang di-deny (mis. akses file/exec) mengikuti panduan "hardened baseline" resmi OpenClaw — cek halaman docs.openclaw.ai/gateway/security/hardened-baseline sebelum dipasang, karena ini konfigurasi keamanan Level 2 yang sebaiknya didampingi (jasa setup), bukan dijalankan sendiri oleh pemula.

## 6. Ringkasan larangan (Keputusan pemilik Komunitech, 2026-09-23)
- WA hanya dengan **nomor terpisah** untuk notifikasi ke pemilik sendiri, dan hanya dengan **persetujuan risiko tertulis**.
- Agen CS di WA = **Copilot**: AI menyiapkan draf, manusia yang mengirim. **Tidak ada** auto-send ke pelanggan lewat WA Web dari skill ini.
- **Tidak ada broadcast/blast** lewat OpenClaw.
