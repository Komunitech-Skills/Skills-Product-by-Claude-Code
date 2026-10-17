# Referensi perintah `scripts/kasir.py`

Semua perintah menerima `--db PATH` dan `--json` (tulis **setelah** nama perintah, mis. `kasir.py jual --db D:\kasir.db ...`). Perintah bertanda **(tulis)** hanya menyimpan jika diberi `--ya`; tanpa `--ya` hasilnya pratinjau (`"mode": "pratinjau"`, `"perlu_konfirmasi": true`) yang dijalankan dalam transaksi lalu dibatalkan, jadi angka & nomor nota di pratinjau sama persis dengan yang akan tersimpan.

Angka gaya Indonesia: `15000`, `15.000`, `Rp 15.000`, `15.000,-`, `100rb`, `1,5jt`, `1,5` (desimal). Format meragukan (`1,250,000.50`, `15.000.00`, `1,5E+04`) ditolak.
Waktu: `2026-09-24 10:15` atau `24/09/2026 10.15`. Tanggal: `hari-ini`, `kemarin`, `2026-09-24`, `24/09/2026`. Bulan: `ini`, `lalu`, `2026-09`, `09/2026`.

| Perintah | Fungsi | Opsi penting |
|---|---|---|
| `init` (tulis) | Buat database. Jika sudah ada, tidak mengubah apa pun | `--nama-toko` (wajib) `--alamat --telp --footer --npwp --pajak tanpa\|ppn-belum\|ppn-termasuk\|pbjt-belum\|pbjt-termasuk --pkp ya\|tidak --tarif-pbjt N --service-charge N --sc-kena-pajak ya\|tidak --zona WIB\|WITA\|WIT --stok tidak\|kasir\|buku-stok --kertas 58\|80` |
| `mulai` (tulis) | **Pemakaian pertama, satu konfirmasi:** `init` + `produk impor` + `jual` dalam satu perintah. Tanpa `--ya` = pratinjau gabungan (daftar produk, pengaturan toko dengan bagian "Saya anggap", nota + struk teks); dicoba dulu di salinan sementara sehingga bila gagal buku kasir asli tidak tersentuh. Ditolak bila buku kasir sudah ada. JSON: `asumsi`, `produk_baru`, `no`, `total`, `kembalian`, `struk_teks`, `struk_baris`, `nota` | `--produk FILE` (wajib) `--nama-toko` (wajib) `--pesan "..."` (opsional; tanpa ini tidak ada nota) `--kasir --catatan` + semua opsi toko seperti `init` |
| `atur` (tulis) | Ubah pengaturan (berlaku untuk nota berikutnya) | sama seperti `init` |
| `info` | Lokasi DB, pengaturan, jumlah produk/nota, sesi kasir, backup terakhir; peringatan bila zona jam komputer ≠ zona toko | — |
| `produk tambah` (tulis) | Tambah produk | `--kode --nama --harga` wajib; `--varian --satuan --stok` |
| `produk ubah` (tulis) | Ubah produk | `--kode` + `--nama --varian --harga --satuan --stok --kode-baru --tanpa-stok --nonaktif --aktif` |
| `produk cari [kata]` | Cari produk | `--semua` (termasuk nonaktif) |
| `produk impor FILE` (tulis, backup) | Impor CSV. Kolom dikenali: Kode/SKU/PLU/Barcode, Nama/Produk/Menu, Varian, Harga/Harga Jual, Satuan, Stok. Kode kosong → otomatis `P001`… | `--perbarui` (perbarui nama/harga kode yang sudah ada) |
| `stok` (tulis) | Barang datang / hasil hitung fisik (mode stok `kasir`) | `--kode` + `--tambah N` atau `--jadi N`; `--catatan` |
| `jual` (tulis) | Catat nota penjualan. Hasil (pratinjau dan tersimpan) memuat `struk_teks` (blok kode; 32 kolom untuk kertas 58 mm, 48 untuk 80 mm) dan `struk_baris`; `teks` setelah `--ya` = nomor nota, total, kembalian, catatan, lalu struk. Di `--pesan`, awalan "Tolong catat penjualan:" dan permintaan struk ("bikinin struknya", "kirim struknya ke sini ya") diabaikan; kata "struk" di dalam nama barang ("kertas struk") tidak pernah dibuang; "struk 58mm" ditolak (pakai `--kertas`) | `--pesan "..."` atau `--item` (berulang); `--diskon` (nota); `--bayar metode=jumlah` (berulang); `--kasir --catatan --waktu --izinkan-duplikat --izinkan-minus --struk 58\|80` |
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
- Item: `2 kopi susu` · `kopi susu x2` · `kopi susu 2` · `dua kopi hitam` · `setengah kg gula` · `1,5 kg gula pasir` · `2kg gula` · `KH=2` · `2 sak semen` · `semen 2 sak` · `0,5 m3 pasir`
- Satuan: semua satuan di tabel produk + satuan umum (sak, pail, dus, lusin, lembar, batang, rol, ikat, m, m2, m3, ton, liter, …) dikenali di depan atau belakang nama, di `jual` maupun `retur`. Satuan yang disebut harus sama dengan satuan produk (alias: kilo=kg, zak=sak, kubik=m3, …) atau satuan hitung generik (buah/pcs/biji/unit untuk produk yang tidak ditimbang); selain itu ditolak (mis. `2 lusin` untuk produk per pcs). Bila beberapa produk cocok, satuan dipakai untuk mempersempit (`0,5 m3 pasir` → Pasir Beton, disebut di pratinjau). Pecahan hanya untuk kg, gram, ons, liter, ml, cc, m, cm, m2, m3, ton, kwintal.
- Diskon item: `3 es teh diskon 10%` · `diskon 2rb` · `diskon 10%+5%`
- Diskon nota: segmen yang diawali `diskon`/`potongan`: `diskon 10%`, `diskon 5rb`, `diskon 10%+2rb`
- Bayar: `bayar tunai 100rb` · `bayar pas` · `bayar qris` · `bayar qris 50rb, tunai 50rb` · `bayar transfer`. Metode: Tunai, QRIS, Transfer, Debit, Kartu kredit, E-wallet (OVO/GoPay/DANA/ShopeePay/LinkAja), Lainnya. Satu metode boleh tanpa jumlah (= sisa).
- Catatan: `catatan: meja 4`, `atas nama Budi`.
- Ditolak: `bon`, `utang`, `bayar nanti`, `tempo`; harga di pesanan (`@15rb`). Bon/utang dicatat di skill `buku-piutang` (kasir hanya mencatat yang sudah dibayar); belum terpasang → cara lama `buat-invoice`.

