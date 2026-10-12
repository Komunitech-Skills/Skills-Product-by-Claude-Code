# Naskah Live Jualan Siap Baca per Menit

**Sebut produk dan promonya, dapat rundown dan naskah live TikTok/Shopee yang tinggal dibaca host.**

## Manfaat
- ✅ Rundown per menit: semua produk kebagian waktu, penonton yang baru masuk selalu dapat rekap promo
- ✅ Kalimat siap ucap untuk hook, demo, harga, dan ajakan checkout, lengkap dengan arahan aksi host
- ✅ Angka promo dihitung otomatis: potongan, persen hemat, dan harga per pcs paket bundling
- ✅ Jawaban cepat untuk pertanyaan penonton ("size?", "bisa COD?", "ongkir?")
- ✅ Urgensi yang jujur, tanpa "tinggal 3!" palsu yang bisa bikin akun kena penalti

## Cocok untuk siapa
- Seller yang rutin live di TikTok Live atau Shopee Live
- Pemilik toko yang melatih host atau admin baru
- Toko yang menyiapkan live spesial tanggal kembar (10.10, 11.11, 12.12) atau payday

## Contoh sebelum & sesudah
**Sebelum:** Host bingung mau ngomong apa, satu produk dibahas 30 menit, produk lain terlupa, penonton baru tidak tahu promonya.

**Sesudah (cukup ketik):** "Bikinin script TikTok Live 1 jam jam 7 malam, Hijab Voal 89rb jadi 69rb, paket 3 jadi 189rb, Pashmina Kaos 65rb diskon 10%"
→ Rundown 19.00–20.00, tabel angka promo (Hijab Voal hemat Rp 20.000, paket isi 3 jatuhnya Rp 63.000/pcs), naskah per segmen, dan jawaban cepat untuk penonton.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatin naskah Shopee Live 30 menit buat jualan kopi bubuk 3 varian"
- "Script live TikTok 2 jam buat 5 produk skincare, host-nya 2 orang"
- "Siapin jawaban cepat buat pertanyaan penonton live tentang ukuran gamis"

## Instalasi singkat
Salin folder `naskah-live-jualan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 9, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/831/849 — skor 5,5
- Dengan skill: https://t.me/c/4407409583/832/851 — skor 8
Verdik gelombang: LULUS — DENGAN memberi rundown 30 menit bertanggal jam, tabel promo yang benar (hemat Rp7.000/20%, paket Rp26.000/pcs, hemat Rp18.000/25%), stok sebagai `[stok nyata]`, dan bank jawaban tanpa klaim karangan; TANPA mengarang klaim produk ("tanpa pengawet", "tahan lama", "paling nagih") dan menyarankan "stok terbatas" serta "tersisa X botol … buat efek urgensi".

## FAQ
**Kenapa tidak boleh bilang "stok tinggal sedikit" untuk memancing pembeli?**
Boleh, asalkan benar. Skill menaruh `[stok nyata]` agar host membaca angka dari layar. Stok atau hitung mundur palsu termasuk informasi menyesatkan dan bisa merugikan tokomu.

**Bisa untuk live dengan 2 host atau bahasa daerah?**
Bisa. Sebutkan saja, misalnya "host 2 orang, pakai sedikit bahasa Sunda".

**Bagaimana kalau Python tidak ada di komputer saya?**
Skill tetap jalan. AI agent menghitung manual dengan rumus yang sama dan memberi tahu kamu bahwa hitungannya manual.

## Catatan revisi 1.0.7 (2026-10-05)
- Judul tabel kini hanya "Angka promo"; semua label proses internal dihapus dari format dan contoh. Pemeriksaan internal memakai file sementara yang dihapus dan tidak pernah disebut. Klaim "paling banyak diambil"/"stok terbatas"/"laris" dilarang kecuali Anda yang memberi datanya.

## Catatan revisi 1.0.6 (2026-10-05)
- Balasan langsung dimulai dengan naskah. Hasil pemeriksaan internal (mis. "lulus cek-silang, 0 GAGAL") tidak lagi ikut tampil; masalah yang perlu Anda lengkapi disebut dengan bahasa biasa.

## Catatan revisi 1.0.5 (2026-10-01)
- Langkah wajib baru: AI menulis dulu "Fakta dari pengguna" (hanya yang Anda sebut), lalu setiap klaim di naskah harus bisa ditelusuri ke daftar itu.
- Script baru `scripts/cek_fakta.py` mencocokkan naskah dengan pesan Anda: jam live yang tidak Anda sebut, asal produk yang dikarang ("diambil dari Pekanbaru" padahal Anda hanya bilang *kirim* dari Pekanbaru), ukuran/isi, manfaat kesehatan, reputasi, dan urgensi palsu ditandai GAGAL dan wajib diperbaiki.
- Tanpa jam mulai, rundown memakai "menit 0–3" (atau [isi: jam mulai]) — tidak lagi memakai jam 19:00 diam-diam.

## Catatan revisi 1.0.4 (2026-10-01)
- Persen diskon dan harga akhir dijaga konsisten: bila harga dibulatkan, yang diucapkan adalah persen sebenarnya atau "hemat RpX". Contoh Pashmina diperbaiki.
- Detail produk yang tidak Anda berikan ditulis [isi: ...] atau arahan aksi, tidak dikarang.
- Jam mulai yang tidak diberikan memakai menit relatif dan dicatat di Asumsi.
