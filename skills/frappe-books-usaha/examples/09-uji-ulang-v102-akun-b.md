# 09 — Uji ulang independen v1.0.2 dengan Frappe Books v0.36.0 ASLI (penguji Akun B, 26 Sep 2026)

Penguji independen ketiga (bukan pembuat, bukan penguji 03–08). Semua nama usaha/pelanggan **fiktif**. Berkas kerja di scratchpad
penguji (`rt-frappe3/`), tidak ada yang masuk repo. Script, SKILL.md, README, dan katalog **tidak diubah**.

## 1. Lingkungan
| Hal | Nilai |
|---|---|
| Aplikasi | `Frappe-Books-v0.36.0-linux-x86_64.AppImage`, **diunduh sendiri** dari GitHub releases `frappe/books` tag v0.36.0 |
| Checksum | SHA-512 (base64) `nFHZaPXph+L63yBvX4gQontVek2AZMDijuvPDFjQoOGQTJ4aTDxNxGNcCn/M4FcI33i01jdbhZpn8vkkqfBXmg==`, **cocok** dengan `latest-linux.yml` rilis yang sama (diunduh sendiri); ukuran 103.984.584 byte cocok; SHA-256 `c079d60b…fee79602` |
| Jalan | AppImage diekstrak, headless Xvfb, `TZ=Asia/Jakarta`, mode produksi (`app://`), proxy keluar diblokir, HOME terpisah |
| Kendali | Chrome DevTools Protocol lokal (renderer 9342, proses utama 9359). Hanya `dialog.showOpenDialog` di proses utama yang diarahkan ke path CSV |
| Kode sumber | dibaca dari source map di dalam `app.asar` rilis ini (`reports/LedgerReport.ts`, `reports/AccountReport.ts`, `models/inventory/StockTransfer.ts`) |
| Skill | `scripts/frappe_books.py` **1.0.2** (`--versi`), dijalankan dengan `--db` ke file asli saat aplikasi terbuka |

## 2. Database baru milik penguji
Setup Wizard aplikasi → "Grosir Uji v102 Akun B (fiktif)", Indonesia → IDR + "Indonesia - Chart of Accounts" (215 akun bernomor).
Inventory dicentang. Sebelum Stock In Hand diisi, `csv-barang` memberi peringatan "Inventory Settings 'Stock In Hand' belum diisi" ✓.
Lalu lewat mesin aplikasi: akun `Persediaan Gudang - 1141.001` (tipe Stock) → Stock In Hand; template pajak `PPN 11% (12% x 11/12)`.
Bawaan bagan Indonesia: `stockReceivedButNotBilled = Stock Diterima Tapi Tidak Ditagih - 2115.000`, `costOfGoodsSold = HPP Pembelian - 4210.000`.

## 3. Impor lewat Import Wizard ASLI (tombol "Select File" → "Import Data" → "Submit entries?" → **No**)
Input pengguna (pemisah `;`, bahasa sehari-hari):
```text
pelanggan.csv : 3 pelanggan + 2 pemasok; 2 NPWP; "Toko Makmur, Bekasi"; HP 0812-…, +62 813 …, 0215550001
barang.csv    : Beras Premium 5kg (stok ya, Rp 72.000) | Minyak Goreng 2L (stok ya, 38,5rb) | Telur Ayam 1 Tray (stok ya, 55000)
                Kantong Plastik Besar (barang, stok TIDAK, 7.500) | Jasa Antar Lokal (jasa, 25rb)
nota-beli.csv : B-01 PT Beras Nusantara Jaya (beras 20×60.000, minyak 30×32.000, PPN) | B-02 CV Telur Segar (telur 15×45.000, kantong 10×5.000)
nota-jual.csv : J-01 5 Sep "warung bu tini" (beras 5, minyak 6, PPN) | J-02 2026-09-10 Toko Makmur (telur 4 + jasa antar, ket. "antar sore, gerbang biru")
                J-03 "15 Sep 2026" Kios Pak Darto (beras 3, kantong 4) | J-04 01/10/2026 Kios Pak Darto (minyak 2)
```
| CSV dari script | Kode | Import Wizard asli | Hasil |
|---|---|---|---|
| `csv-pelanggan` | 0, LOLOS 5 + 2 peringatan NPWP | errorMessage kosong, requiredNotSelected `[]`, cellErrors `[]`, absentLinks `[]` | **5/5 sukses** |
| `csv-barang` | 0, LOLOS 5 | idem | **5/5 sukses**; barang stok ya → `expenseAccount = Stock Diterima Tapi Tidak Ditagih - 2115.000`, `trackItem=1`; kantong & jasa → `HPP Pembelian - 4210.000`, `trackItem=0`; jasa → `Pendapatan Service - 4310.000` |
| `csv-transaksi --jenis pembelian` | pertama kode 5: `pajak 'PPN' belum ada (yang ada: PPN 11% (12% x 11/12))` — benar, tidak menebak. Setelah nama lengkap: 0, LOLOS 2 nota | idem | **PINV-1001..1002 sukses**, 0 gagal |
| `csv-transaksi` penjualan | 0, LOLOS 4 nota; pratinjau J-01 DPP 591.000 PPN 65.010 total 656.010 | idem | **SINV-1001..1004 sukses**, 0 gagal; total draf = pratinjau |

