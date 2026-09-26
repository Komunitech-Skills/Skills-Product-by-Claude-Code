# CSV untuk Import Wizard Frappe Books (v0.36.0)

Script membuat CSV dengan **3 baris judul** persis seperti tombol "Template" di Import Wizard:
baris 1 = nama jenis data, baris 2 = label kolom, baris 3 = kunci kolom (yang dibaca Frappe Books), lalu data.
Pemisah koma, akhir baris CRLF, UTF-8. Angka tanpa pemisah ribuan (`85000`), tanggal `YYYY-MM-DD`, centang `1`/`0`.

## Kolom yang diisi skill
| Perintah | Jenis di Import Wizard | Kunci kolom |
|---|---|---|
| `csv-pelanggan` | Party | `Party.name`, `Party.role` (Customer/Supplier/Both), `Party.email`, `Party.phone`, `Party.taxId` |
| `csv-barang` | Item | `Item.name`, `Item.itemCode`, `Item.for` (Both), `Item.itemType` (Product/Service), `Item.unit`, `Item.rate`, `Item.description`, `Item.incomeAccount`, `Item.expenseAccount`, `Item.barcode`, `Item.trackItem` |
| `csv-transaksi --jenis penjualan` | Sales Invoice | `SalesInvoice.name` (pengelompok), `.party`, `.account` (akun piutang), `.date`, `.terms`, `SalesInvoiceItem.item`, `.rate`, `.quantity`, `.account`, `.tax` |
| `csv-transaksi --jenis pembelian` | Purchase Invoice | sama, dengan `PurchaseInvoice.*` / `PurchaseInvoiceItem.*` (akun utang) |

Kolom wajib Frappe Books (`required` di skema): Party `name`, `role`; Item `name`, `for`, `incomeAccount`, `expenseAccount`;
Invoice `name`, `party`, `account`, `date`, `numberSeries` (punya nilai bawaan SINV-/PINV-), baris `item`, `rate`, `quantity`, `account`.

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

## Tidak dikerjakan skill (arahkan manual)
- Retur (jumlah negatif) → buat dari invoice asli dengan tombol **Return** di Frappe Books.
- Pembayaran, jurnal umum, saldo awal, multi-mata uang → input manual di Frappe Books (atau Import Wizard dengan template bawaan aplikasi).
