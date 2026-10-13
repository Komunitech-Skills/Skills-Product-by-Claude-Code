# Rekap Penjualan Otomatis dari File Kasir

**Kirim file penjualan, dapat laporan omzet dan produk terlaris dalam semenit.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Total omzet, rata-rata harian, dan 5 produk terlaris
- ✅ Hari terbaik dan hari terendah terlihat jelas
- ✅ Angka dihitung dengan script, bukan dikira-kira
- ✅ Membaca format Indonesia: `Rp 15.000`, `15.000,50`, dan pemisah `;`
- ✅ 2–3 insight yang bisa langsung dijalankan

## Cocok untuk siapa
- Pemilik toko atau usaha yang punya ekspor data kasir, Shopee, Tokopedia, atau spreadsheet
- Admin yang setiap minggu harus membuat laporan penjualan

## Contoh sebelum & sesudah
**Sebelum:** Rekap manual di Excel memakan waktu 1–2 jam.

**Sesudah (cukup ketik):** "Tolong rekap penjualan dari file penjualan-september.csv"
→ Laporan untuk contoh kedai kopi (127 transaksi, 1–14 September): omzet Rp 5.084.000, rata-rata Rp 363.143 per hari, 5 produk terlaris dengan persentasenya (Matcha Latte Rp 1.320.000 = 26,0% omzet), hari terbaik Senin 7 September (Rp 549.000) dan hari terendah Senin 14 September (Rp 214.000), plus insight yang bisa langsung dijalankan.

**Hasil uji A/B (simulasi agent, 23 September 2026):** pada file yang rapi, angka agent tanpa skill sama benarnya. Nilai tambahnya ada di format Indonesia yang berantakan: pada file dengan harga `68.500,00`, cara "ambil digit saja" menghasilkan Rp 1.389.910.000 padahal yang benar Rp 13.899.100 (100 kali lipat), tanpa peringatan. Pada ekspor marketplace, bila pesanan batal dan retur ikut dihitung, omzet contoh membengkak menjadi Rp 10.793.000 dari yang seharusnya Rp 9.006.000; dengan skill keduanya benar. Rincian: `examples/00-pembanding-tanpa-skill.md`. Uji OpenClaw 1 Okt 2026: skor tanpa skill 7,5 → dengan skill 8,5, lalu 9 setelah perbaikan v1.2.3; selisihnya kecil dan terutama pada kelengkapan format, bukan ketepatan angka (lihat `examples/00-openclaw-sebelum-sesudah.md`).

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent kamu dan lampirkan file CSV-nya, misalnya:
- "Tolong rekap penjualan dari file penjualan-september.csv"
- "Ini ekspor kasir kedai kopi aku 2 minggu, menu mana yang paling laku sama hari apa yang paling rame?"
- "Rekap pesanan Shopee bulan ini, yang batal dan retur jangan dihitung."
- "Buatkan ringkasan penjualan minggu ini untuk ditempel di grup tim."

## Syarat
File berformat **CSV** yang punya kolom tanggal, nama produk, dan total atau harga. Jika filenya Excel (.xlsx), simpan dulu sebagai CSV. Butuh Python di komputer (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org).

## Instalasi singkat
Salin folder `rekap-penjualan-csv` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## FAQ
**Apakah data saya dikirim ke internet?**
Script berjalan di komputermu sendiri. Isi data tetap dibaca oleh AI agent yang kamu pakai.

**Nama kolom di file saya berbeda. Tetap bisa?**
Bisa. AI agent akan mencocokkan kolom secara otomatis.

**Bagaimana kalau ada baris yang rusak?**
Baris yang rusak dilewati, lalu jumlah dan alasannya dilaporkan.

> **Catatan:** rekap ini menghitung omzet dari file penjualan yang kamu kirim. Bukan laporan laba rugi dan bukan perhitungan pajak; hasilnya sebaik kualitas datanya.

## Riwayat perubahan

Versi terkini: **1.2.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
