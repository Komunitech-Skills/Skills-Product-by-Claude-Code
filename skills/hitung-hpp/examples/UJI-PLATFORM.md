# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (input persis examples/01 keripik pisang; agent membaca SKILL.md + references/format-input.md, menulis JSON, menjalankan scripts/hitung_hpp.py)
3 Permintaan malas: ✅ ("bikinin dong harga jual brownies aku, modalnya kira2 berapa ya" → bertanya sekali, 5 poin singkat + opsi jawab seingatnya)
4 Script: ✅ HPP Rp 6.950, harga Rp 11.000 (margin 36,8%), BEP 114 bungkus/≈Rp 1.245.000 — sama persis dengan examples/01
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara (tabel komponen + ringkasan + BEP + saran). Sedikit lebih ringkas: tanpa blok penjelasan margin vs markup & asumsi upah pemilik
Masalah: (1) Agent menyarankan "skill harga-jual-marketplace" yang tidak terpasang — sebaiknya SKILL.md menyebut skill lain hanya bila terpasang. (2) Uji 3 sempat mencoba path skill bawaan OpenClaw (file not found) sebelum path ~/.openclaw/skills — tidak berdampak.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
