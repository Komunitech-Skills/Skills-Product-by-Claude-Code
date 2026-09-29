# Jadwal otomatis + notifikasi Telegram lewat OpenClaw

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

Pola di bawah **dipakai ulang** dari skill `pantau-pasar-kripto`
(`references/openclaw-jadwal.md`), yang sudah **terbukti (T)** di Gateway OpenClaw 2026.9.5 Linux:
`automations add --cron … --tz … --command-argv '[…]' --command-cwd … --announce --channel telegram --to …`.
Job command tidak memanggil model AI; OpenClaw tidak mengirim apa pun bila keluaran persis `NO_REPLY`.

Status untuk skill ini: kombinasi opsi = **T** (sama persis dengan pola terbukti); dijalankan
dengan script `jalankan_bot.py --openclaw` = **S** (belum diuji di Gateway khusus untuk skill ini;
perilaku `--openclaw` yang selalu exit 0 dan mencetak `NO_REPLY` saat tenang sudah diuji di
`tests/uji_regresi.py`). Uji dulu dengan `automations run <id> --wait` (lihat bawah).

## 1. Bot mode paper/testnet: tiap jam
```bash
openclaw automations add --cron "0 * * * *" --tz "Asia/Jakarta" \
  --name "Bot kripto (paper) tiap jam" --session isolated \
  --command-argv '["python3", "<folder-skill-ini-absolut>/scripts/jalankan_bot.py", "--konfigurasi", "bot/konfigurasi.json", "--openclaw"]' \
  --command-cwd "<folder-workspace-member>" \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Windows: ganti `"python3"` dengan `"python"` bila `python3` tidak ada (status S di Windows).

## 2. Bot mode live
Sama, tetapi tambahkan `"--izinkan-live"` ke array argv **setelah** member menyelesaikan
Langkah E di SKILL.md. Nama job sebaiknya memuat kata "LIVE". Tanpa `--izinkan-live`, bot
berhenti sendiri dan mengirim notifikasi penolakan.

## 3. Menguji sebelum mengaktifkan
1. Jalankan dulu dari terminal: `python3 <skill>/scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --openclaw`
   → keluaran pesan atau `NO_REPLY`, kode keluar 0.
2. Setelah `automations add`, jalankan `openclaw automations run <id> --wait` sekali dan periksa
   `openclaw automations runs <id>`: `completionStatus: succeeded`, pesan terkirim saat ada
   transaksi, tidak ada upaya kirim saat `NO_REPLY`.

## 4. Kelola
```bash
openclaw automations list --all
openclaw automations disable <id>     # jeda (WAJIB id/UUID, bukan nama)
openclaw automations enable <id>
openclaw automations rm <id>          # hapus
```
Menjeda jadwal **bukan** tombol berhenti: bila member ingin bot berhenti total, jalankan
`scripts/berhenti.py` (membuat file `bot/STOP`) **dan** jeda jadwalnya.

## 5. Perintah dari Telegram
Member cukup menulis ke agen OpenClaw: "stop bot", "status bot", "lanjutkan bot". Agent menjalankan
`berhenti.py` sesuai Langkah G SKILL.md. "Stop" dijalankan segera; "lanjutkan" hanya setelah
alasan berhenti dijelaskan dan member setuju eksplisit.

## 6. Kanal
Telegram (bot resmi) = default. WhatsApp hanya dengan nomor terpisah + persetujuan risiko
tertulis (keputusan pemilik Komunitech 2026-09-23). Tidak ke grup, tidak broadcast.
Mesin harus menyala agar bot berjalan: laptop/mini PC menyala 24 jam atau VPS milik member,
atau jasa setup berbayar Komunitech.
