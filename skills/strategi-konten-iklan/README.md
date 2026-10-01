# Strategi Konten & Anggaran Iklan - konten jelas, uang iklan tidak bocor

**Tagline:** Satu kalimat dari Anda: pilar konten yang tepat sasaran plus pembagian anggaran iklan per kanal per minggu, lengkap dengan batas impas yang dihitung, bukan dikira.

## Manfaat
- **Tahu harus posting apa:** 3-5 pilar konten dari pertanyaan dan keberatan pembeli Anda sendiri, lengkap 5 judul contoh per pilar.
- **Anggaran terbagi jelas:** Meta/Instagram, TikTok, Shopee Ads, TikTok Shop Ads, Google Ads, per minggu, dengan porsi uji 30%.
- **Tahu batas rugi:** titik impas ROAS (1 per margin), CPA maksimal, dan jumlah pesanan minimal agar anggaran bulan itu impas, dihitung script.
- **Anggaran kecil tetap masuk akal:** Rp500rb sampai Rp20jt per bulan; script menyingkirkan kanal yang uangnya terlalu tipis untuk diuji.
- **Aman dan jujur:** tanpa janji hasil, dengan catatan aturan iklan untuk kesehatan, keuangan, kripto.

## Cocok untuk siapa
Pemilik toko online, kafe, jasa lokal, reseller, dan admin sosmed yang mulai atau ingin merapikan iklan berbayar dan bingung membagi uang ke banyak kanal.

## Sebelum / sesudah
**Sebelum:** "Rp5 juta ya saya taruh semua di boost postingan IG." Tidak tahu hasil minimal, tidak ada bagian untuk uji, pesanan dari Shopee tidak terlayani.
**Sesudah:** untuk kaos Rp150.000 margin 40% yang pesanannya kebanyakan lewat Shopee: Shopee Ads Rp3.333.333 (kanal utama) dan Meta Rp1.666.667 (per minggu terperinci), ROAS impas 2,50x, target aman 3,58x, CPA maksimal Rp42.000, minimal 84 pesanan agar impas, plus 4 pilar konten dan aturan keputusan mingguan. Lihat `examples/01-toko-kaos-shopee-ig.md`.

## Cara pakai
Ketik: *"Anggaran iklan saya Rp5 juta sebulan, harga rata-rata Rp150.000, margin 40%, saya punya Shopee dan IG. Bagi anggarannya dan bikin strategi kontennya."* Bila ada info kurang, skill bertanya sekali. Angka boleh gaya Indonesia: `1.500.000`, `1,5jt`, `500rb`. Angka yang bisa berarti dua hal (mis. `1,500`) akan ditanyakan ulang, tidak ditebak.

Bagian hitung juga bisa dijalankan sendiri (Windows: `python` atau `py`):
`python3 scripts/alokasi_anggaran.py --anggaran 5jt --aov 150rb --margin 40% --kanal meta,shopee --kanal-utama shopee`

## Instalasi singkat
Salin folder `strategi-konten-iklan` ke lokasi skill di platform Anda (OpenClaw, OpenAI Codex, Claude Code, Cursor). Lokasi lengkap dan langkah per platform ada di `docs/instalasi.md` pada paket Anda.

## FAQ
1. **Apakah skill ini menjalankan iklan saya?** Tidak. Skill merencanakan dan menghitung; Anda yang membuat dan menayangkan iklan. Jangan pernah membagikan password atau kode OTP akun iklan.
2. **Apakah ada jaminan penjualan atau ROAS tertentu?** Tidak. Yang dihitung hanya batas impas dan pembagian uang; hasil bergantung produk, harga, kreatif, dan persaingan.
3. **Apa bedanya dengan skill rencana marketing, kalender konten, dan laporan iklan?** Rencana marketing (`rencana-marketing-usaha`) menyusun rencana menyeluruh 1-12 bulan; kalender konten menjadwalkan posting harian; laporan iklan membaca hasil iklan yang sudah tayang. Skill ini di tengahnya: pilar konten dan anggaran iklan bulanan.

## Skill pendamping
`rencana-marketing-usaha`, `kalender-konten-30hari`, `laporan-iklan-mingguan`, `caption-sosmed-umkm`, `hitung-hpp`, `strategi-harga-produk`

## Riwayat versi
- **Catatan revisi 1.0.3 (2026-10-01):** (1) kanal penjualan utama: `--kanal-utama` (otomatis Shopee/TikTok Shop bila `--jenis marketplace`) membuat porsi kanal tempat pembeli bertransaksi 2x kanal pendukung terbesar, sehingga penjual Shopee tidak lagi mendapat porsi Meta terbesar; skill menanyakan "penjualan paling banyak dari mana?"; (2) nama momen wajib dari tabel referensi: Harbolnas = 12.12, 11.11 bukan Harbolnas; (3) larangan menulis "dihitung pakai script" kecuali script benar-benar dijalankan pada giliran itu; script wajib dijalankan tiap kali angka anggaran disusun/berubah; (4) tes regresi kanal utama ditambahkan.
- **1.0.1 (2026-09-30):** saringan kanal konsisten (dasar minggu terkecil; tidak ada "0 - DI BAWAH BATAS" tanpa catatan); saat uang tipis kanal yang paling cocok dipertahankan (`--jenis marketplace|jasa-lokal`); tujuan campuran (`--tujuan awareness:30,penjualan:70`); peringatan margin tipis/negatif; kata kunci kategori lebih lengkap (skincare, suplemen, klinik, pinjaman, dll.); alias kanal (ig, fb, tiktok shop, tokopedia) dan format `Rp 3.000.000,-`; panduan retargeting singkat; pembeda tegas dengan `rencana-marketing-usaha`.
- **1.0.0 (2026-09-30):** rilis awal.

## Asal-usul
Diadaptasi dan diperluas dari skill `content-strategy` dan `ads` (marketingskills, Corey Haines, lisensi MIT); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber. Nama platform hanya sebagai penyebut kanal.
