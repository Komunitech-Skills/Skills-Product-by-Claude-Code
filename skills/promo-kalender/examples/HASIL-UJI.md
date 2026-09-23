# HASIL UJI — promo-kalender

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Folder kerja uji:** `/tmp/uji-promo-kalender/`

## Ringkasan pengujian
| Uji | Hasil |
|---|---|
| Audit keamanan | `cek_promo.py` hanya library standar (argparse, csv, io, json, re, sys, datetime, decimal). Tidak ada jaringan, subprocess, tulis/hapus file, atau kredensial. Tidak ada prompt injection. ✅ |
| Verifikasi independen margin | Kalkulator terpisah (pecahan eksak) untuk **300 kombinasi acak**: diskon %, harga promo, potongan Rp, bundling, beli-gratis, voucher Rp & % (cap + min. belanja), subsidi ongkir, cashback, biaya lain/hadiah, biaya platform 0–15%, biaya per pesanan. Laba/unit, margin, harga impas, **diskon maksimal sebelum rugi**, status RUGI/TIPIS/AMAN → **cocok 300/300** ✅ |
| Pembulatan | Harga dari diskon % dibulatkan ke atas ke Rp 100 (Rp 66.750 → 66.800) ✓; klaim % dibulatkan ke bawah (24,9% → "hemat 24%") ✓; diskon maks dibulatkan ke bawah, impas ke atas ✓ |
| Tanggal & nama hari | 11.11, 12.12, 9.9, 10.10, gajian, Lebaran perkiraan: semua tanggal & nama hari dicek dengan `datetime` ✓. Tahun bergulir benar (9.9 dari 23 Sep 2026 → 9 Sep 2027) ✓ |
| Data rusak/tepi | `Rp 1.500.000`, `1.500.000,50`, `1.5jt`, `89.000,-`, `1,500,000` ✓; `abc`, negatif, harga 0, diskon 100, harga promo > normal, dua mekanisme sekaligus, config kosong → `ERROR` kode 2 ✓; HPP ≥ harga → RUGI + peringatan ✓; voucher di bawah min. belanja → peringatan ✓; voucher > harga (dibayar Rp 0) tidak crash ✓. **`1,250` dibaca 1,25** tanpa peringatan ⚠️ |
| S1–S5 | Lihat file 01–05 |
| Uji A/B | Skill jelas lebih baik |
| Banding pesaing | Menang telak vs `discount-marketing-strategy` (kostja94, MIT) |

## Skor
| Kriteria | Skor (1–10) | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Momen Indonesia lengkap; batas dengan skill konten/harga jelas |
| Kemudahan awam | 8 | Bahasa sederhana; konsep "unit normal sepanjang periode promo" dan periode multi-hari masih perlu penjelasan agent |
| Kualitas output | 9 | Rencana 7 bagian siap pakai, S&K jujur |
| Akurasi (angka/fakta) | 9 | 300/300 cocok; tanggal benar; regulasi berlabel & bersumber |
| Penanganan input kurang | 9 | Maks. 5 pertanyaan, jalur cepat dengan default |
| Penanganan di luar cakupan | 9 | Harga coret palsu, hitung mundur palsu, undian: ditolak dengan dasar hukum; konten harian diarahkan |
| Keamanan | 10 | Tidak ada risiko teknis |

## SKOR AKHIR: **8 / 10 — LULUS**
Hitungan akurat dan terverifikasi, konteks Indonesia kuat. Tidak ada cacat berat. Beberapa kekurangan kecil di penjadwalan dan label.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Label "diskon maksimal agar tidak rugi" ambigu saat ada voucher.** Di `analisis_produk`, harga impas dihitung sebagai harga **dibayar pembeli** (sudah termasuk voucher). Contoh: diskon 10% + voucher Rp 20.000 → "diskon maksimal 33,5%". Pengguna bisa mengira masih boleh diskon 33% **ditambah** voucher, padahal itu rugi. **Perbaikan:** di `cetak_margin`, bila `voucher` ≠ 0 tulis "…diskon maksimal **total (termasuk voucher)**: X%". Tambahkan juga "diskon % maksimal bila voucher tetap berjalan" = 1 − (impas + voucher/qty)/harga normal.
2. **Jadwal tidak memadatkan fase walau tertulis begitu.** `buat_jadwal`: catatan "Sisa waktu hanya N hari: fase yang sudah lewat **dipadatkan**…" padahal script hanya menandai "(sudah lewat)". Untuk `--momen gajian`, tanggal 2 hari lagi tetap dipilih. **Perbaikan:** ubah teks menjadi "…agent perlu memadatkan/menggeser fase", atau benar-benar geser fase lewat ke `dari`..H-1. Untuk gajian, bila sisa < 7 hari, pilih bulan berikutnya dan sebut opsi "versi kilat".

### Ringan
3. `parse_angka("1,250")` → 1,25 (koma dianggap desimal). Pengguna yang menulis ribuan gaya Inggris untuk biaya per pesanan mendapat Rp 1,25 tanpa peringatan. Tambahkan peringatan bila bagian setelah koma tepat 3 digit dan tanpa titik ("1,250 dibaca 1,25; maksud Anda 1.250?").
4. `--config` berisi banyak **opsi** untuk produk yang sama → "Ringkasan kampanye" menjumlahkan semua opsi (mis. "total target 519 unit"). Tambahkan kolom/flag `"opsi": true` atau tulis di SKILL.md langkah 3: "bandingkan opsi dengan run terpisah; config ringkasan hanya untuk rencana final".
5. Jadwal hanya mengenal satu hari H. Promo 3 hari (10–12 Nov) harus disesuaikan manual. Tambah `--sampai YYYY-MM-DD` agar fase "HARI H" menjadi rentang.
6. SKILL.md tabel Input, baris "Penjualan normal per periode": tambahkan "(periode sama panjang dengan promo; mis. 80/bulan → 8 untuk promo 3 hari)". Script `--unit-normal` sudah benar tapi pengguna awam memberi angka bulanan.
7. Pola Lebaran fase H-14 berlabel "THR mulai cair", padahal aturan yang dikutip menyebut paling lambat H-7. Ganti menjadi "THR mulai cair (umumnya paling lambat H-7)".

## Verifikasi angka script
**Ya.** `/tmp/uji-promo-kalender/indep.py` (300 kasus acak, pecahan eksak) cocok 100%. Semua angka di contoh 01–03 & 05 dicek manual. Nama hari dicek dengan `datetime`.
