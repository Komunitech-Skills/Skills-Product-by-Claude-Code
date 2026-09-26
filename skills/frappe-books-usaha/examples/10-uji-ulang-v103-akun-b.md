# 10 — Uji ulang independen v1.0.3 dengan Frappe Books v0.36.0 ASLI (penguji Akun B, 26 Sep 2026)

Penguji independen keempat (bukan pembuat, bukan penguji 03–09). Semua nama usaha/pelanggan/pemasok **fiktif**. Berkas kerja di
scratchpad penguji (`rt-frappe4/`), tidak ada yang masuk repo. Script, SKILL.md, README, dan katalog **tidak diubah**.
Fokus: temuan A v1.0.2 (`laba-rugi` tidak mengoreksi pengiriman retur) + dua siklus transaksi berbeda + regresi.

## 1. Lingkungan
| Hal | Nilai |
|---|---|
| Aplikasi | `Frappe-Books-v0.36.0-linux-x86_64.AppImage`, **diunduh sendiri** dari GitHub releases `frappe/books` tag v0.36.0 |
| Checksum | SHA-512 (base64) `nFHZaPXph+L63yBvX4gQontVek2AZMDijuvPDFjQoOGQTJ4aTDxNxGNcCn/M4FcI33i01jdbhZpn8vkkqfBXmg==` **cocok** dengan `latest-linux.yml` rilis yang sama (diunduh sendiri); ukuran 103.984.584 byte cocok; SHA-256 `c079d60b…fee79602` |
| Jalan | AppImage diekstrak, headless Xvfb, `TZ=Asia/Jakarta`, mode produksi (`app://`), proxy keluar diblokir (`--proxy-server=127.0.0.1:9`), HOME terpisah |
| Kendali | Chrome DevTools Protocol lokal. Hanya `dialog.showOpenDialog` di proses utama yang diarahkan ke path CSV (pengganti klik dialog OS) |
| Skill | `scripts/frappe_books.py` **1.0.3** (`--versi`), salinan folder skill, dijalankan dengan `--db` ke file asli **saat aplikasi terbuka** |

## 2. Database baru milik penguji + impor lewat Import Wizard ASLI
Setup Wizard → "Toko Uji Siklus v103 Akun B (fiktif)", Indonesia → IDR + "Indonesia - Chart of Accounts" (216 akun). Inventory &
Enable Partial Payment dicentang; akun `Persediaan Toko - 1141.001` (tipe Stock) → Stock In Hand; template `PPN 11% (12% x 11/12)`.
`cek` → 0.36.0 | IDR | Inventory aktif | struktur cocok ✓.

Input pengguna (pemisah `;`, bahasa sehari-hari): 3 pelanggan + 2 pemasok (2 NPWP, `"Warung Kopi Bang Udin, Depok"`, HP `0812-…`/`+62 857 …`/`021-…`);
barang `Kopi Arabika Gayo 250g` (`Rp 95.000`, stok ya), `Gula Aren Cair 1L` (`45rb`, stok ya), `Susu UHT 1L` (`22000`, stok ya),
`Jasa Seduh Event` (jasa, `150rb`), `Jasa Desain Label` (jasa, `500.000`); nota dengan tanggal `02/09/2026`, `5 Sep 2026`, `2026-09-12`,
nama pelanggan huruf kecil (`kafe senja jaya`), harga `60.000`/`25rb`/`95rb`.