Saat semua masih draf: `penjualan` Sep "final 0, draf 3" (J-04 = Oktober, benar tidak dihitung); `pembelian` "draf 2" ✓.

## 4. Siklus lanjutan di aplikasi
Submit semua → **Purchase Receipt** dari PINV-1001 (PREC-1001) dan PINV-1002 (PREC-1002) → **Shipment** SINV-1001 (SHPM-1001),
SINV-1003 (SHPM-1002), SINV-1004 1 Okt (SHPM-1003), SINV-1002 (SHPM-1004, baris jasa dihapus dulu — dengan jasa gagal
"reading 'Stores'", perilaku v0.36.0 yang sudah dicatat) → bayar sebagian SINV-1001 Rp 300.000 (perlu Enable Partial Payment;
tanpa itu ditolak "Enable Partial payment…") → bayar penuh SINV-1002 → bayar PINV-1002 (PAY-1002 salah akun oleh harness penguji,
**dibatalkan**, diganti PAY-1004 — sekaligus menguji entri `reverted`) → **retur** SINV-1005 atas SINV-1003 (1 beras, 30 Sep 23:50 WIB)
+ **pengiriman retur** SHPM-1005 (barang kembali ke gudang, dibuat oleh tombol retur aplikasi) → jurnal beban sewa gudang Rp 100.000
(25 Sep) → invoice SINV-1006 jasa 2×25.000 tanggal **1 Okt 00:30 WIB** (tersimpan `2026-09-30T17:30Z`).

Buku besar asli (baris kunci, dibaca read-only):
```text
PINV-1001 Stock Diterima Tapi Tidak Ditagih D 2.160.000 | Hutang Pajak D 237.600 | Hutang Dagang K 2.397.600
PINV-1002 Stock Diterima…  D 675.000 | HPP Pembelian D 50.000 (kantong, non-stok) | Hutang Dagang K 725.000
PREC-1001 Persediaan D 2.397.600 | Stock Diterima… K 2.397.600      <- Frappe menilai Receipt TERMASUK PPN (lihat §8 catatan aplikasi)
SHPM-1001 HPP D 492.000 (5×60.000 + 6×32.000) | SHPM-1002 HPP D 200.000 (3×60.000 + kantong 4×5.000) | SHPM-1004 HPP D 180.000
SHPM-1003 (1 Okt) HPP D 64.000
SINV-1005 (retur)  Piutang  debit 0 / credit -72.000 | Penjualan debit -72.000 / credit 0
SHPM-1005 (retur)  Persediaan debit -72.000 / credit 0 | HPP debit 0 / credit -72.000   <- nilai jual, bukan harga pokok 60.000
```
HPP barang berstok **hanya tercatat sekali** (saat Shipment); pembelian barang berstok tidak menyentuh HPP ✓ (temuan A v1.0.1 beres).

