# Integrasi dengan skill Komunitech lain

kas-umkm adalah **pencatatan harian**. Tiga skill lain punya tugas berbeda; kas-umkm hanya menyiapkan file untuk
mereka dan tidak mengubah skill tersebut.

| Skill | Tugasnya | Hubungan dengan kas-umkm |
|---|---|---|
| `kasir-lokal` | Nota per pembeli, struk, tutup kasir | Rekap harian kasir **diimpor** ke kas-umkm |
| `laporan-keuangan-emkm` | Laba rugi + neraca SAK EMKM (periode yang sudah lewat) | kas-umkm **mengekspor** buku kas ke format yang dibacanya |
| `arus-kas-13minggu` | Proyeksi kas 13 minggu ke depan | kas-umkm **mengekspor** draf rencana dari riwayat |

## 1. Dari kasir-lokal (impor rekap harian)
Format yang dipakai: keluaran `kasir.py rekap --tanggal <tgl> --json` (field `periode`, `per_metode`, `total_diterima`,
`pajak`). `per_metode` adalah uang yang benar-benar diterima per metode, sudah dikurangi kembalian dan uang retur,
sudah termasuk PPN/PBJT dan service charge.

```bash
python3 <folder-kasir-lokal>/scripts/kasir.py rekap --tanggal hari-ini --json > rekap-kasir.json
python3 <folder-kas-umkm>/scripts/kas.py impor-kasir rekap-kasir.json          # pratinjau
python3 <folder-kas-umkm>/scripts/kas.py impor-kasir rekap-kasir.json --ya     # setelah setuju
```
- Satu file = satu hari. Rekap rentang/bulanan ditolak (tanggal kas harus tepat).
- Pemetaan metode kasir → akun: Tunai → akun tunai; QRIS → akun penampung QRIS; Transfer, Debit, Kartu kredit →
  rekening bank; E-wallet → akun e-wallet; **Lainnya (voucher) tidak dicatat** (bukan uang). Beberapa rekening bank →
  `--akun-untuk transfer=BCA --akun-untuk kartu=BRI`.
- Nilai per metode minus (uang retur lebih besar dari penjualan metode itu) dicatat sebagai keluar kategori penjualan
  (retur/refund).
- Tanggal yang sama tidak bisa diimpor dua kali. Kasir menerima transaksi lagi setelah diimpor → ekspor ulang lalu
  `--ganti` (impor lama dibatalkan dengan alasan, tidak dihapus).
- PPN/PBJT yang ikut diterima disebut di peringatan; saat disetor, catat `--keluar ... --kategori pajak`.
- Pengeluaran laci yang dicatat di kasir (`kasir.py kas --keluar`) **tidak** ikut. Bila memakai keduanya, catat
  penjualan lewat kasir saja (jangan juga dicatat manual di kas-umkm), dan catat pengeluaran usaha di kas-umkm.
- Windows PowerShell 5 menyimpan `>` sebagai UTF-16; kas-umkm membacanya otomatis.

## 2. Ke laporan-keuangan-emkm (laba rugi & neraca)
```bash
python3 <folder-kas-umkm>/scripts/kas.py ekspor --format emkm --bulan 09/2026 --csv kas-emkm-2026-09.csv
```
Hasil: CSV `Tanggal;Keterangan;Masuk;Keluar;Kategori` (UTF-8 BOM, tanggal DD/MM/YYYY):
- Baris pertama `Saldo awal` = gabungan saldo semua akun (laci + rekening + e-wallet) di awal periode; emkm memakainya
  sebagai kas awal.
- Kolom Kategori berisi kode emkm: penjualan → `pendapatan_usaha` (keluar → `retur_penjualan`), modal →
  `setoran_modal`, beli-stok → `pembelian_bahan`, gaji → `beban_gaji`, listrik-air → `beban_utilitas`, sewa →
  `beban_sewa`, prive → `prive`, pinjaman → `pinjaman_diterima`/`bayar_pinjaman`, kasbon (v1.0.3) → `piutang_lain`, selisih hitung laci →
  `pendapatan_lain`/`beban_lain`.
- Kategori `pajak` sengaja dikosongkan agar emkm mengklasifikasi dari keterangan (mis. "PPh final" → beban PPh,
  "PBJT" → pajak daerah + pertanyaan). Keterangan pajak tanpa kata pajak diberi awalan "Pajak: ".
- `lain-lain` (v1.0.2): pemasukan → `pendapatan_lain`; biaya bank (biaya tarik tunai/adm/transfer, atau biaya/adm di
  akun bank/e-wallet selain admin marketplace) → `beban_keuangan`; pengeluaran yang keterangannya memuat kata pindah
  dana/prive/modal/pinjaman (mis. "PINDAH BUKU" yang digolongkan lain-lain) → `beban_lain`; selain itu dikosongkan agar
  emkm memilih pos beban yang lebih rinci. Tujuannya: laba emkm = hasil usaha kas-umkm (dulu "BIAYA TARIK TUNAI" dibaca
  emkm sebagai pindah dana → laba lebih besar Rp 7.500 dan neraca tidak seimbang).
- v1.0.3: catatan baru `lain-lain` berketerangan kasbon/uang muka karyawan, keperluan pribadi, atau utang/cicilan
  sudah dipindah ke `kasbon`/`prive`/`pinjaman` saat dicatat. Catatan LAMA yang masih `lain-lain` tetap ditulis
  `beban_lain` (laba emkm = hasil usaha) dan ekspor memberi daftar perintah `golongkan --id N --kategori …` untuk
  membetulkannya. Bila ada cicilan/bayar utang, ekspor mengingatkan `--utang-bank-awal <sisa utang awal periode>`
  (tanpa ini sisa utang emkm minus dan neraca tidak seimbang); kasbon yang dikembalikan melebihi yang diberikan →
  `--piutang-lain-awal`.
