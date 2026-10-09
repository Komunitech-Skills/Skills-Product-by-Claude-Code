# Tahu Kapan Kas Menipis, Sebelum Terlambat

**Proyeksi kas 13 minggu ke depan, lengkap dengan tanda bahaya dan jalan keluarnya — cukup ceritakan pemasukan dan pengeluaranmu.**

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

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Saya tidak punya data rapi, hanya perkiraan. Bisa?**
Bisa. Cukup jawab beberapa pertanyaan singkat dari AI (saldo sekarang, penjualan per minggu, pengeluaran rutin). Perkiraan kasar pun sudah sangat membantu, lalu perbarui tiap minggu.

**Apakah butuh Python?**
Sebaiknya ada (gratis, biasanya sudah ada di Mac/Linux; di Windows pasang dari python.org) agar angka dihitung pasti. Jika tidak ada, AI tetap menghitung manual langkah demi langkah dan memberi tahu kamu.

**Apakah data keuangan saya dikirim ke internet?**
Script berjalan di komputermu sendiri tanpa internet. Isi percakapan tetap dibaca oleh AI agent yang kamu pakai.

## Catatan revisi 1.0.3 (2026-10-01)
Perbaikan dari uji OpenClaw asli (arus kas 13 minggu, info kurang lalu dilengkapi):
- Script kini mencetak **kejadian per minggu** (pos masuk/keluar apa saja yang jatuh di tiap minggu) dan rincian minggu kritis. AI wajib mengutip nomor minggu dan pos dari daftar ini, sehingga tidak ada lagi salah sebut "cicilan di minggu 12" padahal di minggu 11.
- Pos yang ditanyakan tetapi belum dijawab (mis. BPJS, PPh 21) ditulis jelas sebagai "Belum termasuk" di Asumsi.
- Path script ditulis jelas (subfolder `scripts/`); AI dilarang mencari file ke seluruh disk.
