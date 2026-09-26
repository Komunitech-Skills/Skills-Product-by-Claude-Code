# 04 (UJI INDEPENDEN Akun B) — Input tidak lengkap, angka ambigu, file rusak, tanpa hledger

> Penguji independen (Akun B), 2026-09-26. Jurnal = salinan hasil skenario 01. hledger 1.52.4 asli kecuali bagian "tanpa hledger".

**Pengguna (pesan awam):** "catat bayar tukang servis oven 2 juta sama jual 62,500 kemarin, trus gajih 500rb. oh ya angsuran KUR 1,45 juta."

**Balasan agent sesuai SKILL.md (satu pesan, bernomor — simulasi penguji):**
> Sebelum saya catat, ada 4 hal singkat:
> 1. Servis oven Rp 2.000.000 dibayar pakai apa: tunai, transfer (Mandiri), atau belum dibayar?
> 2. "62,500" maksudnya Rp 62.500 atau Rp 62,50?
> 3. Gaji Rp 500.000 dibayar tunai atau transfer?
> 4. Angsuran KUR Rp 1.450.000: berapa bunganya (lihat jadwal angsuran)? Bila tidak tahu, saya catat semuanya sebagai pokok, dan laba bisa sedikit terlalu tinggi.

Script mendukung setiap pertanyaan itu dengan galat yang jelas (log di bawah) — tidak ada tebakan, tidak ada yang tertulis.

## Log A — input kurang / salah
```
$ catat --jenis beban --akun Beban:Perawatan --nominal 2jt --ket Bayar tukang servis oven
GAGAL: --via belum diisi: dibayar pakai kas (tunai), bank (transfer/QRIS), atau tempo (belum dibayar)?
(kode 2)

$ catat --jenis jual --nominal 62,500 --via kas --tanggal kemarin
GAGAL: --nominal '62,500' ambigu: maksudnya 62,500 (desimal) atau 62.500? Tulis ulang tanpa koma atau dengan titik ribuan.
(kode 2)

$ catat --jenis beban --akun Beban:Gajih --nominal 500rb --via kas
GAGAL: Akun 'Beban:Gajih' belum ada di jurnal. Mungkin maksudnya: Beban:Gaji, Beban:Sewa, Beban:Pajak Lain. Bila memang akun baru, ulangi dengan --akun-baru.
(kode 2)

$ catat --jenis jual --nominal -500rb --via kas
usage: hledger_usaha.py catat [-h] [--jurnal JURNAL] [--hledger HLEDGER]
                              [--mesin {auto,hledger,bawaan}] [--json]
                              [--jenis JENIS] [--tanggal TANGGAL]
                              [--nominal NOMINAL] [--via VIA] [--bank BANK]
                              [--pihak PIHAK] [--ket KET] [--akun AKUN]
                              [--dari DARI] [--ke KE] [--posting POSTING]
                              [--pokok POKOK] [--bunga BUNGA] [--batch BATCH]
                              [--akun-baru] [--tetap-catat] [--ya]
hledger_usaha.py catat: error: argument --nominal: expected one argument
(kode 2)

$ catat --jenis jual --nominal sejuta --via kas
GAGAL: --nominal 'sejuta' bukan angka rupiah yang dikenali. Contoh: 150000, 150.000, 150rb, 1,5jt.
(kode 2)

$ catat --jenis jual --via kas
GAGAL: --nominal belum diisi.
(kode 2)

$ catat --jenis angsuran --nominal 1,45jt --via bank --bank Mandiri
GAGAL: --pokok belum diisi.
(kode 2)

$ catat --jenis jual --nominal 100rb --via kas --tanggal 31/02/2026
GAGAL: tanggal '31/02/2026' tidak ada di kalender.
(kode 2)

$ catat --jenis bebas --ket tidak seimbang --posting Aset:Kas=100rb --posting Beban:Lain-lain=50rb
GAGAL: Posting tidak seimbang: jumlahnya Rp 150.000 (harus 0).
(kode 2)

$ laba-rugi --bulan Septembr 2026
GAGAL: Bulan 'Septembr 2026' tidak dikenali. Pakai 2026-09, 09/2026, 'September 2026', 'ini', atau 'lalu'.
(kode 2)

```

