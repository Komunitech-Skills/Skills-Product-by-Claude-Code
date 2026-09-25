# Skenario 03 — Penawaran 76% HPS + satu baris volume × harga salah di CSV pengguna

> Uji independen, 2026-09-25. Tiga varian CSV yang lazim ditempel pengguna dari Excel. Output script apa adanya.

## Input pengguna
"Saya PKP. Tender mebel kantor, HPS Rp538 juta. Ini rincian dari Excel saya, total Rp379.370.250 sudah termasuk PPN. 70% HPS, aman kan?"

## Varian A — ada kolom Jumlah + baris TOTAL di kolom Harga Satuan (layout Excel umum)
```
No;Uraian;Volume;Satuan;Harga Satuan;Jumlah
1;Kursi kerja staf jaring;120;unit;Rp1.185.000;Rp142.200.000
2;Meja kerja 120x60 cm;60;unit;Rp1.640.000;Rp98.400.000
3;Lemari arsip besi 4 laci;25;unit;Rp2.975.000;Rp47.375.000   <- SALAH (seharusnya 74.375.000)
4;Rak buku 5 susun;30;unit;Rp1.210.000;Rp36.300.000
5;Ongkos kirim & pasang;1;ls;Rp17.500.000;Rp17.500.000
;;;;TOTAL;Rp341.775.000
```
`python3 scripts/cek_penawaran.py harga s03.csv --ppn nonmewah --hps "Rp538.000.000"`
```
RINCIAN PENAWARAN HARGA (hasil hitung script)

 No  Uraian                        Volume  Sat             Harga Satuan              Jumlah
  1  Kursi kerja staf jaring          120  unit             Rp1.185.000       Rp142.200.000
  2  Meja kerja 120x60 cm              60  unit             Rp1.640.000        Rp98.400.000
  3  Lemari arsip besi 4 laci          25  unit             Rp2.975.000        Rp74.375.000
  4  Rak buku 5 susun                  30  unit             Rp1.210.000        Rp36.300.000
  5  Ongkos kirim & pasang              1  ls              Rp17.500.000        Rp17.500.000

Subtotal (DPP)                     : Rp368.775.000
PPN 12% x 11/12 DPP (efektif 11%)  : Rp40.565.250
TOTAL PENAWARAN                    : Rp409.340.250
Terbilang: Empat Ratus Sembilan Juta Tiga Ratus Empat Puluh Ribu Dua Ratus Lima Puluh Rupiah

HPS                                : Rp538.000.000
Penawaran terhadap HPS             : 76,09%
Batas 80% HPS                      : Rp430.400.000
Selisih (HPS - penawaran)          : Rp128.659.750

PERINGATAN:
  - 1 baris tidak bisa dibaca dan TIDAK ikut dihitung -> TOTAL BELUM FINAL. Perbaiki dulu.
  - Total penawaran 76,09% HPS (< 80% HPS = di bawah Rp430.400.000). Pokja/Pejabat Pengadaan akan melakukan KLARIFIKASI KEWAJARAN HARGA: siapkan rincian harga dasar (bukti harga pemasok/upah/alat). Jika dinyatakan wajar dan menang, biasanya wajib menaikkan jaminan pelaksanaan menjadi 5% dari nilai HPS (cek dokumen pemilihan).

Baris bermasalah:
  - baris 7 ('?'): uraian kosong

Pembulatan: jumlah baris ke rupiah terdekat; PPN dihitung persis dari DPP lalu dibulatkan ke bawah. Belum dicocokkan dengan Coretax/SPSE. Pastikan format & aturan pembulatan mengikuti dokumen pemilihan.
```
**Temuan:** (1) kolom `Jumlah` milik pengguna **diabaikan** — script tidak menunjuk baris 3 sebagai baris yang salah; (2) baris `TOTAL` yang labelnya ada di kolom Harga Satuan tidak dikenali sebagai baris total → dilaporkan "uraian kosong" dan status **TOTAL BELUM FINAL**, padahal semua item terbaca. Agent harus membandingkan sendiri kolom Jumlah.

