# Laporan Odoo otomatis ke Telegram pemilik (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur, 30 September 2026).** Bentuk perintah di bawah mengikuti pola yang sudah dijalankan
sungguhan di Gateway lokal OpenClaw 2026.9.6 untuk skill lain di repo Komunitech (`dolibarr-usaha`: job diterima,
jadwal & zona waktu tersimpan, `automations run` menjalankan script, galat tercatat `status: error`). Untuk
`odoo-usaha` sendiri, jadwal **belum** diuji di Gateway sungguhan dan **belum** diuji ke Odoo asli; pengiriman ke
Telegram belum diuji (butuh token bot asli). Jika sebuah opsi ditolak, jalankan `openclaw automations add --help`.

## 0. Aturan kanal (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**.
- **WhatsApp** hanya jika: (1) **nomor terpisah** milik pemilik, bukan nomor toko/CS; (2) laporan hanya ke pemilik sendiri; (3) pemilik membalas "ya, saya mengerti risikonya" setelah membaca: *"OpenClaw memakai WhatsApp Web (tidak resmi, scan QR). Pesan otomatis bisa membuat nomor diblokir. Untuk laporan ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya risiko ini."*
- **Tidak ada broadcast**, tidak ke grup, tidak ke pelanggan/karyawan. `laporan-harian` sengaja menyamarkan nama pelanggan (nomor faktur + inisial).
- Jadwal hanya menjalankan perintah **baca** (`laporan-harian`, `piutang --samarkan`, `stok-menipis`); tidak pernah `quotation` atau `--ya`.
- **Privasi:** teks laporan (nomor faktur, inisial, nama barang, angka penjualan) tersimpan di riwayat chat Telegram pemilik. Beri tahu pemilik sebelum membuat jadwal.
- Tunjukkan perintah + "Lanjut? (ya/tidak)" sebelum membuat jadwal apa pun.

## 1. Siapkan (sekali)
1. Gateway OpenClaw menyala saat jadwal. Odoo **lokal**: Odoo juga harus menyala (komputer toko yang tidak dimatikan, mini PC, VPS milik pengguna, atau jasa setup Komunitech). Odoo Online (*.odoo.com): cukup Gateway + internet.
2. Pakai kunci pengguna **Bot Laporan (baca-saja)** di file default `~/.komunitech/odoo-kunci.txt`, disimpan **oleh akun yang menjalankan Gateway**: `python3 <path odoo.py> simpan-kunci`. **Jangan** menaruh kunci di `--command-env` atau `--message` (isi jadwal tersimpan di database Gateway). Odoo 19+: kunci punya masa berlaku; catat tanggalnya dan ganti sebelum habis (laporan akan GAGAL kode 5 bila kunci kedaluwarsa).
3. Alamat/database sudah disimpan dengan `atur` oleh akun yang sama (berkas `~/.komunitech/odoo.json`, non-rahasia).
4. Telegram: buat bot di @BotFather → `openclaw channels add --channel telegram --token <token>` (pengguna sendiri yang menempel token di terminalnya) → kirim "halo" ke bot → `openclaw pairing list telegram` lalu `openclaw pairing approve telegram <KODE>`. Cara mencari ID chat: skill `laporan-otomatis-terjadwal`, `references/openclaw.md`.
5. Cari path lengkap (argv tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/odoo-usaha/scripts/odoo.py'))"
   ```
6. Uji dulu dari terminal: `python3 <path odoo.py> laporan-harian` harus menampilkan laporan (bukan GAGAL).

## 2. Pilihan 1 (disarankan): perintah langsung, tanpa AI
Script dijalankan Gateway, teksnya dikirim apa adanya. Tanpa kuota model, angka tidak bisa diubah AI.

**Harian 21.00 WIB:**
```bash
openclaw automations add --name "Laporan harian Odoo" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/odoo-usaha/scripts/odoo.py","laporan-harian"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- Alamat Odoo belum disimpan dengan `atur`: tambahkan `--command-env "ODOO_URL=https://tokosaya.odoo.com"`. Hanya alamat, **bukan kunci**.
- Toko tutup lewat tengah malam: `--cron "0 7 * * *"` dan tambahkan `"--tanggal","kemarin"` ke argv.
- WITA/WIT: `--tz Asia/Makassar` / `Asia/Jayapura` **dan** tambahkan `"--tz","WITA"` / `"--tz","WIT"` ke argv.
- Pengingat piutang mingguan (inisial, bukan nama): argv `[..., "piutang", "--samarkan", "--maks", "10"]`, `--cron "0 8 * * 1"`.
- Payload perintah = fitur admin Gateway. Tanpa hak itu: `requires credentials` → jalankan dari perangkat yang sudah dipasangkan atau dengan token Gateway pemilik.

## 3. Pilihan 2: lewat agent AI (Windows, atau ingin saran tambahan)
Memakai kuota model; `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari chat utama.
```bash
openclaw automations add --name "Laporan harian Odoo (agent)" --cron "0 21 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill odoo-usaha: jalankan scripts/odoo.py laporan-harian (hanya baca) lalu kirim teksnya apa adanya. Boleh tambah maksimal 3 saran singkat. Jangan ubah angka. Jangan jalankan quotation atau perintah dengan --ya. Jangan kirim ke siapa pun selain pemilik." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## 4. WhatsApp nomor terpisah (hanya jika syarat §0 terpenuhi)
Ganti baris terakhir menjadi `--announce --channel whatsapp --to "+62<nomor pemilik>"`. Pengiriman nyata ke WA ⚠️ belum diuji.

## 5. Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id> --wait` (cek `status`, `summary`, `deliveryStatus`) |
| Riwayat | `openclaw automations runs --id <id>` |
| Jeda / aktifkan | `openclaw automations disable <id>` / `openclaw automations enable <id>` |
| Hapus jadwal | `openclaw automations rm <id>` |

## 6. Jika bermasalah
- `Gateway not reachable` → Gateway/komputer belum menyala.
- `summary` "GAGAL: ... tidak bisa dihubungi" → Odoo lokal mati / internet putus.
- `summary` "Kunci API belum diatur" padahal di terminal jalan → kunci disimpan oleh akun lain; jalankan `simpan-kunci` dengan akun yang menjalankan Gateway.
- `summary` "Kunci API ditolak" → kunci dicabut/kedaluwarsa; buat kunci baru di Odoo, `simpan-kunci --ya`.
- `deliveryStatus: not-delivered` + `Telegram bot token missing` → kanal Telegram belum disiapkan (§1 langkah 4).
