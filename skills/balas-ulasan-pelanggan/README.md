# Balas Ulasan Bintang 1 Tanpa Emosi

**Tempel ulasan pelanggan, dapat balasan yang menenangkan, aman, dan membuat calon pembeli tetap percaya.**

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

## FAQ
**Bolehkah menawarkan voucher supaya pembeli mengubah bintangnya?**
Tidak. Marketplace dan Google melarang imbalan untuk mengubah ulasan. Skill tetap membantu kamu memberi solusi yang tulus lewat chat pribadi, tanpa syarat ulasan.

**Bagaimana kalau ulasannya palsu atau dari pesaing?**
Skill membuat balasan yang tetap sopan dan netral, lalu menyarankan kamu melaporkan ulasan itu lewat fitur yang disediakan platform.

**Apakah balasannya diposting otomatis?**
Tidak. Kamu tinggal menyalin dan menempelkannya sendiri, jadi tetap bisa dicek dulu.

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw (klinik): balasan publik Google Maps menyebut "saat periksa gigi putra/putri Bapak" — mengonfirmasi perawatan pasien di ruang publik.
- Aturan baru khusus klinik/faskes: balasan publik tidak menyebut status pasien, kunjungan, tindakan, atau kondisi kesehatan, dan mengalihkan ke kanal pribadi (rahasia kesehatan UU 17/2023 Ps. 301; data kesehatan = data pribadi spesifik UU 27/2022 Ps. 4 ayat (2) huruf a). `cek_balasan.py --faskes` menandai GAGAL frasa semacam itu. Ditambah 3 uji regresi. **PERLU REVIEW** tenaga medis/kepatuhan.