| CSV dari script | Kode | Import Wizard asli (Select File → Import Data → "Submit entries?" **No**) |
|---|---|---|
| `csv-pelanggan` | 0, LOLOS 5 + **2 peringatan NPWP** per nama | errorMessage kosong, requiredNotSelected/cellErrors/absentLinks `[]` → **5/5 sukses** |
| `csv-barang --lacak-stok` | 0, LOLOS 5 | **5/5 sukses**; barang stok → `Stock Diterima Tapi Tidak Ditagih - 2115.000`, `trackItem=1`; jasa → `HPP Pembelian - 4210.000` / `Pendapatan Service - 4310.000`, `trackItem=0` |
| `csv-transaksi --jenis pembelian` (siklus 1) | 0, B1-01 DPP 1.450.000 PPN 159.500 total 1.609.500 | **PINV-1001 sukses**; draf total 1.609.500 = pratinjau |
| `csv-transaksi` (siklus 1) | 0, J1-01 DPP 750.000 PPN 82.500 total 832.500; J1-02 285.000 | **SINV-1001..1002 sukses**; total = pratinjau |
| `csv-transaksi --jenis pembelian` (siklus 2) | 0, B2-01 (Susu + Jasa Desain) 954.600; B2-02 620.000 | **PINV-1002..1003 sukses** |
| `csv-transaksi` (siklus 2) | 0, J2-01 DPP 695.000 PPN 76.450 total 771.450 | **SINV-1005 sukses** |
| `csv-transaksi` nota pecahan (12.345 × 3 + 45.005) | 0, DPP 82.040 PPN (floor) 9.024 | **SINV-1007 sukses (draf)**; Frappe pajak 9.024,40 → beda 0,40 sesuai peringatan skill |

Total 0 gagal. Tanggal CSV `2026-09-05` tersimpan `2026-09-04T17:00Z` (00:00 WIB) ✓.

## 3. Siklus 1 (September): beli → terima → jual → kirim → retur penjualan → barang retur masuk stok
Lewat mesin aplikasi (fungsi yang sama dengan tombol UI): submit PINV-1001/SINV-1001/SINV-1002 → **Purchase Receipt** PREC-1001 (3 Sep) →
**Shipment** SHPM-1001 (SINV-1001) & SHPM-1002 (SINV-1002) → SINV-1003 jasa Rp 150.000 bertanggal **1 Sep 00:30 WIB** (tersimpan
`2026-08-31T17:30Z`) → bayar penuh SINV-1002 (PAY-1001) → **retur** SINV-1004 atas SINV-1001 (2 kopi + PPN, 20 Sep, −210.900) →
**pengiriman retur** SHPM-1003 (`isReturn`, `returnAgainst = SHPM-1001`, dibuat oleh `getStockTransfer` invoice retur) → jurnal beban BBM 75.000.

Buku besar retur (read-only): `SHPM-1003 HPP Pembelian credit 190.000` (GL Frappe menampilkan Credit positif; dinilai harga jual 95.000).

**Pembanding September** (laporan bawaan dijalankan di aplikasi: `/report/ProfitAndLoss` 1–30 Sep Monthly, `/report/GeneralLedger`,
`/report/StockBalance`, `Party.outstandingAmount`; Decimal penguji = `verif.py` sendiri, tidak mengimpor script skill):

| Besaran | Frappe bawaan | Penguji (Decimal) | Skill v1.0.3 | |
|---|---|---|---|---|
| Pendapatan (Penjualan + Service) | 845.000 + 150.000 | 750.000 + 285.000 − 190.000 + 150.000 = **995.000** | Rp 845.000 + Rp 150.000 = Rp 995.000 | ✓ |
| **HPP** | **450.000** (GL: 460.000 + 180.000 − 190.000) | **450.000** | **Rp 450.000** | ✓ |
| Beban | 75.000 | 75.000 | Rp 75.000 | ✓ |
| **Laba bersih** | **Total Profit 470.000** | **470.000** | **LABA BERSIH Rp 470.000** | ✓ |
| Catatan retur | — | SINV-1004, SHPM-1003 | "2 dokumen retur (SHPM-1003, SINV-1004) sudah MENGURANGI pendapatan/HPP" | ✓ |
| `penjualan` DPP / pajak / total | GL Hutang Pajak 82.500 − 20.900 | 995.000 / 61.600 / 1.056.600 | sama; final 4 (termasuk 1 retur) | ✓ |
| `penjualan` terbayar / belum dibayar | GL Piutang closing 771.600 | 285.000 / 771.600 | Rp 285.000 / Rp 771.600 (dikurangi kredit retur −210.900) | ✓ |
| `penjualan --per barang` | — | Kopi 6+3−2 = 7 (665.000), Gula 4 (180.000), Jasa 1 (150.000) | sama | ✓ |
| `pembelian` | GL Hutang −1.609.500 | 1.450.000 / 159.500 / 1.609.500 | sama | ✓ |
| `piutang` bersih (30 Sep) | saldo pihak Kafe Senja 771.600 + Warung 0 | 150.000 + 832.500 − 210.900 = **771.600** | PIUTANG BERSIH Rp 771.600; kredit SINV-1004 −210.900 didaftar | ✓ |
| `utang` (30 Sep) | saldo pihak 1.609.500 | 1.609.500 | Rp 1.609.500 | ✓ |
| `stok --semua` | Stock Balance: Kopi 13, Gula 6 | 20−6−3+2 = 13; 10−4 = 6 | Kopi 13, Gula 6, Susu 0 (HABIS) | ✓ |
| `laporan-harian` 20 Sep | — | hanya retur | "Penjualan final: 0 … Retur penjualan: 1 nota, -Rp 210.900" (label retur benar) | ✓ |
| `laporan-harian` 1 Sep (00:30 WIB) | GL Piutang: Sep 1 | 1 invoice 150.000 | "1 invoice, Rp 150.000"; `penjualan --bulan 2026-08` = 0 invoice | ✓ |
| File tidak berubah saat dibaca | — | SHA-256 sebelum/sesudah semua perintah | sama | ✓ |