## Log B — file & keadaan rusak
```
$ catat --jenis jual --nominal=-500rb --via kas --jurnal <scratch>/s4/Pembukuan/usaha.journal
GAGAL: --nominal '-500rb' negatif. Arah uang ditentukan oleh jenis transaksi; tulis angkanya positif.
(kode 2)

$ laba-rugi --bulan 2026-09 --jurnal <scratch>/s4/tidak-ada/usaha.journal
GAGAL: File jurnal tidak ditemukan: <scratch>/s4/tidak-ada/usaha.journal
Buat dulu dengan perintah `init`, atau sebutkan --jurnal <path>.
(kode 3)

$ impor-bank kosong.csv --bank Mandiri --jurnal <scratch>/s4/Pembukuan/usaha.journal
GAGAL: Tidak ada baris transaksi yang terbaca dari kosong.csv.
(kode 2)

$ impor-bank mutasi.pdf.csv --bank Mandiri --jurnal <scratch>/s4/Pembukuan/usaha.journal
GAGAL: File mutasi.pdf.csv adalah PDF. Unduh mutasi dalam format CSV dari internet banking.
(kode 2)

$ impor-bank tanpa-arah.csv --bank Mandiri --jurnal <scratch>/s4/Pembukuan/usaha.journal
GAGAL: Kolom nominal tanpa penanda masuk/keluar (CR/DB) di baris 2. Sebutkan --kolom-dk atau --kolom-masuk/--kolom-keluar.
(kode 2)

$ impor-bank <scratch>/s3/mandiri-sept.csv --jurnal <scratch>/s4/Pembukuan/usaha.journal
IMPOR MUTASI BANK (PRATINJAU, belum disimpan)
File: mandiri-sept.csv -> rekening Aset:Bank:Mandiri
Kolom terbaca: Tanggal, Keterangan, Dana Keluar (IDR), Dana Masuk (IDR), Saldo (IDR)
Terbaca 7 transaksi (2026-09-02 s.d. 2026-09-23); 0 sudah pernah diimpor (dilewati); 7 baru.
Uang masuk Rp 3.906.845,33 | uang keluar Rp 4.677.500
Uji silang aturan dengan hledger: COCOK (7 baris)

RINGKASAN PER AKUN
- Beban:Sewa: 1 transaksi, keluar Rp 3.000.000
- Pendapatan:Penjualan: 1 transaksi, masuk Rp 2.405.000
- Aset:Kas: 1 transaksi, masuk Rp 1.500.000
- Beban:Belum Dikelompokkan: 1 transaksi, keluar Rp 1.250.000
- Beban:Listrik Air Internet: 1 transaksi, keluar Rp 415.000
- Beban:Admin Bank: 1 transaksi, keluar Rp 12.500
- Pendapatan:Lain-lain: 1 transaksi, masuk Rp 1.845,33

PERLU DITANYAKAN KE PENGGUNA (1 transaksi belum dikelompokkan):
- baris 3: 2026-09-04 Transfer ke CV BESEK BAMBU kemasan keluar Rp 1.250.000
Tetapkan dengan --tetapkan "BARIS=Akun", atau simpan kata kuncinya untuk bulan depan dengan perintah tambah-aturan.

Cek saldo: saldo bank sebelum transaksi pertama Rp 5.000.000; saldo Aset:Bank:Mandiri di catatan sebelum tanggal itu Rp 8.250.000.
SELISIH Rp 3.250.000: periksa transaksi bank sebelum periode ini yang belum/dobel dicatat.

Contoh 2 transaksi pertama:
2026-09-02 Transfer dari TOKOPEDIA PENARIKAN DANA  ; ref:7f8b48938d53, sumber:mutasi-bank
    Aset:Bank:Mandiri                               Rp 2.405.000
    Pendapatan:Penjualan                           -Rp 2.405.000
2026-09-04 Transfer ke CV BESEK BAMBU kemasan  ; ref:55b43e5067e2, sumber:mutasi-bank
    Aset:Bank:Mandiri                              -Rp 1.250.000
    Beban:Belum Dikelompokkan                       Rp 1.250.000

Simpan 7 transaksi? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode 0)

$ tambah-aturan --kata J&T (PERSERO) 50% --akun Beban:Transportasi --arah keluar --jurnal <scratch>/s4/Pembukuan/usaha.journal
ATURAN BARU untuk <scratch>/s4/Pembukuan/aturan-bank.rules:

# ditambahkan 2026-09-26 lewat tambah-aturan
if %keterangan J&T \(PERSERO\) 50%
& %keluar [1-9]
 account2 Beban:Transportasi

Simpan? Setelah pengguna menjawab ya, ulangi dengan --ya.
(kode 0)

$ tambah-aturan --kata BI --akun Beban:Lain-lain --arah keluar --jurnal <scratch>/s4/Pembukuan/usaha.journal
GAGAL: --kata minimal 3 huruf (kata terlalu pendek akan cocok ke mana-mana).
(kode 2)

$ tambah-aturan --kata TOKO X --akun Beban:Hiburan --arah keluar --jurnal <scratch>/s4/Pembukuan/usaha.journal
GAGAL: Akun 'Beban:Hiburan' belum ada di jurnal. Mungkin: Beban:Bunga, Beban:Perawatan, Beban:Pemasaran
(kode 2)

--- hitung ulang tanpa hledger (PATH bersih, HLEDGER kosong) ---
Total beban: Rp 6.075.000

LABA BERSIH: Rp 914.749,50 (7,6% dari pendapatan)

Sumber: usaha.journal | Dihitung dengan: pembaca bawaan skill (hledger belum terpasang)
Laporan manajemen dari catatan Anda sendiri, bukan laporan audit/pajak. Untuk bank/KUR format SAK EMKM, pakai perintah ekspor-emkm.
--- jurnal dirusak manual: ubah satu angka (tidak seimbang) ---
$ laba-rugi --bulan 2026-09 --jurnal <scratch>/s4/Pembukuan/usaha.journal
GAGAL: hledger menolak file jurnal:
hledger: Error: <scratch>/s4/Pembukuan/usaha.journal:74-76:
74 | 2026-09-01 Penjualan kue harian
   |     Aset:Kas                 Rp 2.305.000,
   |     Pendapatan:Penjualan    Rp -2.350.000,
This transaction is unbalanced.
The real postings' sum should be 0 but is: Rp -45.000
(kode 4)

$ catat --jenis jual --nominal 100rb --via kas --tanggal 2026-09-26 --jurnal <scratch>/s4/Pembukuan/usaha.journal --ya
GAGAL: hledger menolak file jurnal:
hledger: Error: <scratch>/s4/Pembukuan/usaha.journal:74-76:
74 | 2026-09-01 Penjualan kue harian
   |     Aset:Kas                 Rp 2.305.000,
   |     Pendapatan:Penjualan    Rp -2.350.000,
This transaction is unbalanced.
The real postings' sum should be 0 but is: Rp -45.000
(kode 4)

Pembukuan/usaha.journal: OK
GAGAL: baris 74: transaksi 'Penjualan kue harian' tidak seimbang (selisih -Rp 45.000).
(kode tanpa hledger 4)
```
Tambahan: aturan `J&T (PERSERO) 50%` disimpan lalu CSV berisi "Bayar J&T (PERSERO) 50% ongkir" diimpor → `Uji silang aturan dengan hledger: COCOK (1 baris)`, masuk `Beban:Transportasi` (escape regex benar). Jurnal dipulihkan dari salinan setelah uji.

