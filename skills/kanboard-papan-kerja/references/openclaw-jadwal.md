# Laporan papan harian ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah mengikuti pola `openclaw automations add` yang sudah dijalankan sungguhan di Gateway lokal OpenClaw 2026.9.x untuk skill lain di repo Komunitech. Untuk `kanboard-papan-kerja`, jadwal **belum** diuji di Gateway sungguhan dan pengiriman ke Telegram belum diuji (butuh token bot asli). Jika sebuah opsi ditolak, jalankan `openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik/admin**, bukan pelanggan atau grup pelanggan.
- **Tidak ada broadcast** dan tidak ada pesan otomatis ke pelanggan.
- Jadwal hanya menjalankan perintah **baca** (`laporan`, atau `terlambat`/`macet`); tidak pernah `--ya`, `buat-papan`, `tambah-kartu`, `pindah-kartu`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** laporan berisi judul kartu (sering berisi nama pelanggan/nomor invoice) dan nama anggota tim; akan tersimpan di riwayat chat Telegram pemilik. Sampaikan ini sebelum membuat jadwal; sarankan judul kartu memakai nama panggilan/nomor order, bukan data pribadi lengkap.

## Syarat
- Gateway OpenClaw berjalan di komputer yang bisa menjangkau Kanboard (idealnya **komputer yang sama**, karena Kanboard diikat ke `127.0.0.1` — `docs/panduan-kanboard.md` §4) dan **menyala saat jadwal**.
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui.
- Kunci sudah disimpan dengan `simpan-kunci` di komputer itu. Sebaiknya pakai akun Kanboard khusus laporan yang hanya jadi anggota papan yang perlu dilaporkan; **jangan** pakai token aplikasi `jsonrpc` untuk jadwal.

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks script dikirim apa adanya; tidak memakai kuota model.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/kanboard-papan-kerja/scripts/kanboard.py'))"
   ```
2. Laporan tiap hari 07.00 WIB:
   ```bash
   openclaw automations add --name "Kanboard - laporan pagi" --cron "0 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/kanboard-papan-kerja/scripts/kanboard.py","laporan"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   Satu papan saja: tambahkan `"--papan","Konveksi"` ke argv. Ambang macet lain: `"--hari","5"`.
- Token/URL **tidak** ditulis ke `--command-argv`. Alamat bukan bawaan → `--command-env '{"KANBOARD_URL":"http://127.0.0.1:8081"}'` (hanya URL, **bukan** token).
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
```bash
openclaw automations add --name "Kanboard - laporan pagi (agent)" --cron "0 7 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill kanboard-papan-kerja: jalankan laporan (hanya baca; JANGAN menjalankan buat-papan/tambah-kartu/pindah-kartu/--ya). Kirim teksnya apa adanya ke saya." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id>` |
| Lihat hasil | `openclaw automations runs <id>` |
| Hentikan / aktifkan | `openclaw automations disable <id>` / `enable <id>` |
| Hapus jadwal | `openclaw automations rm <id>` (hanya jadwalnya, bukan data Kanboard) |

## Jika bermasalah
- Hasil berisi "tidak bisa dihubungi" → Kanboard/Docker mati saat jadwal, atau alamat beda → samakan lewat `--command-env`.
- Hasil berisi "401" → token dihapus/diganti; buat token baru dan `simpan-kunci --ya` di komputer yang sama dengan Gateway.
- Tidak terkirim → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "laporan papan" tiap pagi.
