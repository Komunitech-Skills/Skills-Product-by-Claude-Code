# Hasil Uji Ulang — laporan-keuangan-emkm v1.2.0 (kandidat VIP)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** `scripts/laporan_emkm.py` **v1.2.0** (`VERSI = "1.2.0"`), SKILL.md, README.md, ATTRIBUTION.md, `references/`, `templates/`, `scripts/uji_regresi.py`
- **Riwayat:** v1.0.0 skor 6 (B1 + S1–S5). v1.1.0 skor 6 (B1 lama beres, muncul cacat berat BB1 + sedang BS1–BS3).
- **Metode:** data & verifikator independen dari uji v1.1.0 dipakai ulang (`/tmp/uji-laporan-keuangan-emkm/v110/` → `v120/`). Konveksi 6 bulan (63 transaksi) dicek per bulan dengan `verif_6bln.py` (ledger akrual bulanan buatan penguji, tanpa kode skill). Ada dua data baru dengan verifikator sendiri: toko bangunan dengan piutang & bon pemasok besar lintas bulan (`verif_toko.py`), dan kafe dengan PB1 dipungut terpisah & disetor bulan berikutnya. Skenario 04 (input kurang) dan 05 (di luar cakupan) tidak memakai script, jadi tetap berlaku. A/B dan banding pesaing dipertahankan dan diberi catatan pembaruan.

## Audit keamanan
Diff v1.1.0 → v1.2.0 hanya menambah logika hitung, opsi CLI, dan kategori `titipan_pajak`. Tidak ada impor baru, akses jaringan, subprocess, eval/exec, atau tulis file (output tetap ke stdout). `uji_regresi.py` hanya menjalankan script skill sendiri pada file sementara. SKILL.md/references tidak mengandung prompt injection. **Aman.**

## Status cacat v1.1.0
| Cacat | Uji ulang v1.2.0 | Status |
|---|---|---|
| **BB1** piutang/utang pemasok tidak bergulir → pendapatan/HPP ganda | Konveksi: **April −1.695.167 ✔, Juni −1.766.667 ✔**. Semua 11 pos (kas, piutang, kasbon, stok, aset tetap, utang pemasok, utang KUR, modal awal, laba, modal akhir, penyusutan) cocok dengan penguji di **setiap bulan**. Modal akhir N = modal awal N+1 di kelima sambungan. **Σ laba bulanan = −1.996.002 = laporan Jan–Jun**. Toko bangunan (piutang 8→9→12→2 jt, bon 5→8→7→0 jt): 3 bulan cocok, Σ = triwulan 2.730.000. Tanpa `--piutang-awal-periode`/`--utang-usaha-awal-periode`, script **SEMENTARA + pertanyaan eksplisit** (tidak lagi salah diam-diam) (06, 08) | **Tuntas** |
| **BS1** penyusutan dari nilai buku | Kini per bulan dari harga beli: Feb 216.667, Mei–Jun 291.667 ✔. Pembulatan per bulan (total 6 bulan 1.400.002) konsisten di laporan bulanan & gabungan | Tuntas |
| **BS2** kas minus tidak bisa dikonfirmasi | `--abaikan-kas-minus` → status LENGKAP (dengan asumsi), konfirmasi tertulis di Asumsi (02) | Tuntas |
| **BS3** pertanyaan PB1 tak bisa ditutup; tidak ada titipan | `--tetapkan` menutup pertanyaan (07). Kategori `titipan_pajak` bekerja: PB1 tidak masuk pendapatan/beban, muncul sebagai utang pajak daerah (09) | Tuntas, tetapi ada celah saldo awal (lihat S-1) |
| Ringan v1.1.0 (tanggal awal data, peringatan stok, tampilan kas/bank, kasbon di mode awal-periode) | Semua diperbaiki. Mode `awal-periode` kini tetap menggulir pos yang tidak diisi (kasbon April benar) | Tuntas |

