# Listing Shopee, Tokopedia, TikTok Shop Sekali Jadi

**Ceritakan produk Anda, dapat judul, deskripsi, dan kata kunci yang siap tempel ke tiga marketplace.**

Diuji AI penguji independen di OpenClaw: 5,5 → 9 dari 10 (satu skenario, versi 1.0.4, 1 Oktober 2026; tanpa skill, deskripsi hijab ditambahi enam klaim yang tidak pernah disebut pemilik toko, mis. "Dikirim cepat & packing aman"; dengan skill, AI bertanya sekali dulu, lalu judul dan deskripsi terutama dari fakta pemilik dengan panjang karakter yang cocok dengan hitung ulang penguji).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Judul disusun mengikuti batas karakter aman tiap platform, supaya lebih kecil kemungkinan terpotong atau ditolak (batas terbaru tetap Anda cek di Seller Center)
- ✅ Kata kunci yang biasa diketik pembeli ditaruh di awal judul agar lebih mudah ditemukan
- ✅ Deskripsi rapi dan lengkap: keunggulan, spesifikasi, isi paket, cara pakai, siap tempel
- ✅ Dicek dengan skrip hitung kecil: nomor WA, link, @akun, dan klaim berisiko ("halal", "BPOM", "termurah") yang bisa bikin produk diturunkan
- ✅ Diupayakan tanpa karangan: data yang belum Anda berikan ditandai `[isi: ...]` supaya Anda lengkapi sendiri

## Cocok untuk siapa
- Seller Shopee, Tokopedia, dan TikTok Shop yang upload produk baru setiap minggu
- Pemilik toko yang listingnya sepi pengunjung dan ingin diperbaiki
- Admin toko online yang mengelola satu produk di beberapa marketplace

## Contoh sebelum & sesudah
**Sebelum:** Judul "SAMBAL ENAK MURAH!!! 🔥🔥 ORDER WA 0812xxxx" — terpotong di Tokopedia dan berisiko kena penalti.

**Sesudah (cukup ketik):** "Bikinin listing buat gamis busui aku, namanya Gamis Alya dari Rumah Alya (Solo). Bahan katun rayon, ada resleting depan buat menyusui. Ukuran M (LD 100, PB 135), L (LD 106, PB 137), XL (LD 112, PB 139). Warna navy, sage, mocca. Mau upload di Shopee, Tokopedia, sama TikTok Shop." (LD = lingkar dada, PB = panjang badan)

Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-gamis-busui-tiga-platform.md`):
```
| Platform | Judul | Panjang / batas aman |
|---|---|---|
| Shopee | Gamis Busui Katun Rayon Resleting Depan Gamis Alya Ukuran M L XL Navy Sage Mocca | 80/100 |
| Tokopedia | Gamis Busui Katun Rayon Resleting Depan Gamis Alya M L XL | 57/70 |
| TikTok Shop | Gamis Busui Katun Rayon Resleting Depan Ramah Menyusui Ukuran M L XL | 68/100 (min. 25) |
…
Gamis busui katun rayon dengan resleting depan — adem, praktis untuk menyusui.

