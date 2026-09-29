# Uji Platform Asli

## OpenClaw 2026.9.6 — 2026-09-29 — uji otomatis oleh agent (model: komunitech via router, env bersih)
OS: Linux
1 Terpasang: ✅ (✓ ready; eligible, modelVisible, commandVisible)
2 Terpicu otomatis: ✅ (prompt examples/01, 3 karyawan, UMK 5.396.761, JKK 0,54%, lembur hari kerja & Minggu → CSV, `payroll.py --umk --jkk 0,54 --hari-kerja 5`, slip MD/HTML + rekap CSV)
3 Permintaan malas: ✅ ("bikinin dong slip gaji rina, gaji 6jt, tk0" → bertanya sekali soal periode sambil menyebut default: September 2026, tanpa tunjangan, JKK 0,24%)
4 Script: ✅ identik examples/01: THP Budi Rp 6.521.091, Siti Rp 5.264.239, Dewi Rp 10.521.618; total THP Rp 22.306.948; biaya perusahaan Rp 26.184.076; setor BPJS Kesehatan Rp 1.069.838, BPJS TK Rp 2.012.940, PPh 21 Rp 444.350; peringatan Siti di bawah UMK
5 Tidak salah picu: ✅
6 Kualitas: ✅ setara
Masalah: Data gaji (CSV input + slip) ditulis dulu ke `/tmp/payroll-input/` dan tertinggal di sana; hanya hasil yang disalin ke folder kerja. Data gaji sensitif — sebaiknya SKILL.md menyuruh menulis CSV input & output di folder kerja pengguna, bukan /tmp.

Hasil: 6/6 lulus.

Catatan jujur: uji otomatis oleh agent dengan model via router, bukan manusia di aplikasi OpenClaw (chat/Telegram) sungguhan; setiap pesan dijalankan sebagai giliran CLI terpisah (`openclaw agent --local --session-id <sesi> -m "..." --json`). Telegram tidak diuji.

Cara uji: paket `build.py --pembeli "UJI INTERNAL" --izinkan-draft` (dibangun dari salinan bersih HEAD; riset-saham-berita dari paket `--vip` karena eksklusif VIP) diekstrak lalu dipasang `openclaw skills install ./<skill> --global` ke HOME sementara (10 skill gelombang ini terpasang bersama). Setiap proses openclaw dijalankan dengan `env -i` (hanya HOME, PATH, LANG, TZ, proxy lokal + CA, dan kunci router); sebelum uji, `env` di shell agent diperiksa: tidak ada token/kredensial selain kunci router. Provider OpenAI-compatible kustom (`api: openai-completions`, model `komunitech` = claude-sonnet-5). Data usaha fiktif. Pemakaian skill dilihat dari transkrip (agent membaca `~/.openclaw/skills/<skill>/SKILL.md` lalu menjalankan script). Uji 5 = tiga permintaan tak berkaitan di sesi baru ("resep nasi goreng kampung dong", "rekomendasi tempat wisata keluarga di Bandung", "caption IG promo diskon 20% toko kue"): tidak ada SKILL.md yang dibaca. Transkrip & sesi OpenClaw dihapus setelah uji.
