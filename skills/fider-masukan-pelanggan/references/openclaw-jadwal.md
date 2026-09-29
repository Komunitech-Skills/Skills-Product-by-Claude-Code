# Ringkasan masukan mingguan ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat. Kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak: berhenti dan beri langkah persiapannya.

**Status verifikasi (jujur).** Bentuk perintah di bawah mengikuti pola yang sudah dipakai skill lain di repo ini (`umami-analitik`, `pantau-website-toko`) di Gateway OpenClaw 2026.9.x. Untuk `fider-masukan-pelanggan`, **jadwal dan pengiriman ke Telegram belum diuji** (PERLU UJI NYATA). Yang sudah diuji: `ringkasan-mingguan` terhadap Fider v0.38.0 asli. Jika opsi ditolak: `openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik usaha**, bukan pelanggan/grup. Tidak ada broadcast.
- Jadwal hanya menjalankan perintah **baca** (`ringkasan-mingguan`). Perintah tulis (impor, status, gabung, komentar) **tidak boleh dijadwalkan**; selalu lewat persetujuan manusia.
- Ringkasan memuat judul pos yang sudah publik, tanpa data pribadi. Teks tetap tersimpan di riwayat Telegram pemilik.

## Syarat
- Gateway berjalan di komputer yang bisa menjangkau Fider (komputer/VPS yang sama dengan Fider, atau alamat `https://...`), dan **menyala saat jadwal**.
- Kunci API sudah disimpan dengan `simpan-kunci` di komputer Gateway (akun Collaborator disarankan; ringkasan hanya butuh membaca).

## Perintah langsung (tanpa model AI), tiap Senin 07.00 WIB
1. Path lengkap script: `python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/fider-masukan-pelanggan/scripts/fider.py'))"`
2. Tunjukkan perintah ini ke pemilik, tunggu "ya", lalu jalankan:
   ```bash
   openclaw automations add --name "Fider - ringkasan masukan mingguan" --cron "0 7 * * 1" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/fider-masukan-pelanggan/scripts/fider.py","ringkasan-mingguan","--top","5"]' \
     --command-env '{"FIDER_URL":"http://localhost:3000"}' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
3. Cek: `openclaw automations list`. Hentikan: hapus jadwal lewat `openclaw automations` sesuai `--help`.

Untuk analisis lanjutan (apa yang harus dikerjakan dulu), tempelkan ringkasan ke skill `iterasi-dari-masukan-pelanggan`.
