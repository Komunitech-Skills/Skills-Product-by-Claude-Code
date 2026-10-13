# Broadcast WA Personal, Aman, dan Sopan

**Tulis promonya sekali, dapat beberapa variasi pesan WA yang menyapa nama pelanggan dan patuh aturan.**

## Manfaat
- ✅ 3–5 variasi pesan yang menyapa pelanggan dengan namanya ("Halo Bu Siti", "Halo Kak Rina")
- ✅ Teks berhenti ("Balas STOP") selalu ada, jadi pelanggan tidak merasa terganggu dan nomor tokomu lebih aman
- ✅ Dari file kontak, otomatis hanya mengambil pelanggan yang sudah setuju, membuang nomor dobel/salah, dan yang minta berhenti
- ✅ Jadwal kirim bertahap plus link WA per kontak, tinggal klik dan kirim
- ✅ Pengingat UU Pelindungan Data Pribadi dalam bahasa sederhana

## Cocok untuk siapa
- Pemilik laundry, katering, toko kue, salon, bengkel, dan toko online yang menyimpan nomor pelanggan
- Admin yang rutin mengirim info promo, restock, atau pre-order lewat WhatsApp
- Usaha yang ingin rapi soal izin pelanggan sebelum mengirim promo

## Contoh sebelum & sesudah
**Sebelum:** Satu pesan yang sama dikirim ke semua nomor di HP, ada yang tidak pernah setuju, lalu banyak yang memblokir.

**Sesudah (cukup ketik):** "Buatin broadcast WA promo gajian laundry, cuci setrika 8 ribu jadi 7 ribu per kilo, ini file pelanggan.csv"
→ 3 variasi pesan dengan nama pelanggan, saran jam kirim, dan file `broadcast_siap.csv` berisi hanya pelanggan yang setuju, lengkap dengan jadwal dan link WA.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Bikin pesan broadcast WA info PO kue kering, 4 variasi"
- "Olah kontak.csv jadi daftar kirim, mulai Senin jam 10 pagi"
- "Pesan WA buat kasih tahu pelanggan toko kami pindah alamat"

## Instalasi singkat
Salin folder `broadcast-wa` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap per platform (termasuk Windows): lihat `docs/instalasi.md` dan `CARA-INSTAL.md` di paket.

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1–3 Okt 2026 (v1.0.10), skor 1–10 penguji independen: tanpa skill **6,5** → dengan skill **8,67** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`, `promosi/sebelum-sesudah.jsonl`. Dari 10 kontak fiktif, tanpa skill menyiapkan 6 pesan (termasuk nomor dobel, tanpa cara berhenti); dengan skill 5 kontak sah, opt-out/duplikat/nomor rusak dibuang, tiap pesan ada *Balas STOP* + link wa.me.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent) dan bot Telegram uji (gelombang tampilan). Codex/Cursor belum uji platform asli. Mengirim broadcast tetap manual — skill menyiapkan file dan draf saja.

## FAQ
**Apakah skill ini mengirim pesan otomatis?**
Tidak. Skill menyiapkan pesan, jadwal, dan link WA per kontak. Kamu yang menekan tombol kirim, jadi tetap aman dan terkendali.

**Kontak saya belum ada kolom "setuju". Bagaimana?**
Skill akan membantu membuat pesan untuk meminta izin pelanggan lebih dulu. Mengirim promo ke orang yang tidak setuju melanggar UU PDP dan membuat nomor rawan diblokir.

**Kenapa harus ada kalimat "Balas STOP"?**
Pelanggan berhak berhenti menerima promo kapan saja. Dengan cara berhenti yang jelas, pelanggan lebih jarang memblokir atau melaporkan nomormu.

## Catatan revisi 1.0.10 (2026-10-03)
- ATURAN WAJIB baru: draf teks pada jalur penolakan (tanpa file kontak) juga wajib lolos `cek_fakta.py`; klaim/urgensi karangan ("Hari ini ada promo", "Khusus hari ini", "sebelum kehabisan") dilarang.
- `cek_fakta.py` menambah deteksi "hari ini ada promo", "promo hari ini", "mumpung promo"; tes regresi ditambah.

## Catatan revisi 1.0.9 (2026-10-01)
- Cek fakta kini **otomatis di dalam perintah utama** (`siapkan_broadcast.py`) dan tidak bisa dilewati: klaim yang tidak disebut pemilik ("Khusus hari ini", "sebelum kehabisan", "promo terakhir", "buruan", "jangan sampai ketinggalan", "waktu terbatas", "stok terbatas", dst.) membuat script **GAGAL** dan tidak menghasilkan file siap kirim, dengan atau tanpa `--fakta-file`.
- Daftar frasa urgensi di `cek_fakta.py` diperluas; tes regresi ditambah.

## Catatan revisi 1.0.8 (2026-10-01)
- Kolom **Sapaan/Panggilan** di file kontak kini dipakai ("Bu Siti", "Pak Fajar"), tidak lagi diganti "Kak".
- Versi daftar siaran (tanpa nama) dipisah jelas dan ditolak bila masuk ke daftar kirim personal.
- Pemeriksaan anti-karang: klaim seperti "stok terbatas", "terlaris", "halal" ditolak bila tidak disebut pemilik (`--fakta-file`).
- Kolom "Setuju Promo" dikenali otomatis sebagai kolom persetujuan.
