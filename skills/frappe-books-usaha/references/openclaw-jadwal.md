# Laporan Frappe Books otomatis ke Telegram pemilik (OpenClaw)

**Status:** ⚠️ **BELUM DIVERIFIKASI untuk skill ini.** Perintah di bawah menyalin pola `openclaw automations add --command-argv`
yang sudah diuji pada skill `dolibarr-usaha` (OpenClaw 2026.9.6, CLI asli: jadwal diterima, `automations run --wait`
menjalankan script dan `summary` berisi teks laporan). Untuk `frappe-books-usaha` sendiri belum dijalankan di Gateway sungguhan,
dan pengiriman nyata ke Telegram belum diuji (butuh bot token asli).

## Aturan kanal (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**. Laporan keuangan tidak dikirim ke grup/karyawan/pelanggan.
- **WhatsApp** hanya dengan **nomor terpisah** milik pemilik + pemilik menulis "ya, saya mengerti risikonya" setelah dijelaskan
  bahwa OpenClaw memakai WhatsApp Web (tidak resmi) dan nomor bisa diblokir. Tidak ada broadcast.
- `laporan-harian` sengaja **tanpa nama pelanggan** (hanya nomor invoice).
- Tunjukkan perintah lengkap + "Lanjut? (ya/tidak)" sebelum membuat jadwal apa pun.

## Syarat
1. Gateway OpenClaw berjalan di **komputer yang sama** dengan file `.books.db` dan menyala saat jadwal
   (laptop/mini PC selalu menyala, atau jasa setup Komunitech). Frappe Books sendiri **tidak perlu dibuka** — script membaca file langsung.
2. Path lengkap script & database (argv tidak mengenal `~`):
   `python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/frappe-books-usaha/scripts/frappe_books.py'))"`
3. Uji dulu di terminal: `python3 <path script> laporan-harian --db "<path .books.db>"` harus menampilkan laporan (bukan GAGAL).

## Pilihan 1 (disarankan): perintah langsung, tanpa AI (angka tidak bisa diubah AI, tanpa kuota model)
Harian 21.00 WIB:
```bash
openclaw automations add --name "Laporan harian Frappe Books" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/frappe-books-usaha/scripts/frappe_books.py","laporan-harian","--db","/home/NAMA/Documents/Frappe Books/Toko Saya.books.db"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- Toko tutup lewat tengah malam: `--cron "0 7 * * *"` dan tambahkan `"--tanggal","kemarin"` ke argv.
- WITA/WIT: `--tz Asia/Makassar` / `Asia/Jayapura` **dan** `"--tz","WITA"` / `"--tz","WIT"` di argv.
- Piutang mingguan (Senin 08.00, nama disamarkan): argv `[..., "piutang", "--db", "<path>", "--samarkan"]`, `--cron "0 8 * * 1"`.
- Ringkasan bulan lalu (tanggal 1, 07.50): argv `[..., "penjualan", "--db", "<path>", "--bulan", "lalu", "--samarkan"]`, `--cron "50 7 1 * *"`.
- Windows: path pakai garis miring maju atau `\\`, dan `"python"`/`"py"` sebagai gantinya `"python3"`; `--command-argv` di Gateway Windows belum diuji → bila gagal pakai Pilihan 2.

## Pilihan 2: lewat agent AI (memakai kuota model)
```bash
openclaw automations add --name "Laporan harian Frappe Books (agent)" --cron "0 21 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill frappe-books-usaha: jalankan scripts/frappe_books.py laporan-harian --db '<path .books.db>' lalu kirim teksnya apa adanya. Boleh tambah maksimal 3 saran singkat. Jangan ubah angka. Jangan kirim ke siapa pun selain pemilik." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## Telegram (sekali)
Buat bot di @BotFather → `openclaw channels add --channel telegram --token <token>` → kirim "halo" ke bot dari akun pemilik →
`openclaw pairing list telegram` lalu `openclaw pairing approve telegram <KODE>`.

## Mengelola jadwal
`openclaw automations list` (lihat id) · `openclaw automations run <id> --wait` (uji sekarang; cek `status`, `summary`, `deliveryStatus`) ·
`openclaw automations disable <id>` / `enable <id>` · `openclaw automations rm <id>`.

## Jika bermasalah
- `summary` "GAGAL: File ... tidak ditemukan" → path `--db` salah atau file dipindah; cek ulang dengan perintah `cek`.
- "tidak bisa dibuka ... dikunci" → Frappe Books sedang menyimpan; jadwalkan di luar jam input, atau coba `run` lagi.
- `deliveryStatus: not-delivered` + `Telegram bot token missing` → kanal Telegram belum disiapkan.
- Kode keluar 4 (struktur berbeda) → Frappe Books diperbarui ke versi yang belum diuji; laporkan ke Komunitech.
