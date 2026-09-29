# Ringkasan bulanan arsip nota ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah disalin dari pola `openclaw automations add` yang sudah
dijalankan sungguhan di Gateway lokal OpenClaw **2026.9.5-2026.9.6** untuk skill lain (`kasir-lokal`, `crm-wa`,
`buku-stok`). Khusus arsip-nota, jadwal ini **belum** diuji di Gateway sungguhan; ikuti `docs/uji-platform.md`
sebelum mengklaim "teruji" di `catalog.csv`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**, bukan karyawan/pelanggan/grup.
- **WhatsApp** hanya dengan nomor terpisah milik pemilik, hanya ke pemilik sendiri, dan persetujuan risiko
  tertulis (lihat CLAUDE.md §1). Untuk ringkasan arsip yang tidak sensitif, Telegram tetap disarankan.
- Jadwal **hanya menjalankan perintah baca**: `rekap`, `info`, `duplikat`. Tidak pernah `--ya`, `tambah`, `restore`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" ke pengguna sebelum membuat jadwal.
- **Privasi:** ringkasan berisi nama vendor dan nominal pengeluaran usaha; tersimpan di riwayat chat Telegram
  pemilik. Beri tahu pemilik.

## Syarat
- Gateway OpenClaw berjalan di komputer yang **sama dengan indeks arsip** dan menyala saat jadwal (laptop/mini PC
  yang selalu menyala, atau VPS milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui.

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Rekap bulan lalu, dikirim tanggal 1 tiap bulan jam 07.30 WIB:
```bash
openclaw automations add --name "Rekap nota bulanan" --cron "30 7 1 * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/arsip-nota/scripts/arsip.py","rekap","--bulan","lalu"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- Cari path lengkap script dulu bila skill dipasang di lokasi lain:
  ```bash
  python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/arsip-nota/scripts/arsip.py'))"
  ```
- Indeks bukan di lokasi default → tambahkan `"--db","/path/arsip.db"` setelah nama perintah di dalam argv.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji), atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Rekap nota (agent)" --cron "30 7 1 * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill arsip-nota: jalankan rekap --bulan lalu (hanya baca; JANGAN menjalankan perintah tulis "
            "atau --ya). Kirim teksnya apa adanya ke saya." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id>` |
| Lihat hasil | `openclaw automations runs <id>` |
| Hentikan / aktifkan | `openclaw automations disable <id>` / `enable <id>` |
| Hapus | `openclaw automations rm <id>` |

## Jika bermasalah
- Ringkasan bilang "Indeks arsip belum ada" → path `--db` di jadwal berbeda dari yang dipakai saat chat; samakan.
- "sedang dipakai program lain" → indeks sedang ditulis; data aman, jalankan `automations run <id>` lagi.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "rekap nota bulan lalu" tiap awal bulan, atau pasang pengingat
  kalender sendiri.
