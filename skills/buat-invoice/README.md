# Invoice & Kuitansi Rapi dalam Semenit

**Sebut item dan harganya, dapat invoice profesional yang angkanya pasti benar dan siap dicetak.**

## Manfaat
- ✅ Nomor invoice otomatis dan berurutan
- ✅ Diskon, ongkir, DP, termin, dan sisa tagihan dihitung otomatis, lengkap terbilang
- ✅ PPN 12% sesuai aturan terbaru, hanya untuk penjual PKP
- ✅ Mengingatkan kapan wajib meterai Rp10.000
- ✅ Versi siap kirim (teks) dan siap cetak/PDF (HTML) tanpa aplikasi tambahan

## Cocok untuk siapa
- Freelancer dan penyedia jasa yang menagih klien
- UMKM, konveksi, katering, dan toko yang melayani pesanan partai
- Admin kantor yang butuh kuitansi DP atau pelunasan dengan cepat

## Contoh sebelum & sesudah
**Sebelum:** Mengetik invoice di Word, menghitung diskon dan sisa tagihan pakai kalkulator, lupa nomor terakhir.

**Sesudah (cukup ketik):** "Buat invoice ke PT Pelanggan: 100 kaos @65 ribu diskon 5%, desain 500 ribu, ongkir 75 ribu, DP 3 juta sudah masuk."
→ Invoice lengkap: total Rp6.750.000, sisa tagihan Rp3.750.000, terbilang, rekening, jatuh tempo, dan file HTML siap dicetak.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan kuitansi pelunasan Rp7.500.000 dari Bu Sari untuk pesanan kue."
- "Invoice proyek website 15 juta, termin 30-30-40, saya PKP pakai PPN."
- "Nomor invoice terakhir saya INV/2026/09/0007, buat yang berikutnya."

## Instalasi singkat
Salin folder `buat-invoice` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Bagaimana cara membuat PDF-nya?**
Buka file HTML yang dibuat di browser, tekan Cetak (Ctrl+P / Cmd+P), lalu pilih "Simpan sebagai PDF".

**Saya belum PKP, bisa tambah PPN?**
Tidak. Hanya PKP yang boleh menagih PPN, jadi skill akan menolak menambahkan PPN dan menjelaskan alasannya.

**Kapan invoice/kuitansi perlu meterai?**
Bila dokumen menyatakan uang yang diterima lebih dari Rp5.000.000, misalnya kuitansi pelunasan Rp7,5 juta. Skill akan menandainya dan menyediakan tempat meterai.