Pencocokan produk: kode persis → nama+varian persis → nama persis (satu produk) → semua kata ada di tepat satu produk (disebut di pratinjau "dibaca sebagai"). Selain itu **ditolak** dengan saran produk mirip; tidak pernah ditebak.

## Nomor nota
`N-YYMMDD-0001` untuk penjualan, `R-YYMMDD-0001` untuk retur/void; berurutan per hari, tidak pernah dipakai ulang atau dihapus.

## Format CSV
- **Penjualan** (`rekap --csv`, `ekspor --format penjualan`): `Tanggal;Jam;No. Nota;Jenis;Kode;Produk;Varian;Qty;Satuan;Harga Satuan;Diskon;Total;Status;Metode Bayar`. Retur/void = baris minus, Status tetap `Selesai`, sehingga jumlah kolom Total = penjualan bersih. Untuk `rekap-penjualan-csv`: `--kolom-tanggal "Tanggal" --kolom-produk "Produk" --kolom-qty "Qty" --kolom-total "Total" --kolom-status "Status"`. Total pada mode PPN belum termasuk = sebelum PPN.
- **Buku-stok** (`ekspor --format buku-stok`): `Nomor Pesanan;Tanggal;SKU;Nama Produk;Varian;Jumlah;Harga Satuan;Status` (Status `Selesai` atau `Dibatalkan` bila di-void; harga satuan = setelah diskon). Diimpor dengan `stok.py impor-pesanan FILE --platform lainnya`. Retur sebagian tidak ikut (catat manual `masuk --jenis retur-pembeli`).
- Semua CSV: UTF-8 dengan BOM, pemisah `;` (Excel Indonesia), qty pecahan ditulis `1,5`; teks diawali `= + @` atau `-` yang bukan angka diberi `'` (anti formula injection); angka minus (`-2,5`) tetap angka.

