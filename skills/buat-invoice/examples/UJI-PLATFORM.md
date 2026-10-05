# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (prompt examples/01 → JSON di folder kerja, `buat_invoice.py --html --nomor-terakhir`)
3 Permintaan malas: ✅ (prompt examples/02 kuitansi pelunasan 7,5 jt → langsung jalan: KWT/2026/09/0001 LUNAS, terbilang benar, meterai; nomor default disebut)
4 Script: ✅ subtotal Rp 19.380.000, total Rp 19.530.000, DP −Rp 6.000.000, sisa Rp 13.530.000, terbilang benar, meterai (penerimaan > Rp5 juta) — sama dengan examples/01
5 Tidak salah picu: ✅
6 Kualitas: ❌ **nomor invoice salah**: pengguna menulis "Nomor terakhir INV/2026/09/0012", tetapi agent memberi `--nomor-terakhir INV/2026/09/0011` → invoice bernomor INV/2026/09/0012 (dobel dengan nomor yang sudah ada), dan agent menulis "lanjut dari 0011". examples/01 benar 0013.
Masalah: (1) Nomor dobel di atas — kesalahan agent (SKILL.md sudah jelas), tetapi berdampak ke dokumen resmi. Saran: SKILL.md minta nomor terakhir disalin persis dari pesan pengguna lalu dicek "nomor baru = terakhir + 1" sebelum ditampilkan; atau script mencetak "Nomor terakhir dibaca: X → nomor baru: Y". (2) Uji malas: kota "Jakarta" dan penanda tangan "Rina" dikarang tanpa disebut sebagai asumsi.

Hasil: 5/6 (nomor 1, 2, 4 lulus; perlu perbaikan kecil pada instruksi penomoran).

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
