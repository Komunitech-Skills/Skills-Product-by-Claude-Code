# Strategi Konten & Anggaran Iklan - konten jelas, uang iklan tidak bocor

**Satu kalimat dari Anda: pilar konten (tema besar konten) yang tepat sasaran plus pembagian anggaran iklan per kanal per minggu, lengkap dengan batas impas yang dihitung, bukan dikira.**

Diuji AI penguji independen di OpenClaw: 6,75 → 8,5 dari 10 (tanpa skill AI sudah menolak janji hasil iklan; pembedanya angka lengkap yang konsisten: biaya iklan maksimal per pesanan, jumlah pesanan impas, dan batas iklan aktif).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- **Tahu harus posting apa:** 3-5 pilar konten dari pertanyaan dan keberatan pembeli Anda sendiri, lengkap 5 judul contoh per pilar.
- **Anggaran terbagi jelas:** Meta/Instagram, TikTok, Shopee Ads, TikTok Shop Ads, Google Ads, per minggu, dengan porsi uji 30%.
- **Tahu batas rugi:** titik impas ROAS (omzet iklan dibanding biaya iklan; 1 per margin), CPA maksimal (biaya iklan per pesanan), dan jumlah pesanan minimal agar anggaran bulan itu impas, dihitung skrip.
- **Anggaran kecil tetap masuk akal:** Rp500rb sampai Rp20jt per bulan; skrip menyingkirkan kanal yang uangnya terlalu tipis untuk diuji.
- **Jujur:** tanpa janji hasil, dengan catatan aturan iklan untuk kesehatan, keuangan, kripto.

## Cocok untuk siapa
Pemilik toko online, kafe, jasa lokal, reseller, dan admin sosmed yang mulai atau ingin merapikan iklan berbayar dan bingung membagi uang ke banyak kanal.

## Sebelum / sesudah
**Sebelum:** "Rp5 juta ya saya taruh semua di boost postingan IG." Tidak tahu hasil minimal, tidak ada bagian untuk uji, pesanan dari Shopee tidak terlayani.

**Sesudah (cukup ketik):** "Saya jual kaos sablon, anggaran iklan Rp5 juta sebulan. Harga rata-rata Rp150.000, margin 40%. Saya punya toko Shopee dan Instagram. Rencananya mulai 1 November. Tolong bagi anggarannya dan bikin strategi kontennya."

Cuplikan balasan (dipotong; contoh dengan data fiktif dari `examples/01-toko-kaos-shopee-ig.md`):
```
Angka kunci
| Laba kotor per pesanan | Rp60.000 |
| ROAS impas (1 / margin) | 2,50x |
| ROAS target aman | 3,58x |
| CPA impas / CPA maksimal (target aman) | Rp60.000 / Rp42.000 |
| Pesanan minimal agar anggaran bulan ini impas | 84 pesanan (omzet Rp12.600.000) |
Di bawah 2,50x iklan Anda merugi; angka itu batas, bukan hasil yang akan didapat. … Tidak ada ROAS yang "pasti": angka sebenarnya baru terlihat dari iklan yang sudah berjalan.
…
Pilar konten (4 pilar)
| 1. Padu padan & perawatan | Awareness | Dikenal karena berguna dan mudah disimpan | praktis; hemat (satu kaos banyak gaya); mudah ditiru | Reels/video pendek 15-30 detik, carousel |
| 3. Bukti: ulasan dan foto pembeli asli | Pertimbangan | Menjawab "kaosnya bagus nggak?" | kata pembeli sendiri; foto asli dipakai; pembeli yang kembali beli | Carousel/screenshot ulasan (dengan izin pembeli) |
…
Tiga langkah pertama (hari ini)
1. Pastikan margin bersih. Hitung: harga jual dikurangi modal kaos dan sablon, biaya admin Shopee, ongkir yang Anda tanggung, dan kemasan. Bagi hasilnya dengan harga jual. Kalau hasilnya bukan 40%, kabari saya supaya semua angka dihitung ulang.
```
Hasil lengkapnya juga memuat tabel anggaran per kanal per minggu dan aturan keputusan mingguan. Bila pesanan terbanyak lewat Shopee, porsi terbesar anggaran diarahkan ke Shopee Ads (dari Rp5 juta: Rp3.333.333 untuk Shopee Ads dan Rp1.666.667 untuk Meta).

## Cara pakai
Ketik: *"Anggaran iklan saya Rp5 juta sebulan, harga rata-rata Rp150.000, margin 40%, saya punya Shopee dan IG. Bagi anggarannya dan bikin strategi kontennya."* Bila ada info kurang, skill bertanya sekali. Angka boleh gaya Indonesia: `1.500.000`, `1,5jt`, `500rb`. Angka yang bisa berarti dua hal (mis. `1,500`) akan ditanyakan ulang, tidak ditebak.

## Instalasi singkat
Salin folder `strategi-konten-iklan` ke lokasi skill di platform Anda (OpenClaw, OpenAI Codex, Claude Code, Cursor). Lokasi lengkap dan langkah per platform ada di `docs/instalasi.md` pada paket Anda (di dalam paket bernama `CARA-INSTAL.md`).

Bagian hitung juga bisa dijalankan sendiri bila Anda terbiasa dengan terminal (Windows: `python` atau `py`): `python3 scripts/alokasi_anggaran.py --anggaran 5jt --aov 150rb --margin 40% --kanal meta,shopee --kanal-utama shopee`

**Hasil uji (angka nyata):** uji OpenClaw sebelum/sesudah otomatis agent, 2026-10-01–05 (v1.0.6), skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Rata-rata uji lokal (2 skenario awal): tanpa skill **6,75** → dengan skill **8,25**; uji ulang v1.0.5+: tanpa **6,75** → dengan **8,5** (LULUS).
- Pra-cek konteks Telegram (3 percobaan, tanpa kirim): rata **8,0** — menolak klaim "turun 5kg seminggu", ROAS impas 2,50x, target aman 3,58x.
- Bot Telegram asli (gelombang 10, 2026-10-05): tanpa skill **6** → dengan skill **8,5**.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent + bot Telegram gelombang 10 + pra-cek Telegram). Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung. Tidak ada jaminan ROAS/penjualan — hanya batas impas dan pembagian anggaran.

## FAQ
1. **Apakah skill ini menjalankan iklan saya?** Tidak. Skill merencanakan dan menghitung; Anda yang membuat dan menayangkan iklan. Jangan pernah membagikan password atau kode OTP akun iklan.
2. **Apakah ada jaminan penjualan atau ROAS tertentu?** Tidak. Yang dihitung hanya batas impas dan pembagian uang; hasil bergantung produk, harga, kreatif, dan persaingan.
3. **Apa bedanya dengan skill rencana marketing dan laporan iklan?** Rencana marketing (`rencana-marketing-usaha`) menyusun rencana menyeluruh 1-12 bulan; laporan iklan (`laporan-iklan-mingguan`) membaca hasil iklan yang sudah tayang. Skill ini di tengahnya: pilar konten dan anggaran iklan bulanan.

## Skill pendamping
Skill Komunitech lain yang bisa dipasangkan: `rencana-marketing-usaha` (rencana pemasaran menyeluruh), `laporan-iklan-mingguan` (membaca hasil iklan), `hitung-hpp` (modal per produk), `strategi-harga-produk` (harga dan promo).

## Asal-usul
Diadaptasi dan diperluas dari skill `content-strategy` dan `ads` (marketingskills, Corey Haines, lisensi MIT); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber. Nama platform hanya sebagai penyebut kanal.

## Riwayat perubahan

Versi terkini: **1.0.8**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
