# Ringkasan piutang harian ke Telegram (OpenClaw)

**Status verifikasi (jujur).** Bentuk perintah di bawah disalin dari pola yang sudah dijalankan sungguhan pada
Gateway lokal OpenClaw untuk skill `crm-wa`, `kasir-lokal`, dan `pengingat-follow-up` (job diterima, jadwal & zona
waktu tersimpan, `automations run` menjalankan script). Khusus buku-piutang, jadwal **belum** diuji di Gateway;
pengiriman ke Telegram belum diuji (butuh token bot asli). Jika sebuah opsi ditolak, jalankan
`openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**, bukan pelanggan atau grup.
- **WhatsApp** hanya bila: nomor **terpisah** milik pemilik, pesan hanya ke pemilik sendiri, dan pemilik membalas
  "ya, saya mengerti risikonya" setelah membaca: *"OpenClaw memakai WhatsApp Web (tidak resmi). Pesan otomatis bisa
  membuat nomor diblokir. Untuk pengingat ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya
  risiko ini."*
- **Tidak ada broadcast** dan tidak ada pesan tagihan otomatis ke pelanggan. Jadwal hanya menjalankan perintah
  **baca** (`ringkasan`, `jatuh-tempo`, `rekap`); tidak pernah `--ya`, `catat`, `bayar`, `terkirim`, `impor`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** tanpa `--samarkan`, teks berisi nama pelanggan dan nominal utangnya, dan akan tersimpan di riwayat
  chat Telegram pemilik. Default yang disarankan: `--samarkan` (nama jadi inisial, kode pelanggan tetap, nomor WA
  tidak ditampilkan). Draf pesan tagihan & tautan wa.me tidak ikut dijadwalkan; minta langsung ke agent di komputer
  ("pesan tagihan untuk P0002").

## Syarat
- Gateway OpenClaw berjalan di komputer yang **sama dengan database piutang** dan **menyala saat jadwal**
  (laptop/mini PC yang selalu menyala atau VPS milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui (lihat skill `laporan-otomatis-terjadwal`).
- Zona waktu jadwal (`--tz`) sama dengan zona buku piutang (`piutang.py info`).

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks script dikirim apa adanya. Tidak memakai kuota model; hasil selalu sama.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/buku-piutang/scripts/piutang.py'))"
   ```
2. Ringkasan harian 07.45 WIB (disamarkan):
   ```bash
   openclaw automations add --name "Ringkasan piutang harian" --cron "45 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/buku-piutang/scripts/piutang.py","ringkasan","--samarkan"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   Pemilik ingin nama lengkap: hapus `"--samarkan"` setelah ia menyetujui catatan privasi di atas.
3. Rekap bulanan tiap tanggal 1 pukul 07.50 WIB:
   ```bash
   openclaw automations add --name "Rekap piutang bulanan" --cron "50 7 1 * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/buku-piutang/scripts/piutang.py","rekap","--periode","bulan-lalu","--samarkan"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Database bukan di lokasi default → tambahkan `"--db","/path/piutang.db"` setelah nama perintah di dalam argv.
- WITA: `--tz Asia/Makassar`; WIT: `--tz Asia/Jayapura`.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Ringkasan piutang (agent)" --cron "45 7 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill buku-piutang: jalankan ringkasan --samarkan (hanya baca; JANGAN menjalankan perintah tulis, --ya, atau mengirim pesan ke pelanggan). Kirim teksnya apa adanya ke saya. Jangan ubah angka dan tanggal." \
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
- `summary` berisi "Database piutang belum ada" → path `--db` di jadwal berbeda dengan yang dipakai saat chat;
  samakan.
- "sedang dipakai program lain" → saat jadwal berjalan ada perubahan yang sedang disimpan; data aman, jalankan
  `automations run <id>` lagi.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "ringkasan piutang" tiap pagi, atau pasang alarm HP sendiri.
