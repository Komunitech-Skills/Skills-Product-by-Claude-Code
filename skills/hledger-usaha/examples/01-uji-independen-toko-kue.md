# 01 (UJI INDEPENDEN Akun B) — Toko kue: pembukuan bulanan September

> Penguji independen (Akun B), 2026-09-26. Skill disalin ke scratchpad dan dijalankan dari sana; hledger **1.52.4 asli** (binary resmi Linux x64, SHA-256 cocok) dijalankan dari scratchpad, tidak dipasang ke sistem. `HOME` diarahkan ke folder uji. Path dipendekkan `<scratch>`. Data usaha fiktif, dibuat penguji (bukan data uji pembuat).

**Pengguna:** "Mulai pembukuan hledger untuk toko kue saya, Dapur Bu Rina, rekening Mandiri. Saldo per 31 Agustus: kas 1,5 juta, Mandiri 8,25 juta, stok bahan 2,4 juta, oven 6 juta, utang ke Toko Bahan Sinar 1,2 juta. Catat September: jual kue 2,35 jt tunai; tart PT Arunika 1,8 jt bayar belakangan; beli bahan 3,15 jt transfer ke Toko Bahan Sinar; lunasi utang Toko Bahan Sinar 1,2 jt; sewa kios 2 jt transfer; pencairan GoFood 4.725.500 masuk Mandiri; token listrik 275rb tunai; PT Arunika lunas 1,8 jt via Mandiri; beli gula/coklat/keju Rp 1.625.750,50 ke CV Gula Manis bayar bulan depan; gaji 2 karyawan 3,6 jt transfer; saya ambil 750rb untuk rumah; setor uang laci 1,5 jt ke Mandiri; jual 3,14 jt tunai; ongkir GoSend 185rb tunai; admin bank 15rb. Stok akhir dihitung 2,15 juta. Buatkan laporan bulanannya."

**Alur agent (mengikuti SKILL.md):** `init` → pratinjau saldo awal → ya → `catat --batch` (15 transaksi, file JSON) pratinjau → ya → uji dobel (batch diulang) → `stok-akhir` pratinjau → ya → `bulanan`.

