# Surat Penawaran Harga Rapi dalam 1 Menit

**Sebutkan barang dan harganya, dapat surat penawaran resmi plus teks WhatsApp-nya, dengan hitungan dari kalkulator bawaan, bukan dikira-kira.**

Diuji AI penguji independen di OpenClaw: 7 → 8 dari 10 (selisih kecil karena angka sudah benar di kedua sisi; pembedanya surat lengkap dengan keterangan PPN yang tidak menyesatkan, terbilang, daftar asumsi, dan teks WhatsApp siap kirim).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Surat penawaran lengkap: kop, nomor surat otomatis, tabel harga, total, terbilang, masa berlaku, syarat bayar & kirim
- ✅ Hitungan diskon, ongkir, dan PPN dikerjakan oleh kalkulator bawaan, bukan dikira-kira
- ✅ PPN mengikuti aturan terbaru (12% × DPP 11/12, yaitu 11/12 dari harga sebelum pajak) dan tidak dimunculkan bila usaha Anda belum PKP (Pengusaha Kena Pajak); pembulatan PPN belum dicocokkan dengan Coretax (sistem pajak online DJP)
- ✅ Sekaligus dapat versi pesan WhatsApp singkat yang sopan untuk dikirim ke calon pembeli
- ✅ Gampang direvisi: "diskonnya jadi 7%", "tambah 5 unit", "perpanjang sampai akhir bulan"

## Cocok untuk siapa
- Supplier, toko bangunan, katering, percetakan, vendor event, dan jasa yang sering diminta "quotation"
- Pemilik UMKM yang mulai melayani kantor, sekolah, atau instansi
- Admin sales yang tiap hari mengetik ulang penawaran di Word

## Contoh sebelum & sesudah
**Sebelum:** 30–60 menit menyalin template Word, menghitung PPN dengan kalkulator HP, dan takut salah angka.

**Sesudah (cukup ketik):** "Saya CV Teknik Mandiri Fiktif, Surabaya, sudah PKP. Mau kirim penawaran ke Klinik Sehat Sentosa Fiktif, Pak dr. Budi (pemilik). 5 unit AC split 1 PK @4.250.000, jasa pasang + pipa 3 meter 350rb per titik, ongkir 200rb. Harga belum PPN. Berlaku seminggu aja karena harga AC naik terus. Pembayaran 30% DP, sisanya setelah terpasang. Nomor surat 7."

Cuplikan surat (dipotong; DPP = harga sebelum pajak; dari `examples/03-ac-pkp-dengan-ongkir.md`):
```
Nomor    : 007/SPH/TMF/IX/2026
Perihal  : Penawaran Harga Pengadaan dan Pemasangan AC Split
| No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
|---|---|---|---|---|---|---|
| 1 | AC split 1 PK | 5 | unit | Rp 4.250.000 | - | Rp 21.250.000 |
| 2 | Jasa pasang + pipa 3 m | 5 | titik | Rp 350.000 | - | Rp 1.750.000 |
| Subtotal | Rp 23.000.000 |
| Ongkos kirim | Rp 200.000 |
| DPP | Rp 23.200.000 |
| PPN 12% (DPP nilai lain 11/12 = Rp 21.266.667) | Rp 2.552.000 |
| **TOTAL** | **Rp 25.752.000** |
Terbilang: *Dua Puluh Lima Juta Tujuh Ratus Lima Puluh Dua Ribu Rupiah*
…
2. Penawaran berlaku sampai 30 September 2026 mengingat fluktuasi harga unit AC.
```
Surat lengkapnya juga memuat kop, syarat pembayaran dan pengiriman, serta teks WhatsApp siap kirim.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bikin surat penawaran harga katering 150 nasi box buat panitia seminar"
- "Quotation jasa desain logo + kemasan untuk klien, harga sudah termasuk PPN"
- "Revisi penawaran kemarin, diskon totalnya jadi 5%"

## Instalasi singkat
Salin folder `surat-penawaran-harga` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (jujur):** dua sumber yang terpisah, skor 1–10.
- **Uji perbandingan oleh penguji independen (simulasi agent; skor kualitas 8/10):** 400 surat acak (diskon baris dan total, ongkir, non-PKP/PKP, harga termasuk PPN) dicocokkan dengan hitungan independen: 0 selisih. Pada uji A/B untuk percetakan non-PKP, surat tanpa skill menulis "belum termasuk pajak" (menyesatkan), masa berlaku tanpa tanggal, nomor surat tanpa kode usaha, dan tanpa teks WhatsApp; dengan skill: "Harga tidak dikenakan PPN", berlaku sampai tanggal pasti, nomor baku `045/SPH/PSJ/IX/2026`, plus teks WA siap kirim. Rincian: `examples/HASIL-UJI.md` dan `examples/00-pembanding-tanpa-skill.md`.
- **Uji OpenClaw, 2026-10-01** (uji otomatis agent, satu skenario surat; angka dari `examples/00-openclaw-sebelum-sesudah.md`): 7 → 8 (8 pada uji ulang terakhir; selisih kecil). Temuannya diperbaiki di versi 1.0.3 sampai 1.0.5 (rincian di `CHANGELOG.md`). Uji ulang terakhir memakai v1.0.4; perbaikan v1.0.5 belum diuji ulang di OpenClaw.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Usaha saya belum PKP, apakah tetap bisa?**
Bisa, justru itu pengaturan bawaannya. Surat dibuat tanpa PPN dan diberi keterangan "Harga final; penjual bukan PKP sehingga tidak memungut PPN."

**Apakah surat ini bisa jadi faktur pajak?**
Tidak. Surat penawaran hanya penawaran. Faktur pajak tetap dibuat lewat Coretax (sistem pajak online DJP) oleh PKP. Untuk tagihan, pakai skill Invoice & Kuitansi.

**Harus install Python?**
Tidak wajib. Jika komputer punya Python, angka dihitung otomatis oleh kalkulator bawaan. Jika tidak, AI tetap menghitung langkah demi langkah dan memberi tanda agar Anda mengecek ulang.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
