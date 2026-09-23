# HASIL UJI — rekonsiliasi-bank v1.1.0 (uji ulang)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi diuji:** v1.1.0 (commit `8d7f613`). Uji sebelumnya: v1.0.0, skor 6, REVISI.
- **Folder kerja uji:** `/tmp/uji-rekonsiliasi-bank/`. Data fiktif bergaya BCA, Mandiri, dan BRI, ditambah data berisik baru.
- **Script dijalankan:** ya.
  - Skenario: S1 BCA, S2 Mandiri (1 dan 2 kolom keterangan), BRI masuk + `--toleransi-nominal 200`, BRI keluar.
  - Data berisik: ref numerik "105", nama mirip, nominal sama beda orang, gabungan, termin 3×.
  - Kasus tepi: file kosong, .xlsx, nominal 0/kosong, masking nomor bertanda hubung.
- **Verifikasi independen:** ya. `verif_bca.py` (parser terpisah) dan `verif_v110.py` (kunci jawaban pasangan + rincian selisih):
  - S1: 11/11 pasangan benar, rincian **+Rp 600.000 − Rp 662.346 + Rp 2.006.500 = Rp 1.944.154** ✔
  - S2: 8/8 pasangan benar, rincian +1.750.001 − 8.123 + 12.350 ✔
  - BRI keluar: rincian +1.350.000 − 1.005.500 + 6.500 ✔
  - Data berisik: 5/9 pasangan sesuai kunci (lihat `06-data-berisik-nama-mirip.md`)
- **Audit keamanan:** hanya library standar. Tidak ada jaringan atau subprocess. Satu-satunya file yang ditulis adalah `--output-csv`, dan masking nomor rekening kini juga menangani format bertanda hubung/spasi.

