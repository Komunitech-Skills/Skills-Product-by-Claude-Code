# Kalkulator PPN 12% Tanpa Salah Hitung

**Ketik harganya, langsung tahu DPP, PPN, dan totalnya sesuai aturan terbaru.**

## Manfaat
- ✅ Sesuai aturan PPN 12% dengan DPP nilai lain 11/12 (efektif 11%) untuk barang/jasa biasa
- ✅ Bisa dari harga sebelum pajak **atau** harga yang sudah termasuk PPN
- ✅ Membedakan barang biasa dan barang mewah otomatis
- ✅ Mengingatkan bila penjual belum PKP (tidak boleh menagih PPN)
- ✅ Pembulatan dijelaskan, angka dihitung script, bukan dikira-kira

## Cocok untuk siapa
- Pemilik usaha yang sudah PKP dan sering membuat penawaran/tagihan
- Admin keuangan yang mengecek PPN di tagihan supplier
- Pengusaha yang bingung "harga ini sudah termasuk PPN atau belum?"

## Contoh sebelum & sesudah
**Sebelum:** Menghitung 11/12 × 12% di kalkulator HP, lalu ragu apakah angkanya benar dan bagaimana membulatkannya.

**Sesudah (cukup ketik):** "Harga 7,5 juta sudah termasuk PPN, PPN-nya berapa? Saya PKP."
→ DPP Rp 6.756.757, DPP nilai lain Rp 6.193.693,92, PPN Rp 743.243, total Rp 7.500.000, lengkap dengan cara hitungnya.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "PPN dari harga 2,5 juta berapa?"
- "Pisahkan PPN dari harga Rp 11.100.000."
- "Barang mewah seharga 250 juta, PPN-nya berapa?"

## Instalasi singkat
Salin folder `hitung-ppn` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Kenapa PPN-nya 11%, bukan 12%?**
Untuk barang/jasa biasa, tarif 12% dikalikan dengan DPP nilai lain (11/12 dari harga), sehingga hasilnya sama dengan 11% dari harga. Tarif 12% penuh hanya untuk barang mewah.

**Saya belum PKP, boleh pakai skill ini?**
Boleh untuk simulasi, misalnya mengecek tagihan supplier. Tapi kamu tidak boleh menagih PPN ke pembeli sebelum dikukuhkan sebagai PKP; skill akan mengingatkan hal ini.

**Apakah ini menggantikan faktur pajak?**
Tidak. Faktur pajak resmi tetap dibuat di Coretax. Skill ini membantu menghitung dan mengecek angkanya.

## Catatan revisi 1.0.4 (2026-10-01)
- Hasil hitung kini menyertakan **teks siap tempel** untuk penawaran/chat yang selalu memuat baris "DPP nilai lain (11/12)", agar pembaca tidak mengira "PPN 12%" salah hitung.
