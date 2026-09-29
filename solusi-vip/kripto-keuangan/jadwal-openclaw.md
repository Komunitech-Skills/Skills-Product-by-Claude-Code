# Jadwal OpenClaw siap salin — Riset Kripto & Keuangan Pribadi

Semua perintah **disalin dari** `skills/pantau-pasar-kripto/references/openclaw-jadwal.md`
(pola `--command-argv` + `--command-cwd` + wrapper `NO_REPLY` dan ringkasan pagi bentuk agent).
Tidak ada sintaks baru. Pola dasarnya sama dengan paket lain di `solusi-vip/`.

Legenda (tanda teknis untuk orang teknis; pemilik cukup tahu ✅ = terbukti jalan, S/⚠️ = uji dulu): ✅/T = dijalankan sungguhan di Gateway uji Linux (OpenClaw 2026.9.5) oleh tim
kurasi. 📖/S = sintaks konsisten dengan pola ✅ tetapi kombinasi persisnya belum diuji ulang.
⚠️ = belum diverifikasi. **Pesan benar-benar tiba di Telegram belum pernah diuji** (butuh bot
token asli) — uji dulu dengan `openclaw automations run <id> --wait`.

**Semua ambang dan daftar koin berasal dari member sendiri. Jadwal ini hanya memberi tahu,
tidak pernah memberi saran beli/jual dan tidak pernah mengeksekusi order.** Setiap pesan memuat
disclaimer: *"Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda."*

## 0. Aturan kanal
- **Telegram (bot resmi) = default.** `--to` = ID chat pribadi member. Tidak ke grup, tidak ke
  orang lain, tidak ada broadcast.
- **WhatsApp** hanya bila: nomor **terpisah**, hanya ke diri sendiri, dan member menyetujui
  tertulis: *"OpenClaw memakai WhatsApp Web (tidak resmi, lewat scan QR). Syarat Layanan
  WhatsApp melarang pesan otomatis/massal, jadi nomor bisa diblokir. Untuk pesan ke diri sendiri
  risikonya rendah, tapi tetap ada. Telegram tidak punya risiko ini. Saya mengerti risikonya."*
  Lalu ganti baris terakhir menjadi `--announce --channel whatsapp --to "+62<nomor member>"`.
  Pengiriman nyata ke WA ⚠️ belum diuji.
- Tunjukkan perintah + "Lanjut? (ya/tidak)" sebelum membuat jadwal.

## 1. [VIP] Notifikasi ambang harga, tiap jam (T di Linux, S di Windows)
Wrapper `cek_dan_lapor.py` mencetak pesan hanya bila ambang **member** terlewati atau
pemantauan bermasalah; selain itu mencetak `NO_REPLY` sehingga tidak ada pesan terkirim.
Cari path lengkap (ganti `NAMA`):
```bash
python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/pantau-pasar-kripto/scripts/cek_dan_lapor.py'))"
```
```bash
openclaw automations add --cron "0 * * * *" --tz "Asia/Jakarta" \
  --name "Cek ambang kripto (per jam)" --session isolated \
  --command-argv '["python3", "/home/NAMA/.openclaw/skills/pantau-pasar-kripto/scripts/cek_dan_lapor.py", "--konfigurasi", "kripto/konfigurasi.json", "--state", "kripto/state.json"]' \
  --command-cwd "/home/NAMA/.openclaw/workspace" \
  --announce --channel telegram --to "<ID chat Telegram member>"
```
- Pakai `--command-argv` (bukan `--command`): tanpa shell perantara, sehingga keluaran tenang
  persis `NO_REPLY`.
- `--command-cwd` = folder workspace yang berisi folder `kripto/`.
- Windows: ganti `"python3"` dengan `"py"` atau `"python"`; belum diuji di Windows, uji dulu.
- **Cara uji yang benar:** (1) uji skrip di terminal dengan data tenang lalu data ambang
  terlewati (lihat `SKILL.md` skill); (2) `openclaw automations run <id> --wait` sekali dalam
  kondisi tenang: keluaran harus persis `NO_REPLY`, tanpa upaya pengiriman.
