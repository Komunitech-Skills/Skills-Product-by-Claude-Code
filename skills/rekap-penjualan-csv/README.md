# Rekap Penjualan Otomatis dari File Kasir

**Kirim file penjualan, dapat laporan omzet dan produk terlaris dalam semenit.**

*Diuji AI penguji independen di OpenClaw: 7,5 → 9 dari 10 (angka sama-sama benar; dengan skill laporan lebih lengkap: persentase tiap produk, rata-rata harian, dan saran yang bisa dijalankan).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Total omzet, rata-rata harian, dan 5 produk terlaris
- ✅ Hari terbaik dan hari terendah terlihat jelas
- ✅ Angka dihitung dengan script, bukan dikira-kira
- ✅ Membaca format Indonesia: `Rp 15.000`, `15.000,50`, dan pemisah titik koma (`;`) seperti file Excel berbahasa Indonesia
- ✅ 2–3 saran (insight) yang bisa langsung dijalankan

## Cocok untuk siapa
- Pemilik toko atau usaha yang punya ekspor data kasir, Shopee, Tokopedia, atau spreadsheet
- Admin yang setiap minggu harus membuat laporan penjualan

## Contoh sebelum & sesudah
**Sebelum:** Rekap manual di Excel memakan waktu 1–2 jam.

**Sesudah (cukup ketik):** "Halo, ini file export kasir kedai kopi aku 2 minggu pertama September (kasir-kopi-sept.csv). Tolong direkap ya, mau tau menu mana yang paling laku sama hari apa yang paling rame."

*Cuplikan hasil nyata dari `examples/01-kasir-kedai-kopi-2-minggu.md` (produk peringkat 3–5 dan saran tindakan dipotong):*
```
## Rekap Penjualan 1 – 14 September 2026

**Total omzet:** Rp 5.084.000
**Jumlah transaksi (baris):** 127
**Rata-rata omzet per hari (kalender):** Rp 363.143  _(hari berjualan: Rp 363.143; 14 dari 14 hari ada penjualan)_

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Matcha Latte | 60 | Rp 1.320.000 | 26,0% |
| 2 | Es Kopi Susu Gula Aren | 63 | Rp 1.134.000 | 22,3% |
…
Hari terbaik: Senin, 7 September 2026 (Rp 549.000). Hari terendah: Senin, 14 September 2026 (Rp 214.000).
```

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent Anda dan lampirkan file CSV-nya (file tabel sederhana yang bisa dibuka di Excel), misalnya:
- "Tolong rekap penjualan dari file penjualan-september.csv"
- "Ini ekspor kasir kedai kopi aku 2 minggu, menu mana yang paling laku sama hari apa yang paling rame?"
- "Rekap pesanan Shopee bulan ini, yang batal dan retur jangan dihitung."
- "Buatkan ringkasan penjualan minggu ini untuk ditempel di grup tim."

## Syarat
File berformat **CSV** yang punya kolom tanggal, nama produk, dan total atau harga. Jika filenya Excel (.xlsx), simpan dulu sebagai CSV. Sebaiknya ada Python 3 di komputer (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org) agar angka dihitung skrip; tanpa Python, AI menghitung manual dan akan memberi tahu bahwa hasilnya belum diverifikasi skrip.

## Instalasi singkat
Salin folder `rekap-penjualan-csv` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, dua sumber yang terpisah.
- **Uji OpenClaw, 1 Oktober 2026** (angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario ekspor Shopee): skor tanpa skill 7,5 → dengan skill 8,5, lalu 9 setelah perbaikan v1.2.3. Selisihnya kecil dan terutama pada kelengkapan format, bukan ketepatan angka.
- **Uji simulasi agent (perbandingan tanpa dan dengan skill), 23 September 2026** (`examples/00-pembanding-tanpa-skill.md`): pada file yang rapi, angka agent tanpa skill sama benarnya. Nilai tambahnya ada di format Indonesia yang berantakan: pada file dengan harga `68.500,00`, cara "ambil digit saja" menghasilkan Rp 1.389.910.000 padahal yang benar Rp 13.899.100 (100 kali lipat), tanpa peringatan. Pada ekspor marketplace, bila pesanan batal dan retur ikut dihitung, omzet contoh membengkak menjadi Rp 10.793.000 dari yang seharusnya Rp 9.006.000; dengan skill keduanya benar.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Format ekspor Tokopedia, kasir kedai, dan angka berformat campur belum diuji di OpenClaw. Bot Telegram asli belum diuji.

## FAQ
**Apakah data saya dikirim ke internet?**
Script berjalan di komputer Anda sendiri. Isi data tetap dibaca oleh AI agent yang Anda pakai.

**Nama kolom di file saya berbeda. Tetap bisa?**
Biasanya bisa: AI agent mencocokkan kolom berdasarkan isi file. Syaratnya ada kolom tanggal, nama produk, dan total atau harga.

**Bagaimana kalau ada baris yang rusak?**
Baris yang rusak dilewati, lalu jumlah dan alasannya dilaporkan.

> **Catatan:** rekap ini menghitung omzet dari file penjualan yang Anda kirim. Bukan laporan laba rugi dan bukan perhitungan pajak; hasilnya sebaik kualitas datanya.

## Riwayat perubahan

Versi terkini: **1.2.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
