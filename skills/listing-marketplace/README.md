# Listing Shopee, Tokopedia, TikTok Shop Sekali Jadi

**Ceritakan produkmu, dapat judul, deskripsi, dan kata kunci yang siap tempel ke tiga marketplace.**

## Manfaat
- ✅ Judul otomatis disesuaikan batas karakter tiap platform, jadi tidak terpotong atau ditolak
- ✅ Kata kunci yang biasa diketik pembeli ditaruh di awal judul agar lebih mudah ditemukan
- ✅ Deskripsi rapi dan lengkap: keunggulan, spesifikasi, isi paket, cara pakai, siap tempel
- ✅ Dicek otomatis: nomor WA, link, @akun, dan klaim berisiko ("halal", "BPOM", "termurah") yang bisa bikin produk diturunkan
- ✅ Tidak mengarang: data yang belum kamu berikan ditandai `[isi: ...]`

## Cocok untuk siapa
- Seller Shopee, Tokopedia, dan TikTok Shop yang upload produk baru setiap minggu
- Pemilik toko yang listingnya sepi pengunjung dan ingin diperbaiki
- Admin toko online yang mengelola satu produk di beberapa marketplace

## Contoh sebelum & sesudah
**Sebelum:** Judul "SAMBAL ENAK MURAH!!! 🔥🔥 ORDER WA 0812xxxx" — terpotong di Tokopedia dan berisiko kena penalti.

**Sesudah (cukup ketik):** "Bikinin listing sambal cumi asin 200 ml, 2 level pedas, tanpa pengawet, sudah PIRT, buat Shopee dan Tokopedia"
→ Judul "Sambal Cumi Asin Pedas 200 ml Tanpa Pengawet Oleh Oleh Sidoarjo" (63/70 karakter), deskripsi lengkap, daftar kata kunci, dan hasil pengecekan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatin judul dan deskripsi Shopee buat gamis busui bahan ceruty, size M–XXL"
- "Perbaiki listing Tokopedia ini biar lebih gampang dicari: <tempel judul & deskripsi lama>"
- "Cariin kata kunci buat jual tumbler stainless 500 ml di TikTok Shop"

## Instalasi singkat
Salin folder `listing-marketplace` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## FAQ
**Apakah batas karakternya pasti sesuai aturan terbaru marketplace?**
Skill memakai batas aman yang sama atau lebih ketat dari batas yang pernah berlaku, dan selalu mengingatkan kamu untuk cek batas terbaru di Seller Center. Kalau kamu tahu angka terbarunya, sebutkan saja dan skill akan memakainya.

**Kalau produk saya belum punya sertifikat halal atau BPOM?**
Skill tidak akan menuliskannya. Klaim tanpa bukti bisa membuat produk diturunkan dan melanggar aturan perlindungan konsumen.

**Harus pakai Python?**
Tidak wajib. Kalau Python ada, pengecekan panjang teks dan kata terlarang berjalan otomatis. Kalau tidak ada, AI agent akan mengecek manual dan memberi tahu kamu.

## Catatan revisi 1.0.4 (2026-10-01)
- Temuan uji ulang OpenClaw: panjang deskripsi yang dilaporkan (505) beda dengan teks yang ditampilkan (515).
- Kini angka panjang wajib diambil dari run script terakhir pada teks final yang persis sama dengan yang ditampilkan.

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw: AI sempat menambah klaim "ga gampang buyar" yang tidak disebut pemilik, dan cek otomatis tetap lulus.
- Aturan baru: setiap sifat/klaim produk harus berasal dari kata-kata pemilik. Script `cek_listing.py` kini menerima `--fakta`/`--fakta-file` dan menandai GAGAL frasa sifat/layanan ("awet", "anti …", "tidak mudah …", "dikirim cepat", "packing aman") yang tidak ada di fakta. Ditambah 4 uji regresi.
