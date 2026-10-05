# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (input persis examples/01: K/1, gaji 12 jt, THR Maret, iuran 360rb → `pph21.py setahun ...` persis sama dengan contoh)
3 Permintaan malas: ✅ ("bikinin dong itungan pph tukang harian 300rb sehari kerja 20 hari" → langsung jalan `pph21.py harian`, Rp 0, alasan batas Rp 450.000/hari)
4 Script: ✅ Jan–Feb & Apr–Nov Rp 360.000, Maret Rp 2.160.000, Desember Rp 642.000, setahun Rp 6.402.000 — sama persis dengan examples/01; tukang harian Rp 0 = examples/02
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara (tabel 12 bulan, hitung ulang Desember per lapisan, asumsi DTP, disclaimer + dasar aturan)
Masalah: Sama seperti temuan lama examples/01: catatan bahwa premi JKK/JKM/BPJS Kes perusahaan masuk bruto tidak muncul di output `setahun`; kalimat "pembulatan belum dicocokkan dengan Coretax" juga tidak disebut agent di jawaban akhir.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
