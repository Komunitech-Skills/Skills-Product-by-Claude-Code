# Digest harian "tugas hari ini & terlambat" ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah mengikuti pola yang sudah dijalankan
sungguhan di Gateway lokal OpenClaw **2026.9.5/2026.9.6** untuk skill lain di repo ini (`dolibarr-usaha`,
`kasir-lokal`, `pengingat-follow-up`: job diterima, jadwal & zona waktu tersimpan, `automations run`
menjalankan script). Untuk `vikunja-tugas` sendiri, jadwal **belum** diuji di Gateway sungguhan
(hanya `scripts/uji_openclaw.sh`, uji muat/eligibility, bukan uji pengiriman); pengiriman ke
Telegram belum diuji (butuh token bot asli). Jika sebuah opsi ditolak, jalankan
`openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik/admin**, bukan pelanggan atau grup.
- **Tidak ada broadcast** dan tidak ada pesan otomatis ke pelanggan — Vikunja hanya berisi tugas internal, tapi aturan ini tetap berlaku untuk semua jadwal.
- Jadwal hanya menjalankan perintah **baca** (`hari-ini`, `terlambat`, `ringkasan`); tidak pernah `--ya`, `tambah`, `selesai`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** teks laporan berisi judul tugas dan nama anggota (username Vikunja), dan akan tersimpan di riwayat chat Telegram pemilik. Beri tahu pemilik. Judul tugas adalah data tim internal (bukan data pelanggan/PII pihak ketiga), tapi tetap sampaikan hal ini sebelum membuat jadwal.

## Syarat
- Gateway OpenClaw berjalan di komputer/jaringan yang bisa menjangkau Vikunja (idealnya **komputer yang sama** dengan Vikunja, karena Vikunja dibatasi ke `127.0.0.1` — lihat `docs/panduan-vikunja.md` §4) dan **menyala saat jadwal** (laptop/mini PC yang selalu menyala atau VPS milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui.
- Token API **baca-saja** sudah disimpan (`simpan-kunci`, lihat SKILL.md bagian Persiapan) — **jangan** pakai token baca-tulis untuk jadwal otomatis.
- Zona waktu jadwal (`--tz` di `openclaw automations add` dan `--tz` di `vikunja.py`) sebaiknya sama, mis. `Asia/Jakarta` untuk WIB.

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks script dikirim apa adanya. Tidak memakai kuota model; hasil selalu sama.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/vikunja-tugas/scripts/vikunja.py'))"
   ```
2. Digest harian 07.00 WIB (tugas hari ini):
   ```bash
   openclaw automations add --name "Vikunja - tugas hari ini" --cron "0 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/vikunja-tugas/scripts/vikunja.py","hari-ini"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
3. Digest tugas terlambat, jadwal terpisah 07.05 WIB (menghindari satu pesan terlalu panjang):
   ```bash
   openclaw automations add --name "Vikunja - tugas terlambat" --cron "5 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/vikunja-tugas/scripts/vikunja.py","terlambat"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Token/URL **tidak** ditulis ke dalam `--command-argv` (jangan pernah menambahkan `--kunci-file`/token ke argv jadwal). Script membaca token dari file default (`~/.komunitech/vikunja-kunci.txt`) atau ENV — untuk ENV, pakai `--command-env` **hanya** untuk `VIKUNJA_URL` (bukan `VIKUNJA_TOKEN`), mis. `--command-env '{"VIKUNJA_URL":"http://127.0.0.1:3456"}'`, agar token tidak pernah tersimpan di konfigurasi jadwal.
- Alamat Vikunja bukan bawaan → tambahkan URL lewat `--command-env` seperti di atas, bukan lewat argv.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Vikunja - digest harian (agent)" --cron "0 7 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill vikunja-tugas: jalankan hari-ini lalu terlambat (hanya baca; JANGAN menjalankan tambah/selesai/--ya). Kirim teksnya apa adanya ke saya. Jangan ubah judul/tanggal." \
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
- `summary` berisi "tidak bisa dihubungi" → Vikunja mati saat jadwal berjalan, atau `VIKUNJA_URL` di jadwal beda dengan yang dipakai saat chat biasa — samakan lewat `--command-env`.
- `summary` berisi "401" → token baca-saja kedaluwarsa/dihapus; buat token baru, `simpan-kunci` ulang di komputer yang sama dengan Gateway.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "tugas hari ini" tiap pagi, atau pasang alarm HP sendiri.
