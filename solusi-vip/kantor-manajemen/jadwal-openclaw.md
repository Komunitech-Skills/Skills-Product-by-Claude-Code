# Jadwal OpenClaw siap salin — Kantor & Manajemen

Semua perintah **disalin dari** `skills/<nama-skill>/references/openclaw-jadwal.md` skill terkait
(bukan sintaks baru). Pola dasarnya (`automations add`, `--cron`/`--tz`, `--command-argv`,
`--session isolated --tools exec,read`, `--announce --channel telegram --to`) sama dengan yang
dipakai paket `konsultan/` dan `usaha-offline/`, yang flag-nya sudah dicocokkan dengan
`openclaw automations add --help` OpenClaw 2026.9.6 (lihat `solusi-vip/README.md`, bagian
Metodologi).

Legenda (tanda teknis untuk staf IT; pemilik cukup tahu ✅ = sudah terbukti jalan, 📖/⚠️ = perlu diuji dulu): ✅ = pola dijalankan sungguhan di Gateway uji oleh tim kurasi. 📖 = hanya dicek lewat
`--help`/disalin dari pola ✅ skill lain. ⚠️ = kombinasi persis skill ini belum dicoba di Gateway.
**Kirim pesan sungguhan ke Telegram belum pernah diuji** (butuh bot token asli) — uji dulu
dengan `openclaw automations run <id> --wait`.

Ganti `NAMA` dengan nama pengguna komputer, `<ID chat Telegram pimpinan>` dengan ID chat
Telegram **pribadi** penerima. Cari path lengkap script (tanda `~` tidak dikenal di
`--command-argv`):
```bash
python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/laporan-harian-usaha/scripts/laporan.py'))"
```
Windows: ganti `"python3"` dengan `"py"` atau `"python"` — belum diuji; bila gagal pakai
bentuk agent (`--message`) di tiap bagian.

## 0. Aturan kanal
- **Telegram (bot resmi) = default.** `--to` = ID chat pribadi **pimpinan**. Penerima tambahan
  (mis. manajer keuangan) = **jadwal terpisah** dengan ID chatnya sendiri. **Tidak ada** kirim ke
  grup, karyawan, atau pelanggan; **tidak ada** broadcast.
- **WhatsApp** hanya bila: nomor **terpisah**, laporan hanya ke pemilik sendiri, dan pemilik
  menyetujui secara tertulis: *"OpenClaw memakai WhatsApp Web (tidak resmi, lewat scan QR).
  Syarat Layanan WhatsApp melarang pesan otomatis/massal, jadi nomor bisa diblokir. Untuk laporan
  ke diri sendiri risikonya rendah, tapi tetap ada. Telegram tidak punya risiko ini. Saya
  mengerti risikonya."* Lalu ganti baris terakhir jadwal menjadi
  `--announce --channel whatsapp --to "+62<nomor pemilik>"`. Pengiriman nyata ke WA ⚠️ belum diuji.
- Semua jadwal di bawah **hanya membaca**. Tunjukkan perintah + "Lanjut? (ya/tidak)" sebelum
  membuat jadwal, dan uji sekali sebelum dinyatakan aktif.

## 1. [VIP] Laporan harian manajemen, 21.00 WIB (laporan-harian-usaha) ✅
Dari `skills/laporan-harian-usaha/references/openclaw-jadwal.md` (flag inti ✅ dijalankan sungguhan):
```bash
openclaw automations add --name "Laporan harian usaha" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/laporan-harian-usaha/scripts/laporan.py"]' \
  --command-cwd "/home/NAMA/.openclaw/workspace" \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```
- Pasang `buku-stok` dan alat lain di folder skills yang sama; alat yang tidak ada dilewati.
- Nama karyawan jadi inisial: tambahkan `"--samarkan"` ke argv.
- Pabrik/gudang shift malam: `--cron "0 7 * * *"` dan tambahkan `"--tanggal","kemarin"` ke argv.

