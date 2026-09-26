# hledger Usaha: Pembukuan Rapi Tanpa Biaya Bulanan

**Ceritakan transaksi Anda seperti chat biasa ("jual 750rb ke Kantor Maju, bayarnya minggu depan"), dan AI mencatatnya ke buku besar berpasangan di komputer Anda sendiri. Akhir bulan tinggal minta: laba rugi, neraca, dan arus kas dalam Rupiah.**

Dibangun di atas **hledger**, program pembukuan gratis dan open-source yang sudah dipakai bertahun-tahun oleh komunitas akuntansi di seluruh dunia. Pengganti aplikasi pembukuan berlangganan.

## Manfaat
- ✅ **Catat dari kalimat biasa.** Jual, beli, bayar listrik, pelanggan belum bayar, ambil uang pribadi, angsuran KUR, semua langsung jadi catatan akuntansi yang benar. Anda tidak perlu paham debit-kredit.
- ✅ **Mutasi bank masuk sendiri.** Unggah CSV dari internet banking (BCA, Mandiri, BRI, BNI, dll.). Transaksi dikelompokkan otomatis (listrik, gaji, QRIS, ongkir, admin bank), yang ragu ditanyakan, dan saldo akhir dicocokkan dengan saldo bank sampai sen. Impor ulang tidak membuat data dobel.
- ✅ **Laporan bulanan siap kirim.** Laba rugi (lengkap dengan laba kotor & margin), neraca yang selalu dicek seimbang, dan arus kas dari mana uang datang dan ke mana perginya.
- ✅ **Siap untuk KUR/bank.** Sekali perintah, buku kas dan saldo-saldonya siap diolah menjadi laporan format SAK EMKM (skill Laporan Keuangan EMKM).
- ✅ **Data milik Anda, aman.** Satu file teks di komputer sendiri. Setiap perubahan dipratinjau dulu, disetujui Anda, dicadangkan otomatis, dan diperiksa ulang. Bila pemeriksaan gagal, file dikembalikan seperti semula.

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

Panduan pemasangan skill lengkap: `CARA-INSTAL.md` di paket. Butuh **Python 3.8+** (gratis di python.org). Tidak butuh akun, internet, atau paket tambahan.

**Status uji jujur (versi 1.0.0, draft):** diuji oleh pembuat dengan hledger **1.52.4 asli** di Linux dan tanpa hledger; 32 uji otomatis lulus, termasuk pencocokan angka dengan `hledger is/bs/cf` dan dengan skill Laporan Keuangan EMKM. **Belum** diuji penguji independen, belum diuji di Windows/Mac, dan jadwal laporan OpenClaw belum dicoba di Gateway sungguhan.

## FAQ
**Apakah saya harus paham akuntansi?**
Tidak. Anda cukup bercerita; AI memilih akun yang tepat dan menjelaskan artinya dalam bahasa sehari-hari ("Artinya: penjualan Rp 750.000 kepada Kantor Maju, belum dibayar"). Setiap catatan harus Anda setujui sebelum disimpan.

**Bagaimana kalau AI salah catat atau file-nya rusak?**
Setiap penyimpanan membuat cadangan versi sebelumnya dan memeriksa ulang buku. Bila pemeriksaan gagal, file otomatis dikembalikan. Transaksi kembar ditolak. Koreksi dilakukan dengan transaksi pembalik, jadi riwayat tetap jelas. Backup bertanggal tinggal minta.

**Apakah data saya dikirim ke internet?**
Tidak oleh skill ini. Buku Anda adalah file di komputer Anda sendiri, dan script tidak membuka koneksi internet. Tampilan web hledger-web (opsional) hanya bisa dibuka dari komputer itu sendiri.

---
Komunitech tidak berafiliasi dengan proyek hledger. hledger adalah perangkat lunak terpisah (GPL-3.0) milik pembuatnya; Anda mengunduhnya sendiri dari sumber resmi.
