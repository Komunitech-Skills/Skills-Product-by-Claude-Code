# Pengingat mingguan "SOP belum diperbarui" ke Telegram (OpenClaw)

**Status verifikasi (jujur).** Bentuk perintah `openclaw automations add ... --command-argv ...` di
bawah sama persis dengan pola yang sudah dijalankan sungguhan di Gateway OpenClaw untuk skill lain
(`dolibarr-usaha`, `crm-wa` - lihat referensi masing-masing). **Khusus `siyuan-sop`, jadwal ini
belum diuji di Gateway OpenClaw sungguhan** (baru diuji manual dari terminal: perintah
`siyuan.py lama --hari 90` berjalan dan menampilkan hasil yang benar terhadap kernel SiYuan resmi).
Pengiriman ke Telegram juga belum diuji (butuh token bot asli). Jangan menambah flag yang tidak ada
di sini; jalankan `openclaw automations add --help` bila ragu.

## Aturan kanal (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik**, bukan grup/pelanggan.
- **Tidak ada broadcast.** Jadwal ini hanya menjalankan perintah **baca** (`lama`); tidak pernah
  `buat`, `tambah`, atau `--ya`.
- Tunjukkan perintah + "Lanjut? (ya/tidak)" ke pengguna sebelum membuat jadwal apa pun.
- WhatsApp hanya dengan nomor terpisah milik pemilik + persetujuan risiko tertulis (lihat aturan
  yang sama di `references/openclaw-jadwal.md` skill `dolibarr-usaha`/`crm-wa`).

## Syarat
- Komputer yang menjalankan Gateway OpenClaw **sama dengan komputer SiYuan** dan **kedua-duanya
  menyala saat jadwal berjalan**.
- Token API SiYuan sudah disimpan **oleh akun yang menjalankan Gateway**:
  `python3 <path siyuan.py> simpan-kunci`.
- ID buku catatan (notebook) yang mau dipantau (`daftar-buku` untuk melihatnya).

## Langkah
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/siyuan-sop/scripts/siyuan.py'))"
   ```
2. Uji dulu dari terminal: `python3 <path siyuan.py> lama --hari 90` harus menampilkan daftar
   (atau "Tidak ada dokumen ..."), bukan GAGAL.
3. Jadwal mingguan, tiap Senin 08.00 WIB:
   ```bash
   openclaw automations add --name "SOP belum diperbarui (SiYuan)" --cron "0 8 * * 1" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/siyuan-sop/scripts/siyuan.py","lama","--hari","90"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   - Hanya mau satu buku catatan tertentu: tambahkan `"--notebook","<id-buku-catatan>"` ke argv.
   - Alamat SiYuan bukan default: tambahkan `--command-env "SIYUAN_URL=http://127.0.0.1:6806"`
     (hanya alamat, **jangan pernah** menaruh token di `--command-env`/`--message`; token dibaca
     dari file lokal `simpan-kunci`).
   - Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau lewat agent (opsi di bawah).

## Lewat agent AI (opsional, memakai kuota model)
```bash
openclaw automations add --name "SOP belum diperbarui (agent)" --cron "0 8 * * 1" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill siyuan-sop: jalankan scripts/siyuan.py lama --hari 90 (hanya baca; JANGAN menjalankan buat/tambah/--ya). Kirim daftarnya apa adanya. Kalau kosong, katakan semua SOP masih baru." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id> --wait` |
| Riwayat | `openclaw automations runs --id <id>` |
| Jeda / aktifkan | `openclaw automations disable <id>` / `enable <id>` |
| Hapus | `openclaw automations rm <id>` |

## Jika bermasalah
- `summary` "GAGAL: Tidak bisa terhubung ..." → SiYuan belum dibuka di komputer itu.
- `summary` "Token API belum diatur" padahal jalan di terminal sendiri → token disimpan oleh akun
  lain; jalankan `simpan-kunci` dengan akun yang menjalankan Gateway.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat, lihat skill
  `laporan-otomatis-terjadwal`).
