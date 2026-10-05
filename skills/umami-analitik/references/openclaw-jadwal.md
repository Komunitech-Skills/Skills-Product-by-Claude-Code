# Laporan web mingguan ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah disalin dari pola yang sudah dijalankan
sungguhan di Gateway lokal OpenClaw **2026.9.5/2026.9.6** untuk skill lain di repo ini (`dolibarr-usaha`,
`kasir-lokal`, `pengingat-follow-up`: job diterima, jadwal & zona waktu tersimpan, `automations run`
menjalankan script) dan sama dengan `inventree-gudang`/`pantau-website-toko`. Untuk `umami-analitik` sendiri,
jadwal **belum** diuji di Gateway sungguhan dan pengiriman ke Telegram belum diuji (butuh token bot asli).
Yang sudah diuji: `laporan-mingguan` terhadap Umami 3.4.0 asli (teks < 4.096 karakter = muat satu pesan
Telegram). Jika sebuah opsi ditolak, jalankan `openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik usaha/admin**, bukan pelanggan atau grup.
- **Tidak ada broadcast.** Laporan hanya untuk pemilik; skill ini tidak mengirim apa pun ke pengunjung website.
- Jadwal hanya menjalankan perintah **baca** (`laporan-mingguan`, `ringkasan`, `banding`, `konversi`).
  Skill ini memang tidak punya perintah tulis ke Umami.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** laporan berisi angka agregat (jumlah pengunjung, halaman, kota) — tidak ada data pribadi pengunjung
  (Umami tidak menyimpan IP/nama). Teks tetap tersimpan di riwayat chat Telegram pemilik; beri tahu pemilik.

## Syarat
- Gateway OpenClaw berjalan di komputer yang bisa menjangkau Umami: **komputer/VPS yang sama** dengan Umami
  (alamat `http://localhost:3000`), atau komputer mana pun bila Umami ada di server ber-HTTPS milik pengguna
  (mis. `https://analitik.tokosaya.id`), dan **menyala saat jadwal** (laptop/mini PC yang selalu menyala atau VPS
  milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui.
- Kunci API akun **view-only** (panduan §7) sudah disimpan dengan `simpan-kunci` di komputer Gateway — **jangan**
  pakai kunci akun admin untuk jadwal otomatis.
- Zona waktu jadwal (`--tz` di `openclaw automations add`) sebaiknya sama dengan `--tz` skill (bawaan WIB =
  `Asia/Jakarta`; WITA `Asia/Makassar`, WIT `Asia/Jayapura`).

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks script dikirim apa adanya. Tidak memakai kuota model; angka selalu sama dengan layar Umami.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/umami-analitik/scripts/umami.py'))"
   ```
2. Laporan mingguan tiap **Senin 07.00 WIB** (minggu lalu Senin–Minggu vs minggu sebelumnya):
   ```bash
   openclaw automations add --name "Umami - laporan web mingguan" --cron "0 7 * * 1" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/umami-analitik/scripts/umami.py","laporan-mingguan","--situs","tokosaya.id"]' \
     --command-env '{"UMAMI_URL":"http://localhost:3000"}' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
3. (Opsional) Ringkasan kemarin tiap pagi 07.30 WIB saat kampanye berjalan:
   ```bash
   openclaw automations add --name "Umami - ringkasan kemarin" --cron "30 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/umami-analitik/scripts/umami.py","ringkasan","--periode","kemarin","--situs","tokosaya.id"]' \
     --command-env '{"UMAMI_URL":"http://localhost:3000"}' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Kunci **tidak** ditulis ke dalam `--command-argv` maupun `--command-env` (jangan pernah menambahkan
  `--kunci-file`, `UMAMI_API_KEY`, `UMAMI_PASSWORD`, atau kunci ke jadwal). Script membaca kunci dari file default
  (`~/.komunitech/umami-kunci.txt`). `--command-env` **hanya** untuk `UMAMI_URL` (alamat), agar kunci tidak pernah
  tersimpan di konfigurasi jadwal.
- Umami di server ber-HTTPS milik pengguna → ganti nilai `UMAMI_URL`, mis. `{"UMAMI_URL":"https://analitik.tokosaya.id"}`.
- Hanya satu website di Umami → `--situs` boleh dihapus.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Umami - laporan web (agent)" --cron "0 7 * * 1" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill umami-analitik: jalankan laporan-mingguan untuk website tokosaya.id (hanya baca). Kirim teksnya apa adanya ke saya, lalu tambahkan maksimal 3 saran singkat berdasarkan angka itu. Jangan ubah angka." \
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
- `summary` berisi "Tidak bisa menghubungi" → Umami mati saat jadwal berjalan, atau `UMAMI_URL` di jadwal beda
  dengan yang dipakai saat chat biasa — samakan lewat `--command-env`.
- `summary` berisi "401" → kunci API dihapus/diganti, atau sandi akun diganti (bila memakai sandi). Buat kunci
  baru, `simpan-kunci --ya` di komputer yang sama dengan Gateway.
- `summary` berisi "Ada 2 website" → tambahkan `--situs <domain>` di `--command-argv`.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "laporan web minggu lalu" tiap Senin, atau pasang alarm HP.