Temuan A v1.0.2 **beres**: dengan aturan lama (koreksi hanya invoice retur) HPP akan 830.000 dan laba 90.000; v1.0.3 = P&L Frappe.

## 4. Siklus 2 (Oktober): beli barang berstok & jasa, jual sebagian, retur pembelian ke pemasok, pembayaran sebagian
Submit PINV-1002 (Susu 24 × 15.000 + Jasa Desain Label 500.000, PPN) / PINV-1003 (Kopi 10 × 62.000) / SINV-1005 → Receipt PREC-1002
(baris jasa dihapus) & PREC-1003 → Shipment SHPM-1004 (Susu 10 + Kopi 5; jual sebagian stok) → **retur pembelian** PINV-1005 atas
PINV-1002 (4 Susu, −60.000 + PPN −6.600 = −66.600, 10 Okt) → **barang keluar ke pemasok** PREC-1004 (`isReturn`, `returnAgainst = PREC-1002`)
→ bayar sebagian SINV-1005 400.000 (PAY-1002), PINV-1002 500.000 (PAY-1005), PINV-1001 1.000.000 (PAY-1006) → jurnal sewa kantor 100.000
→ SINV-1006 jasa 300.000 bertanggal **1 Nov 00:15 WIB** (tersimpan `2026-10-31T17:15Z`) → SINV-1007 draf (nota pecahan, 5 Nov).

Kesalahan harness penguji yang **dibatalkan** di aplikasi (sekaligus menguji entri `reverted`/dokumen batal): PINV-1004 (retur dengan
tarif salah, lihat catatan aplikasi 2) dan PAY-1003/PAY-1004 (akun kas tertukar). Keduanya di-**Cancel**, lalu dibuat ulang dengan benar.

