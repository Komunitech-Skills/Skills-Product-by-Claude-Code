# Laporan Dolibarr otomatis ke Telegram pemilik (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (24 September 2026, OpenClaw 2026.9.6, CLI asli, HOME sementara, Gateway lokal
`gateway run --dev --allow-unconfigured --bind loopback --auth token`), terhadap Dolibarr asli 24.0.1:**
- ✅ `skills check --json` → `dolibarr-usaha` ada di `eligible`, `modelVisible`, `commandVisible`.
- ✅ `automations add` dengan `--command-argv` + `--command-env DOLIBARR_URL=...` diterima: `schedule {cron "0 21 * * *", tz "Asia/Jakarta"}`, `nextRunAt` = **21.00 WIB**.
- ✅ `automations run <id> --wait` menjalankan script sungguhan: `status: ok`, `summary` = teks laporan lengkap dari Dolibarr. Kunci API dibaca dari file `~/.komunitech/dolibarr-kunci.txt` milik akun Gateway (tidak ditaruh di jadwal).
- ✅ Dolibarr mati saat jadwal → `status: error`, `summary` berisi "GAGAL: Dolibarr ... tidak bisa dihubungi ... Saran: Nyalakan Dolibarr", exit code 3.
- ⚠️ **Pesan sampai di Telegram belum diuji** (butuh bot token asli). Tanpa token: `deliveryStatus: not-delivered`, `Telegram bot token missing`. Apakah pesan GAGAL juga dikirim ke Telegram belum diketahui.
- ⚠️ Gateway Windows belum diuji untuk `--command-argv`; di Windows pakai Pilihan 2.

## 0. Aturan kanal (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**.
- **WhatsApp** hanya jika: (1) **nomor terpisah** milik pemilik, bukan nomor toko/CS; (2) laporan hanya ke pemilik sendiri; (3) pemilik membalas "ya, saya mengerti risikonya" setelah membaca: *"OpenClaw memakai WhatsApp Web (tidak resmi, scan QR). Pesan otomatis bisa membuat nomor diblokir. Untuk laporan ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya risiko ini."*
- **Tidak ada broadcast**, tidak ke grup, tidak ke pelanggan/karyawan. Laporan harian sengaja **tanpa nama pelanggan** (hanya nomor invoice).
- Tunjukkan perintah + "Lanjut? (ya/tidak)" sebelum membuat jadwal apa pun.

## 1. Siapkan (sekali)
1. Gateway OpenClaw berjalan di **komputer yang sama dengan Dolibarr (DoliWamp)** dan keduanya menyala saat jadwal. Komputer mati/DoliWamp belum dijalankan jam 21.00 → laporan gagal. Opsi: komputer toko yang tidak dimatikan, mini PC, atau jasa setup Komunitech.
2. Pakai kunci user **baca-saja** (`api_baca`, panduan §6.1) untuk jadwal; kunci yang bisa membuat draf juga bisa memvalidasi/menandai lunas lewat API, jadi jangan dipakai untuk jadwal. Kunci sudah disimpan **oleh akun yang menjalankan Gateway**: `python3 <path dolibarr.py> simpan-kunci` (lihat SKILL.md). **Jangan** menaruh kunci di `--command-env` atau `--message`: isi jadwal tersimpan di database Gateway dan bisa terbaca.
3. Telegram: buat bot di @BotFather → `openclaw channels add --channel telegram --token <token>` → kirim "halo" ke bot dari akun pemilik → `openclaw pairing list telegram` lalu `openclaw pairing approve telegram <KODE>`. Cara mencari ID chat: skill `laporan-otomatis-terjadwal`, `references/openclaw.md`.
4. Cari path lengkap (argv tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/dolibarr-usaha/scripts/dolibarr.py'))"
   ```
5. Uji dulu dari terminal: `python3 <path dolibarr.py> laporan-harian` harus menampilkan laporan (bukan GAGAL).

## 2. Pilihan 1 (disarankan): perintah langsung, tanpa AI
Script dijalankan Gateway, teksnya dikirim apa adanya. Tanpa kuota model, angka tidak bisa diubah AI.

**Harian 21.00 WIB:**
```bash
openclaw automations add --name "Laporan harian Dolibarr" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/dolibarr-usaha/scripts/dolibarr.py","laporan-harian"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- Dolibarr bukan di `http://localhost/dolibarr`: tambahkan `--command-env "DOLIBARR_URL=http://localhost:8080/dolibarr"` (diuji). Hanya alamat, **bukan kunci**.
- Toko tutup lewat tengah malam: `--cron "0 7 * * *"` dan tambahkan `"--tanggal","kemarin"` ke argv.
- WITA/WIT: `--tz Asia/Makassar` / `Asia/Jayapura` **dan** tambahkan `"--tz","WITA"` / `"--tz","WIT"` ke argv.
- Pengingat piutang mingguan untuk pemilik (dengan inisial, bukan nama): argv `[..., "piutang", "--samarkan"]`, `--cron "0 8 * * 1"`.
- Payload perintah = fitur admin Gateway. Tanpa hak itu: `requires credentials` → jalankan dari perangkat yang sudah dipasangkan atau dengan `--token` Gateway pemilik.

## 3. Pilihan 2: lewat agent AI (Windows, atau ingin saran tambahan)
Memakai kuota model; `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari chat utama.
```bash
openclaw automations add --name "Laporan harian Dolibarr (agent)" --cron "0 21 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill dolibarr-usaha: jalankan scripts/dolibarr.py laporan-harian (hanya baca) lalu kirim teksnya apa adanya. Boleh tambah maksimal 3 saran singkat. Jangan ubah angka. Jangan jalankan perintah yang menulis (tanpa --ya). Jangan kirim ke siapa pun selain pemilik." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
Isi jawaban agent **tidak** diuji (butuh API key model).

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
- `summary` "GAGAL: ... tidak bisa dihubungi" → DoliWamp belum dijalankan (menu Start > Dolibarr > Tools > Start DoliWamp server); atur DoliWamp agar ikut menyala saat Windows mulai (panduan §8).
- `summary` "Kunci API belum diatur" padahal di terminal jalan → kunci disimpan oleh akun lain; jalankan `simpan-kunci` dengan akun yang menjalankan Gateway.
- `summary` "401" → kunci diganti di Dolibarr; simpan kunci baru.
- `deliveryStatus: not-delivered` + `Telegram bot token missing` → kanal Telegram belum disiapkan (§1 langkah 3).
