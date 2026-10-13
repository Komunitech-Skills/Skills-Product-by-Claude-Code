# Landing Page Jualan Sekali Jadi, Siap Kirim ke Pembeli

**Ceritakan produkmu, dapat halaman jualan lengkap — headline, manfaat, penawaran, FAQ, sampai tombol WhatsApp — siap tempel ke website atau link-in-bio.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Struktur lengkap yang terbukti (headline → masalah → manfaat → bukti sosial → penawaran → garansi → FAQ → CTA), bukan asal susun paragraf jualan
- ✅ Tombol CTA otomatis dibentuk jadi tautan WhatsApp yang benar (`wa.me`) lengkap pesan siap kirim — dihitung script, bukan ditulis manual dan salah encode
- ✅ 3 variasi headline sekaligus untuk dites, plus meta title & meta description SEO dengan panjang karakter dihitung persis
- ✅ Dijaga tidak melanggar aturan: tidak akan mengarang testimoni/rating/angka penjualan, dan menandai klaim berisiko (kesehatan, BPOM, halal, harga coret) sebelum kamu publish
- ✅ Ada versi pendek untuk link-in-bio/halaman satu layar HP, bukan cuma versi panjang

## Cocok untuk siapa
- Pemilik UMKM (makanan, fashion, jasa servis, kursus) yang mau jualan lewat website/landing page sendiri, bukan lewat marketplace
- Pemilik usaha yang link-in-bio Instagram/TikTok-nya masih sekadar daftar link tanpa cerita jualan
- Freelancer/jasa (servis AC, klinik gigi, tukang, guru les) yang butuh halaman jualan tapi tidak sanggup bayar copywriter
- **Bukan untuk:** caption sosmed (pakai `caption-sosmed-umkm`), judul/deskripsi Shopee/Tokopedia/TikTok Shop (pakai `listing-marketplace`), atau broadcast WA (pakai `broadcast-wa`)

## Contoh sebelum & sesudah
**Sebelum:** "Jual keripik pedas enak dan murah, order chat aja ya kak 😊" — ditempel di halaman kosong tanpa struktur, tanpa CTA jelas, tanpa jawaban keberatan calon pembeli.

**Sesudah (cukup ketik):** "Buatkan landing page untuk keripik pedas saya, harga 25 ribu"
→ Headline "Ngemil Pedas Sepuasnya, Tanpa Ribet Mikirin Kadaluarsa", struktur lengkap masalah-manfaat-penawaran-garansi-FAQ, 3 variasi headline untuk dites, meta title/description SEO terukur, dan tombol `https://wa.me/62...` siap klik. Lihat contoh penuh di `examples/uji-pembuat-01-keripik-pedas.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan landing page untuk keripik pedas saya, harga 25 ribu"
- "Bikin halaman jualan jasa servis AC, format link in bio"
- "Perbaiki landing page kursus online saya ini biar CTA-nya jelas: <tempel teks lama>"

Kalau info produkmu belum lengkap, AI akan tanya sekali dalam satu pesan (nomor WA, harga, cara bayar, dll). Kalau kamu buru-buru, bilang saja "pakai default aja" — nanti asumsinya disebutkan di akhir supaya kamu tinggal sesuaikan.

## Instalasi singkat
Salin folder `copy-landing-page` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

## FAQ
**Apakah testimoni/rating di halaman jualan dibuatkan otomatis?**
Tidak. Skill ini sengaja **tidak pernah mengarang** testimoni, rating bintang, atau angka penjualan — itu melanggar kepercayaan pembeli dan berisiko hukum. Kalau kamu belum punya testimoni asli, bagian itu ditandai placeholder yang bisa kamu isi belakangan.

**Produk saya makanan/kosmetik, boleh tulis "halal" atau klaim sehat?**
Hanya kalau kamu memang sudah punya sertifikat resmi (BPJPH/MUI untuk halal, izin edar BPOM untuk klaim kesehatan/kosmetik). Kalau belum, skill tidak akan menuliskannya — akan diganti kalimat manfaat umum yang aman, dan ditandai di ceklis kepatuhan di akhir output.

**Harus pakai Python?**
Tidak wajib. Kalau Python ada, tautan WhatsApp dan panjang meta title/description dihitung otomatis lewat script. Kalau tidak ada, AI agent tetap menyusun halamannya dan menghitung manual, lalu memberitahumu untuk dicek sekali sebelum dipakai.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