## 2. [VIP] Laporan mingguan manajemen, Senin 07.00 WIB ✅
```bash
openclaw automations add --name "Laporan mingguan usaha" --cron "0 7 * * 1" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/laporan-harian-usaha/scripts/laporan.py","--periode","mingguan"]' \
  --command-cwd "/home/NAMA/.openclaw/workspace" \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```

## 3. Tugas tim dari Vikunja: hari ini 07.00 & terlambat 07.05 WIB (vikunja-tugas) ✅/📖
Dari `skills/vikunja-tugas/references/openclaw-jadwal.md` §Pilihan 1 (tanpa model AI). Simpan
token API Vikunja **baca-saja** lebih dulu (`simpan-kunci`, lihat `SKILL.md` skill itu).
```bash
openclaw automations add --name "Vikunja - tugas hari ini" --cron "0 7 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/vikunja-tugas/scripts/vikunja.py","hari-ini"]' \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"

openclaw automations add --name "Vikunja - tugas terlambat" --cron "5 7 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/vikunja-tugas/scripts/vikunja.py","terlambat"]' \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```
- **Jangan** menaruh token/kunci di `--command-argv`. Alamat Vikunja bukan bawaan → tambahkan
  `--command-env '{"VIKUNJA_URL":"http://127.0.0.1:3456"}'` (hanya alamat, bukan token).
- Jadwal hanya `hari-ini`/`terlambat` (baca). Tidak pernah `tambah`, `selesai`, atau `--ya`.
- Isi pesan memuat judul tugas dan nama pengguna Vikunja, dan tersimpan di riwayat chat
  Telegram penerima. Beri tahu tim (lihat `PANDUAN.md` Bab 3).
- Bentuk agent (bila `--command-argv` gagal, mis. Windows):
  ```bash
  openclaw automations add --name "Vikunja - digest harian (agent)" --cron "0 7 * * *" --tz Asia/Jakarta \
    --session isolated --tools exec,read \
    --message "Pakai skill vikunja-tugas: jalankan hari-ini lalu terlambat (hanya baca; JANGAN menjalankan tambah/selesai/--ya). Kirim teksnya apa adanya ke saya. Jangan ubah judul/tanggal." \
    --announce --channel telegram --to "<ID chat Telegram pimpinan>"
  ```

## 4. Ringkasan piutang, 07.45 WIB (buku-piutang) ✅/⚠️
Dari `skills/buku-piutang/references/openclaw-jadwal.md` (sama dengan `konsultan/` §8c). Nama
pelanggan disamarkan jadi inisial.
```bash
openclaw automations add --name "Ringkasan piutang harian" --cron "45 7 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/buku-piutang/scripts/piutang.py","ringkasan","--samarkan"]' \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```
Hanya perintah baca — tidak pernah `catat`/`bayar`/`--ya`. Draf penagihan (`tagih-piutang`)
**disalin & dikirim staf keuangan**, tidak pernah dijadwalkan ke pelanggan.

## 5. Stok menipis, 07.00 WIB (buku-stok) 📖
Sama dengan `usaha-offline/jadwal-openclaw.md` §3 (bentuk agent ✅ untuk pola, hanya baca):
```bash
openclaw automations add --name "Laporan stok menipis" --cron "0 7 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill buku-stok: jalankan laporan menipis (hanya baca) dan kirim daftarnya apa adanya." \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```

## 6. [VIP] Laporan gabungan lewat agent dengan saran singkat (opsional) ✅ (isi jawaban ⚠️)
Dari `skills/laporan-harian-usaha/references/openclaw-jadwal.md` "Pilihan 2". Diterima Gateway
(`agentTurn`, `toolsAllow: ["exec","read"]`); kualitas isi jawaban butuh model AI sungguhan.
```bash
openclaw automations add --name "Laporan harian (agent)" --cron "0 21 * * *" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill laporan-harian-usaha: jalankan scripts/laporan.py (hanya baca) lalu kirim teksnya apa adanya. Boleh tambah maksimal 3 saran singkat di bawahnya. Jangan ubah angka. Jangan kirim ke siapa pun selain pemilik." \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```

