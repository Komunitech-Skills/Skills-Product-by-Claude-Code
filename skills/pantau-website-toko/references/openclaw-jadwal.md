# Ringkasan status website terjadwal ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah mengikuti pola yang sudah dijalankan
sungguhan di Gateway lokal OpenClaw **2026.9.5/2026.9.6** untuk skill lain di repo ini
(`vikunja-tugas`, `dolibarr-usaha`, `kasir-lokal`: job diterima, jadwal & zona waktu tersimpan,
`automations run` menjalankan script). Untuk `pantau-website-toko` sendiri, jadwal ini **belum**
diuji di Gateway sungguhan; pengiriman ke Telegram lewat OpenClaw belum diuji (butuh token bot
asli). Jika sebuah opsi ditolak, jalankan `openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik/admin toko**, bukan pelanggan.
- **Tidak ada broadcast** ke pelanggan lewat jadwal ini — hanya laporan status ke pemilik/admin.
- Jadwal hanya menjalankan perintah **baca** (`ringkasan`, `mingguan`); tidak pernah mengubah
  Uptime Kuma (skill ini memang tidak punya perintah tulis sama sekali).
- **Interval wajar, wajib.** Jangan jadwalkan `ringkasan`/`cek-cepat` lebih cepat dari **tiap 5
  menit** — Uptime Kuma sendiri sudah memantau terus-menerus (heartbeat interval-nya sendiri, lihat
  `docs/panduan-uptime-kuma.md` §5); jadwal di sini untuk **laporan ringkasan berkala** (harian/tiap
  beberapa jam), bukan menggantikan pemantauan Uptime Kuma. `cek-cepat` **tidak boleh** dijadwalkan
  berulang sama sekali untuk memantau situs pihak lain — itu di luar cakupan skill ini (lihat
  SKILL.md "Kapan TIDAK digunakan").
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** teks laporan berisi nama monitor (biasanya nama website/halaman toko sendiri, bukan
  data pelanggan) dan akan tersimpan di riwayat chat Telegram pemilik. Beri tahu pemilik sebelum
  membuat jadwal.

## Syarat
- Gateway OpenClaw berjalan di komputer/jaringan yang bisa menjangkau Uptime Kuma (idealnya
  **komputer/VPS yang sama**, karena disarankan diikat ke `127.0.0.1` — lihat
  `docs/panduan-uptime-kuma.md` §3/§5) dan **menyala saat jadwal** (laptop/mini PC yang selalu
  menyala atau VPS milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui.
- Status page Uptime Kuma sudah **dipublikasikan** dan dicoba manual dulu lewat perintah `cek`
  (lihat SKILL.md bagian A) sebelum dijadwalkan.
- Zona waktu jadwal (`--tz` di `openclaw automations add`) sebaiknya `Asia/Jakarta` untuk WIB.

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks laporan dikirim apa adanya. Tidak memakai kuota model; hasil selalu sama.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/pantau-website-toko/scripts/pantau.py'))"
   ```
2. Ringkasan harian jam 08.00 WIB:
   ```bash
   openclaw automations add --name "Pantau Website - ringkasan harian" --cron "0 8 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/pantau-website-toko/scripts/pantau.py","ringkasan","--status-url","http://127.0.0.1:3001/status/toko-saya"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   Ganti alamat status page sesuai milik pengguna (dicatat saat mengikuti `docs/panduan-uptime-kuma.md` §5).
3. Ringkasan mingguan, jadwal terpisah (mis. Senin jam 08.10 WIB):
   ```bash
   openclaw automations add --name "Pantau Website - ringkasan mingguan" --cron "10 8 * * 1" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/pantau-website-toko/scripts/pantau.py","mingguan","--hari","7"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   **Catatan penting:** `mingguan` membaca log lokal yang **hanya bertambah setiap kali `ringkasan`
   dijalankan** — jadwal harian di langkah 2 di atas WAJIB tetap ada agar `mingguan` punya data yang
   cukup (lihat SKILL.md bagian C).
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari
percakapan utama.
```bash
openclaw automations add --name "Pantau Website - ringkasan harian (agent)" --cron "0 8 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill pantau-website-toko: jalankan 'ringkasan' untuk status page http://127.0.0.1:3001/status/toko-saya (hanya baca; skill ini memang tidak punya perintah tulis). Kirim ringkasannya apa adanya ke saya, termasuk catatan jendela waktu downtime & sisa hari SSL bila ada." \
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
- `summary` berisi "tidak bisa dihubungi" → Uptime Kuma mati saat jadwal berjalan, atau alamat di
  jadwal beda dengan yang dicoba manual — samakan alamatnya.
- `summary` berisi "tidak ditemukan" (slug) → status page belum/tidak lagi dipublikasikan; cek
  langsung di Uptime Kuma (Settings status page → tombol Publish).
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat) — uji dulu lewat
  fitur **Test** di Uptime Kuma sendiri (`docs/panduan-uptime-kuma.md` §6) untuk memastikan bot &
  chat id benar, sebelum menyalahkan jadwal OpenClaw.
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "ringkasan status website saya" tiap pagi, atau
  pasang alarm HP sendiri; atau tetap andalkan notifikasi Telegram bawaan Uptime Kuma (§6) yang
  memang otomatis saat down, tanpa perlu jadwal terpisah untuk itu.
