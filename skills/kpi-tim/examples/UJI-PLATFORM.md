# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (`openclaw skills list`: ✓ ready, openclaw-managed; `skills check`: eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("Toko saya 5 orang: Wulan & Rudi kasir, Fajar gudang, Nadia admin online (balas chat), Bayu iklan/medsos. Bikinin KPI bulanan di Excel ya." → SKILL.md + katalog + aturan-skor dibaca, `skor_kpi.py template` → 20 KPI, rencana-kpi.xlsx + realisasi-2026-10.csv, `cek` ✅; asumsi disebut: target contoh katalog, periode 2026-10)
3 Permintaan malas: ✅ ("bikinin kpi dong buat tim sales saya" → menampilkan 4 KPI sales bawaan lalu bertanya sekali: nama tim wajib, sisanya boleh default)
4 Script: ✅ skor Bayu September 112,4 (36,0 + 30,0 + 27,5 + 18,9; leads dibatasi 120%) — sama dengan examples/01 dan hitung tangan
5 Tidak salah picu: ✅ (lihat cara uji)
6 Kualitas: ✅ setara untuk alur yang diuji (tanpa realisasi format campur / baca teks grup WA)
Masalah: (1) File rencana disimpan di `~/workspace/kpi-toko/` (folder baru di HOME), bukan folder kerja OpenClaw `~/.openclaw/workspace` — pembeli bisa bingung mencari file; sebaiknya SKILL.md menyebut "simpan di folder kerja". (2) Untuk skor Bayu, agent membuat rencana terpisah (target 250) di samping rencana Oktober (target 300) — agent sendiri menandai bedanya dan bertanya, baik.

Hasil: 6/6 lulus.

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