## 5. Laporan skill (file asli, aplikasi terbuka; SHA-256 file sama sebelum/sesudah semua perintah baca)
```text
$ penjualan --bulan 2026-09   -> final 4 (termasuk 1 retur); DPP Rp 1.010.000; Pajak Rp 65.010; TOTAL Rp 1.075.010;
                                 Terbayar (bersih) Rp 473.000 | Belum dibayar Rp 602.010
   --per barang               -> Beras 7 Rp 504.000; Minyak 6 Rp 231.000; Telur 4 Rp 220.000; Kantong 4 Rp 30.000; Jasa 1 Rp 25.000
$ penjualan --bulan 2026-10   -> final 2 (SINV-1004, SINV-1006); TOTAL Rp 127.000      <- SINV-1006 (UTC 30 Sep) masuk Oktober WIB
$ pembelian --bulan 2026-09   -> DPP Rp 2.885.000; Pajak Rp 237.600; TOTAL Rp 3.122.600; terbayar Rp 725.000
$ piutang --tempo 14 --hari-ini 2026-09-26 -> SINV-1001 sisa 356.010 telat 7 hari; SINV-1004 "tanggal invoice setelah hari ini";
                                 kredit retur SINV-1005 -Rp 72.000; PIUTANG BERSIH Rp 607.010
$ piutang --hari-ini 2026-10-05 (setelah SINV-1006) -> 4 invoice Rp 729.010; kredit -72.000; PIUTANG BERSIH Rp 657.010
$ utang --hari-ini 2026-09-26 -> PINV-1001 Rp 2.397.600 (PINV-1002 lunas; PAY-1002 batal diabaikan)
$ stok --semua                -> Beras 13, Minyak 22, Telur 11 (kantong tanpa Track Inventory tidak ditampilkan, sesuai aturan)
$ laba-rugi --bulan 2026-09   -> Penjualan 985.000 + Service 25.000 = 1.010.000; HPP Rp 994.000; beban 100.000; RUGI BERSIH -Rp 84.000
                                 "Catatan retur: … buku besar apa adanya (Reports > Profit And Loss Frappe Books): pendapatan
                                 Rp 1.154.000, HPP Rp 994.000, beban Rp 100.000, laba Rp 60.000"
$ laba-rugi --bulan 2026-10   -> pendapatan 127.000; HPP 64.000; LABA 63.000
$ laba-rugi --dari 2026-09-01 --sampai 2026-10-01 -> pendapatan 1.137.000; HPP 1.058.000; RUGI -Rp 21.000
$ laporan-harian --tanggal 2026-09-30 -> "Penjualan final: 1 invoice, -Rp 72.000" (itu retur)
$ laporan-harian --tanggal 2026-10-01 -> 2 invoice Rp 127.000, tanpa nama pelanggan
$ cek                         -> 0.36.0 | IDR | Inventory aktif | 5 pihak, 5 barang, 5→6 SINV, 2 PINV, 216 akun | struktur cocok
```

## 6. Pembanding: laporan BAWAAN Frappe Books (dijalankan di aplikasi) + hitungan Decimal penguji
Laporan bawaan dijalankan lewat komponen report aplikasi (`/report/ProfitAndLoss`, `/report/GeneralLedger`, `/report/StockBalance`).
Hitungan penguji: script Decimal sendiri (`verif.py`, tidak mengimpor script skill), membaca DB read-only.

**Profit And Loss Frappe Books, Sep 2026 (toDate 30 Sep, Monthly):**
```text
Penjualan - 4110.000          Rp 985.000
Pendapatan Service - 4310.000 Rp  25.000
HPP Pembelian - 4210.000      Rp -850.000
Biaya Sewa Gudang - 5110.015  Rp 100.000
Total Profit                  Rp  60.000
```
(sampai 1 Okt: Penjualan 1.062.000, Service 75.000, HPP −914.000, Profit 123.000.)

**General Ledger Frappe Books** menampilkan retur di sisi yang benar dengan nilai positif: SINV-1005 Piutang **Credit 72.000**;
SHPM-1005 HPP **Credit 72.000**; saldo Piutang Dagang 657.010; HPP s.d. 1 Okt 914.000. Penyebabnya di kode sumber rilis:
`reports/LedgerReport.ts` baris 108–109 `debit: Math.abs(...)`, `credit: Math.abs(...)` — **semua** laporan akuntansi Frappe
(P&L, GL, Trial Balance, Balance Sheet) membaca nilai mutlak per kolom, sehingga retur **mengurangi** pendapatan dan HPP.

