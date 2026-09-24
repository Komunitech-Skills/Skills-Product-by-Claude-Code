# Rekap absensi otomatis ke Telegram (OpenClaw)

Semua perintah di bawah **diverifikasi 23–24 September 2026 dengan OpenClaw 2026.9.5** (CLI asli, `--help`, lalu dijalankan sungguhan pada Gateway lokal dengan HOME sementara). Yang diverifikasi: job diterima Gateway, jadwal & zona waktu tersimpan, `automations run` menjalankan script dan menangkap teks rekap (status `ok`, exit code 0). Pengiriman ke Telegram **tidak** diuji karena butuh bot token asli; tanpa token, run tetap `ok` tetapi `deliveryStatus: not-delivered`.

Syarat:
- Gateway OpenClaw berjalan di komputer yang **menyala 24 jam** (laptop/mini PC selalu hidup, atau VPS milik pemilik) — komputer yang sama dengan database absensi.
- Kanal **Telegram** sudah tersambung (bot resmi) dan chat id pemilik diketahui. Cara menyiapkannya ada di skill `laporan-otomatis-terjadwal` (`references/openclaw.md`, bagian Telegram & mencari chat id). WhatsApp hanya dengan nomor terpisah + persetujuan risiko tertulis pemilik; tidak dipakai sebagai default.
- Jadwal **hanya menjalankan laporan (baca)**: `harian` dan `rekap`. Tidak pernah `--ya`, impor, catat, atau lembur.
- Selalu minta persetujuan pemilik sebelum membuat jadwal, dan tunjukkan perintahnya.

## Pilihan 1 (disarankan): payload perintah, tanpa model AI
Script dijalankan langsung oleh Gateway, keluaran teksnya dikirim apa adanya. Tidak memakai kuota model, hasil selalu sama.

1. Cari path lengkap script (payload `--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/absensi-lokal/scripts/absensi.py'))"
   ```
   Pastikan file itu ada. Jika skill dipasang di tempat lain, pakai path folder skill ini.
2. Rekap harian jam 10.00 WIB. Usaha pola 6 hari: `--cron "0 10 * * 1-6"` (Senin–Sabtu, seperti contoh). Usaha pola **5 hari**: pakai `--cron "0 10 * * 1-5"` (Senin–Jumat).
   ```bash
   openclaw automations add --name "Absensi harian" --cron "0 10 * * 1-6" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/absensi-lokal/scripts/absensi.py","harian"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
3. Rekap bulan lalu, setiap tanggal 1 jam 07.00 WIB (bahan gaji):
   ```bash
   openclaw automations add --name "Rekap absensi bulanan" --cron "0 7 1 * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/absensi-lokal/scripts/absensi.py","rekap","--bulan","lalu"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Database bukan di lokasi default? Tambahkan `"--db","/path/absensi.db"` ke dalam daftar argv.
- Alternatif `--command 'python3 ~/.openclaw/skills/absensi-lokal/scripts/absensi.py harian'` juga diterima (dijalankan lewat `sh -lc`), tetapi pesan dari profil shell bisa ikut terkirim (saat uji, baris tambahan dari profil muncul di atas rekap). `--command-argv` lebih bersih.
- Payload perintah adalah fitur admin Gateway (butuh hak `operator.admin`, yaitu pemilik Gateway). Contoh `sh`/`python3` di atas untuk Mac/Linux/VPS; di Windows **belum diuji** — pakai Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Berguna bila Pilihan 1 tidak bisa dipakai (mis. Windows). Memakai kuota model; `--tools exec,read` membatasi alat yang boleh dipakai; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Absensi harian (agent)" --cron "0 10 * * 1-6" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill absensi-lokal: jalankan perintah harian (hanya baca, jangan jalankan perintah tulis atau --ya) lalu kirim teksnya apa adanya." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## Mengelola jadwal (add, run, runs, list, disable, rm dijalankan saat uji; enable dicek lewat `--help`)
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang (tanpa menunggu jadwal) | `openclaw automations run <id>` |
| Lihat hasil & status kirim | `openclaw automations runs <id>` (cek `status`, `summary`, `deliveryStatus`) |
| Hentikan sementara / aktifkan | `openclaw automations disable <id>` / `openclaw automations enable <id>` |
| Hapus | `openclaw automations rm <id>` |

`automations` adalah alias `cron` (keduanya sama). Cron dibaca dengan zona waktu `--tz`; tanpa `--tz`, dipakai zona waktu komputer Gateway.

## Jika bermasalah
- `Gateway not reachable` → Gateway belum jalan; minta pemilik menyalakan OpenClaw/komputer 24 jam.
- `requires credentials` → jalankan dari perangkat yang sudah dipasangkan (paired) atau dengan token Gateway pemilik.
- `deliveryStatus: not-delivered` + `Telegram bot token missing` → kanal Telegram belum disiapkan.
- `summary` berisi `GAGAL: Database absensi belum ada` → path `--db` di jadwal berbeda dengan yang dipakai saat chat; samakan.
