# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech → claude-sonnet-5 via router)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("Mulai pakai aplikasi gaji ya ..." + 4 karyawan dari examples/01 (Andi, Budi, Citra, Indah) + bonus/kasbon/lembur → pratinjau → ya → hitung → "Kunci gaji September, buatkan slip dan file transfernya" → final, 4 slip + CSV transfer)
3 Permintaan malas: ✅ ("ada karyawan baru nih, dewi, gajinya 4,5jt. masukin ya" → bertanya sekali: PTKP & tanggal masuk, menawarkan default)
4 Script: ✅ Andi PPh 21 Rp 79.767 / bersih Rp 7.050.233 / biaya Rp 8.361.450; Budi bersih Rp 3.826.032; Citra PPh Rp 543.568 / bersih Rp 11.965.569; Indah lembur Rp 280.925 / bersih Rp 5.464.925 — sama persis dengan baris K01/K02/K03/K09 examples/01
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara (rekap, setoran BPJS/PPh, peringatan UMK, disclaimer dasar aturan + Coretax)
Masalah: (1) Agent mengira `atur` butuh `--ya` (error argparse), lalu memperbaiki sendiri; akibatnya `atur` sempat tersimpan saat "pratinjau" sebelum pengguna setuju — di SKILL.md/perintah.md sebaiknya ditegaskan `atur` langsung tersimpan. (2) File transfer kosong karena rekening belum diisi — dijelaskan dengan baik. (3) Uji 3: default "5 hari kerja" padahal usaha memakai 6 hari.

Hasil: 6/6 lulus. Catatan jujur: ini uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah dalam sesi yang sama.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` diekstrak lalu dipasang dengan `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill beta gelombang 1 terpasang bersama). Agent dijalankan non-interaktif `openclaw agent --local --session-id <sesi> -m "..." --json` (provider OpenAI-compatible kustom `models.providers`, `api: openai-completions`, model `komunitech` = claude-sonnet-5). Onboarding BOOTSTRAP.md dianggap selesai. Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = dua permintaan tak berkaitan ("resep nasi goreng kampung", "caption IG promo diskon toko kue") dengan ke-10 skill terpasang: tidak ada SKILL.md yang dibaca.