## Penilaian
- ✅ Semua input kurang/ambigu ditolak dengan kode 2 dan pesan bahasa awam yang langsung bisa diubah menjadi pertanyaan; `62,500` ditolak sebagai ambigu; tanggal 31/02 ditolak; posting tidak seimbang ditolak; salah ketik akun yang ada (`Beban:Gajih`) diberi saran `Beban:Gaji`.
- ✅ Jurnal diedit manual hingga tidak seimbang → laporan ditolak (kode 4) dengan nomor baris & selisih, **dan** penulisan ditolak (md5 file tidak berubah). Tanpa hledger, pembaca bawaan memberi galat setara (baris 74, selisih −Rp 45.000).
- ✅ Tanpa hledger (PATH bersih): laba rugi identik (Rp 914.749,50), keluaran jujur "hledger belum terpasang".
- ✅ CSV kosong / PDF berganti nama / tanpa penanda arah → galat jelas; kata aturan < 3 huruf ditolak; akun aturan yang belum ada ditolak dengan saran.
- ✅ Mandiri diimpor ke jurnal yang saldo awal Mandiri-nya berbeda → "SELISIH Rp 3.250.000: periksa transaksi bank sebelum periode ini" (tidak dipaksa).
- ⚠️ Minor: `--nominal -500rb` (tanpa `=`) jatuh ke galat argparse berbahasa Inggris; dengan `--nominal=-500rb` pesannya bagus. Dampak kecil (agent yang menyusun perintah).
- ⚠️ Minor: angsuran tanpa `--pokok` → "--pokok belum diisi", kurang menjelaskan bahwa yang dibutuhkan adalah porsi pokok & bunga (SKILL.md/references sudah menutupinya).
