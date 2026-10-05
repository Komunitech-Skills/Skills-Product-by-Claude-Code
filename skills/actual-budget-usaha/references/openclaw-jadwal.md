# Ringkasan anggaran terjadwal ke Telegram pemilik (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status:** ⚠️ **belum diverifikasi untuk skill ini.** Perintah mengikuti pola yang sudah diuji pada skill
`dolibarr-usaha` (OpenClaw 2026.9.6: `automations add --command-argv` diterima, `automations run --wait` menjalankan
script). Untuk `actual-budget-usaha` sendiri belum dijalankan di Gateway sungguhan, dan pengiriman nyata ke Telegram
belum diuji (butuh bot token asli). Uji muat skill mengikuti `scripts/uji_openclaw.sh` repo pengembang.

## Aturan kanal (keputusan pemilik Komunitech)
- Telegram (bot resmi) = default; `--to` selalu ID chat **pemilik**. Ringkasan keuangan tidak dikirim ke grup,
  karyawan, atau pelanggan.
- WhatsApp hanya dengan **nomor terpisah** milik pemilik + persetujuan risiko tertulis (OpenClaw memakai WhatsApp Web,
  tidak resmi, nomor bisa diblokir). Tanpa broadcast.
- Tunjukkan perintah lengkap + "Lanjut? (ya/tidak)" sebelum membuat jadwal.

## Syarat
1. Gateway OpenClaw jalan di komputer yang **sama** dengan folder budget Actual (aplikasi desktop), dan menyala saat
   jadwal. Aplikasi Actual tidak perlu dibuka (file dibaca langsung, read-only).
2. Path lengkap script dan budget (argv tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/actual-budget-usaha/scripts/actual_budget.py'))"
   python3 <path actual_budget.py> cari
   ```
3. Uji dulu di terminal: `python3 <path> ringkasan --db "<folder budget>" --bulan ini` harus menampilkan ringkasan.

## Pilihan 1 (disarankan): perintah langsung, tanpa AI
Script dijalankan Gateway; teksnya dikirim apa adanya (angka tidak bisa diubah AI, tanpa kuota model).

**Tiap Senin 07.50 WIB, posisi bulan berjalan:**
```bash
openclaw automations add --name "Ringkasan anggaran mingguan" --cron "50 7 * * 1" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/actual-budget-usaha/scripts/actual_budget.py","ringkasan","--db","/home/NAMA/Documents/Actual/Studio-Rina-abc1234","--bulan","ini"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
**Tanggal 1 tiap bulan 07.50 WIB, rekap bulan lalu:** ganti `--cron "50 7 1 * *"` dan `"--bulan","lalu"`.

- Windows: path seperti `"C:\\Users\\NAMA\\Documents\\Actual\\Studio-Rina-abc1234"` (garis miring terbalik digandakan
  di JSON) dan `"python"` atau `"py"` sebagai ganti `"python3"`. ⚠️ `--command-argv` di Gateway Windows belum diuji;
  bila gagal pakai Pilihan 2.
- WITA/WIT: `--tz Asia/Makassar` / `Asia/Jayapura`.
- Ringkasan hanya seakurat transaksi yang sudah diimpor. Ingatkan pemilik mengimpor mutasi (skill ini, perintah
  `konversi`) sebelum jadwal, misalnya tiap Minggu malam.
- File budget sedang dikunci Actual saat jadwal → kode keluar 4, jadwal tercatat gagal (sengaja, agar pemilik tahu).

## Pilihan 2: lewat agent AI (Windows, atau ingin saran tambahan)
```bash
openclaw automations add --name "Ringkasan anggaran (agent)" --cron "50 7 * * 1" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill actual-budget-usaha: jalankan scripts/actual_budget.py ringkasan --db '<folder budget>' --bulan ini (hanya baca) lalu kirim teksnya apa adanya. Boleh tambah maksimal 3 saran singkat berbasis angka. Jangan ubah angka. Jangan kirim ke siapa pun selain pemilik." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```
Isi jawaban agent ⚠️ belum diuji (butuh API key model).

## Menyiapkan Telegram (sekali)
Buat bot di @BotFather → `openclaw channels add --channel telegram --token <token>` → kirim "halo" ke bot dari akun
pemilik → `openclaw pairing list telegram` lalu `openclaw pairing approve telegram <KODE>`. Cara mencari ID chat:
skill `laporan-otomatis-terjadwal`, `references/openclaw.md`.

## Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id> --wait` (cek `status`, `summary`, `deliveryStatus`) |
| Jeda / aktifkan | `openclaw automations disable <id>` / `openclaw automations enable <id>` |
| Hapus | `openclaw automations rm <id>` |

## Jika bermasalah
- `Gateway not reachable` → komputer/Gateway belum menyala.
- `summary` "File budget ... tidak ditemukan" → folder budget pindah (mis. setelah ganti folder data di Actual);
  jalankan `cari` dan perbarui path.
- `summary` "sedang dipakai" → Actual sedang menyimpan; ubah jam jadwal atau jalankan ulang.
- `deliveryStatus: not-delivered` + `Telegram bot token missing` → kanal Telegram belum disiapkan.