- Varian trigger JavaScript (job tidak berjalan sama sekali saat tenang) ada di
  `skills/pantau-pasar-kripto/references/openclaw-jadwal.md` §2 — kombinasi lengkapnya S; pakai
  hanya bila pola di atas tidak cukup.

## 2. [VIP] Ringkasan pagi: harga + berita bertautan sumber, 07.00 WIB (S)
Job agent yang selalu mengirim. Sintaks konsisten dengan pola `laporan-otomatis-terjadwal`
(✅); isi prompt ini butuh model AI sungguhan sehingga belum diuji ulang.
```bash
openclaw automations add "0 7 * * *" \
  "Jalankan 'python3 /home/NAMA/.openclaw/skills/pantau-pasar-kripto/scripts/cek_ambang.py --konfigurasi kripto/konfigurasi.json --state kripto/state.json' untuk data harga. Cari berita terbaru untuk kata kunci di kripto/PANTAU.md kalau ada akses pencarian web (sertakan tautan sumber tiap judul); kalau tidak ada akses, katakan jujur tidak bisa mencari berita. Susun ringkasan sesuai format Langkah B di SKILL.md skill pantau-pasar-kripto, sertakan disclaimer. JANGAN memberi rekomendasi beli/jual/tahan." \
  --tz "Asia/Jakarta" --name "Ringkasan pagi kripto" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram member>"
```
Bentuk ini "Bentuk A": jadwal & pesan sebagai argumen posisi, **tanpa** `--cron`. Jangan
dicampur dengan `--cron`/`--at`/`--every` dalam satu perintah.

## 3. Keuangan pribadi
`atur-keuangan-pribadi`, `notebook-riset-lokal`, dan `asisten-tulis-riset` sengaja **tanpa
jadwal otomatis**: perhitungannya membutuhkan angka yang member konfirmasi setiap kali, dan
riset dipicu oleh keingintahuan member. Bila member ingin pengingat rutin (mis. "tiap tanggal 25
ingatkan saya mengisi anggaran bulan depan"), gunakan pengingat sekali jalan:
```bash
openclaw automations add --name "Isi anggaran bulan depan" --at "2026-10-25T19:00" --tz "Asia/Jakarta" \
  --message "Ingatkan pemilik: hari ini waktunya menyusun anggaran bulan depan. Tawarkan memakai skill atur-keuangan-pribadi. Jangan mengarang angka." \
  --session isolated --tools exec,read --announce --channel telegram --to "<ID chat Telegram member>" --delete-after-run
```
(Pola `--at` + `--delete-after-run` ✅ dari `solusi-vip/konsultan/jadwal-openclaw.md` §4.)

## 4. Mengelola jadwal ✅
```bash
openclaw automations list --all
openclaw automations show "<nama persis>"           # boleh nama ATAU id
openclaw automations edit <id> --to "<ID chat baru>"
openclaw automations disable <id>                   # hanya id
openclaw automations enable <id>                    # hanya id
openclaw automations run <id> --wait                # uji dulu sebelum percaya "aktif"
openclaw automations runs --id <id>
openclaw automations rm <id>                        # hanya id, permanen
```
`disable`/`enable`/`edit`/`run`/`rm` dengan **nama** ditolak ("Automation not found") — pakai
`id` (UUID) dari hasil `add`.

## 5. Yang belum diverifikasi ⚠️
- Pesan benar-benar tiba di Telegram/WhatsApp (uji internal tanpa token/nomor asli).
- Ringkasan pagi bentuk agent dengan model AI dan pencarian web sungguhan.
- Gateway Windows untuk `--command-argv`.
- Membuat jadwal langsung dari chat ("aktifkan notifikasi tiap jam"); bila gagal, jalankan
  perintah dari terminal/Control UI.

## 6. Syarat mesin menyala
Jadwal berjalan **di dalam proses Gateway**. Mesin mati/tidur → notifikasi **tidak terkirim**,
tanpa pesan error, padahal pasar kripto buka 24 jam. Opsi (tanpa harga): laptop/PC yang
menyala di jam yang diinginkan, mini PC/VPS 24 jam milik member, atau **jasa setup berbayar
Komunitech**.
