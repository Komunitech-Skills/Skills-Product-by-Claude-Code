# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (prompt examples/01: Budi/Rina/Joko harian/Wati PHK → CSV, `thr.py --hari-raya 2027-03-10 --nama-hari-raya "Idul Fitri 1448 H" --data ... --hari-ini 2026-09-29` + draf pengumuman)
3 Permintaan malas: ✅ (prompt examples/02 → langsung jalan, PTKP kosong disebut sebagai asumsi, menawarkan hitung PPh 21)
4 Script: ✅ identik examples/01: THR total Rp 16.908.333, PPh 21 Rp 666.500, diterima Rp 16.241.833 (Joko rata-rata 12 bln Rp 3.008.333; Wati PHK 18 hari sebelum hari raya tetap berhak, tarif Pasal 17); examples/02: 7/12 × Rp 4.500.000 = Rp 2.625.000, batas bayar H-7 Rabu 3 Maret 2027
5 Tidak salah picu: ✅
6 Kualitas: ✅ setara
Masalah: CSV karyawan & rekap ditulis ke `/tmp/` (di luar folder kerja, tertinggal). Di akhir agent menawarkan "kirim rekap via WA/email ke HR" padahal kanal tidak dikonfigurasi (hanya tawaran, tidak dijalankan).

Hasil: 6/6 lulus.

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
