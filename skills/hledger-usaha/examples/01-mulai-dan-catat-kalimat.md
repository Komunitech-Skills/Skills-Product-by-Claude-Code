# 01 — Mulai pembukuan & mencatat dari kalimat biasa (uji pembuat, hledger 1.52.4 asli)

**Pengguna:** "Mulai pembukuan hledger untuk kedai saya, Kopi Sari, rekening BCA. Saldo per 30 Juni: kas 2 juta, BCA 10 juta, stok 3 juta, utang KUR 5 juta. Lalu catat transaksi Juli ini: jual harian 1,25 juta tunai; Kantor Maju Jaya ambil kopi rapat 750rb bayar belakangan; beli biji kopi 2 juta transfer ke Roastery Gayo; token listrik 350rb tunai; susu 1,5 juta dari Susu Segar CV bayar bulan depan; saya ambil 500rb buat rumah; Kantor Maju lunas 750rb via BCA; beli grinder 4,5 juta; angsuran KUR 450rb (pokok 400rb, bunga 50rb); setor uang laci 1 juta ke BCA; gaji 2 barista 3 juta; QRIS Juli 6,8 juta masuk BCA. Stok akhir Juli dihitung 2,7 juta."

**Yang dilakukan agent:** `init` → pratinjau saldo awal → "ya" → pratinjau satu transaksi tempo (menunjukkan sub-akun piutang per pelanggan dibuat otomatis) → 12 transaksi dalam satu `--batch` (file `tests/data/batch-juli.json`) → `stok-akhir`. Setiap tulis didahului pratinjau dan persetujuan. Di akhir, `hledger check accounts` (program hledger asli) lulus.

Lingkungan: Linux, Python 3.11, hledger 1.52.4 (binary resmi, SHA-256 cocok). Path dipendekkan menjadi `~`.

