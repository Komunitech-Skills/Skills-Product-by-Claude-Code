# Buku Kas Jadi Laporan Keuangan SAK EMKM

**Tempel catatan uang masuk-keluar, dapat laba rugi, neraca seimbang, dan penjelasan bahasa awam dalam semenit.**

## Manfaat
- ✅ Tiga laporan standar SAK EMKM langsung jadi: Laba Rugi, Posisi Keuangan (neraca), dan Catatan atas Laporan Keuangan. Siap dilampirkan saat mengajukan KUR atau untuk arsip usaha
- ✅ Uang pribadi dan uang usaha otomatis dipisah (prive), jadi laba yang tampil adalah laba usaha yang sebenarnya
- ✅ Neraca dicek otomatis: Aset = Utang + Modal. Jika tidak seimbang, selisih dan penyebabnya ditunjukkan
- ✅ Transaksi yang tidak jelas tidak ditebak. AI akan menanyakannya ke kamu dulu
- ✅ Ringkasan bahasa sehari-hari: "Usaha kamu untung Rp X, pengeluaran terbesar ..."

## Cocok untuk siapa
- Pemilik warung, toko, katering, laundry, konveksi, atau jasa yang mencatat kas di buku, Excel, atau catatan HP
- Pelaku UMKM yang diminta bank atau koperasi menyerahkan laporan keuangan sederhana
- Admin atau keluarga yang membantu tutup buku bulanan
- Pendamping UMKM dan mahasiswa KKN yang membantu banyak usaha sekaligus

## Contoh sebelum & sesudah
**Sebelum:** Catatan kas 3 bulan tersebar di Excel. Tidak tahu sebenarnya untung atau rugi, karena uang belanja rumah tangga ikut tercampur.

**Sesudah (cukup ketik):** "Buatkan laporan keuangan dari buku-kas.csv, kas awal 3 juta, stok akhir kira-kira 200 ribu"
→ Laporan laba rugi (untung Rp 2.185.417), neraca seimbang Rp 5.185.417, catatan laporan, tren per bulan, daftar asumsi, dan ringkasan: "Pengeluaran terbesar: gaji karyawan, 59,9% dari total biaya."

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Tolong buatkan laporan keuangan bulan ini dari catatan kas ini" (lalu tempel tabelnya)
- "Aku untung berapa Januari sampai Maret? Filenya kas-2026.csv"
- "Bikinkan neraca dan laba rugi buat pengajuan KUR"

Belum punya catatan? Pakai `templates/buku-kas-template.csv` (kolom: Tanggal, Keterangan, Masuk, Keluar, Kategori).

## Instalasi singkat
Salin folder `laporan-keuangan-emkm` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Perhitungan memakai Python (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org). Tanpa Python, AI tetap bisa menghitung manual dengan rumus yang disediakan.

## FAQ
**Apakah laporan ini bisa dipakai untuk bank atau pajak?**
Formatnya mengikuti SAK EMKM, standar yang umum diminta untuk UMKM. Laporan ini bukan laporan audit dan bukan nasihat pajak. Untuk tender, investor besar, atau pelaporan pajak, minta akuntan atau konsultan pajak memeriksanya.

**Catatan saya berantakan dan ada yang tidak jelas. Tetap bisa?**
Bisa. Format angka Indonesia (`Rp 15.000`, `1,5jt`, `150rb`), tanggal seperti "5 Januari 2026", file CSV, dan tabel tempelan bisa dibaca. Baris yang rusak atau tidak jelas akan dilaporkan nomornya dan ditanyakan ke kamu, bukan diabaikan diam-diam.

**Kata-kata di catatan saya khas usaha saya. Apakah dikenali?**
Kata umum seperti bahan, gaji, listrik, ongkir, iklan, dan prive sudah dikenali. Kata khas usahamu (mis. "deterjen" untuk laundry) bisa ditambahkan sekali di file pemetaan, lalu dipakai terus.