## Zona waktu
Waktu nota = jam **zona toko** (`--zona`, default WIB/Asia/Jakarta; WITA = Asia/Makassar, WIT = Asia/Jayapura, juga Asia/Pontianak), bukan jam komputer — penting di VPS yang memakai UTC. Offset (+07:00/+08:00/+09:00) disimpan di setiap nota dan label WIB/WITA/WIT dicetak di struk. Memakai `zoneinfo` bila tersedia; tanpa tzdata (mis. Windows) dipakai offset tetap (Indonesia tidak memakai musim panas, jadi hasilnya sama).

## Script terpisah: `scripts/rekap_nota.py` (nota ditempel, tanpa database)
`python3 scripts/rekap_nota.py FILE|- [--teks "..."] [--tanggal LABEL] [--kas-awal N --kas-fisik N] [--kas-masuk N] [--kas-keluar N] [--batal 011,..] [--bukan-batal 012,..] [--grup-tanpa-rupiah] [--json]`
- Tidak menulis apa pun. Membaca teks (satu nota per baris, atau blok `Nota X` + baris item sampai baris kosong) atau CSV (`nota;menu;qty;harga;subtotal;bayar;status`, kolom `pelanggan` diabaikan).
- Nota BATAL/void/dibatalkan dikecualikan (kata "batal" setelah "pengganti/ganti/koreksi" diabaikan). Nomor telepon dibuang sebelum dibaca; bagian nama orang (Pak/Bu/Mbak/a.n.) dibuang dari nama menu.
- Field JSON: `nota_sah`, `nota_batal`, `porsi_total`, `omzet_tercatat` (termasuk bon), `uang_masuk` (tanpa bon), `per_metode`, `menu` (`porsi`, `nota`, `omzet` per menu, urut porsi), `kas` (`seharusnya` = kas awal + tunai + kas masuk − kas keluar; `selisih` = fisik − seharusnya), `perlu_dicek`, `peringatan`, `diabaikan`, `teks` (pemilik), `teks_grup` (RINGKASAN SIAP TEMPEL untuk grup: agregat, tanpa nama/nomor pelanggan & bon per orang).
- Uji: `python3 tests/uji_rekap_nota.py`.

## Kode keluar
`0` berhasil (termasuk pratinjau), `1` gagal dengan pesan jelas (`error`), `2` perintah salah tulis.

## Struktur data (pengguna mahir)
Satu file SQLite: `produk`, `nota` (jual/retur/void, angka rupiah bulat; kolom `ppn` = jumlah pajak PPN atau PBJT sesuai `pajak_mode`, `dpp` = dasar pengenaan, plus `tarif_pajak`, `service`, `service_persen`, `service_kena`, `zona`; database v1.0.0 diperbarui otomatis saat dibuka), `nota_item` (retur menunjuk baris asal lewat `ref_item_id`), `bayar` (jumlah per metode; minus = uang kembali), `sesi` (buka/tutup kasir), `kas`, `stok_mutasi`, `log`, `meta` (pengaturan). Bisa dibuka read-only dengan DB Browser for SQLite atau Datasette; jangan diedit manual.
