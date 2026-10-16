# 04 — Input kurang: hanya angka diketik, tanpa tanggal & jenis barang

## Skenario
S4 — input tidak lengkap. Pengguna tidak mengirim foto. Ia hanya mengetik tiga angka dari invoice, tanpa tanggal, nama penjual, NPWP, atau jenis barang/jasa. Skill harus memakai default (aturan PPN yang berlaku sekarang, barang/jasa biasa), menyebut asumsinya, dan bertanya sekali hanya untuk hal yang bisa mengubah kesimpulan.

## Input pengguna
> Invoice dari vendor: harga 15 juta, PPN 1,8 juta, total 16,8 juta. Bener nggak PPN-nya?

## Langkah agent
JSON minimal: `{"id":"I1","jenis":"invoice","dpp":"15 juta","ppn":"1,8 juta","total":"16,8 juta"}` → `cek_nota.py`. Script memberi info "tanggal tidak tercantum; aturan PPN diasumsikan yang berlaku sekarang" dan peringatan 12% × DPP penuh.

## Output
> **Disegarkan ke v1.0.5 (2026-10-16):** dijalankan ulang dengan `scripts/cek_nota.py --hari-ini 2026-09-23` dari JSON minimal yang sama. Status, PPN seharusnya Rp 1.650.000, dan selisih Rp 150.000 tidak berubah; yang baru, **total seharusnya Rp 16.650.000 kini dihitung script** (baris "[!] Bila PPN dihitung benar …" dan kolom CSV **Total Seharusnya**), tidak lagi dihitung agent. Tampilan di bawah untuk Claude Code/Cursor; versi kanal chat ada di bagian berikutnya.


**Hasil cek (dari angka yang Anda ketik)**

| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| I1 | (belum disebut) | (belum disebut) | Invoice | Rp 16.800.000 | ⚠️ Perlu dicek |

**Yang perlu Anda cek**
- **PPN Rp 1.800.000 = 12% × Rp 15.000.000 (DPP penuh).** Untuk barang/jasa **biasa**, aturan sejak 1 Januari 2025 adalah 12% × 11/12 × DPP (efektif 11%), sehingga **PPN seharusnya Rp 1.650.000** dan total **Rp 16.650.000**. Selisihnya **Rp 150.000**. Tanyakan ke vendor sebelum membayar.
- Total Rp 16.800.000 = Rp 15.000.000 + Rp 1.800.000, jadi penjumlahannya sendiri cocok.

**Asumsi yang saya pakai** (karena belum disebut):
- Tanggal invoice tahun 2025 atau sesudahnya, jadi dipakai aturan PPN yang berlaku sekarang.
- Barang/jasa **biasa**, bukan barang mewah.

Dua hal yang bisa mengubah kesimpulan. Jawab kalau tahu:
1. Barang/jasanya apa? (Kalau **barang mewah** yang kena PPnBM, misalnya mobil mewah, maka 12% penuh justru benar.)
2. Bisa kirim foto invoice-nya? Nanti sekalian saya cek NPWP penjual, nomor faktur, terbilang, dan saya buatkan tabel/CSV-nya.

_Dasar PPN: UU HPP & PMK 131/2024, per 23 September 2026. Alat bantu cek, bukan nasihat pajak; untuk kepastian hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

## Versi kanal chat (Telegram/WhatsApp) — ditambahkan 2026-10-16 (v1.0.5)
Tanpa tabel Markdown:

> **Hasil cek (dari angka yang Anda ketik)**
> I1 · tanggal & penjual belum disebut · Invoice · Rp 16.800.000 · ⚠️ Perlu dicek
>
> **Yang perlu Anda cek**
> • PPN Rp 1.800.000 = 12% × DPP penuh. Untuk barang/jasa biasa seharusnya Rp 1.650.000, total seharusnya Rp 16.650.000 (lebih Rp 150.000). Tanyakan ke vendor sebelum membayar.
> • Penjumlahan 15.000.000 + 1.800.000 = 16.800.000 sendiri cocok.
>
> (Asumsi & dua pertanyaan sama dengan di atas.)

## Catatan penguji
- Sesuai SKILL.md: tidak menahan jawaban dengan banyak pertanyaan. Default (jenis biasa, aturan sekarang) dipakai dan disebut. Hanya 2 pertanyaan yang benar-benar mengubah hasil.
- Verifikasi independen: 15.000.000 × 11/100 = 1.650.000. Selisih 150.000. Total seharusnya 16.650.000. Format "1,8 juta" dan "16,8 juta" terbaca benar oleh script (1.800.000 / 16.800.000).
- Script menambahkan info "Ada PPN tapi NPWP penjual tidak tercantum…". Agent **tidak** menyampaikannya sebagai temuan karena NPWP-nya hanya belum diketik, bukan tidak ada di dokumen. Ini benar, tetapi bergantung pada kejelian agent.
- Kurang (ringan): bagian Input SKILL.md hanya mengatur "dokumen belum dikirim → tanyakan sekali". Tidak ada panduan untuk kasus umum "pengguna hanya mengetik angka", misalnya "boleh dicek dari angka yang diketik; sebutkan asumsi tanggal & jenis; tawarkan kirim foto".
