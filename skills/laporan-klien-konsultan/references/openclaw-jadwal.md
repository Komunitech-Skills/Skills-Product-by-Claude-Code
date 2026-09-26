# Jadwal OpenClaw siap salin — Draf laporan klien tiap Jumat sore

Sumber pola: `skills/pengingat-follow-up/references/openclaw-jadwal.md` — dokumen paling lengkap
verifikasinya di seluruh library (diuji sungguhan di OpenClaw **2026.9.5 (ec9c1a1)** dan **2026.9.6
(eb377ac)** terhadap Gateway lokal `gateway run --dev --allow-unconfigured --bind loopback`).
Salinan pola yang sama juga sudah dipakai di `skills/crm-wa/references/openclaw-jadwal.md` dan
`solusi-vip/konsultan/jadwal-openclaw.md`. Flag di bawah **tidak diarang baru** — semuanya persis
flag yang sudah terbukti diterima `openclaw automations add`.

Legenda: ✅ = pola **dijalankan sungguhan** untuk skill lain (job terbentuk & terverifikasi dari
JSON hasilnya). ⚠️ = kombinasi khusus dengan `laporan_klien.py` **belum diuji** di Gateway oleh tim
kurasi (Tahap 6 CLAUDE.md tetap wajib sebelum status `lulus`).

**Jadwal ini hanya mengirim draf ke Telegram/WhatsApp PEMILIK/KONSULTAN sendiri — tidak pernah
langsung ke klien.** Draf yang diterima wajib ditinjau lalu disalin manual ke email/WA klien.

## 0. Aturan kanal (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **konsultan sendiri**, bukan klien.
- **WhatsApp** hanya bila: nomor **terpisah** dari nomor usaha/pribadi utama, draf hanya dikirim ke
  konsultan sendiri, dan konsultan sudah membalas "ya, saya mengerti risikonya" setelah membaca:
  *"OpenClaw memakai WhatsApp Web (tidak resmi, lewat scan QR), bukan WhatsApp Business API resmi.
  Syarat Layanan WhatsApp melarang pesan otomatis/massal, jadi nomor bisa diblokir. Untuk draf ke
  diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya risiko ini."*
- **Tidak ada** broadcast, tidak ada kirim ke grup, dan **tidak ada** pengiriman langsung ke klien
  lewat jadwal ini. Konsultan selalu meninjau draf dulu sebelum menyalinnya ke saluran klien.

## 1. Draf laporan mingguan, Jumat 16.00 WIB (satu klien) ✅ pola / ⚠️ kombinasi skill ini
```bash
openclaw automations add "0 16 * * 5" \
  "Pakai skill laporan-klien-konsultan. Jalankan: python3 <folder-skill>/scripts/laporan_klien.py --file <folder-kerja>/laporan/log-kerja-klien.csv laporan --klien \"<Nama Klien>\" --periode mingguan --json. Tampilkan field teks_email dan teks_wa apa adanya dalam Bahasa Indonesia -- JANGAN mengubah angka atau jam. Ini DRAF untuk saya tinjau, JANGAN mengirim apa pun ke klien." \
  --name "Draf laporan mingguan - <Nama Klien>" --tz "Asia/Jakarta" --session isolated \
  --tools exec,read --announce --channel telegram --to "<ID chat Telegram konsultan>"
```
- `--tools exec,read` ✅ (terbukti untuk skill lain) — jadwal ini hanya boleh menjalankan script &
  membaca file, tidak bisa mengirim pesan/browser/tulis file sendiri.
- Bentuk ini ("Bentuk A": jadwal & pesan sebagai argumen posisi, **tanpa** `--cron`) — jangan
  dicampur dengan `--cron`/`--at`/`--every` di perintah yang sama.
- Satu klien = satu jadwal. Untuk beberapa klien, ulangi perintah ini dengan `--name` dan
  `--klien` berbeda per klien (mis. jam berbeda-beda agar tidak menumpuk, contoh: 16.00, 16.10,
  16.20).