## Verifikasi angka (independen)
| Uji | Hasil |
|---|---|
| Konveksi 6 laporan bulanan (11 pos × 6 bulan) | **66/66 cocok**. Neraca seimbang tiap bulan, modal bersambung, Σ laba = laporan 6 bulan |
| Konveksi Jan–Jun sekaligus | laba −1.996.002; kas 9.574.000; utang KUR 13.170.000; modal 14.503.998 ✔ |
| B1 data lama, Februari | kas akhir 22.408.250 ✔ (+ pertanyaan piutang/bon per 1 Feb) |
| Toko bangunan Jul/Agu/Sep + triwulan | pendapatan 20,3/19,3/9,0 jt; HPP 13/12/4 jt; laba 1.700.000/1.650.000/−620.000; kas, piutang, bon, modal cocok ✔ |
| S1 katering (bunga KUR, kasbon) | laba −2.026.917; A = L+E = 37.939.750 ✔ (identik v1.1.0) |
| Warung sembako + selisih kas + `--abaikan-kas-minus` | laba 6.100.000; A = L+E = 10.650.000 ✔; LENGKAP (dengan asumsi) |
| Warung makan (PB1 ditanggung sendiri, gas, air, `(200.000)`) | laba 5.985.000; kas 8.685.000 ✔; LENGKAP (dengan asumsi) |
| Kafe PB1 titipan | laba Jul 5.500.000 / Agu 2.000.000 ✔; kas ✔; **utang PB1 salah** (Jul Rp 0 vs benar 1.500.000; Agu −300.000 vs 1.200.000) karena saldo awal titipan tidak bisa diisi |
| Sambal online (Jumlah+Jenis) | laba 13.335.000; kas 14.435.000 ✔ |
| Data rusak/tepi (`Rp 1.500.000`, `1.500.000,50`, `1,5jt`, `150rb`, `15.000,-`, `0`, `abc`, `1.250.000.50`, masuk+keluar terisi, TOTAL, file kosong/header saja/tanpa kolom/`.xlsx`/Debit-Kredit, nominal opsi baru `abc`) | Semua benar / `GALAT:` berbahasa Indonesia ✔ |
| `scripts/uji_regresi.py` | **SEMUA UJI LULUS** (56 cek) |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Tidak berubah. Kata kunci awam + Inggris, batas dengan skill lain jelas. |
| Kemudahan awam | 8 | Pertanyaan piutang/bon per awal bulan muncul otomatis, dan semua status SEMENTARA kini bisa ditutup. Pertanyaan PB1 masih per baris (bisa belasan) dan harus dirangkum agent. |
| Kualitas output | 8 | SAK EMKM lengkap, laporan bulanan bersambung, utang pajak daerah tampil di neraca. Belum ada pemisahan lancar/tidak lancar dan jadwal penyusutan per aset di CaLK. |
| Akurasi (angka/fakta) | 8 | Semua laba, kas, piutang, utang, aset, dan modal cocok sampai rupiah di 6 data uji, termasuk laporan bulanan lintas bulan. Satu celah: saldo awal titipan PB1 tidak bisa diisi (neraca, bukan laba). |
| Penanganan input kurang | 9 | Tanya sekali, default + asumsi tertulis (04). Saldo per awal periode yang kurang otomatis masuk "Pertanyaan untuk pemilik". |
| Penanganan di luar cakupan | 9 | Audit/SAK EP/konsolidasi/SPT diarahkan dengan benar (05). |
| Keamanan | 10 | Lokal, tanpa jaringan, tanpa tulis file. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Cacat berat BB1 dan ketiga cacat sedang v1.1.0 tuntas dan terbukti dengan verifikasi independen. Untuk data konveksi 6 bulan, 66 dari 66 pos bulanan cocok, modal bersambung, dan Σ laba bulanan sama dengan laporan 6 bulan. Data baru toko bangunan dengan piutang besar lintas bulan juga cocok persis. Bila saldo per awal bulan belum diisi, script kini **bertanya**, tidak lagi menebak diam-diam. Skill jelas lebih baik daripada agent tanpa skill dan tetap menang atas pesaing.

