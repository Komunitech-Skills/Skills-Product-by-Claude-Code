# 08 — Uji ulang independen v1.0.1 dengan Frappe Books v0.36.0 ASLI (penguji Akun B, 26 Sep 2026)

Penguji independen (bukan pembuat). Semua nama usaha/pelanggan **fiktif**. Semua berkas uji ada di scratchpad penguji
(`rt-frappe2/`), tidak ada yang masuk repo. Script skill tidak diubah.

## 1. Lingkungan
| Hal | Nilai |
|---|---|
| Aplikasi | `Frappe-Books-v0.36.0-linux-x86_64.AppImage`, diunduh ulang dari GitHub releases `frappe/books` (tag v0.36.0) |
| Checksum | SHA-512 (base64) `nFHZaPXph+L63yBvX4gQontVek2AZMDijuvPDFjQoOGQTJ4aTDxNxGNcCn/M4FcI33i01jdbhZpn8vkkqfBXmg==`, **cocok** dengan `latest-linux.yml` rilis yang sama; ukuran 103.984.584 byte |
| Jalan | AppImage diekstrak, dijalankan headless di Xvfb, `TZ=Asia/Jakarta`, `NODE_ENV` dikosongkan (mode produksi `app://`), proxy keluar diblokir, HOME terpisah |
| Kendali | Chrome DevTools Protocol lokal: renderer (port 9322) + proses utama Electron (`--inspect`, port 9339) |
| Kode sumber | tag v0.36.0 commit `2f028f42` (untuk membaca `ImportWizard.vue`, `Item.ts`) |
| Skill | `scripts/frappe_books.py` 1.0.1, dijalankan dengan `--db` ke file asli **saat aplikasi sedang terbuka** |

## 2. Database asli dibuat sendiri
Lewat **Setup Wizard** aplikasi: perusahaan baru "Toko Uji Ulang v101 (fiktif)", negara Indonesia → otomatis IDR +
"Indonesia - Chart of Accounts" (216 akun, nama bernomor). Lalu lewat mesin aplikasi: centang Inventory (tersimpan
`enableInventory = '1.0'`), akun `Persediaan Toko - 1141.001` sebagai Stock In Hand, template pajak `PPN 11% (12% x 11/12)`.
File: `home/Frappe Books/Toko Uji Ulang v101 (fiktif).books.db`.

## 3. Jalur impor: Import Wizard ASLI, lewat tombol GUI
Per jenis data, harness penguji melakukan persis urutan pengguna di layar Import Wizard:
1. Router aplikasi ke `/import-wizard`; pilih jenis lewat handler `setImportType` (sama dengan `@change` AutoComplete "Import Type").
2. **Klik tombol "Select File"** → IPC `SELECT_FILE` → proses utama → `dialog.showOpenDialog` (satu-satunya bagian yang
   diganti: dialog OS dikembalikan ke path CSV hasil script, karena Xvfb tidak punya pemilih file yang bisa diketik) →
   `fs.readFile` asli → `importer.selectFile(text)` asli.
3. Baca status layar: `errorMessage`, `requiredNotSelected`, `checkCellErrors()`, `checkLinks()`.
4. **Klik tombol "Import Data"** → `preImportValidations` → dialog **"Submit entries?" → klik "No"** (sesuai saran skill: masuk draf)
   → `doc.sync()` per dokumen oleh `importData()` asli → daftar `success`/`failed` komponen.

### Input pengguna (bahasa sehari-hari, pemisah `;`)
```text
pelanggan.csv : Nama Pelanggan;No HP;Email;NPWP;Peran  (5 baris: 4 pelanggan + 1 pemasok; 3 berisi NPWP; "CV Berkah, Solo"; "Café Dingin Jaya")
barang.csv    : nama barang;sku;satuan;harga jual;jenis;stok  (Rp 85.000 / 32.500 / 150rb / 1,5jt; 3 barang stok=ya, 1 jasa Hour)
nota-jual.csv : 4 nota, 6 baris; tanggal 01/09/2026, "15 Sep 2026", 30/09/2026, 01/10/2026; nama huruf kecil "kedai kopi senja";
                keterangan berkoma "lantai 2, meja 5"; PPN pada N-01 & N-03
nota-beli.csv : 2 nota pemasok, 3 baris, PPN pada B-01
```