## Log (dipotong hanya pada pratinjau batch yang panjang)
```
$ init --nama "Dapur Bu Rina" --bank Mandiri
BUKU BARU DIBUAT
File jurnal: <scratch>/s1/Pembukuan/usaha.journal
Aturan mutasi bank: <scratch>/s1/Pembukuan/aturan-bank.rules (baru)
Folder: impor/, ekspor/, backup/
Akun siap pakai: Kas, Bank (Mandiri), Piutang Usaha, Persediaan, Peralatan, Utang Usaha, Utang Bank, Modal, Prive, Pendapatan, HPP, Beban.
Diperiksa dengan: hledger 1.52.4

Langkah berikut: catat saldo awal (uang di laci, saldo rekening, stok, piutang, utang) dengan `catat --jenis saldo-awal`.
Agar hledger langsung memakai file ini, atur variabel LEDGER_FILE (lihat docs/panduan-hledger.md).
(kode 0)
$ catat --jenis saldo-awal ... (pratinjau)
PRATINJAU CATATAN (BELUM disimpan)
File: <scratch>/s1/Pembukuan/usaha.journal

2026-08-31 Saldo awal
    Aset:Kas                                        Rp 1.500.000
    Aset:Bank:Mandiri                               Rp 8.250.000
    Aset:Persediaan                                 Rp 2.400.000
    Aset:Peralatan                                  Rp 6.000.000
    Utang:Usaha:Toko Bahan Sinar                   -Rp 1.200.000
    Modal:Saldo Awal                              -Rp 16.950.000
Artinya: Saldo awal pembukuan per 31 Agustus 2026.

Akun baru yang akan dibuat: Utang:Usaha:Toko Bahan Sinar
Simpan 1 transaksi ini? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode 0)
$ catat saldo-awal --ya
Akun baru yang akan dibuat: Utang:Usaha:Toko Bahan Sinar
Tersimpan 1 transaksi ke <scratch>/s1/Pembukuan/usaha.journal. Cadangan versi sebelumnya: usaha.journal.sebelum-ubah
(kode 0)
$ catat --batch batch-sept.json (pratinjau)
PRATINJAU CATATAN (BELUM disimpan)
File: <scratch>/s1/Pembukuan/usaha.journal

2026-09-01 Penjualan kue harian
    Aset:Kas                                        Rp 2.350.000
    Pendapatan:Penjualan                           -Rp 2.350.000
Artinya: Penjualan Rp 2.350.000, uang masuk ke Aset:Kas.

2026-09-03 Tart ulang tahun kantor  ; pihak:PT Arunika
    Aset:Piutang Usaha:PT Arunika                   Rp 1.800.000
    Pendapatan:Penjualan                           -Rp 1.800.000
Artinya: Penjualan Rp 1.800.000 kepada PT Arunika, belum dibayar (piutang bertambah).

2026-09-04 Tepung, mentega, telur  ; pihak:Toko Bahan Sinar
    HPP:Pembelian                                   Rp 3.150.000
    Aset:Bank:Mandiri                              -Rp 3.150.000
Artinya: Beli barang dagangan/bahan Rp 3.150.000 dari Toko Bahan Sinar, dibayar dari Aset:Bank:Mandiri.

2026-09-05 Pelunasan utang Agustus  ; pihak:Toko Bahan Sinar
    Utang:Usaha:Toko Bahan Sinar                    Rp 1.200.000
    Aset:Bank:Mandiri                              -Rp 1.200.000
Artinya: Membayar utang ke pemasok Rp 1.200.000 (utang berkurang).

2026-09-08 Sewa kios September
    Beban:Sewa                                      Rp 2.000.000
    Aset:Bank:Mandiri                              -Rp 2.000.000
Artinya: Biaya Rp 2.000.000 untuk Beban:Sewa.

2026-09-10 Pencairan GoFood
    Aset:Bank:Mandiri                               Rp 4.725.500
    Pendapatan:Penjualan                           -Rp 4.725.500
Artinya: Penjualan Rp 4.725.500, uang masuk ke Aset:Bank:Mandiri.

2026-09-12 Token listrik
    Beban:Listrik Air Internet                        Rp 275.000
    Aset:Kas                                         -Rp 275.000
Artinya: Biaya Rp 275.000 untuk Beban:Listrik Air Internet.

2026-09-15 Pelunasan tart  ; pihak:PT Arunika
    Aset:Bank:Mandiri                               Rp 1.800.000
    Aset:Piutang Usaha:PT Arunika                  -Rp 1.800.000
Artinya: Pelanggan membayar piutang Rp 1.800.000 (piutang berkurang).

2026-09-18 Gula, coklat, keju  ; pihak:CV Gula Manis
    HPP:Pembelian                                Rp 1.625.750,50
    Utang:Usaha:CV Gula Manis                   -Rp 1.625.750,50
Artinya: Beli barang dagangan/bahan Rp 1.625.750,50 dari CV Gula Manis, belum dibayar (utang bertambah).

2026-09-20 Gaji 2 karyawan
    Beban:Gaji                                      Rp 3.600.000
    Aset:Bank:Mandiri                              -Rp 3.600.000
Artinya: Biaya Rp 3.600.000 untuk Beban:Gaji.

2026-09-22 Belanja rumah
    Modal:Prive                                       Rp 750.000
    Aset:Kas                                         -Rp 750.000
Artinya: Pemilik mengambil uang usaha untuk pribadi Rp 750.000 (prive, mengurangi modal, BUKAN beban).

2026-09-25 Setor uang laci
    Aset:Bank:Mandiri                               Rp 1.500.000
    Aset:Kas                                       -Rp 1.500.000
Artinya: Pindah uang sendiri Rp 1.500.000 dari Aset:Kas ke Aset:Bank:Mandiri (bukan pendapatan/biaya).

2026-09-28 Penjualan kue minggu terakhir
    Aset:Kas                                        Rp 3.140.000
    Pendapatan:Penjualan                           -Rp 3.140.000
Artinya: Penjualan Rp 3.140.000, uang masuk ke Aset:Kas.
PERINGATAN: tanggal 2026-09-28 ada di masa depan.

2026-09-30 Ongkir GoSend
    Beban:Transportasi                                Rp 185.000
    Aset:Kas                                         -Rp 185.000
Artinya: Biaya Rp 185.000 untuk Beban:Transportasi.
PERINGATAN: tanggal 2026-09-30 ada di masa depan.

2026-09-30 Biaya admin bulanan
    Beban:Admin Bank                                   Rp 15.000
    Aset:Bank:Mandiri                                 -Rp 15.000
Artinya: Biaya Rp 15.000 untuk Beban:Admin Bank.
PERINGATAN: tanggal 2026-09-30 ada di masa depan.

Akun baru yang akan dibuat: Aset:Piutang Usaha:PT Arunika, Utang:Usaha:CV Gula Manis
Simpan 15 transaksi ini? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode 0)
$ catat --batch batch-sept.json --ya
Akun baru yang akan dibuat: Aset:Piutang Usaha:PT Arunika, Utang:Usaha:CV Gula Manis
Tersimpan 15 transaksi ke <scratch>/s1/Pembukuan/usaha.journal. Cadangan versi sebelumnya: usaha.journal.sebelum-ubah
(kode 0)
$ catat --batch batch-sept.json --ya  (diulang: uji dobel)
KEMUNGKINAN DOBEL: transaksi ke-12 sama persis dengan catatan 2026-09-25 'Setor uang laci'.
KEMUNGKINAN DOBEL: transaksi ke-13 sama persis dengan catatan 2026-09-28 'Penjualan kue minggu terakhir'.
KEMUNGKINAN DOBEL: transaksi ke-14 sama persis dengan catatan 2026-09-30 'Ongkir GoSend'.
KEMUNGKINAN DOBEL: transaksi ke-15 sama persis dengan catatan 2026-09-30 'Biaya admin bulanan'.
TIDAK DISIMPAN. Bila memang transaksi berbeda (mis. dua kali beli barang yang sama), ulangi dengan --tetap-catat.
(kode 7)
$ stok-akhir --nilai 2.150.000 --tanggal 2026-09-30
PENYESUAIAN PERSEDIAAN per 30 September 2026
Nilai stok hasil hitung: Rp 2.150.000
Nilai Aset:Persediaan di catatan: Rp 2.400.000

2026-09-30 Penyesuaian persediaan (hitung stok)
    Aset:Persediaan                                  -Rp 250.000
    HPP:Penyesuaian Persediaan                        Rp 250.000

Artinya: stok turun Rp 250.000; HPP bulan ini bertambah sebesar itu (barang terjual/terpakai/rusak lebih banyak dari stok baru).
Simpan? Setelah pengguna menjawab ya, ulangi dengan --ya.
(kode 0)
TERSIMPAN ke <scratch>/s1/Pembukuan/usaha.journal
$ bulanan --bulan 2026-09
RINGKASAN 1 SEPTEMBER 2026 S.D. 30 SEPTEMBER 2026
Dapur Bu Rina
- Pendapatan: Rp 12.015.500
- Laba bersih: Rp 914.749,50
- Kas & bank akhir: Rp 10.590.500 (+Rp 840.500 dari awal bulan)
- Piutang (belum dibayar pelanggan): Rp 0
- Utang: Rp 1.625.750,50
- Neraca: seimbang

--------------------------------

LAPORAN LABA RUGI
Dapur Bu Rina
Periode: 1 September 2026 s.d. 30 September 2026

PENDAPATAN
- Penjualan: Rp 12.015.500
Total pendapatan: Rp 12.015.500

HARGA POKOK PENJUALAN (HPP)
- Pembelian: Rp 4.775.750,50
- Penyesuaian Persediaan: Rp 250.000
Total HPP: Rp 5.025.750,50

LABA KOTOR: Rp 6.989.749,50 (58,2% dari pendapatan)

BEBAN USAHA
- Gaji: Rp 3.600.000
- Sewa: Rp 2.000.000
- Listrik Air Internet: Rp 275.000
- Transportasi: Rp 185.000
- Admin Bank: Rp 15.000
Total beban: Rp 6.075.000

LABA BERSIH: Rp 914.749,50 (7,6% dari pendapatan)

--------------------------------

NERACA (POSISI KEUANGAN)
Dapur Bu Rina
Per 30 September 2026

ASET (yang dimiliki)
- Bank: Rp 6.310.500
- Peralatan: Rp 6.000.000
- Kas: Rp 4.280.000
- Persediaan: Rp 2.150.000
Total aset: Rp 18.740.500

UTANG (kewajiban)
- Utang Usaha: Rp 1.625.750,50
Total utang: Rp 1.625.750,50

MODAL
- Saldo Awal: Rp 16.950.000
- Prive: -Rp 750.000
- Laba (rugi) tahun 2026 s.d. tanggal ini: Rp 914.749,50
Total modal: Rp 17.114.749,50

```