| Besaran | Frappe bawaan | Penguji (Decimal) | Skill v1.0.2 | |
|---|---|---|---|---|
| Sep: DPP penjualan (retur dikurangi) | — | 591.000+245.000+246.000−72.000 = **1.010.000** | Rp 1.010.000 | ✓ |
| Sep: pajak / total | — | 65.010 / 1.075.010 | Rp 65.010 / Rp 1.075.010 | ✓ |
| Sep: pendapatan di laba rugi | 985.000 + 25.000 | 1.010.000 | Rp 1.010.000 | ✓ |
| **Sep: HPP** | **850.000** | 50.000+492.000+200.000+180.000−72.000 = **850.000** | **Rp 994.000** | ✗ (+144.000) |
| **Sep: laba bersih** | **60.000** | **60.000** | **RUGI −Rp 84.000** | ✗ |
| Catatan retur "angka P&L Frappe" | pendapatan 1.010.000, HPP 850.000 | — | "pendapatan 1.154.000, HPP 994.000" | ✗ (klaim salah; hanya laba 60.000 kebetulan sama) |
| Sep–1 Okt: HPP / laba | 914.000 / 123.000 | 914.000 / 123.000 | 1.058.000 / −21.000 | ✗ |
| Okt: pendapatan / HPP / laba | (127.000 / 64.000 / 63.000) | 127.000 / 64.000 / 63.000 | sama | ✓ |
| HPP barang berstok tercatat sekali | ya (Shipment saja) | ya | tidak ada HPP dari PINV-1001 | ✓ |
| Pembelian Sep | — | DPP 2.885.000, pajak 237.600, total 3.122.600 | sama | ✓ |
| Piutang bersih (26 Sep, sebelum SINV-1006) | saldo pihak 356.010 + 251.000 = **607.010** | Σ outstanding = 607.010 | **Rp 607.010** | ✓ |
| Piutang bersih (setelah SINV-1006) | GL Piutang 657.010 = saldo pihak 406.010 + 251.000 | 657.010 | **Rp 657.010** | ✓ |
| Utang | saldo pihak 2.397.600; GL Hutang Dagang −2.397.600 | 2.397.600 | Rp 2.397.600 | ✓ |
| Stok (Stock Balance s.d. 31 Okt) | Beras 13, Minyak 22, Telur 11 | 20−8+1=13; 30−8=22; 15−4=11 | sama | ✓ |
| Sep: "Belum dibayar" di `penjualan` | — | Σ outstanding Sep termasuk kredit retur = 530.010 → terbayar 545.000 (= kas 300.000 + 245.000) | 602.010 / terbayar 473.000 | ⚠ tidak konsisten dengan `piutang` bersih |
| Umur SINV-1001 (tempo 14, per 26 Sep) | — | jatuh tempo 19 Sep → telat 7 | telat 7 hari | ✓ |

## 7. Regresi
| Uji | Hasil |
|---|---|
| Akun bernomor | `Penjualan - 4110.000`, `Pendapatan Service - 4310.000`, `Piutang Dagang - 1131.0010`, `Hutang Dagang Dalam Negeri - 2111.001`, `Stock Diterima Tapi Tidak Ditagih - 2115.000`, `HPP Pembelian - 4210.000` — semua diterima Import Wizard ✓ |
| `--keluar` salinan `.books.db` / path `.books.db` asli / `keluar.db` / `keluar.txt` | kode 2 "harus berakhiran .csv (file ini TIDAK ditulis)" ✓ |
| `--keluar` SQLite dinamai `.csv` / symlink `.csv` → `.books.db` | kode 2 "adalah file database … Ditolak" ✓; SHA-256 file asli & salinan tidak berubah ✓ |
| NPWP (2 baris) | 2 peringatan "TIDAK ikut diimpor … catat manual"; kolom Party asli tanpa `taxId` ✓ |
| PPN `--dpp 332345` / `999999` | 36.557,95 → **36.557**; 109.999,89 → **109.999** (floor sekali) = Decimal penguji ✓ |
| PPN `--harga-termasuk 1665000` / `1000000` / `100` | DPP 1.500.000 sisa 0; DPP 900.901 PPN 99.099 sisa 0; DPP 90 PPN 9 **sisa 1** = Decimal penguji ✓ |
| Tanggal WIB | CSV `2026-09-05` → `2026-09-04T17:00Z`; SINV-1006 `2026-09-30T17:30Z` masuk Oktober WIB di `penjualan`/`laporan-harian` ✓ |
| Peringatan HPP data lama | pada salinan DB v1.0.1 (barang berstok akun HPP): `laba-rugi` mencetak "PERINGATAN: 3 barang berstok memakai akun pembelian HPP…" ✓ |
| Stock In Hand kosong | `csv-barang` memperingatkan ✓ |
| Entri dibatalkan (PAY-1002 `reverted`) | tidak mempengaruhi laporan ✓ |
| `python3 skills/frappe-books-usaha/tests/uji_regresi.py` | **42 tes OK** |
| `python3 scripts/validate.py --skill frappe-books-usaha` | "1 skill valid, 91 baris katalog sesuai" ✓ |

