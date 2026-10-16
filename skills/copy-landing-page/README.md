# Landing Page Jualan Siap Kirim ke Pembeli

**Ceritakan produk Anda, dapat halaman jualan lengkap — judul utama, manfaat, penawaran, FAQ, sampai tombol WhatsApp — siap tempel ke website atau link-in-bio.**

Diuji AI penguji independen di OpenClaw: 6,0 → 8,0 dari 10 (dengan skill struktur halaman lengkap, tautan WhatsApp dan panjang judul/deskripsi Google diperiksa skrip, dan testimoni tidak dikarang).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Struktur halaman jualan yang lazim dipakai (judul utama/headline → masalah → manfaat → bukti sosial → penawaran → garansi → FAQ → tombol ajakan/CTA), bukan asal susun paragraf jualan
- ✅ Tombol ajakan (CTA) dibentuk jadi tautan WhatsApp yang benar (`wa.me`, link yang langsung membuka chat) lengkap pesan siap kirim — dihitung skrip, bukan ditulis manual dan salah ketik
- ✅ 3 variasi judul utama (headline) sekaligus untuk dites, plus judul dan deskripsi yang tampil di Google (meta title & meta description SEO) dengan panjang karakter dihitung persis
- ✅ Dijaga tidak melanggar aturan: tidak mengarang testimoni/rating/angka penjualan, dan menandai klaim berisiko (kesehatan, BPOM, halal, harga coret) sebelum Anda publish
- ✅ Ada versi pendek untuk link-in-bio/halaman satu layar HP, bukan cuma versi panjang

## Cocok untuk siapa
- Pemilik UMKM (makanan, fashion, jasa servis, kursus) yang mau jualan lewat website/landing page sendiri, bukan lewat marketplace
- Pemilik usaha yang link-in-bio Instagram/TikTok-nya masih sekadar daftar link tanpa cerita jualan
- Freelancer/jasa (servis AC, klinik gigi, tukang, guru les) yang butuh halaman jualan tapi tidak sanggup bayar copywriter
- **Bukan untuk:** caption sosmed (pakai paket konten mingguan, `konten-mingguan`), judul/deskripsi Shopee/Tokopedia/TikTok Shop (pakai `listing-marketplace`), atau pesan WhatsApp massal ke banyak kontak (pakai `broadcast-wa`)

## Contoh sebelum & sesudah
**Sebelum:** "Jual keripik pedas enak dan murah, order chat aja ya kak 😊" — ditempel di halaman kosong tanpa struktur, tanpa tombol ajakan (CTA) yang jelas, tanpa jawaban keberatan calon pembeli.

**Sesudah (cukup ketik):** "Buatkan landing page untuk keripik pedas saya, harga 25 ribu"

Cuplikan hasil (dipotong; contoh dengan data fiktif dari `examples/01-keripik-pedas-normal.md`). Hal yang tidak Anda sebutkan (ukuran, level pedas, masa simpan, garansi) tidak dikarang, tetapi ditandai `[isian: ...]` untuk Anda isi:
```
# Pesan Keripik Pedas Mak Iyem Lewat WhatsApp, Dikirim ke Rumahmu
### Keripik Setan Mak Iyem — Rp25.000 [isian: per bungkus/ukuran]. Kirim ke Jabodetabek dan luar kota, bayar transfer atau QRIS.

**[Pesan Sekarang lewat WhatsApp →](https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini)**
…
- Rasa dan tingkat pedas: [isian: varian rasa/level pedas yang tersedia sesuai produkmu].
…
## Kata Mereka yang Sudah Coba
[ISI TESTIMONI ASLI — nama & kota pembeli. Hapus bagian ini sampai ada testimoni asli.]
…
## Garansi
[isi: garansi/retur, hanya yang benar-benar kamu berlakukan.]
```
Hasil lengkapnya juga memuat struktur masalah–manfaat–penawaran–garansi–FAQ, 3 variasi judul untuk dites, serta judul dan deskripsi Google yang panjangnya sudah diukur.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan landing page untuk keripik pedas saya, harga 25 ribu"
- "Bikin halaman jualan jasa servis AC, format link in bio"
- "Perbaiki landing page kursus online saya ini biar CTA-nya jelas: <tempel teks lama>"

