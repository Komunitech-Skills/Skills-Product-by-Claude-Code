# Naskah Live Jualan Siap Baca per Menit

**Sebut produk dan promonya, dapat rundown (urutan acara) dan naskah live TikTok/Shopee yang tinggal dibaca host.**

Diuji AI penguji independen di OpenClaw: 6,17 → 8,83 dari 10 (rundown per menit dengan angka promo yang dihitung dan tanpa klaim produk karangan; tanpa skill naskahnya generik tanpa pembagian waktu live).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Rundown per menit: setiap produk kebagian waktu, dan ada segmen rekap promo untuk penonton yang baru masuk
- ✅ Kalimat siap ucap untuk pembuka penarik perhatian (hook), demo produk, harga, dan ajakan checkout, lengkap dengan arahan aksi untuk host (pembawa acara live)
- ✅ Angka promo dihitung otomatis: potongan, persen hemat, dan harga per pcs paket (beli beberapa lebih hemat)
- ✅ Jawaban cepat untuk pertanyaan penonton ("size?", "bisa COD?", "ongkir?")
- ✅ Urgensi yang jujur, tanpa "tinggal 3!" palsu yang bisa bikin akun kena penalti

## Cocok untuk siapa
- Seller yang rutin live di TikTok Live atau Shopee Live
- Pemilik toko yang melatih host atau admin baru
- Toko yang menyiapkan live spesial tanggal kembar (10.10, 11.11, 12.12) atau payday

## Contoh sebelum & sesudah
**Sebelum:** Host bingung mau ngomong apa, satu produk dibahas 30 menit, produk lain terlupa, penonton baru tidak tahu promonya.

**Sesudah (cukup ketik):** "Bikinin script live TikTok 1 jam ya, mulai jam 8 malam. Toko Batik Lestari dari Pekalongan. Produk: Kemeja batik cap pria katun primisima, normal 185rb, pas live 149rb, beli 2 jadi 280rb. Daster batik rayon allsize (LD 120), 95rb diskon 15%. Kain batik tulis 2 meter pewarna alam, 650rb gak diskon, stoknya emang cuma 5 lembar bulan ini. …"

Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-tiktok-live-batik-60-menit.md`):
> ## Naskah Live TikTok — Batik Lestari, 60 menit (20.00–21.00 WIB)
>
> …
>
> | Waktu | Segmen | Produk |
> |---|---|---|
> | 20.00–20.03 | Pembukaan: sapa, hook besar, janji promo live | – |
> | 20.03–20.04 | Hook | Kemeja Batik Cap Pria |
> | 20.04–20.08 | Demo produk | Kemeja Batik Cap Pria |
>
> …
>
> | Produk | Normal | Harga live | Hemat | Bundling |
> |---|---|---|---|---|
> | Kemeja Batik Cap Pria | Rp 185.000 | Rp 149.000 | Rp 36.000 (±19%) | Isi 2 Rp 280.000 → Rp 140.000/pcs, hemat Rp 90.000 vs 2× harga normal |
>
> …
>
> **[20.08–20.10] Harga & promo — Kemeja Batik Cap Pria**
> "Harga normalnya Rp 185.000. Khusus selama live malam ini jadi Rp 149.000 — hemat Rp 36.000. Mau lebih hemat? Ambil paket isi 2, Rp 280.000 saja, jadi Rp 140.000 per potong — hemat Rp 90.000 dibanding beli 2 di harga normal. Cocok buat Bapak dan kakaknya, atau satu buat kantor satu buat kondangan." [pin produk no. 1]

Hasil lengkapnya juga memuat naskah semua segmen dan jawaban cepat untuk pertanyaan penonton.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatin naskah Shopee Live 30 menit buat jualan kopi bubuk 3 varian"
- "Script live TikTok 2 jam buat 5 produk skincare, host-nya 2 orang"
- "Siapin jawaban cepat buat pertanyaan penonton live tentang ukuran gamis"

## Instalasi singkat
Salin folder `naskah-live-jualan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (skill v1.0.5), skor 1–10 penguji independen: tanpa skill **6,17** → dengan skill **8,83** (lulus acuan kami). Sumber semua angka: `examples/00-openclaw-sebelum-sesudah.md`. Uji ulang di konteks Telegram pada v1.0.7 (5 Okt 2026, 3 percobaan, tanpa kirim ke grup): rata-rata dengan skill **8,17**, lulus 3 dari 3 (tanpa pembanding tanpa-skill). Dengan skill: rundown per menit dengan tanda kapan menyebut stok dan harga, fakta dicek silang, dan tidak ada istilah internal yang ikut terucap; tanpa skill: naskah generik tanpa pembagian waktu live.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 5 Okt 2026, skill versi 1.0.7; versi 1.0.8 hanya mengganti rujukan ke skill lain) dengan pesan yang sama: naskah TikTok Live 30 menit jam 8 malam untuk sambal botol, harga normal Rp35.000, harga live Rp28.000, paket isi 2 Rp52.000. Tanpa skill skor **5,5** → dengan skill skor **8** (selisih +2,5, lulus acuan kami, tetapi tepat di batas skor 8). Dengan skill, naskah dibagi per menit lengkap dengan jam tayangnya (20.00–20.30), tabel promonya dihitung benar (hemat Rp7.000 atau 20%; paket isi 2 jadi Rp26.000 per botol, hemat Rp18.000 atau 25%), stok ditulis sebagai isian `[stok nyata]`, dan ada daftar jawaban untuk pertanyaan penonton tanpa klaim karangan. Tanpa skill, bot mengarang klaim produk seperti "tanpa pengawet", "tahan lama", dan "paling nagih", serta menyarankan menyebut "stok terbatas" dan "tersisa sekian botol" demi efek terburu-buru padahal tidak ada data stok. Catatan jujur: banyak bagian masih berupa isian `[isi: ...]` (bahan, tingkat pedas, ukuran, COD, masa simpan) yang harus Anda lengkapi sendiri, sehingga bagian demo produk masih tipis. Jawaban untuk "Halal/BPOM?" hanya menyuruh melihat deskripsi produk, sebaiknya Anda ganti dengan nomor izin atau sertifikat halal Anda, dan belum ada pengingat bahwa harga normal Rp35.000 harus benar-benar pernah berlaku. Uji sebelumnya di komputer uji OpenClaw (1 Okt 2026) memberi 6,17 → 8,83.

## FAQ
**Kenapa tidak boleh bilang "stok tinggal sedikit" untuk memancing pembeli?**
Boleh, asalkan benar. Skill menaruh `[stok nyata]` agar host membaca angka dari layar. Stok atau hitung mundur palsu termasuk informasi menyesatkan dan bisa merugikan toko Anda.

**Bisa untuk live dengan 2 host atau bahasa daerah?**
Bisa. Sebutkan saja, misalnya "host 2 orang, pakai sedikit bahasa Sunda".

**Bagaimana kalau Python tidak ada di komputer saya?**
Skill tetap jalan. AI agent menghitung manual dengan rumus yang sama dan memberi tahu Anda bahwa hitungannya manual.

## Riwayat perubahan

Versi terkini: **1.0.8**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
