# Jadwal OpenClaw siap salin — Toko Online

Semua perintah di bawah diambil/diturunkan dari `references/openclaw*.md` skill terkait
(`laporan-otomatis-terjadwal`, `buku-stok`, `konten-mingguan`, `agen-cs-toko`), yang sudah
diverifikasi lewat `--help` OpenClaw **2026.9.5/2026.9.6**, dan sebagian **dijalankan sungguhan**
terhadap Gateway lokal uji. Untuk sesi penyusunan paket ini, **flag-flag yang dipakai di bawah
diverifikasi ulang** dengan menjalankan `bash scripts/uji_openclaw.sh 2026.9.6` lalu memeriksa
`openclaw automations add --help` dan `openclaw channels add --help` sungguhan di OpenClaw
**2026.9.6 (eb377ac)** — semua flag (`--cron`/argumen posisi, `--tz`, `--name`, `--session`,
`--announce`, `--channel`, `--to`, `--tools`, `--best-effort-deliver`, `--model`) **cocok
persis** dengan yang tertulis di `--help`. **Tidak ada perintah baru yang ditebak** untuk
dokumen ini.

Legenda: ✅ = benar-benar dijalankan terhadap Gateway nyata (dicatat di skill sumber). 📖 = dicek
lewat `--help`/`config schema` (termasuk verifikasi ulang sesi ini), kombinasi utuhnya belum
dicoba ujung-ke-ujung. ⚠️ = belum diverifikasi sama sekali.

**Sebelum menjalankan apa pun:** tunjukkan ringkasan ke pemilik toko dan tanya "Lanjut?
(ya/tidak)". Ganti `<ID chat Telegram pemilik>` dengan angka nyata dari Langkah 4 `PANDUAN.md`.
Semua jadwal di bawah mengirim **hanya ke pemilik**, tidak pernah ke grup/pelanggan.

## 1. Laporan toko harian, jam 21.00 WIB ✅/📖

Kalau memakai `buku-stok` untuk stok (disarankan — laporannya sudah mencakup omzet, stok
menipis, barang tidak laku, nilai persediaan dalam satu pesan) — bentuk ini **diverifikasi lewat
`--help`** di dokumentasi `buku-stok/SKILL.md` (flag intinya sama dengan yang **dijalankan
sungguhan** ✅ oleh `laporan-otomatis-terjadwal`):
```bash
openclaw automations add --name "Laporan stok & omzet harian" --cron "0 21 * * *" \
  --tz "Asia/Jakarta" --session isolated --tools exec,read \
  --message "Pakai skill buku-stok: jalankan laporan ringkas hari ini (hanya baca, jangan jalankan perintah tulis atau --ya) lalu kirim teksnya apa adanya dalam Bahasa Indonesia." \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

Kalau sumber data Anda adalah **file ekspor penjualan CSV/Excel** (marketplace/kasir) tanpa
`buku-stok`, pakai pola `laporan-otomatis-terjadwal` — **Bentuk A, flag intinya ✅ dijalankan
sungguhan** di Gateway uji:
```bash
openclaw automations add "0 21 * * *" \
  "Jalankan resep laporan/RESEP-penjualan-harian.md untuk hari ini (pakai rekap-penjualan-csv). Tulis dalam Bahasa Indonesia, maksimal 12 baris, sebutkan jika data belum ada — jangan mengarang angka." \
  --tz "Asia/Jakarta" --name "Laporan penjualan harian" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- `--tz "Asia/Jakarta"` wajib eksplisit — tanpa ini cron memakai zona waktu komputer Gateway.
- `--tools exec,read` (dipakai contoh `buku-stok`) membatasi jadwal hanya boleh membaca laporan,
  **tidak boleh** menjalankan transaksi tulis (`--ya`).
- Uji dulu sebelum percaya jadwal aktif: `openclaw automations run <id> --wait` (✅, `<id>`
  didapat dari field `"id"` hasil `add`, **wajib** UUID — memakai nama pada `run` gagal dengan
  pesan `Automation not found`, dibuktikan di Gateway uji).