## 2. Alternatif hemat token: tanpa AI, langsung teks script ✅ pola / ⚠️ kombinasi skill ini
```bash
openclaw automations add --name "Draf laporan mingguan (tanpa AI) - <Nama Klien>" \
  --cron "0 16 * * 5" --tz "Asia/Jakarta" \
  --command-argv '["python3","/path/lengkap/laporan-klien-konsultan/scripts/laporan_klien.py","--file","/path/lengkap/laporan/log-kerja-klien.csv","laporan","--klien","<Nama Klien>","--periode","mingguan"]' \
  --announce --channel telegram --to "<ID chat Telegram konsultan>"
```
Cocok untuk nol biaya token model — keluaran default (tanpa `--json`) sudah berisi ketiga versi
(email/WA/markdown) berlabel jelas. `--command-argv` tidak mengenal `~`, cari path lengkap dulu:
```bash
python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/laporan-klien-konsultan/scripts/laporan_klien.py'))"
```
⚠️ Belum diuji di Gateway Windows — di Windows pakai §1 atau ganti `python3` dengan `py`.

## 3. Draf laporan bulanan, tanggal 1 pukul 08.00 WIB
Sama seperti §1/§2, ganti `"0 16 * * 5"`/`--cron "0 16 * * 5"` menjadi `"0 8 1 * *"` dan
`--periode mingguan` menjadi `--periode bulanan`.

## 4. Mengelola jadwal ✅
```bash
openclaw automations list --all
openclaw automations show "<nama persis>"           # show boleh nama ATAU id
openclaw automations edit <id> --cron "0 16 * * 5" --tz "Asia/Jakarta"
openclaw automations disable <id>                   # hanya id
openclaw automations enable <id>                    # hanya id
openclaw automations run <id> --wait                # uji dulu sebelum percaya "aktif"
openclaw automations runs --id <id>
openclaw automations rm <id>                         # hanya id, permanen
```
`disable`/`enable`/`edit`/`run`/`rm` dengan **nama** (bukan id) ditolak: `Automation not found` —
dibuktikan langsung di Gateway uji untuk skill lain.

## 5. WhatsApp nomor terpisah (hanya bila syarat §0 terpenuhi)
Ganti baris terakhir tiap perintah menjadi
`--announce --channel whatsapp --to "+62<nomor konsultan>"`.

## 6. Telegram: menyiapkan bot 📖
Buat bot di @BotFather → `openclaw channels add --channel telegram --token <token>` → kirim
"halo" dari akun konsultan → `openclaw pairing list telegram` → `openclaw pairing approve
telegram <KODE>` (berlaku 1 jam). Cara mencari ID chat: lihat
`skills/laporan-otomatis-terjadwal/references/openclaw.md` §4.

## 7. Yang belum diverifikasi ⚠️
- Kombinasi persis `openclaw automations add` dengan `laporan_klien.py` (§1-§3 di atas) — pola
  cron/flag sudah terbukti untuk skill lain, tapi belum dicoba sungguhan di Gateway untuk skill
  ini. **Wajib** diuji (Tahap 6 CLAUDE.md, `automations run <id> --wait`) sebelum status `lulus`.
- Pengiriman nyata ke Telegram/WhatsApp (uji internal tidak memakai token bot/nomor asli).
- Membuat jadwal ini langsung dari chat ("aktifkan draf laporan tiap Jumat") — kombinasi persis
  belum dicoba tim kami. Kalau gagal/aneh, jalankan perintah dari terminal/Control UI.

## 8. Syarat komputer menyala
Jadwal berjalan **di dalam proses Gateway**. Kalau laptop/mini PC mati/tidur di jam 16.00 Jumat,
draf **tidak terkirim** dan tidak ada pesan error. Tiga opsi (tanpa harga): laptop/mini PC yang
selalu menyala, VPS milik konsultan sendiri, atau jasa setup Komunitech.
