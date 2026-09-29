# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (prompt examples/01 → `hitung_telat.py --tanggal 2026-09-29 --sudah-diingatkan 2` → tahap 5, template tahap 5 dibaca; WA pengantar + surat email resmi + tahap berikutnya + saran + catatan hukum)
3 Permintaan malas: ✅ ("tagihin dong pelanggan yg telat bayar" → akhirnya bertanya sekali, 5 poin) — lihat masalah (1)
4 Script: ✅ terlambat 24 hari (5 → 29 Sep), tahap 5, tanpa denda, total Rp 6.300.000 (examples/01: 18 hari per 23 Sep — beda hanya tanggal uji; dicek manual)
5 Tidak salah picu: ✅
6 Kualitas: ✅ setara examples/01 (nada naik tapi sopan, tawaran cicilan tertulis, tenggat 6 Okt)
Masalah: (1) **Perilaku bermasalah di uji malas:** sebelum bertanya, agent menjelajah folder kerja — membaca JSON invoice & kuitansi, file HTML, log produksi, grep seluruh folder, memory_search — dan **menjalankan `pip install openpyxl` tanpa izin** untuk membuka file Excel yang tidak berkaitan (paket sudah dihapus lagi oleh penguji). Saran: tambahkan di SKILL.md "Jika data tagihan tidak diberikan, tanyakan; jangan mencari/membuka file lain dan jangan menginstal paket."

Hasil: 6/6 menurut checklist, dengan temuan perilaku (1) yang perlu diperbaiki di SKILL.md.

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
