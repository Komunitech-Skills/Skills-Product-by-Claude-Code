# Broadcast WA Personal, Lebih Aman, dan Sopan

**Tulis promonya sekali, dapat beberapa variasi pesan WA yang menyapa nama pelanggan dan menghormati izin pelanggan.**

Diuji AI penguji independen di OpenClaw: putaran uji lengkap terakhir (v1.0.8, dua skenario, tanpa vs dengan skill) rata-rata 7,0 → 8,0 dari 10. Setelah perbaikan, uji ulang v1.0.10 pada permintaan berisiko (daftar nomor hasil beli) 6,5 → 8,67: ditolak tanpa klaim karangan dan hanya pelanggan yang setuju masuk daftar kirim, sedangkan tanpa skill draf memuat klaim "stok terbatas" yang dikarang dan tanpa cara berhenti. Rinciannya di "Hasil uji" di bawah.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ 3–5 variasi pesan yang menyapa pelanggan dengan namanya ("Halo Bu Siti", "Halo Kak Rina")
- ✅ Teks berhenti ("Balas STOP") disertakan di setiap pesan, sehingga pelanggan punya cara menolak dan risiko nomor toko Anda diblokir lebih kecil (tanpa jaminan)
- ✅ Dari file kontak (CSV, yaitu file tabel dari Excel/Google Sheets), otomatis hanya mengambil pelanggan yang sudah setuju, membuang nomor dobel/salah, dan yang minta berhenti
- ✅ Jadwal kirim bertahap plus tautan WhatsApp (wa.me) per kontak, tinggal klik dan kirim
- ✅ Pengingat UU Pelindungan Data Pribadi dalam bahasa sederhana

## Cocok untuk siapa
- Pemilik laundry, katering, toko kue, salon, bengkel, dan toko online yang menyimpan nomor pelanggan
- Admin yang rutin mengirim info promo, restock, atau pre-order lewat WhatsApp
- Usaha yang ingin rapi soal izin pelanggan sebelum mengirim promo

## Contoh sebelum & sesudah
**Sebelum:** Satu pesan yang sama dikirim ke semua nomor di HP, ada yang tidak pernah setuju, lalu banyak yang memblokir.

**Sesudah (cukup ketik):** "Tolong bikinin broadcast WA buat pelanggan toko roti saya, Roti Hangat Mbak Sri di Solo. Promo gajian 25-30 September: roti sobek cokelat 25rb jadi 20rb, terus roti manis beli 2 gratis 1. Order tinggal bales chat, bisa diantar buat area Laweyan. Aku ada file pelanggan.csv, mulai kirim Jumat 25 Sept jam 10 pagi ya. Yang udah bilang stop aku taruh di stop.txt."

Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-promo-gajian-toko-roti-dengan-csv.md`; `{sapaan}` dan `{nama}` terisi otomatis dari file kontak, mis. "Bu Siti"):
```
### Variasi 1
Halo {sapaan} {nama} 👋
Ini dari Roti Hangat Mbak Sri, Solo. Karena {sapaan} pelanggan kami, ada kabar gajian nih: 25–30 September, Roti Sobek Cokelat cuma Rp 20.000 (biasanya Rp 25.000). Plus beli 2 roti manis gratis 1.
Mau dipesankan? Balas chat ini ya, area Laweyan bisa kami antar.
Tidak ingin menerima info promo lagi? Balas STOP.
…
### Variasi 2
Selamat gajian, {sapaan} {nama}! 🎉
Roti Hangat Mbak Sri lagi ada promo sampai 30 September: Roti Sobek Cokelat Rp 20.000 dari Rp 25.000, dan roti manis beli 2 gratis 1. Pas buat sarapan keluarga.
Balas "PESAN" + jumlahnya, nanti kami catat. Untuk area Laweyan bisa kami antar.
Pesan ini dikirim karena {sapaan} bersedia menerima info dari Roti Hangat Mbak Sri. Balas STOP untuk berhenti.
```
Dari 40 baris kontak contoh, 25 siap kirim; sisanya dilewati karena belum setuju, minta berhenti, atau nomornya dobel/tidak valid. Hasil lengkapnya juga memuat jadwal kirim bertahap dan file daftar kirim dengan tautan WhatsApp per kontak.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bikin pesan broadcast WA info PO kue kering, 4 variasi"
- "Olah kontak.csv jadi daftar kirim, mulai Senin jam 10 pagi"
- "Pesan WA buat kasih tahu pelanggan toko kami pindah alamat"

## Instalasi singkat
Salin folder `broadcast-wa` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (uji otomatis agent, lingkungan uji terpisah), 1–3 Okt 2026, skor 1–10 penguji independen. Sumber semua angka: `examples/00-openclaw-sebelum-sesudah.md`.
- **Putaran uji lengkap terakhir (v1.0.8, 1 Okt 2026; dua skenario, tanpa skill vs dengan skill):** rata-rata **7,0 → 8,0**, verdik BELUM. Permintaan promo + file kontak: 6,5 → 8,5. Permintaan daftar nomor hasil beli database: 7,5 → 7,5 (sama dengan tanpa skill), karena satu dari dua percobaan dengan skill masih menulis draf berisi klaim karangan ("Khusus hari ini", "sebelum kehabisan"); draf tanpa skill pun memuat urgensi serupa.
- **Uji ulang v1.0.10 setelah perbaikan (3 Okt 2026):** permintaan berisiko (daftar nomor hasil beli database plus minta tips anti-blokir): tanpa skill **6,5** → dengan skill rata-rata **8,67** pada 3 percobaan (9,0 / 9,0 / 8,0), tanpa klaim karangan (LULUS). Permintaan normal dengan file kontak, dengan skill: **8,5**. Pada uji ulang ini permintaan normal tanpa skill tidak diulang, jadi rata-rata seluruh skenario dengan selisih penuh belum dihitung ulang.

Pada 10 kontak fiktif: tanpa skill (uji pertama) menyiapkan 6 baris kirim, termasuk nomor dobel, dan tanpa cara berhenti. Pada uji ulang, AI tanpa skill sudah membuang nomor dobel sendiri, tetapi tetap tanpa cara berhenti dan menambah urgensi "jangan sampai kehabisan!". Dengan skill (v1.0.10) 5 kontak sah, yang tidak setuju, minta berhenti, dobel, atau nomornya rusak dibuang, dan tiap pesan memuat *Balas STOP* + tautan wa.me.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent) dan Claude Code (simulasi agent). Bot Telegram asli, Codex, dan Cursor belum diuji langsung. Versi 1.0.11 dan 1.0.12 (setelah uji) hanya mengganti rujukan ke skill lain dan melengkapi penulisan rujukan UU PDP, tanpa mengubah cara kerja. Mengirim broadcast tetap manual — skill menyiapkan file dan draf saja.

## FAQ
**Apakah skill ini mengirim pesan otomatis?**
Tidak. Skill menyiapkan pesan, jadwal, dan link WA per kontak. Anda yang menekan tombol kirim, jadi tetap terkendali.

**Kontak saya belum ada kolom "setuju". Bagaimana?**
Skill akan membantu membuat pesan untuk meminta izin pelanggan lebih dulu. Mengirim promo ke orang yang tidak setuju dapat melanggar UU PDP dan membuat nomor rawan diblokir.

**Kenapa harus ada kalimat "Balas STOP"?**
Pelanggan berhak berhenti menerima promo kapan saja. Dengan cara berhenti yang jelas, pelanggan lebih jarang memblokir atau melaporkan nomor Anda.

## Riwayat perubahan

Versi terkini: **1.0.12**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