## Varian B — baris Jumlah/PPN/Total di kolom Uraian
```
No;Uraian;Volume;Satuan;Harga Satuan;Jumlah
1;Kursi kerja staf jaring;120;unit;Rp1.185.000;Rp142.200.000
2;Meja kerja 120x60 cm;60;unit;Rp1.640.000;Rp98.400.000
3;Lemari arsip besi 4 laci;25;unit;Rp2.975.000;Rp47.375.000
4;Rak buku 5 susun;30;unit;Rp1.210.000;Rp36.300.000
5;Ongkos kirim & pasang;1;ls;Rp17.500.000;Rp17.500.000
;Jumlah;;;;Rp341.775.000
;PPN 11%;;;;Rp37.595.250
;Total;;;;Rp379.370.250
```
```
RINCIAN PENAWARAN HARGA (hasil hitung script)

 No  Uraian                        Volume  Sat             Harga Satuan              Jumlah
  1  Kursi kerja staf jaring          120  unit             Rp1.185.000       Rp142.200.000
  2  Meja kerja 120x60 cm              60  unit             Rp1.640.000        Rp98.400.000
  3  Lemari arsip besi 4 laci          25  unit             Rp2.975.000        Rp74.375.000
  4  Rak buku 5 susun                  30  unit             Rp1.210.000        Rp36.300.000
  5  Ongkos kirim & pasang              1  ls              Rp17.500.000        Rp17.500.000

Subtotal (DPP)                     : Rp368.775.000
PPN 12% x 11/12 DPP (efektif 11%)  : Rp40.565.250
TOTAL PENAWARAN                    : Rp409.340.250
Terbilang: Empat Ratus Sembilan Juta Tiga Ratus Empat Puluh Ribu Dua Ratus Lima Puluh Rupiah

HPS                                : Rp538.000.000
Penawaran terhadap HPS             : 76,09%
Batas 80% HPS                      : Rp430.400.000
Selisih (HPS - penawaran)          : Rp128.659.750

PERINGATAN:
  - Baris 'Jumlah' di file bernilai Rp341.775.000 tetapi TIDAK cocok dengan hitungan script (subtotal Rp368.775.000, total Rp409.340.250). Cek rumus di Excel/dokumen.
  - Baris 'PPN 11%' di file bernilai Rp37.595.250 tetapi TIDAK cocok dengan hitungan script (subtotal Rp368.775.000, total Rp409.340.250). Cek rumus di Excel/dokumen.
  - Baris 'Total' di file bernilai Rp379.370.250 tetapi TIDAK cocok dengan hitungan script (subtotal Rp368.775.000, total Rp409.340.250). Cek rumus di Excel/dokumen.
  - Total penawaran 76,09% HPS (< 80% HPS = di bawah Rp430.400.000). Pokja/Pejabat Pengadaan akan melakukan KLARIFIKASI KEWAJARAN HARGA: siapkan rincian harga dasar (bukti harga pemasok/upah/alat). Jika dinyatakan wajar dan menang, biasanya wajib menaikkan jaminan pelaksanaan menjadi 5% dari nilai HPS (cek dokumen pemilihan).

Baris dilewati:
  - baris 7: 'Jumlah' dianggap baris total/pajak -> tidak dihitung ulang
  - baris 8: 'PPN 11%' dianggap baris total/pajak -> tidak dihitung ulang
  - baris 9: 'Total' dianggap baris total/pajak -> tidak dihitung ulang

Pembulatan: jumlah baris ke rupiah terdekat; PPN dihitung persis dari DPP lalu dibulatkan ke bawah. Belum dicocokkan dengan Coretax/SPSE. Pastikan format & aturan pembulatan mengikuti dokumen pemilihan.
```
**Catatan:** ketiga baris ringkasan dikenali & dibandingkan ✅. Pesan untuk baris "PPN 11%" hanya menampilkan subtotal & total, bukan PPN hitungan script (Rp40.565.250) — kurang jelas.

