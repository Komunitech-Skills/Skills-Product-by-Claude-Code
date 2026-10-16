# Foto Produk Kelas Toko Besar, Cukup Pakai HP

**Dapatkan daftar foto, cara menata cahaya jendela, dan ide video 15–30 detik yang tinggal dikerjakan, tanpa studio dan tanpa alat mahal.**

Diuji AI penguji independen di OpenClaw: 6,5 → 8,8 dari 10 (1 Okt 2026; skor tanpa skill dari uji awal, skor dengan skill dari uji ulang v1.0.3 setelah perbaikan; uji awal 6,5 → 7,5 belum lulus). Pembeda: untuk kamar berjendela menghadap timur, dengan skill jam foto disesuaikan ke 11.00–16.00 dan brief memuat urutan foto per tempat jualan, rasio, serta catatan keselamatan api untuk lilin; tanpa skill AI menyarankan foto pagi saat matahari timur masuk langsung.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Daftar foto (shot list) 8–10 foto yang menjawab pertanyaan pembeli: bentuk, detail, ukuran, cara pakai, isi paket, varian
- ✅ Panduan cahaya jendela, latar kertas karton, dan pemantul styrofoam, supaya hasilnya lebih terang dan bersih
- ✅ Pengaturan kamera HP langkah demi langkah (fokus, kunci kecerahan atau exposure, lensa yang tepat)
- ✅ Rasio yang benar untuk tiap tempat: 1:1 marketplace, 3:4/4:5 feed, 9:16 TikTok & Reels
- ✅ 2–3 ide video pendek dengan urutan adegan per detik (storyboard), plus checklist sebelum upload

## Cocok untuk siapa
- Seller marketplace yang memotret produk sendiri di rumah
- Pemilik UMKM kuliner, fashion, kecantikan, kerajinan yang ingin foto lebih meyakinkan
- Pemilik usaha yang ingin memberi brief (arahan kerja tertulis) jelas ke staf, teman, atau fotografer freelance

## Contoh sebelum & sesudah
**Sebelum:** Foto produk di meja makan dengan lampu kuning, latar berantakan, warna tidak sesuai aslinya. Pembeli sering bertanya "ukurannya berapa?" dan ada ulasan "warna beda dengan foto".

**Sesudah (cukup ketik):** "Aku jual hijab voal segi empat 115x115, ada 4 warna: hitam, mocca, dusty pink, sage. Mau foto sendiri pake HP (android, ga punya tripod) buat Shopee sama TikTok Shop. Sering dapet review “warnanya beda sama foto”. Kamar aku ada jendela gede hadap timur. Bikinin brief fotonya dong."

Cuplikan hasil (dipotong; dari uji simulasi Claude Code oleh penguji independen, 23 Sep 2026, data fiktif, `examples/01-hijab-voal-4-warna.md`; "slot" = urutan posisi foto di halaman produk marketplace):
> ## 2. Setup cahaya & pengaturan HP
> 1. **Matikan semua lampu kamar.** Lampu kuning + cahaya jendela membuat warna mocca dan dusty pink bergeser. Ini sumber utama keluhan "warna beda".
> 2. Lap lensa. Nyalakan **grid/garis bantu** di pengaturan kamera.
> 3. Pakai lensa **1x** (jangan 0,5x). Jangan zoom digital; dekatkan HP bila perlu.
> …
> 8. **Tes warna:** jepret 1 foto uji tiap warna, lalu bandingkan layar HP dengan kain asli di dekat jendela. Kalau beda, ubah kecerahan, bukan filter.
>
> …
>
> | No | Nama foto | Dipakai di | Rasio | Sudut & jarak | Latar & properti | Catatan |
> |---|---|---|---|---|---|---|
> | 1 | **Foto utama**: hijab dilipat rapi (lipatan segitiga/persegi), warna terlaris | Shopee & TikTok Shop slot 1 | 1:1 | Dari atas 90°, HP ±50 cm | Karton putih polos | Produk mengisi ±70–85% bingkai; **tanpa teks promo, tanpa nomor WA/watermark besar** |
> | 2 | Hijab dipakai: tampak depan | Slot 2 | 1:1 (& 3:4 bila tersedia di kategori) | Setinggi dada model, ±1,5 m | Dinding polos terang dekat jendela | Model menghadap jendela (cahaya dari samping depan); izin model |

