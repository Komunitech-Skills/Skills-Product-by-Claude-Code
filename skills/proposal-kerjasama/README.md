# Proposal Kerja Sama yang Bikin Mitra Tertarik

**Ceritakan ide kerja samamu, dapat proposal rapi yang fokus pada untungnya calon mitra, lengkap dengan simulasi angka.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Proposal jadi dalam dua pilihan: 1 halaman ringkas atau versi lengkap
- ✅ Kerangka khusus untuk titip jual (konsinyasi), reseller/agen, pasokan ke kantor/kafe, sponsorship acara, dan kolaborasi brand
- ✅ Tabel simulasi bagi hasil, margin reseller, dan porsi titip jual dihitung otomatis, jadi angkanya pasti benar
- ✅ Sekaligus dapat pesan pengantar WhatsApp dan email untuk mengirim proposalnya
- ✅ Tidak mengarang klaim atau data yang tidak kamu berikan

## Cocok untuk siapa
- UMKM yang ingin menitipkan produk di kafe, toko oleh-oleh, atau minimarket lokal
- Pemilik brand yang sedang mencari reseller atau agen
- Panitia acara, komunitas, dan organisasi kampus yang mencari sponsor
- Pemasok dan penyedia jasa yang ingin masuk ke kantor, hotel, atau pabrik

## Contoh sebelum & sesudah
**Sebelum:** Bingung mulai dari mana, proposal jadi panjang tapi isinya memuji produk sendiri, dan calon mitra tidak membalas.

**Sesudah (cukup ketik):** "Bikin proposal titip jual keripik singkong ke 5 cabang Kopi Senja Jogja, harga 25rb, toko dapat 20%"
→ Proposal 1 halaman berisi skema titip jual, tabel pendapatan kafe per bulan (Rp 250.000–Rp 1.000.000 per cabang), tawaran uji coba 3 bulan, plus pesan WA pengantarnya.

**Hasil uji (OpenClaw, uji otomatis agent):** pada uji pertama rata-rata nilai 5,5 tanpa skill menjadi 8,0 dengan skill (skala 10). Tanpa skill, modal dan tulisan "rugi Rp1.000/botol" ikut masuk ke proposal untuk mitra; dengan skill, peringatan rugi hanya sampai ke kamu dan proposal ke mitra tetap bersih. Uji ulang v1.0.7: rata-rata 8,33 dengan skill, semua angka benar. Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`. Hasil di bot Telegram ada di bagian "Bukti uji di bot Telegram" di bawah. Claude Code diuji lewat simulasi agent; Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buat proposal sponsorship bazar UMKM kampus, ada paket platinum, gold, silver"
- "Proposal cari reseller untuk hijab, HET 150rb, diskon reseller 20%"
- "Proposal kerja sama katering makan siang untuk pabrik garmen 200 karyawan, versi lengkap"

## Instalasi singkat
Salin folder `proposal-kerjasama` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 9, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/827/835 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/828/837 — skor 8,5
Verdik gelombang: LULUS — DENGAN kini memberi peringatan rugi lengkap (laba per botol = Rp9.750 − HPP − kirim, contoh Rp3.750 / impas / rugi Rp1.250) plus proposal, pesan WA, dan email yang ditulis utuh tanpa kata proses; TANPA menolak klaim palsu dengan tepat tetapi tidak menghitung untung/rugi, tidak memberi pesan WA/email, dan mengarang komitmen (kirim rutin, tarik barang kedaluwarsa).

## FAQ
**Apakah modal dan keuntungan saya ikut tertulis di proposal?**
Tidak. Hitungan modal dan laba hanya ditunjukkan ke kamu. Proposal hanya berisi angka yang penting bagi mitra.

**Kalau mitra setuju, apakah proposal ini sudah jadi kontrak?**
Belum. Proposal adalah ajakan. Setelah sepakat, buat perjanjian tertulis (bisa dengan skill Perjanjian Sederhana).

**Bisa dalam bahasa Inggris?**
Bisa. Minta saja "buat versi bahasa Inggris" setelah proposal jadi.

## Riwayat perubahan

Versi terkini: **1.0.10**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
