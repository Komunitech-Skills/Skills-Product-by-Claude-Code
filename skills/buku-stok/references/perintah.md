# Referensi perintah `scripts/stok.py`

Semua perintah menerima `--db PATH` dan `--json`. Perintah bertanda **(tulis)** hanya menyimpan jika diberi `--ya`; tanpa `--ya` hasilnya pratinjau (`"mode": "pratinjau"`, `"perlu_konfirmasi": true`) dan database tidak berubah sama sekali (transaksi di-rollback).

Angka boleh ditulis gaya Indonesia: `34000`, `34.000`, `Rp 34.000`, `Rp 15.000,-`, `12,5`. Format meragukan (`15.000.00`, `1.5E+06`) ditolak, tidak ditebak.
Tanggal: `2026-09-23`, `23/09/2026`, `23 Sep 2026` (hari dulu, gaya Indonesia).

| Perintah | Fungsi | Opsi penting |
|---|---|---|
| `init` (tulis) | Buat database baru. Jika sudah ada, tidak mengubah apa pun | — |
| `info` | Lokasi DB, jumlah produk/mutasi/pesanan, backup terakhir | — |
| `produk tambah` (tulis) | Tambah produk (1 SKU = 1 varian) | `--sku --nama` wajib; `--varian --satuan --harga-beli --harga-jual --stok-min --lokasi --stok-awal --tanggal` |
| `produk ubah` (tulis) | Ubah data produk | `--sku` + field yang diubah; `--sku-baru`, `--nonaktif`, `--aktif`, `--koreksi-hpp` (hanya bila HPP salah input) |
| `produk cari [kata]` | Cari SKU/nama/varian/lokasi; kosong = semua | `--semua` (termasuk nonaktif) |
| `produk impor FILE` (tulis, backup) | Impor daftar produk CSV/XLSX. SKU yang sudah ada dilewati | kolom dikenali: SKU, Nama, Varian, Satuan, Harga Beli/Modal, Harga Jual, Stok, Stok Minimum, Lokasi/Rak |
| `masuk` (tulis) | Barang masuk; HPP rata-rata tertimbang diperbarui | `--sku --qty --harga` atau `--file` (SKU, Qty, Harga); `--jenis beli\|retur-pembeli\|saldo-awal\|lainnya`; `--biaya-tambahan` (total, dibagi sesuai nilai item); `--ref --catatan --tanggal` |
| `keluar` (tulis) | Barang keluar; stok tidak cukup = ditolak | `--jenis jual\|retur-supplier\|rusak\|hilang\|pakai-sendiri\|lainnya`; `--harga` (harga jual, default harga jual produk); `--catatan` wajib untuk rusak/hilang/lainnya; `--izinkan-minus` |
| `opname` (tulis, backup) | Hitung fisik → selisih → penyesuaian | `--hitung SKU=n` (berulang) atau `--file` (SKU, Fisik, Alasan); `--alasan` default; `--tanggal --ref` |
| `impor-pesanan FILE` (tulis, backup) | Potong stok dari ekspor pesanan marketplace | `--platform shopee\|tiktok\|tokopedia\|lainnya`; `--kolom-no-pesanan --kolom-sku --kolom-nama --kolom-varian --kolom-qty --kolom-status --kolom-resi --kolom-kurir --kolom-tanggal --kolom-batas-kirim --kolom-harga --kolom-harga-total --kolom-tipe-retur --kolom-qty-retur` (`-` = abaikan); `--abaikan-status "kata1,kata2"`; `--lewati-tak-dikenal` |
| `picking` | Daftar ambil barang + urutan kemas/resi dari pesanan belum dikemas | `--urut kurir\|resi\|batas\|pesanan`; `--csv FILE --csv-pesanan FILE --pemisah ";"`; `--platform`; `--tandai-dikemas` (tulis) |
| `laporan stok` | Stok, HPP, nilai persediaan, status (aman/MENIPIS/HABIS/MINUS) | `--cari --csv` |
| `laporan menipis` | Stok ≤ minimum atau habis + rata-rata laku/hari (30 hari) + perkiraan habis | `--csv` |
| `laporan tidak-laku` | Masih ada stok tapi tidak terjual N hari + modal tertahan | `--hari 30 --csv` |
| `laporan mutasi` | Awal + masuk − keluar ± opname = akhir per produk + rincian | `--dari --sampai --sku --ringkas-saja --csv` (default: awal bulan s/d hari ini) |
| `laporan ringkas` | Ringkasan harian siap kirim (untuk jadwal) | `--tanggal --hari` |
| `backup` | Salinan DB bertanggal di `backup-stok/` | `--label`, `--daftar` |
| `restore` (tulis) | Ganti DB aktif dengan backup (DB aktif dibackup dulu) | `--dari FILE` |

## Rumus
- **HPP rata-rata tertimbang (bergerak):** `HPP_baru = (stok_lama × HPP_lama + qty_masuk × harga_masuk) ÷ (stok_lama + qty_masuk)`; jika `stok_lama ≤ 0` → `HPP_baru = harga_masuk`. Keluar & opname tidak mengubah HPP.
- **Biaya tambahan:** `porsi_item = biaya × (qty_item × harga_item) ÷ total_nilai_nota`; `harga_masuk = harga_item + porsi_item ÷ qty_item`.
- **Nilai persediaan:** `Σ max(stok, 0) × HPP`, dibulatkan ke rupiah terdekat (0,5 ke atas).
- **Opname:** `selisih = fisik − (stok_sistem + barang pesanan yang belum dikemas)`; nilai selisih = selisih × HPP.
- **Pesanan batal setelah diimpor:** mutasi penjualannya ditandai `dibatalkan=1` dan tidak dihitung di laporan penjualan (ringkas, mutasi, rata-rata laku, tidak laku); stoknya dikembalikan lewat mutasi `batal-pesanan`.
- **Laba kotor (laporan ringkas):** omzet transaksi jual yang punya harga − (qty × HPP saat keluar). Belum dikurangi biaya admin marketplace, ongkir, iklan, pajak.

## Kode keluar
`0` = berhasil (termasuk pratinjau), `1` = gagal dengan pesan jelas (`error`), `2` = salah penulisan perintah (argparse).

## Struktur data (untuk pengguna mahir)
Satu file SQLite: tabel `produk` (stok & HPP terkini), `mutasi` (riwayat setiap perubahan stok, bertanda + masuk / − keluar), `pesanan` + `pesanan_item` (nomor pesanan marketplace yang sudah diimpor, status, resi, sudah dikemas), `impor`, `log` (setiap operasi yang disimpan), `meta`. Database versi 1.0.0 otomatis diperbarui saat dibuka (kolom `mutasi.dibatalkan`, tanpa mengubah angka stok). Stok di `produk` selalu sama dengan jumlah `mutasi` (diuji di `uji_regresi.py`). File bisa dibuka read-only dengan DB Browser for SQLite atau Datasette; jangan diedit manual.