Satu cacat sedang tersisa di fitur baru `titipan_pajak`. PB1 yang dipungut bulan lalu tidak punya isian saldo awal. Karena PB1 disetor bulan berikutnya, laporan pertama kafe mencatat utang PB1 terlalu kecil (laba tetap benar). Laporan bulan kedua terkunci SEMENTARA dengan saran perbaikan yang menyesatkan. Tidak ada cacat berat. Disarankan memperbaiki S-1 sebelum status `rilis` (perbaikannya kecil).

## Daftar cacat & saran perbaikan (v1.2.0)

### Berat
- Tidak ada.

### Sedang
- **S-1 — Saldo awal titipan PB1/PBJT tidak bisa diisi, dan saran anomali menyesatkan** (`hitung()`: `titipan_pajak_awal = 0` hanya diisi dari transaksi sebelum periode; teks `saran["Titipan"]`). Bukti (09): PB1 Juni Rp 1,5 jt disetor 10 Juli. Neraca 31 Juli: utang PB1 Rp 0 (benar Rp 1.500.000) dan modal awal Rp 5.000.000 (benar Rp 3.500.000), tetap LENGKAP. Agustus: utang PB1 −Rp 300.000 → SEMENTARA, dengan saran "catat penyetorannya sebagai beban_pajak_lain". Kalau saran itu diikuti, laba turun Rp 1,5 jt secara keliru.
  *Saran:* tambah `--titipan-pajak-awal` (digulir seperti kasbon; dipakai apa adanya di mode `awal-periode`). Masukkan ke "Pertanyaan untuk pemilik" bila ada baris `titipan_pajak` keluar sebelum ada pemungutan di periode itu. Ubah `saran["Titipan"]` menjadi "Apakah ada PB1 bulan lalu yang belum disetor per <awal periode>? Isi --titipan-pajak-awal". Sebutkan saldo ini di tabel Input SKILL.md dan tambahkan uji regresi "PB1 disetor bulan berikutnya".

### Ringan
- Pertanyaan PB1 muncul per baris (kafe: 12 pertanyaan untuk 18 transaksi), termasuk baris penjualan yang hanya menyebut "(belum termasuk PB1)". Baris "PB1 10% dipungut dari pembeli" otomatis terbaca sebagai penjualan (kata `pembeli`) sampai ditetapkan. *Saran:* satukan menjadi satu pertanyaan dengan daftar nomor baris. Kecualikan frasa "belum/tidak termasuk PB1". Baris masuk yang diawali "PB1/pajak restoran" sebaiknya tidak diklasifikasi sebagai penjualan.
- Mode `--saldo-awal-per awal-periode` dengan `--aset-tetap-awal` = nilai buku per awal periode: penyusutan dihitung dari nilai buku itu dengan `--umur-aset-tahun` penuh. Hasilnya benar bila umur yang diberikan adalah **sisa** umur, tetapi SKILL.md tidak menjelaskannya. Pada uji "rantai", penyusutan bulanan meleset 2.778–17.935 per bulan. *Saran:* satu kalimat di SKILL.md: "di mode awal-periode, isi --umur-aset-tahun dengan sisa umur", atau sarankan mode awal-file untuk laporan berurutan (yang sudah tepat).
- Belum diadopsi dari pesaing: aset/liabilitas lancar vs tidak lancar dan jadwal penyusutan per aset di CaLK.

## Contoh yang diperbarui / ditambah
- `01`, `03`: output diperbarui ke v1.2.0 (angka identik).
- `02`: `--abaikan-kas-minus` → LENGKAP (dengan asumsi).
- `06`: ditulis ulang untuk v1.2.0: alur pertanyaan piutang/bon per awal bulan, laporan April, tabel 11 pos × 6 bulan.
- `07`: PB1 ditutup dengan `--tetapkan 8=beban_pajak_lain` → LENGKAP (dengan asumsi).
- **Baru** `08-toko-bangunan-piutang-lintas-bulan.md` (data baru, piutang besar lintas bulan).
- **Baru** `09-kafe-pb1-titipan-lintas-bulan.md` (data baru, PB1 dipungut terpisah; bukti S-1).
- `04`, `05`: tetap. `00-pembanding-tanpa-skill.md` & `00-banding-pesaing.md`: dipertahankan + catatan v1.2.0. **A/B: skill jelas lebih baik. Pesaing: skill kita menang.**