## 7. Data dari file ekspor (laporan-otomatis-terjadwal)
Bila data penjualan/kas masih berupa CSV/Excel dari aplikasi lain, `laporan-otomatis-terjadwal`
menjadwalkan pengiriman hasil olahannya dengan pola yang sama (Bentuk A). Contoh (jadwal & pesan sebagai argumen posisi, tanpa `--cron`):
```bash
openclaw automations add "0 21 * * *" \
  "Pakai skill rekap-penjualan-csv pada file <folder-kerja>/penjualan/terbaru.csv lalu kirim ringkasannya apa adanya. Jangan mengubah angka." \
  --name "Rekap penjualan dari CSV" --tz "Asia/Jakarta" --session isolated --tools exec,read \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```
Perintah lengkap: `skills/laporan-otomatis-terjadwal/
references/openclaw.md`.

## 8. Mengelola jadwal ✅
```bash
openclaw automations list --all
openclaw automations show "<nama persis>"           # boleh nama ATAU id
openclaw automations edit <id> --cron "30 7 * * *" --tz "Asia/Jakarta"
openclaw automations disable <id>                   # hanya id
openclaw automations enable <id>                    # hanya id
openclaw automations run <id> --wait                # uji dulu sebelum percaya "aktif"
openclaw automations runs --id <id>
openclaw automations rm <id>                        # hanya id, permanen
```
`disable`/`enable`/`edit`/`run`/`rm` dengan **nama** ditolak ("Automation not found") — pakai
`id` (UUID) dari hasil `add`.

## 9. [PILIH SATU] Laporan harian dari Dolibarr ATAU Frappe Books, 21.00 WIB ✅/⚠️
**Dolibarr** — dari `skills/dolibarr-usaha/references/openclaw-jadwal.md` (✅ dijalankan
sungguhan; kunci API dibaca dari file lokal, tidak ditaruh di jadwal):
```bash
openclaw automations add --name "Laporan harian Dolibarr" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/dolibarr-usaha/scripts/dolibarr.py","laporan-harian"]' \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```
- Alamat bukan `http://localhost/dolibarr`: tambahkan `--command-env "DOLIBARR_URL=http://localhost:8080/dolibarr"`.
- Dolibarr mati saat jadwal → pesan "GAGAL ... Nyalakan Dolibarr" (kode keluar 3), bukan angka palsu.

**Frappe Books** — dari `skills/frappe-books-usaha/references/openclaw-jadwal.md` (⚠️ belum
dijalankan di Gateway untuk skill ini; menyalin pola Dolibarr):
```bash
openclaw automations add --name "Laporan harian Frappe Books" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/frappe-books-usaha/scripts/frappe_books.py","laporan-harian","--db","/home/NAMA/Documents/Frappe Books/Toko Saya.books.db"]' \
  --announce --channel telegram --to "<ID chat Telegram pimpinan>"
```
Sesuaikan path `.books.db`. Keduanya aplikasi yang **perlu dipasang** — tawarkan **jasa setup
berbayar Komunitech**.

## 10. Yang belum diverifikasi ⚠️
- Pesan benar-benar tiba di Telegram/WhatsApp (uji internal tanpa token/nomor asli).
- Membuat jadwal langsung dari chat ("aktifkan laporan jam 9 malam"): bergantung izin `cron`
  agent; kalau gagal/aneh, jalankan perintah dari terminal/Control UI.
- Kombinasi persis `--command-argv` dengan skrip `vikunja-tugas`, `buku-piutang`, dan
  `frappe-books-usaha` di Gateway (pola dasarnya sudah terbukti untuk skill lain).
- Gateway Windows untuk `--command-argv`.

## 11. Syarat mesin menyala
Jadwal berjalan **di dalam proses Gateway**. Mesin mati/tidur di jam jadwal → laporan **tidak
terkirim**, tanpa pesan error. Opsi (tanpa harga): komputer kantor yang menyala di jam kerja,
mini PC/VPS 24 jam milik perusahaan, atau **jasa setup berbayar Komunitech**.
