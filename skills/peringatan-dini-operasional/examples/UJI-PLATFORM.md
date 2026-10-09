# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("Ini log harian pabrik roti saya 30 hari terakhir, filenya log-produksi.csv ... Pemasok tepung biasanya kirim 2 hari ... Nama usaha: Roti Bu Ratna." — file = examples/log-roti-30hari.csv → `peringatan_dini.py --nama-usaha --lead-time 2 --format json`, laporan teks ditampilkan apa adanya)
3 Permintaan malas: ✅ ("cek dong usaha saya minggu ini ada yg aneh ga" → agent menemukan satu-satunya log di folder kerja dan langsung menjalankan script)
4 Script: ✅ 2 🔴 · 1 🟠 · 1 🟡 · 4 normal; % reject 3,08 (7,0σ), reject 63 pcs (6,8σ, +26% dari target 50), stok tepung 169 kg ±3,2 hari → mulai kurang Sab 3 Okt, penjualan Rp 8.644.500 turun 3 hari — identik dengan examples/01
5 Tidak salah picu: ✅
6 Kualitas: ✅ setara; analisis tambahan agent mengaitkan catatan "tepung merk baru" & "oven 2" dengan hati-hati (bukan kepastian)
Masalah: (1) Uji malas: agent tidak menyebut eksplisit file mana yang dipakai dan mengarang nama usaha "Usaha Roti" — sebaiknya asumsi disebut. (2) Tawaran jadwal menyebut "Telegram/WhatsApp", padahal SKILL.md menetapkan Telegram (WA hanya nomor terpisah + persetujuan risiko); jadwal tidak dibuat (tidak diminta), jadi tanpa dampak.

Hasil: 6/6 lulus.

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
