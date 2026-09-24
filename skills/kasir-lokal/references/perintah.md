# Referensi perintah `scripts/kasir.py`

Semua perintah menerima `--db PATH` dan `--json` (tulis **setelah** nama perintah, mis. `kasir.py jual --db D:\kasir.db ...`). Perintah bertanda **(tulis)** hanya menyimpan jika diberi `--ya`; tanpa `--ya` hasilnya pratinjau (`"mode": "pratinjau"`, `"perlu_konfirmasi": true`) yang dijalankan dalam transaksi lalu dibatalkan, jadi angka & nomor nota di pratinjau sama persis dengan yang akan tersimpan.

Angka gaya Indonesia: `15000`, `15.000`, `Rp 15.000`, `15.000,-`, `100rb`, `1,5jt`, `1,5` (desimal). Format meragukan (`1,250,000.50`, `15.000.00`, `1,5E+04`) ditolak.
Waktu: `2026-09-24 10:15` atau `24/09/2026 10.15`. Tanggal: `hari-ini`, `kemarin`, `2026-09-24`, `24/09/2026`. Bulan: `ini`, `lalu`, `2026-09`, `09/2026`.

| Perintah | Fungsi | Opsi penting |
|---|---|---|
| `init` (tulis) | Buat database. Jika sudah ada, tidak mengubah apa pun | `--nama-toko` (wajib) `--alamat --telp --footer --npwp --pajak tanpa\|ppn-belum\|ppn-termasuk --pkp ya\|tidak --stok tidak\|kasir\|buku-stok --kertas 58\|80` |
| `atur` (tulis) | Ubah pengaturan (berlaku untuk nota berikutnya) | sama seperti `init` |
| `info` | Lokasi DB, pengaturan, jumlah produk/nota, sesi kasir, backup terakhir | — |
| `produk tambah` (tulis) | Tambah produk | `--kode --nama --harga` wajib; `--varian --satuan --stok` |
| `produk ubah` (tulis) | Ubah produk | `--kode` + `--nama --varian --harga --satuan --stok --kode-baru --tanpa-stok --nonaktif --aktif` |
| `produk cari [kata]` | Cari produk | `--semua` (termasuk nonaktif) |
| `produk impor FILE` (tulis, backup) | Impor CSV. Kolom dikenali: Kode/SKU/PLU/Barcode, Nama/Produk/Menu, Varian, Harga/Harga Jual, Satuan, Stok. Kode kosong → otomatis `P001`… | `--perbarui` (perbarui nama/harga kode yang sudah ada) |
| `stok` (tulis) | Barang datang / hasil hitung fisik (mode stok `kasir`) | `--kode` + `--tambah N` atau `--jadi N`; `--catatan` |
| `jual` (tulis) | Catat nota penjualan | `--pesan "..."` atau `--item` (berulang); `--diskon` (nota); `--bayar metode=jumlah` (berulang); `--kasir --catatan --waktu --izinkan-duplikat --izinkan-minus --struk 58\|80` |
| `retur` (tulis) | Retur sebagian barang (entri balik `R-…`) | `--nota --item` (berulang) `--alasan` wajib; `--refund tunai\|qris\|transfer…`; `--stok-kembali ya\|tidak`; `--waktu` |
| `void` (tulis) | Batalkan seluruh nota (entri balik `R-…`) | `--nota --alasan` wajib; `--stok-kembali`; `--waktu` |
| `nota` | Satu nota (`--no N-…`) atau daftar nota per `--tanggal` | — |
| `struk` | Struk HTML siap cetak (default nota terakhir) | `--nota --kertas 58\|80 --keluar FILE --teks` |
| `buka-kasir` (tulis) | Mulai sesi dengan kas awal | `--kas-awal` wajib; `--kasir --waktu` (waktu lampau: nota sejak jam itu ikut sesi) |
| `kas` (tulis) | Uang laci masuk/keluar di luar penjualan | `--masuk N` atau `--keluar N`; `--catatan` wajib |
| `tutup-kasir` (tulis, backup) | Hitung kas seharusnya, selisih, setoran | `--kas-fisik` wajib; `--setoran --catatan --waktu` |
| `rekap` | Rekap teks siap Telegram | `--tanggal \| --bulan \| --tahun \| --dari --sampai`; `--csv FILE --csv-produk FILE --pemisah ";"` |
| `ekspor` | CSV penjualan per baris nota, atau file untuk buku-stok | `--format penjualan\|buku-stok --csv FILE` + periode |
| `backup` | Salinan DB bertanggal di `backup-kasir/` | `--label --daftar` |
| `restore` (tulis) | Ganti DB aktif dengan backup (DB aktif dibackup dulu) | `--dari FILE` |

