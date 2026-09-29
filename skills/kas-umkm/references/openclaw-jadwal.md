# Ringkasan kas otomatis ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah disalin dari pola yang sudah dijalankan sungguhan pada Gateway
lokal OpenClaw **2026.9.5** untuk skill `kasir-lokal` dan `crm-wa` (job diterima, jadwal & zona waktu tersimpan,
`automations run` menjalankan script). Khusus kas-umkm, jadwal **belum** diuji di Gateway, dan pengiriman ke Telegram
belum diuji (butuh token bot asli). Jika sebuah opsi ditolak, jalankan `openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**, bukan karyawan, pelanggan, atau grup.
- **WhatsApp** hanya bila: nomor **terpisah** milik pemilik, pesan hanya ke pemilik sendiri, dan pemilik membalas
  "ya, saya mengerti risikonya" setelah membaca: *"OpenClaw memakai WhatsApp Web (tidak resmi). Pesan otomatis bisa
  membuat nomor diblokir. Untuk ringkasan ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya
  risiko ini."*
- Jadwal **hanya menjalankan perintah baca**: `rekap`, `saldo`, `info`. Tidak pernah `--ya`, `catat`, `pindah`,
  `opname`, `impor`, `batal`, `restore`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** ringkasan berisi saldo rekening, uang masuk/keluar, dan prive pemilik; teksnya akan tersimpan di riwayat
  chat Telegram pemilik. Beri tahu pemilik.

## Syarat
- Gateway OpenClaw berjalan di komputer yang **sama dengan database kas** dan **menyala saat jadwal** (laptop/mini PC
  yang selalu menyala atau VPS milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui (lihat skill `laporan-otomatis-terjadwal`).
- Zona waktu jadwal (`--tz`) sama dengan zona buku kas (`kas.py info`). Jam komputer/VPS boleh UTC; "hari ini" buku
  kas mengikuti zona buku kas.

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks script dikirim apa adanya. Tidak memakai kuota model; angka selalu sama dengan buku kas.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/kas-umkm/scripts/kas.py'))"
   ```
   Pastikan file itu ada. Jika skill dipasang di tempat lain, pakai path folder skill ini.
2. Ringkasan harian 21.00 WIB (sesuaikan dengan jam tutup; di atas jam tutup):
   ```bash
   openclaw automations add --name "Ringkasan kas harian" --cron "0 21 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/kas-umkm/scripts/kas.py","rekap","--tanggal","hari-ini"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
3. Rekap mingguan tiap Senin 07.30 WIB:
   ```bash
   openclaw automations add --name "Rekap kas mingguan" --cron "30 7 * * 1" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/kas-umkm/scripts/kas.py","rekap","--minggu","lalu"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
4. Rekap bulan lalu setiap tanggal 1 jam 07.00 WIB (termasuk peringatan prive bulanan):
   ```bash
   openclaw automations add --name "Rekap kas bulanan" --cron "0 7 1 * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/kas-umkm/scripts/kas.py","rekap","--bulan","lalu"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Usaha tutup setelah tengah malam? Jadwalkan pagi berikutnya dengan `"--tanggal","kemarin"`.
- Database bukan di lokasi default → tambahkan `"--db","/path/kas.db"` setelah nama perintah di dalam argv
  (mis. `...,"rekap","--db","/path/kas.db","--tanggal","hari-ini"]`).
- WITA: `--tz Asia/Makassar`; WIT: `--tz Asia/Jayapura`.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Ringkasan kas (agent)" --cron "0 21 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill kas-umkm: jalankan rekap --tanggal hari-ini (hanya baca; JANGAN menjalankan perintah tulis atau --ya). Kirim teksnya apa adanya ke saya. Jangan ubah angka dan tanggal." \
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
- `summary` berisi "Buku kas belum ada" → path `--db` di jadwal berbeda dengan yang dipakai saat chat; samakan.
- "sedang dipakai program lain" → saat jadwal berjalan ada catatan yang sedang disimpan; data aman, jalankan
  `automations run <id>` lagi.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "rekap kas hari ini" tiap malam, atau pasang alarm HP sendiri.
