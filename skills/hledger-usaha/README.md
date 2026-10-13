# hledger Usaha: Pembukuan Rapi Tanpa Biaya Bulanan

**Ceritakan transaksi Anda seperti chat biasa ("jual 750rb ke Kantor Maju, bayarnya minggu depan"), dan AI mencatatnya ke buku besar berpasangan (pembukuan standar akuntansi: tiap transaksi dicatat dari dua sisi) di komputer Anda sendiri. Akhir bulan tinggal minta: laba rugi, neraca, dan arus kas dalam Rupiah.**

Dibangun di atas **hledger**, program pembukuan gratis dan open-source yang sudah dipakai bertahun-tahun oleh komunitas akuntansi di seluruh dunia. Pengganti aplikasi pembukuan berlangganan.

*Diuji AI penguji independen: 5,25 → 9,0 dari 10 (tanpa skill agent mengubah file pembukuan tanpa bertanya dan salah mencatat potongan pajak PPh 23; dengan skill entri ditampilkan dulu dan disimpan setelah Anda setuju).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux (hledger sudah diuji di Linux; Windows dan Mac belum diuji langsung). Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan: Hledger (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Catat dari kalimat biasa.** Jual, beli, bayar listrik, pelanggan belum bayar, ambil uang pribadi, angsuran KUR (Kredit Usaha Rakyat), semua diubah jadi catatan akuntansi berpasangan yang Anda setujui dulu sebelum disimpan. Anda tidak perlu paham debit-kredit.
- ✅ **Mutasi bank masuk sendiri.** Unggah file CSV (tabel mutasi dari internet banking: BCA, Mandiri, BRI, BNI, dll.). Transaksi dikelompokkan otomatis (listrik, gaji, QRIS, ongkir, admin bank), yang ragu ditanyakan, dan saldo akhir dicocokkan dengan saldo bank sampai sen. Impor ulang tidak membuat data dobel.
- ✅ **Laporan bulanan siap kirim.** Laba rugi (lengkap dengan laba kotor & margin), neraca yang dicek seimbang setiap laporan dibuat, dan arus kas dari mana uang datang dan ke mana perginya.
- ✅ **Siap untuk KUR/bank.** Sekali perintah, buku kas dan saldo-saldonya siap diolah menjadi laporan format SAK EMKM (standar laporan keuangan untuk usaha kecil; lewat skill Laporan Keuangan EMKM).
- ✅ **Data milik Anda, tersimpan lokal.** Satu file teks di komputer sendiri. Setiap perubahan dipratinjau dulu, disetujui Anda, dicadangkan otomatis, dan diperiksa ulang. Bila pemeriksaan gagal, file dikembalikan seperti semula.

## Cocok untuk siapa
- Pemilik UMKM (kedai, toko, jasa, produksi rumahan) yang ingin pembukuan **benar-benar rapi**: piutang & utang per pelanggan/pemasok, neraca, riwayat bertahun-tahun.
- Usaha yang sedang membayar aplikasi pembukuan bulanan dan ingin berhenti berlangganan.
- Profesional/freelancer dan konsultan yang terbiasa dengan AI agent (OpenClaw, Claude Code, Codex, Cursor).

**Pilih skill lain bila:** hanya butuh buku kas masuk-keluar paling sederhana → **Kas UMKM**; butuh invoice, stok per barang, dan kasir dalam satu program → **Dolibarr Usaha**; hanya ingin laporan SAK EMKM sekali jadi dari catatan Excel → **Laporan Keuangan EMKM**.

## Contoh sebelum & sesudah
**Sebelum:** catatan tersebar di buku tulis, WA, dan mutasi bank. Akhir bulan menebak-nebak untung. Tidak tahu persis siapa yang belum bayar. Mau ajukan KUR, bingung menyusun neraca.

**Sesudah:** ketik *"Laporan keuangan Juli"*:
```
LAPORAN LABA RUGI
Kopi Sari
Periode: 1 Juli 2026 s.d. 31 Juli 2026
PENDAPATAN
- Penjualan: Rp 8.800.000
HARGA POKOK PENJUALAN (HPP)
- Pembelian: Rp 3.500.000
- Penyesuaian Persediaan: Rp 300.000
LABA KOTOR: Rp 5.000.000 (56,8% dari pendapatan)
BEBAN USAHA
- Gaji: Rp 3.000.000
- Listrik Air Internet: Rp 350.000
- Bunga: Rp 50.000
LABA BERSIH: Rp 1.600.000 (18,2% dari pendapatan)
...
Cek: Aset = Utang + Modal (Rp 17.200.000). SEIMBANG.
```
(Contoh nyata dari uji dengan hledger 1.52.4. Angkanya sama dengan hitungan hledger sendiri dan dengan skill Laporan Keuangan EMKM.)

## Cara pakai
- "Mulai pembukuan untuk usaha saya, nama Kopi Sari, rekening BCA"
- "Catat: jual 1,25 juta tunai, bayar listrik 350rb, beli susu 1,5 juta belum dibayar ke CV Susu Segar"
- "Ini mutasi BCA bulan ini, masukkan ke pembukuan"
- "Saldo kas di buku berapa? Uang di laci 1,35 juta"
- "Stok akhir bulan dihitung 2,7 juta"
- "Laporan keuangan bulan lalu", "neraca per 31 Juli", "arus kas 3 bulan terakhir"
- "Buatkan laporan SAK EMKM untuk pengajuan KUR"
- "Backup pembukuan saya"

## Instalasi singkat
1. **hledger (opsional tapi disarankan).** Ikuti `docs/panduan-hledger.md` di paket: unduh dari situs resmi, cek keasliannya, ±15–30 menit. Skill tetap bisa dipakai walau hledger belum dipasang.
2. Salin folder `hledger-usaha` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan pemasangan skill lengkap: lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`). Butuh **Python 3.8+** (gratis di python.org). Tidak butuh akun, internet, atau paket tambahan.

**Hasil uji (jujur):** penguji AI independen, skor 1–10; tiga sumber yang terpisah.
- **Uji OpenClaw, 2 Oktober 2026** (uji otomatis agent dengan hledger 1.30.1 dan data contoh, versi 1.0.9; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 5,25 tanpa skill menjadi 9,0 dengan skill; uji pertama sebelum perbaikan sempat belum lulus (7,25). Pada jurnal kecil, angka laporan tanpa skill juga bisa dihitung; pembedanya ada di keamanan data dan pajak. Tanpa skill, agent langsung mengubah file pembukuan tanpa bertanya, dan potongan pajak "PPh 23" atas penjualan kopi dicatat sebagai kredit pajak dengan piutang dinyatakan lunas. Dengan skill entri ditampilkan dulu, disimpan setelah Anda bilang "ya" (dengan cadangan otomatis), laba bersih September Rp 7.865.500, neraca seimbang Rp 21.515.500, dan sisa Rp 40.000 tetap tercatat sebagai piutang.
- **Uji dengan hledger asli dan uji otomatis (versi 1.0.5):** diuji pembuat dan penguji independen dengan hledger **1.52.4 asli** di Linux dan tanpa hledger; versi 1.0.5 juga lulus 51 uji otomatis dengan hledger **1.30.1** (versi lama dari paket Ubuntu/Debian) - hledger yang terlalu lama/tidak cocok otomatis diganti pembaca bawaan. 1.0.5 juga: file pembukuan di folder kerja dikenali (tidak membuat buku baru tanpa konfirmasi), dan potongan "PPh 23" atas penjualan barang dicatat sebagai sisa piutang + draf pesan klarifikasi (perlakuan pajaknya PERLU REVIEW konsultan). Sebelumnya 45 uji otomatis lulus, termasuk pencocokan angka dengan `hledger is/bs/cf` dan dengan skill Laporan Keuangan EMKM. Versi 1.0.1 menambah pencatatan pembayaran pelanggan yang dipotong PPh 23, pengingat penjualan tunai yang tidak ada di mutasi bank, dan penolakan tegas pembukuan ganda. Versi 1.0.2: pengingat penjualan tunai di laporan laba rugi tetap muncul walau mutasi berisi tarik tunai ATM/setor tunai, dan potongan PPh 23 ditolak untuk penjualan barang. Versi 1.0.3: potongan PPh 23 juga ditolak saat pelanggan melunasi piutang dari penjualan barang (`terima-piutang`); piutang campuran barang+jasa atau dari saldo awal diberi peringatan. Versi 1.0.4: asal piutang dikenali dari jenis catatannya (jual/jasa), bukan dari nama akun; pelunasan piutang yang tidak tercatat di buku diberi peringatan agar tagihan/saldo awalnya dicatat dulu.
- **Perubahan setelah itu (versi terkini 1.0.10):** nomor versi di script disamakan, dan penolakan PPh 23 atas penjualan barang dilunakkan (tidak mutlak: bisa berlaku bila transaksinya sebenarnya jasa, mis. katering; Anda diminta klarifikasi atau bukti potong), dari temuan uji ulang OpenClaw.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent); Claude Code hanya lewat simulasi agent pada versi 1.0.1–1.0.2, dan Codex serta Cursor belum diuji langsung (format skill-nya sama). **Belum** diuji di Windows/Mac, jadwal laporan OpenClaw belum dicoba di Gateway sungguhan (program OpenClaw yang berjalan di latar belakang), dan ekspor CSV asli BRI, BNI, serta bank digital belum diuji (hasil impor selalu dipratinjau dulu sebelum disimpan).

## FAQ
**Apakah saya harus paham akuntansi?**
Tidak. Anda cukup bercerita; AI memilih akun yang tepat dan menjelaskan artinya dalam bahasa sehari-hari ("Artinya: penjualan Rp 750.000 kepada Kantor Maju, belum dibayar"). Setiap catatan harus Anda setujui sebelum disimpan.

**Bagaimana kalau AI salah catat atau file-nya rusak?**
Setiap penyimpanan membuat cadangan versi sebelumnya dan memeriksa ulang buku. Bila pemeriksaan gagal, file otomatis dikembalikan. Transaksi kembar ditolak. Koreksi dilakukan dengan transaksi pembalik, jadi riwayat tetap jelas. Backup bertanggal tinggal minta.

**Apakah data saya dikirim ke internet?**
Tidak oleh skill ini. Buku Anda adalah file di komputer Anda sendiri, dan script tidak membuka koneksi internet. Tampilan web hledger-web (opsional) hanya bisa dibuka dari komputer itu sendiri.

> **Catatan penting:** alat bantu pembukuan, bukan nasihat akuntansi atau pajak. Laporan dihitung dari transaksi yang Anda setujui; sebelum dipakai untuk pengajuan KUR/bank atau laporan pajak, sebaiknya diperiksa akuntan. Perlakuan pajak atas potongan PPh 23 PERLU REVIEW konsultan pajak, dan pembulatan belum dicocokkan dengan Coretax (sistem pajak online DJP). Skill menolak pembukuan ganda (dua versi laporan).

---
Komunitech tidak berafiliasi dengan proyek hledger. hledger adalah perangkat lunak terpisah (GPL-3.0) milik pembuatnya; Anda mengunduhnya sendiri dari sumber resmi.