## Status perbaikan cacat v1.0.0
| # | Cacat v1.0.0 | Status v1.1.0 |
|---|---|---|
| 1 (berat) | Salah pasang karena nama diabaikan (Dewi↔Hendra, Fajar↔Yulia) | ✅ Diperbaiki. Pencocokan berpetunjuk nama didahulukan, ada `konflik()`, dan label KEMUNGKINAN TERTUKAR |
| 2 | Substring nama ("andi"→"ANDIKA"), ref "105" di dalam nominal | ✅ Diperbaiki (kata utuh, ref angka ≥ 4 digit) |
| 3 | Tahap 2e tanpa batas nominal | ✅ Diperbaiki (bank ≤ catatan atau selisih ≤ 50%) |
| 4 | `--toleransi-nominal` membuat tidak seimbang | ✅ Diperbaiki (`dari_selisih_dalam_toleransi_cocok`) |
| 5 | Header ganda saling menimpa | ✅ Diperbaiki (`Description_2`, `--bank-keterangan` bisa diulang). Lihat sisa #B |
| 6 | Alasan tidak mengikuti `--arah` | ✅ Diperbaiki |
| 7–11 (ringan) | PEND digabung; deteksi saldo/Supplier; masking bertanda hubung; alasan QRIS; "ganti PIN" | ✅ PEND terpisah; deteksi saldo & Supplier; masking; alasan QRIS. (#11 tidak dicek ulang) |

## Skor
| Kriteria | Skor (1–10) | Catatan |
|---|---:|---|
| Pemicu (description tepat) | 9 | Tetap tepat |
| Kemudahan awam | 8 | Konfirmasi kolom 1 pesan. Untuk file kolom ganda, agent harus tahu menambahkan `Description_2` |
| Kualitas output | 8 | Alasan per arah/QRIS sudah tepat; peringatan "seimbang ≠ semua pasangan benar" |
| Akurasi (angka/fakta) | 7 | Total & selisih selalu benar. S1/S2/BRI pasangan benar. Masih ada kasus nama depan sama yang tertukar |
| Penanganan input kurang | 9 | Tidak berubah (contoh 04) |
| Penanganan di luar cakupan | 9 | Tidak berubah (contoh 05) |
| Keamanan | 9 | Tetap aman; masking diperluas |
| **SKOR AKHIR** | **7** | |

**Status: LULUS (7).** Batas bawah kelulusan. Cacat sedang di bawah sebaiknya diperbaiki sebelum rilis ke pembeli.

- Uji A/B ulang: skill sekarang **jelas lebih baik** (`00-pembanding-tanpa-skill.md`).
- Banding pesaing: tetap menang (`00-banding-pesaing.md`).

## Cacat tersisa
### Berat
- Tidak ada. Pada data S1/S2/BRI semua pasangan benar.

### Sedang
A. **Nama depan sama → pasangan tertukar berlabel ✅ COCOK "nama ada di keterangan bank"** (`scripts/rekonsiliasi.py` `cocok_nama` baris 524–530, tahap 0 baris 588–598).
   - Bukti di `06`: invoice Andi Wijaya ↔ transfer ANDI SAPUTRA, dan sebaliknya.
   - Varian `andi-cat2.csv`: hanya ANDI SAPUTRA yang transfer, tetapi invoice Andi Wijaya yang ✅ COCOK, sementara Andi Saputra tercatat "belum dibayar". Akibatnya orang yang salah bisa ditagih.
   - Saran: beri skor kecocokan = jumlah kata nama yang cocok (atau proporsinya), dan urutkan kandidat tahap 0 (serta 2b–2e) berdasarkan skor tertinggi dulu.
   - Saran: bila ada catatan lain dengan skor lebih tinggi untuk transaksi bank yang sama, perlakukan sebagai `konflik()`. Bila hanya sebagian kata yang cocok dan ada kata lain yang berbeda, turunkan ke PARSIAL "nama sebagian cocok".
B. **`deteksi` tidak menyarankan `Description_2`** sebagai kolom keterangan kedua pada file bergaya Mandiri (hanya "Description", yang isinya "TRANSFER DARI").
   - Agent yang mengikuti saran deteksi mendapat rincian yang salah (+2,75 jt −0,996 jt +0), QRIS tidak terpasang, dan 4 COCOK "nama tidak terlihat".
   - Saran: di `cmd_deteksi`, masukkan semua kolom dengan kata kunci keterangan (termasuk akhiran `_2`) ke `kolom_terdeteksi["keterangan"]` sebagai daftar. Bila isi kolom pertama nyaris seragam ("TRANSFER DARI"), sarankan kolom lain.
C. **"Nama tidak terlihat" tetap berstatus COCOK dan ikut dihitung di baris ✅** (tahap 1, baris 600–610). Contoh: S1 INV-113 ↔ ANDIKA, `06` Rudi ↔ SURYA KENCANA.
   - SKILL.md langkah 5 melarang memberi ✅ untuk pasangan seperti ini, tetapi angka ringkasan `per_status.COCOK` tetap memasukkannya, sehingga tabel ✅ tidak konsisten dengan daftar yang pasti.
   - Saran: bila catatan punya nama dan keterangan bank memuat nama orang (ada kata huruf ≥ 3 selain kata umum/perbankan) yang tidak cocok, masukkan ke PARSIAL "pengirim berbeda — cek". Pertahankan COCOK hanya bila keterangan memang tidak memuat nama (mis. "SETORAN", "QRIS").

### Ringan
D. Nama yang seluruhnya kata umum ("CV Maju Jaya") dianggap cocok dengan "PT JAYA MAJU MOTOR" (`kata_nama_umum`, baris 498–500). Pertimbangkan membedakan CV/PT atau mensyaratkan urutan kata yang sama.
E. Kombinasi cicilan untuk transaksi yang namanya cocok (tahap 2c) hanya memakai jendela `--maks-hari-parsial` (14 hari), bukan `--maks-hari-nama` (31 hari). Contoh: cicilan ke-3 Bambang (hari ke-15) tidak terkumpul. Saran: pakai `maks_nama` bila semua transfer dalam kombinasi berpetunjuk nama.
F. COCOK dalam toleransi nominal (`--toleransi-nominal 200`) beralasan "nominal sama" padahal beda Rp 100. Sebutkan "beda Rp 100 (dalam toleransi)".

## Yang sudah bagus
- Parser tetap tangguh untuk BCA/Mandiri/BRI, PEND dilaporkan terpisah, dan kesalahan input dijelaskan dengan pesan yang jelas.
- Nama kata utuh bekerja: Heru ≠ Hermawan, Andi ≠ ANDIKA, ref "105" tidak cocok ke nominal 1.050.000.
- Pembayaran gabungan, termin, potong biaya, bayar sebagian, dan telat bayar (sampai 31 hari bila nama cocok) terdeteksi dengan benar.
- Rincian selisih kini mencakup selisih dalam toleransi, dan `catatan_seimbang` mencegah salah tafsir "seimbang ✔".
