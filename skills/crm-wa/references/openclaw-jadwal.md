# Pengingat follow-up otomatis ke Telegram (OpenClaw)

**Status verifikasi (jujur).** Bentuk perintah di bawah sama dengan yang sudah dijalankan sungguhan pada Gateway
lokal OpenClaw **2026.9.5** untuk skill `kasir-lokal` dan `pengingat-follow-up` (job diterima, jadwal & zona waktu
tersimpan, `automations run` menjalankan script). Khusus crm-wa, jadwal **belum** diuji di Gateway; pengiriman ke
Telegram belum diuji (butuh token bot asli). Jika sebuah opsi ditolak, jalankan `openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**, bukan pelanggan atau grup.
- **WhatsApp** hanya bila: nomor **terpisah** milik pemilik, pesan hanya ke pemilik sendiri, dan pemilik membalas
  "ya, saya mengerti risikonya" setelah membaca: *"OpenClaw memakai WhatsApp Web (tidak resmi). Pesan otomatis bisa
  membuat nomor diblokir. Untuk pengingat ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya
  risiko ini."*
- **Tidak ada broadcast** dan tidak ada pesan otomatis ke pelanggan. Jadwal hanya menjalankan perintah **baca**
  (`hari-ini`, `rekap`); tidak pernah `--ya`, `tambah`, `catat`, `terkirim`, `impor`, `hapus`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** teks `hari-ini` berisi nama, nomor, dan tautan wa.me pelanggan, dan akan tersimpan di riwayat chat
  Telegram pemilik. Beri tahu pemilik. Jika keberatan, pakai `--samarkan` (nama jadi inisial, nomor disamarkan, tanpa
  tautan); tautan tetap bisa diminta langsung ke agent di komputer ("bikinin pesan untuk K0002").

## Syarat
- Gateway OpenClaw berjalan di komputer yang **sama dengan database CRM** dan **menyala saat jadwal** (laptop/mini PC
  yang selalu menyala atau VPS milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui (lihat skill `laporan-otomatis-terjadwal`).
- Zona waktu jadwal (`--tz`) sama dengan zona CRM (`crm.py info`). Jam komputer/VPS boleh UTC; "hari ini" CRM
  mengikuti zona CRM.

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks script dikirim apa adanya. Tidak memakai kuota model; hasil selalu sama.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/crm-wa/scripts/crm.py'))"
   ```
2. Follow-up harian 08.00 WIB:
   ```bash
   openclaw automations add --name "Follow-up CRM harian" --cron "0 8 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/crm-wa/scripts/crm.py","hari-ini"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   Versi disamarkan: tambahkan `"--samarkan"` setelah `"hari-ini"`.
3. Rekap mingguan tiap Senin 07.30 WIB:
   ```bash
   openclaw automations add --name "Rekap CRM mingguan" --cron "30 7 * * 1" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/crm-wa/scripts/crm.py","rekap","--periode","minggu-lalu"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Database bukan di lokasi default → tambahkan `"--db","/path/crm.db"` setelah nama perintah di dalam argv.
- WITA: `--tz Asia/Makassar`; WIT: `--tz Asia/Jayapura`.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Follow-up CRM (agent)" --cron "0 8 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill crm-wa: jalankan hari-ini (hanya baca; JANGAN menjalankan perintah tulis, --ya, atau mengirim pesan ke pelanggan). Kirim teksnya apa adanya ke saya. Jangan ubah angka dan tanggal." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id>` |
| Lihat hasil | `openclaw automations runs <id>` (cek `status`, `summary`, `deliveryStatus`) |
| Hentikan / aktifkan | `openclaw automations disable <id>` / `enable <id>` |
| Hapus | `openclaw automations rm <id>` |

## Jika bermasalah
- `summary` berisi "Database CRM belum ada" → path `--db` di jadwal berbeda dengan yang dipakai saat chat; samakan.
- "sedang dipakai program lain" → saat jadwal berjalan ada perubahan yang sedang disimpan; data aman, jalankan
  `automations run <id>` lagi.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "follow-up hari ini" tiap pagi, atau pasang alarm HP sendiri.