## Verifikasi independen (Decimal, dihitung dari cerita pengguna, tanpa membaca kode skill) — `verif1.py`
```
pendapatan 12015500 hpp 5025750.50 laba kotor 6989749.50 beban 6075000 laba 914749.50
kas 4280000 bank 6310500 aset 18740500 utang 1625750.50 modal 17114749.50 selisih 0.00
kas+bank awal 9750000 akhir 10590500 perubahan 840500
margin kotor % 58.2 margin bersih % 7.6
```
Rincian arus kas operasi dihitung tangan: masuk penjualan tunai/bank 2.350.000 + 4.725.500 + 3.140.000 = 10.215.500; piutang tertagih 1.800.000; keluar 3.150.000 + 1.200.000 + 2.000.000 + 275.000 + 3.600.000 + 185.000 + 15.000 = 10.425.000 → bersih +1.590.500; pendanaan (prive) −750.000; total +840.500.

## Pembanding hledger asli (`hledger -n -f usaha.journal ...`)
- `is -p 2026-09` → Net **Rp 914.750** (tampilan hledger dibulatkan ke rupiah; `bal -c 'Rp 1.000,00'` menunjukkan HPP Rp 5.025.750,50 persis).
- `bs -e 2026-10-01` → Aset Rp 18.740.500, Utang Rp 1.625.750 (bulat), Net Rp 17.114.750 (bulat).
- `cf -p 2026-09` → Kas +2.780.000, Mandiri −1.939.500, total **+840.500**.
- `bal --depth 1` total = 0; `check accounts balanced` lulus.