## Varian C — hanya baris total dari Excel
```
RINCIAN PENAWARAN HARGA (hasil hitung script)

 No  Uraian                        Volume  Sat             Harga Satuan              Jumlah
  1  Kursi kerja staf jaring          120  unit             Rp1.185.000       Rp142.200.000
  2  Meja kerja 120x60 cm              60  unit             Rp1.640.000        Rp98.400.000
  3  Lemari arsip besi 4 laci          25  unit             Rp2.975.000        Rp74.375.000
  4  Rak buku 5 susun                  30  unit             Rp1.210.000        Rp36.300.000
  5  Ongkos kirim & pasang              1  ls              Rp17.500.000        Rp17.500.000

Subtotal (DPP)                     : Rp368.775.000
PPN 12% x 11/12 DPP (efektif 11%)  : Rp40.565.250
TOTAL PENAWARAN                    : Rp409.340.250
Terbilang: Empat Ratus Sembilan Juta Tiga Ratus Empat Puluh Ribu Dua Ratus Lima Puluh Rupiah

HPS                                : Rp538.000.000
Penawaran terhadap HPS             : 76,09%
Batas 80% HPS                      : Rp430.400.000
Selisih (HPS - penawaran)          : Rp128.659.750

PERINGATAN:
  - Baris 'Total (dari Excel)' di file bernilai Rp379.370.250 tetapi TIDAK cocok dengan hitungan script (subtotal Rp368.775.000, total Rp409.340.250). Cek rumus di Excel/dokumen.
  - Total penawaran 76,09% HPS (< 80% HPS = di bawah Rp430.400.000). Pokja/Pejabat Pengadaan akan melakukan KLARIFIKASI KEWAJARAN HARGA: siapkan rincian harga dasar (bukti harga pemasok/upah/alat). Jika dinyatakan wajar dan menang, biasanya wajib menaikkan jaminan pelaksanaan menjadi 5% dari nilai HPS (cek dokumen pemilihan).

Baris dilewati:
  - baris 7: '' dianggap baris total/pajak -> tidak dihitung ulang

Pembulatan: jumlah baris ke rupiah terdekat; PPN dihitung persis dari DPP lalu dibulatkan ke bawah. Belum dicocokkan dengan Coretax/SPSE. Pastikan format & aturan pembulatan mengikuti dokumen pemilihan.
```

## Jawaban agent
- **Ada salah hitung di baris 3 (Lemari arsip):** 25 × Rp2.975.000 = **Rp74.375.000**, bukan Rp47.375.000 (kemungkinan salah ketik 74↔47). Selisih Rp27.000.000.
  *(Baris ini ditemukan agent dengan membandingkan manual kolom Jumlah; script tidak menunjuknya.)*
- Setelah dikoreksi: DPP **Rp368.775.000**, PPN **Rp40.565.250**, total **Rp409.340.250** (Empat Ratus Sembilan Juta Tiga Ratus Empat Puluh Ribu Dua Ratus Lima Puluh Rupiah) = **76,09% HPS**.
- Versi Excel Anda (Rp379.370.250 = 70,51% HPS) **salah**; jangan unggah angka itu. Pada kontrak harga satuan, pokja dapat melakukan koreksi aritmatik — total berubah, dan terbilang di surat penawaran jadi tidak cocok.
- **< 80% HPS (batas Rp430.400.000):** siap-siap **klarifikasi kewajaran harga** — siapkan bukti harga pemasok per item, ongkos kirim, margin. Jika wajar & menang: **jaminan pelaksanaan 5% × HPS = Rp26.900.000** (bukan 5% × nilai kontrak Rp20.467.013). Tidak wajar → gugur.
- Arus kas: bendahara memungut PPN Rp40.565.250 & PPh 22 1,5% × DPP = Rp5.531.625.

## Verifikasi independen (Decimal)
142.200.000 + 98.400.000 + 74.375.000 + 36.300.000 + 17.500.000 = **368.775.000** ✅; PPN floor(368.775.000 × 0,11) = **40.565.250** ✅; total **409.340.250** ✅; 409.340.250 / 538.000.000 = 76,0855% → **76,09%** ✅; 80% = 430.400.000 ✅; versi pengguna 341.775.000 + 37.595.250 = 379.370.250 → 70,51% ✅; 5% HPS = 26.900.000 ✅.
