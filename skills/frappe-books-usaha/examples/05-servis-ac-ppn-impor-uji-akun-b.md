# Skenario 5 (normal 3) — Jasa servis AC dengan PPN + impor CSV lewat Import Wizard ASLI — uji Akun B

Data: "Servis AC Dingin (fiktif)", file asli Frappe Books v0.36.0. Template pajak `PPN 11% (12% x 11/12)` (akun
`Hutang Pajak - 2141.000`, tarif 11) dan satu template salah `PPN 12% (salah)` (tarif 12).

## A. Laporan & PPN
| Invoice | DPP | PPN di Frappe (TaxSummary) | PPN standar Komunitech (floor sekali) | Independen |
|---|---|---|---|---|
| SINV-1001 | 12×85.000 + 3×350.000 = 2.070.000 | 227.700,00 | 227.700 | 2.070.000 × 11/12 × 12% = 227.700 |
| SINV-1002 | 123.457 + 3×85.000 = 378.457 | 41.630,27 | 41.630 | 41.630,27 → 41.630 |
| SINV-1003 (30 Sep 22:00 WIB) | 250.000 + 332.345 = 582.345 | 64.057,95 | 64.057 | 64.057,95 → 64.057 |
| SINV-1004 (template 12%) | 85.000 | 10.200 | — | 12% dari harga penuh (terlalu besar) |

- `penjualan --bulan 2026-09`: DPP Rp 3.115.802, Pajak Rp 343.588 (= 343.588,22 dibulatkan tampilan), Total Rp 3.459.390,
  belum dibayar Rp 3.039.303. Independen: 3.115.802 / 343.588,22 / 3.459.390,22 / 3.039.302,95. **Cocok.**
- `pembelian`: DPP 800.000, pajak 88.000, total 888.000. Cocok. `laba-rugi`: pendapatan 3.115.802 (PPN tidak masuk laba), HPP 800.000. Cocok.
- `akun`: template 12% diberi PERHATIAN. Bagus.
- `ppn --dpp 378457` → 41.630; `--dpp 582345` → 64.057; `--harga-termasuk 646402` → DPP 582.345 + 64.057, sisa 0
  (cek: DPP 582.346 → 582.346 + 64.058 = 646.404 > harga, jadi 582.345 memang terbesar); `--harga-termasuk 1665000` → 1.500.000 + 165.000.
  `--dpp 85,000` ditolak (ambigu), `--dpp -5` ditolak. Semua benar. Disclaimer + "belum dicocokkan dengan Coretax" tampil.

## B. Impor CSV (input cp1252, pemisah `;`, angka gaya Indonesia) → Import Wizard asli
Uji impor memakai kelas `Importer` milik aplikasi yang sedang berjalan (jalur yang sama dengan tombol Select File →
Import Data; watcher kolom di `ImportWizard.vue` ikut ditiru), dokumen disimpan sebagai **draf**.

**Template resmi v0.36.0 (diambil dari `importer.getCSVTemplate()` di aplikasi):**
- Party: `Party.name, role, email, phone, address, defaultAccount, currency, loyaltyProgram, gstType, gstin` — **tidak ada `Party.taxId`**
  pada perusahaan Indonesia yang dibuat di uji ini (skema regional India ikut terpasang; tabel `Party` di file juga berkolom `gstin`, bukan `taxId`).
- Item: `Item.name, itemCode, itemGroup, for, itemType, unit, rate, description, incomeAccount, expenseAccount, tax, hsnCode, barcode, trackItem, ...`
- SalesInvoice: `SalesInvoice.name, **numberSeries**, party, account, date, ..., terms, ...; SalesInvoiceItem.item, rate, quantity, account, tax, ...`

| Langkah | Keluaran skill | Import Wizard asli |
|---|---|---|
| `csv-pelanggan` (Café Dingin Jaya, Hotel Mawar; `é` dari cp1252; PT Kantor Sejuk sudah ada → dilewati; email salah dikosongkan) | LOLOS, 2 pihak, telepon → `+62...` | **Berhasil** 2 Party. Kolom `Party.taxId` (NPWP) **diabaikan diam-diam** (kunci tidak dikenal) |
| `csv-barang` (Rp 150.000, 85.000,50, 1,5jt, `¼`) | LOLOS; "Akun penjualan: **Pendapatan Bunga Bank - 4410.000**" | **Berhasil** 3 Item — dengan akun penjualan **salah** (bunga bank) |
| `csv-transaksi` (2 nota, 4 baris, pajak PPN 11%) | LOLOS; pratinjau N-01 DPP 320.000 PPN 35.200 total 355.200; N-02 DPP 648.457 PPN 71.330 total 719.787 | **DITOLAK**: "Required fields not selected: Number Series" |
| CSV transaksi yang sama + kolom `SalesInvoice.numberSeries = SINV-` (ditambah penguji di scratchpad, bukan di skill) | — | Berhasil 2 draf: SINV-1005 total 355.200 (PPN 35.200), SINV-1006 total 719.787,27 (PPN 71.330,27) — cocok dengan pratinjau skill |

Verifikasi pratinjau (independen): N-01 = 2×85.000 + 150.000 = 320.000 → PPN 35.200; N-02 = 123.457 + 1,5×350.000 = 648.457 → 71.330,27 → 71.330. Cocok.

## Temuan dari skenario ini
1. **TINGGI — CSV transaksi tidak bisa diimpor.** Import Wizard v0.36.0 mewajibkan kolom `SalesInvoice.numberSeries`
   (`requiredNotSelected`), skill tidak menulisnya. `references/import-wizard.md` menyebut "numberSeries punya nilai bawaan" — di
   Import Wizard asli tetap ditolak. Perbaikan teruji: tambah kolom `<Skema>.numberSeries` berisi `SINV-`/`PINV-`.
2. **TINGGI — Akun otomatis salah pada bagan akun Indonesia asli.** `createCOA.ts` memberi nama akun `<nama> - <nomor>`
   (mis. `Penjualan - 4110.000`, `Pendapatan Service - 4310.000`, `Piutang Dagang - 1131.0010`). `pilih_akun` mencari nama persis
   `Penjualan`/`Pendapatan Service` → gagal → jatuh ke akun pendapatan pertama menurut abjad = **Pendapatan Bunga Bank**. Barang & jasa
   hasil impor memposting penjualan ke akun bunga bank. Untuk `--jenis pembelian`, akun utang otomatis akan jatuh ke
   `HUtang Dagang Biaya Kirim Luar Negeri - 2111.004` (urutan abjad huruf besar), bukan `Hutang Dagang Dalam Negeri - 2111.001`.
   Akun piutang kebetulan benar karena urutan abjad. Fixture pembuat memakai nama tanpa nomor, sehingga tidak tertangkap.
3. (rendah-sedang) NPWP (`Party.taxId`) hilang tanpa peringatan di instalasi uji; skill melaporkan LOLOS tanpa menyebut ini.
4. (rendah) Satuan bawaan file asli berbahasa Inggris (`Day, Gram, Hour, Kg, Meter, Unit`), lokasi `Stores` — bukan `Jam/Hari/Toko`
   seperti di `references/sumber-resmi.md` & peringatan tanpa `--db`. Dengan `--db` script tetap memakai nama yang ada, jadi aman.