### Hasil
| CSV dari script | Kode script | Import Wizard asli | Dokumen |
|---|---|---|---|
| `csv-pelanggan` (Party) | 0, LOLOS 5 | errorMessage kosong, requiredNotSelected `[]`, cellErrors `[]`, absentLinks `[]` | **5/5 sukses**, 0 gagal |
| `csv-barang` (Item) | 0, LOLOS 4 | idem | **4/4 sukses** |
| `csv-transaksi` penjualan | 0, LOLOS 4 nota | idem; dialog "Submit entries?" → No | **SINV-1001..1004 sukses**, 0 gagal |
| `csv-transaksi --jenis pembelian` | 0, LOLOS 2 nota | idem | **PINV-1001..1002 sukses** |

Isi database setelah impor (dibaca langsung, read-only):
```text
SINV-1001 Toko Sinar Abadi  Piutang Dagang - 1131.0010  2026-08-31T17:00Z  net 332345  grand 368902.95  draf
SINV-1002 Kedai Kopi Senja  ...                          2026-09-14T17:00Z  net 300000  terms "lantai 2, meja 5"
SINV-1003 Café Dingin Jaya  ...                          2026-09-29T17:00Z  net 340000  grand 377400
SINV-1004 CV Berkah, Solo   ...                          2026-09-30T17:00Z  net 325000
PINV-1001 PT Pemasok Biji Nusantara  Hutang Dagang Dalam Negeri - 2111.001  net 1900000 grand 2109000
Baris: Kopi/Gula -> Penjualan - 4110.000 ; Jasa Seduh Event -> Pendapatan Service - 4310.000
Party: telepon +6281234567890 dst.; kolom Party = ... gstType, gstin (TIDAK ada taxId)
Item : trackItem 1 untuk 3 barang, 0 untuk jasa; unit Unit/Kg/Hour
```
Tanggal CSV `2026-09-01` tersimpan `2026-08-31T17:00:00Z` = 1 Sep 00:00 WIB — cocok dengan pratinjau skill. Total draf =
pratinjau skill (N-01: Frappe 368.902,95 vs pratinjau standar Komunitech Rp 368.902 — selisih pecahan sudah diperingatkan script).

## 4. Transaksi lanjutan di aplikasi (lewat mesin aplikasi)
Semua draf di-Submit; stok masuk (StockMovement 2 Sep: Arabika 20, Robusta 10, Gula 30); pengiriman (Shipment) untuk SINV-1001..1003;
pembayaran sebagian SINV-1001 Rp 200.000 (10 Sep 23:30 WIB; perlu centang Enable Partial Payment); pembayaran penuh PINV-1002;
**retur** SINV-1005 atas SINV-1003 (1 unit, 30 Sep **23:50 WIB** → UTC 30 Sep 16:50); invoice SINV-1006 tanggal **1 Okt 00:30 WIB**
(tersimpan `2026-09-30T17:30Z`, tanggal UTC masih September); jurnal beban sewa Rp 150.000 (25 Sep).

Catatan aplikasi (bukan kesalahan skill): tombol Shipment dari invoice yang berisi barang **dan jasa** gagal di v0.36.0
("Cannot read properties of undefined (reading 'Stores')") karena baris jasa ikut; berhasil setelah baris jasa dihapus.

