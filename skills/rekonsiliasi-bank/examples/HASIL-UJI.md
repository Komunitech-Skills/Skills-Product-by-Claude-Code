# HASIL UJI — rekonsiliasi-bank

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Folder kerja uji:** `/tmp/uji-rekonsiliasi-bank/` (data fiktif bergaya BCA, Mandiri, BRI)
- **Script dijalankan:** ya (`deteksi`, `cocokkan` JSON/teks/CSV, arah masuk & keluar, data rusak/tepi)
- **Verifikasi angka independen:** ya — `verif_bca.py` (parser terpisah) + hitung manual untuk Mandiri & BRI.

## Skor
| Kriteria | Skor (1–10) | Catatan |
|---|---:|---|
| Pemicu (description tepat) | 9 | Jelas, sebut bank-bank, sinonim ID/EN, batas "bukan rekap omzet" |
| Kemudahan awam | 8 | Konfirmasi kolom 1 pesan; boleh pakai tebakan bila pengguna minta cepat |
| Kualitas output | 7 | Format 4 kelompok + tindakan sangat baik; alasan script kadang menyesatkan (QRIS "bayar sebagian", arah keluar "bukan penjualan") |
| Akurasi (angka/fakta) | 5 | Total & selisih selalu benar; **pengelompokan salah** pada data realistis (lihat cacat berat) |
| Penanganan input kurang | 9 | Bertanya sekali, 5 pertanyaan, default disebut |
| Penanganan di luar cakupan | 9 | Tolak kredensial, arahkan ke unduh CSV & skill lain |
| Keamanan | 9 | Tanpa jaringan/subprocess/penghapusan file; hanya tulis `--output-csv`; masking ≥ 8 digit |
| **SKOR AKHIR** | **6** | Dibatasi cacat berat: pasangan salah (termasuk yang berlabel ✅ COCOK) mengubah tindakan pengguna |

**Status: REVISI**

## Cacat
### Berat
1. **Salah pasang karena nama diabaikan pada tahap awal** (`scripts/rekonsiliasi.py` fungsi `cocokkan`, tahap 1 baris 483–498 dan tahap 2a baris 503–513). Bukti: S1 — INV-106 Dewi dipasangkan ke transfer "HENDRA WIJAYA" Rp 1 jt (+6 hari), transfer Dewi Rp 993.500 jadi "tidak ada di catatan", INV-107 Hendra jadi "belum dibayar" (tagih 3 jt penuh, padahal sudah bayar 1 jt). S2 — transfer "FAJAR NUGROHO" diberi ✅ COCOK ke invoice **Yulia** (tanggal sama). Penjelasan selisih script (+3,6 jt − 1,66 jt + 0) berbeda dari yang benar (+0,6 jt − 0,66 jt + 2,0 jt); tanda "seimbang ✔" tetap muncul karena seimbang secara konstruksi.
   **Saran:** (a) buat fungsi `konflik_nama(c, b)` = keterangan bank memuat nama/ref catatan *lain* yang masih terbuka tetapi tidak memuat milik `c`; pada tahap 1 turunkan ke PARSIAL "nama berbeda", pada 2a lewati kandidat itu; (b) jalankan pasangan berpetunjuk nama (2d/2e dengan `petunjuk_teks`) **sebelum** 2a tanpa petunjuk; (c) di SKILL.md langkah 5 tambahkan: "periksa setiap COCOK/PARSIAL yang nama di catatan berbeda dengan nama di keterangan bank; laporkan sebagai 'kemungkinan tertukar'"; (d) ubah teks "seimbang ✔" agar tidak dibaca sebagai bukti pengelompokan benar.

### Sedang
2. **`petunjuk_teks` memakai substring** (baris 452–462): "andi" cocok dengan "ANDIKA" (S1: INV-112 ✅ COCOK "nama ada di keterangan" ke Andika Pratama); no. invoice numerik "105" cocok di dalam angka nominal "1050000.00" pada keterangan BCA → tahap 2e memberi PARSIAL "nama/no. invoice cocok" ke transfer orang lain Rp 1.050.000 untuk invoice Rp 300.000 (uji `noise-*.csv`). **Saran:** cocokkan per kata utuh (`\b`), ref numerik hanya bila dikelilingi non-digit dan ≥ 4 karakter atau berawalan huruf; abaikan deret angka yang sama dengan nominal.
3. **Tahap 2e tanpa batas nominal** (baris 567–579): nama cocok → PARSIAL berapa pun selisihnya (bank bisa 3,5× catatan). **Saran:** batasi `b.nominal <= c.nominal` (bayar sebagian) atau selisih ≤ 50%, sisanya biarkan tak cocok.
4. **`--toleransi-nominal` > 0 membuat `cek_rumus_seimbang` = false** (baris 647–655: selisih kelompok COCOK tidak ikut dijumlah). Uji BRI dengan `--toleransi-nominal 200` → false. **Saran:** jumlahkan selisih semua kelompok berpasangan (COCOK + PARSIAL), atau pindahkan pasangan beda nominal ke PARSIAL.
5. **Kolom header ganda** (mis. dua "Description" gaya Mandiri) — `baca_tabel` baris 267 menimpa kolom pertama; "BUNGA JASA GIRO" hilang sehingga bunga tidak dikenali. **Saran:** ganti nama duplikat jadi "Description_2" dan izinkan `--bank-keterangan` beberapa kolom (digabung).
6. **Teks alasan tidak mengikuti `--arah keluar`** (baris 564–565, 581–590): "bukan penjualan", "pemasukan lain", "potongan biaya transfer". **Saran:** kamus alasan per arah.

### Ringan
7. PEND digabung dengan baris ringkasan saldo di `dilewati` (baris 377) padahal checklist meminta PEND disampaikan — hitung terpisah dan tampilkan keterangan PEND (disamarkan) sebagai "tertunda, cek periode berikut".
8. `deteksi` memetakan "nominal" ke `SALDO_AKHIR_MUTASI` pada format BRI dan tidak mengenali "Supplier/Vendor/Pemasok" sebagai kolom nama (`KATA_CATAT["nama"]`).
9. Masking hanya deret ≥ 8 digit berurutan; nomor bertanda hubung ("0021-01-000123-50-9") atau berspasi tidak disamarkan. Tambah pola `(\d[\s-]?){8,}`.
10. Alasan PARSIAL untuk settlement QRIS berbunyi "kemungkinan baru bayar sebagian"; kenali kata "QRIS/SETTLEMENT/EDC/MDR" → "dipotong biaya merchant".
11. SKILL.md bagian privasi: tambahkan "bila pengguna sudah menempel PIN/password, sarankan segera ganti".

## Yang sudah bagus
- Parser tangguh: baris info rekening, `'02/09` + tahun dari "Periode", kolom CR/DB tanpa judul, PEND, ringkasan saldo, `1,500,000.00` / `1.500.000,00` / `Rp 1.500.000` / `"1.750.000,50"`, file kosong, .xlsx, kolom hilang, nominal 0/kosong → pesan error JSON yang jelas.
- Gabungan (2 invoice 1 transfer) dan terpecah (1 invoice 2 transfer) terdeteksi benar di BCA & BRI; potong biaya terdeteksi bila tidak didahului tahap 2a.
- Totals & selisih semua skenario cocok dengan verifikasi independen.
- Uji A/B: lebih baik dari agent tanpa skill secara keseluruhan (angka total benar, tunai/PEND ditangani, privasi); banding pesaing: menang atas PythonMuse `bank-reconciliation`.