```
$ python3 hledger_usaha.py init --nama Kopi Sari --bank BCA
BUKU BARU DIBUAT
File jurnal: ~/Pembukuan/usaha.journal
Aturan mutasi bank: ~/Pembukuan/aturan-bank.rules (baru)
Folder: impor/, ekspor/, backup/
Akun siap pakai: Kas, Bank (BCA), Piutang Usaha, Persediaan, Peralatan, Utang Usaha, Utang Bank, Modal, Prive, Pendapatan, HPP, Beban.
Diperiksa dengan: hledger 1.52.4

Langkah berikut: catat saldo awal (uang di laci, saldo rekening, stok, piutang, utang) dengan `catat --jenis saldo-awal`.
Agar hledger langsung memakai file ini, atur variabel LEDGER_FILE (lihat docs/panduan-hledger.md).
(kode keluar: 0)

$ python3 hledger_usaha.py catat --jenis saldo-awal --tanggal 2026-06-30 --posting Aset:Kas=2.000.000 --posting Aset:Bank:BCA=10.000.000 --posting Aset:Persediaan=3.000.000 --posting Utang:Bank=-5.000.000
PRATINJAU CATATAN (BELUM disimpan)
File: ~/Pembukuan/usaha.journal

2026-06-30 Saldo awal
    Aset:Kas                                        Rp 2.000.000
    Aset:Bank:BCA                                  Rp 10.000.000
    Aset:Persediaan                                 Rp 3.000.000
    Utang:Bank                                     -Rp 5.000.000
    Modal:Saldo Awal                              -Rp 10.000.000
Artinya: Saldo awal pembukuan per 30 Juni 2026.

Simpan 1 transaksi ini? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode keluar: 0)

$ python3 hledger_usaha.py catat --jenis saldo-awal --tanggal 2026-06-30 --posting Aset:Kas=2.000.000 --posting Aset:Bank:BCA=10.000.000 --posting Aset:Persediaan=3.000.000 --posting Utang:Bank=-5.000.000 --ya
TERSIMPAN
File: ~/Pembukuan/usaha.journal

2026-06-30 Saldo awal
    Aset:Kas                                        Rp 2.000.000
    Aset:Bank:BCA                                  Rp 10.000.000
    Aset:Persediaan                                 Rp 3.000.000
    Utang:Bank                                     -Rp 5.000.000
    Modal:Saldo Awal                              -Rp 10.000.000
Artinya: Saldo awal pembukuan per 30 Juni 2026.

Tersimpan 1 transaksi ke ~/Pembukuan/usaha.journal. Cadangan versi sebelumnya: usaha.journal.sebelum-ubah
(kode keluar: 0)

$ python3 hledger_usaha.py catat --jenis jual --nominal 750rb --via tempo --pihak Kantor Maju Jaya --ket Kopi rapat 30 cup --tanggal 2026-07-02
PRATINJAU CATATAN (BELUM disimpan)
File: ~/Pembukuan/usaha.journal

2026-07-02 Kopi rapat 30 cup  ; pihak:Kantor Maju Jaya
    Aset:Piutang Usaha:Kantor Maju Jaya               Rp 750.000
    Pendapatan:Penjualan                             -Rp 750.000
Artinya: Penjualan Rp 750.000 kepada Kantor Maju Jaya, belum dibayar (piutang bertambah).

Akun baru yang akan dibuat: Aset:Piutang Usaha:Kantor Maju Jaya
Simpan 1 transaksi ini? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.
(kode keluar: 0)

$ python3 hledger_usaha.py catat --batch batch-juli.json --ya
TERSIMPAN
File: ~/Pembukuan/usaha.journal

2026-07-01 Penjualan harian kopi
    Aset:Kas                                        Rp 1.250.000
    Pendapatan:Penjualan                           -Rp 1.250.000
Artinya: Penjualan Rp 1.250.000, uang masuk ke Aset:Kas.

2026-07-02 Kopi rapat 30 cup  ; pihak:Kantor Maju Jaya
    Aset:Piutang Usaha:Kantor Maju Jaya               Rp 750.000
    Pendapatan:Penjualan                             -Rp 750.000
Artinya: Penjualan Rp 750.000 kepada Kantor Maju Jaya, belum dibayar (piutang bertambah).

2026-07-03 Biji kopi 10 kg  ; pihak:Roastery Gayo
    HPP:Pembelian                                   Rp 2.000.000
    Aset:Bank:BCA                                  -Rp 2.000.000
Artinya: Beli barang dagangan/bahan Rp 2.000.000 dari Roastery Gayo, dibayar dari Aset:Bank:BCA.

2026-07-05 Token listrik
    Beban:Listrik Air Internet                        Rp 350.000
    Aset:Kas                                         -Rp 350.000
Artinya: Biaya Rp 350.000 untuk Beban:Listrik Air Internet.

2026-07-06 Susu 1 bulan  ; pihak:Susu Segar CV
    HPP:Pembelian                                   Rp 1.500.000
    Utang:Usaha:Susu Segar CV                      -Rp 1.500.000
Artinya: Beli barang dagangan/bahan Rp 1.500.000 dari Susu Segar CV, belum dibayar (utang bertambah).

2026-07-10 Prive (ambil untuk pribadi)
    Modal:Prive                                       Rp 500.000
    Aset:Kas                                         -Rp 500.000
Artinya: Pemilik mengambil uang usaha untuk pribadi Rp 500.000 (prive, mengurangi modal, BUKAN beban).

2026-07-15 Terima pelunasan - Kantor Maju Jaya  ; pihak:Kantor Maju Jaya
    Aset:Bank:BCA                                     Rp 750.000
    Aset:Piutang Usaha:Kantor Maju Jaya              -Rp 750.000
Artinya: Pelanggan membayar piutang Rp 750.000 (piutang berkurang).

2026-07-16 Grinder kopi
    Aset:Peralatan                                  Rp 4.500.000
    Aset:Bank:BCA                                  -Rp 4.500.000
Artinya: Beli peralatan/aset Rp 4.500.000 (dicatat sebagai aset, bukan beban bulan ini).

2026-07-20 Angsuran pinjaman
    Utang:Bank                                        Rp 400.000
    Beban:Bunga                                        Rp 50.000
    Aset:Bank:BCA                                    -Rp 450.000
Artinya: Bayar angsuran Rp 450.000: pokok Rp 400.000 (utang berkurang), bunga Rp 50.000 (beban).

2026-07-21 Setor tunai ke BCA
    Aset:Bank:BCA                                   Rp 1.000.000
    Aset:Kas                                       -Rp 1.000.000
Artinya: Pindah uang sendiri Rp 1.000.000 dari Aset:Kas ke Aset:Bank:BCA (bukan pendapatan/biaya).

2026-07-25 Gaji 2 barista
    Beban:Gaji                                      Rp 3.000.000
    Aset:Bank:BCA                                  -Rp 3.000.000
Artinya: Biaya Rp 3.000.000 untuk Beban:Gaji.

2026-07-28 Penjualan QRIS Juli
    Aset:Bank:BCA                                   Rp 6.800.000
    Pendapatan:Penjualan                           -Rp 6.800.000
Artinya: Penjualan Rp 6.800.000, uang masuk ke Aset:Bank:BCA.

Akun baru yang akan dibuat: Aset:Piutang Usaha:Kantor Maju Jaya, Utang:Usaha:Susu Segar CV
Tersimpan 12 transaksi ke ~/Pembukuan/usaha.journal. Cadangan versi sebelumnya: usaha.journal.sebelum-ubah
(kode keluar: 0)

$ python3 hledger_usaha.py stok-akhir --tanggal 2026-07-31 --nilai 2.700.000
PENYESUAIAN PERSEDIAAN per 31 Juli 2026
Nilai stok hasil hitung: Rp 2.700.000
Nilai Aset:Persediaan di catatan: Rp 3.000.000

2026-07-31 Penyesuaian persediaan (hitung stok)
    Aset:Persediaan                                  -Rp 300.000
    HPP:Penyesuaian Persediaan                        Rp 300.000

Artinya: stok turun Rp 300.000; HPP bulan ini bertambah sebesar itu (barang terjual/terpakai/rusak lebih banyak dari stok baru).
Simpan? Setelah pengguna menjawab ya, ulangi dengan --ya.
(kode keluar: 0)

$ python3 hledger_usaha.py stok-akhir --tanggal 2026-07-31 --nilai 2.700.000 --ya
PENYESUAIAN PERSEDIAAN per 31 Juli 2026
Nilai stok hasil hitung: Rp 2.700.000
Nilai Aset:Persediaan di catatan: Rp 3.000.000

2026-07-31 Penyesuaian persediaan (hitung stok)
    Aset:Persediaan                                  -Rp 300.000
    HPP:Penyesuaian Persediaan                        Rp 300.000

Artinya: stok turun Rp 300.000; HPP bulan ini bertambah sebesar itu (barang terjual/terpakai/rusak lebih banyak dari stok baru).
TERSIMPAN ke ~/Pembukuan/usaha.journal
(kode keluar: 0)

$ hledger check accounts   (hledger 1.52.4 asli)
(lulus, tanpa pesan)
```

**Catatan pembuat:** semua entri seimbang, piutang/utang per pihak tercatat di sub-akun, prive masuk `Modal:Prive` (bukan beban), angsuran dipecah pokok/bunga, setor tunai = pindah dana. Pratinjau batch dipotong di file ini (12 entri penuh ada di keluaran asli).