## 5. Laporan baca (regresi) — file asli, aplikasi terbuka, SHA-256 file sama sebelum/sesudah
```text
$ penjualan --bulan 2026-09   -> final 4 (termasuk 1 retur); DPP Rp 887.345; Pajak Rp 64.608; TOTAL Rp 951.953;
                                 Terbayar (bersih) Rp 105.650 | Belum dibayar Rp 846.303
$ penjualan --bulan 2026-10   -> final 2 (SINV-1004, SINV-1006); TOTAL Rp 357.500   <- SINV-1006 (UTC 30 Sep) benar masuk Oktober WIB
$ pembelian --bulan 2026-09   -> DPP Rp 2.500.000; Pajak Rp 209.000; TOTAL Rp 2.709.000; terbayar Rp 600.000
$ piutang --tempo 14          -> 5 invoice Rp 1.203.803; SINV-1001 sisa Rp 168.903 telat 11 hari
$ utang --tempo 30            -> PINV-1001 Rp 2.109.000, jatuh tempo 2 Okt 2026
$ stok --min 5 --semua        -> Gula 28 Kg, Arabika 13 Unit, Robusta 8 Kg
$ laba-rugi --bulan 2026-09   -> pendapatan Rp 887.345 (dikoreksi retur), HPP Rp 3.070.000, beban Rp 150.000, RUGI -Rp 2.332.655
                                 + "Catatan retur": buku besar apa adanya pendapatan Rp 1.057.345, rugi -Rp 2.162.655
$ laporan-harian --tanggal 2026-10-01 -> 2 invoice Rp 357.500, dibanding kemarin Rp 283.050 (+26,3%), tanpa nama pelanggan
$ cek                         -> Versi 0.36.0 | IDR | Inventory: aktif | struktur cocok
```
Saat semua invoice masih draf: `penjualan` = 0 final, "draf belum final: 3" (SINV-1004 = Oktober WIB, benar tidak dihitung).

## 6. Verifikasi angka independen (kode Decimal penguji sendiri, tidak mengimpor script)
| Besaran | Penguji | Skill |
|---|---|---|
| Sep: invoice | SINV-1001/1002/1003/1005 | 4 (1 retur) ✓ |
| Sep: DPP / total | 887.345 / 951.952,95 | Rp 887.345 / Rp 951.953 ✓ |
| Okt: invoice / total | SINV-1004/1006, 357.500 | ✓ |
| Buku besar Sep apa adanya | pendapatan 1.057.345; HPP 3.070.000; beban 150.000; laba −2.162.655 | sama dengan "Catatan retur" ✓ |
| Pendapatan dikoreksi retur | 1.057.345 − 2×85.000 = 887.345 | = `penjualan` DPP ✓ (konsisten) |
| PPN DPP 332.345 | 332.345×11/12×12% = 36.557,95 → **36.557** | Rp 36.557 ✓ |
| PPN harga termasuk 1.665.000 | DPP 1.500.000, PPN 165.000, sisa 0 | ✓ |
| Umur SINV-1001 (tempo 14, per 26 Sep) | jatuh tempo 15 Sep → telat 11 | ✓ |
| Stok | 20−3−4=13; 10−2=8; 30−2=28 | ✓ |
| Piutang bersih termasuk kredit retur (outstanding SINV-1005 = −94.350) | **1.109.452,95** | 1.203.803 (retur tidak disebut) ✗ lihat temuan B |

## 7. Keamanan & data rusak
| Uji | Hasil |
|---|---|
| `--keluar salinan.books.db` / path `.books.db` asli / `keluar.db` / `keluar.txt` | ditolak kode 2 "harus berakhiran .csv (file ini TIDAK ditulis)" |
| `--keluar salinan-sqlite.csv` (SQLite dinamai .csv) | ditolak kode 2 "adalah file database" |
| `--keluar tautan.csv` (symlink ke .books.db) | ditolak kode 2 "adalah file database" |
| SHA-256 semua salinan + file asli | tidak berubah |
| CSV dengan byte 0x81 | kode 5 "Huruf ... tidak bisa dibaca" + saran simpan ulang CSV UTF-8 (dulu UnboundLocalError) |
| Tanpa `--db`, HOME tanpa Documents | ketemu otomatis di `~/Frappe Books/` |
| Pelanggan diimpor ulang | "tidak ada baris baru" (tidak ganda) |
| Nota dengan pelanggan/barang belum ada | kode 5 per baris, CSV tidak dibuat |
| NPWP (3 baris) | 3 peringatan "NPWP ... TIDAK ikut diimpor ... catat manual"; kolom Tax ID tidak ditulis |

