# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ ("Penjualan 2026.xlsx" dari examples/buat_fixture_uji.py + "Kategori apa paling laku, tren per bulan gimana, dan Q2 vs Q3 naik atau turun?" → `analisis.py profil/daftar/pivot/tren/banding --sheet semua`)
3 Permintaan malas: ✅ ("rapikan data excel saya dong" → agent mencari *.xlsx/*.csv di folder kerja, memakai satu-satunya xlsx dan menyebut namanya, `bersihkan` → `Penjualan 2026-bersih.csv`; file asli tidak diubah)
4 Script: ✅ Q2 Rp 97.112.500 (171 baris) vs Q3 Rp 69.130.500 → turun 28,8%; total Jan–Sep Rp 233.556.000, Semen Rp 105.444.000 tertinggi; puncak Apr Rp 34.340.000, terendah Jul Rp 17.476.000 — sama dengan examples/01. Baris TOTAL tiap sheet dikeluarkan, sheet tersembunyi tidak ikut, selisih Rp 680.000 SUM Excel Q1 (sel teks) dijelaskan
5 Tidak salah picu: ✅
6 Kualitas: ✅ setara
Masalah: (1) Uji malas: langsung menulis file baru tanpa konfirmasi (tidak menimpa file asli). (2) Agent menilai sendiri 3 sel rumus tanpa nilai "tidak berpengaruh signifikan" — sebaiknya tetap minta pengguna menyimpan ulang file seperti saran script.

Hasil: 6/6 lulus.

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
