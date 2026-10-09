# Laporan gudang harian ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah mengikuti pola yang sudah dijalankan
sungguhan di Gateway lokal OpenClaw **2026.9.5/2026.9.6** untuk skill lain di repo ini (`dolibarr-usaha`,
`kasir-lokal`, `pengingat-follow-up`: job diterima, jadwal & zona waktu tersimpan, `automations run`
menjalankan script), dan disalin dari `vikunja-tugas`. Untuk `inventree-gudang` sendiri, jadwal **belum**
diuji di Gateway sungguhan (hanya `scripts/uji_openclaw.sh`, uji muat/eligibility, bukan uji pengiriman);
pengiriman ke Telegram belum diuji (butuh token bot asli). Jika sebuah opsi ditolak, jalankan
`openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik/admin gudang**, bukan pelanggan, pemasok, atau grup.
- **Tidak ada broadcast** dan tidak ada pesan otomatis ke pemasok/pelanggan (mis. "PO otomatis ke supplier" → tolak; buat draf, manusia yang mengirim).
- Jadwal hanya menjalankan perintah **baca** (`laporan-harian`, `stok-menipis`, `po-terbuka`, `produksi-ringkas`); tidak pernah `opname`, `terima-barang`, atau `--ya`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** teks laporan berisi nama barang, jumlah stok, nama pemasok, dan nomor PO, dan akan tersimpan di riwayat chat Telegram pemilik. Beri tahu pemilik sebelum membuat jadwal.

## Syarat
- Gateway OpenClaw berjalan di komputer/jaringan yang bisa menjangkau InvenTree (idealnya **komputer yang sama**, karena InvenTree dibatasi ke `127.0.0.1`/`localhost` — lihat `docs/panduan-inventree.md` §4) dan **menyala saat jadwal** (laptop/mini PC yang selalu menyala atau VPS milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui.
- Token API akun **baca-saja** (grup "Agen Baca", panduan §6) sudah disimpan dengan `simpan-kunci` — **jangan** pakai token akun yang bisa menulis untuk jadwal otomatis.
- Zona waktu jadwal (`--tz` di `openclaw automations add` dan `--tz` di `inventree.py`) sebaiknya sama, mis. `Asia/Jakarta` untuk WIB.

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks script dikirim apa adanya. Tidak memakai kuota model; hasil selalu sama.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/inventree-gudang/scripts/inventree.py'))"
   ```
2. Laporan gudang harian 07.00 WIB (stok menipis + PO terbuka + produksi terbuka dalam satu pesan):
   ```bash
   openclaw automations add --name "InvenTree - laporan gudang" --cron "0 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/inventree-gudang/scripts/inventree.py","laporan-harian"]' \
     --command-env '{"INVENTREE_API_HOST":"http://localhost"}' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
3. (Opsional) Stok menipis saja, sore hari 16.00 WIB sebelum belanja besok:
   ```bash
   openclaw automations add --name "InvenTree - stok menipis" --cron "0 16 * * 1-6" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/inventree-gudang/scripts/inventree.py","stok-menipis"]' \
     --command-env '{"INVENTREE_API_HOST":"http://localhost"}' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Token **tidak** ditulis ke dalam `--command-argv` maupun `--command-env` (jangan pernah menambahkan `--kunci-file`, `INVENTREE_API_TOKEN`, atau token ke jadwal). Script membaca token dari file default (`~/.komunitech/inventree-kunci.txt`). `--command-env` **hanya** untuk `INVENTREE_API_HOST` (alamat), agar token tidak pernah tersimpan di konfigurasi jadwal.
- Alamat InvenTree bukan `http://localhost` (mis. instalasi manual di `http://127.0.0.1:8000`) → ganti nilai `INVENTREE_API_HOST` di `--command-env`.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "InvenTree - laporan gudang (agent)" --cron "0 7 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill inventree-gudang: jalankan laporan-harian (hanya baca; JANGAN menjalankan opname/terima-barang/--ya). Kirim teksnya apa adanya ke saya. Jangan ubah angka." \
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
- `summary` berisi "tidak bisa dihubungi" → InvenTree mati saat jadwal berjalan, atau `INVENTREE_API_HOST` di jadwal beda dengan yang dipakai saat chat biasa — samakan lewat `--command-env`.
- `summary` berisi "401" → token akun baca-saja kedaluwarsa/dicabut (token InvenTree punya tanggal kedaluwarsa, default 1 tahun); buat token baru, `simpan-kunci --ya` di komputer yang sama dengan Gateway.
- `summary` berisi "403" → grup akun baca-saja kurang hak lihat (panduan §6).
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "laporan gudang hari ini" tiap pagi, atau pasang alarm HP sendiri.
