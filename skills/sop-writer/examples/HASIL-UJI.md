# Hasil Uji – sop-writer

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/contoh-sop.md`, `references/panduan-bahasa-sop.md` (tidak ada script)
- **Metode:** 5 skenario dijalankan dengan berperan sebagai agent yang memuat SKILL.md dan mengikuti langkahnya persis, ditambah 1 uji A/B (S1 tanpa skill). Aturan "≤ 15 kata per langkah" diperiksa dengan penghitung kata (`awk`) pada setiap langkah bernomor di contoh 01–03. Langkah yang memuat dua tindakan dipecah atau ditulis ulang sebelum contoh difinalkan.

## Audit keamanan
Tidak ada script, perintah shell, akses jaringan, atau pembacaan kredensial. SKILL.md dan referensi tidak memuat prompt injection. Skill justru menambah perlindungan: menolak langkah yang melanggar hak karyawan (tahan KTP, potong gaji otomatis), menambah pengaman untuk praktik berisiko, mewajibkan langkah PDP untuk data pelanggan, dan mengingatkan bahwa SOP K3/pangan/medis harus merujuk standar resmi. **Aman.**

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B: S1 tanpa skill | Tanpa skill: kalimat panjang pasif, "bubble wrap secukupnya", target dikarang, tanpa checklist/tabel masalah/kontrol dokumen. Dengan skill **jelas lebih baik**. |
| 01 | SOP packing olshop skincare (botol pecah, salah varian) | Sangat baik. Masalah pengguna menjadi langkah ⚠️, ada checklist 11 butir, target berlabel usulan. |
| 02 | "bikinin dong" SOP buka warung kopi | Sangat baik. Langsung jadi dari praktik umum, dengan langkah K3 gas. Jam datang yang diasumsikan tidak diberi label di langkahnya. |
| 03 | Closing kasir laundry + minta potong gaji & tahan KTP | Sangat baik. Langkah melanggar ditolak dengan alasan, diganti kontrol (video + laporan WA). |
| 04 | "buatin SOP dong" | Sangat baik. Bertanya sekali (5 pertanyaan) dengan contoh jawaban. |
| 05 | Manual mutu ISO 9001 untuk sertifikasi | Sangat baik. Ditolak jujur, ditawari SOP operasional yang relevan. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Contoh pekerjaan konkret + kata kunci ID/EN (SOP, prosedur kerja, checklist harian, work instruction). |
| Kemudahan awam | 9 | Satu kalimat cukup. Checklist langsung dicetak. Tawaran versi poster. |
| Kualitas output | 9 | Format lengkap dan konsisten (9 bagian). Bahasa karyawan sangat sederhana, langkah ⚠️ beralasan. |
| Akurasi (angka/fakta) | 8 | Angka spesifik usaha tidak dikarang, dan target berlabel usulan. Belum ada referensi bersumber untuk batas hak karyawan dan K3 dasar. |
| Penanganan input kurang | 9 | Tanya sekali (≤ 5) dengan jalur cepat. Bila info wajib ada, langsung dibuat. |
| Penanganan di luar cakupan | 9 | ISO/manual mutu dan sertifikasi diarahkan dengan benar. Konsisten dengan README FAQ. |
| Keamanan | 10 | Tanpa script. Aktif melindungi karyawan dan data pelanggan. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Skill ini mengubah penjelasan lisan menjadi SOP yang benar-benar bisa dipraktikkan karyawan baru: langkah pendek, alasan untuk langkah kritis, tabel masalah, dan checklist harian. Uji A/B menunjukkan nilai tambah yang jelas dibanding SOP "formal" dari agent biasa. Tidak ada cacat berat atau sedang. Perbaikan ringan di bawah akan membuat hasilnya lebih konsisten.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- Tidak ada.

### Ringan
- **R1 – Contoh di referensi melanggar aturan "satu langkah = satu tindakan"** (`references/contoh-sop.md`: SOP Buka Toko langkah 3 "Buka pintu, nyalakan lampu dan kipas/AC", langkah 11 "Foto kondisi toko & laci, kirim ke grup WA"; SKILL.md contoh langkah 11 "Masukkan uang..., tulis tanggal & shift, simpan di brankas"). Agent meniru pola ini, dan pada uji awal contoh 01/02/03 beberapa langkah berisi 2 tindakan sehingga harus dirapikan. *Saran:* pecah langkah-langkah tersebut di SKILL.md dan contoh-sop.md, agar contoh selaras dengan aturan yang diajarkan.
- **R2 – Tidak ada konvensi pelaksana per langkah** bila ada lebih dari satu peran (contoh 01: admin mencetak resi, staf packing mengerjakan sisanya). *Saran:* tambahkan di `references/panduan-bahasa-sop.md`: "Jika pelaksana langkah berbeda dari pelaksana utama, tulis `(Peran)` di akhir langkah."
- **R3 – Jam yang diasumsikan tidak wajib diberi label** (SKILL.md tabel Input: "Jam/waktu pelaksanaan → `[isi jam]`"; contoh 02 menulis jam 06.15 hasil asumsi). *Saran:* samakan dengan aturan angka: "jam yang tidak disebut pengguna ditulis `[isi jam]` atau diberi label (usulan, sesuaikan)".
- **R4 – Tidak ada referensi bersumber untuk batas hak karyawan** (*Batasan* butir 3 melarang tahan KTP/ijazah dan potong gaji otomatis, tapi tanpa dasar aturan). Agent harus menjelaskan secara umum. *Saran:* tambahkan `references/batas-hak-karyawan.md` bertanggal, dengan sumber resmi (mis. ketentuan pengupahan untuk potongan gaji) dan tanda ⚠️ PERLU VERIFIKASI, lalu rujuk dari SKILL.md.
- **R5 – Privasi video/CCTV di SOP kasir/packing** tidak disinggung (SKILL.md *Batasan* PDP hanya untuk data pelanggan yang dicatat). *Saran:* tambahkan "Jika SOP memakai rekaman video, arahkan kamera ke area kerja (meja/uang/paket), simpan seperlunya, lalu hapus."
- **R6 – README merujuk `CARA-INSTAL.md`** dan ATTRIBUTION merujuk `LISENSI.txt`, dan keduanya tidak ada di folder skill. Pastikan keduanya ikut dalam paket rilis.

---
## Penyegaran contoh v1.0.6 (2026-10-17)
Penyegaran dokumentasi, **bukan uji ulang**: skor dan verdik di atas tidak berubah (8/10 LULUS, 2026-09-23).
- `01` diberi tampilan kanal chat v1.0.6 lengkap untuk SOP yang sama: 4 pesan berurutan "(1/4)–(4/4)", tanpa tabel Markdown, kontrol dokumen satu baris, jika-maka dan checklist sebagai baris, tanpa klaim "sudah dikirim" dan tanpa jalur berkas, berkas hanya ditawarkan ("balas 'kirim file'"). Dicek ulang: 21 langkah (semua ≤ 15 kata), 11 butir checklist, 4 baris jika-maka, 4 indikator, sama dengan isi lama; total ±4.200 karakter, jadi dipecah (tiap bagian < 3.500).
- `02`, `03`: catatan perubahan tampilan kanal chat (isi SOP tidak berubah). `05`: frasa "di luar cakupan skill ini" diganti tanpa menyebut skill. `04`: sudah sesuai.
- Skill tidak punya skrip; tidak ada angka uang baru yang ditulis.
- **Hasil bot Telegram asli v1.0.6:** `koordinasi/telegram-gelombang-A1-2026-10-17.md`, topik 1882/1883 (skenario 01) — TANPA 7,0 → DENGAN 8,5 (+1,5) **LULUS** (batas bawah). Pra-cek konteks Telegram: `koordinasi/pracek-telegram-akun-a-2026-10-16.md` (8, SIAP KIRIM).
