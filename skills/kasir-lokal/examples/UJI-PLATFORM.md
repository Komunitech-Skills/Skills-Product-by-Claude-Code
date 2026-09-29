# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("pakai kasir buat kedai saya ya ... ini menunya" + produk.csv dari examples/01 (BOM, `;`, CRLF) → agent bertanya sekali soal PBJT/stok/zona, pratinjau init → ya → pratinjau impor 15 produk → ya → buka kasir → 3 nota → struk 58 mm → tutup kasir → rekap; semua lewat scripts/kasir.py)
3 Permintaan malas: ✅ ("catet dong es teh 2 sama roti bakar, qris" → script menolak ambigu, agent bertanya sekali Es Teh Manis/Lemon & Roti Bakar Coklat/Keju)
4 Script: ✅ N-0001 Rp 53.000 kembali Rp 47.000; diskon 10%+5% → −Rp 2.610, total Rp 28.890; diskon item 2rb + nota 10% → Rp 55.800 kembali Rp 4.200 (sama dengan examples/01); tutup kasir seharusnya Rp 337.690, fisik 337.000 → kurang Rp 690; rekap bersih Rp 137.690, diskon Rp 10.810 (dicek manual)
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara untuk alur yang diuji (versi ringkas examples/01: tanpa void/retur/dobel ketik)
Masalah: (1) Saat menampilkan struk di chat, agent membuang baris qty×harga per item (file HTML struk dari script lengkap & benar). (2) Agent menjalankan `find / -maxdepth 6 -iname produk.csv` untuk mencari file — berlebihan, sebaiknya cek folder kerja dulu. (3) Sempat melanjutkan transaksi saat buka-kasir belum dikonfirmasi, tapi agent sendiri memperingatkan dan minta konfirmasi — baik.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
