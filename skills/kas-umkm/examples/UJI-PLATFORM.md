# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (input persis examples/01 Warung Makan Bu Tini → agent membaca SKILL.md + references/perintah.md, menampilkan pratinjau gabungan + asumsi kategori, simpan setelah "ya")
3 Permintaan malas: ✅ ("catet dong td laku 800rb, abis itu beli gas 25rb" → langsung pratinjau 2 baris + saldo laci Rp 2.353.500, minta "ya")
4 Script: ✅ Laci Rp 1.578.500, BRI Rp 4.830.000, GoPay Rp 225.000, total Rp 6.633.500 (naik Rp 2.983.500); masuk Rp 4.735.000, keluar Rp 1.751.500, hasil usaha Rp 3.083.500, per hari 1.265.000 / 988.500 / 830.000; opname Rp 1.233.500 selisih kurang Rp 345.000 — sama dengan examples/01
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara (rekap, saldo per akun, opname + ajakan cek tanpa menuduh)
Masalah: Uji 3: agent menulis "Tidak ada asumsi kategori yang ditebak" padahal metode tunai & kategori beli-stok untuk gas diasumsikan — sebaiknya asumsi selalu disebut.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
