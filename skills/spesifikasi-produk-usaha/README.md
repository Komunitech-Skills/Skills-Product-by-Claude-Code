# Spesifikasi Produk Usaha Siap Kirim ke Maklon

**Dari ide di kepala jadi dokumen 1-3 halaman, lengkap dengan urutan mana dikerjakan dulu.**

## Manfaat
- ✅ Spesifikasi produk (resep/bahan, kemasan, standar mutu, HPP target) dalam satu kalimat perintah.
- ✅ Urutan ide dengan **skor RICE/ICE yang dihitung**, bukan perasaan; hasilnya langsung jadi roadmap Sekarang/Berikutnya/Nanti.
- ✅ Brief siap kirim ke maklon, supplier, penjahit, atau desainer tanpa membocorkan modal Anda.
- ✅ Catatan versi resep/spesifikasi supaya perubahan tidak hilang.
- ✅ Pengingat PIRT/BPOM/halal dengan tautan resmi, tanpa klaim kesehatan yang berisiko.

## Cocok untuk siapa
Pemilik usaha makanan-minuman, fashion, kosmetik, kerajinan, dan jasa/aplikasi sederhana yang mau membuat produk baru atau merapikan produk lama, terutama yang bekerja sama dengan maklon atau produsen.

## Contoh sebelum & sesudah
**Sebelum:** "Mau bikin teh botol, bilang ke maklon lewat chat panjang, lalu bingung varian mana dulu."

**Sesudah (cukup ketik):** "Bikin spesifikasi teh serai jahe botol 250 ml, jual Rp15.000, margin 50%. Ide lain: tanpa gula, paket 6 botol, langganan."
→ dokumen 11 bagian (HPP maksimal Rp7.500), tabel skor (paket 6 botol 80,00 jadi prioritas), roadmap, dan brief pemasok. Lihat folder `examples/`.

## Cara pakai
- "Buatkan spesifikasi produk kaos oversize untuk konveksi."
- "Mana yang dikerjakan dulu dari 5 ide varian ini?" (siapkan angka perkiraan; agen akan menanyakan)
- "Buat brief untuk maklon skincare."
- "Resep saya revisi, catat sebagai v0.4."

## Instalasi singkat
Salin folder `spesifikasi-produk-usaha` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Script hanya butuh Python standar (`python3`; Windows: `python` atau `py`), dan skill tetap berguna walau script tidak bisa dijalankan.

## FAQ
**Apakah ini menjamin izin PIRT/BPOM/halal saya beres?**
Tidak. Ini pengingat dan tautan resmi; aturan bisa berubah. Konfirmasi ke Dinas Kesehatan, BPJPH, atau pendamping resmi.

**Bagaimana menghitung modal dan harga jual?**
Skill ini menetapkan target HPP lalu merujuk ke skill `hitung-hpp` untuk angka pasti (dan `harga-jual-marketplace` untuk potongan marketplace).

**Apakah bisa untuk produk digital atau jasa?**
Bisa: bagian bahan/kemasan diganti fitur, cerita pengguna, dan kriteria selesai.

*Skill ini memakai ide dari pm-skills (MIT & Apache-2.0); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat aslinya.*
