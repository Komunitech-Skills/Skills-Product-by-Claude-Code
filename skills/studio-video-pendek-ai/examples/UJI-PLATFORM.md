# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("Bikinin video 15 detik promo laundry kiloan Laundry Bersih Jaya, Rp6.500/kg, pesan lewat WA." → 7 bagian sesuai SKILL.md: hook, naskah & timing, storyboard jalur A (HP) / B (prompt AI), sulih suara final, caption, checklist label AI, langkah produksi)
3 Permintaan malas: ✅ ("bikinin video tiktok dong buat jualan" → bertanya sekali, 5 poin singkat)
4 Script: ✅ `durasi_naskah.py --target 15` → 10,7 dtk PAS (dicek manual: 24 kata / 150 × 60 = 9,6 + jeda 0,5 + 2 × 0,3 = 10,7)
5 Tidak salah picu: ✅
6 Kualitas: ✅ setara examples/01 (harga dari pengguna, lama pengerjaan tidak dikarang, unggah manual, label AI)
Masalah: (1) **Pencarian file berlebihan:** agent menjalankan `find / -iname durasi_naskah.py`, lalu membaca & menjalankan script dari folder lain di luar instalasi OpenClaw (repo kurator) — path `scripts/durasi_naskah.py` di SKILL.md langkah 5 tidak di-resolve ke folder skill. Saran: tulis `python3 <folder-skill-ini>/scripts/durasi_naskah.py` seperti skill lain. (2) Naskah menambah klaim umum "bersih, wangi" yang tidak diberikan pengguna (risiko rendah).

Hasil: 6/6 lulus (dengan catatan path script).

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
