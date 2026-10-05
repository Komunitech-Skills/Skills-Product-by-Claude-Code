# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (prompt examples/01 paket telat JNE → SKILL.md dibaca; balasan siap kirim + catatan admin)
3 Permintaan malas: ✅ ("balesin chat pelanggan dong" → bertanya sekali: isi chat + platform; SKILL.md belum dibaca di giliran ini)
4 Script: — (skill tanpa script)
5 Tidak salah picu: ✅
6 Kualitas: ✅ setara examples/01: resi & status transit disebut, tidak menjanjikan pasti sampai, janji kabar dengan jam (placeholder `[isi jam kerja, mis. 17.00]`, examples/01 langsung 16.00), catatan admin lebih lengkap (siapkan opsi refund/kirim ulang). Tidak ada "alternatif lebih singkat".
Masalah: Tidak ada yang berarti.

Hasil: 5/5 lulus (nomor 4 tidak berlaku).

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
