# Laporan bulanan hledger otomatis ke Telegram pemilik (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status:** perintah di bawah mengikuti pola yang sudah diuji pada skill `dolibarr-usaha` (OpenClaw 2026.9.6, `automations add --command-argv`). Untuk `hledger-usaha` sendiri **belum diuji** di Gateway sungguhan; uji muat skill (`skills check`) mengikuti `scripts/uji_openclaw.sh` repo pengembang.

## Aturan kanal (keputusan pemilik Komunitech)
- Telegram (bot resmi) = default, `--to` selalu ID chat **pemilik**. Laporan keuangan tidak dikirim ke grup/karyawan/pelanggan.
- WhatsApp hanya dengan nomor terpisah milik pemilik + persetujuan risiko tertulis (OpenClaw memakai WhatsApp Web, tidak resmi).
- Tunjukkan perintah + "Lanjut? (ya/tidak)" sebelum membuat jadwal.

## Syarat
1. Gateway OpenClaw jalan di komputer yang **sama** dengan file `Pembukuan/usaha.journal` dan menyala saat jadwal.
2. Cari path lengkap script (argv tidak mengenal `~`):
   `python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/hledger-usaha/scripts/hledger_usaha.py'))"`
3. Uji dulu di terminal: `python3 <path> bulanan --bulan lalu` harus menampilkan laporan.

## Tanggal 1 tiap bulan, 07.50 WIB, laporan bulan lalu (tanpa AI, angka tidak bisa diubah)
```bash
openclaw automations add --name "Laporan bulanan pembukuan" --cron "50 7 1 * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/hledger-usaha/scripts/hledger_usaha.py","bulanan","--bulan","lalu"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- File jurnal bukan di `~/Pembukuan/usaha.journal`: tambahkan `"--jurnal","/path/lengkap/usaha.journal"` ke argv.
- Ingat: laporan bulan lalu baru akurat bila stok akhir (`stok-akhir`) dan mutasi bank sudah dicatat. Alternatif: jadwalkan tanggal 5.
- Neraca tidak seimbang → kode keluar 4, jadwal tercatat gagal (sengaja, agar pemilik tahu).

Kelola jadwal: `openclaw automations list`, `run <id> --wait`, `disable <id>`, `rm <id>`.
