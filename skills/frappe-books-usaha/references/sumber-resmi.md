# Sumber resmi & hasil riset skema (diakses 26 September 2026)

Skill ini ditulis Komunitech dari nol. Kode Frappe Books **dibaca** untuk memastikan nama tabel/kolom
dan format file; tidak ada kode Frappe Books yang disalin ke skill.

## Sumber
- Situs resmi: https://frappe.io/books (tombol unduh mengarah ke https://github.com/frappe/books/releases)
- Kode sumber: https://github.com/frappe/books (lisensi **AGPL-3.0**, file `LICENSE`)
- Versi yang dicocokkan:
  - **Tag `v0.36.0`**: commit `2f028f42be70a1dbd45bd4c6483d57df2fc64805` (tanggal commit 5 Nov 2025), rilis terbaru yang ada tag-nya.
  - **Cabang `main`**: commit `8f09465821dc81b5587aaf3b7aab10099b2f61b9` (20 Sep 2026, `package.json` 0.37.0, belum dirilis).
    Semua kolom yang dibaca skill ada di kedua versi. Perbedaan skema v0.36.0 → main hanya kolom yang tidak dipakai skill
    (`Item.batchSeries`, `Item.serialNumberSeries`, `Item.datafromErp`, `SalesInvoice.availableLoyaltyPoints`).
- **Catatan risiko proyek:** README cabang `main` (20 Sep 2026) memuat pengumuman bahwa Frappe Books
  *sedang terhambat merilis pembaruan karena sertifikat code-signing belum diperpanjang*. Pembeli memakai
  installer rilis yang ada; pantau https://github.com/frappe/books sebelum menjanjikan versi baru.

