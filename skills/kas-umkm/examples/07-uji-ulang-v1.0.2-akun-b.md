# 07 — Uji ulang v1.0.2 (penguji independen Akun B, 26-09-2026)

> Uji perawatan atas perbaikan temuan uji ulang v1.0.1 (U19): biaya tarik tunai hilang dari laba emkm [SEDANG] dan baris "Per minggu" mencampur 'Perlu dicek' [RENDAH]. Skill + `laporan-keuangan-emkm` (1.3.0) disalin ke scratchpad `rt-u19b/sk/`, data **fiktif**, simulasi agent `claude-code`. Kode skill tidak diubah.

## 1. Data uji 06 diulang persis (Warung Uji Fiktif, mutasi BRI 9 baris)
Hasil impor sama dengan uji 06 (Laci 600.000 / BRI 9.042.500 / GoPay 400.000; hasil usaha 2.092.500; 3 'Perlu dicek'). Setelah `golongkan` #11 prive, #12 lain-lain, #13 penjualan → hasil usaha **4.942.500**.
Ekspor emkm kini: `BIAYA TARIK TUNAI ATM BERSAMA;;7500;beban_keuangan` (v1.0.1: kolom kosong).
`laporan_emkm.py … --kas-akhir-aktual 10042500 --format json`:
| Besaran | v1.0.1 (uji 06) | v1.0.2 |
|---|---:|---:|
| Laba bersih emkm | 4.950.000 | **4.942.500** = hasil usaha ✅ |
| Beban keuangan | 0 | 7.500 |
| Neraca | TIDAK SEIMBANG −7.500 | **seimbang, selisih 0, selisih kas 0** ✅ |
| Total aset | — | 10.042.500 (= saldo gabungan) |

## 2. Data baru buatan penguji (Katering Uji Fiktif)
Mulai 10/09/2026: Laci 750.000, Mandiri (bank, QRIS) 8.000.000, OVO 0. Mutasi Mandiri 10 baris (`Debit/Kredit`): QRIS +2.400.000; BIAYA ADM BULANAN −12.500; TARIK TUNAI ATM −1.000.000; BIAYA TARIK TUNAI ATM LINK −6.500; BIAYA TRF BI-FAST −2.500; TRF BI-FAST ke CV Sayur −850.000; SETOR TUNAI +500.000; TOPUP OVO −150.000; BUNGA TABUNGAN +1.234; PAJAK BUNGA −247. Impor dengan `--tetapkan 6=lain-lain --tetapkan 7=beli-stok --ya`. Catat manual 21/09: jualan tunai 1,8 jt; belanja pasar 350rb; lain-lain: "biaya tarik tunai agen BRILink" 75rb (tidak dibelokkan ke `pindah` — benar, ini biaya), sumbangan 120rb, hadiah lomba (masuk) 50rb, "biaya adm OVO" 5rb (akun OVO), "ongkos pindah barang ke dapur baru" 40rb.

Verifikasi Decimal dari input:
| Besaran | Penguji | App |
|---|---:|---:|
| Laci = 750.000 +1.000.000 −500.000 +1.800.000 −350.000 −75.000 −120.000 +50.000 −40.000 | 2.515.000 | 2.515.000 ✅ |
| Mandiri (= saldo akhir file) | 8.879.487 | 8.879.487 ✅ |
| OVO = 150.000 − 5.000 | 145.000 | 145.000 ✅ |
| Hasil usaha = 4.251.234 − 1.461.747 | 2.789.487 | 2.789.487 ✅ |
| Naik total kas = hasil usaha (tanpa prive/modal) | 2.789.487 | 2.789.487 ✅ |

Kode ekspor: 5 biaya bank/e-wallet → `beban_keuangan`; bunga & hadiah → `pendapatan_lain`; "ongkos pindah barang" → `beban_lain`; sumbangan & pajak bunga → kosong (emkm: beban lain / PPh). emkm `--kas-akhir-aktual 11539487`: **laba 2.789.487 = hasil usaha, seimbang, selisih 0, selisih kas 0** ✅.
Pembanding: ekspor v1.0.1 (dari `git show 230da94`) atas DB yang sama → emkm laba **2.870.987**, neraca **TIDAK SEIMBANG −81.500** (semua "biaya tarik/adm/trf" dibaca pindah dana). Perbaikan terbukti.

## 3. Penanda 'Perlu dicek' per hari/minggu
- Bulanan (sebelum golongkan): "01/09-06/09: … hasil usaha Rp 2.342.500 [termasuk 'Perlu dicek' keluar Rp 1.000.000 - belum dihitung di hasil usaha]"; "07/09-13/09: … −Rp 250.000 [termasuk 'Perlu dicek' masuk Rp 3.000.000, keluar Rp 150.000 …]" — dicek tangan: 2.750.000 − 407.500 = 2.342.500 ✅.
- `rekap --minggu 07/09/2026` per hari: Sen 07/09 dan Sel 08/09 diberi penanda; Rab 09/09 (tanpa 'Perlu dicek') tanpa penanda ✅. Setelah `golongkan`, penanda hilang ✅.

## 4. Temuan
1. **[RENDAH-SEDANG] Keterangan lain-lain yang memuat kata non-beban emkm masih bisa menggeser laba.** Pada salinan DB, 5 catatan `--kategori lain-lain` tunai: "bayar utang toko Pak Joko", "belanja rumah", "beli kursi plastik", "uang muka karyawan Andi", "cicilan etalase". Kolom kategori ekspor kosong untuk semuanya (tidak cocok `POLA_RAWAN_EMKM`); emkm menggolongkan prive / piutang_lain / bayar_pinjaman → laba emkm **2.559.487** vs hasil usaha **2.149.487** (selisih 410.000), dan emkm menandai "Utang bank/pinjaman akhir negatif (−150.000)" (neraca `seimbang: false`). Tidak diam-diam: `catat` sudah memberi catatan "keperluan pribadi? … prive" untuk "belanja rumah", dan emkm mengajukan pertanyaan/anomali. Saran: tambahkan `utang|hutang|cicil\w*|angsuran|uang muka|kredit|keperluan rumah|belanja rumah` ke `POLA_RAWAN_EMKM` (atau isi `beban_lain` untuk semua lain-lain keluar yang tidak cocok pos beban rinci) + tes rantai.
2. **[RENDAH]** "BIAYA TRF BI-FAST" saat impor jatuh ke 'Perlu dicek' (aman), padahal pola ekspor sudah mengenalinya sebagai biaya bank; bisa ditebak lain-lain langsung.
3. Temuan lama **[RENDAH]** `golongkan` penjualan → modal tanpa peringatan: belum diubah (di luar cakupan v1.0.2).

## 5. Tanpa regresi
- `python3 tests/uji_regresi.py` → **68 tes OK** di repo; salinan scratchpad 68 OK (1 dilewati: kasir-lokal tidak disalin).
- DB uji lama (s01, s03) dibaca v1.0.1 dan v1.0.2: `rekap` Agustus & September **0 baris berbeda**; laundry Agustus **8.245.000**; ekspor emkm Agustus **identik byte-per-byte** dengan berkas uji v1.0.0 (tidak ada baris lain-lain); saldo s01 Laci 1.233.500 / BRI 4.830.000 / GoPay 225.000 sama.
- `python3 scripts/validate.py --skill kas-umkm` → ✅ valid.

**Skor: 9/10.**
