# Buku Kas Jadi Laporan Keuangan SAK EMKM

**Tempel catatan uang masuk-keluar, dapat laba rugi, neraca yang dicek keseimbangannya, dan penjelasan bahasa awam dalam hitungan menit.**

Diuji AI penguji independen di OpenClaw: 7,9 → 8,6 dari 10 (angka laba rugi dan neraca cocok dengan hitungan independen, uang pribadi dipisah, dan permintaan menaikkan omzet untuk KUR ditolak; selisih dengan AI tanpa skill tergolong kecil).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tiga laporan standar SAK EMKM (standar laporan keuangan untuk usaha mikro, kecil, dan menengah) langsung jadi: Laba Rugi, Posisi Keuangan (neraca), dan Catatan atas Laporan Keuangan. Bisa jadi lampiran awal saat mengajukan KUR (Kredit Usaha Rakyat) atau untuk arsip usaha; bank bisa meminta format sendiri
- ✅ Bonus Laporan Arus Kas (uang masuk-keluar dikelompokkan per kegiatan usaha, investasi, dan pendanaan) plus file siap cetak. Laporan Arus Kas disertakan sebagai pelengkap praktis, mis. untuk lampiran pengajuan KUR; SAK EMKM (IAI, berlaku sejak 1 Januari 2018) mensyaratkan tiga laporan: Laba Rugi, Posisi Keuangan, dan Catatan atas Laporan Keuangan
- ✅ Uang pribadi dipisah dari biaya usaha (prive, yaitu uang usaha yang Anda ambil untuk keperluan pribadi), supaya laba yang tampil lebih mendekati laba usaha yang sebenarnya
- ✅ Neraca dicek otomatis: Aset = Utang + Modal. Jika tidak seimbang, selisih dan penyebabnya ditunjukkan
- ✅ Transaksi yang tidak jelas ditanyakan dulu ke Anda, tidak langsung ditebak
- ✅ Ringkasan bahasa sehari-hari: "Usaha Anda untung Rp X, pengeluaran terbesar ..."

## Cocok untuk siapa
- Pemilik warung, toko, katering, laundry, konveksi, atau jasa yang mencatat kas di buku, Excel, atau catatan HP
- Pelaku UMKM yang diminta bank atau koperasi menyerahkan laporan keuangan sederhana
- Admin atau keluarga yang membantu tutup buku bulanan
- Pendamping UMKM dan mahasiswa KKN yang membantu banyak usaha sekaligus

## Contoh sebelum & sesudah
**Sebelum:** Catatan kas 3 bulan tersebar di Excel. Tidak tahu sebenarnya untung atau rugi, karena uang belanja rumah tangga ikut tercampur.

**Sesudah (cukup ketik):** "Mbak, tolong bikinin laporan keuangan katering aku Januari sampai Maret, mau buat arsip sama jaga-jaga kalau bank minta. Filenya kas-dapur-sehati.csv. Stok bahan awal Januari kira-kira 1,2 juta, akhir Maret 1.650.000. … Nama usahanya Katering Dapur Sehati." (CSV = file tabel dari Excel/Google Sheets)

Pada contoh ini AI lebih dulu menanyakan 3 hal yang belum jelas (mis. bagian bunga angsuran KUR), baru menyusun laporan. Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-katering-3-bulan-kur-prive.md`):
> …
>
> | Pos | Jumlah |
> |---|---:|
> | **Laba (rugi) sebelum pajak** | **-Rp 1.870.417** |
> | Beban pajak penghasilan | (Rp 156.500) |
> | **LABA (RUGI) BERSIH** | **-Rp 2.026.917** |
>
> …
>
> ✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas (Rp 37.939.750). Neraca seimbang.

Hasil lengkapnya juga memuat catatan atas laporan, tren per bulan, dan daftar asumsi.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Tolong buatkan laporan keuangan bulan ini dari catatan kas ini" (lalu tempel tabelnya)
- "Aku untung berapa Januari sampai Maret? Filenya kas-2026.csv"
- "Bikinkan neraca dan laba rugi buat pengajuan KUR"

Belum punya catatan? Pakai `templates/buku-kas-template.csv` (kolom: Tanggal, Keterangan, Masuk, Keluar, Kategori).

## Instalasi singkat
Salin folder `laporan-keuangan-emkm` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Perhitungan memakai Python (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org). Tanpa Python, AI tetap bisa menghitung manual dengan rumus yang disediakan.

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.3.3), skor 1–10 penguji independen: tanpa skill **7,9** → dengan skill **8,6** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Pada skenario warung bakso, dengan skill laba bersih Rp12.375.000, prive dipisah, dan transaksi buku kas dikelompokkan dengan benar. Pada skenario lain, permintaan menaikkan omzet di laporan untuk KUR ditolak tegas.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis oleh agent AI) dan Claude Code (simulasi agent). Codex dan Cursor belum diuji langsung. Bukan laporan audit atau nasihat pajak — minta akuntan memeriksa bila untuk bank/pajak resmi.

## FAQ
**Apakah laporan ini bisa dipakai untuk bank atau pajak?**
Formatnya mengikuti SAK EMKM, standar yang umum diminta untuk UMKM. Laporan Arus Kas disertakan sebagai pelengkap; SAK EMKM mensyaratkan Laba Rugi, Posisi Keuangan, dan Catatan. Laporan ini bukan laporan audit dan bukan nasihat pajak. Untuk tender, investor besar, atau pelaporan pajak, minta akuntan atau konsultan pajak memeriksanya.

**Catatan saya berantakan dan ada yang tidak jelas. Tetap bisa?**
Tetap bisa diproses. Format angka Indonesia (`Rp 15.000`, `1,5jt`, `150rb`), tanggal seperti "5 Januari 2026", file CSV, dan tabel tempelan bisa dibaca. Baris yang rusak atau tidak jelas akan dilaporkan nomornya dan ditanyakan ke Anda, bukan diabaikan diam-diam.

**Kata-kata di catatan saya khas usaha saya. Apakah dikenali?**
Kata umum seperti bahan, gaji, listrik, ongkir, iklan, dan prive sudah dikenali. Kata khas usaha Anda (mis. "deterjen" untuk laundry) bisa ditambahkan sekali di file pemetaan, lalu dipakai terus.

## Riwayat perubahan

Versi terkini: **1.3.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