Kalau info produk Anda belum lengkap, AI akan tanya sekali dalam satu pesan (nomor WA, harga, cara bayar, dll). Kalau Anda buru-buru, bilang saja "pakai default aja" — nanti asumsinya disebutkan di akhir supaya Anda tinggal sesuaikan.

## Instalasi singkat
Salin folder `copy-landing-page` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.0.4), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **8,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dengan skill struktur halaman jualan lengkap, judul/deskripsi Google dan tautan WhatsApp diperiksa skrip, testimoni tidak dikarang. Catatan jujur: pada uji ini masih ada detail layanan kecil yang dikarang (mis. garansi 1×24 jam), jadi periksa janji layanan di hasil sebelum Anda publish.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01; uji muat CLI) dan Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: "Buatkan landing page untuk keripik pedas saya, harga 25 ribu per bungkus. Namanya Keripik Setan Mak Iyem, WA 0812-3456-7890, kirim se-Jabodetabek pakai ojol/kurir sendiri kalau dekat, luar kota pakai ekspedisi, bayar…". Tanpa skill skor **3** → dengan skill skor **8** (selisih +5, lulus acuan kami). Dengan skill, bot langsung menulis teks landing page lengkap di chat: versi panjang, versi link-in-bio, 3 headline, judul dan deskripsi Google yang hurufnya sudah dihitung, serta tautan WA yang bisa diklik. Bot juga mengingatkan izin PIRT/BPOM dan wajib halal, dan semua yang belum diberikan (varian rasa, ukuran, masa simpan, garansi) ditulis [isian]. Tanpa skill, bot hanya mengirim ringkasan isi yang memuat klaim karangan ("fresh", "dibuat dari hati"), dan file HTML-nya gagal terkirim, jadi tidak ada teks yang bisa dipakai. Salah angka yang ditemukan penilai: TANPA: daftar 'Kenapa harus beli' memuat klaim 'fresh' dan 'dibuat dari hati'. Pemilik tidak pernah menyebut keduanya, jadi ini klaim karangan dan skor dibatasi maks 5. DENGAN: tidak ada salah angka/fakta. Yang sudah dicek ulang: nomor WA 0812-3456-7890 → wa.me/6281234567890 (URL di balik tautan sudah di-encode benar), panjang meta title 47/60 dan deskripsi 135/155 karakter, serta tanggal wajib halal UMK makanan-minuman 18 Okt 2026 (cocok dengan rujukan BPJPH). Kalimat asumsi 'satuan harga tidak disebut' adalah salah baca pesan pemilik; dicatat sebagai cacat, bukan salah fakta di isi halaman.. Catatan jujur: Harga ditulis "Rp25.000 [isian: per bungkus/ukuran]" walaupun pemilik sudah menyebut "per bungkus", jadi isian itu harus dihapus sendiri. Hasilnya berupa teks untuk ditempel ke pembuat halaman web atau link-in-bio, bukan file halaman web yang langsung jadi.

## FAQ
**Apakah testimoni/rating di halaman jualan dibuatkan otomatis?**
Tidak. Skill ini sengaja **tidak mengarang** testimoni, rating bintang, atau angka penjualan — itu melanggar kepercayaan pembeli dan berisiko hukum. Kalau Anda belum punya testimoni asli, bagian itu ditandai placeholder yang bisa Anda isi belakangan.

**Produk saya makanan/kosmetik, boleh tulis "halal" atau klaim sehat?**
Hanya kalau Anda memang sudah punya sertifikat resmi (BPJPH/MUI untuk halal, izin edar BPOM untuk klaim kesehatan/kosmetik). Kalau belum, skill tidak akan menuliskannya — akan diganti kalimat manfaat umum yang tidak melanggar aturan, dan ditandai di ceklis kepatuhan di akhir output.

**Harus pakai Python?**
Tidak wajib. Kalau Python ada, tautan WhatsApp dan panjang meta title/description dihitung otomatis lewat script. Kalau tidak ada, AI agent tetap menyusun halamannya dan menghitung manual, lalu memberi tahu Anda untuk dicek sekali sebelum dipakai.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.

Skill ini diadaptasi dari struktur marketing skill open-source (MIT, coreyhaines31/marketingskills); teks, contoh Indonesia, script, dan ceklis kepatuhan milik Komunitech. Komunitech tidak berafiliasi dengan pembuat sumber.
