# Balas Ulasan Bintang 1 Tanpa Emosi

**Tempel ulasan pelanggan, dapat balasan yang menenangkan, aman, dan membuat calon pembeli tetap percaya.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Balasan untuk ulasan positif, netral, dan negatif di Shopee, Tokopedia, TikTok Shop, dan Google Maps
- ✅ Nada tenang dan tidak defensif, jadi calon pembeli melihat tokomu bertanggung jawab
- ✅ Dicek otomatis: tidak ada nomor pesanan, resi, alamat, atau nomor HP pembeli yang ikut terpajang
- ✅ Keluhan diarahkan ke chat pribadi, lengkap dengan pesan chat pembukanya
- ✅ Aman dari pelanggaran: tidak ada tawaran voucher untuk ganti bintang atau ajakan ke WA di marketplace

## Cocok untuk siapa
- Seller marketplace yang sering dapat ulasan "barang telat" atau "paket rusak"
- Pemilik rumah makan, kafe, salon, dan bengkel yang ulasannya muncul di Google Maps
- Admin CS yang ingin balasan konsisten tapi tidak terasa template

## Contoh sebelum & sesudah
**Sebelum:** "Kak, seharusnya baca deskripsi dulu. Pengiriman itu salah kurir, bukan salah kami." (pembeli lain ikut ilfeel)

**Sesudah (cukup ketik):** "Balasin ulasan bintang 1: paket nyampe 6 hari, botol sambal bocor. Kami mau ganti kalau ada video unboxing."
→ Balasan publik yang minta maaf dan mengajak ke chat toko, versi singkat, pesan chat pribadi yang meminta video unboxing, dan hasil pengecekan.

**Hasil uji (angka nyata):** uji banding tanpa vs dengan skill oleh agen penguji independen (simulasi Claude Code; ulasan Shopee bintang 1 "gamis ukuran L yang datang M").
- Tanpa skill: balasan memuat 2 pelanggaran kebijakan marketplace sekaligus, yaitu mengajak ke WhatsApp lengkap dengan nomor dan meminta pembeli mengubah rating. Alasan keterlambatan ("lonjakan pesanan") dikarang dan janji ongkir retur ditulis di depan umum.
- Dengan skill: 0 pelanggaran; balasan publik 358 dari batas 500 karakter dan mengarah ke chat toko, ditambah pesan chat pribadi siap kirim dan urutan "chat pribadi dulu, baru posting balasan publik".
- Skor penguji independen: 8 dari 10 (lulus uji).

Uji OpenClaw 2026-10-01: 5,5 → 8,25 (rata-rata dua skenario ulasan; 8,5 setelah perbaikan dan uji ulang) (lihat `examples/00-openclaw-sebelum-sesudah.md`).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Bantu balas review Google Maps ini: <tempel ulasan>"
- "Balasin 5 ulasan Shopee ini sekaligus, ada yang bintang 5 dan ada yang bintang 2"
- "Bikin template balasan ulasan buat admin toko saya"

## Instalasi singkat
Salin folder `balas-ulasan-pelanggan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## FAQ
**Bolehkah menawarkan voucher supaya pembeli mengubah bintangnya?**
Tidak. Marketplace dan Google melarang imbalan untuk mengubah ulasan. Skill tetap membantu kamu memberi solusi yang tulus lewat chat pribadi, tanpa syarat ulasan.

**Bagaimana kalau ulasannya palsu atau dari pesaing?**
Skill membuat balasan yang tetap sopan dan netral, lalu menyarankan kamu melaporkan ulasan itu lewat fitur yang disediakan platform.

**Apakah balasannya diposting otomatis?**
Tidak. Kamu tinggal menyalin dan menempelkannya sendiri, jadi tetap bisa dicek dulu.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
