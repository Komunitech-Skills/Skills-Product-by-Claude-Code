# HASIL UJI — analisis-ulasan

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Folder kerja uji:** `/tmp/uji-analisis-ulasan/` (data fiktif; tidak ada data pribadi asli)

## Ringkasan pengujian
| Uji | Hasil |
|---|---|
| Audit keamanan | Script hanya memakai library standar (argparse, csv, io, json, re, sys, collections). Tidak ada jaringan, subprocess, penghapusan file, atau pembacaan kredensial. Tidak ada prompt injection di SKILL/README/references. ✅ |
| S1 CSV 160 ulasan (gaul, sarkasme, negasi, campur bintang, PII) | Sebaran & rata-rata **cocok 100%** dengan hitungan python independen (81/27/22/12/18; 3,8813). Tema: dibandingkan dengan label ground truth penguji |
| S2 kafe Google Maps (teks) | Kamus bawaan melewatkan keluhan khas kafe; berhasil diperbaiki dengan `--kamus-tambahan` |
| S3 malas, format ⭐ | Format terbaca, ide konten bagus |
| S4 tanpa data | Bertanya sekali, daftar singkat ✅ |
| S5 ulasan palsu + balas 1 ulasan | Ditolak & diarahkan ke `balas-ulasan-pelanggan` ✅ (penolakan ulasan palsu belum tertulis di SKILL.md) |
| Data rusak/tepi | File kosong, hanya header, kolom tak dikenal, file tidak ada → `ERROR` + kode 2 ✅. Bintang `0`, `4,5`, `★★★★★★` → diabaikan & dilaporkan ✅. `Rp 1.500.000` di teks → kutipan terpotong "000 worth it" ⚠️ |
| Uji A/B | Skill jelas lebih baik (lihat `00-pembanding-tanpa-skill.md`) |
| Banding pesaing | Menang vs `review-objection-miner-ecommerce` (MIT) |

### Akurasi tema S1 (script mentah vs ground truth penguji)
| Tema | Ground truth | Script | Catatan |
|---|---|---|---|
| k_pengiriman | 15 | 13 | kurang 2: sarkasme & "resi ga gerak2" |
| **k_respons** | **8** | **14** | **+6 false positive: "pesanan diproses lama" terbaca sebagai chat** |
| k_kualitas | 11 | 9 | "resleting macet", "ga sebanding kualitas" |
| k_salah_kirim | 10 | 9 | sarkasme "pesen hitam dikirim putih" |
| k_tidak_sesuai | 8 | 8 | ✅ |
| k_ukuran | 8 | 6 | "size L kayak M", ulasan Sunda |
| k_kemasan | 5 | 4 | "kurir lempar paket" |
| k_rasa | 0 | 1 | "baunya apek" (kata "apek" ada di k_rasa) |
| p_* (8 tema) | – | selisih 0–5 | p_kualitas 22 vs 27 ("tebel", bahasa Inggris, negasi "ga terlalu tipis") |

Peringkat prioritas mentah dari script: **Respons (52) > Pengiriman (49)**. Yang benar: Pengiriman (59) > Salah kirim (40) > Kualitas (39) > Respons (34). Setelah langkah verifikasi SKILL.md dijalankan, laporan akhir benar.

## Skor
| Kriteria | Skor (1–10) | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Jelas, dwibahasa, batas dengan `balas-ulasan-pelanggan` tegas |
| Kemudahan awam | 8 | Format tempel sederhana, README jelas; menambah tema butuh regex (tugas agent, bukan pengguna) |
| Kualitas output | 9 | Laporan 7 bagian siap rapat: prioritas + ukuran keberhasilan, ide konten |
| Akurasi (angka/fakta) | 7 | Statistik bintang tepat. Kandidat tema punya bug regex yang membalik prioritas #1 bila verifikasi dilewati. Kamus lemah untuk kafe/resto |
| Penanganan input kurang | 9 | Bertanya sekali, contoh format jelas |
| Penanganan di luar cakupan | 8 | Rujukan skill lain jelas; kasus ulasan palsu belum tertulis |
| Keamanan (termasuk privasi) | 7 | Aman secara teknis. Masking baik, tapi ada celah: potongan email & nama di `kata_teratas` |

## SKOR AKHIR: **7 / 10 — LULUS (dengan revisi disarankan)**
Nilai tambah nyata dibanding agent tanpa skill, dan menang atas pesaing. Skor ditahan di 7 karena kandidat tema bisa salah arah bila agent tidak disiplin, dan ada celah privasi kecil.

## Daftar cacat & saran perbaikan

