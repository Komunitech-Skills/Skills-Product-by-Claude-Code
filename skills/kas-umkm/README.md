# Buku Kas Warung, Cukup Lewat Chat

**Catat uang masuk-keluar, cocokkan uang laci, dan tahu kapan uang usaha terpakai untuk pribadi, semua tersimpan di komputer Anda sendiri.**

## Manfaat
- ✅ **Tanpa aplikasi berlangganan, tanpa akun.** Buku kas tersimpan di satu file di komputer Anda. Tidak ada biaya bulanan, tidak perlu internet.
- ✅ **Cukup ketik seperti biasa.** "Hari ini jualan tunai 780 ribu, QRIS 240 ribu, beli gas 25 ribu, ambil 200 ribu buat jajan anak" → langsung tercatat per kategori, per laci/rekening, lengkap dengan saldo terbaru. Yang tidak jelas ditanyakan, bukan ditebak.
- ✅ **Uang laci ketahuan pas atau selisih.** Hitung per lembar ("seratus ribuan 22 lembar, lima puluh ribuan 10...") dan langsung terlihat kurang/lebih berapa, beserta kemungkinan penyebabnya.
- ✅ **Rem untuk "uang usaha kepakai pribadi".** Ada peringatan bila ambil pribadi melebihi hasil usaha atau melewati batas bulanan yang Anda tetapkan.
- ✅ **Laporan siap kirim.** Rekap harian, mingguan, bulanan per kategori, bisa dikirim otomatis ke Telegram tiap malam. Datanya juga bisa langsung dipakai untuk laporan keuangan (pengajuan KUR) dan proyeksi kas.

## Cocok untuk siapa
- Warung, toko kelontong, kedai, warung makan, katering rumahan, laundry, bengkel kecil, toko online rumahan — yang selama ini mencatat di buku tulis atau tidak mencatat sama sekali.
- Pemilik yang uang usahanya tersebar di laci, rekening, QRIS, dan e-wallet, dan sering bingung "uangnya ke mana".
- Pengguna skill **Kasir Lokal**: rekap penjualan harian kasir bisa dimasukkan ke buku kas sekali perintah.

**Kurang cocok:** usaha yang butuh akuntansi lengkap (jurnal, stok, piutang, penyusutan) atau dipakai beberapa komputer/cabang sekaligus.

## Contoh sebelum & sesudah
**Sebelum:** uang laci dan uang belanja rumah bercampur. Akhir bulan tidak tahu untung berapa, dan tiba-tiba uang untuk kulakan tidak cukup.

