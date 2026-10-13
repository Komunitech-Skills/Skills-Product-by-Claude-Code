# Invoice & Kuitansi Rapi dalam Semenit

**Sebut item dan harganya, dapat invoice profesional yang angkanya pasti benar dan siap dicetak.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

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

**Hasil uji A/B (simulasi agent, 23 September 2026):** untuk permintaan invoice konveksi seragam (DP Rp6.000.000, sisa tagihan Rp13.530.000), agent tanpa skill menulis angka yang benar tetapi tanpa terbilang, tanpa penanda bea meterai, dan tanpa file siap cetak. Dengan skill semuanya ada, dan permintaan PPN dari penjual non-PKP ditolak. Rincian: `examples/00-pembanding-tanpa-skill.md`. Uji OpenClaw 1 Okt 2026: skor tanpa skill 7 → dengan skill 8 pada uji pertama, lalu 9 setelah perbaikan v1.0.4 (lihat `examples/00-openclaw-sebelum-sesudah.md`).

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

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## FAQ
**Bagaimana cara membuat PDF-nya?**
Buka file HTML yang dibuat di browser, tekan Cetak (Ctrl+P / Cmd+P), lalu pilih "Simpan sebagai PDF".

**Saya belum PKP, bisa tambah PPN?**
Tidak. Hanya PKP yang boleh menagih PPN, jadi skill akan menolak menambahkan PPN dan menjelaskan alasannya.

**Kapan invoice/kuitansi perlu meterai?**
Bila dokumen menyatakan uang yang diterima lebih dari Rp5.000.000, misalnya kuitansi pelunasan Rp7,5 juta. Skill akan menandainya dan menyediakan tempat meterai.

> **Catatan penting:** alat bantu membuat invoice, bukan nasihat pajak atau hukum. Invoice ini bukan faktur pajak (faktur pajak tetap dibuat lewat Coretax). Dasar aturan (berlaku per 23 September 2026): PPN 12% dengan DPP nilai lain 11/12 untuk barang/jasa biasa, hanya untuk penjual PKP (UU HPP, PMK 131/2024, berlaku 1 Januari 2025); bea meterai Rp10.000 untuk dokumen yang menyatakan penerimaan uang lebih dari Rp5.000.000 (UU 10/2020); PPh 23 atas jasa 2%, atau 4% bila tanpa NPWP (UU PPh Pasal 23). PPN dibulatkan ke bawah sekali dan pembulatan ini belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax. Untuk kasus khusus (mis. perlakuan ongkir) tanyakan ke konsultan pajak atau Kring Pajak 1500200.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
