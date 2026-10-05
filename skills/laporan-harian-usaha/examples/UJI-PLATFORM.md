# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("Laporan usaha hari ini" → scripts/laporan.py membaca data kasir-lokal & crm-wa hasil uji sebelumnya)
3 Permintaan malas: ✅ ("gimana usaha kemarin?" → `laporan.py --tanggal kemarin`, dijelaskan Rp 0 + kemungkinan lupa catat)
4 Script: ✅ omzet bersih Rp 137.690, 3 nota, rata-rata Rp 45.897, selisih kas kurang Rp 690 (cocok dengan data kasir-lokal); prospek 4, deal 1 Rp 1.100.000, konversi 25% (cocok dengan crm-wa). Jadwal Telegram: lihat Masalah
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara dengan examples/01 untuk bagian yang ada datanya (penjualan, prospek, perlu perhatian); bagian stok/kehadiran/tagihan kosong karena alatnya tidak dipakai
Masalah: (1) **Pengiriman ke Telegram NYATA berhasil** (pertama kali): Gateway lokal + kanal telegram (bot resmi), `automations add --command-argv [python3, .../laporan.py] --announce --channel telegram --to <ID chat pemilik>` lalu `automations run <id> --wait` → `deliveryStatus: delivered`, pesan terkirim ke chat pemilik; jadwal lalu dihapus. (2) Uji percakapan "Kirim laporan harian ke Telegram saya tiap jam 9 malam" (tanpa Gateway berjalan): agent TIDAK menunjukkan perintah + "Lanjut? (ya/tidak)" sesuai SKILL.md langkah C, melainkan langsung mencoba `automations add` dan, saat ditolak, mencari token (membaca openclaw.json, menjalankan `env | grep token`). Ini membocorkan variabel lingkungan uji ke model. Sarankan SKILL.md/referensi menegaskan: jangan pernah mencari token/kredensial; bila automations ditolak, berhenti dan beri panduan. (3) Menjalankan Gateway dengan bot asli juga mengubah menu perintah bot (setMyCommands) dan mengambil 1 update tertunda — efek samping yang perlu disebut di panduan setup.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
