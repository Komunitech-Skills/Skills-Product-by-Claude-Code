# Pengingat pajak bulanan ke Telegram pemilik (OpenClaw)

**Status verifikasi (25 September 2026):** ⚠️ **Jadwal di bawah BELUM diuji** untuk skill ini di OpenClaw sungguhan. Sintaks `openclaw automations add ... --command-argv ... --announce --channel telegram` meniru pola yang **sudah diuji** di skill `laporan-harian-usaha` (`references/openclaw-jadwal.md`, OpenClaw 2026.9.5). Script-nya sendiri sudah diuji dari terminal (`--hari-ini hari-ini` membaca tanggal komputer saat jadwal berjalan). Pengiriman nyata ke Telegram belum diuji.

## 0. Aturan kanal (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` = ID chat **pemilik** (atau admin keuangan yang pemilik tunjuk secara eksplisit, lewat jadwal terpisah ke chat pribadinya). Tidak ke grup.
- **WhatsApp** hanya dengan **nomor terpisah** milik pemilik, pesan hanya ke diri sendiri, dan pemilik menjawab "ya, saya mengerti risikonya" setelah membaca: *"OpenClaw memakai WhatsApp Web (tidak resmi, scan QR). Pesan otomatis bisa membuat nomor diblokir. Untuk pengingat ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya risiko ini."*
- **Tidak ada broadcast**, tidak ke pelanggan/karyawan.
- Tunjukkan perintah + "Lanjut? (ya/tidak)" sebelum membuat jadwal apa pun.

## 1. Siapkan (sekali)
1. Gateway OpenClaw berjalan di komputer yang **menyala pada jam jadwal** (komputer kantor yang tidak dimatikan, mini PC, atau VPS milik pemilik). Jika mati, pengingat **tidak terkirim** tanpa pesan error. Opsi: komputer selalu menyala, VPS sendiri, atau jasa setup Komunitech.
2. Pasang skill: `openclaw skills install ./kalender-pajak --global`.
3. Telegram: buat bot di @BotFather → `openclaw channels add --channel telegram --token <token>` → kirim "halo" ke bot dari akun pemilik → `openclaw pairing list telegram` lalu `openclaw pairing approve telegram <KODE>`.
4. Cari path lengkap script (argv tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/kalender-pajak/scripts/kalender_pajak.py'))"
   ```
5. Uji dulu dari terminal dengan profil Anda:
   `python3 <path kalender_pajak.py> --profil badan-pkp,pemberi-kerja --hari-ini hari-ini --rentang 10`
6. Pastikan **jam & zona waktu komputer Gateway benar** (WIB/WITA/WIT): script memakai tanggal komputer.

## 2. Jadwal yang disarankan (perintah langsung, tanpa AI)
Tanpa kuota model, hasil selalu sama, tanggal tidak bisa "dikarang" AI. Ganti `--profil` sesuai hasil skill, dan `/home/NAMA/...` dengan path dari langkah 1.4.

**a. Ringkasan awal bulan — tanggal 1, 07.00:** semua tenggat 31 hari ke depan.
```bash
openclaw automations add --name "Pajak: ringkasan bulan ini" --cron "0 7 1 * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/kalender-pajak/scripts/kalender_pajak.py","--profil","badan-pkp,pemberi-kerja","--hari-ini","hari-ini","--rentang","31"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
**b. Pengingat tgl 15/20 — tanggal 10, 07.00:** tenggat 16 hari ke depan (menangkap tgl 15, 20, dan pergeserannya — termasuk libur panjang Lebaran seperti 20→25 Maret 2026).
```bash
openclaw automations add --name "Pajak: pengingat tgl 15 & 20" --cron "0 7 10 * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/kalender-pajak/scripts/kalender_pajak.py","--profil","badan-pkp,pemberi-kerja","--hari-ini","hari-ini","--rentang","16"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
**c. Pengingat akhir bulan (PPN) — tanggal 24, 07.00:** hanya bila profil memuat `ppn`/`badan-pkp`/`pkp`. (Batas unggah faktur pajak keluaran tgl 20 sudah tertangkap jadwal (b) bila profil memuat PPN; tgl 20 itu **tidak** bergeser walau libur.)
```bash
openclaw automations add --name "Pajak: pengingat PPN akhir bulan" --cron "0 7 24 * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/kalender-pajak/scripts/kalender_pajak.py","--profil","ppn","--hari-ini","hari-ini","--rentang","10"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- Mengapa tanggal 10 dan 24: pergeseran hanya **memundurkan** tenggat, jadi pengingat 5 hari sebelum tanggal normal selalu datang sebelum tenggat akhir.
- UMKM 0,5% tanpa karyawan cukup jadwal (a) dan (b) dengan `--profil op-umkm`.
- WITA/WIT: ganti `--tz Asia/Makassar` / `Asia/Jayapura` dan atur zona waktu komputer yang sama.
- **Awal tahun:** tambahkan file libur tahun baru (`references/libur-nasional-<tahun>.csv`) setelah SKB terbit. Tanpa itu pesan memuat PERINGATAN "data libur belum ada".

## 3. Pilihan lewat agent AI (Windows, atau ingin pesan lebih ramah)
Memakai kuota model; batasi alat.
```bash
openclaw automations add --name "Pajak: pengingat (agent)" --cron "0 7 10 * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill kalender-pajak: jalankan scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja --hari-ini hari-ini --rentang 16, lalu kirim tabelnya apa adanya plus maksimal 2 kalimat pengingat. Jangan ubah tanggal. Jangan hitung besaran pajak. Jangan kirim ke siapa pun selain pemilik." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## 4. WhatsApp nomor terpisah (hanya jika syarat §0 terpenuhi)
Ganti baris terakhir menjadi `--announce --channel whatsapp --to "+62<nomor pemilik>"`. Pengiriman nyata ke WA ⚠️ belum diuji.

## 5. Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id> --wait` (cek `status`, `summary`, `deliveryStatus`) |
| Jeda / aktifkan | `openclaw automations disable <id>` / `openclaw automations enable <id>` |
| Hapus | `openclaw automations rm <id>` |

## 6. Jika bermasalah
- `Gateway not reachable` → komputer/Gateway mati.
- `deliveryStatus: not-delivered` + `Telegram bot token missing` → kanal Telegram belum disiapkan (§1 langkah 3).
- `summary` berisi `ERROR: profil ... tidak dikenal` → periksa ejaan `--profil` (lihat `--daftar-profil`).
- Tanggal di pesan meleset sehari → zona waktu komputer Gateway salah.

## Alternatif tanpa OpenClaw
Buat file kalender sekali setahun: `python3 scripts/kalender_pajak.py --profil <profil> --tahun 2027 --format ics --keluar pajak-2027.ics`, lalu impor ke Google Calendar/Outlook/Kalender HP. File memuat pengingat H-3 & H-1 pukul 09.00 yang biasanya dipakai Apple Calendar/Outlook; **Google Calendar sering mengabaikannya** — atur notifikasi default kalender, atau tambah `--acara-pengingat` agar dibuat acara "Pengingat H-3/H-1" terpisah. Impor ulang ke Google bisa membuat duplikat (impor ke kalender khusus "Pajak" agar mudah dihapus).
