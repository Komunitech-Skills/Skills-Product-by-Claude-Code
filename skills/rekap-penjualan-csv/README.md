# Rekap Penjualan Otomatis dari File Kasir

**Kirim file penjualan, dapat laporan omzet dan produk terlaris dalam semenit.**

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
→ Laporan lengkap berisi tabel produk terlaris, tren harian, dan insight.

## Syarat
File berformat **CSV** yang punya kolom tanggal, nama produk, dan total atau harga. Jika filenya Excel (.xlsx), simpan dulu sebagai CSV. Butuh Python di komputer (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org).

## Instalasi singkat
Salin folder `rekap-penjualan-csv` ke folder skills AI agent kamu. Panduan lengkap per platform ada di `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah data saya dikirim ke internet?**
Script berjalan di komputermu sendiri. Isi data tetap dibaca oleh AI agent yang kamu pakai.

**Nama kolom di file saya berbeda. Tetap bisa?**
Bisa. AI agent akan mencocokkan kolom secara otomatis.

**Bagaimana kalau ada baris yang rusak?**
Baris yang rusak dilewati, lalu jumlah dan alasannya dilaporkan.

## Catatan revisi 1.2.3 (2026-10-01)
- Temuan uji OpenClaw: pertanyaan "hari paling rame" hanya dijawab dari sisi omzet.
- Rekap kini juga menampilkan hari dengan transaksi terbanyak (per pesanan unik lewat `--kolom-pesanan`, atau per baris). Ditambah uji regresi `scripts/uji_regresi.py` (4 tes).
