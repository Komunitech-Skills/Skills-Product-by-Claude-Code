# Kalkulator PPN 12% yang Dihitung Skrip

**Ketik harganya, langsung tahu harga sebelum PPN (DPP), PPN, dan totalnya sesuai aturan per 23 September 2026.**

*Diuji AI penguji independen: 7,75 → 9,0 dari 10 (angka PPN sama-sama benar; dengan skill label tarif dan dasar aturannya tepat, dan tagihan supplier yang salah hitung ketahuan).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Sesuai aturan PPN 12% yang dihitung dari "DPP nilai lain" (11/12 dari harga sebelum PPN, sehingga efektif 11%) untuk barang/jasa biasa
- ✅ Bisa dari harga sebelum pajak **atau** harga yang sudah termasuk PPN
- ✅ Membedakan barang biasa dan barang mewah otomatis
- ✅ Mengingatkan bila penjual belum PKP (Pengusaha Kena Pajak), karena yang belum PKP tidak boleh menagih PPN
- ✅ Pembulatan dijelaskan, angka dihitung script, bukan dikira-kira

## Cocok untuk siapa
- Pemilik usaha yang sudah PKP dan sering membuat penawaran/tagihan
- Admin keuangan yang mengecek PPN di tagihan supplier
- Pengusaha yang bingung "harga ini sudah termasuk PPN atau belum?"

## Contoh sebelum & sesudah
**Sebelum:** Menghitung 11/12 × 12% di kalkulator HP, lalu ragu apakah angkanya benar dan bagaimana membulatkannya.

**Sesudah (cukup ketik):** "bikinin dong itungan ppn, harga 3.330.000 udah include ppn"

*Cuplikan hasil nyata dari `examples/02-bikinin-dong-pisahkan-ppn.md` (sisa catatan dasar aturan dipotong):*
```
**Perhitungan PPN** (barang/jasa biasa)
- Harga termasuk PPN: Rp 3.330.000
- Harga sebelum PPN (DPP): Rp 3.000.000
- DPP nilai lain (11/12): Rp 2.750.000
- PPN 12%: **Rp 330.000** (setara 11% dari DPP)
- **Total: Rp 3.330.000** (tanpa selisih pembulatan)

Cara hitung: DPP = 3.330.000 × 100/111 = Rp 3.000.000; PPN = 11% × 3.000.000 = Rp 330.000.
Pembulatan: PPN dibulatkan ke bawah ke rupiah penuh.

⚠️ Pastikan penjualnya sudah dikukuhkan sebagai PKP sebelum menagih PPN. Kalau belum PKP, jangan cantumkan PPN di tagihan — seluruh Rp 3.330.000 adalah harga jual biasa.
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "PPN dari harga 2,5 juta berapa?"
- "Pisahkan PPN dari harga Rp 11.100.000."
- "Barang mewah seharga 250 juta, PPN-nya berapa?"

## Instalasi singkat
Salin folder `hitung-ppn` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, di OpenClaw (uji otomatis agent, 1 Oktober 2026; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 7,75 tanpa skill menjadi 9,0 dengan skill. Catatan jujur: untuk hitungan PPN sederhana, model AI polos sudah menghasilkan angka yang benar (di uji ini PPN Rp 577.500 dan total Rp 5.827.500). Bedanya, tanpa skill penawaran memakai label "PPN 11%" yang sudah tidak sesuai aturan 2025 dan tanpa dasar aturan; dengan skill labelnya "PPN 12% × DPP nilai lain 11/12", lengkap dengan cara hitung, pembulatan, dasar PMK 131/2024 (peraturan Menteri Keuangan tentang PPN), tanggal berlaku, dan disclaimer, tanpa perlu mencari di internet. Tagihan supplier kertas yang memakai "12% penuh" langsung ditandai kelebihan Rp 20.000.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Kenapa PPN-nya 11%, bukan 12%?**
Untuk barang/jasa biasa, tarif 12% dikalikan dengan DPP nilai lain (11/12 dari harga), sehingga hasilnya sama dengan 11% dari harga. Tarif 12% penuh hanya untuk barang mewah.

**Saya belum PKP, boleh pakai skill ini?**
Boleh untuk simulasi, misalnya mengecek tagihan supplier. Tapi Anda tidak boleh menagih PPN ke pembeli sebelum dikukuhkan sebagai PKP; skill akan mengingatkan hal ini.

**Apakah ini menggantikan faktur pajak?**
Tidak. Faktur pajak resmi tetap dibuat di Coretax (sistem pajak online milik DJP). Skill ini membantu menghitung dan mengecek angkanya.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak. Dasar aturan (berlaku per 23 September 2026): UU HPP dan PMK 131/2024, yaitu tarif 12% dengan DPP nilai lain 11/12 (dasar hitung 11/12 dari harga sebelum PPN) untuk barang/jasa non-mewah (berlaku 1 Januari 2025) dan 12% dari harga penuh untuk barang mewah (sejak 1 Februari 2025). PPN dihitung dari DPP lalu dibulatkan ke bawah sekali; pembulatan ini belum dicocokkan dengan Coretax, jadi bila Coretax menampilkan angka berbeda, ikuti Coretax. Kasus khusus: hubungi DJP (Kring Pajak 1500200) atau konsultan pajak.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
