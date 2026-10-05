# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (teks 8 produk pesaing kopi gayo ditempel — data sama dengan examples/01, termasuk 1/2 kg & 1 duplikat — agent menulis CSV dari template lalu menjalankan scripts/banding_harga.py)
3 Permintaan malas: ✅ ("cekin dong harga pasaran sambal botol 200ml, punyaku 35rb kemahalan ga" → bertanya sekali: minta teks/screenshot 5–8 listing + HPP + biaya marketplace; memberi kisaran kasar berlabel "bukan data live")
4 Script: ✅ median Rp 53.125, P25 Rp 49.375, P75 Rp 54.825, balik modal Rp 35.715, minimum Rp 46.297, titik Rp 53.125 (laba Rp 15.234), harga cantik Rp 52.900 (laba Rp 15.038), duplikat dibuang, 1/2 kg dibaca 500 g — semua sama dengan examples/01
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara (tabel pesaing, ringkasan pasar, batas harga, rekomendasi, promo, asumsi, saran)
Masalah: Uji 3 (tanpa link): agent atas inisiatif sendiri mencoba web_search, web_fetch halaman pencarian Tokopedia/Google, dan menyalakan browser (semua gagal/diblokir) sebelum bertanya. SKILL.md belum mengatur kasus "tidak ada link" — sarankan tambah aturan: tanpa link → langsung minta teks/screenshot, jangan mencari/menjelajah sendiri.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
