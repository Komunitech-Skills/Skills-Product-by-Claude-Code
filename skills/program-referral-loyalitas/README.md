# Program Referral & Loyalitas — pelanggan ajak teman, balik lagi, tetap untung

**Tagline:** Satu kalimat dari Anda, satu program "ajak teman" atau poin lengkap dengan angka hadiah yang aman.

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

## FAQ
1. **Apakah harus punya data penjualan?** Tidak wajib. Tanpa data, skill memakai default (margin 40-55% sesuai jenis usaha, beli 1x per bulan, 6 bulan) berlabel "asumsi" dan menjadikan pencatatan data sebagai tugas minggu pertama.
2. **Apakah skill mengirim pesan ke pelanggan saya?** Tidak. Skill menyiapkan teks; Anda mengirim sendiri satu per satu ke pelanggan yang sudah berhubungan dengan Anda. Tidak ada kirim massal otomatis.
3. **Apakah ini menjamin pelanggan akan mengajak teman?** Tidak. Skill membuat program yang aman secara hitungan dan aturan; hasil bergantung produk, layanan, dan momen ajakan. Uji dulu selama 30 hari.

## Skill pendamping
`hitung-hpp`, `strategi-harga-produk`, `promo-kalender`, `rencana-marketing-usaha`, `caption-sosmed-umkm`, `pesan-prospek-wa`, `crm-wa`, `kebijakan-privasi-pdp`, `pengingat-pasien-klinik`.

## Riwayat versi
- **1.0.2 (2026-09-30):** temuan uji ulang: kartu info klinik kini untuk pasien sendiri; klinik tidak meminta/mendorong pasien membagikannya (KODEKGI 2020 Pasal 3 butir 1.2.4 & Pasal 5, KODEKI Pasal 3). Tetap PERLU REVIEW tenaga medis/hukum.
- **1.0.1 (2026-09-30):** script menerima angka format Indonesia di semua isian (uang dan jumlah: `40.000`, `1.500.000`, `Rp38.000`, `38rb`, `1,5jt`, desimal koma `0,25`/`12,5`); angka yang bisa dibaca dua arah ditolak dengan pesan jelas, tidak ditebak. Fasilitas kesehatan: tidak lagi merancang hadiah/diskon untuk merujuk pasien (Permenkes 1787/2010 Pasal 5, kode etik profesi); diganti edukasi, pengingat kontrol, dan kartu info tanpa imbalan. Status `impas` tidak lagi "AMAN" bila pesanan pertama rugi (status `RUGI DI PESANAN PERTAMA`); batas hadiah pemberi diberi label BATAS ATAS (bukan anjuran) plus hadiah SARAN yang lebih konservatif. Tes regresi 26 -> 43.
- **1.0.0 (2026-09-30):** rilis awal.

## Asal-usul
Diadaptasi dan diperluas dari skill `referrals` (marketingskills, Corey Haines, lisensi MIT); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.