## 8. Temuan
**A. TINGGI (akuntansi, pemakai stok) — `laba-rugi` salah bila retur penjualan disertai pengiriman balik barang.**
Koreksi tanda di `cmd_laba_rugi` hanya berlaku untuk entri milik **invoice** retur (`SalesInvoice`/`PurchaseInvoice` dengan
`returnAgainst`). Pengiriman retur (Shipment/Purchase Receipt ber-`returnAgainst`, dibuat tombol retur aplikasi saat barang kembali ke
gudang) juga ditulis Frappe dengan nilai negatif di sisi "terbalik" (`HPP credit −72.000`), tetapi tidak dikoreksi → HPP naik 72.000
alih-alih turun 72.000. Pada data uji: HPP Rp 994.000 vs **Rp 850.000** di P&L Frappe dan hitungan penguji; **laba Rp 60.000 dilaporkan
RUGI −Rp 84.000**. Selain itu klaim di kode, SKILL.md ("retur menambah pendapatan di buku besar & di Profit And Loss Frappe Books")
dan teks "Catatan retur" (angka "apa adanya" = P&L Frappe) **tidak sesuai aplikasi asli**: P&L/GL Frappe memakai `Math.abs` per kolom
(`reports/LedgerReport.ts`), sehingga retur mengurangi pendapatan & HPP. Perbaikan yang disarankan: baca **setiap** entri buku besar
seperti Frappe (`abs(debit)`, `abs(credit)`), hapus/ubah "Catatan retur" menjadi keterangan bahwa angka = P&L Frappe, perbaiki kalimat
di SKILL.md, dan tambah tes regresi berisi Shipment retur (HPP harus 850.000, laba 60.000 pada data seperti di atas).

**B. SEDANG/RENDAH — `penjualan` "Belum dibayar / Terbayar (bersih)" tidak memakai kredit retur**, padahal `piutang` sudah (v1.0.2).
Sep: belum dibayar 602.010 & terbayar 473.000, sedangkan sisa bersih 530.010 dan uang yang benar-benar masuk 545.000. Angka 473.000 tidak
bermakna bagi pemilik. Samakan dengan `piutang` (sertakan outstanding negatif retur) atau tampilkan "kredit retur" terpisah.

**C. RENDAH —** `laporan-harian` 30 Sep menulis "Penjualan final: 1 invoice, -Rp 72.000" untuk hari yang hanya berisi retur; beri label
"retur". Esoknya "Kemarin: belum ada penjualan final" padahal ada retur — tidak salah, tapi bisa membingungkan.

**D. RENDAH/UX —** `csv-transaksi` menolak `pajak = PPN` walau hanya ada satu template `PPN 11% (12% x 11/12)`. Aman (tidak menebak) dan
pesannya jelas; pertimbangkan menerima awalan yang cocok tunggal atau contoh di SKILL.md memakai nama lengkap.

**Catatan aplikasi Frappe Books v0.36.0 (bukan kesalahan skill, layak masuk `references/import-wizard.md`):**
1. Purchase Receipt dari invoice ber-PPN dinilai **termasuk PPN** (Persediaan 2.397.600 vs Stock Diterima… 2.160.000) → saldo akun
   Stock Diterima Tapi Tidak Ditagih −237.600 dan nilai Persediaan di buku besar lebih besar dari Stock Balance. HPP tidak terpengaruh
   (Shipment memakai tarif penilaian 60.000/32.000).
2. Barang **tanpa** Track Inventory (kantong) tetap ikut Purchase Receipt/Shipment: HPP 50.000 saat pembelian + 20.000 lagi saat
   Shipment, dan masuk Persediaan. Sarankan menghapus baris non-stok dari Receipt/Shipment (seperti baris jasa).
3. Pengiriman retur dinilai dengan **harga jual** (72.000), bukan harga pokok (60.000) → nilai stok & HPP sedikit menyimpang.
4. Shipment dari nota barang+jasa gagal ("reading 'Stores'"); pembayaran sebagian butuh Enable Partial Payment (sudah dicatat 08).

## 9. Status temuan v1.0.1
| # | Temuan v1.0.1 | Status v1.0.2 |
|---|---|---|
| A | Barang berstok dibukukan ke HPP → HPP ganda | **Beres** — CSV memberi `Stock Diterima Tapi Tidak Ditagih - 2115.000`; PINV tidak menyentuh HPP; HPP dari Shipment saja; peringatan data lama berfungsi |
| B | `piutang` mengabaikan kredit retur | **Beres** — kredit retur didaftar; PIUTANG BERSIH = saldo pihak & GL Frappe (607.010 / 657.010) |
| C | Invoice bertanggal masa depan | **Beres** — ditandai "tanggal invoice setelah hari ini" |
| D | Dokumen | Sebagian — klaim retur vs P&L Frappe kini terbukti keliru (temuan A baru) |
