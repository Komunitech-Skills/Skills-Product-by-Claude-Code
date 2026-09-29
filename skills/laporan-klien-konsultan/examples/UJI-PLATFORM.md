# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("Catat kerjaan saya buat PT Maju Jaya ya: ..." 3 pekerjaan seperti examples/01 → 3× `laporan_klien.py catat`; "Buatkan laporan mingguan untuk PT Maju Jaya" → `laporan`)
3 Permintaan malas: ✅ ("td abis revisi logo buat kopi senja 3 jam, catet ya" → langsung dicatat, proyek/status/tanggal diasumsikan dan disebut)
4 Script: ✅ total 4 jam dari 3 entri (entri tanpa jam tidak dijumlah) — sama dengan examples/01
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara (versi WA ditampilkan, versi email/markdown ditawarkan; ringkasan, butuh dari klien, rencana)
Masalah: (1) Kendala "menunggu data laba rugi Q3" dicatat sebagai `--butuh-klien`, bukan `--kendala`, sehingga bagian Terkendala tanpa alasan. (2) Periode kustom membuat subjek email berlabel "Periode kustom" — agent sendiri menyarankan pakai preset mingguan.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