**Sesudah (cukup ketik):** "rekap kas hari ini"
```
BUKU KAS Warung Bu Sri
Rekap harian Sabtu, 26/09/2026
UANG MASUK: Rp 1.020.000
- Penjualan: Rp 1.020.000
UANG KELUAR: Rp 261.000
- Beli stok/bahan: Rp 28.000
- Prive (ambil pribadi): Rp 200.000
- Pengeluaran lain-lain: Rp 30.000
- Selisih laci kurang: Rp 3.000
HASIL USAHA (masuk usaha - keluar usaha): Rp 959.000
SALDO per akhir 26/09/2026:
- Laci kas: Rp 2.829.000
- BRI: Rp 11.480.000
Total: Rp 14.309.000
PERINGATAN PRIVE bulan ini: Rp 1.800.000 melewati batas prive bulanan yang Anda tetapkan (Rp 1.500.000).
```
(Contoh lengkap dengan data fiktif ada di folder `examples/`.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bikinin buku kas untuk warung saya, uang laci sekarang 500 ribu, rekening BRI 3 juta"
- "Catat: jualan tunai 1,2 juta, QRIS 350 ribu, bayar listrik 200 ribu dari BRI"
- "Ambil 300 ribu buat belanja rumah" / "Masukin modal 2 juta ke BRI"
- "Setor uang laci 1 juta ke BRI" (pindah dana, tidak mengubah hasil usaha)
- "Hitung laci: seratus ribuan 12 lembar, lima puluh ribuan 6, receh 3.500"
- "Saldo kas sekarang?" / "Rekap kas minggu lalu" / "Rekap September"
- "Masukin mutasi BRI ini" (kirim file CSV dari internet banking)
- "Kirim ringkasan kas ke Telegram saya tiap jam 9 malam" (OpenClaw)

Setiap pencatatan ditampilkan dulu untuk Anda cek; baru disimpan setelah Anda bilang "ya". Salah catat bisa dibatalkan dengan alasan; catatan lama tetap ada di riwayat.

## Instalasi singkat
Salin folder `kas-umkm` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

Butuh **Python 3.8+** (gratis di python.org; Mac/Linux biasanya sudah ada). Tidak butuh internet, akun, atau API key. Data tersimpan di folder `KomunitechData/kas/` di folder pengguna Anda; cadangan dibuat otomatis setiap hari ada perubahan.

## Yang perlu Anda tahu (jujur)
- **"Hasil usaha" bukan laba resmi.** Ini selisih uang masuk dan keluar untuk usaha (tanpa modal, pinjaman/cicilan utang, kasbon karyawan, ambil pribadi, dan pindah dana). Stok yang masih ada, piutang, dan penyusutan alat belum dihitung. Untuk laporan laba rugi & neraca (mis. untuk bank), pakai skill **Laporan Keuangan SAK EMKM**; buku kas ini bisa langsung diekspor ke sana.
- **Bukan aplikasi bank.** Saldo rekening tidak terbaca otomatis; masukkan lewat catatan atau file mutasi CSV dari internet banking. Tarik tunai/setor tunai perlu Anda pastikan (pindah dana atau pribadi).
- **Satu usaha, satu komputer.** Jangan membuka file buku kas yang sama dari dua komputer (mis. lewat Google Drive).
- Ringkasan otomatis ke Telegram butuh OpenClaw yang menyala di komputer yang sama; isinya (saldo, prive) tersimpan di chat Telegram Anda. Jadwal ini belum diuji langsung di OpenClaw untuk skill ini (polanya sudah teruji di skill Kasir Lokal).
- Alat bantu catat, bukan nasihat keuangan atau pajak.

**Riwayat versi singkat.** 1.0.1: baris impor yang belum jelas jadi "Perlu dicek", tarik/setor tunai = pindah dana, tolak pembukuan ganda. 1.0.2: biaya tarik tunai/admin bank = biaya, bukan pindah dana. **1.0.3:** pengeluaran "lain-lain" yang sebenarnya cicilan utang, kasbon karyawan, atau belanja rumah otomatis dipindah ke kategori yang benar (tidak lagi mengurangi hasil usaha) dengan pemberitahuan; kategori baru **kasbon**; ekspor ke laporan keuangan mengingatkan sisa utang awal agar neraca seimbang. **1.0.4:** denda/bunga/biaya cicilan tetap dihitung biaya; bayar utang ke toko/pemasok tidak lagi dianggap cicilan pinjaman bank (ditanyakan: belanja stok atau belanja lain); pelanggan yang melunasi bon = penjualan; "X pinjam uang" = kasbon; denda pajak tidak dicatat sebagai PPh di laporan keuangan. **1.0.5:** "angsuran + denda" dalam satu catatan diminta dipisah; "bayar utang" yang tidak jelas ke siapa ditanyakan dulu; pelanggan jasa (servis, cuci, jahit, laundry) yang melunasi bon = penjualan; belanja dapur/sayur rumah = pengambilan pribadi; pembelian bon/tempo yang belum dibayar tidak dicatat dulu (mencegah pengeluaran terhitung dua kali); pajak atas bunga bank dicatat sebagai PPh, bukan denda. **1.0.6:** "plus dendanya", "KUR termasuk bunga" juga diminta dipisah; "tanpa denda"/"bunga 0%" tidak lagi ditolak; uang masuk dari pelanggan "yang kemarin ngebon" bisa langsung dicatat; setiap pertanyaan dari buku kas memakai kalimat sehari-hari; kosakata usaha jasa (laundry, deterjen, service mesin) lebih lengkap; ekspor laporan keuangan menjelaskan bila pembelian alat membuat laba berbeda dari hasil usaha. **1.0.7:** belanja bahan kue/warung (tepung, gula, mentega, telur, ragi, minyak goreng, gas elpiji) langsung dikenali sebagai belanja bahan; "denda nihil"/"dendanya dihapus" tidak lagi ditolak; biaya lain-lain yang sudah Anda pilih masuk ke pos biaya yang tepat di laporan keuangan (tidak lagi "belum terklasifikasi"). 93 uji otomatis lulus.

## FAQ
**Apakah data saya dikirim ke internet?**
Tidak. Script buku kas tidak memakai internet sama sekali; semuanya tersimpan di satu file di komputer Anda. Yang terkirim hanya ringkasan yang Anda minta dikirim ke Telegram.

**Uang laci saya sering selisih. Bisa bantu cari penyebabnya?**
Bisa. Setelah menghitung uang fisik, Anda langsung tahu kurang/lebih berapa dan daftar penyebab yang paling sering (pengeluaran kecil belum dicatat, kembalian salah, QRIS tercatat tunai, dll.). Kalau sudah ketemu, catat yang terlewat; kalau tidak ketemu, buku bisa disesuaikan dengan catatan "selisih hitung laci" supaya tidak menumpuk.

**Saya sudah pakai Kasir Lokal. Perlu catat penjualan dua kali?**
Tidak. Rekap harian kasir dimasukkan ke buku kas dengan satu perintah (tunai ke laci, QRIS ke rekening penampung). Buku kas juga menolak memasukkan rekap kasir bila tanggal itu sudah ada catatan penjualan manual, supaya penjualan tidak dobel.