## 8. Temuan baru
**A. TINGGI (akuntansi, pemakai stok) — akun pembelian barang yang dilacak stoknya salah.** `csv-barang` memberi
`Item.expenseAccount = HPP Pembelian - 4210.000` untuk **semua** barang, termasuk `stok: ya` (`trackItem=1`). Frappe Books v0.36.0
sendiri memakai **`Stock Received But Not Billed`** (di file uji: `Stock Diterima Tapi Tidak Ditagih - 2115.000`) untuk barang dilacak
(`models/baseModels/Item/Item.ts` formula `expenseAccount`; filter akun di layar pun meminta akun Kewajiban bila Track Inventory).
Terbukti di aplikasi asli: invoice pembelian men-debit HPP Rp 2.500.000 **dan** Shipment men-debit HPP Rp 570.000 (nilai persediaan
keluar) → `laba-rugi` September menampilkan HPP Rp 3.070.000 dan **rugi −Rp 2.332.655**, padahal dengan akun bawaan Frappe HPP = Rp 570.000
dan **laba Rp 167.345**. Import Wizard tidak memvalidasi filter ini, jadi kesalahan masuk diam-diam. Perbaikan: untuk barang `trackItem=1`
pakai `InventorySettings.stockReceivedButNotBilled` (baca dari SingleValue), jasa/barang tanpa stok tetap HPP; tambahkan tes regresi.
`csv-transaksi` sudah mengambil akun dari data barang, jadi ikut benar setelah perbaikan ini.

**B. SEDANG — `piutang` mengabaikan kredit retur.** Retur SINV-1005 punya `outstandingAmount = −94.350`, sedangkan SINV-1003 tetap
377.400 (perilaku Frappe). `piutang` menampilkan Café Dingin Jaya berutang Rp 377.400 dan total Rp 1.203.803 tanpa catatan; saldo bersih
Rp 1.109.453. Tambahkan baris "Kredit retur belum dikembalikan: ..." per pelanggan atau netto per pelanggan.

**C. RENDAH —** `piutang` "per 26 Sep 2026" ikut mendaftar invoice bertanggal masa depan (30 Sep, 1 Okt) sebagai "belum jatuh tempo"
tanpa tanda. Pertimbangkan catatan "tanggal invoice setelah hari ini".

**D. RENDAH/dokumentasi —** SKILL.md masih menulis "Impor v1.0.1 belum diuji ulang di Import Wizard asli"; kini sudah (lihat file ini).
Tambahkan juga di `references/import-wizard.md`: pembayaran sebagian butuh centang "Enable Partial Payment", dan Shipment dari nota
campuran barang+jasa gagal di v0.36.0 (hapus baris jasa dulu).

## 9. Status temuan uji v1.0.0
| # | Temuan lama | Status v1.0.1 |
|---|---|---|
| 1 | CSV invoice ditolak (Number Series) | **Beres** — 4 jenis CSV diterima Import Wizard asli lewat tombol GUI, 0 gagal |
| 2 | Akun bernomor salah | **Beres** untuk penjualan/jasa/piutang/utang; **baru**: akun pembelian barang dilacak (temuan A) |
| 3 | `--keluar` menimpa DB | **Beres** (5 variasi + symlink ditolak) |
| 4 | Inventory `'1.0'` | **Beres** ("aktif", tanpa peringatan palsu) |
| 5 | Retur vs laba-rugi | **Beres** — dikoreksi & konsisten dengan `penjualan`, angka buku besar apa adanya dicetak dan cocok |
| 6 | NPWP hilang diam-diam | **Beres** — peringatan per NPWP |
| 7 | Byte tak valid → galat | **Beres** (kode 5) |
| 8 | `~/Frappe Books` | **Beres** |
| 9 | `Stores`/`Hour` | Beres di dokumen (`--lokasi Stores`); satuan `Hour` diterima |
| 10 | `--samarkan` nama berkurung | Tidak diuji ulang (tidak ada nama berkurung di data) |
| 11 | Label "Terbayar (bersih)" | **Beres** (label + catatan) |

Tes bawaan: `python3 tests/uji_regresi.py` → 39 tes OK. `python3 scripts/validate.py --skill frappe-books-usaha` → valid.
`uji_openclaw.sh` tidak dijalankan (sesuai instruksi).