## 2. Stok menipis terpisah (opsional, kalau tidak digabung ke laporan harian) 📖
```bash
openclaw automations add --name "Laporan stok menipis" --cron "0 8 * * *" --tz "Asia/Jakarta" \
  --session isolated --tools exec,read \
  --message "Pakai skill buku-stok: jalankan laporan menipis (hanya baca) dan kirim daftarnya apa adanya." \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 3. Paket konten mingguan — Jumat jam 16.00 WIB ✅/📖
Flag inti sama dengan §1 (dikonfirmasi via `--help` sesi ini, dan sudah diuji sungguhan lewat
`laporan-otomatis-terjadwal`):
```bash
openclaw automations add "0 16 * * 5" \
  "Jalankan skill konten-mingguan untuk minggu depan memakai profil di konten/PROFIL.md. Tulis paket lengkap dalam Bahasa Indonesia, simpan arsip ke konten/minggu-<label>.md, lalu kirimkan ringkasan per hari." \
  --tz "Asia/Jakarta" --name "Paket konten Jumat sore" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

## 4. Pengingat posting harian, jam 08.00 WIB ✅/📖
```bash
openclaw automations add "0 8 * * *" \
  "Baca konten/minggu-<label minggu berjalan>.md, ambil bagian untuk HARI INI saja, lalu kirim ringkas: platform, hook, dan caption siap tempel hari ini. Kalau arsip minggu ini belum ada, katakan itu apa adanya, jangan mengarang." \
  --tz "Asia/Jakarta" --name "Pengingat posting harian" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
**Ingat:** ini hanya menyiapkan & mengingatkan. OpenClaw **tidak** memposting otomatis ke
Instagram/TikTok/Facebook (tidak ada plugin/kanal resmi untuk itu).

## 5. Rekap harian CS (mode Copilot), jam 20.00 WIB 📖
```bash
openclaw automations add \
  --cron "0 20 * * *" --tz "Asia/Jakarta" \
  --name "Rekap CS harian" \
  --message "Baca isi file cs/log/<tanggal hari ini>.md di workspace. Ringkas: jumlah chat dibalas, 5 kategori pertanyaan terbanyak, daftar yang dieskalasi, dan pertanyaan yang belum ada di cs/PENGETAHUAN.md. Jika file belum ada/kosong, katakan belum ada aktivitas hari ini, jangan mengarang angka. Bahasa Indonesia, maksimal 15 baris." \
  --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Log `cs/log/<tanggal>.md` **tidak boleh** berisi nama/nomor HP/alamat/isi chat lengkap pelanggan —
hanya kategori & ringkasan pertanyaan (lihat aturan di `skills/agen-cs-toko/references/eskalasi-dan-kanal.md` §3a).

## 6. Mengelola jadwal (semua ✅, dibuktikan di Gateway uji)
```bash
openclaw automations list --all                     # semua jadwal + id
openclaw automations show "<nama persis>"           # show boleh pakai nama ATAU id
openclaw automations run <id> --wait                # uji sekarang sebelum percaya "aktif"
openclaw automations disable <id>                   # jeda (hanya id, BUKAN nama)
openclaw automations enable <id>                     # aktifkan lagi (hanya id)
openclaw automations edit <id> --cron "0 22 * * *" --tz "Asia/Jakarta"   # ubah jam (hanya id)
openclaw automations rm <id>                         # hapus permanen (hanya id, tak bisa dibatalkan)
```
`run`/`disable`/`enable`/`edit`/`rm` **wajib** pakai `id` (UUID dari hasil `add`) — memakai nama
di perintah-perintah ini ditolak dengan `Automation not found: <nama>`.

## 7. Follow-up CRM harian (crm-wa) — opsional, 08.00 WIB 📖
Kalau Anda memakai `crm-wa` untuk mencatat calon pembeli (`PANDUAN.md` §5g), jadwal ini mengirim
daftar follow-up hari ini ke Telegram pemilik setiap pagi. Pola perintah (`--command-argv`,
`--cron`, `--tz`, `--announce --channel telegram`) sama dengan yang **dijalankan sungguhan** ✅
untuk `kasir-lokal`/`pengingat-follow-up`; kombinasi khusus dengan `crm.py` **belum diuji** di
Gateway oleh tim kurasi (lihat `skills/crm-wa/references/openclaw-jadwal.md`).

