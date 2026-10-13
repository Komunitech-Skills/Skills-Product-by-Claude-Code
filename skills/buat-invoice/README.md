# Invoice & Kuitansi Rapi dalam Hitungan Menit

**Sebut item dan harganya, dapat invoice profesional yang angkanya dihitung skrip (bukan dikira-kira) dan siap dicetak.**

*Diuji AI penguji independen di OpenClaw: 7 → 9 dari 10 pada satu skenario invoice jasa (tanpa skill masih menulis "PPN 11%"; dengan skill tarif terbaru dan potongan pajak dari klien ikut dihitung; skor 9 didapat setelah perbaikan, sisi tanpa skill tidak diulang).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Nomor invoice berurutan, melanjutkan dari nomor terakhir yang Anda sebut (periksa sekilas sebelum dikirim)
- ✅ Diskon, ongkir, DP, termin, dan sisa tagihan dihitung otomatis, lengkap dengan terbilang (nominal ditulis dengan huruf)
- ✅ PPN 12% (pajak yang ditambahkan ke harga) sesuai aturan per 23 September 2026, hanya untuk penjual PKP (Pengusaha Kena Pajak, yaitu usaha yang sudah dikukuhkan untuk memungut PPN)
- ✅ Mengingatkan kapan wajib meterai Rp10.000
- ✅ Versi siap kirim (teks) dan siap cetak/PDF (berkas HTML yang dibuka di browser) tanpa aplikasi tambahan

## Cocok untuk siapa
- Freelancer dan penyedia jasa yang menagih klien
- UMKM, konveksi, katering, dan toko yang melayani pesanan partai
- Admin kantor yang butuh kuitansi DP atau pelunasan dengan cepat

## Contoh sebelum & sesudah
**Sebelum:** Mengetik invoice di Word, menghitung diskon dan sisa tagihan pakai kalkulator, lupa nomor terakhir.

**Sesudah (cukup ketik):** "Buatin invoice dari Konveksi Maju Fiktif ke SMP Contoh Nusantara: 120 kaos olahraga @85rb, 120 celana @70rb diskon 5%, sablon nama 120 x 10rb, ongkir 150rb. DP 6 juta udah ditransfer tgl 15 September. Jatuh tempo 30 hari. … Saya belum PKP."

*Cuplikan hasil nyata dari `examples/01-konveksi-seragam-dp.md` (bagian alamat dan rekening dipotong):*
```
**No.:** INV/2026/09/0013
**Jatuh tempo:** 23 Oktober 2026
**Status:** SEBAGIAN DIBAYAR
…
| 1 | Kaos olahraga | 120 pcs | Rp 85.000 | - | Rp 10.200.000 |
| 2 | Celana olahraga | 120 pcs | Rp 70.000 | Rp 420.000 (5%) | Rp 7.980.000 |
| 3 | Sablon nama siswa | 120 pcs | Rp 10.000 | - | Rp 1.200.000 |
| Subtotal | Rp 19.380.000 |
| Ongkos kirim | Rp 150.000 |
| **TOTAL** | **Rp 19.530.000** |
| Sudah dibayar - DP (15 September 2026) | -Rp 6.000.000 |
| **SISA TAGIHAN** | **Rp 13.530.000** |
Terbilang: _Tiga Belas Juta Lima Ratus Tiga Puluh Ribu Rupiah_
```
Hasil lengkapnya juga berupa file HTML yang siap dicetak.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan kuitansi pelunasan Rp7.500.000 dari Bu Sari untuk pesanan kue."
- "Invoice proyek website 15 juta, termin 30-30-40, saya PKP pakai PPN." (termin = pembayaran bertahap, di sini 30%, 30%, 40%)
- "Nomor invoice terakhir saya INV/2026/09/0007, buat yang berikutnya."

## Instalasi singkat
Salin folder `buat-invoice` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, dua sumber yang terpisah.
- **Uji OpenClaw, 1 Oktober 2026** (angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario invoice jasa konsultan): skor tanpa skill 7 → dengan skill 8 pada uji pertama, lalu 9 setelah perbaikan v1.0.4. Pembedanya: tanpa skill menulis "PPN 11%"; dengan skill PPN 12% (dihitung dari 11/12 harga sebelum PPN), potongan PPh 23 (pajak 2% yang dipotong klien perusahaan) Rp270.000, dan estimasi diterima bersih Rp14.715.000 dihitung skrip. Catatan jujur: pada skor 9 hanya sisi "dengan skill" yang diulang; sisi "tanpa skill" memakai skor uji pertama.
- **Uji simulasi agent, 23 September 2026** (`examples/00-pembanding-tanpa-skill.md`, invoice konveksi seragam, DP Rp6.000.000, sisa tagihan Rp13.530.000): agent tanpa skill menulis angka yang benar tetapi tanpa terbilang, tanpa penanda bea meterai, dan tanpa file siap cetak. Dengan skill semuanya ada, dan permintaan PPN dari penjual non-PKP ditolak.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Bot Telegram asli belum diuji. Invoice non-PKP, termin, dan PPh 23 tanpa NPWP belum diuji di OpenClaw.

## FAQ
**Bagaimana cara membuat PDF-nya?**
Buka file HTML yang dibuat di browser, tekan Cetak (Ctrl+P / Cmd+P), lalu pilih "Simpan sebagai PDF".

**Saya belum PKP, bisa tambah PPN?**
Tidak. Hanya PKP yang boleh menagih PPN, jadi skill akan menolak menambahkan PPN dan menjelaskan alasannya.

**Kapan invoice/kuitansi perlu meterai?**
Bila dokumen menyatakan uang yang diterima lebih dari Rp5.000.000, misalnya kuitansi pelunasan Rp7,5 juta. Skill akan menandainya dan menyediakan tempat meterai.

> **Catatan penting:** alat bantu membuat invoice, bukan nasihat pajak atau hukum. Invoice ini bukan faktur pajak (faktur pajak tetap dibuat lewat Coretax, sistem pajak online milik DJP). Dasar aturan (berlaku per 23 September 2026): PPN 12% dengan "DPP nilai lain" 11/12 (dasar hitung 11/12 dari harga sebelum PPN, hasil akhirnya setara 11% dari harga) untuk barang/jasa biasa, hanya untuk penjual PKP (UU HPP = Undang-Undang Harmonisasi Peraturan Perpajakan, PMK 131/2024 = Peraturan Menteri Keuangan, berlaku 1 Januari 2025); bea meterai Rp10.000 untuk dokumen yang menyatakan penerimaan uang lebih dari Rp5.000.000 (UU 10/2020); PPh 23 atas jasa 2% (pajak yang dipotong klien berbentuk badan dari pembayaran jasa), atau 4% bila tanpa NPWP (UU PPh Pasal 23). PPN dibulatkan ke bawah sekali dan pembulatan ini belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax. Untuk kasus khusus (mis. perlakuan ongkir) tanyakan ke konsultan pajak atau Kring Pajak 1500200.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
