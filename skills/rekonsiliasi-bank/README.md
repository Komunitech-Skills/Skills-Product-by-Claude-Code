# Cocokkan Mutasi Bank dengan Invoice, Otomatis

**Kirim file mutasi rekening dan daftar penjualan — dalam semenit tahu transfer mana yang sudah masuk, mana yang belum, dan dari mana selisihnya.**

## Manfaat
- ✅ Membaca ekspor mutasi BCA, Mandiri, BRI, BNI, dan bank lain (kolom dikonfirmasi dulu, jadi tidak salah baca)
- ✅ Mengenali kasus yang bikin pusing: pelanggan bayar 2 invoice sekaligus, invoice dicicil, transfer terpotong biaya, tanggal meleset
- ✅ Penjelasan selisih yang angkanya **pas** — bukan sekadar "ada beda Rp 5 juta"
- ✅ Daftar tindakan: siapa yang perlu ditagih, uang masuk mana yang belum dicatat
- ✅ Nomor rekening disamarkan otomatis; data diproses di komputermu sendiri

## Cocok untuk siapa
- Pemilik usaha yang menerima banyak transfer dari pelanggan
- Admin keuangan yang tiap akhir bulan mencocokkan rekening koran dengan invoice
- Usaha jasa/B2B dengan pembayaran termin atau dicicil

## Contoh sebelum & sesudah
**Sebelum:** Mencentang satu per satu mutasi bank di kertas, 2–3 jam, dan tetap ada selisih yang tidak ketemu.

**Sesudah (cukup ketik):** "Tolong cocokkan mutasi-bca-september.csv dengan invoice-september.csv"
→ Laporan: 3 cocok, 4 perlu dicek (termasuk "Andi bayar 2 invoice sekaligus Rp 3.000.000"), 1 invoice belum masuk (Joko Rp 1.250.000), 2 uang masuk belum dicatat — plus penjelasan selisih Rp 5.245.154 yang seimbang dan file Excel.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Rekonsiliasi mutasi Mandiri bulan ini dengan daftar penjualan saya"
- "Cek transfer pelanggan mana yang belum masuk rekening"
- "Cocokkan pembayaran ke supplier di mutasi BRI dengan catatan pembelian"

## Instalasi singkat
Salin folder `rekonsiliasi-bank` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah data rekening saya aman?**
Script berjalan di komputermu tanpa internet dan tidak menyimpan apa pun selain file hasil yang kamu minta. Isi file tetap dibaca oleh AI agent yang kamu pakai, jadi hapus baris nomor rekening di atas file bila tidak diperlukan. Skill ini tidak pernah meminta PIN, password, atau OTP.

**Mutasi saya hanya PDF. Bisa?**
Sebaiknya unduh ulang dalam format CSV/Excel dari internet banking. Jika tidak bisa, salin tabelnya ke Excel lalu simpan sebagai CSV.

**Bagaimana jika pencocokannya salah?**
Hasil yang tidak pasti ditandai "perlu dicek", bukan dianggap benar. Menambahkan kolom nomor invoice atau nama pelanggan di catatan membuat hasil jauh lebih akurat.