| Angka | Skill | hledger asli | Hitungan penguji |
|---|---|---|---|
| Pendapatan | 12.015.500 | 12.015.500 | 12.015.500 |
| HPP | 5.025.750,50 | 5.025.750,50 (format sen) | 5.025.750,50 |
| Laba bersih | 914.749,50 | 914.750 (bulat tampilan) / 914.749,50 | 914.749,50 |
| Total aset | 18.740.500 | 18.740.500 | 18.740.500 |
| Utang | 1.625.750,50 | 1.625.750,50 | 1.625.750,50 |
| Modal akhir | 17.114.749,50 | 17.114.749,50 | 17.114.749,50 |
| Perubahan kas & bank | +840.500 | +840.500 | +840.500 |

**Ekspor SAK EMKM:** `ekspor-emkm --bulan 2026-09` lalu `laporan_emkm.py` (skill laporan-keuangan-emkm): laba bersih Rp 914.749 (EMKM menampilkan rupiah bulat), total aset Rp 18.740.500, neraca seimbang, prive Rp 750.000 dipisahkan. Konsisten.

## Penilaian
- ✅ Semua angka tepat sampai sen; neraca seimbang; kas akhir cocok dengan saldo akun; uji silang pembaca bawaan COCOK.
- ✅ Prive dicatat sebagai `Modal:Prive` (bukan beban), setor tunai tidak dihitung pendapatan, piutang/utang per pihak otomatis.
- ✅ Pratinjau → "ya" → `--ya`; batch diulang ditolak (kode 7) tanpa menulis apa pun.
- ✅ Peringatan tanggal masa depan (28–30 Sep; hari uji 26 Sep).
- ⚠️ Minor: laporan arus kas memakai nama akun mentah (`Pendapatan:Penjualan`, `Aset:Piutang Usaha`), kurang ramah awam dibanding laba rugi/neraca. Laporan bulan berjalan (per 30 Sep, dibuat 26 Sep) tidak memberi catatan "bulan belum selesai".
