# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (input persis examples/01 "Catat Bu Rina, kontrol behel lagi 3 hari lagi ..." → `pengingat_pasien.py tambah ... --persetujuan ya`; "Siapa yang harus diingatkan hari ini?" → daftar H-3 + draf)
3 Permintaan malas: ✅ ("catet dong pak budi vaksin lagi bulan depan" → bertanya sekali: nomor WA & persetujuan diingatkan)
4 Script: ✅ 29 Sep + 3 hari = Jumat 2 Okt 2026, masuk kelompok H-3; draf pesan sama dengan templat examples/01 (hanya tanggal berbeda karena hari uji 29/9)
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara (draf + peringatan salin & kirim sendiri, tanpa kirim otomatis)
Masalah: Kosmetik: agent menulis nomor tersimpan sebagai "62812-3456-7890".

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
