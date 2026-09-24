# Laporan otomatis ke Telegram pemilik (OpenClaw)

**Status verifikasi (24 September 2026, OpenClaw 2026.9.5, CLI asli, HOME sementara, Gateway lokal
`gateway run --dev --allow-unconfigured --bind loopback`):**
- ✅ `skills install <folder> --global` untuk skill ini + 4 alatnya, lalu `skills check --json` → `laporan-harian-usaha` ada di `eligible` dan `modelVisible`.
- ✅ `automations add` dengan `--command-argv` diterima: `schedule {cron "0 21 * * *", tz "Asia/Jakarta"}`, `nextRunAt` 14.00 UTC = **21.00 WIB**. Jadwal Senin `0 7 * * 1` → `nextRunAt` Senin 00.00 UTC = **07.00 WIB**.
- ✅ `automations run <id> --wait` menjalankan script sungguhan: `status: ok`, exit code 0, `summary` berisi teks laporan lengkap (penjualan, stok, kehadiran, tagihan).
- ✅ `--command-env` dan `--command-cwd` tersimpan di payload dan dipakai saat run. ✅ `list`, `runs --id`, `disable`, `enable`, `rm`.
- ✅ Pilihan 2 (agent) diterima Gateway: `payload.kind: agentTurn`, `toolsAllow: ["exec","read"]`. Isi jawabannya **tidak** diuji (butuh API key model).
- ⚠️ **Pesan sampai di Telegram belum diuji** (butuh bot token asli). Tanpa token: `deliveryStatus: not-delivered`, `Telegram bot token missing`. Artinya job memang mencoba mengirim.
- ⚠️ Gateway Windows belum diuji untuk `--command-argv`; di Windows pakai Pilihan 2.

## 0. Aturan kanal (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` = ID chat **pemilik**. Penerima tambahan hanya **pemilik bersama/pengelola yang pemilik tunjuk secara eksplisit**, masing-masing lewat **jadwal terpisah** ke chat pribadinya sendiri (`--to` = ID chat orang itu), tidak pernah ke grup.
- **WhatsApp** hanya jika: (1) **nomor terpisah** milik pemilik, bukan nomor toko/CS; (2) laporan hanya ke pemilik sendiri; (3) pemilik membalas "ya, saya mengerti risikonya" setelah membaca: *"OpenClaw memakai WhatsApp Web (tidak resmi, scan QR). Pesan otomatis bisa membuat nomor diblokir. Untuk laporan ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya risiko ini."*
- **Tidak ada broadcast**, tidak ke grup, tidak ke pelanggan/karyawan (kecuali pengelola yang ditunjuk eksplisit seperti di atas).
- Tunjukkan perintah + "Lanjut? (ya/tidak)" sebelum membuat jadwal apa pun.