Brief lengkapnya juga memuat daftar alat dan properti murah, 9 foto, 2 ide video pendek, dan checklist sebelum upload.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bikinin shot list foto untuk hijab voal 4 warna"
- "Cara foto produk skincare pakai HP biar kelihatan premium tapi tetap jujur"
- "Ide video 15 detik untuk kopi susu botolan"

## Instalasi singkat
Salin folder `foto-produk-brief` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw otomatis oleh agent penguji (lingkungan uji terpisah), 1 Okt 2026 (v1.0.3), skor 1–10 penguji independen: tanpa skill **6,5** → dengan skill **8,8** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Contoh lilin aromaterapi dengan jendela menghadap timur: dengan skill, brief berisi 9 foto lengkap dengan urutan slot di marketplace, rasio, sudut, tes warna, catatan keselamatan api, dan 3 ide video per detik; tanpa skill, AI menyarankan foto pagi hari saat matahari timur masuk langsung, dan daftar fotonya tanpa rasio, urutan slot, maupun catatan keselamatan api. Catatan jujur: skor 6,5 tanpa skill berasal dari uji awal; sisi dengan skill diulang setelah perbaikan (uji awal 7,5, belum lulus, karena pada permintaan foto bermasalah, yaitu logo BPOM dan before-after, skill belum terpanggil). Teks video hasil skill masih sekali memuat klaim yang tidak Anda berikan ("tahan lama"), jadi baca ulang sebelum dipakai.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung, dan bot Telegram asli belum diuji.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: Aku jual hijab voal segi empat 115x115, ada 4 warna: hitam, mocca, dusty pink, sage. Mau foto sendiri pake HP (android, ga punya tripod) buat Shopee sama TikTok Shop. Sering dapet review "warnanya beda sama foto". Kamar aku…. Tanpa skill skor **6,5** → dengan skill skor **8,5** (selisih +2, lulus acuan kami). Hanya sisi DENGAN yang menghindari matahari pagi langsung dari jendela timur (memotret sekitar 10.30-14.00), memetakan 9 foto ke slot upload dengan urutan prioritas bila slot kurang, menambah teks penjelas "warna bisa sedikit berbeda", dan memberi dua storyboard video per detik. Sisi TANPA menyarankan pagi 7:30-9:30 dan hanya memberi 5 foto umum per warna, tanpa urutan slot dan tanpa ide video, walau sudah memakai kertas HVS putih sebagai patokan warna. Catatan jujur: Tabel foto terlalu lebar untuk layar HP dan terpotong di tengah kalimat antar pesan, jadi sebagian baris sulit dibaca; ide video ditulis sebagai daftar singkat, bukan tabel per detik. Saran menurunkan kecerahan untuk warna hitam kurang jelas alasannya dan tidak ada panduan mengunci white balance, jadi hasil warna tetap perlu dites dulu dengan kertas putih sebelum memotret semua varian.

## FAQ
**Harus beli lampu studio atau kamera?**
Tidak harus. Panduan dirancang untuk HP, cahaya jendela, dan properti murah seperti kertas karton dan styrofoam. Kalau Anda punya tripod atau lampu, skill akan memakainya.

**Apakah skill ini mengedit foto saya?**
Tidak. Skill membuat brief dan daftar foto yang tinggal Anda kerjakan, lalu memberi checklist sebelum upload.

**Bolehkah foto dibuat lebih bagus dari aslinya?**
Foto boleh dibuat terang dan rapi, tapi warna, ukuran, dan isi harus sesuai barang asli. Foto yang berlebihan memicu ulasan "tidak sesuai foto" dan retur.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
