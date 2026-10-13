# Balas Chat Pelanggan Cepat, Ramah, Tanpa Salah Janji

**Tempel chat pelanggan, dapat balasan siap kirim yang menenangkan dan menyelesaikan masalah.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Balasan pertanyaan stok, ongkir, cara order, dan pembayaran dalam hitungan detik
- ✅ Komplain barang rusak, telat, atau salah kirim ditangani dengan alur minta maaf, beri solusi, lalu tindak lanjut
- ✅ Bisa membuat "bank jawaban" 15–30 template quick reply dari info tokomu
- ✅ Nada menyesuaikan brand: santai, ramah, atau formal
- ✅ Aman: tidak mengarang stok, ongkir, atau kebijakan retur, dan tidak menjanjikan hal yang belum kamu setujui

## Cocok untuk siapa
- Pemilik online shop dan admin CS di WhatsApp, Shopee, Tokopedia, atau TikTok Shop
- Usaha kuliner, fashion, skincare, dan jasa yang chat-nya ramai setiap hari
- Pemilik usaha yang ingin admin baru langsung bisa membalas dengan standar yang sama

## Contoh sebelum & sesudah
**Sebelum:** Pelanggan marah karena warna pashmina salah, admin panik dan membalas "maaf kak, nanti dicek".

**Sesudah (cukup ketik):** "Pembeli komplain pashmina dusty pink yang datang malah mocca, mau dipakai kondangan Sabtu. Kita bisa tukar, ongkir kita tanggung"
→ Balasan yang meminta maaf dengan tulus, meminta foto, menawarkan tukar dengan ongkir ditanggung, dan menjanjikan kabar resi jam 17.00, plus catatan hal yang perlu dicek admin.

**Hasil uji (OpenClaw, uji otomatis agent, uji ulang v1.0.3, 2026-10-01):** rata-rata nilai 6,5 tanpa skill menjadi 8,25 dengan skill (skala 10). Tanpa skill, AI mengarang voucher toko, gratis ongkir, dan diskon yang tidak pernah Anda tawarkan; dengan skill, balasan hanya memakai kebijakan toko yang Anda berikan, menanggapi permintaan refund pembeli, dan menandai bagian yang perlu Anda konfirmasi. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Balas chat ini: 'kak paketku udah 5 hari belum sampe'"
- "Buatin bank jawaban CS untuk toko sambal kemasan, kirim pakai JNE & SiCepat, bayar transfer BCA & QRIS"
- "Bikin auto reply WA di luar jam kerja, toko buka Senin–Sabtu 08.00–17.00"

## Instalasi singkat
Salin folder `balas-chat-cs` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apa bedanya dengan skill balas ulasan?**
Skill ini untuk chat pribadi dengan pelanggan (WA atau chat marketplace). Untuk membalas ulasan bintang yang tampil publik, pakai skill Balas Ulasan Pelanggan.

**Apakah bisa langsung terhubung ke WhatsApp atau Shopee saya?**
Tidak. Kamu menempelkan chat-nya, lalu menyalin balasan yang dibuat. Data tokomu tidak dikirim ke mana pun oleh skill ini.

**Bagaimana kalau info tokoku belum lengkap?**
Balasan tetap dibuat, dengan bagian `[isi ...]` yang tinggal kamu lengkapi, misalnya estimasi restok atau nomor rekening.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
