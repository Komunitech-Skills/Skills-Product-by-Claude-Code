# Perintah OpenClaw untuk Pantau Cron (siap salin)

> **Kredensial & aksi (wajib):** jangan membaca token/kunci dari environment, `openclaw.json`, `.env`, database atau log OpenClaw. Cek kanal hanya dengan `openclaw channels status --channel telegram`. Jangan membuat/mengubah jadwal atau mengirim pesan uji sebelum pengguna membalas "ya" atas ringkasan rencana.
> **Aturan berhenti:** bila SATU perintah `openclaw automations ...`/`cron ...` gagal (ditolak, token/kredensial, Gateway tidak bisa dihubungi), berhenti memakai alat `openclaw`. DILARANG: membaca/mengubah `openclaw.json`, memeriksa/menulis token, menjalankan `openclaw doctor` (termasuk `--fix`), merestart Gateway, atau meminta alat lain mengubah konfigurasi Gateway. Lanjut ke bagian 0 (rencana siap salin).

## 0. Rencana siap salin saat terblokir
Tampilkan seluruh bagian ini dengan nilai terisi (jadwal job, nama, folder skill), tutup "Lanjut? (ya/tidak)":
1. Tabel job (nama, jadwal dalam kata-kata, toleransi, jadwal berikutnya dari keluaran `daftar`).
2. Per job, perintah edit prompt (bagian 2) dengan `<id-job>` diisi dari `openclaw automations list --all` bila ada, bila tidak `[isian: id job]`.
3. Dua perintah pengawas (bagian 3), tujuan `[isian: ID chat Telegram Anda]`.
4. Satu kalimat awam: agen belum punya izin ke pengatur jadwal OpenClaw; salin perintah ke terminal sendiri atau minta pemilik/penyedia OpenClaw memberi izin.

Pola dan status verifikasi (meniru `laporan-otomatis-terjadwal/references/openclaw.md` dan `bot-trading-kripto/references/openclaw-jadwal.md`):
- Semua flag di bawah (`--cron`, `--tz`, `--name`, `--session`, `--command-argv`, `--announce`, `--channel`, `--to`, `--message`, `--exact`, `edit`, `list --all`, `runs`, `disable`) **dicek lewat `--help` OpenClaw 2026.9.8 dan 2026.10.2** (statusnya "dicek --help").
- Pola *job perintah tanpa model AI* + keluaran persis `NO_REPLY` tidak dikirim ke chat: **terbukti** untuk skill `bot-trading-kripto` di Gateway uji 2026.9.5. Kombinasi utuh untuk skill ini (pengiriman Telegram sungguhan) **belum diuji** -- sebutkan jujur ke pengguna: "uji dulu dengan `automations run <id> --wait`".
- Versi OpenClaw pengguna bisa berbeda: bila flag gagal, jalankan `openclaw automations add --help` dan sesuaikan.
- Fallback: bila perintah komputer tidak diizinkan (atau platform bukan OpenClaw), tampilkan perintah sebagai teks untuk dijalankan pengguna sendiri di terminal, atau lewat Control UI (`Settings -> Automations`).

`<folder-skill-absolut>` = alamat lengkap folder skill ini di komputer pengguna (mis. `~/.openclaw/skills/pantau-cron-openclaw`). Windows: ganti `python3` dengan `python`, dan tulis alamat dengan garis miring biasa `/`.

## 1. Daftarkan job ke pantauan (lokal, boleh langsung)
```bash
python3 scripts/pantau_cron.py tambah laporan-harian --jadwal "0 21 * * *" --zona WIB --toleransi 30
python3 scripts/pantau_cron.py tambah piutang-pagi  --jadwal "45 7 * * 1-5" --zona WIB
python3 scripts/pantau_cron.py daftar
```
Zona: `WIB`, `WITA`, `WIT`, `UTC` (atau `Asia/Jakarta`, `Asia/Makassar`, `Asia/Jayapura`). Jadwal pantauan **harus sama** dengan jadwal `--cron` dan `--tz` job aslinya (lihat `openclaw automations list --all`). Toleransi 30 menit sudah menutupi penundaan acak (stagger) bawaan OpenClaw; job yang butuh tepat waktu bisa ditambah `--exact` saat dibuat.

## 2. Ping di akhir job
**Job berupa pesan ke agent** -- ubah prompt (butuh "ya"; tampilkan prompt lama dan baru):
```bash
openclaw automations list --all          # catat id job
openclaw automations edit <id-job> --message "<prompt lama utuh> Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah python3 <folder-skill-absolut>/scripts/pantau_cron.py ping laporan-harian . Jangan dijalankan bila ada langkah yang gagal."
```
Job harus boleh menjalankan perintah (tool `exec`). Bila job dibuat dengan `--tools`, pastikan `exec` ada di daftarnya.