1. Cari path lengkap script (ganti `NAMA` dengan nama pengguna komputer Anda; argv tidak mengenal
   `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/crm-wa/scripts/crm.py'))"
   ```
2. Buat jadwal (tanpa memakai kuota model, hasil selalu sama):
   ```bash
   openclaw automations add --name "Follow-up CRM harian" --cron "0 8 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/crm-wa/scripts/crm.py","hari-ini"]' \
     --announce --channel telegram --to "<ID chat Telegram pemilik>"
   ```
   Versi disamarkan (nama jadi inisial, tanpa catatan obrolan/nilai rupiah) — tambahkan
   `"--samarkan"` setelah `"hari-ini"` di dalam argv.
3. Uji dulu sebelum percaya jadwal aktif: `openclaw automations run <id> --wait`.

**Privasi:** teks `hari-ini` memuat nama, nomor WA, tautan wa.me, catatan obrolan terakhir, dan
nilai rupiah calon pembeli — akan tersimpan di riwayat chat Telegram Anda. Kalau keberatan atau
kontaknya banyak, pakai `--samarkan` (dan/atau `--tanpa-draf` di dalam argv). Detail lengkap &
pilihan lain (termasuk lewat agent AI): `skills/crm-wa/references/openclaw-jadwal.md`.

## 8. Ringkasan kas harian (kas-umkm), 21.00 WIB — kalau catatan kas terpisah dari kasir ✅/⚠️
Disalin persis dari `skills/kas-umkm/references/openclaw-jadwal.md` §"Pilihan 1". Pola
`--command-argv`/`--cron`/`--tz`/`--announce --channel telegram` ✅ **dijalankan sungguhan** untuk
skill lain (`kasir-lokal`, `crm-wa`); kombinasi persis dengan `kas.py` ⚠️ **belum diuji** di
Gateway oleh tim kurasi.
1. Cari path lengkap script (ganti `NAMA` dengan nama pengguna komputer Anda; argv tidak mengenal
   `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/kas-umkm/scripts/kas.py'))"
   ```
2. Buat jadwal:
   ```bash
   openclaw automations add --name "Ringkasan kas harian" --cron "0 21 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/kas-umkm/scripts/kas.py","rekap","--tanggal","hari-ini"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Database bukan di lokasi default → tambahkan `"--db","/path/kas.db"` setelah nama perintah di
  dalam argv.
- Uji dulu sebelum percaya jadwal aktif: `openclaw automations run <id> --wait`.
- Jadwal **hanya menjalankan perintah baca** (`rekap`) — tidak pernah `--ya`/`catat`/`pindah`.
  Detail lengkap & Pilihan 2 (lewat agent): `skills/kas-umkm/references/openclaw-jadwal.md`.

## 9. Ringkasan piutang reseller/pelanggan tempo (buku-piutang), 07.45 WIB ✅/⚠️
Disalin persis dari `skills/buku-piutang/references/openclaw-jadwal.md` §"Pilihan 1". Pola sama
dengan §8; kombinasi persis dengan `piutang.py` ⚠️ **belum diuji** di Gateway oleh tim kurasi.
1. Cari path lengkap script:
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/buku-piutang/scripts/piutang.py'))"
   ```
2. Buat jadwal (nama pelanggan disamarkan jadi inisial secara default):
   ```bash
   openclaw automations add --name "Ringkasan piutang harian" --cron "45 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/buku-piutang/scripts/piutang.py","ringkasan","--samarkan"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   Pemilik ingin nama lengkap: hapus `"--samarkan"` setelah ia menyetujui catatan privasi di
   `skills/buku-piutang/references/openclaw-jadwal.md`.
- Jadwal **hanya menjalankan perintah baca** (`ringkasan`) — tidak pernah `--ya`/`catat`/`bayar`.
  Draf pesan tagihan & tautan wa.me **tidak** ikut dijadwalkan; minta langsung ke agent.
- Uji dulu sebelum percaya jadwal aktif: `openclaw automations run <id> --wait`.

## 10. Laporan iklan mingguan (laporan-iklan-mingguan), Senin 08.00 WIB ✅/⚠️
Skill ini sendiri tidak membuat jadwal (§4 `references/openclaw-jadwal.md` skill ini) — perintah
di bawah adalah bentuk "3a" (perintah langsung, disarankan) yang **disalin persis** dari
`skills/laporan-iklan-mingguan/references/openclaw-jadwal.md`, hanya jam digeser dari 07.50 ke
**08.00 WIB** (sesuai jam yang diminta untuk paket ini — flag/struktur perintahnya tidak diubah).
Flag inti (`--command-argv`, `--cron`, `--tz`, `--announce --channel telegram`) ✅ **dijalankan
sungguhan** untuk skill lain (lihat `laporan-harian-usaha/references/openclaw-jadwal.md`);
kombinasi persis dengan `laporan_iklan.py` ⚠️ belum diuji end-to-end oleh tim kurasi.

**Wajib manual tiap minggu, sebelum jam jadwal:** ekspor CSV iklan dari Ads Manager dan pakai
**nama file tetap** — Senin pagi, ganti nama `meta-minggu-ini.csv` yang lama menjadi
`meta-minggu-lalu.csv` (timpa yang lama), lalu simpan ekspor baru sebagai `meta-minggu-ini.csv`.
```bash
openclaw automations add --name "Laporan iklan mingguan" --cron "0 8 * * 1" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/laporan-iklan-mingguan/scripts/laporan_iklan.py","analisis","/home/NAMA/Laporan-AI/iklan/meta-minggu-ini.csv","--sebelumnya","/home/NAMA/Laporan-AI/iklan/meta-minggu-lalu.csv","--nama-hasil","pesan WA"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
- Lebih dari satu platform (Meta + TikTok + Shopee, dst.): buat satu job per platform dengan
  `--name` berbeda, atau pakai Bentuk A (agent, §3 di `skills/laporan-iklan-mingguan/references/
  openclaw-jadwal.md`) agar agent menjalankan `analisis --json` per platform lalu `gabung`.
- Nama file berisi tanggal (`meta-2026-09-21.csv`) **tidak** bisa dipakai di bentuk ini — pakai
  nama tetap di atas.
- Windows: bentuk `--command-argv` ini belum diuji di Gateway Windows; pakai Bentuk A.
- Uji dulu sebelum percaya jadwal aktif: `openclaw automations run <id> --wait`.

## WhatsApp (hanya bila syarat berikut semua terpenuhi)
1. **Nomor terpisah** — bukan nomor toko/CS yang dikenal pelanggan.
2. Hanya mengirim ke **pemilik sendiri**.
3. Persetujuan risiko tertulis, contoh kalimat: *"OpenClaw memakai WhatsApp Web (tidak resmi,
   lewat scan QR). Syarat Layanan WhatsApp melarang pesan otomatis/massal, jadi nomor bisa
   diblokir. Untuk kirim ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya
   risiko ini. Saya mengerti risikonya."*
4. Jalankan `cek-privasi-openclaw` setelah nomor WA ditautkan, untuk memastikan
   `dmPolicy: "allowlist"` (bukan `pairing`/`open`) dan `allowFrom` hanya berisi nomor pemilik.

Ganti baris terakhir tiap perintah `add` di atas menjadi
`--announce --channel whatsapp --to "+62<nomor pemilik>"`. Status: `add` dengan
`--channel whatsapp` **diterima** ✅ walau plugin belum terpasang, tapi pengiriman nyata ke WA
⚠️ belum diverifikasi ujung-ke-ujung oleh tim kurasi.

## Yang BELUM diverifikasi ujung-ke-ujung ⚠️
- Membuat jadwal di atas langsung lewat chat WhatsApp/Telegram (pengguna mengetik "aktifkan
  laporan jam 9 malam" di chat, bukan lewat terminal/Control UI). Dukungannya ada di dokumentasi
  resmi, tapi belum dicoba tim kami. Kalau gagal/aneh, jalankan perintah yang sama dari terminal
  atau Control UI (`Settings → Automations`).
- Pesan benar-benar tiba di Telegram/WhatsApp pembeli (uji internal tidak memakai token bot/nomor
  asli — hanya struktur job yang diverifikasi).
- Perilaku agent AI sungguhan menjalankan skill di dalam job terjadwal (uji internal tidak
  memakai API key model).
- Jadwal follow-up CRM (§7, `crm-wa`) di atas — pola cron & `--command-argv` sudah terbukti untuk
  skill lain, tapi kombinasi persis dengan `crm.py` belum dicoba di Gateway oleh tim kurasi.
- Jadwal kas harian, piutang harian, dan laporan iklan mingguan (§8-10, `kas-umkm`,
  `buku-piutang`, `laporan-iklan-mingguan`) — pola cron & `--command-argv` sudah terbukti untuk
  skill lain, tapi kombinasi persis dengan script masing-masing skill belum dicoba di Gateway
  oleh tim kurasi.
