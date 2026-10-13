# Program Referral & Loyalitas — pelanggan ajak teman, balik lagi, tetap untung

**Tagline:** Satu kalimat dari Anda, satu program "ajak teman" atau poin lengkap dengan angka hadiah yang aman.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- **Hadiah dihitung dari margin, bukan dikira:** biaya per referral, titik impas, batas hadiah aman, dan nilai poin dihitung script.
- **Tahu "utang poin" Anda:** liability poin yang beredar dan biaya per bulan dihitung, supaya tidak kaget.
- **Siap tempel:** syarat & ketentuan, teks ajakan WhatsApp/Instagram, kartu poin, lembar catatan.
- **Anti-curang untuk usaha kecil:** akun ganda, self-referral, retur demi hadiah, tanpa aplikasi khusus.
- **Aman dan sopan:** promo tidak menyesatkan, data pelanggan seminimal mungkin (UU PDP), tanpa blast, tanpa skema berjenjang.

## Cocok untuk siapa
Pemilik toko online, kafe/warung, jasa (laundry, bengkel, salon), reseller/dropship, dan usaha mapan yang ingin pelanggan lebih sering kembali dan membawa teman. Klinik/praktik kesehatan mendapat versi **tanpa imbalan untuk merujuk** (edukasi, pengingat kontrol, kartu info) sesuai aturan iklan pelayanan kesehatan (PERLU REVIEW tenaga medis/hukum). Tidak butuh istilah teknis.

## Sebelum / sesudah
**Sebelum:** "Kasih diskon 50% buat yang ajak teman aja deh." (tidak dihitung; rugi di pesanan pertama, mudah dicurangi)
**Sesudah:** referral dua sisi Rp15.000 + Rp15.000 untuk toko hijab dengan pesanan Rp180.000 dan margin 40%: biaya per referral Rp30.000, laba pesanan pertama tetap Rp42.000, lebih murah dari iklan Rp45.000, kuota 20 per bulan, S&K dan teks WA siap kirim. Lihat `examples/01-toko-hijab-referral.md`.

## Cara pakai
Ketik contoh: *"Toko hijab online saya, pesanan rata-rata Rp180.000, untung kotor 40%. Mau program ajak teman, hadiah Rp15.000 untuk dua-duanya. Aman nggak?"* Skill akan bertanya sekali bila ada data yang kurang, lalu menyusun program lengkap. Jika Anda buru-buru, ia memakai asumsi yang disebut di awal jawaban.

## Instalasi singkat
Salin folder `program-referral-loyalitas` ke lokasi skill di platform Anda (OpenClaw, OpenAI Codex, Claude Code, Cursor). Lokasi lengkap dan langkah per platform: `docs/instalasi.md` di paket ini. Script memakai Python standar (tanpa pemasangan paket); di Windows pakai `python` atau `py`. Skill tetap berguna bila script tidak bisa dijalankan (rumus cadangan ada di `references/rumus-dan-acuan.md`).

**Hasil uji (angka nyata):** uji OpenClaw sebelum/sesudah otomatis agent, 2026-10-02 (v1.0.4+), skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Rata-rata 2 skenario: tanpa skill **5,25** → dengan skill **9,0** (LULUS).
- Bot Telegram asli (gelombang 5, 2026-10-03): tanpa skill **5,5** → dengan skill **9** — hitungan biaya referral vs laba, kuota anggaran, anti-curang, teks WA satu-per-satu (bukan blast).

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent + bot Telegram gelombang 5). Claude Code, Codex, dan Cursor belum kami uji langsung. Bagian klinik: PERLU REVIEW tenaga medis/hukum sebelum promosi.

## FAQ
1. **Apakah harus punya data penjualan?** Tidak wajib. Tanpa data, skill memakai default (margin 40-55% sesuai jenis usaha, beli 1x per bulan, 6 bulan) berlabel "asumsi" dan menjadikan pencatatan data sebagai tugas minggu pertama.
2. **Apakah skill mengirim pesan ke pelanggan saya?** Tidak. Skill menyiapkan teks; Anda mengirim sendiri satu per satu ke pelanggan yang sudah berhubungan dengan Anda. Tidak ada kirim massal otomatis.
3. **Apakah ini menjamin pelanggan akan mengajak teman?** Tidak. Skill membuat program yang aman secara hitungan dan aturan; hasil bergantung produk, layanan, dan momen ajakan. Uji dulu selama 30 hari.

## Skill pendamping
`hitung-hpp`, `strategi-harga-produk`, `promo-kalender`, `rencana-marketing-usaha`, `caption-sosmed-umkm`, `pesan-prospek-wa`, `crm-wa`, `kebijakan-privasi-pdp`, `pengingat-pasien-klinik`.

## Asal-usul
Diadaptasi dan diperluas dari skill `referrals` (marketingskills, Corey Haines, lisensi MIT); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