### Berat
- (tidak ada yang dinilai berat, karena langkah verifikasi wajib di SKILL.md menangkap kesalahan tema di S1. Namun cacat sedang #1 **hampir berat**: harus diperbaiki sebelum rilis berikutnya.)

### Sedang
1. **False positive `k_respons` pada kata "pesanan".** `scripts/olah_ulasan.py`, tema `k_respons`, pola `r"\b(?:chat|pesan)\w*" + DEKAT + r"(?:…|lama|…)"`: `pesan\w*` ikut menangkap "pesanan/pesenan" ("pesanan diproses lama" → respons admin). **Perbaikan:** ganti jadi `r"\b(?:chat|pesan(?!an)|pesen(?!an))\w*…"` atau daftar eksplisit `(?:chat|pesan|pesannya|dm|inbox)`. Tambah tes regresi "pesanan diproses lama, 5 hari baru dikirim" yang hanya boleh masuk `k_pengiriman`. Hal serupa: "pelayanannya lama" (kafe) sebaiknya masuk tema waktu layanan, bukan hilang.
2. **Kamus tambahan tidak bisa mengecualikan.** `muat_kamus_tambahan` hanya menambah pola. Agent tidak punya cara menghitung ulang lewat script setelah menemukan false positive, sehingga bertentangan dengan checklist "semua angka dari script". **Perbaikan:** dukung `"kecualikan": ["regex"]` per tema (klausa yang cocok pola kecualikan tidak dihitung), atau opsi `--abaikan-id tema:3,14,16`. Tulis caranya di SKILL.md langkah 3.
3. **Kebocoran sebagian email & nama.** Kalimat dipecah di titik **sebelum** disamarkan (`pecah_klausa` lalu `samarkan`), sehingga `siti.rahma@gmail.com` menjadi kutipan "…email siti" (uji: `klausa_cocok`/`contoh`). Selain itu `kata_teratas` dihitung dari teks yang tidak disamarkan, jadi nama ("siti", "budi", "rina") bisa muncul. **Perbaikan:** jalankan `samarkan()` pada teks utuh sebelum `pecah_klausa()` di `analisis()`, dan hitung `kata_teratas` dari teks yang sudah disamarkan (atau buang token yang berasal dari email/@akun).
4. **Kamus tidak cocok untuk kafe/resto/jasa, padahal dijanjikan di README** ("Pemilik kafe, resto, salon, atau klinik… Google Maps"). Waktu tunggu, kebersihan/benda asing, parkir, toilet dan suasana tidak dikenali. Keluhan keamanan pangan "nemu rambut di pastry" tidak terdeteksi sama sekali. **Perbaikan:** tambah tema bawaan `k_waktu_tunggu`, `k_kebersihan` (rambut/serangga/kotor → masuk aturan "Segera" keamanan), `k_fasilitas`, `p_suasana`, atau sediakan `templates/kamus-kuliner-jasa.json` dan sebut di SKILL.md bagian Input/Langkah 2.

### Ringan
5. Negasi pujian terbaca keluhan: "ga terlalu manis" → `tidak_manis` → `k_rasa`. Di `k_rasa`, hapus `manis` dari `(?:tidak|kurang)_(…)` atau kecualikan bila didahului "terlalu".
6. "bau apek" masuk `k_rasa` karena `apek` ada di pola rasa. Hapus `apek` dari `k_rasa` (sudah ada di `k_bau`).
7. Pemecah klausa memotong angka ribuan: "harga Rp 1.500.000 worth it" → kutipan "000 worth it". Di `pecah_klausa`, pecah di titik hanya bila diikuti spasi/akhir (`\.(?=\s|$)`), bukan di antara angka.
8. Slang kurang: `tebel`→tebal, `ketagihan`→nagih, `dateng`→datang, `nunggu`→tunggu, bahasa Inggris dasar (`good quality`, `fast delivery`, `will buy again`).
9. Warna beda di klausa terpisah koma ("ga sesuai deskripsi, warnanya beda") terhitung ganda (`k_tidak_sesuai` + `k_salah_kirim`). Terapkan PRESEDEN per kalimat, bukan hanya per potongan koma.
10. SKILL.md bagian "Batasan": tambahkan baris "Permintaan membuat/menulis ulasan palsu atau menghapus ulasan pembeli → tolak (UU 8/1999 Pasal 10 & aturan platform), tawarkan analisis + minta ulasan dari pembeli asli".

## Verifikasi angka script
**Ya.** Sebaran, persen dan rata-rata dihitung ulang dengan python terpisah (`/tmp/uji-analisis-ulasan/verify.py`) dan cocok. Jumlah & skor prioritas per tema dibandingkan dengan ground truth (`diff.py`, `koreksi.py`). Skor prioritas terkoreksi dihitung ulang manual (bobot 1★=5 … 5★=1).