**Job berupa perintah** (`--command-argv`): tambahkan `python3 .../pantau_cron.py ping <nama>` sebagai perintah terakhir di script job itu.

## 3. Job pengawas (tanpa model AI, tanpa biaya token)
Tiap jam, hanya bicara bila ada masalah:
```bash
openclaw automations add --cron "5 * * * *" --tz "Asia/Jakarta" \
  --name "Pengawas jadwal (tiap jam)" --session isolated \
  --command-argv '["python3", "<folder-skill-absolut>/scripts/pantau_cron.py", "cek", "--openclaw"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Keluaran `NO_REPLY` (tenang) tidak dikirim. Bila ada masalah, pesan berawalan `PANTAU CRON` dikirim; masalah yang sama tidak diulang dalam 6 jam (`--ulang-jam` bisa diubah di argv), dan satu pesan PULIH dikirim saat job kembali melapor.

Ringkasan harian sekali (semua job + ping terakhir):
```bash
openclaw automations add --cron "0 8 * * *" --tz "Asia/Jakarta" \
  --name "Ringkasan pantauan jadwal (harian)" --session isolated \
  --command-argv '["python3", "<folder-skill-absolut>/scripts/pantau_cron.py", "cek", "--tanpa-catat"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Folder data lain dari bawaan: tambahkan `"--folder", "<alamat>"` di argv semua perintah (atau atur `PANTAU_CRON_DIR`).

## 4. Uji sebelum dianggap aktif
1. `python3 scripts/pantau_cron.py cek` -> semua job OK atau "menunggu jadwal pertama".
2. `openclaw automations run <id-pengawas> --wait`, lalu `openclaw automations runs <id-pengawas>` -> berhasil, tidak ada pesan saat tenang.
3. Alarm palsu terkendali (setelah "ya"): `tambah uji-alarm --jam <HH.MM tiga menit dari sekarang> --toleransi 1`, tunggu ±5 menit (jadwal harus lewat SESUDAH job didaftarkan), jalankan pengawas sekali -> pesan HILANG masuk Telegram; lalu `hapus uji-alarm` (pengawas akan mengirim PULIH atau diam).
4. Jalankan satu job asli (`automations run <id-job> --wait`) -> `riwayat <nama>` menampilkan ping baru.

## 5. Opsi lanjutan: Healthchecks milik sendiri (tanpa wajib, tidak berafiliasi)
Kelemahan pengawas lokal: bila komputer/gateway mati total, pengawas ikut diam. Layanan Healthchecks (open-source; bisa dipasang sendiri atau memakai versi hosted milik pengguna) memantau dari luar: ia yang mengabari bila ping berhenti datang. Komunitech tidak berafiliasi dengan proyek atau layanannya; kebijakan harga dan batas layanan hosted mengikuti penyedianya.

Langkah untuk pengguna (agent hanya memandu, tidak menyentuh alamatnya):
1. Buat akun/instalasi Healthchecks sendiri, buat satu *check* per job, atur jadwal (cron + zona) dan masa tenggang sama dengan toleransi. Atur notifikasinya di sana (mis. Telegram atau email).
2. Salin alamat ping tiap check. **Jangan tempel di chat.** Alamat itu rahasia siapa pun yang punya bisa mengirim ping palsu.
3. Buka berkas `healthchecks.json` di folder data pantauan dengan editor teks, isi:
   ```json
   {"laporan-harian": "<alamat ping check laporan-harian>",
    "piutang-pagi": "<alamat ping check piutang-pagi>"}
   ```
4. Selesai: setiap `ping` kini juga memanggil layanan itu (gagal jaringan tidak menggagalkan job; `--tanpa-luar` melewatinya). Ping lokal tetap dicatat, jadi `cek` lokal tetap berjalan.
Data yang keluar komputer hanya "ping" kosong ke alamat itu; isi laporan tidak pernah dikirim.

## 6. Kelola
```bash
python3 scripts/pantau_cron.py daftar            # semua job + ping terakhir
python3 scripts/pantau_cron.py riwayat laporan-harian
python3 scripts/pantau_cron.py hapus piutang-pagi        # berhenti memantau
openclaw automations disable <id-pengawas>       # jeda (WAJIB id, bukan nama)
openclaw automations enable <id-pengawas>
```
Mengubah jadwal job asli? Jalankan `tambah <nama> --jadwal "..." --ganti` agar pantauan ikut berubah. Libur panjang/mesin sengaja dimatikan: jeda pengawas atau `hapus` jobnya dulu supaya tidak ada peringatan palsu.

## 7. Mesin 24 jam
Jadwal OpenClaw hanya jalan saat komputer/gateway menyala. Panduan opsi mesin 24 jam (laptop/mini PC/VPS milik sendiri) ada di skill `laporan-otomatis-terjadwal`; Komunitech menawarkan **jasa setup berbayar**.
