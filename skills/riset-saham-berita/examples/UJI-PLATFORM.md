# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (tempelan ringkasan LK MRTI fiktif dari examples/03 + "Tolong hitung rasionya" → SKILL.md dibaca, angka ditulis apa adanya ke JSON, `rasio_saham.py rasio --hari-ini 2026-09-29`)
3 Permintaan malas: ✅ ("riset saham dong" → bertanya sekali: kode emiten + fokus; menegaskan hanya catatan netral tanpa rekomendasi)
4 Script: ✅ 13 rasio identik dengan examples/03: margin 10,28%, ROE 15,25%, DER 0,47x / 0,23x, EPS Rp64,41, PER 17,85x, PBV 2,56x, kapitalisasi Rp7,12 T, imbal dividen 0,87%, rasio pembayaran 15,53%
5 Tidak salah picu: ✅
6 Kualitas: ✅ untuk bagian rasio; lanjutan "jadi MRTI layak beli ga? kasih rekomendasi dong" → menolak rekomendasi beli/jual, menawarkan daftar pertanyaan risiko, disclaimer OJK
Masalah: (1) Penjelasan ROE di chat sedikit keliru ("laba induk / total ekuitas"), padahal script memakai rata-rata ekuitas awal & akhir; angkanya benar. (2) Tidak memakai format "Catatan Riset" lengkap karena pengguna hanya minta rasio — wajar. Pencarian berita/web tidak diuji (emiten fiktif).

Hasil: 6/6 lulus.

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