- v1.0.4: `lain-lain` keluar berketerangan bunga/denda/biaya + cicilan/angsuran/utang/pinjaman → `beban_keuangan`;
  utang/bon ke pemasok/toko/grosir → `bayar_utang_usaha` (emkm menghitungnya sebagai pembelian kredit bila tidak ada
  `--utang-usaha-awal`, jadi laba tetap = hasil usaha; isi `--utang-usaha-awal` hanya bila bon itu memang sudah
  tercatat sebagai utang di awal periode); denda/sanksi pajak (kategori `pajak` maupun `lain-lain`) → `beban_lain`.
- v1.0.5: "PAJAK BUNGA"/"PPh bunga" (PPh final atas bunga tabungan/jasa giro, kategori `pajak` atau `lain-lain`) → `beban_pajak_penghasilan`, bukan `beban_lain`. Catatan gabungan pokok + denda tidak bisa dibuat lagi (dipisah saat catat/impor), jadi pokok selalu `bayar_pinjaman` dan denda `beban_keuangan`.
- v1.0.6: pengeluaran `lain-lain` berisi kata alat/aset (mesin, rak, etalase, kulkas, meja, renovasi…, bukan servis/perbaikan) tetap dikirim dengan kolom Kategori kosong; laporan-keuangan-emkm dapat menggolongkannya `aset_tetap` sehingga **laba emkm = hasil usaha + nilai aset tersebut (dikurangi penyusutan)**. Ekspor menuliskan catatan berisi daftar baris dan totalnya; bila pengguna ingin barang kecil dihitung beban, isi kolom Kategori baris itu dengan `beban_lain`.
- v1.0.7: pengeluaran `lain-lain` lainnya **tidak lagi dikosongkan** (dulu mis. "belanja dapur" masuk "BELUM TERKLASIFIKASI" dan laporan ditandai sementara). Kode rinci dari keterangan: servis/perbaikan → `beban_perawatan`, bensin/parkir/ongkir → `beban_transportasi`, gas/elpiji/internet/pulsa → `beban_utilitas`, materai/retribusi → `beban_pajak_lain`, iklan/promosi → `beban_pemasaran`, kemasan/plastik/ATK → `beban_perlengkapan`, admin/komisi marketplace → `beban_admin_penjualan`, selain itu `beban_lain`. Semuanya beban usaha, jadi laba emkm tetap = hasil usaha. Yang tetap kosong hanya pembelian alat/aset (lihat v1.0.6).
- Pindah dana antar akun tidak ditulis (kas + rekening dihitung sebagai satu pos kas di emkm). Catatan yang dibatalkan
  tidak ikut.
- Teks script memberi perintah emkm siap pakai, termasuk `--kas-akhir-aktual` = saldo akhir gabungan (cek silang).
  Sebelum menjalankannya, tanyakan stok awal/akhir, piutang, utang, dan aset (lihat SKILL.md emkm).
- v1.0.8: bila ada cicilan pinjaman (`bayar_pinjaman`), teks ekspor memuat satu "PERTANYAAN BUNGA" untuk seluruh
  periode, JSON `baris_cicilan` (nomor baris file; judul = baris 1) dan `perintah_pokok_saja` (= perintah emkm +
  `--bunga N=0` per baris cicilan). Jawaban "ya, pokok saja" → pakai `perintah_pokok_saja`; emkm tidak lagi bertanya
  per baris. Ada cicilan yang masih termasuk bunga → ganti `0` baris itu dengan nominal bunganya.
- Diuji: laba bersih emkm = hasil usaha kas-umkm bila tidak ada stok/piutang/utang/aset (tes otomatis).

## 3. Ke arus-kas-13minggu (proyeksi)
```bash
python3 <folder-kas-umkm>/scripts/kas.py ekspor --format arus-kas --csv rencana-kas.csv [--minggu-riwayat 8]
```
Hasil: CSV `minggu;jenis;kategori;nominal;keterangan;kritis` yang dibaca `proyeksi_kas.py`:
- Jendela riwayat = N minggu penuh (Senin-Minggu) terakhir, default 8; minimal 2 minggu penuh.
- Pos rutin mingguan (penjualan, beli stok, prive, lain-lain) → `semua` dengan rata-rata per minggu (rupiah terdekat).
- Pos bulanan (gaji, sewa, listrik/air, pajak, cicilan) yang muncul di kurang dari separuh minggu → `tgl:<tanggal
  bayar terakhir>` dengan jumlah bulan terakhirnya (dilihat dari 62 hari terakhir). Gaji yang dibayar mingguan tetap
  jadi rata-rata mingguan.
- Kolom kritis: gaji, sewa, listrik/air, pajak, cicilan = `ya`; prive & lain-lain = `tidak`; beli stok kosong (label
  "Beli stok (bahan/supplier)" dikenali arus-kas-13minggu sebagai pembayaran pemasok).
- Modal masuk dan pinjaman cair tidak diproyeksikan (sekali waktu) dan disebut di teks.
- Teks script memberi perintah `proyeksi_kas.py` dengan `--saldo-awal` = total saldo semua akun hari ini dan `--mulai`
  = Senin depan. **Sebelum menjalankannya**, tanyakan rencana yang tidak terlihat di riwayat (THR, piutang yang akan
  dibayar, pembelian besar, musim ramai/sepi) dan tambahkan barisnya.
