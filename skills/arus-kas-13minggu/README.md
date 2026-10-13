# Tahu Kapan Kas Menipis, Sebelum Terlambat

**Proyeksi kas 13 minggu ke depan, lengkap dengan tanda bahaya dan jalan keluarnya — cukup ceritakan pemasukan dan pengeluaranmu.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tahu persis **minggu ke berapa** uang usaha bakal kurang dan berapa kurangnya
- ✅ Tanggal gajian, sewa, cicilan, dan pajak otomatis ditempatkan di minggu yang benar
- ✅ 3–5 jalan keluar konkret (tagih lebih cepat, atur termin supplier, tunda belanja) **beserta hitungan dampaknya**
- ✅ File CSV siap buka di Excel/Google Sheets untuk dipantau tiap minggu
- ✅ Angka dihitung script, bukan dikira-kira

## Cocok untuk siapa
- Pemilik UMKM yang sering deg-degan menjelang tanggal gajian atau jatuh tempo supplier
- Usaha dengan pelanggan yang membayar belakangan (termin/tempo)
- Admin keuangan yang diminta atasan membuat rencana kas 3 bulan

## Contoh sebelum & sesudah
**Sebelum:** "Kayaknya aman sih…" — lalu tiba-tiba kas habis tepat saat gajian karena pembayaran pelanggan baru masuk minggu depannya.

**Sesudah (cukup ketik):** "Kas saya 20 juta, jualan 12 juta seminggu, gaji 18 juta tiap tanggal 25, sewa 6,5 juta tiap tanggal 1, bahan 7 juta/minggu, PT Sinar bayar 15 juta awal Desember. Aman nggak sampai akhir tahun?"
→ Tabel 13 minggu dengan tanda 🟢🟡🔴, penjelasan bahwa minggu 23–29 November kas tinggal Rp 0, dan pilihan tindakan seperti "minta PT Sinar bayar 2 minggu lebih awal" beserta hasil hitungannya, plus file Excel.

**Hasil uji A/B (simulasi agent, 23 September 2026):** usaha katering dengan kas Rp 35 juta. Jawaban tanpa skill per bulan: "aman, saldo terendah sekitar Rp 14,9 juta". Padahal di minggu ke-6 (2–8 November) saldo tinggal Rp 6.300.000 karena freezer, sewa, dan bahan jatuh di minggu yang sama. Dengan skill titik kritis itu ketemu, lengkap dengan 5 opsi tindakan berangka; saldo 13 minggu cocok dengan hitungan independen (13 dari 13 minggu). Rincian: `examples/00-pembanding-tanpa-skill.md`. Uji OpenClaw 1 Okt 2026: skor tanpa skill 7,5 → dengan skill 8,5, lalu 9 setelah perbaikan v1.0.3 (lihat `examples/00-openclaw-sebelum-sesudah.md`).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan proyeksi arus kas 13 minggu dari data ini: …"
- "Uang usaha saya cukup nggak buat bayar THR bulan depan?"
- "Kalau saya beli mesin 25 juta bulan depan, kas saya aman?"

## Instalasi singkat
Salin folder `arus-kas-13minggu` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## FAQ
**Saya tidak punya data rapi, hanya perkiraan. Bisa?**
Bisa. Cukup jawab beberapa pertanyaan singkat dari AI (saldo sekarang, penjualan per minggu, pengeluaran rutin). Perkiraan kasar pun sudah sangat membantu, lalu perbarui tiap minggu.

**Apakah butuh Python?**
Sebaiknya ada (gratis, biasanya sudah ada di Mac/Linux; di Windows pasang dari python.org) agar angka dihitung pasti. Jika tidak ada, AI tetap menghitung manual langkah demi langkah dan memberi tahu kamu.

**Apakah data keuangan saya dikirim ke internet?**
Script berjalan di komputermu sendiri tanpa internet. Isi percakapan tetap dibaca oleh AI agent yang kamu pakai.

> **Catatan penting:** proyeksi dari angka dan jadwal yang kamu berikan, bukan ramalan, bukan jaminan, dan bukan nasihat keuangan profesional. Pos yang belum kamu sebut (mis. BPJS atau PPh 21) ditulis "Belum termasuk", dan kewajiban yang jatuh setelah minggu ke-13 diperingatkan terpisah. Untuk keputusan besar (PHK, jual aset, restrukturisasi utang) diskusikan dengan akuntan atau konsultan.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
