# Rekap kasir otomatis ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

Semua perintah di bawah **diverifikasi 24 September 2026 dengan OpenClaw 2026.9.5** (CLI asli: `--help`, lalu dijalankan sungguhan pada Gateway lokal dengan HOME sementara). Yang diverifikasi: `skills install <folder> --global` + `skills check --json` (kasir-lokal eligible, terlihat model, bisa dipanggil), job diterima Gateway, jadwal & zona waktu tersimpan (21.00 WIB → `nextRunAt` 14.00 UTC), `automations run` menjalankan script dan menangkap teks rekap (status `ok`, exit code 0), `runs`, `list`, `disable`, `enable`, `rm`. Pengiriman ke Telegram **tidak** diuji karena butuh bot token asli; tanpa token, run tetap `ok` tetapi `deliveryStatus: not-delivered`.

Syarat:
- Gateway OpenClaw berjalan di komputer yang **sama dengan database kasir** dan **menyala saat jadwal** (komputer kasir yang tidak dimatikan malam hari, mini PC, atau VPS milik pemilik). Jam komputer harus benar (boleh UTC di VPS); "hari ini" dan "per jam" memakai zona toko yang diatur `--zona`.
- Kanal **Telegram** sudah tersambung (bot resmi) dan chat id pemilik diketahui (lihat skill `laporan-otomatis-terjadwal`, `references/openclaw.md`). WhatsApp hanya dengan nomor terpisah + persetujuan risiko tertulis pemilik; bukan default.
- Jadwal **hanya menjalankan laporan (baca)**: `rekap`, `info`. Tidak pernah `--ya`, `jual`, `void`, `tutup-kasir`.
- Minta persetujuan pemilik sebelum membuat jadwal dan tunjukkan perintahnya.

## Pilihan 1 (disarankan): payload perintah, tanpa model AI
Script dijalankan langsung oleh Gateway, teksnya dikirim apa adanya. Tidak memakai kuota model; hasil selalu sama.

1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/kasir-lokal/scripts/kasir.py'))"
   ```
   Pastikan file itu ada. Jika skill dipasang di tempat lain, pakai path folder skill ini.
2. Rekap harian setiap jam 21.00 WIB (sesuaikan dengan jam tutup toko; di atas jam tutup):
   ```bash
   openclaw automations add --name "Rekap kasir harian" --cron "0 21 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/kasir-lokal/scripts/kasir.py","rekap","--tanggal","hari-ini"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
3. Rekap bulan lalu setiap tanggal 1 jam 07.00 WIB (bahan PPh final & evaluasi):
   ```bash
   openclaw automations add --name "Rekap kasir bulanan" --cron "0 7 1 * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/kasir-lokal/scripts/kasir.py","rekap","--bulan","lalu"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Toko tutup setelah tengah malam? Jadwalkan pagi berikutnya dengan `"--tanggal","kemarin"`.
- Database bukan di lokasi default? Tambahkan `"--db","/path/kasir.db"` **setelah** `"rekap"` di dalam argv.
- WITA: `--tz Asia/Makassar`; WIT: `--tz Asia/Jayapura`. Samakan dengan zona toko (`kasir.py info` menampilkan zona toko dan memperingatkan bila jam komputer/VPS berbeda). Sejak v1.1.0 "hari ini" dan pembagian per jam memakai zona toko, bukan jam komputer.
- Payload perintah adalah fitur admin Gateway (pemilik Gateway). Contoh `python3` di atas untuk Mac/Linux/VPS; di Windows **belum diuji** — pakai Pilihan 2 (atau `"py"` sebagai ganti `"python3"`, belum diuji).

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model; `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama. Job ini diverifikasi sampai diterima Gateway (`payload.kind: agentTurn`, `toolsAllow` exec & read); menjalankannya butuh API key model, jadi isi rekapnya tidak diuji.
```bash
openclaw automations add --name "Rekap kasir (agent)" --cron "0 21 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill kasir-lokal: jalankan rekap --tanggal hari-ini (hanya baca, jangan jalankan perintah tulis atau --ya) lalu kirim teksnya apa adanya." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang (tanpa menunggu jadwal) | `openclaw automations run <id>` |
| Lihat hasil & status kirim | `openclaw automations runs <id>` (cek `status`, `summary`, `deliveryStatus`) |
| Hentikan sementara / aktifkan | `openclaw automations disable <id>` / `openclaw automations enable <id>` |
| Hapus | `openclaw automations rm <id>` |

`automations` adalah alias `cron`. Cron dibaca dengan zona waktu `--tz`; tanpa `--tz` dipakai zona waktu komputer Gateway.

## Jika bermasalah
- `Gateway not reachable` → Gateway belum jalan; nyalakan OpenClaw/komputer.
- `requires credentials` → jalankan dari perangkat yang sudah dipasangkan (paired) atau dengan token Gateway pemilik (`--token`).
- `deliveryStatus: not-delivered` + `Telegram bot token missing` → kanal Telegram belum disiapkan.
- `summary` berisi `GAGAL: Database kasir belum ada` → path `--db` di jadwal berbeda dengan yang dipakai saat chat; samakan.
- `summary` berisi "sedang dipakai program lain" → saat jadwal berjalan ada transaksi yang sedang disimpan; data aman, jalankan `automations run <id>` lagi.
