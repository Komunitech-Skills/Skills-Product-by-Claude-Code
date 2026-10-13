# Kalkulator PPN 12% Tanpa Salah Hitung

**Ketik harganya, langsung tahu DPP, PPN, dan totalnya sesuai aturan terbaru.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

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

**Hasil uji (OpenClaw, uji otomatis agent, 1 Oktober 2026):** rata-rata nilai 7,75 tanpa skill menjadi 9,0 dengan skill (skala 10). Catatan jujur: untuk hitungan PPN sederhana, model AI polos sudah menghasilkan angka yang benar (di uji ini PPN Rp 577.500 dan total Rp 5.827.500). Bedanya, tanpa skill penawaran memakai label "PPN 11%" yang sudah tidak sesuai aturan 2025 dan tanpa dasar aturan; dengan skill labelnya "PPN 12% × DPP nilai lain 11/12", lengkap dengan cara hitung, pembulatan, dasar PMK 131/2024, tanggal berlaku, dan disclaimer, tanpa perlu mencari di internet. Tagihan supplier kertas yang memakai "12% penuh" langsung ditandai kelebihan Rp 20.000. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

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

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## FAQ
**Kenapa PPN-nya 11%, bukan 12%?**
Untuk barang/jasa biasa, tarif 12% dikalikan dengan DPP nilai lain (11/12 dari harga), sehingga hasilnya sama dengan 11% dari harga. Tarif 12% penuh hanya untuk barang mewah.

**Saya belum PKP, boleh pakai skill ini?**
Boleh untuk simulasi, misalnya mengecek tagihan supplier. Tapi kamu tidak boleh menagih PPN ke pembeli sebelum dikukuhkan sebagai PKP; skill akan mengingatkan hal ini.

**Apakah ini menggantikan faktur pajak?**
Tidak. Faktur pajak resmi tetap dibuat di Coretax. Skill ini membantu menghitung dan mengecek angkanya.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak. Dasar aturan (berlaku per 23 September 2026): UU HPP dan PMK 131/2024, yaitu tarif 12% dengan DPP nilai lain 11/12 untuk barang/jasa non-mewah (berlaku 1 Januari 2025) dan 12% dari harga penuh untuk barang mewah (sejak 1 Februari 2025). PPN dihitung dari DPP lalu dibulatkan ke bawah sekali; pembulatan ini belum dicocokkan dengan Coretax, jadi bila Coretax menampilkan angka berbeda, ikuti Coretax. Kasus khusus: hubungi DJP (Kring Pajak 1500200) atau konsultan pajak.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
