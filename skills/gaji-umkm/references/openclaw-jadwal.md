# Pengingat gajian & setoran otomatis ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah disalin dari pola `crm-wa` (dijalankan sungguhan pada Gateway
lokal OpenClaw 2026.9.5/2026.9.6 untuk skill `kasir-lokal`, `pengingat-follow-up`, dan `crm-wa`). Khusus gaji-umkm,
jadwal **belum** diuji di Gateway; pengiriman ke Telegram belum diuji (butuh token bot asli). Jika sebuah opsi
ditolak, jalankan `openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**, bukan karyawan atau grup.
- **WhatsApp** hanya bila: nomor **terpisah** milik pemilik, pesan hanya ke pemilik sendiri, dan pemilik membalas
  "ya, saya mengerti risikonya" setelah membaca: *"OpenClaw memakai WhatsApp Web (tidak resmi). Pesan otomatis bisa
  membuat nomor diblokir. Untuk pengingat ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya
  risiko ini."*
- **Tidak ada pesan otomatis ke karyawan** dan tidak ada broadcast slip. Jadwal hanya menjalankan perintah **baca**
  (`pengingat`, `rekap`); tidak pernah `--ya`, `hitung`, `final`, `isi`, `transfer`, `restore`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** teks `pengingat` hanya berisi tanggal dan **total** perusahaan (gaji bersih, BPJS, PPh 21), tanpa nama
  atau NIK/rekening karyawan. `rekap --bulan` berisi nama & gaji tiap karyawan dan akan tersimpan di riwayat chat
  Telegram pemilik — beri tahu pemilik sebelum menjadwalkannya; sarankan cukup `pengingat`.

## Syarat
- Gateway OpenClaw berjalan di komputer yang **sama dengan database gaji** dan **menyala saat jadwal** (laptop/mini PC
  yang selalu menyala atau VPS milik pemilik; Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui (lihat skill `laporan-otomatis-terjadwal`).
- Jam komputer benar. Zona waktu jadwal (`--tz`) sesuai lokasi usaha.

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI
Teks script dikirim apa adanya. Tidak memakai kuota model; hasil selalu sama.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/gaji-umkm/scripts/gaji.py'))"
   ```
2. Pengingat harian 07.00 WIB (tenggat 3 hari ke depan: tanggal gajian, BPJS Kesehatan tgl 10, BPJS TK & setor PPh 21
   tgl 15, lapor SPT Masa PPh 21 tgl 20):
   ```bash
   openclaw automations add --name "Pengingat gaji & setoran" --cron "0 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/gaji-umkm/scripts/gaji.py","pengingat","--rentang","3"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   Hari tanpa tenggat tetap mengirim satu baris "Tidak ada tenggat ...". Bila terlalu sering, ganti cron menjadi
   beberapa tanggal saja, mis. `"0 7 7,12,17,22 * *"` dan `--rentang 5` (tambahkan tanggal H-3 gajian Anda).
3. Rekap setahun tiap tanggal 1 pukul 07.30 (hanya total per bulan, tanpa nama karyawan):
   ```bash
   openclaw automations add --name "Rekap gaji tahunan" --cron "30 7 1 * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/gaji-umkm/scripts/gaji.py","rekap","--tahun","2026"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   Ganti tahunnya setiap Januari.
- Database bukan di lokasi default → tambahkan `"--db","/path/gaji.db"` setelah nama perintah di dalam argv.
- WITA: `--tz Asia/Makassar`; WIT: `--tz Asia/Jayapura`.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model. `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Pengingat gaji (agent)" --cron "0 7 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill gaji-umkm: jalankan pengingat --rentang 3 (hanya baca; JANGAN menjalankan hitung, final, isi, transfer, --ya, atau mengirim apa pun ke karyawan). Kirim teksnya apa adanya ke saya. Jangan ubah angka dan tanggal." \
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
- `summary` berisi "Database gaji belum ada" → path `--db` di jadwal berbeda dengan yang dipakai saat chat; samakan.
- "sedang dipakai program lain" → saat jadwal berjalan ada perubahan yang sedang disimpan; data aman, jalankan
  `automations run <id>` lagi.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "pengingat gaji minggu ini" ke agent, atau pasang alarm HP sendiri
  untuk tanggal gajian, tgl 10, 15, dan 20.