## Bahasa pesanan (`jual --pesan`)
Dipisah koma (bukan koma di dalam angka), titik koma, baris baru, "dan", "sama".
- Item: `2 kopi susu` · `kopi susu x2` · `kopi susu 2` · `dua kopi hitam` · `setengah kg gula` · `1,5 kg gula pasir` · `KH=2`
- Diskon item: `3 es teh diskon 10%` · `diskon 2rb` · `diskon 10%+5%`
- Diskon nota: segmen yang diawali `diskon`/`potongan`: `diskon 10%`, `diskon 5rb`, `diskon 10%+2rb`
- Bayar: `bayar tunai 100rb` · `bayar pas` · `bayar qris` · `bayar qris 50rb, tunai 50rb` · `bayar transfer`. Metode: Tunai, QRIS, Transfer, Debit, Kartu kredit, E-wallet (OVO/GoPay/DANA/ShopeePay/LinkAja), Lainnya. Satu metode boleh tanpa jumlah (= sisa).
- Catatan: `catatan: meja 4`, `atas nama Budi`.
- Ditolak: `bon`, `utang`, `bayar nanti`, `tempo`; harga di pesanan (`@15rb`).

Pencocokan produk: kode persis → nama+varian persis → nama persis (satu produk) → semua kata ada di tepat satu produk (disebut di pratinjau "dibaca sebagai"). Selain itu **ditolak** dengan saran produk mirip; tidak pernah ditebak.

## Nomor nota
`N-YYMMDD-0001` untuk penjualan, `R-YYMMDD-0001` untuk retur/void; berurutan per hari, tidak pernah dipakai ulang atau dihapus.

## Format CSV
- **Penjualan** (`rekap --csv`, `ekspor --format penjualan`): `Tanggal;Jam;No. Nota;Jenis;Kode;Produk;Varian;Qty;Satuan;Harga Satuan;Diskon;Total;Status;Metode Bayar`. Retur/void = baris minus, Status tetap `Selesai`, sehingga jumlah kolom Total = penjualan bersih. Untuk `rekap-penjualan-csv`: `--kolom-tanggal "Tanggal" --kolom-produk "Produk" --kolom-qty "Qty" --kolom-total "Total" --kolom-status "Status"`. Total pada mode PPN belum termasuk = sebelum PPN.
- **Buku-stok** (`ekspor --format buku-stok`): `Nomor Pesanan;Tanggal;SKU;Nama Produk;Varian;Jumlah;Harga Satuan;Status` (Status `Selesai` atau `Dibatalkan` bila di-void; harga satuan = setelah diskon). Diimpor dengan `stok.py impor-pesanan FILE --platform lainnya`. Retur sebagian tidak ikut (catat manual `masuk --jenis retur-pembeli`).
- Semua CSV: UTF-8 dengan BOM, pemisah `;` (Excel Indonesia), qty pecahan ditulis `1,5`; teks diawali `= + - @` diberi `'` (anti formula injection).

## Kode keluar
`0` berhasil (termasuk pratinjau), `1` gagal dengan pesan jelas (`error`), `2` perintah salah tulis.

## Struktur data (pengguna mahir)
Satu file SQLite: `produk`, `nota` (jual/retur/void, angka rupiah bulat), `nota_item` (retur menunjuk baris asal lewat `ref_item_id`), `bayar` (jumlah per metode; minus = uang kembali), `sesi` (buka/tutup kasir), `kas`, `stok_mutasi`, `log`, `meta` (pengaturan). Bisa dibuka read-only dengan DB Browser for SQLite atau Datasette; jangan diedit manual.