## 1. Siapkan (sekali)
1. Gateway OpenClaw berjalan di **komputer yang sama dengan database kasir/stok/absensi**, dan menyala saat jadwal (komputer toko yang tidak dimatikan, mini PC, atau VPS milik pemilik). Jika mati jam 21.00, laporan **tidak terkirim** dan tidak ada pesan error. Opsi: komputer selalu menyala, VPS sendiri, atau jasa setup Komunitech.
2. Skill ini dan alat-alatnya terpasang di folder yang sama, mis. `openclaw skills install ./laporan-harian-usaha --global` (juga `kasir-lokal`, `buku-stok`, `absensi-lokal`, `pengingat-follow-up` yang dipakai).
3. Telegram: buat bot di @BotFather → `openclaw channels add --channel telegram --token <token>` → kirim "halo" ke bot dari akun pemilik → `openclaw pairing list telegram` lalu `openclaw pairing approve telegram <KODE>`. Cara mencari ID chat: skill `laporan-otomatis-terjadwal`, `references/openclaw.md`.
4. Cari path lengkap (argv tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/laporan-harian-usaha/scripts/laporan.py'))"
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/workspace'))"
   ```
5. Uji dulu dari terminal: `python3 <path laporan.py>` harus menampilkan laporan. Bagian "Belum ada data" padahal alatnya dipakai → lokasi data berbeda; tambahkan `--kasir-db`/`--stok-db`/`--absensi-db`/`--pengingat` ke argv.

## 2. Pilihan 1 (disarankan): perintah langsung, tanpa AI
Script dijalankan Gateway, teksnya dikirim apa adanya. Tidak memakai kuota model, hasil selalu sama, tidak ada AI yang bisa salah mengubah angka.

**Harian 21.00 WIB:**
```bash
openclaw automations add --name "Laporan harian usaha" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/laporan-harian-usaha/scripts/laporan.py"]' \
  --command-cwd "/home/NAMA/.openclaw/workspace" \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
**Mingguan Senin 07.00 WIB** (minggu lalu Senin–Minggu vs minggu sebelumnya):
```bash
openclaw automations add --name "Laporan mingguan usaha" --cron "0 7 * * 1" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/laporan-harian-usaha/scripts/laporan.py","--periode","mingguan"]' \
  --command-cwd "/home/NAMA/.openclaw/workspace" \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- `--command-cwd` = folder yang berisi `pengingat/DAFTAR.csv` (workspace OpenClaw). Alternatif: tambahkan `"--pengingat","/path/lengkap/pengingat/DAFTAR.csv"` ke argv (diuji).
- Data di lokasi lain: tambahkan ke argv, mis. `"--kasir-db","/path/kasir.db"`, atau `--command-env "KOMUNITECH_DATA=/path/folder"` (diuji).
- Nama karyawan jadi inisial: tambahkan `"--samarkan"` ke argv (diuji).
- Toko tutup lewat tengah malam: jadwalkan `--cron "0 7 * * *"` dan tambahkan `"--tanggal","kemarin"`.
- WITA/WIT: ganti `--tz Asia/Makassar` / `Asia/Jayapura` **dan** tambahkan `"--tz","Asia/Makassar"` ke argv.
- Jadwal setelah tengah malam tanpa `"--tanggal","kemarin"` akan melaporkan tanggal baru (masih kosong).
- Payload perintah = fitur admin Gateway (pemilik Gateway). Tanpa hak itu: `requires credentials` → jalankan dari perangkat yang sudah dipasangkan atau dengan `--token` Gateway pemilik.

## 3. Pilihan 2: lewat agent AI (Windows, atau ingin saran tambahan)
Memakai kuota model; `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari chat utama.
```bash
openclaw automations add --name "Laporan harian (agent)" --cron "0 21 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill laporan-harian-usaha: jalankan scripts/laporan.py (hanya baca) lalu kirim teksnya apa adanya. Boleh tambah maksimal 3 saran singkat di bawahnya. Jangan ubah angka. Jangan kirim ke siapa pun selain pemilik." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## 4. WhatsApp nomor terpisah (hanya jika syarat §0 terpenuhi)
Ganti baris terakhir menjadi `--announce --channel whatsapp --to "+62<nomor pemilik>"`. Kanal WA harus sudah ditambahkan (`openclaw channels add --channel whatsapp`, lalu `openclaw channels login --channel whatsapp`, scan QR). Pengiriman nyata ke WA ⚠️ belum diuji.

## 5. Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id> --wait` (cek `status`, `summary`, `deliveryStatus`) |
| Riwayat | `openclaw automations runs --id <id>` |
| Jeda / aktifkan | `openclaw automations disable <id>` / `openclaw automations enable <id>` |
| Hapus | `openclaw automations rm <id>` |

`disable/enable/run/rm` memakai **id** (dari output `add` atau `list`), bukan nama.

## 6. Jika bermasalah
- `Gateway not reachable` → Gateway/komputer belum menyala.
- `deliveryStatus: not-delivered` + `Telegram bot token missing` → kanal Telegram belum disiapkan (§1 langkah 3).
- `summary` berisi "Belum ada data (...)" padahal alat dipakai → path data di jadwal beda dengan saat chat; samakan (§2).
- `summary` berisi "sedang dipakai program lain" → saat jadwal ada transaksi yang sedang disimpan; data aman, `automations run <id> --wait` lagi.
- `summary` berisi "Jam komputer ini bukan Asia/Jakarta" → atur zona waktu komputer Gateway ke WIB/WITA/WIT yang benar.
