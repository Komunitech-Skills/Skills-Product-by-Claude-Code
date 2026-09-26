# Akun, jenis transaksi, dan format jurnal

## 1. Daftar akun bawaan (`init`)
| Akun | Golongan (`type`) | Dipakai untuk |
|---|---|---|
| `Aset:Kas` | C (kas) | Uang tunai di laci/brankas |
| `Aset:Bank:<nama>` | C (kas) | Rekening bank usaha, mis. `Aset:Bank:BCA` (dibuat `init --bank BCA` atau otomatis saat `--bank`) |
| `Aset:Piutang Usaha[:<pihak>]` | A | Pelanggan belum bayar (sub-akun per pelanggan dibuat otomatis) |
| `Aset:Persediaan` | A | Nilai stok barang/bahan (disesuaikan dengan `stok-akhir`) |
| `Aset:Peralatan` | A | Mesin, etalase, laptop, motor usaha (aset tetap) |
| `Utang:Usaha[:<pihak>]` | L | Utang ke pemasok (sub-akun per pemasok dibuat otomatis) |
| `Utang:Bank` | L | Pinjaman bank/KUR/koperasi |
| `Utang:Pajak` | L | Pajak yang sudah dipungut tapi belum disetor (mis. PB1) |
| `Modal:Saldo Awal` | E | Lawan saldo awal saat mulai pembukuan |
| `Modal:Setoran` | E | Pemilik menambah modal |
| `Modal:Prive` | E | Pemilik mengambil uang/barang untuk pribadi (bukan beban) |
| `Pendapatan:Penjualan`, `:Jasa`, `:Lain-lain` | R | Penjualan barang, jasa, bunga/cashback |
| `HPP:Pembelian` | X (HPP) | Beli barang dagang/bahan baku |
| `HPP:Penyesuaian Persediaan` | X (HPP) | Selisih stok akhir (otomatis dari `stok-akhir`) |
| `Beban:Gaji`, `:Sewa`, `:Listrik Air Internet`, `:Transportasi`, `:Pemasaran`, `:Perlengkapan`, `:Perawatan`, `:Admin Bank`, `:Bunga`, `:Pajak Penghasilan`, `:Pajak Lain`, `:Lain-lain` | X | Biaya operasional |
| `Pendapatan:Belum Dikelompokkan`, `Beban:Belum Dikelompokkan` | R / X | Hasil impor bank yang belum jelas; wajib ditanyakan |

Akun baru boleh dibuat di bawah akun utama di atas (mis. `Beban:Kebersihan`) dengan `--akun-baru`, setelah pengguna setuju.

## 2. Kalimat → jenis
| Kalimat pengguna | Perintah `catat` |
|---|---|
| "Jual 1,25 juta tunai" | `--jenis jual --nominal 1,25jt --via kas` |
| "Jualan QRIS masuk BCA 6,8 juta" | `--jenis jual --nominal 6,8jt --via bank --bank BCA` |
| "Kantor Maju ambil kopi 750rb, bayar minggu depan" | `--jenis jual --nominal 750rb --via tempo --pihak "Kantor Maju"` |
| "Jasa desain 2 juta ditransfer" | `--jenis jasa --nominal 2jt --via bank` |
| "Beli biji kopi 2 juta transfer" | `--jenis beli --nominal 2jt --via bank --pihak "Roastery"` |
| "Ambil susu 1,5 juta, bayar bulan depan" | `--jenis beli --nominal 1,5jt --via tempo --pihak "CV Susu"` |
| "Bayar listrik 350rb tunai" | `--jenis beban --akun "Beban:Listrik Air Internet" --nominal 350rb --via kas` |
| "Kantor Maju sudah lunas 750rb via BCA" | `--jenis terima-piutang --nominal 750rb --via bank --pihak "Kantor Maju"` |
| "Lunasi utang CV Susu 1,5 juta" | `--jenis bayar-utang --nominal 1,5jt --via bank --pihak "CV Susu"` |
| "Saya tambah modal 5 juta ke rekening" | `--jenis modal --nominal 5jt --via bank` |
| "Ambil 500rb buat belanja rumah" | `--jenis prive --nominal 500rb --via kas` |
| "Pinjaman KUR cair 50 juta" | `--jenis pinjaman --nominal 50jt --via bank` |
| "Angsuran KUR 1.450.000 (pokok 1,2 jt, bunga 250rb)" | `--jenis angsuran --pokok 1,2jt --bunga 250rb --via bank` |
| "Setor uang laci 1 juta ke BCA" | `--jenis setor-tunai --nominal 1jt` (atau `transfer --dari kas --ke bank`) |
| "Tarik tunai 500rb" | `--jenis tarik-tunai --nominal 500rb` |
| "Beli grinder 4,5 juta" | `--jenis aset --nominal 4,5jt --via bank --ket "Grinder kopi"` |
| Kasus lain | `--jenis bebas --ket "..." --posting "Akun=nominal" --posting "Akun"` (satu baris tanpa nominal dihitung otomatis) |

Tanggal: `--tanggal 2026-09-25`, `25/09/2026`, `25 Sep 2026`, `kemarin` (default hari ini). Nominal: `150000`, `150.000`, `150rb`, `1,5jt`, `Rp 1.250,50`. Angka seperti `62,500` ditolak karena ambigu.
Angsuran tanpa rincian bunga → tanyakan porsi bunga (lihat jadwal angsuran bank); bila tidak tahu, catat seluruhnya sebagai pokok (`--bunga 0`) dan beri tahu pengguna bahwa laba bisa sedikit terlalu tinggi.

## 3. Format jurnal (untuk menulis manual bila Python tidak bisa dijalankan)
```
2026-09-02 Kopi rapat 30 cup  ; pihak:Kantor Maju Jaya
    Aset:Piutang Usaha:Kantor Maju Jaya     Rp 750.000
    Pendapatan:Penjualan                   -Rp 750.000
```
Aturan:
- Baris tanggal di kolom pertama (`YYYY-MM-DD`), baris akun **menjorok** minimal 1 spasi (pakai 4).
- Antara nama akun dan jumlah **minimal 2 spasi** (nama akun boleh berisi 1 spasi).
- Jumlah memakai `Rp`, titik ribuan, koma desimal (file memakai `decimal-mark ,`). Debit positif, kredit negatif. Total harus 0; satu baris boleh tanpa jumlah (dihitung otomatis).
- Komentar diawali `;`. Jangan memakai `;` di keterangan.
- Akun baru wajib didaftarkan dengan baris `account Nama:Akun` sebelum dipakai (hledger `check accounts`).
- Tempel di **akhir** file, dipisah satu baris kosong, lalu `hledger check accounts`.

Debit/kredit singkat: uang/aset **bertambah** = positif; utang/modal/pendapatan **bertambah** = negatif; beban/HPP bertambah = positif.

## 4. Perintah hledger yang setara (untuk pengguna yang ingin melihat sendiri)
| Laporan skill | Perintah hledger |
|---|---|
| `laba-rugi --bulan 2026-09` | `hledger is -p 2026-09` |
| `neraca --tanggal 2026-09-30` | `hledger bs -e 2026-10-01` (tanpa baris modal; skill menambah modal & laba) |
| `arus-kas --bulan 2026-09` | `hledger cf -p 2026-09` (hanya perubahan per akun kas; skill merinci per sumber) |
| `saldo Aset:Kas` | `hledger bal Aset:Kas` |
| `cek` | `hledger check accounts` |
Tampilan hledger membulatkan ke rupiah karena baris `commodity Rp 1.000,`; angka yang disimpan tetap persis sampai sen.