## File kode yang dibaca & temuan
| File (repo frappe/books) | Temuan yang dipakai skill |
|---|---|
| `schemas/app/*.json`, `schemas/app/inventory/*.json`, `schemas/meta/*.json`, `schemas/index.ts` | Nama tabel = nama skema (`SalesInvoice`, `PurchaseInvoice`, `SalesInvoiceItem`, `Party`, `Item`, `Account`, `AccountingLedgerEntry`, `StockLedgerEntry`, `TaxSummary`, `Tax`, `TaxDetail`, `UOM`, `Location`, `SingleValue`). Skema turunan (`SalesInvoice` extends `Invoice`) digabung dengan skema abstrak. Kolom meta `submitted`/`cancelled` (skema submittable), `parent`/`parentSchemaName`/`idx` (tabel anak). |
| `backend/helpers.ts` (`sqliteTypeMap`) | `Currency` disimpan sebagai **teks**, `Check` boolean (0/1), `Datetime` datetime, `Float` float. |
| `fyo/core/converter.ts` | Datetime disimpan lewat `toISOString()` → **ISO UTC** (`2026-08-31T17:00:00.000Z` = 1 Sep 00:00 WIB). Currency disimpan sebagai `pesa.store` (teks desimal). Import: tanggal dibaca `DateTime.fromISO` (pakai `YYYY-MM-DD`), Check dari angka (`1`/`0`). |
| `fyo/utils/consts.ts` | Presisi internal uang bawaan 11 desimal. |
| `backend/database/bespoke.ts` | Frappe Books sendiri menghitung piutang dari `outstandingAmount` invoice `submitted=1, cancelled=0`; laba rugi dari `AccountingLedgerEntry` `reverted=false` digabung `Account.rootType`; stok = `SUM(quantity)` di `StockLedgerEntry` per `item` (opsional per `location`). |
| `models/baseModels/AccountingLedgerEntry/AccountingLedgerEntry.ts` | Saat dokumen dibatalkan, entri asli **dan** entri pembaliknya diberi `reverted=true` → cukup saring `reverted = 0`. |
| `schemas/app/Invoice.json` | **Tidak ada kolom tanggal jatuh tempo.** Skill menghitung jatuh tempo = tanggal invoice + `--tempo` hari (bawaan 30). |
| `src/importer.ts` | Template Import Wizard = 3 baris judul: label skema, label kolom, **kunci kolom** (`Party.name`, `SalesInvoiceItem.item`, ...). Importer mencari baris kunci di 4 baris pertama, lalu data. Baris dengan nilai `SalesInvoice.name` yang sama digabung jadi satu invoice (baris anak = barang). Kolom Link (pelanggan, barang, akun, pajak, satuan) harus **sudah ada**. |
| `src/pages/ImportWizard.vue` | Jenis yang bisa diimpor: Sales Invoice, Purchase Invoice, Payment, Party, Item, Journal Entry, Tax, Account, Address, Number Series (+ Stock Movement, Shipment, Purchase Receipt, Location bila Inventory aktif). Setelah simpan, wizard bertanya apakah dokumen di-*submit*. |
| `fyo/model/naming.ts` | Invoice memakai Number Series: nilai kolom "Invoice No" di CSV hanya pengelompok; nomor final diberikan otomatis. Party/Item: nama manual (= kolom `name`). |
| `utils/csvParser.ts` | CSV dipisah koma, baris CRLF. Pembacaan tanda kutip ganda di dalam nilai tidak andal → skill mengganti `"` dengan `'`. |
| `models/baseModels/Invoice/Invoice.ts` (`getTaxItems`) | Pajak = jumlah baris × tarif/100, per baris, **tanpa pembulatan** (presisi internal). |
| `models/baseModels/Item/Item.ts` | Akun penjualan otomatis hanya bila akun bernama `Sales`/`Service` ada → pada bagan akun Indonesia sering kosong; skill mengisi akun dari database. |
| `src/setup/createCOA.ts` (`getAccountName`) | Nama akun = `<nama> - <nomor akun>` bila bagan punya nomor → bagan Indonesia: `Penjualan - 4110.000`, `Piutang Dagang - 1131.0010`, `Hutang Dagang Dalam Negeri - 2111.001`, `HPP Pembelian - 4210.000`, `Hutang Pajak - 2141.000`. |
| `models/Transactional/LedgerPosting.ts` (`timezoneDateTimeAdjuster`) | Tanggal entri buku besar = tengah malam UTC dari tanggal lokal dokumen. |
| `models/baseModels/SalesInvoice/SalesInvoice.ts` & `PurchaseInvoice.ts` (`getPosting`) | Retur: sisi debit/kredit ditukar **dan** jumlahnya negatif → di buku besar retur menambah pendapatan/beban. Skill mengoreksi di `laba-rugi` dan menampilkan angka buku besar apa adanya. |
| `fixtures/verified/id.json` | Bagan akun Indonesia bawaan (sebelum diberi nomor): `Piutang Dagang` (Receivable), `Hutang Dagang Dalam Negeri` (Payable), `Penjualan`, `HPP Pembelian` (Cost of Goods Sold, di bawah akar pendapatan), `Hutang Pajak`. |
| `utils/defaults.ts`, `translations/id.csv` | Satuan bawaan Unit, Kg, Gram, Meter, Hour, Day; lokasi Stores (nama diterjemahkan saat dibuat; file asli uji berbahasa Inggris: `Hour`, `Day`, `Stores`; bila UI Indonesia bisa `Jam`, `Hari`, `Toko`). |
| `main/registerIpcMainActionListeners.ts` | Lokasi file bawaan: `<Documents>/Frappe Books/<nama usaha>.books.db`. |

## Temuan dari file ASLI (uji independen v1.0.0, 26 Sep 2026, Frappe Books v0.36.0 AppImage resmi)
- Centang di `SingleValue` disimpan `'1.0'`/`'0.0'` (bukan `1`/`true`).
- Tabel `Party` berkolom `gstin`/`gstType`, tanpa `taxId`.
- Import Wizard mewajibkan kolom Number Series untuk invoice.
- Semua kolom di `SKEMA_WAJIB` ada; laporan baca v1.0.0 cocok dengan hitungan independen.

## Yang BELUM diverifikasi
- Perbaikan impor v1.0.1 (Number Series, akun bernomor, NPWP) belum dijalankan ulang di Import Wizard asli.
- Fixture uji (`tests/data/buat_db_contoh.py`) meniru temuan file asli di atas, tetapi tetap database tiruan.