| Besaran (Oktober) | Frappe bawaan | Penguji (Decimal) | Skill v1.0.3 | |
|---|---|---|---|---|
| Pendapatan | 695.000 | 220.000 + 475.000 = 695.000 | Rp 695.000 | ✓ |
| **HPP** | **950.000** (SHPM-1004 450.000 + jasa beli PINV-1002 500.000) | Susu 10×15.000 + Kopi 5×60.000 (FIFO) + 500.000 = **950.000** | **Rp 950.000** | ✓ |
| Beban | 100.000 | 100.000 | Rp 100.000 | ✓ |
| **Laba** | **Total Profit −355.000** | **−355.000** | **RUGI BERSIH: -Rp 355.000** (LABA KOTOR −255.000) | ✓ |
| Retur pembelian di P&L | tidak menyentuh akun laba rugi | — | tidak ada "Catatan retur" (benar) | ✓ |
| `penjualan` Okt | GL Piutang closing Okt 371.450 | 695.000 / 76.450 / 771.450; terbayar 400.000 | sama; SINV-1006 **tidak** masuk Okt | ✓ |
| `penjualan` Nov | P&L Nov Service 300.000 | 300.000; draf 1 | "final 1 | draf 1 (tidak dihitung)", Rp 300.000 | ✓ |
| `pembelian` Okt | GL Hutang Okt: +66.600 retur | DPP 860.000+620.000−60.000 = 1.420.000; pajak 94.600−6.600 = 88.000; total 1.508.000; terbayar 500.000; belum 1.008.000 | sama; "dibatalkan: 1" (PINV-1004); per pemasok CV Mitra Kemasan 888.000 | ✓ |
| `pembelian --per barang` | — | Susu 24−4 = 20 (300.000), Kopi 10, Jasa 1 | sama | ✓ |
| `utang` bersih (31 Okt) | saldo pihak 388.000 + 1.229.500; GL Hutang Sep–Nov −1.617.500 | 609.500 + 454.600 + 620.000 − 66.600 = **1.617.500** | UTANG BERSIH Rp 1.617.500; kredit PINV-1005 −66.600 didaftar; PINV-1001 telat 29 hari | ✓ |
| `piutang` bersih (31 Okt) | saldo pihak 771.600 + 671.450; GL Piutang Sep–Nov 1.443.050 | **1.443.050** | Rp 1.443.050; SINV-1006 ditandai "tanggal invoice setelah hari ini" | ✓ |
| `piutang --tempo 14` (10 Nov) | — | SINV-1003 1 Sep+14 → telat 56; SINV-1005 → 21 | sama, dikelompokkan 31–60 / 1–30 hari | ✓ |
| `stok --semua` / `--min 10` | Stock Balance: Kopi 18, Gula 6, Susu 10 | 13+10−5 = 18; 6; 24−10−4 = 10 | sama; `--min 10` → Gula & Susu menipis | ✓ |
| `laporan-harian` 6 Okt / 1 Nov / 31 Okt | — | 771.450 / 300.000 / 0 | sama; tanpa nama pelanggan; telat dihitung terhadap `--tanggal` | ✓ |
| `laba-rugi` 1 Sep–30 Nov | P&L: 470.000 − 355.000 + 300.000 | 1.990.000 / 1.400.000 / 175.000 / **415.000** | sama | ✓ |
| Entri batal (PINV-1004, PAY-1003/1004) | tidak tampil di GL | diabaikan (`reverted`/`cancelled`) | tidak dihitung | ✓ |

## 5. PPN (`ppn`) vs Frappe dan Decimal penguji
| Input | Frappe (template 11%) | Decimal penguji (floor sekali) | Skill | |
|---|---|---|---|---|
| DPP 750.000 / 190.000 / 860.000 / 60.000 / 695.000 | 82.500 / 20.900 / 94.600 / 6.600 / 76.450 | sama | sama (pratinjau CSV & `ppn`) | ✓ |
| DPP 82.040 (SINV-1007) | **9.024,40** | 9.024 | 9.024 (+ peringatan beda pecahan) | ✓ |
| DPP 37.035 / 332.345 / 999.999 | — | 4.073 / 36.557 / 109.999 | sama | ✓ |
| Harga termasuk 1.665.000 / 1.000.000 / 100 | — | DPP 1.500.000 sisa 0 / 900.901 PPN 99.099 sisa 0 / 90 PPN 9 **sisa 1** | sama | ✓ |

