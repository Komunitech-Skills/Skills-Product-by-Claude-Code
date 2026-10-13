# Surat Penawaran Harga Rapi dalam 1 Menit

**Sebutkan barang dan harganya, dapat surat penawaran resmi plus teks WhatsApp-nya, dengan hitungan yang pasti benar.**

## Manfaat
- ✅ Surat penawaran lengkap: kop, nomor surat otomatis, tabel harga, total, terbilang, masa berlaku, syarat bayar & kirim
- ✅ Hitungan diskon, ongkir, dan PPN dikerjakan oleh kalkulator bawaan, bukan dikira-kira
- ✅ PPN mengikuti aturan terbaru (12% × DPP 11/12) dan otomatis tidak muncul kalau usahamu belum PKP
- ✅ Sekaligus dapat versi pesan WhatsApp singkat yang sopan untuk dikirim ke calon pembeli
- ✅ Gampang direvisi: "diskonnya jadi 7%", "tambah 5 unit", "perpanjang sampai akhir bulan"

## Cocok untuk siapa
- Supplier, toko bangunan, katering, percetakan, vendor event, dan jasa yang sering diminta "quotation"
- Pemilik UMKM yang mulai melayani kantor, sekolah, atau instansi
- Admin sales yang tiap hari mengetik ulang penawaran di Word

## Contoh sebelum & sesudah
**Sebelum:** 30–60 menit menyalin template Word, menghitung PPN dengan kalkulator HP, dan takut salah angka.

**Sesudah (cukup ketik):** "Buatin SPH dari CV Maju Kreasi (PKP) ke PT Sinar Logistik, 10 kursi @1.250.000 diskon 5%, 10 meja @950rb, potongan 250rb, ongkir 300rb, nomor urut 12"
→ Surat bernomor `012/SPH/MKS/IX/2026` dengan total Rp 23.781.750 (sudah PPN), terbilang, berlaku 14 hari, plus teks WA siap kirim.

**Hasil uji (penguji independen, simulasi agent; skor kualitas 8/10):** 400 surat acak (diskon baris dan total, ongkir, non-PKP/PKP, harga termasuk PPN) dicocokkan dengan hitungan independen: 0 selisih. Pada uji A/B untuk percetakan non-PKP, surat tanpa skill menulis "belum termasuk pajak" (menyesatkan), masa berlaku tanpa tanggal, nomor surat tanpa kode usaha, dan tanpa teks WhatsApp; dengan skill: "Harga tidak dikenakan PPN", berlaku sampai tanggal pasti, nomor baku `045/SPH/PSJ/IX/2026`, plus teks WA siap kirim. Rincian: `examples/HASIL-UJI.md` dan `examples/00-pembanding-tanpa-skill.md`. Skill ini juga diuji ulang di OpenClaw; temuannya tercatat di catatan revisi 1.0.3 sampai 1.0.5 di bawah. Uji OpenClaw 2026-10-01: 7 → 8 (8 pada uji ulang terakhir; selisih kecil) (lihat `examples/00-openclaw-sebelum-sesudah.md`). Claude Code diuji lewat simulasi agent; Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Bikin surat penawaran harga katering 150 nasi box buat panitia seminar"
- "Quotation jasa desain logo + kemasan untuk klien, harga sudah termasuk PPN"
- "Revisi penawaran kemarin, diskon totalnya jadi 5%"

## Instalasi singkat
Salin folder `surat-penawaran-harga` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## FAQ
**Usaha saya belum PKP, apakah tetap bisa?**
Bisa, justru itu pengaturan bawaannya. Surat dibuat tanpa PPN dan diberi keterangan "Harga tidak dikenakan PPN".

**Apakah surat ini bisa jadi faktur pajak?**
Tidak. Surat penawaran hanya penawaran. Faktur pajak tetap dibuat lewat Coretax oleh PKP. Untuk tagihan, pakai skill Invoice.

**Harus install Python?**
Tidak wajib. Jika komputer punya Python, angka dihitung otomatis oleh kalkulator bawaan. Jika tidak, AI tetap menghitung langkah demi langkah dan memberi tanda agar kamu mengecek ulang.

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: kota "Jakarta" dikarang di surat padahal tidak diberikan.
- Kini kota/tanggal/nomor yang tidak diberikan menjadi `[isi: …]` atau asumsi tercantum; default wajib masuk daftar asumsi.

## Catatan revisi 1.0.4 (2026-10-01)
- Temuan uji ulang OpenClaw: surat hanya disimpan ke file (tidak tampil di chat, teks WA tidak dibuat), PIC ditulis `[Nama PIC]`, dan non-PKP ditulis "belum kena PPN".
- Kini balasan chat wajib memuat isi surat lengkap + teks WA siap kirim; file hanya tambahan. PIC tidak diketahui → "Bapak/Ibu Bagian Pengadaan". Non-PKP → "Harga final; penjual bukan PKP sehingga tidak memungut PPN." (catatan script diperbarui + 1 tes baru).

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw: teks WA menulis "Surat penawaran resmi (PDF) terlampir" padahal tidak ada file yang dibuat.
- Teks WA kini tidak boleh menyebut lampiran yang tidak benar-benar dikirim. Surat lengkap disediakan sebagai versi siap cetak (markdown, bisa disimpan sebagai `SPH-<nomor>.md`); skill menyebut terus terang bahwa PDF tidak dibuat dan memberi cara menyimpannya sebagai PDF lewat Word/Google Docs. Script tidak berubah.
