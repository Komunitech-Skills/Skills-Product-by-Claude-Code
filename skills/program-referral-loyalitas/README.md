# Program Referral & Loyalitas yang Tetap Untung

**Satu kalimat dari Anda, satu program referral (pelanggan mengajak teman) atau program poin pelanggan setia, lengkap dengan angka hadiah yang masih menguntungkan.**

Diuji AI penguji independen di OpenClaw: 5,25 → 9,0 dari 10 (hitungan hadiah sudah benar di kedua sisi; pembedanya: klinik gigi yang minta diskon rujukan dan kirim ke 2.000 kontak, AI tanpa skill menjawab "udah bagus", dengan skill ditolak sesuai aturan iklan layanan kesehatan dan dialihkan ke kartu info serta pengingat yang dikirim staf satu per satu).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- **Hadiah dihitung dari margin (untung per penjualan), bukan dikira:** biaya per referral, titik impas (titik balik modal), batas hadiah yang disarankan, dan nilai poin dihitung skrip.
- **Tahu "utang poin" Anda:** nilai poin yang beredar dan belum ditukar pelanggan, serta biayanya per bulan, dihitung supaya tidak kaget.
- **Siap tempel:** syarat & ketentuan, teks ajakan WhatsApp/Instagram, kartu poin, lembar catatan.
- **Anti-curang untuk usaha kecil:** akun ganda, mengajak diri sendiri (self-referral), retur demi hadiah, tanpa aplikasi khusus.
- **Sopan dan sesuai aturan:** promo tidak menyesatkan, data pelanggan seminimal mungkin (UU PDP = Pelindungan Data Pribadi), tanpa blast (kirim massal), tanpa skema berjenjang (MLM).

## Cocok untuk siapa
Pemilik toko online, kafe/warung, jasa (laundry, bengkel, salon), reseller/dropship, dan usaha mapan yang ingin pelanggan lebih sering kembali dan membawa teman. Klinik/praktik kesehatan mendapat versi **tanpa imbalan untuk merujuk** (edukasi, pengingat kontrol, kartu info) sesuai aturan iklan pelayanan kesehatan (bagian ini belum direview tenaga medis/hukum, jadi mohon ditinjau dulu). Tidak butuh istilah teknis.

## Sebelum / sesudah
**Sebelum:** "Kasih diskon 50% buat yang ajak teman aja deh." (tidak dihitung; rugi di pesanan pertama, mudah dicurangi)

**Sesudah (cukup ketik):** "Toko hijab online saya di Shopee dan WA, pesanan rata-rata Rp180.000, untung kotor 40%. Mau program ajak teman, hadiahnya Rp15.000 untuk dua-duanya. Aman nggak? Pelanggan lama sekitar 300 orang, sekali beli kira-kira tiap 2 bulan. Biaya iklan sekarang Rp45.000 per pelanggan baru."

Cuplikan hitungan (contoh buatan pembuat skill, usaha fiktif; keluaran nyata skrip hitung, `examples/01-toko-hijab-referral.md`):
```
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp180.000  |  margin kotor 40%
Laba kotor pesanan pertama      : Rp72.000 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp15.000
Hadiah/diskon teman             : Rp15.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp30.000 = 16,67% dari nilai pesanan, 41,67% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp42.000
Anggaran Rp600.000 cukup untuk maksimal 20 referral berhasil.
Pembanding: biaya per pelanggan baru dari iklan Rp45.000 -> referral LEBIH MURAH (selisih Rp15.000).
```
Hasil lengkapnya juga memuat batas hadiah, aturan anti-curang, syarat & ketentuan (S&K), dan teks WA siap kirim.

## Cara pakai
Ketik contoh: *"Toko hijab online saya, pesanan rata-rata Rp180.000, untung kotor 40%. Mau program ajak teman, hadiah Rp15.000 untuk dua-duanya. Aman nggak?"* Skill akan bertanya sekali bila ada data yang kurang, lalu menyusun program lengkap. Jika Anda buru-buru, ia memakai asumsi yang disebut di awal jawaban.

## Instalasi singkat
Salin folder `program-referral-loyalitas` ke lokasi skill di platform Anda (OpenClaw, OpenAI Codex, Claude Code, Cursor). Lokasi lengkap dan langkah per platform: `docs/instalasi.md` di paket ini (di dalam paket bernama `CARA-INSTAL.md`). Skrip memakai Python standar (tanpa pemasangan paket); di Windows pakai `python` atau `py`. Skill tetap berguna bila skrip tidak bisa dijalankan (rumus cadangan ada di `references/rumus-dan-acuan.md`).

**Hasil uji (angka nyata):** uji OpenClaw sebelum/sesudah otomatis agent, 2026-10-02 (v1.0.4), skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Rata-rata 2 skenario: tanpa skill **5,25** → dengan skill **9,0** (LULUS): referral toko kue online + teks WA 6,5 → 9, dan jebakan klinik gigi (diskon rujukan + kirim massal ke 2.000 kontak) 4 → 9. Jujur: hitungan hadiah tanpa skill sudah benar; pembedanya aturan program, syarat & ketentuan, teks satu per satu (bukan blast), dan batas aturan klinik.
- Bot Telegram uji (bot OpenClaw asli di grup uji Komunitech), 3 Okt 2026: tanpa skill **5,5** → dengan skill **9** — hitungan biaya referral vs laba, kuota anggaran, anti-curang, teks WA satu-per-satu (bukan blast).

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan di bot Telegram uji. Claude Code, Codex, dan Cursor belum kami uji langsung. Bagian klinik: belum direview tenaga medis/hukum, tinjau dulu sebelum dipakai untuk promosi.

## FAQ
1. **Apakah harus punya data penjualan?** Tidak wajib. Tanpa data, skill memakai default (margin 40-55% sesuai jenis usaha, beli 1x per bulan, 6 bulan) berlabel "asumsi" dan menjadikan pencatatan data sebagai tugas minggu pertama.
2. **Apakah skill mengirim pesan ke pelanggan saya?** Tidak. Skill menyiapkan teks; Anda mengirim sendiri satu per satu ke pelanggan yang sudah berhubungan dengan Anda. Tidak ada kirim massal otomatis.
3. **Apakah ini menjamin pelanggan akan mengajak teman?** Tidak. Skill membuat program yang masih menguntungkan secara hitungan dan mengikuti aturan yang dirujuk; hasil bergantung produk, layanan, dan momen ajakan. Uji dulu selama 30 hari.

## Skill pendamping
Skill Komunitech lain yang bisa dipasangkan: `hitung-hpp` (modal per produk), `strategi-harga-produk` (menentukan harga jual), `promo-kalender` (rencana promo momen belanja), `rencana-marketing-usaha` (rencana pemasaran kuartalan/tahunan), `pesan-prospek-wa` (pesan ke calon pembeli), `crm-wa` (catatan pelanggan lewat WhatsApp), `kebijakan-privasi-pdp` (kebijakan privasi sesuai UU PDP), `pengingat-pasien-klinik` (draf pengingat kontrol pasien klinik).

## Asal-usul
Diadaptasi dan diperluas dari skill `referrals` (marketingskills, Corey Haines, lisensi MIT); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