✅ Resleting depan untuk menyusui
✅ Katun rayon, adem & jatuh
✅ Ukuran M / L / XL (LD 100 / 106 / 112 cm)
✅ Warna: Navy, Sage, Mocca
…
```
Hasil lengkapnya juga memuat deskripsi untuk Shopee dan Tokopedia, daftar kata kunci, dan hasil pengecekan batas karakter serta kata berisiko.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatin judul dan deskripsi Shopee buat gamis busui bahan ceruty, size M–XXL"
- "Perbaiki listing Tokopedia ini biar lebih gampang dicari: <tempel judul & deskripsi lama>"
- "Cariin kata kunci buat jual tumbler stainless 500 ml di TikTok Shop"

## Instalasi singkat
Salin folder `listing-marketplace` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji sebelum/sesudah oleh AI penguji independen di OpenClaw (uji otomatis oleh agent AI, bukan oleh manusia; versi 1.0.4, 1 Oktober 2026; satu skenario dalam uji paket Toko Online, bukan lima skenario per skill). Pesan uji ditulis penguji seperti pemilik toko awam: "bikinin deskripsi produk buat hijab voal aku dong, mau upload di shopee" (info produk belum diberikan), lalu jawaban pemilik dalam satu pesan; pesan yang sama dikirim tanpa dan dengan skill. Nilai **5,5 tanpa skill → 9 dengan skill** (dari 10): 8,5 pada uji pertama, lalu 9 pada dua uji ulang (versi 1.0.3 dan 1.0.4); sisi tanpa skill tidak diulang.
- Tanpa skill: AI langsung menulis deskripsi dan menambah enam klaim yang tidak pernah disebut pemilik (mis. "Dikirim cepat & packing aman", "Barang sesuai foto & deskripsi", "Banyak pelanggan repeat order!"), menaruh harga di deskripsi, dan tidak membuat judul terpisah.
- Dengan skill: AI bertanya sekali dulu (lima pertanyaan bernomor), lalu memberi judul untuk Shopee, Tokopedia, dan TikTok Shop beserta deskripsi; pada uji terakhir panjang karakter yang dilaporkan sama dengan hitung ulang penguji (deskripsi 673 dan 294 karakter; judul 68 dan 47), harga tidak dimasukkan ke deskripsi, dan sertifikat yang tidak ada tidak ditulis.
- Catatan jujur: nilai tanpa skill hanya dari giliran 2 (balasan giliran 1 sisi tanpa skill tidak terbaca penguji). Uji pertama menemukan satu klaim tambahan kecil ("ga gampang buyar") yang lolos pengecekan, diperbaiki di versi 1.0.3. Di uji terakhir dua tambahan kecil ("warna kalem" dan contoh pemakaian) masih lolos pengecekan, jadi tetap baca ulang deskripsi sebelum diunggah. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.
- Uji Claude Code (simulasi agent, 5 skenario + A/B skenario 1): skor penguji independen **8/10** (LULUS). Tanpa skill: judul 141 karakter (melewati batas Shopee/Tokopedia/TikTok), klaim karangan (“tidak menerawang”, “wudhu friendly”); dengan skill: judul per platform + batas karakter, deskripsi polos siap tempel, cek kata terlarang. Sumber: `examples/HASIL-UJI.md`, `examples/00-pembanding-tanpa-skill.md`.

**Status uji (jujur):** sudah diuji di Claude Code (simulasi agent) dan OpenClaw (uji muat lewat CLI, ditambah uji sebelum/sesudah otomatis oleh agent AI pada 1 Oktober 2026: satu skenario, tiga putaran, terakhir versi 1.0.4). Versi terkini 1.0.5 mengganti rujukan ke skill yang sudah diarsipkan dengan `konten-mingguan` (lihat `CHANGELOG.md`); uji sebelum/sesudah yang tercatat di folder `examples/` memakai versi 1.0.4. Codex dan Cursor belum kami uji langsung.

## FAQ
**Apakah batas karakternya pasti sesuai aturan terbaru marketplace?**
Skill memakai batas aman yang sama atau lebih ketat dari batas yang pernah berlaku, dan mengingatkan Anda untuk cek batas terbaru di Seller Center. Kalau Anda tahu angka terbarunya, sebutkan saja dan skill akan memakainya.

**Kalau produk saya belum punya sertifikat halal atau BPOM?**
Skill tidak menuliskannya. Klaim tanpa bukti bisa membuat produk diturunkan dan melanggar aturan perlindungan konsumen.

**Harus pakai Python?**
Tidak wajib. Kalau Python (program gratis untuk menjalankan skrip) ada, pengecekan panjang teks dan kata terlarang berjalan otomatis. Kalau tidak ada, AI agent mengecek manual dan memberi tahu Anda.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