## 6. Regresi
| Uji | Hasil |
|---|---|
| Akun bernomor | `Penjualan - 4110.000`, `Pendapatan Service - 4310.000`, `Piutang Dagang - 1131.0010`, `Hutang Dagang Dalam Negeri - 2111.001`, `Stock Diterima Tapi Tidak Ditagih - 2115.000`, `HPP Pembelian - 4210.000` — diterima Import Wizard ✓ |
| `--keluar` ke `.books.db` asli / salinan `.books.db` / `keluar.db` / `keluar.txt` / SQLite dinamai `.csv` / symlink `.csv` → `.books.db` | semua kode 2, tidak ada file dibuat; SHA-256 DB asli & salinan tidak berubah ✓ |
| NPWP | 2 peringatan per nama "TIDAK ikut diimpor … Catat manual" ✓ |
| PPN bulat ke bawah | lihat §5 ✓ |
| Tanggal WIB | CSV → 17:00Z hari sebelumnya; 1 Sep 00:30 WIB masuk Sep (bukan Agu); 1 Nov 00:15 WIB masuk Nov (bukan Okt) di `penjualan`, `laba-rugi`, `laporan-harian` ✓ |
| `pajak = PPN` (temuan D v1.0.2) | kini diterima bila hanya satu template cocok, dengan peringatan "dianggap 'PPN 11% (12% x 11/12)'" ✓ |
| Input buruk | `85,000` ambigu → kode 5; pihak belum ada → kode 5; tanggal `31/13/2026` → kode 5; byte 0x81 → kode 5 ramah; `--bulan 2026-13`/`--tz PST` → kode 2; CSV dipakai sebagai `--db` → kode 3; file CSV tidak dibuat saat gagal ✓ |
| `python3 skills/frappe-books-usaha/tests/uji_regresi.py` | **46 tes OK** |
| `python3 scripts/validate.py --skill frappe-books-usaha` | "1 skill valid, 91 baris katalog sesuai" ✓ |
| Aplikasi dimatikan | proses Frappe Books & port DevTools tertutup setelah uji ✓ |

## 7. Temuan
**Tidak ada temuan TINGGI/SEDANG.** Semua angka 8 perintah laporan cocok dengan laporan bawaan Frappe dan hitungan Decimal penguji di dua siklus.

- **A. RENDAH (teks)** — keluaran `pembelian` yang berisi retur menulis "'Belum dibayar' = … (sama dengan **PIUTANG BERSIH** di perintah
  **'piutang'**)". Untuk pembelian seharusnya "UTANG BERSIH … 'utang'". Angkanya benar (1.008.000).
- **B. RENDAH (UX)** — `csv-transaksi` hanya melaporkan masalah pertama per baris (baris dengan tanggal salah **dan** barang tidak ada hanya
  menyebut tanggal) → pengguna bisa perlu dua putaran perbaikan.
- **C. RENDAH (dok)** — SKILL.md masih menulis v1.0.3 "belum diuji ulang oleh penguji independen"; perbarui setelah laporan ini.

**Catatan aplikasi Frappe Books v0.36.0 (bukan kesalahan skill, layak masuk `references/import-wizard.md`):**
1. Membuat pengembalian barang dari **invoice retur pembelian** (`getStockTransfer`) gagal: "Not Found: SalesInvoice PINV-1002" (kode mencari
   `returnAgainst` di SalesInvoice). Jalan keluar: buka Purchase Receipt aslinya → Return. Retur penjualan tidak terkena.
2. Mengubah Quantity di baris dokumen retur pembelian mengganti **Rate ke harga jual barang** (22.000, bukan harga beli 15.000); nilai retur
   jadi −97.680. Pengguna wajib mengecek Rate sebelum Submit.
3. Purchase Receipt dinilai termasuk PPN (PREC-1001 1.609.500) dan retur Receipt PREC-1004 tercatat 34.600 di buku besar (bukan 60.000);
   hanya memengaruhi neraca (Persediaan/Stock Diterima…), bukan laba rugi atau jumlah stok.
4. Pengiriman retur dinilai **harga jual**: HPP Sep turun 190.000 padahal harga pokok 2 kopi 120.000 → laba Frappe 470.000 vs laba
   "ekonomis" 400.000. Skill mengikuti buku besar (= P&L Frappe) dan SKILL.md sudah menjelaskannya.

## 8. Status temuan v1.0.2
| # | Temuan v1.0.2 | Status v1.0.3 |
|---|---|---|
| A | `laba-rugi` tidak mengoreksi Shipment retur | **Beres** — HPP 450.000, laba 470.000 = P&L Frappe = Decimal |
| B | `penjualan` Belum dibayar tanpa kredit retur | **Beres** — 771.600 = piutang bersih; pembelian juga (1.008.000) |
| C | `laporan-harian` hari retur berlabel "Penjualan" | **Beres** — "Retur penjualan: 1 nota, -Rp 210.900" |
| D | `pajak = PPN` ditolak | **Beres** — dicocokkan ke satu-satunya template, dengan peringatan |
