# CSV untuk Import Wizard Frappe Books (v0.36.0)

Script membuat CSV dengan **3 baris judul** persis seperti tombol "Template" di Import Wizard:
baris 1 = nama jenis data, baris 2 = label kolom, baris 3 = kunci kolom (yang dibaca Frappe Books), lalu data.
Pemisah koma, akhir baris CRLF, UTF-8. Angka tanpa pemisah ribuan (`85000`), tanggal `YYYY-MM-DD`, centang `1`/`0`.

## Kolom yang diisi skill
| Perintah | Jenis di Import Wizard | Kunci kolom |
|---|---|---|
| `csv-pelanggan` | Party | `Party.name`, `Party.role` (Customer/Supplier/Both), `Party.email`, `Party.phone`, `Party.taxId` |
| `csv-barang` | Item | `Item.name`, `Item.itemCode`, `Item.for` (Both), `Item.itemType` (Product/Service), `Item.unit`, `Item.rate`, `Item.description`, `Item.incomeAccount`, `Item.expenseAccount`, `Item.barcode`, `Item.trackItem` |
| `csv-transaksi --jenis penjualan` | Sales Invoice | `SalesInvoice.name` (pengelompok), `.numberSeries` (SINV-), `.party`, `.account` (akun piutang), `.date`, `.terms`, `SalesInvoiceItem.item`, `.rate`, `.quantity`, `.account`, `.tax` |
| `csv-transaksi --jenis pembelian` | Purchase Invoice | sama, dengan `PurchaseInvoice.*` / `PurchaseInvoiceItem.*` (akun utang, seri PINV-) |

Kolom wajib Frappe Books (`required` di skema): Party `name`, `role`; Item `name`, `for`, `incomeAccount`, `expenseAccount`;
Invoice `name`, `party`, `account`, `date`, `numberSeries`, baris `item`, `rate`, `quantity`, `account`.

**Koreksi v1.0.1 (dari uji di Import Wizard asli v0.36.0):**
- `numberSeries` punya nilai bawaan di skema, **tetapi Import Wizard tetap menolak** CSV tanpa kolom itu ("Required fields not
  selected: Number Series"). Script kini selalu menulis kolom `<Skema>.numberSeries`. Dengan kolom `SINV-`, penguji berhasil
  memasukkan 2 draf dengan total cocok dengan pratinjau skill.
- `Party.taxId` tidak ada di file asli yang diuji (kolom `gstin`/`gstType`); kunci yang tidak dikenal diabaikan diam-diam.
  Dengan `--db`, script hanya menulis kolom Tax ID bila memang ada, dan memperingatkan tiap NPWP yang tidak bisa diimpor.
- Nama akun bagan Indonesia bernomor (`Penjualan - 4110.000`): pakai nama persis dari perintah `akun`.

## Urutan impor (penting)
1. **Pelanggan/pemasok** (`csv-pelanggan`) dan **barang** (`csv-barang`) dulu.
2. Baru **transaksi** (`csv-transaksi`) — nama pelanggan, barang, akun, dan pajak harus sudah ada; kalau belum, Import Wizard menolak.
3. Selalu pakai `--db` agar script mencocokkan nama dengan data yang sudah ada (huruf besar/kecil disamakan, yang sudah ada dilewati).

## Langkah di Frappe Books (sampaikan ke pengguna)
1. **Backup dulu**: salin file `.books.db` (tutup Frappe Books sebentar) ke folder lain.
2. Buka Frappe Books → menu **Import Wizard** (di bagian Setup) → pilih jenis (Party / Item / Sales Invoice / Purchase Invoice).
3. **Select File** → pilih CSV dari script → periksa tabel pratinjau; sel merah = nilai tidak cocok (baca pesannya).
4. Klik **Import Data**. Untuk transaksi, saat ditanya apakah dokumen di-*submit*, pilih **tidak** agar masuk sebagai draf,
   lalu cocokkan total tiap invoice dengan pratinjau dari script sebelum di-Submit satu per satu.
5. Nomor invoice final diberi otomatis oleh Number Series (kolom `IMPOR-...` hanya pengelompok baris).

Nama menu bisa sedikit berbeda bila bahasa aplikasi diubah ke Bahasa Indonesia; posisinya tetap di bagian Setup/Pengaturan.
Langkah GUI ini disusun dari kode `src/pages/ImportWizard.vue` dan belum difoto dari aplikasi sungguhan.

## Catatan dari uji di aplikasi asli (v0.36.0)
- **Akun pembelian barang berstok** harus `Stock Received But Not Billed` (Inventory Settings), bukan HPP. Import Wizard tidak
  memeriksa ini, jadi akun salah masuk diam-diam dan HPP terhitung dua kali (pembelian + Shipment). `csv-barang` v1.0.2 mengikuti
  bawaan Frappe; data lama yang terlanjur salah diperingatkan oleh `laba-rugi`.
- Bagan akun Indonesia bawaan tidak punya akun persediaan yang bukan grup: buat mis. `Persediaan Toko` (tipe Stock) di bawah
  `Persediaan Barang - 1140.000`/`1141.000` lalu pasang di Inventory Settings > Stock In Hand sebelum menerima barang.
- Pembayaran sebagian perlu centang **Enable Partial Payment** di pengaturan.
- Shipment dari invoice yang berisi barang **dan** jasa gagal di v0.36.0 ("Cannot read properties of undefined (reading 'Stores')");
  hapus baris jasa di Shipment dulu (bug aplikasi, bukan skill).
- Retur membuat invoice retur bersisa negatif (kredit); invoice asli tidak berkurang otomatis. Pengiriman retur (barang kembali ke
  gudang) dibuat dari invoice retur dan dinilai dengan **harga jual**, bukan harga pokok.
- Purchase Receipt dari invoice pembelian ber-PPN dinilai **termasuk PPN** (Persediaan lebih besar dari nilai di Stock Balance;
  saldo Stock Received But Not Billed jadi minus sebesar PPN). HPP tidak terpengaruh.
- Barang **tanpa** Track Inventory tetap ikut Purchase Receipt/Shipment bila tidak dihapus (HPP bisa tercatat dua kali untuk barang
  itu). Hapus baris barang non-stok & jasa dari Receipt/Shipment sebelum disimpan.

## Tidak dikerjakan skill (arahkan manual)
- Retur (jumlah negatif) → buat dari invoice asli dengan tombol **Return** di Frappe Books.
- Pembayaran, jurnal umum, saldo awal, multi-mata uang → input manual di Frappe Books (atau Import Wizard dengan template bawaan aplikasi).
